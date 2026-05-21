from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from amra.crypto.reductions import SecurityReduction, reductions_from_payload
from amra.crypto.security_game import SecurityAssumption, SecurityGameSpec, security_assumptions_from_payload
from amra.crypto.threat_model import ThreatModel, threat_model_from_payload
from amra.modeling.model_spec import _dict_value, _list_value, _number, _string_list, slug
from amra.orchestration.workstreams import utc_now_iso
from amra.portfolio_memory import write_json
from amra.research.evidence import EvidenceConfidence, EvidenceKind, EvidenceRecord, EvidenceStatus
from amra.research.objects import ResearchConfidence, ResearchObjectStatus, SecurityGameRecord
from amra.research_review.security_gate import evaluate_security_gate


CRYPTO_SECURITY_RUN_SCHEMA_VERSION = "amra.crypto_security_run.v1"
ATTACK_SEARCH_REPORT_SCHEMA_VERSION = "amra.crypto.bounded_attack_search_report.v1"

CRYPTO_SECURITY_RUN_FILE = "crypto_security_run.json"
THREAT_MODEL_FILE = "threat_model.json"
SECURITY_GAME_FILE = "security_game.json"
SECURITY_ASSUMPTIONS_FILE = "security_assumptions.json"
SECURITY_REDUCTIONS_FILE = "security_reductions.json"
ATTACK_SEARCH_REPORT_FILE = "bounded_attack_search_report.json"
SECURITY_EVIDENCE_FILE = "security_evidence.json"
SECURITY_GATE_INPUTS_FILE = "security_gate_inputs.json"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(slots=True)
class AttackCandidate:
    attack_id: str
    strategy: str
    oracle_queries: int = 0
    trials: int = 1
    advantage: float = 0.0
    wins: bool = False
    transcript: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any], *, index: int = 0) -> "AttackCandidate":
        return cls(
            attack_id=str(payload.get("attack_id") or payload.get("id") or f"attack-{index + 1}"),
            strategy=str(payload.get("strategy") or payload.get("description") or ""),
            oracle_queries=int(_number(payload.get("oracle_queries") or payload.get("queries")) or 0),
            trials=int(_number(payload.get("trials")) or 1),
            advantage=float(_number(payload.get("advantage") or payload.get("success_advantage")) or 0.0),
            wins=bool(payload.get("wins") or payload.get("winning")),
            transcript=_dict_value(payload.get("transcript")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "attack_id": self.attack_id,
            "strategy": self.strategy,
            "oracle_queries": self.oracle_queries,
            "trials": self.trials,
            "advantage": self.advantage,
            "wins": self.wins,
            "transcript": dict(self.transcript),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class BoundedAttackSearchReport:
    attack_report_id: str
    game_id: str
    search_bound: dict[str, Any]
    attempted_attacks: list[AttackCandidate]
    found_attacks: list[AttackCandidate]
    exhausted: bool
    bounded_evidence_only: bool = True
    proof_status: str = "not_proof"
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": ATTACK_SEARCH_REPORT_SCHEMA_VERSION,
            "attack_report_id": self.attack_report_id,
            "game_id": self.game_id,
            "search_bound": dict(self.search_bound),
            "attempted_attacks": [item.to_dict() for item in self.attempted_attacks],
            "found_attacks": [item.to_dict() for item in self.found_attacks],
            "attempted_count": len(self.attempted_attacks),
            "found_count": len(self.found_attacks),
            "exhausted": self.exhausted,
            "bounded_evidence_only": self.bounded_evidence_only,
            "proof_status": self.proof_status,
            "evidence_confidence": "medium" if self.exhausted and not self.found_attacks else "low",
            "notes": list(self.notes),
        }


class CryptoSecurityRunner:
    def run_fixture(self, *, fixture: Path, output_dir: Path) -> dict[str, Any]:
        fixture_path = fixture.expanduser().resolve()
        output_dir = output_dir.expanduser().resolve()
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("crypto security fixture must be a JSON object")

        threat_model = threat_model_from_payload(payload)
        game_payload = _dict_value(payload.get("security_game") or payload.get("game"))
        security_game = SecurityGameSpec.from_dict(game_payload, threat_model_id=threat_model.threat_model_id)
        assumptions = security_assumptions_from_payload(payload)
        reductions = reductions_from_payload(payload, game_id=security_game.game_id)
        attack_report = self._search_attacks(payload=payload, security_game=security_game)
        evidence = self._security_evidence(security_game=security_game, attack_report=attack_report, fixture_path=fixture_path)
        gate = evaluate_security_gate(
            threat_model=threat_model.to_dict(),
            security_game=security_game.to_dict(),
            assumptions=[item.to_dict() for item in assumptions],
            reductions=[item.to_dict() for item in reductions],
            attack_report=attack_report.to_dict(),
            evidence=evidence.to_dict(),
        )
        game_record = self._security_game_record(
            security_game=security_game,
            assumptions=assumptions,
            reductions=reductions,
            attack_report=attack_report,
            evidence=evidence,
            gate_decision=gate.decision,
            gate_statuses=gate.statuses,
        )

        threat_payload = threat_model.to_dict()
        game_spec_payload = security_game.to_dict()
        game_spec_payload["security_game_record"] = game_record.to_dict()
        assumptions_payload = [item.to_dict() for item in assumptions]
        reductions_payload = [item.to_dict() for item in reductions]
        attack_payload = attack_report.to_dict()
        evidence_payload = evidence.to_dict()
        gate_payload = gate.to_dict()

        output_dir.mkdir(parents=True, exist_ok=True)
        fixture_hash = _sha256_file(fixture_path)
        run = {
            "schema_version": CRYPTO_SECURITY_RUN_SCHEMA_VERSION,
            "status": "succeeded" if gate_payload["approved"] else "needs_review",
            "generated_at": utc_now_iso(),
            "deterministic": True,
            "fixture": {"path": str(fixture_path), "sha256": fixture_hash},
            "output_dir": str(output_dir),
            "threat_model": threat_payload,
            "security_game": game_record.to_dict(),
            "security_game_spec": game_spec_payload,
            "assumptions": assumptions_payload,
            "reductions": reductions_payload,
            "bounded_attack_search_report": attack_payload,
            "security_evidence": evidence_payload,
            "security_gate_inputs": gate_payload,
            "record_files": {
                "run": str(output_dir / CRYPTO_SECURITY_RUN_FILE),
                "threat_model": str(output_dir / THREAT_MODEL_FILE),
                "security_game": str(output_dir / SECURITY_GAME_FILE),
                "assumptions": str(output_dir / SECURITY_ASSUMPTIONS_FILE),
                "reductions": str(output_dir / SECURITY_REDUCTIONS_FILE),
                "bounded_attack_search_report": str(output_dir / ATTACK_SEARCH_REPORT_FILE),
                "security_evidence": str(output_dir / SECURITY_EVIDENCE_FILE),
                "security_gate_inputs": str(output_dir / SECURITY_GATE_INPUTS_FILE),
            },
        }

        write_json(output_dir / THREAT_MODEL_FILE, threat_payload)
        write_json(output_dir / SECURITY_GAME_FILE, game_spec_payload)
        write_json(output_dir / SECURITY_ASSUMPTIONS_FILE, assumptions_payload)
        write_json(output_dir / SECURITY_REDUCTIONS_FILE, reductions_payload)
        write_json(output_dir / ATTACK_SEARCH_REPORT_FILE, attack_payload)
        write_json(output_dir / SECURITY_EVIDENCE_FILE, evidence_payload)
        write_json(output_dir / SECURITY_GATE_INPUTS_FILE, gate_payload)
        write_json(output_dir / CRYPTO_SECURITY_RUN_FILE, run)
        return run

    def _search_attacks(self, *, payload: dict[str, Any], security_game: SecurityGameSpec) -> BoundedAttackSearchReport:
        search_payload = _dict_value(payload.get("attack_search") or payload.get("bounded_attack_search"))
        search_bound = _dict_value(search_payload.get("search_bound") or search_payload.get("budget") or payload.get("search_bound"))
        if not search_bound:
            search_bound = {"max_trials": 0, "max_oracle_queries": 0, "adversary_class": security_game.adversary_model}
        max_trials = int(_number(search_bound.get("max_trials")) or 0)
        max_queries = int(_number(search_bound.get("max_oracle_queries") or search_bound.get("query_budget")) or 0)
        candidates = [
            AttackCandidate.from_dict(item, index=index)
            for index, item in enumerate(_list_value(search_payload.get("candidates") or payload.get("attack_candidates")))
            if isinstance(item, dict)
        ]
        attempted: list[AttackCandidate] = []
        found: list[AttackCandidate] = []
        used_trials = 0
        used_queries = 0
        for candidate in candidates:
            if used_trials + candidate.trials > max_trials:
                continue
            if used_queries + candidate.oracle_queries > max_queries:
                continue
            attempted.append(candidate)
            used_trials += candidate.trials
            used_queries += candidate.oracle_queries
            if candidate.wins or candidate.advantage > security_game.advantage_threshold:
                found.append(candidate)
        exhausted = len(attempted) == len(candidates) or used_trials >= max_trials
        search_bound = {
            **search_bound,
            "max_trials": max_trials,
            "max_oracle_queries": max_queries,
            "used_trials": used_trials,
            "used_oracle_queries": used_queries,
        }
        report_id = str(search_payload.get("attack_report_id") or search_payload.get("id") or f"attack-search-{slug(security_game.game_id)}")
        notes = _string_list(search_payload.get("notes"))
        if not found:
            notes.append("No candidate attack satisfied the winning condition within the declared finite bound; this is not a proof of security.")
        return BoundedAttackSearchReport(
            attack_report_id=report_id,
            game_id=security_game.game_id,
            search_bound=search_bound,
            attempted_attacks=attempted,
            found_attacks=found,
            exhausted=exhausted,
            notes=notes,
        )

    def _security_evidence(
        self,
        *,
        security_game: SecurityGameSpec,
        attack_report: BoundedAttackSearchReport,
        fixture_path: Path,
    ) -> EvidenceRecord:
        found_attack = bool(attack_report.found_attacks)
        return EvidenceRecord(
            evidence_id=f"security-evidence-{slug(attack_report.attack_report_id)}",
            kind=EvidenceKind.SECURITY_EVIDENCE,
            target_object_id=security_game.game_id,
            summary=(
                "Candidate attack found within bounded search."
                if found_attack
                else "No candidate attack found within bounded search; bounded evidence only."
            ),
            status=EvidenceStatus.RECORDED,
            confidence=EvidenceConfidence.LOW if found_attack else EvidenceConfidence.MEDIUM,
            command=f"python3 -m amra crypto search-attack --fixture {fixture_path} --out <output> --json",
            notes="Attack-search failure is bounded evidence and must not be promoted to proof.",
            metadata={
                "attack_report_id": attack_report.attack_report_id,
                "bounded_evidence_only": True,
                "proof_status": "not_proof",
                "found_attack_count": len(attack_report.found_attacks),
                "search_bound": dict(attack_report.search_bound),
            },
        )

    def _security_game_record(
        self,
        *,
        security_game: SecurityGameSpec,
        assumptions: list[SecurityAssumption],
        reductions: list[SecurityReduction],
        attack_report: BoundedAttackSearchReport,
        evidence: EvidenceRecord,
        gate_decision: str,
        gate_statuses: list[str],
    ) -> SecurityGameRecord:
        attack_found = bool(attack_report.found_attacks)
        approved = gate_decision == "security_reviewed_bounded_evidence"
        return SecurityGameRecord(
            object_id=security_game.game_id,
            title=security_game.title,
            status=ResearchObjectStatus.TESTING if attack_found or not approved else ResearchObjectStatus.EMPIRICALLY_SUPPORTED,
            statement=security_game.winning_condition,
            domain="cryptography",
            tags=["cryptography", "security_game", "bounded_attack_search"],
            confidence=ResearchConfidence.LOW if attack_found else ResearchConfidence.MEDIUM,
            evidence_ids=[evidence.evidence_id],
            scheme=security_game.scheme,
            adversary_model=security_game.adversary_model,
            oracle_access=security_game.oracle_access,
            winning_condition=security_game.winning_condition,
            assumptions=[item.assumption_id for item in assumptions],
            reductions=[item.reduction_id for item in reductions],
            attack_attempts=[attack_report.attack_report_id],
            security_status="attack_found" if attack_found else "bounded_no_attack_found_not_proof",
            metadata={
                "threat_model_id": security_game.threat_model_id,
                "security_gate_decision": gate_decision,
                "security_gate_statuses": list(gate_statuses),
                "bounded_evidence_only": True,
                "proof_status": "not_proof",
            },
        )


def run_crypto_attack_search_fixture(*, fixture: Path, output_dir: Path) -> dict[str, Any]:
    return CryptoSecurityRunner().run_fixture(fixture=fixture, output_dir=output_dir)
