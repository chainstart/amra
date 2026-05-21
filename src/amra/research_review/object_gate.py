from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from amra.orchestration.workstreams import utc_now_iso
from amra.portfolio_memory import write_json
from amra.research_review.ml_theory_gate import evaluate_ml_theory_gate
from amra.research_review.model_validation_gate import evaluate_model_validation_gate
from amra.research_review.security_gate import evaluate_security_gate


RESEARCH_OBJECT_REVIEW_SCHEMA_VERSION = "amra.research_object_review.v1"
RESEARCH_OBJECT_REVIEW_FIXTURE_SCHEMA_VERSION = "amra.research_object_review_fixture.v1"
RESEARCH_REVIEW_REPORT_FILE = "research_review_report.json"
RESEARCH_REVIEW_FIXTURE_COPY_FILE = "research_review_fixture.json"

RESEARCH_REVIEW_GATES = (
    "novelty",
    "reproducibility",
    "statistical",
    "benchmark",
    "model_validation",
    "security",
    "theory_coherence",
)

_PASSING_BENCHMARK_STATUSES = {"benchmark_passed", "passed", "approved"}
_PASSING_REPRO_STATUSES = {"reproducible", "rerun_passed", "passed", "succeeded", "reviewed"}
_DUPLICATE_NOVELTY_STATUSES = {"duplicate", "known_result", "not_novel", "superseded"}


@dataclass(slots=True)
class ResearchReviewFinding:
    code: str
    message: str
    gate: str = ""
    blocking: bool = True
    severity: str = "high"
    source_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "gate": self.gate,
            "blocking": self.blocking,
            "severity": self.severity,
            "source_id": self.source_id,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ResearchReviewGateResult:
    gate: str
    approved: bool
    decision: str
    checks: dict[str, Any]
    statuses: list[str] = field(default_factory=list)
    blockers: list[ResearchReviewFinding] = field(default_factory=list)
    warnings: list[ResearchReviewFinding] = field(default_factory=list)
    source_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.statuses = [str(item) for item in self.statuses]
        if not self.statuses:
            self.statuses = [self.decision]
        self.blockers = [
            item if isinstance(item, ResearchReviewFinding) else ResearchReviewFinding(**item)
            for item in self.blockers
        ]
        self.warnings = [
            item if isinstance(item, ResearchReviewFinding) else ResearchReviewFinding(**item)
            for item in self.warnings
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate": self.gate,
            "approved": self.approved,
            "decision": self.decision,
            "statuses": list(self.statuses),
            "checks": dict(self.checks),
            "blockers": [item.to_dict() for item in self.blockers],
            "warnings": [item.to_dict() for item in self.warnings],
            "source_id": self.source_id,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ResearchObjectReviewReport:
    object_id: str
    approved: bool
    decision: str
    gates: list[ResearchReviewGateResult]
    generated_at: str = field(default_factory=utc_now_iso)
    required_gates: list[str] = field(default_factory=list)
    object_type: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blockers = [finding.to_dict() for gate in self.gates for finding in gate.blockers]
        warnings = [finding.to_dict() for gate in self.gates for finding in gate.warnings]
        gate_decisions = {gate.gate: gate.decision for gate in self.gates}
        return {
            "schema_version": RESEARCH_OBJECT_REVIEW_SCHEMA_VERSION,
            "object_id": self.object_id,
            "object_type": self.object_type,
            "approved": self.approved,
            "decision": self.decision,
            "generated_at": self.generated_at,
            "required_gates": list(self.required_gates),
            "gate_decisions": gate_decisions,
            "gates": [gate.to_dict() for gate in self.gates],
            "blockers": blockers,
            "warnings": warnings,
            "blocking_decisions": [item for item in blockers if item.get("blocking")],
            "metadata": dict(self.metadata),
        }


def evaluate_research_object_review(payload: dict[str, Any]) -> ResearchObjectReviewReport:
    """Evaluate review gates for non-proof AMRA research claims.

    The aggregate gate is intentionally deterministic and fixture-friendly. It
    can consume raw gate inputs, or previously persisted gate payloads from the
    modeling/security/ML-theory packs.
    """

    if not isinstance(payload, dict):
        raise ValueError("research review payload must be a JSON object")
    research_object = _dict_value(
        payload.get("research_object")
        or payload.get("object")
        or payload.get("claim")
        or payload.get("algorithm")
        or payload.get("model")
    )
    object_id = str(
        research_object.get("object_id")
        or research_object.get("claim_id")
        or payload.get("object_id")
        or "research-object"
    )
    object_type = str(research_object.get("object_type") or payload.get("object_type") or "").strip()
    required_gates = _ordered_gates(payload.get("required_gates") or RESEARCH_REVIEW_GATES)

    gate_evaluators: dict[str, Callable[[dict[str, Any], dict[str, Any]], ResearchReviewGateResult]] = {
        "novelty": _evaluate_novelty_gate,
        "reproducibility": _evaluate_reproducibility_gate,
        "statistical": _evaluate_statistical_gate,
        "benchmark": _evaluate_benchmark_gate,
        "model_validation": _evaluate_model_validation_review_gate,
        "security": _evaluate_security_review_gate,
        "theory_coherence": _evaluate_theory_coherence_gate,
    }
    gates = [gate_evaluators[name](research_object, payload) for name in required_gates]
    approved = all(gate.approved for gate in gates)
    decision = "approved" if approved else "blocked"
    return ResearchObjectReviewReport(
        object_id=object_id,
        object_type=object_type,
        approved=approved,
        decision=decision,
        gates=gates,
        required_gates=required_gates,
        metadata={
            "fixture_schema_version": str(payload.get("schema_version") or ""),
            "non_proof_claim_review": True,
        },
    )


def run_research_review_fixture(*, fixture: Path, output_dir: Path) -> dict[str, Any]:
    fixture_path = fixture.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    report = evaluate_research_object_review(payload).to_dict()

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / RESEARCH_REVIEW_REPORT_FILE, report)
    if fixture_path != output_dir / RESEARCH_REVIEW_FIXTURE_COPY_FILE:
        shutil.copyfile(fixture_path, output_dir / RESEARCH_REVIEW_FIXTURE_COPY_FILE)
    return {
        **report,
        "output_dir": str(output_dir),
        "record_files": {
            "research_review_report": str(output_dir / RESEARCH_REVIEW_REPORT_FILE),
            "fixture": str(output_dir / RESEARCH_REVIEW_FIXTURE_COPY_FILE),
        },
    }


