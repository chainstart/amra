from __future__ import annotations

import json
from pathlib import Path

from amra.known_problem_smoke import KNOWN_PROBLEM_SMOKE_SCHEMA_VERSION, run_known_problem_smoke
from ara_math.cli import main


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _ledger(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_known_problem_smoke_exports_ara_consumable_bundle(tmp_path: Path) -> None:
    output = tmp_path / "bundle"

    result = run_known_problem_smoke(problem_id="imo_2025_p1", max_seconds=60, output_dir=output, repo_root=tmp_path)

    manifest = _json(output / "artifact_manifest.json")
    build_report = _json(output / "lean_build_report.json")
    declarations = _json(output / "verified_declarations.json")
    smoke_report = _json(output / "known_problem_smoke_report.json")
    handoff_notes = (output / "handoff_notes.md").read_text(encoding="utf-8")
    ledger = _ledger(output / "proof_attempt_ledger.jsonl")

    assert result["schema_version"] == KNOWN_PROBLEM_SMOKE_SCHEMA_VERSION
    assert result["problem_id"] == "imo_2025_p1"
    assert result["status"] in {"verified", "blocked"}
    assert result["llm_calls"] == 0
    assert smoke_report["status"] == result["status"]

    assert manifest["known_problem_smoke"]["problem_id"] == "imo_2025_p1"
    assert manifest["known_problem_smoke"]["status"] == result["status"]
    assert manifest["known_problem_smoke"]["llm_calls"] == 0
    assert manifest["known_problem_smoke"]["proof_loop_state"]["informal_claims"] == 1
    assert manifest["verification_policy"]["only_lean_verified_claim_source"] == "verified_declarations.json"
    assert manifest["verification_boundaries"]["lean_status"]["source"] == "lean_build_report.json"
    assert manifest["verification_boundaries"]["natural_language_proof_artifacts"]["source"] == "natural_language_proof_sketches.json"
    assert manifest["lean_status"]["verified_declaration_source"] == "verified_declarations.json"
    assert manifest["proof_loop_state"]["informal_claims"]["count"] == 1
    assert manifest["proof_loop_state"]["model_mismatch"]["status"] == "absent"
    assert manifest["ara_handoff"]["consumer"] == "ARA"
    assert manifest["ara_handoff"]["handoff_notes"] == "handoff_notes.md"
    assert "proof_attempt_ledger.jsonl" in {item["path"] for item in manifest["files"]}
    files = {item["path"]: item for item in manifest["files"]}
    assert files["handoff_notes.md"]["sha256"]
    assert files["known_problem_smoke_report.json"]["sha256"]
    assert files["natural_language_proof_sketches.json"]["lean_verified_claim_source"] is False
    assert "Natural-language proof artifacts may explain the route" in handoff_notes

    assert len(ledger) == 2
    assert [entry["phase"] for entry in ledger] == ["natural_language_proof", "lean_formalization"]
    assert [entry["proof_loop_state"] for entry in ledger] == [
        "informal_claim",
        "lean_verified_declaration" if result["status"] == "verified" else "blocked_formalization_gap",
    ]
    assert all(entry["backend"] == "deterministic_fixture" for entry in ledger)
    assert all(entry["llm_calls"] == 0 for entry in ledger)

    assert build_report["verification_status"] in {"verified", "blocked"}
    if result["status"] == "verified":
        assert build_report["status"] == "passed"
        assert declarations["declarations"][0]["full_name"] == "AMRA.KnownProblemSmoke.imo_2025_p1_fixture_identity"
    else:
        assert declarations["declarations"] == []
        assert manifest["unresolved_blocker_count"] >= 1


def test_known_problem_smoke_cli_writes_bundle(tmp_path: Path, monkeypatch, capsys) -> None:
    output = tmp_path / "cli-bundle"
    monkeypatch.setenv("AMRA_REPO_ROOT", str(tmp_path))

    exit_code = main(
        [
            "--json",
            "run-known-problem-smoke",
            "--problem",
            "imo_2025_p1",
            "--max-seconds",
            "60",
            "--out",
            str(output),
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["status"] in {"verified", "blocked"}
    assert payload["backend"] == "deterministic_fixture"
    assert (output / "artifact_manifest.json").exists()
    assert (output / "proof_attempt_ledger.jsonl").exists()
    assert (output / "lean_build_report.json").exists()
