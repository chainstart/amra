from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


MODEL_VALIDATION_GATE_SCHEMA_VERSION = "amra.model_validation_gate.v1"


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list_value(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except ValueError:
        return None


@dataclass(slots=True)
class ModelValidationGateDecision:
    code: str
    message: str
    blocking: bool = True
    severity: str = "high"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "blocking": self.blocking,
            "severity": self.severity,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ModelValidationGateInput:
    model_id: str
    statuses: list[str]
    decision: str
    checks: dict[str, Any]
    blockers: list[ModelValidationGateDecision] = field(default_factory=list)
    warnings: list[ModelValidationGateDecision] = field(default_factory=list)
    validation_report_id: str = ""
    sensitivity_report_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": MODEL_VALIDATION_GATE_SCHEMA_VERSION,
            "model_id": self.model_id,
            "statuses": list(self.statuses),
            "decision": self.decision,
            "checks": dict(self.checks),
            "blockers": [item.to_dict() for item in self.blockers],
            "warnings": [item.to_dict() for item in self.warnings],
            "validation_report_id": self.validation_report_id,
            "sensitivity_report_id": self.sensitivity_report_id,
            "approved": not self.blockers,
        }


def evaluate_model_validation_gate(
    *,
    model_spec: dict[str, Any],
    calibration_report: dict[str, Any],
    validation_report: dict[str, Any],
    sensitivity_report: dict[str, Any],
    failure_modes: list[dict[str, Any]] | None = None,
) -> ModelValidationGateInput:
    variables = [item for item in _list_value(model_spec.get("variables")) if isinstance(item, dict)]
    assumptions = [item for item in _list_value(model_spec.get("assumptions")) if isinstance(item, dict)]
    parameters = [item for item in _list_value(model_spec.get("parameters")) if isinstance(item, dict)]
    validity_ranges = [item for item in _list_value(model_spec.get("validity_ranges")) if isinstance(item, dict)]
    calibration_datasets = {
        str(item.get("dataset_id"))
        for item in _list_value(calibration_report.get("datasets"))
        if isinstance(item, dict) and item.get("dataset_id")
    }
    validation_datasets = {
        str(item.get("dataset_id"))
        for item in _list_value(validation_report.get("datasets"))
        if isinstance(item, dict) and item.get("dataset_id")
    }
    validation_metrics = _dict_value(validation_report.get("metrics"))
    scenarios = [item for item in _list_value(sensitivity_report.get("scenarios")) if isinstance(item, dict)]
    extrapolation_cases = [
        item for item in _list_value(validation_report.get("extrapolation_cases")) if isinstance(item, dict)
    ]
    failure_modes = failure_modes or []

    checks = {
        "variables_declared": bool(variables),
        "units_declared": bool(variables) and all(str(item.get("unit") or "") for item in variables),
        "assumptions_declared": bool(assumptions) and all(str(item.get("statement") or "") for item in assumptions),
        "validity_ranges_declared": bool(validity_ranges),
        "parameters_traceable": bool(parameters)
        and all(str(item.get("source") or item.get("calibration_method") or "") for item in parameters),
        "calibration_data_declared": bool(calibration_datasets),
        "validation_data_declared": bool(validation_datasets),
        "calibration_validation_separated": bool(calibration_datasets)
        and bool(validation_datasets)
        and calibration_datasets.isdisjoint(validation_datasets),
        "validation_metrics_declared": bool(validation_metrics),
        "validation_passed": str(validation_report.get("status") or "") == "validated",
        "sensitivity_report_declared": bool(scenarios),
        "failure_modes_recorded": bool(failure_modes),
        "extrapolation_detected": bool(extrapolation_cases),
    }

    blockers: list[ModelValidationGateDecision] = []
    warnings: list[ModelValidationGateDecision] = []

    _require(blockers, checks["variables_declared"], "missing_variables", "Model must declare variables.")
    _require(blockers, checks["units_declared"], "missing_units", "Every model variable must declare a unit.")
    _require(blockers, checks["assumptions_declared"], "missing_assumptions", "Model must declare assumptions.")
    _require(
        blockers,
        checks["validity_ranges_declared"],
        "missing_validity_ranges",
        "Model must declare validity ranges before promotion.",
    )
    _require(
        blockers,
        checks["parameters_traceable"],
        "untraceable_parameters",
        "Every parameter must identify a source or calibration method.",
    )
    _require(
        blockers,
        checks["calibration_data_declared"],
        "missing_calibration_data",
        "Calibration data must be recorded separately.",
    )
    _require(
        blockers,
        checks["validation_data_declared"],
        "missing_validation_data",
        "Validation data must be recorded separately.",
    )
    _require(
        blockers,
        checks["calibration_validation_separated"],
        "calibration_validation_overlap",
        "Calibration and validation datasets must be disjoint.",
        metadata={"overlap": sorted(calibration_datasets & validation_datasets)},
    )
    _require(
        blockers,
        checks["validation_metrics_declared"],
        "missing_validation_metrics",
        "Validation metrics must be recorded.",
    )
    _require(
        blockers,
        checks["validation_passed"],
        "validation_failed",
        "Validation metrics did not satisfy declared thresholds.",
        metadata={"metrics": validation_metrics},
    )
    _require(
        blockers,
        checks["sensitivity_report_declared"],
        "missing_sensitivity_report",
        "Sensitivity analysis must be recorded.",
    )

    if checks["extrapolation_detected"]:
        warnings.append(
            ModelValidationGateDecision(
                code="extrapolation_risk",
                message="Validation or claimed inputs include values outside declared validity ranges.",
                blocking=False,
                severity="medium",
                metadata={"cases": extrapolation_cases},
            )
        )

    for item in failure_modes:
        if bool(item.get("gate_blocking")):
            blockers.append(
                ModelValidationGateDecision(
                    code=str(item.get("failure_mode") or item.get("mode") or "model_failure_mode"),
                    message=str(item.get("description") or "A model failure mode blocks validation."),
                    blocking=True,
                    severity=str(item.get("severity") or "high"),
                    metadata=dict(item),
                )
            )

    statuses = [item.code for item in blockers] + [item.code for item in warnings]
    if not statuses:
        statuses.append("model_validated")
    decision = "model_validated" if not blockers else blockers[0].code
    if not blockers and checks["extrapolation_detected"]:
        decision = "model_validated_with_extrapolation_warning"

    return ModelValidationGateInput(
        model_id=str(model_spec.get("object_id") or model_spec.get("model_id") or ""),
        statuses=statuses,
        decision=decision,
        checks=checks,
        blockers=blockers,
        warnings=warnings,
        validation_report_id=str(validation_report.get("validation_id") or validation_report.get("report_id") or ""),
        sensitivity_report_id=str(sensitivity_report.get("report_id") or ""),
    )


def _require(
    blockers: list[ModelValidationGateDecision],
    condition: bool,
    code: str,
    message: str,
    *,
    metadata: dict[str, Any] | None = None,
) -> None:
    if condition:
        return
    blockers.append(ModelValidationGateDecision(code=code, message=message, metadata=metadata or {}))


def numeric_threshold_passed(value: Any, threshold: dict[str, Any]) -> bool:
    number = _number(value)
    if number is None:
        return False
    if threshold.get("max") is not None and number > float(threshold["max"]):
        return False
    if threshold.get("min") is not None and number < float(threshold["min"]):
        return False
    return True