def _evaluate_novelty_gate(research_object: dict[str, Any], payload: dict[str, Any]) -> ResearchReviewGateResult:
    report = _dict_value(payload.get("novelty_report") or research_object.get("novelty_report"))
    compared_sources = _list_value(report.get("compared_sources") or report.get("sources_checked"))
    status = str(report.get("status") or report.get("decision") or "").strip().lower()
    known_prior_art = _list_value(report.get("known_prior_art") or report.get("related_work"))
    checks = {
        "novelty_report_declared": bool(report),
        "sources_compared": bool(compared_sources),
        "claim_delta_declared": bool(report.get("claim_delta") or report.get("novelty_summary") or report.get("delta")),
        "not_duplicate": status not in _DUPLICATE_NOVELTY_STATUSES,
    }
    blockers: list[ResearchReviewFinding] = []
    _require(blockers, "novelty", checks["novelty_report_declared"], "missing_novelty_report", "Novelty review requires a prior-art comparison.")
    _require(blockers, "novelty", checks["sources_compared"], "missing_prior_art_sources", "Novelty review must list compared sources.")
    _require(blockers, "novelty", checks["claim_delta_declared"], "missing_claim_delta", "Novelty review must describe the claim delta.")
    _require(
        blockers,
        "novelty",
        checks["not_duplicate"],
        "duplicate_claim",
        "The claim is marked as duplicate or already known.",
        metadata={"status": status, "known_prior_art": known_prior_art},
    )
    return _gate("novelty", blockers, checks, approved_decision="novelty_reviewed", source_id=str(report.get("report_id") or ""))


