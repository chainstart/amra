from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from amra.modeling.model_spec import _dict_value, _list_value, _number, _string_list, slug
from amra.orchestration.workstreams import utc_now_iso
from amra.portfolio_memory import write_json
from amra.research.objects import (
    MLTheoryClaimRecord,
    ResearchConfidence,
    ResearchObjectStatus,
)
from amra.research_review.ml_theory_gate import evaluate_ml_theory_gate


ML_THEORY_CLAIM_SCHEMA_VERSION = "amra.ml_theory_claim.v1"
ML_THEORY_EXPERIMENT_MANIFEST_SCHEMA_VERSION = "amra.ml_theory_experiment_manifest.v1"
ML_THEORY_METRIC_SCHEMA_VERSION = "amra.ml_theory_metric_schema.v1"
ML_THEORY_RUN_SCHEMA_VERSION = "amra.ml_theory_run.v1"

ML_THEORY_RUN_FILE = "ml_theory_run.json"
ML_THEORY_CLAIM_RECORD_FILE = "ml_theory_claim_record.json"
ML_THEORY_EXPERIMENT_MANIFEST_FILE = "experiment_manifest.json"
ML_THEORY_DATASET_LEDGER_FILE = "dataset_ledger.json"
ML_THEORY_MODEL_CONFIG_LEDGER_FILE = "model_config_ledger.json"
ML_THEORY_TRAINING_CONFIG_LEDGER_FILE = "training_config_ledger.json"
ML_THEORY_METRIC_SCHEMA_FILE = "metric_schema.json"
ML_THEORY_SCALING_PROBES_FILE = "scaling_probes.json"
ML_THEORY_OPTIMIZATION_PROBES_FILE = "optimization_probes.json"
ML_THEORY_BOUNDARY_FILE = "theorem_empirical_boundary.json"
ML_THEORY_GATE_INPUTS_FILE = "ml_theory_gate_inputs.json"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _threshold_passed(value: Any, threshold: dict[str, Any]) -> bool:
    number = _number(value)
    if number is None:
        return False
    if threshold.get("max") is not None and number > float(threshold["max"]):
        return False
    if threshold.get("min") is not None and number < float(threshold["min"]):
        return False
    return True


