from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from amra.modeling.model_spec import _dict_value, _list_value


ML_THEORY_GATE_SCHEMA_VERSION = "amra.ml_theory_gate.v1"


@dataclass(slots=True)
class MLTheoryGateDecision:
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
class MLTheoryGateInput:
    claim_id: str
    statuses: list[str]
    decision: str
    checks: dict[str, Any]
    blockers: list[MLTheoryGateDecision] = field(default_factory=list)
    warnings: list[MLTheoryGateDecision] = field(default_factory=list)
    experiment_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": ML_THEORY_GATE_SCHEMA_VERSION,
            "claim_id": self.claim_id,
            "experiment_id": self.experiment_id,
            "statuses": list(self.statuses),
            "decision": self.decision,
            "checks": dict(self.checks),
            "blockers": [item.to_dict() for item in self.blockers],
            "warnings": [item.to_dict() for item in self.warnings],
            "approved": not self.blockers,
        }


def evaluate_ml_theory_gate(
    *,
    claim: dict[str, Any],
    experiment_manifest: dict[str, Any],
    dataset_ledger: list[dict[str, Any]],
    model_config_ledger: list[dict[str, Any]],
    training_config_ledger: list[dict[str, Any]],
    metric_schema: list[dict[str, Any]],
    scaling_probes: list[dict[str, Any]],
    optimization_probes: list[dict[str, Any]],
    theorem_empirical_boundary: dict[str, Any],
) -> MLTheoryGateInput:
    claim = _dict_value(claim)
    experiment_manifest = _dict_value(experiment_manifest)
    boundary = _dict_value(theorem_empirical_boundary)
    datasets = [dict(item) for item in dataset_ledger if isinstance(item, dict)]
    model_configs = [dict(item) for item in model_config_ledger if isinstance(item, dict)]
    training_configs = [dict(item) for item in training_config_ledger if isinstance(item, dict)]
    metrics = [dict(item) for item in metric_schema if isinstance(item, dict)]
    scaling_probes = [dict(item) for item in scaling_probes if isinstance(item, dict)]
    optimization_probes = [dict(item) for item in optimization_probes if isinstance(item, dict)]

    claim_id = str(claim.get("object_id") or claim.get("claim_id") or claim.get("id") or boundary.get("claim_id") or "")
    theorem_status = str(boundary.get("theorem_status") or "")
    theorem_like = theorem_status in {"proof", "proven", "theorem"}
    confidence = str(claim.get("confidence") or "")
    proof_artifact_ids = _list_value(boundary.get("proof_artifact_ids"))
    metric_failures = [item for item in metrics if item.get("passed") is False]
    finite_budget = bool(experiment_manifest.get("budget")) and all(
        value is not None for value in _dict_value(experiment_manifest.get("budget")).values()
    )

    checks = {
        "claim_declared": bool(claim_id) and bool(claim.get("statement") or claim.get("theoretical_statement")),
        "experiment_manifest_declared": bool(experiment_manifest.get("experiment_id")),
        "deterministic_manifest": bool(experiment_manifest.get("deterministic", False)),
        "seed_declared": experiment_manifest.get("seed") is not None,
        "finite_budget_declared": finite_budget,
        "dataset_ledger_declared": bool(datasets)
        and all(item.get("dataset_id") and item.get("role") and item.get("checksum") for item in datasets),
        "model_config_ledger_declared": bool(model_configs)
        and all(item.get("config_id") and item.get("architecture") for item in model_configs),
        "training_config_ledger_declared": bool(training_configs)
        and all(item.get("config_id") and item.get("model_config_id") and item.get("optimizer") for item in training_configs),
        "metric_schema_declared": bool(metrics)
        and all(item.get("metric_id") and item.get("name") and "value" in item and item.get("threshold") for item in metrics),
        "metrics_passed": bool(metrics) and not metric_failures,
        "scaling_probes_declared": bool(scaling_probes),
        "optimization_probes_declared": bool(optimization_probes),
        "boundary_declared": bool(boundary.get("boundary_id")) and bool(boundary.get("empirical_status")) and bool(theorem_status),
        "empirical_not_theorem_grade": not theorem_like
        and confidence != "theorem_grade"
        and bool(boundary.get("not_theorem_grade", True)),
        "proof_claim_has_proof_artifact": not theorem_like or bool(proof_artifact_ids),
    }
    checks["theorem_boundary_consistent"] = (
        checks["proof_claim_has_proof_artifact"] if theorem_like else checks["empirical_not_theorem_grade"]
    )

    blockers: list[MLTheoryGateDecision] = []
    warnings: list[MLTheoryGateDecision] = []
    _require(blockers, checks["claim_declared"], "missing_ml_theory_claim", "ML theory run requires a stated claim.")
    _require(blockers, checks["experiment_manifest_declared"], "missing_experiment_manifest", "Experiment manifest must be recorded.")
    _require(blockers, checks["deterministic_manifest"], "non_deterministic_manifest", "Fixture-backed ML theory experiments must be deterministic.")
    _require(blockers, checks["seed_declared"], "missing_seed", "Training or replay seed must be recorded.")
    _require(blockers, checks["finite_budget_declared"], "missing_finite_budget", "Experiment budget must be finite and explicit.")
    _require(blockers, checks["dataset_ledger_declared"], "missing_dataset_ledger", "Dataset ledger entries require id, role, and checksum.")
    _require(blockers, checks["model_config_ledger_declared"], "missing_model_config_ledger", "Model config ledger entries require id and architecture.")
    _require(blockers, checks["training_config_ledger_declared"], "missing_training_config_ledger", "Training config ledger entries require id, model config, and optimizer.")
    _require(blockers, checks["metric_schema_declared"], "missing_metric_schema", "Metric schema must include ids, values, and thresholds.")
    _require(blockers, checks["metrics_passed"], "metric_threshold_failed", "One or more ML theory metrics failed declared thresholds.", metadata={"failures": metric_failures})
    _require(blockers, checks["scaling_probes_declared"], "missing_scaling_probes", "Scaling probes must be recorded before theory promotion.")
    _require(blockers, checks["optimization_probes_declared"], "missing_optimization_probes", "Optimization probes must be recorded before theory promotion.")
    _require(blockers, checks["boundary_declared"], "missing_theorem_empirical_boundary", "The theorem/empirical boundary must be explicit.")
    _require(
        blockers,
        checks["theorem_boundary_consistent"],
        "empirical_claim_misclassified_as_theorem",
        "Empirical ML theory evidence must not be promoted to theorem-grade proof without proof artifacts.",
        metadata={"theorem_status": theorem_status, "confidence": confidence, "proof_artifact_ids": list(proof_artifact_ids)},
    )

    if checks["boundary_declared"] and not blockers:
        warnings.append(
            MLTheoryGateDecision(
                code="bounded_empirical_evidence_not_proof",
                message="Scaling and optimization probes support the claim empirically but do not establish a theorem.",
                blocking=False,
                severity="medium",
                metadata={"theorem_status": theorem_status, "empirical_status": boundary.get("empirical_status")},
            )
        )

    statuses = [item.code for item in blockers] + [item.code for item in warnings]
    if not statuses:
        statuses.append("ml_theory_empirically_supported")
    decision = blockers[0].code if blockers else "ml_theory_empirically_supported"
    return MLTheoryGateInput(
        claim_id=claim_id,
        experiment_id=str(experiment_manifest.get("experiment_id") or ""),
        statuses=statuses,
        decision=decision,
        checks=checks,
        blockers=blockers,
        warnings=warnings,
    )


def _require(
    blockers: list[MLTheoryGateDecision],
    condition: bool,
    code: str,
    message: str,
    *,
    metadata: dict[str, Any] | None = None,
) -> None:
    if condition:
        return
    blockers.append(MLTheoryGateDecision(code=code, message=message, metadata=metadata or {}))