def _evaluate_reproducibility_gate(research_object: dict[str, Any], payload: dict[str, Any]) -> ResearchReviewGateResult:
    report = _dict_value(
        payload.get("reproducibility_report")
        or payload.get("research_reproducibility_report")
        or research_object.get("reproducibility_report")
    )
    experiment = _dict_value(payload.get("experiment") or payload.get("experiment_record"))
    status = str(report.get("status") or experiment.get("rerun_status") or "").strip().lower()
    command = report.get("command") or experiment.get("command") or payload.get("command")
    checks = {
        "reproducibility_report_declared": bool(report),
        "deterministic": bool(report.get("deterministic", experiment.get("deterministic", True))),
        "seed_declared": report.get("seed") is not None or experiment.get("seed") is not None,
        "environment_declared": bool(report.get("environment") or experiment.get("environment")),
        "command_or_checksum_declared": bool(command or report.get("request_hash") or report.get("fixture_sha256")),
        "rerun_passed": status in _PASSING_REPRO_STATUSES,
    }
    blockers: list[ResearchReviewFinding] = []
    _require(blockers, "reproducibility", checks["reproducibility_report_declared"], "missing_reproducibility_report", "Reproducibility review requires a persisted report.")
    _require(blockers, "reproducibility", checks["deterministic"], "non_deterministic_run", "Reproducibility review requires deterministic fixture-backed execution.")
    _require(blockers, "reproducibility", checks["seed_declared"], "missing_seed", "Reproducibility review requires a recorded seed.")
    _require(blockers, "reproducibility", checks["environment_declared"], "missing_environment", "Reproducibility review requires environment metadata.")
    _require(blockers, "reproducibility", checks["command_or_checksum_declared"], "missing_replay_contract", "Reproducibility review requires a replay command or checksum.")
    _require(blockers, "reproducibility", checks["rerun_passed"], "reproduction_not_passed", "The reproduction status has not passed.")
    return _gate("reproducibility", blockers, checks, approved_decision="reproducibility_reviewed", source_id=str(report.get("report_id") or ""))


def _evaluate_statistical_gate(research_object: dict[str, Any], payload: dict[str, Any]) -> ResearchReviewGateResult:
    stats = _dict_value(payload.get("statistical_evidence") or payload.get("statistics") or research_object.get("statistical_evidence"))
    metrics = [dict(item) for item in _list_value(stats.get("metrics")) if isinstance(item, dict)]
    min_sample_size = int(_number(stats.get("min_sample_size")) or 2)
    sample_size = int(_number(stats.get("sample_size") or stats.get("n")) or 0)
    metric_failures = [item for item in metrics if item.get("passed") is False]
    confidence = str(stats.get("confidence") or research_object.get("confidence") or "").strip().lower()
    checks = {
        "statistical_evidence_declared": bool(stats),
        "sample_size_sufficient": sample_size >= min_sample_size,
        "metrics_declared": bool(metrics),
        "metric_thresholds_declared": bool(metrics) and all(item.get("threshold") for item in metrics),
        "metrics_passed": bool(metrics) and not metric_failures,
        "uncertainty_declared": bool(stats.get("confidence_interval") or stats.get("p_value") is not None or stats.get("stddev") is not None or stats.get("bootstrap")),
        "not_theorem_grade": confidence != "theorem_grade",
    }
    blockers: list[ResearchReviewFinding] = []
    _require(blockers, "statistical", checks["statistical_evidence_declared"], "missing_statistical_evidence", "Statistical claims require statistical evidence.")
    _require(blockers, "statistical", checks["sample_size_sufficient"], "insufficient_sample_size", "Statistical evidence must meet the declared minimum sample size.", metadata={"sample_size": sample_size, "min_sample_size": min_sample_size})
    _require(blockers, "statistical", checks["metrics_declared"], "missing_statistical_metrics", "Statistical evidence must declare metrics.")
    _require(blockers, "statistical", checks["metric_thresholds_declared"], "missing_metric_thresholds", "Statistical metrics must declare thresholds.")
    _require(blockers, "statistical", checks["metrics_passed"], "statistical_threshold_failed", "One or more statistical thresholds failed.", metadata={"failures": metric_failures})
    _require(blockers, "statistical", checks["uncertainty_declared"], "missing_uncertainty", "Statistical evidence must record uncertainty.")
    _require(blockers, "statistical", checks["not_theorem_grade"], "statistical_claim_misclassified_as_proof", "Statistical evidence cannot be marked theorem-grade.")
    return _gate("statistical", blockers, checks, approved_decision="statistical_reviewed", source_id=str(stats.get("evidence_id") or ""))


