from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from amra.modeling.calibration import CalibrationReport, ModelDatasetRef
from amra.modeling.model_spec import (
    AppliedModelSpec,
    ValidityRange,
    _dict_value,
    _list_value,
    _number,
    _string_list,
    slug,
)
from amra.modeling.sensitivity import SensitivityReport
from amra.orchestration.workstreams import utc_now_iso
from amra.portfolio_memory import write_json
from amra.research.objects import ModelRecord, ResearchConfidence, ResearchObjectStatus
from amra.research_review.model_validation_gate import evaluate_model_validation_gate, numeric_threshold_passed


MODEL_VALIDATION_REPORT_SCHEMA_VERSION = "amra.model_validation_report.v1"
MODEL_VALIDATION_RUN_SCHEMA_VERSION = "amra.model_validation_run.v1"

MODEL_VALIDATION_RUN_FILE = "model_validation_run.json"
MODEL_SPEC_FILE = "model_spec.json"
MODEL_CALIBRATION_REPORT_FILE = "calibration_report.json"
MODEL_VALIDATION_REPORT_FILE = "validation_report.json"
MODEL_SENSITIVITY_REPORT_FILE = "sensitivity_report.json"
MODEL_FAILURE_MODE_LEDGER_FILE = "model_failure_modes.json"
MODEL_VALIDATION_GATE_INPUTS_FILE = "model_validation_gate_inputs.json"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(slots=True)
class ValidationMetricResult:
    name: str
    value: Any
    threshold: dict[str, Any] = field(default_factory=dict)
    passed: bool = True
    unit: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ValidationMetricResult":
        threshold = _dict_value(payload.get("threshold"))
        value = payload.get("value")
        passed = bool(payload.get("passed", True))
        if threshold:
            passed = numeric_threshold_passed(value, threshold)
        return cls(
            name=str(payload.get("name") or "metric"),
            value=value,
            threshold=threshold,
            passed=passed,
            unit=str(payload.get("unit") or ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "threshold": dict(self.threshold),
            "passed": self.passed,
            "unit": self.unit,
        }


@dataclass(slots=True)
class ValidationReport:
    validation_id: str
    model_id: str
    datasets: list[ModelDatasetRef] = field(default_factory=list)
    metrics: list[ValidationMetricResult] = field(default_factory=list)
    cases: list[dict[str, Any]] = field(default_factory=list)
    extrapolation_cases: list[dict[str, Any]] = field(default_factory=list)
    status: str = "validated"
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_payload(
        cls,
        payload: dict[str, Any],
        *,
        model_id: str,
        validity_ranges: list[ValidityRange],
    ) -> "ValidationReport":
        validation = _dict_value(payload.get("validation"))
        metrics = [
            ValidationMetricResult.from_dict(item)
            for item in _list_value(validation.get("metrics"))
            if isinstance(item, dict)
        ]
        cases = [dict(item) for item in _list_value(validation.get("cases")) if isinstance(item, dict)]
        extrapolation_cases = _extrapolation_cases(cases=cases, validity_ranges=validity_ranges)
        passed = bool(metrics) and all(item.passed for item in metrics)
        declared_status = str(validation.get("status") or "")
        if declared_status in {"failed", "needs_review"}:
            passed = False
        return cls(
            validation_id=str(validation.get("validation_id") or validation.get("id") or f"validation-{model_id}"),
            model_id=model_id,
            datasets=[
                ModelDatasetRef.from_dict(item, role="validation")
                for item in _list_value(validation.get("datasets") or validation.get("data"))
                if isinstance(item, dict)
            ],
            metrics=metrics,
            cases=cases,
            extrapolation_cases=extrapolation_cases,
            status="validated" if passed else "failed",
            notes=_string_list(validation.get("notes")),
        )

    @property
    def dataset_ids(self) -> list[str]:
        return [item.dataset_id for item in self.datasets]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": MODEL_VALIDATION_REPORT_SCHEMA_VERSION,
            "validation_id": self.validation_id,
            "model_id": self.model_id,
            "datasets": [item.to_dict() for item in self.datasets],
            "metrics": {item.name: item.to_dict() for item in self.metrics},
            "cases": [dict(item) for item in self.cases],
            "extrapolation_cases": [dict(item) for item in self.extrapolation_cases],
            "status": self.status,
            "notes": list(self.notes),
        }