@dataclass(slots=True)
class MLDatasetLedgerEntry:
    dataset_id: str
    role: str
    source: str = ""
    split: str = ""
    rows: int = 0
    checksum: str = ""
    preprocessing: list[str] = field(default_factory=list)
    license: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MLDatasetLedgerEntry":
        return cls(
            dataset_id=str(payload.get("dataset_id") or payload.get("id") or "dataset"),
            role=str(payload.get("role") or "train"),
            source=str(payload.get("source") or ""),
            split=str(payload.get("split") or payload.get("role") or ""),
            rows=int(_number(payload.get("rows")) or 0),
            checksum=str(payload.get("checksum") or ""),
            preprocessing=_string_list(payload.get("preprocessing")),
            license=str(payload.get("license") or ""),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "role": self.role,
            "source": self.source,
            "split": self.split,
            "rows": self.rows,
            "checksum": self.checksum,
            "preprocessing": list(self.preprocessing),
            "license": self.license,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class MLModelConfigEntry:
    config_id: str
    architecture: str
    parameter_count: int = 0
    width: int = 0
    depth: int = 0
    initialization: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MLModelConfigEntry":
        return cls(
            config_id=str(payload.get("config_id") or payload.get("id") or "model-config"),
            architecture=str(payload.get("architecture") or payload.get("model") or ""),
            parameter_count=int(_number(payload.get("parameter_count") or payload.get("parameters")) or 0),
            width=int(_number(payload.get("width")) or 0),
            depth=int(_number(payload.get("depth")) or 0),
            initialization=str(payload.get("initialization") or ""),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_id": self.config_id,
            "architecture": self.architecture,
            "parameter_count": self.parameter_count,
            "width": self.width,
            "depth": self.depth,
            "initialization": self.initialization,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class MLTrainingConfigEntry:
    config_id: str
    model_config_id: str
    dataset_ids: list[str] = field(default_factory=list)
    optimizer: str = ""
    loss: str = ""
    seed: int | str | None = None
    epochs: int = 0
    batch_size: int = 0
    learning_rate: float | None = None
    budget: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MLTrainingConfigEntry":
        return cls(
            config_id=str(payload.get("config_id") or payload.get("id") or "training-config"),
            model_config_id=str(payload.get("model_config_id") or ""),
            dataset_ids=_string_list(payload.get("dataset_ids")),
            optimizer=str(payload.get("optimizer") or ""),
            loss=str(payload.get("loss") or ""),
            seed=payload.get("seed"),
            epochs=int(_number(payload.get("epochs")) or 0),
            batch_size=int(_number(payload.get("batch_size")) or 0),
            learning_rate=_number(payload.get("learning_rate") or payload.get("lr")),
            budget=_dict_value(payload.get("budget")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_id": self.config_id,
            "model_config_id": self.model_config_id,
            "dataset_ids": list(self.dataset_ids),
            "optimizer": self.optimizer,
            "loss": self.loss,
            "seed": self.seed,
            "epochs": self.epochs,
            "batch_size": self.batch_size,
            "learning_rate": self.learning_rate,
            "budget": dict(self.budget),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class MLTheoryMetric:
    metric_id: str
    name: str
    value: Any
    threshold: dict[str, Any] = field(default_factory=dict)
    direction: str = "lower_is_better"
    unit: str = ""
    dataset_id: str = ""
    passed: bool = True

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MLTheoryMetric":
        threshold = _dict_value(payload.get("threshold"))
        value = payload.get("value")
        return cls(
            metric_id=str(payload.get("metric_id") or payload.get("id") or slug(str(payload.get("name") or "metric"))),
            name=str(payload.get("name") or "metric"),
            value=value,
            threshold=threshold,
            direction=str(payload.get("direction") or "lower_is_better"),
            unit=str(payload.get("unit") or ""),
            dataset_id=str(payload.get("dataset_id") or ""),
            passed=_threshold_passed(value, threshold) if threshold else bool(payload.get("passed", True)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": ML_THEORY_METRIC_SCHEMA_VERSION,
            "metric_id": self.metric_id,
            "name": self.name,
            "value": self.value,
            "threshold": dict(self.threshold),
            "direction": self.direction,
            "unit": self.unit,
            "dataset_id": self.dataset_id,
            "passed": self.passed,
        }


@dataclass(slots=True)
class MLTheoryExperimentManifest:
    experiment_id: str
    title: str
    claim_id: str
    question: str = ""
    seed: int | str | None = None
    deterministic: bool = True
    dataset_ids: list[str] = field(default_factory=list)
    model_config_ids: list[str] = field(default_factory=list)
    training_config_ids: list[str] = field(default_factory=list)
    metric_ids: list[str] = field(default_factory=list)
    budget: dict[str, Any] = field(default_factory=dict)
    environment: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any], *, claim_id: str) -> "MLTheoryExperimentManifest":
        experiment_id = str(payload.get("experiment_id") or payload.get("id") or f"experiment-{claim_id}")
        return cls(
            experiment_id=experiment_id,
            title=str(payload.get("title") or experiment_id),
            claim_id=str(payload.get("claim_id") or claim_id),
            question=str(payload.get("question") or ""),
            seed=payload.get("seed"),
            deterministic=bool(payload.get("deterministic", True)),
            dataset_ids=_string_list(payload.get("dataset_ids")),
            model_config_ids=_string_list(payload.get("model_config_ids")),
            training_config_ids=_string_list(payload.get("training_config_ids")),
            metric_ids=_string_list(payload.get("metric_ids")),
            budget=_dict_value(payload.get("budget")),
            environment=_dict_value(payload.get("environment")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": ML_THEORY_EXPERIMENT_MANIFEST_SCHEMA_VERSION,
            "experiment_id": self.experiment_id,
            "title": self.title,
            "claim_id": self.claim_id,
            "question": self.question,
            "seed": self.seed,
            "deterministic": self.deterministic,
            "dataset_ids": list(self.dataset_ids),
            "model_config_ids": list(self.model_config_ids),
            "training_config_ids": list(self.training_config_ids),
            "metric_ids": list(self.metric_ids),
            "budget": dict(self.budget),
            "environment": dict(self.environment),
        }


class MLTheoryExperimentRunner:
    def run_fixture(self, *, fixture: Path, output_dir: Path) -> dict[str, Any]:
        fixture_path = fixture.expanduser().resolve()
        output_dir = output_dir.expanduser().resolve()
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("ML theory fixture must be a JSON object")

        claim_payload = _dict_value(payload.get("claim"))
        claim_id = str(claim_payload.get("object_id") or claim_payload.get("claim_id") or claim_payload.get("id") or "ml-theory-claim")
        manifest = MLTheoryExperimentManifest.from_dict(
            _dict_value(payload.get("experiment_manifest") or payload.get("manifest")),
            claim_id=claim_id,
        )
        datasets = [MLDatasetLedgerEntry.from_dict(item) for item in _list_value(payload.get("datasets")) if isinstance(item, dict)]
        model_configs = [MLModelConfigEntry.from_dict(item) for item in _list_value(payload.get("model_configs")) if isinstance(item, dict)]
        training_configs = [
            MLTrainingConfigEntry.from_dict(item)
            for item in _list_value(payload.get("training_configs"))
            if isinstance(item, dict)
        ]
        metrics = [MLTheoryMetric.from_dict(item) for item in _list_value(payload.get("metrics")) if isinstance(item, dict)]
        scaling_probes = [dict(item) for item in _list_value(payload.get("scaling_probes")) if isinstance(item, dict)]
        optimization_probes = [dict(item) for item in _list_value(payload.get("optimization_probes")) if isinstance(item, dict)]
        boundary = self._boundary(payload=payload, claim_id=claim_id)

        manifest.dataset_ids = manifest.dataset_ids or [item.dataset_id for item in datasets]
        manifest.model_config_ids = manifest.model_config_ids or [item.config_id for item in model_configs]
        manifest.training_config_ids = manifest.training_config_ids or [item.config_id for item in training_configs]
        manifest.metric_ids = manifest.metric_ids or [item.metric_id for item in metrics]

        gate = evaluate_ml_theory_gate(
            claim=claim_payload,
            experiment_manifest=manifest.to_dict(),
            dataset_ledger=[item.to_dict() for item in datasets],
            model_config_ledger=[item.to_dict() for item in model_configs],
            training_config_ledger=[item.to_dict() for item in training_configs],
            metric_schema=[item.to_dict() for item in metrics],
            scaling_probes=scaling_probes,
            optimization_probes=optimization_probes,
            theorem_empirical_boundary=boundary,
        )
        gate_payload = gate.to_dict()
        claim_record = self._claim_record(
            claim_payload=claim_payload,
            manifest=manifest,
            metrics=metrics,
            boundary=boundary,
            gate_decision=gate.decision,
            gate_statuses=gate.statuses,
        )
        claim_record_payload = claim_record.to_dict()
        claim_record_payload["schema_version"] = ML_THEORY_CLAIM_SCHEMA_VERSION

        output_dir.mkdir(parents=True, exist_ok=True)
        fixture_hash = _sha256_file(fixture_path)
        run = {
            "schema_version": ML_THEORY_RUN_SCHEMA_VERSION,
            "status": "succeeded" if gate_payload["approved"] else "needs_review",
            "generated_at": utc_now_iso(),
            "deterministic": True,
            "fixture": {"path": str(fixture_path), "sha256": fixture_hash},
            "output_dir": str(output_dir),
            "claim": claim_record_payload,
            "experiment_manifest": manifest.to_dict(),
            "dataset_ledger": [item.to_dict() for item in datasets],
            "model_config_ledger": [item.to_dict() for item in model_configs],
            "training_config_ledger": [item.to_dict() for item in training_configs],
            "metric_schema": [item.to_dict() for item in metrics],
            "scaling_probes": scaling_probes,
            "optimization_probes": optimization_probes,
            "theorem_empirical_boundary": boundary,
            "ml_theory_gate_inputs": gate_payload,
            "record_files": {
                "run": str(output_dir / ML_THEORY_RUN_FILE),
                "claim": str(output_dir / ML_THEORY_CLAIM_RECORD_FILE),
                "experiment_manifest": str(output_dir / ML_THEORY_EXPERIMENT_MANIFEST_FILE),
                "dataset_ledger": str(output_dir / ML_THEORY_DATASET_LEDGER_FILE),
                "model_config_ledger": str(output_dir / ML_THEORY_MODEL_CONFIG_LEDGER_FILE),
                "training_config_ledger": str(output_dir / ML_THEORY_TRAINING_CONFIG_LEDGER_FILE),
                "metric_schema": str(output_dir / ML_THEORY_METRIC_SCHEMA_FILE),
                "scaling_probes": str(output_dir / ML_THEORY_SCALING_PROBES_FILE),
                "optimization_probes": str(output_dir / ML_THEORY_OPTIMIZATION_PROBES_FILE),
                "theorem_empirical_boundary": str(output_dir / ML_THEORY_BOUNDARY_FILE),
                "ml_theory_gate_inputs": str(output_dir / ML_THEORY_GATE_INPUTS_FILE),
            },
        }

        write_json(output_dir / ML_THEORY_CLAIM_RECORD_FILE, claim_record_payload)
        write_json(output_dir / ML_THEORY_EXPERIMENT_MANIFEST_FILE, manifest.to_dict())
        write_json(output_dir / ML_THEORY_DATASET_LEDGER_FILE, [item.to_dict() for item in datasets])
        write_json(output_dir / ML_THEORY_MODEL_CONFIG_LEDGER_FILE, [item.to_dict() for item in model_configs])
        write_json(output_dir / ML_THEORY_TRAINING_CONFIG_LEDGER_FILE, [item.to_dict() for item in training_configs])
        write_json(output_dir / ML_THEORY_METRIC_SCHEMA_FILE, [item.to_dict() for item in metrics])
        write_json(output_dir / ML_THEORY_SCALING_PROBES_FILE, scaling_probes)
        write_json(output_dir / ML_THEORY_OPTIMIZATION_PROBES_FILE, optimization_probes)
        write_json(output_dir / ML_THEORY_BOUNDARY_FILE, boundary)
        write_json(output_dir / ML_THEORY_GATE_INPUTS_FILE, gate_payload)
        write_json(output_dir / ML_THEORY_RUN_FILE, run)
        return run

    def _boundary(self, *, payload: dict[str, Any], claim_id: str) -> dict[str, Any]:
        boundary = _dict_value(payload.get("theorem_empirical_boundary") or payload.get("boundary"))
        return {
            "boundary_id": str(boundary.get("boundary_id") or f"boundary-{slug(claim_id)}"),
            "claim_id": str(boundary.get("claim_id") or claim_id),
            "empirical_status": str(boundary.get("empirical_status") or "bounded_empirical_support"),
            "theorem_status": str(boundary.get("theorem_status") or "not_theorem"),
            "proof_artifact_ids": _string_list(boundary.get("proof_artifact_ids")),
            "empirical_artifact_ids": _string_list(boundary.get("empirical_artifact_ids")),
            "requires_proof_for": _string_list(boundary.get("requires_proof_for")),
            "notes": _string_list(boundary.get("notes")),
            "not_theorem_grade": bool(boundary.get("not_theorem_grade", True)),
        }

    def _claim_record(
        self,
        *,
        claim_payload: dict[str, Any],
        manifest: MLTheoryExperimentManifest,
        metrics: list[MLTheoryMetric],
        boundary: dict[str, Any],
        gate_decision: str,
        gate_statuses: list[str],
    ) -> MLTheoryClaimRecord:
        claim_id = str(claim_payload.get("object_id") or claim_payload.get("claim_id") or claim_payload.get("id") or "ml-theory-claim")
        approved = gate_decision == "ml_theory_empirically_supported"
        return MLTheoryClaimRecord(
            object_id=claim_id,
            title=str(claim_payload.get("title") or claim_id),
            status=ResearchObjectStatus.EMPIRICALLY_SUPPORTED if approved else ResearchObjectStatus.TESTING,
            statement=str(claim_payload.get("statement") or ""),
            domain=str(claim_payload.get("domain") or "machine_learning_theory"),
            tags=sorted(set(["ml_theory", *_string_list(claim_payload.get("tags"))])),
            confidence=ResearchConfidence.MEDIUM if approved else ResearchConfidence.LOW,
            evidence_ids=_string_list(claim_payload.get("evidence_ids")),
            artifact_ids=[manifest.experiment_id, *[item.metric_id for item in metrics]],
            claim_kind=str(claim_payload.get("claim_kind") or "empirical_scaling_law"),
            training_setup={
                "experiment_id": manifest.experiment_id,
                "model_config_ids": list(manifest.model_config_ids),
                "training_config_ids": list(manifest.training_config_ids),
            },
            dataset_ids=list(manifest.dataset_ids),
            metric_ids=[item.metric_id for item in metrics],
            theoretical_statement=str(claim_payload.get("theoretical_statement") or ""),
            empirical_support=[manifest.experiment_id, *[item.metric_id for item in metrics if item.passed]],
            known_gaps=_string_list(claim_payload.get("known_gaps") or boundary.get("requires_proof_for")),
            promotion_target=str(claim_payload.get("promotion_target") or "conjecture"),
            metadata={
                "ml_theory_gate_decision": gate_decision,
                "ml_theory_gate_statuses": list(gate_statuses),
                "theorem_status": boundary["theorem_status"],
                "empirical_status": boundary["empirical_status"],
                "bounded_evidence_only": True,
            },
        )


def run_ml_theory_experiment_fixture(*, fixture: Path, output_dir: Path) -> dict[str, Any]:
    return MLTheoryExperimentRunner().run_fixture(fixture=fixture, output_dir=output_dir)
