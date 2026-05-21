from __future__ import annotations

import json
from pathlib import Path

from amra.cli import main
from amra.crypto import (
    ATTACK_SEARCH_REPORT_FILE,
    CRYPTO_SECURITY_RUN_FILE,
    SECURITY_ASSUMPTIONS_FILE,
    SECURITY_EVIDENCE_FILE,
    SECURITY_GAME_FILE,
    SECURITY_GATE_INPUTS_FILE,
    SECURITY_REDUCTIONS_FILE,
    THREAT_MODEL_FILE,
    SecurityAssumption,
    SecurityGameSpec,
    ThreatModel,
    run_crypto_attack_search_fixture,
)
from amra.research import ResearchObjectRecord, SecurityGameRecord


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "crypto_security_fixture.json"


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_crypto_search_attack_persists_security_pack_and_bounded_evidence(tmp_path: Path) -> None:
    output = tmp_path / "crypto-security"

    payload = run_crypto_attack_search_fixture(fixture=FIXTURE, output_dir=output)

    threat_model = _read_json(output / THREAT_MODEL_FILE)
    security_game = _read_json(output / SECURITY_GAME_FILE)
    assumptions = _read_json(output / SECURITY_ASSUMPTIONS_FILE)
    reductions = _read_json(output / SECURITY_REDUCTIONS_FILE)
    attack_report = _read_json(output / ATTACK_SEARCH_REPORT_FILE)
    evidence = _read_json(output / SECURITY_EVIDENCE_FILE)
    gate = _read_json(output / SECURITY_GATE_INPUTS_FILE)

    restored_game = ResearchObjectRecord.from_dict(security_game["security_game_record"])

    assert payload["schema_version"] == "amra.crypto_security_run.v1"
    assert payload["status"] == "succeeded"
    assert ThreatModel.from_dict(threat_model).threat_model_id == "threat-toy-kem-cca"
    assert SecurityGameSpec.from_dict(security_game).game_id == "game-toy-kem-ind-cca"
    assert SecurityAssumption.from_dict(assumptions[0]).assumption_id == "assumption-ddh-toy-group"
    assert reductions[0]["assumption_id"] == "assumption-ddh-toy-group"
    assert isinstance(restored_game, SecurityGameRecord)
    assert restored_game.security_status == "bounded_no_attack_found_not_proof"
    assert attack_report["found_count"] == 0
    assert attack_report["bounded_evidence_only"] is True
    assert attack_report["proof_status"] == "not_proof"
    assert evidence["kind"] == "security_evidence"
    assert evidence["confidence"] != "theorem_grade"
    assert evidence["theorem_grade"] is False
    assert gate["approved"] is True
    assert gate["decision"] == "security_reviewed_bounded_evidence"
    assert gate["warnings"][0]["code"] == "bounded_evidence_not_proof"
    assert gate["checks"]["attack_failure_bounded_evidence_only"] is True
    assert (output / CRYPTO_SECURITY_RUN_FILE).exists()


def test_crypto_security_gate_blocks_found_attack(tmp_path: Path) -> None:
    fixture_payload = _read_json(FIXTURE)
    fixture_payload["attack_search"]["candidates"][0]["advantage"] = 0.5
    fixture = tmp_path / "winning_attack_fixture.json"
    fixture.write_text(json.dumps(fixture_payload), encoding="utf-8")

    payload = run_crypto_attack_search_fixture(fixture=fixture, output_dir=tmp_path / "out")

    assert payload["status"] == "needs_review"
    assert payload["bounded_attack_search_report"]["found_count"] == 1
    assert payload["security_gate_inputs"]["decision"] == "attack_found"
    assert "attack_found" in payload["security_gate_inputs"]["statuses"]
    assert payload["security_game"]["security_status"] == "attack_found"


def test_crypto_search_attack_cli_accepts_required_smoke_shape(tmp_path: Path, capsys) -> None:
    output = tmp_path / "cli-crypto-security"

    exit_code = main(["crypto", "search-attack", "--fixture", str(FIXTURE), "--out", str(output), "--json"])
    printed = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert printed["schema_version"] == "amra.crypto_security_run.v1"
    assert printed["security_gate_inputs"]["decision"] == "security_reviewed_bounded_evidence"
    assert printed["bounded_attack_search_report"]["proof_status"] == "not_proof"
    assert printed["security_game"]["object_type"] == "security_game"
    assert (output / SECURITY_GATE_INPUTS_FILE).exists()