def _evaluate_benchmark_gate(research_object: dict[str, Any], payload: dict[str, Any]) -> ResearchReviewGateResult:
    benchmark = _dict_value(payload.get("benchmark_gate") or payload.get("benchmark_gate_inputs") or research_object.get("benchmark_gate"))
    checks_payload = _dict_value(benchmark.get("checks"))
    statuses = [str(item) for item in _list_value(benchmark.get("statuses"))]
    decision = str(benchmark.get("decision") or "").strip()
    checks = {
        "benchmark_gate_declared": bool(benchmark),
        "benchmark_passed": decision in _PASSING_BENCHMARK_STATUSES or any(item in _PASSING_BENCHMARK_STATUSES for item in statuses),
        "fixed_benchmark": bool(checks_payload.get("benchmark_fixed", True)),
        "baseline_fair": bool(checks_payload.get("baseline_fair", True)),
        "metric_valid": bool(checks_payload.get("metric_valid", True)),
        "traceable_to_baseline": bool(checks_payload.get("traceable_to_baseline", True)),
        "no_blocking_regressions": int(_number(checks_payload.get("regression_count")) or 0) == 0,
    }
    blockers: list[ResearchReviewFinding] = []
    _require(blockers, "benchmark", checks["benchmark_gate_declared"], "missing_benchmark_gate", "Benchmark claims require benchmark gate inputs.")
    _require(blockers, "benchmark", checks["benchmark_passed"], "benchmark_not_passed", "Benchmark gate has not passed.", metadata={"decision": decision, "statuses": statuses})
    _require(blockers, "benchmark", checks["fixed_benchmark"], "benchmark_not_fixed", "Benchmark inputs must be fixed before review.")
    _require(blockers, "benchmark", checks["baseline_fair"], "baseline_unfair", "Benchmark candidates must use a fair baseline.")
    _require(blockers, "benchmark", checks["metric_valid"], "metric_invalid", "Benchmark metric must be declared and present.")
    _require(blockers, "benchmark", checks["traceable_to_baseline"], "baseline_not_traceable", "Benchmark candidates must be traceable to a baseline.")
    _require(blockers, "benchmark", checks["no_blocking_regressions"], "benchmark_regression", "Blocking benchmark regressions remain unresolved.")
    return _gate("benchmark", blockers, checks, approved_decision="benchmark_reviewed", source_id=str(benchmark.get("benchmark_id") or ""))


def _evaluate_model_validation_review_gate(research_object: dict[str, Any], payload: dict[str, Any]) -> ResearchReviewGateResult:
    raw_gate = _dict_value(payload.get("model_validation_gate") or payload.get("model_validation_gate_inputs"))
    if raw_gate:
        return _from_domain_gate("model_validation", raw_gate, approved_decision="model_validation_reviewed")
    inputs = _dict_value(payload.get("model_validation"))
    if not inputs:
        return _missing_domain_gate("model_validation", "missing_model_validation_gate", "Model claims require model-validation gate inputs.")
    gate = evaluate_model_validation_gate(
        model_spec=_dict_value(inputs.get("model_spec")),
        calibration_report=_dict_value(inputs.get("calibration_report")),
        validation_report=_dict_value(inputs.get("validation_report")),
        sensitivity_report=_dict_value(inputs.get("sensitivity_report")),
        failure_modes=[dict(item) for item in _list_value(inputs.get("failure_modes")) if isinstance(item, dict)],
    ).to_dict()
    return _from_domain_gate("model_validation", gate, approved_decision="model_validation_reviewed")


