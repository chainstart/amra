from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from amra.modeling.model_spec import _dict_value, _list_value, _number


SECURITY_GATE_SCHEMA_VERSION = "amra.security_gate.v1"


@dataclass(slots=True)
class SecurityGateDecision:
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
class SecurityGateInput:
    game_id: str
    statuses: list[str]
    decision: str
    checks: dict[str, Any]
    blockers: list[SecurityGateDecision] = field(default_factory=list)
    warnings: list[SecurityGateDecision] = field(default_factory=list)
    attack_report_id: str = ""
    evidence_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SECURITY_GATE_SCHEMA_VERSION,
            "game_id": self.game_id,
            "statuses": list(self.statuses),
            "decision": self.decision,
            "checks": dict(self.checks),
            "blockers": [item.to_dict() for item in self.blockers],
            "warnings": [item.to_dict() for item in self.warnings],
            "attack_report_id": self.attack_report_id,
            "evidence_id": self.evidence_id,
            "approved": not self.blockers,
        }


def evaluate_security_gate(
    *,
    threat_model: dict[str, Any],
    security_game: dict[str, Any],
    assumptions: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    attack_report: dict[str, Any],
    evidence: dict[str, Any] | None = None,
) -> SecurityGateInput:
    threat_model = _dict_value(threat_model)
    security_game = _dict_value(security_game)
    attack_report = _dict_value(attack_report)
    evidence = _dict_value(evidence)
    assumptions = [dict(item) for item in assumptions if isinstance(item, dict)]
    reductions = [dict(item) for item in reductions if isinstance(item, dict)]

    assumption_ids = {
        str(item.get("assumption_id") or item.get("id") or "")
        for item in assumptions
        if item.get("assumption_id") or item.get("id")
    }
    game_id = str(security_game.get("game_id") or security_game.get("object_id") or "")
    reduction_targets = {
        str(item.get("assumption_id") or item.get("target_assumption_id") or "")
        for item in reductions
        if item.get("assumption_id") or item.get("target_assumption_id")
    }
    found_attacks = [dict(item) for item in _list_value(attack_report.get("found_attacks")) if isinstance(item, dict)]
    search_bound = _dict_value(attack_report.get("search_bound"))
    max_trials = _number(search_bound.get("max_trials"))
    max_queries = _number(search_bound.get("max_oracle_queries") or search_bound.get("query_budget"))
    proof_status = str(attack_report.get("proof_status") or evidence.get("metadata", {}).get("proof_status") or "")
    evidence_confidence = str(evidence.get("confidence") or attack_report.get("evidence_confidence") or "")

    checks = {
        "threat_model_declared": bool(threat_model.get("threat_model_id") or threat_model.get("object_id"))
        and bool(_list_value(threat_model.get("assets")))
        and bool(_list_value(threat_model.get("adversary_goals"))),
        "adversary_capabilities_declared": bool(_list_value(threat_model.get("capabilities"))),
        "security_game_declared": bool(game_id)
        and bool(security_game.get("scheme"))
        and bool(security_game.get("winning_condition")),
        "oracle_access_declared": bool(_list_value(security_game.get("oracle_access"))),
        "assumptions_declared": bool(assumptions)
        and all(str(item.get("statement") or item.get("description") or "") for item in assumptions),
        "reduction_declared": bool(reductions),
        "reduction_targets_assumption": bool(reductions)
        and bool(assumption_ids)
        and len(reduction_targets) == len(reductions)
        and all(item in assumption_ids for item in reduction_targets),
        "bounded_attack_search_recorded": bool(attack_report.get("attack_report_id"))
        and bool(search_bound)
        and max_trials is not None
        and max_trials >= 0,
        "oracle_budget_bounded": max_queries is not None and max_queries >= 0,
        "attack_found": bool(found_attacks),
        "attack_failure_bounded_evidence_only": bool(found_attacks)
        or (
            bool(attack_report)
            and bool(search_bound)
            and proof_status != "proof"
            and evidence_confidence != "theorem_grade"
            and bool(attack_report.get("bounded_evidence_only", True))
        ),
    }

    blockers: list[SecurityGateDecision] = []
    warnings: list[SecurityGateDecision] = []
    _require(blockers, checks["threat_model_declared"], "missing_threat_model", "Security review requires an explicit threat model.")
    _require(
        blockers,
        checks["adversary_capabilities_declared"],
        "missing_adversary_capabilities",
        "Threat model must declare adversary capabilities.",
    )
    _require(blockers, checks["security_game_declared"], "missing_security_game", "Security review requires a security game.")
    _require(blockers, checks["oracle_access_declared"], "missing_oracle_access", "Security game must declare oracle access.")
    _require(blockers, checks["assumptions_declared"], "missing_security_assumptions", "At least one stated security assumption is required.")
    _require(blockers, checks["reduction_declared"], "missing_reduction", "At least one reduction record is required.")
    _require(
        blockers,
        checks["reduction_targets_assumption"],
        "reduction_assumption_mismatch",
        "Every reduction must target a declared security assumption.",
        metadata={"assumption_ids": sorted(assumption_ids), "reduction_targets": sorted(reduction_targets)},
    )
    _require(
        blockers,
        checks["bounded_attack_search_recorded"],
        "missing_bounded_attack_search",
        "Security review requires a bounded attack-search report.",
    )
    _require(blockers, checks["oracle_budget_bounded"], "unbounded_oracle_budget", "Attack search must have a finite oracle budget.")
    _require(
        blockers,
        checks["attack_failure_bounded_evidence_only"],
        "attack_failure_misclassified_as_proof",
        "A failed bounded attack search must not be classified as a proof.",
    )

    if checks["attack_found"]:
        blockers.append(
            SecurityGateDecision(
                code="attack_found",
                message="A candidate adversary satisfied the security game's winning condition.",
                blocking=True,
                severity="critical",
                metadata={"found_attacks": found_attacks},
            )
        )
    elif checks["bounded_attack_search_recorded"] and checks["attack_failure_bounded_evidence_only"]:
        warnings.append(
            SecurityGateDecision(
                code="bounded_evidence_not_proof",
                message="No attack was found within the declared finite search bound; this is evidence, not proof.",
                blocking=False,
                severity="medium",
                metadata={"search_bound": search_bound},
            )
        )

    statuses = [item.code for item in blockers] + [item.code for item in warnings]
    if not statuses:
        statuses.append("security_reviewed")
    decision = blockers[0].code if blockers else "security_reviewed_bounded_evidence"

    return SecurityGateInput(
        game_id=game_id,
        statuses=statuses,
        decision=decision,
        checks=checks,
        blockers=blockers,
        warnings=warnings,
        attack_report_id=str(attack_report.get("attack_report_id") or ""),
        evidence_id=str(evidence.get("evidence_id") or ""),
    )


def _require(
    blockers: list[SecurityGateDecision],
    condition: bool,
    code: str,
    message: str,
    *,
    metadata: dict[str, Any] | None = None,
) -> None:
    if condition:
        return
    blockers.append(SecurityGateDecision(code=code, message=message, metadata=metadata or {}))