class ModelValidationRunner:
    def run_fixture(self, *, fixture: Path, output_dir: Path) -> dict[str, Any]:
        fixture_path = fixture.expanduser().resolve()
        output_dir = output_dir.expanduser().resolve()
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("modeling fixture must be a JSON object")

        model_payload = _dict_value(payload.get("model") or payload.get("model_spec") or payload)
        model = AppliedModelSpec.from_dict(model_payload)
        calibration = CalibrationReport.from_payload(payload, model_id=model.object_id)
        validation = ValidationReport.from_payload(
            payload,
            model_id=model.object_id,
            validity_ranges=model.validity_ranges,
        )
        sensitivity = SensitivityReport.from_payload(payload, model_id=model.object_id)
        failure_modes = self._failure_modes(payload, validation=validation)

        model_spec_payload = model.to_dict()
        calibration_payload = calibration.to_dict()
        validation_payload = validation.to_dict()
        sensitivity_payload = sensitivity.to_dict()
        gate = evaluate_model_validation_gate(
            model_spec=model_spec_payload,
            calibration_report=calibration_payload,
            validation_report=validation_payload,
            sensitivity_report=sensitivity_payload,
            failure_modes=failure_modes,
        )
        model_record = self._model_record(
            model=model,
            calibration=calibration,
            validation=validation,
            sensitivity=sensitivity,
            failure_modes=failure_modes,
            gate_decision=gate.decision,
            gate_statuses=gate.statuses,
        )
        model_spec_payload["model_record"] = model_record.to_dict()
        gate_payload = gate.to_dict()

        output_dir.mkdir(parents=True, exist_ok=True)
        fixture_hash = _sha256_file(fixture_path)
        run = {
            "schema_version": MODEL_VALIDATION_RUN_SCHEMA_VERSION,
            "status": "succeeded" if gate_payload["approved"] else "needs_review",
            "generated_at": utc_now_iso(),
            "deterministic": True,
            "fixture": {"path": str(fixture_path), "sha256": fixture_hash},
            "output_dir": str(output_dir),
            "model": model_record.to_dict(),
            "model_spec": model_spec_payload,
            "calibration_report": calibration_payload,
            "validation_report": validation_payload,
            "sensitivity_report": sensitivity_payload,
            "failure_modes": failure_modes,
            "model_validation_gate_inputs": gate_payload,
            "record_files": {
                "run": str(output_dir / MODEL_VALIDATION_RUN_FILE),
                "model_spec": str(output_dir / MODEL_SPEC_FILE),
                "calibration_report": str(output_dir / MODEL_CALIBRATION_REPORT_FILE),
                "validation_report": str(output_dir / MODEL_VALIDATION_REPORT_FILE),
                "sensitivity_report": str(output_dir / MODEL_SENSITIVITY_REPORT_FILE),
                "failure_modes": str(output_dir / MODEL_FAILURE_MODE_LEDGER_FILE),
                "model_validation_gate_inputs": str(output_dir / MODEL_VALIDATION_GATE_INPUTS_FILE),
            },
        }

        write_json(output_dir / MODEL_SPEC_FILE, model_spec_payload)
        write_json(output_dir / MODEL_CALIBRATION_REPORT_FILE, calibration_payload)
        write_json(output_dir / MODEL_VALIDATION_REPORT_FILE, validation_payload)
        write_json(output_dir / MODEL_SENSITIVITY_REPORT_FILE, sensitivity_payload)
        write_json(output_dir / MODEL_FAILURE_MODE_LEDGER_FILE, failure_modes)
        write_json(output_dir / MODEL_VALIDATION_GATE_INPUTS_FILE, gate_payload)
        write_json(output_dir / MODEL_VALIDATION_RUN_FILE, run)
        return run

    def _failure_modes(self, payload: dict[str, Any], *, validation: ValidationReport) -> list[dict[str, Any]]:
        declared = [dict(item) for item in _list_value(payload.get("failure_modes")) if isinstance(item, dict)]
        records: list[dict[str, Any]] = []
        for index, item in enumerate(declared):
            failure_mode = str(item.get("failure_mode") or item.get("mode") or f"failure-mode-{index + 1}")
            severity = str(item.get("severity") or "medium")
            records.append(
                {
                    "failure_id": str(item.get("failure_id") or item.get("id") or f"failure-{slug(failure_mode)}"),
                    "failure_mode": failure_mode,
                    "description": str(item.get("description") or ""),
                    "severity": severity,
                    "mitigation": str(item.get("mitigation") or ""),
                    "gate_blocking": bool(item.get("gate_blocking", severity == "high")),
                }
            )
        if validation.extrapolation_cases:
            records.append(
                {
                    "failure_id": "failure-extrapolation",
                    "failure_mode": "extrapolation_outside_validity_range",
                    "description": "Some validation or claim inputs are outside declared validity ranges.",
                    "severity": "medium",
                    "mitigation": "Route extrapolated conclusions through model-validation review before promotion.",
                    "gate_blocking": False,
                    "cases": [dict(item) for item in validation.extrapolation_cases],
                }
            )
        return records

    def _model_record(
        self,
        *,
        model: AppliedModelSpec,
        calibration: CalibrationReport,
        validation: ValidationReport,
        sensitivity: SensitivityReport,
        failure_modes: list[dict[str, Any]],
        gate_decision: str,
        gate_statuses: list[str],
    ) -> ModelRecord:
        approved = gate_decision in {"model_validated", "model_validated_with_extrapolation_warning"}
        return ModelRecord(
            object_id=model.object_id,
            title=model.title,
            status=ResearchObjectStatus.MODEL_VALIDATED if approved else ResearchObjectStatus.TESTING,
            statement=model.statement,
            domain=model.domain,
            tags=sorted(set(["modeling", *model.tags])),
            confidence=ResearchConfidence.MEDIUM if approved else ResearchConfidence.LOW,
            application_domain=model.application_domain,
            variables=[item.name for item in model.variables],
            assumptions=[item.statement for item in model.assumptions],
            units=model.units,
            parameters={item.name: item.to_dict() for item in model.parameters},
            calibration_data=calibration.dataset_ids,
            validation_data=validation.dataset_ids,
            sensitivity_reports=[sensitivity.report_id] if sensitivity.scenarios else [],
            validity_range="; ".join(
                f"{item.variable}: {item.min_value}..{item.max_value} {item.unit}".strip()
                for item in model.validity_ranges
            ),
            validity_ranges=[item.to_dict() for item in model.validity_ranges],
            known_failure_modes=[str(item.get("failure_mode") or "") for item in failure_modes if item.get("failure_mode")],
            metadata={
                "model_validation_gate_decision": gate_decision,
                "model_validation_gate_statuses": list(gate_statuses),
                "calibration_id": calibration.calibration_id,
                "validation_id": validation.validation_id,
            },
        )


def _extrapolation_cases(*, cases: list[dict[str, Any]], validity_ranges: list[ValidityRange]) -> list[dict[str, Any]]:
    by_variable = {item.variable: item for item in validity_ranges if item.variable}
    extrapolations: list[dict[str, Any]] = []
    for case in cases:
        inputs = _dict_value(case.get("inputs"))
        for variable, value in inputs.items():
            validity = by_variable.get(str(variable))
            if validity is None or validity.contains(value):
                continue
            extrapolations.append(
                {
                    "case_id": str(case.get("case_id") or case.get("id") or "validation-case"),
                    "variable": str(variable),
                    "value": value,
                    "validity_range": validity.to_dict(),
                }
            )
    return extrapolations


def run_model_validation_fixture(*, fixture: Path, output_dir: Path) -> dict[str, Any]:
    return ModelValidationRunner().run_fixture(fixture=fixture, output_dir=output_dir)