def _evaluate_security_review_gate(research_object: dict[str, Any], payload: dict[str, Any]) -> ResearchReviewGateResult:
    raw_gate = _dict_value(payload.get("security_gate") or payload.get("security_gate_inputs"))
    if raw_gate:
        return _from_domain_gate("security", raw_gate, approved_decision="security_reviewed")
    inputs = _dict_value(payload.get("security"))
    if not inputs:
        return _missing_domain_gate("security", "missing_security_gate", "Security claims require security gate inputs.")
    gate = evaluate_security_gate(
        threat_model=_dict_value(inputs.get("threat_model")),
        security_game=_dict_value(inputs.get("security_game")),
        assumptions=[dict(item) for item in _list_value(inputs.get("assumptions")) if isinstance(item, dict)],
        reductions=[dict(item) for item in _list_value(inputs.get("reductions")) if isinstance(item, dict)],
        attack_report=_dict_value(inputs.get("attack_report")),
        evidence=_dict_value(inputs.get("evidence")),
    ).to_dict()
    return _from_domain_gate("security", gate, approved_decision="security_reviewed")


def _evaluate_theory_coherence_gate(research_object: dict[str, Any], payload: dict[str, Any]) -> ResearchReviewGateResult:
    context = _dict_value(payload.get("theory_coherence") or payload.get("theory_context") or research_object.get("theory_context"))
    dependencies = [dict(item) for item in _list_value(context.get("dependencies")) if isinstance(item, dict)]
    contradictions = _list_value(context.get("contradictions"))
    unresolved_gaps = _list_value(context.get("unresolved_gaps"))
    checks = {
        "theory_context_declared": bool(context),
        "definitions_declared": bool(_list_value(context.get("definitions"))),
        "assumptions_declared": bool(_list_value(context.get("assumptions"))),
        "dependencies_reviewed": bool(dependencies) and all(bool(item.get("reviewed", True)) for item in dependencies),
        "no_known_contradictions": not contradictions,
        "scope_declared": bool(context.get("scope") or research_object.get("scope")),
        "no_unresolved_blocking_gaps": not unresolved_gaps,
    }
    blockers: list[ResearchReviewFinding] = []
    _require(blockers, "theory_coherence", checks["theory_context_declared"], "missing_theory_context", "Theory coherence review requires context.")
    _require(blockers, "theory_coherence", checks["definitions_declared"], "missing_definitions", "Theory coherence review requires definitions.")
    _require(blockers, "theory_coherence", checks["assumptions_declared"], "missing_assumptions", "Theory coherence review requires assumptions.")
    _require(blockers, "theory_coherence", checks["dependencies_reviewed"], "unreviewed_dependencies", "Theory dependencies must be reviewed.", metadata={"dependencies": dependencies})
    _require(blockers, "theory_coherence", checks["no_known_contradictions"], "known_contradiction", "Known theory contradictions block promotion.", metadata={"contradictions": contradictions})
    _require(blockers, "theory_coherence", checks["scope_declared"], "missing_scope", "Theory coherence review requires a declared scope.")
    _require(blockers, "theory_coherence", checks["no_unresolved_blocking_gaps"], "unresolved_theory_gap", "Unresolved theory gaps block promotion.", metadata={"unresolved_gaps": unresolved_gaps})

    ml_theory_gate = _dict_value(payload.get("ml_theory_gate") or payload.get("ml_theory_gate_inputs"))
    if not ml_theory_gate and isinstance(context.get("ml_theory"), dict):
        ml_inputs = _dict_value(context.get("ml_theory"))
        ml_theory_gate = evaluate_ml_theory_gate(
            claim=_dict_value(ml_inputs.get("claim")),
            experiment_manifest=_dict_value(ml_inputs.get("experiment_manifest")),
            dataset_ledger=[dict(item) for item in _list_value(ml_inputs.get("dataset_ledger")) if isinstance(item, dict)],
            model_config_ledger=[dict(item) for item in _list_value(ml_inputs.get("model_config_ledger")) if isinstance(item, dict)],
            training_config_ledger=[dict(item) for item in _list_value(ml_inputs.get("training_config_ledger")) if isinstance(item, dict)],
            metric_schema=[dict(item) for item in _list_value(ml_inputs.get("metric_schema")) if isinstance(item, dict)],
            scaling_probes=[dict(item) for item in _list_value(ml_inputs.get("scaling_probes")) if isinstance(item, dict)],
            optimization_probes=[dict(item) for item in _list_value(ml_inputs.get("optimization_probes")) if isinstance(item, dict)],
            theorem_empirical_boundary=_dict_value(ml_inputs.get("theorem_empirical_boundary")),
        ).to_dict()
    if ml_theory_gate and not bool(ml_theory_gate.get("approved")):
        blockers.append(
            ResearchReviewFinding(
                gate="theory_coherence",
                code="ml_theory_gate_blocked",
                message="The ML theory sub-gate blocks theory coherence review.",
                metadata={"decision": ml_theory_gate.get("decision"), "statuses": _list_value(ml_theory_gate.get("statuses"))},
            )
        )
    return _gate(
        "theory_coherence",
        blockers,
        checks,
        approved_decision="theory_coherence_reviewed",
        source_id=str(context.get("context_id") or ""),
        metadata={"ml_theory_gate": ml_theory_gate} if ml_theory_gate else {},
    )


