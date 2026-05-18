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
    ledger = _ledger(output / "proof_attempt_ledger.jsonl")

    assert result["schema_version"] == KNOWN_PROBLEM_SMOKE_SCHEMA_VERSION
    assert result["problem_id"] == "imo_2025_p1"
    assert result["status"] in {"verified", "blocked"}
    assert result["llm_calls"] == 0
    assert smoke_report["status"] == result["status"]

    assert manifest["known_problem_smoke"]["problem_id"] == "imo_2025_p1"
    assert manifest["known_problem_smoke"]["status"] == result["status"]
    assert manifest["known_problem_smoke"]["llm_calls"] == 0
    assert manifest["verification_policy"]["only_lean_verified_claim_source"] == "verified_declarations.json"
    assert "proof_attempt_ledger.jsonl" in {item["path"] for item in manifest["files"]}

    assert len(ledger) == 2
    assert [entry["phase"] for entry in ledger] == ["natural_language_proof", "lean_formalization"]
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