def _from_domain_gate(gate_name: str, payload: dict[str, Any], *, approved_decision: str) -> ResearchReviewGateResult:
    blockers = [
        ResearchReviewFinding(
            gate=gate_name,
            code=str(item.get("code") or "domain_gate_blocker"),
            message=str(item.get("message") or "Domain gate blocker."),
            blocking=bool(item.get("blocking", True)),
            severity=str(item.get("severity") or "high"),
            metadata=_dict_value(item.get("metadata")),
        )
        for item in _list_value(payload.get("blockers"))
        if isinstance(item, dict)
    ]
    warnings = [
        ResearchReviewFinding(
            gate=gate_name,
            code=str(item.get("code") or "domain_gate_warning"),
            message=str(item.get("message") or "Domain gate warning."),
            blocking=False,
            severity=str(item.get("severity") or "medium"),
            metadata=_dict_value(item.get("metadata")),
        )
        for item in _list_value(payload.get("warnings"))
        if isinstance(item, dict)
    ]
    approved = bool(payload.get("approved")) and not blockers
    return ResearchReviewGateResult(
        gate=gate_name,
        approved=approved,
        decision=approved_decision if approved else str(payload.get("decision") or (blockers[0].code if blockers else "blocked")),
        statuses=[str(item) for item in _list_value(payload.get("statuses"))] or [str(payload.get("decision") or "")],
        checks=_dict_value(payload.get("checks")),
        blockers=blockers,
        warnings=warnings,
        source_id=str(payload.get("model_id") or payload.get("game_id") or payload.get("claim_id") or payload.get("evidence_id") or ""),
        metadata={"domain_gate": payload},
    )


def _missing_domain_gate(gate_name: str, code: str, message: str) -> ResearchReviewGateResult:
    blocker = ResearchReviewFinding(gate=gate_name, code=code, message=message)
    return ResearchReviewGateResult(
        gate=gate_name,
        approved=False,
        decision=code,
        statuses=[code],
        checks={f"{gate_name}_declared": False},
        blockers=[blocker],
    )


def _gate(
    gate_name: str,
    blockers: list[ResearchReviewFinding],
    checks: dict[str, Any],
    *,
    approved_decision: str,
    source_id: str = "",
    metadata: dict[str, Any] | None = None,
) -> ResearchReviewGateResult:
    approved = not blockers
    decision = approved_decision if approved else blockers[0].code
    return ResearchReviewGateResult(
        gate=gate_name,
        approved=approved,
        decision=decision,
        statuses=[decision] if approved else [item.code for item in blockers],
        checks=checks,
        blockers=blockers,
        source_id=source_id,
        metadata=metadata or {},
    )


def _require(
    blockers: list[ResearchReviewFinding],
    gate: str,
    condition: bool,
    code: str,
    message: str,
    *,
    metadata: dict[str, Any] | None = None,
) -> None:
    if condition:
        return
    blockers.append(ResearchReviewFinding(gate=gate, code=code, message=message, metadata=metadata or {}))


def _ordered_gates(values: Any) -> list[str]:
    requested = [str(item).strip().lower().replace("-", "_") for item in _list_value(values)]
    seen: set[str] = set()
    ordered: list[str] = []
    for name in requested:
        if name not in RESEARCH_REVIEW_GATES:
            raise ValueError(f"unknown research review gate: {name}")
        if name in seen:
            continue
        seen.add(name)
        ordered.append(name)
    return ordered


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    return list(value) if isinstance(value, list) else [value]


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except ValueError:
        return None
