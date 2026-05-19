from __future__ import annotations

import json
from pathlib import Path

from amra.nontrivial_benchmark import (
    DEFAULT_NONTRIVIAL_BENCHMARK_CASE,
    NONTRIVIAL_BENCHMARK_SCHEMA_VERSION,
    run_nontrivial_closed_theorem_benchmark,
)
from ara_math.cli import main


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _ledger(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_nontrivial_closed_theorem_benchmark_exports_bundle_and_candidate_report(tmp_path: Path) -> None:
    output = tmp_path / "nontrivial-bundle"

    result = run_nontrivial_closed_theorem_benchmark(output_dir=output, max_seconds=60, repo_root=tmp_path)

    manifest = _json(output / "artifact_manifest.json")
    build_report = _json(output / "lean_build_report.json")
    declarations = _json(output / "verified_declarations.json")
    sketches = _json(output / "natural_language_proof_sketches.json")
    candidates = _json(output / "library_harvest_candidates.json")
    review_gate = _json(output / "benchmark_review_gate.json")
    benchmark_report = _json(output / "nontrivial_benchmark_report.json")
    ledger = _ledger(output / "proof_attempt_ledger.jsonl")

    assert result["schema_version"] == NONTRIVIAL_BENCHMARK_SCHEMA_VERSION
    assert result["problem_id"] == DEFAULT_NONTRIVIAL_BENCHMARK_CASE
    assert result["status"] in {"verified", "blocked"}
    assert result["llm_calls"] == 0
    assert result["selection"]["difficulty"] == "medium_school_induction"

    assert manifest["nontrivial_closed_theorem_benchmark"]["problem_id"] == DEFAULT_NONTRIVIAL_BENCHMARK_CASE
    assert manifest["nontrivial_closed_theorem_benchmark"]["status"] == result["status"]
    assert manifest["nontrivial_closed_theorem_benchmark"]["proof_loop_state"]["informal_claims"] == 1
    assert manifest["verification_policy"]["only_lean_verified_claim_source"] == "verified_declarations.json"
    assert manifest["proof_loop_state"]["informal_claims"]["status"] == "present"
    assert manifest["proof_loop_state"]["model_mismatch"]["status"] == "absent"
    assert {
        "proof_attempt_ledger.jsonl",
        "library_harvest_candidates.json",
        "benchmark_review_gate.json",
        "nontrivial_benchmark_report.json",
    }.issubset({item["path"] for item in manifest["files"]})

    assert [entry["phase"] for entry in ledger] == [
        "problem_selection",
        "natural_language_proof",
        "lean_formalization",
        "library_candidate_detection",
    ]
    assert ledger[1]["proof_loop_state"] == "informal_claim"
    assert ledger[2]["proof_loop_state"] in {"lean_verified_declaration", "blocked_formalization_gap"}
    assert all(entry["backend"] == "deterministic_benchmark" for entry in ledger)
    assert all(entry["llm_calls"] == 0 for entry in ledger)

    assert "induction" in json.dumps(sketches).lower()
    assert "fixture" not in _json(output / "problem_metadata.json")["title"].lower()
    assert benchmark_report["library_candidate_count"] == candidates["candidate_count"]
    assert review_gate["decision"] in {"approved", "blocked"}
    assert build_report["verification_status"] in {"verified", "blocked"}

    if result["status"] == "verified":
        names = {item["full_name"] for item in declarations["declarations"]}
        assert "AMRA.NontrivialClosedBenchmark.oddSum" in names
        assert "AMRA.NontrivialClosedBenchmark.odd_sum_first_n_odds" in names
        assert candidates["candidate_count"] >= 2
        assert review_gate["decision"] == "approved"
        assert manifest["unresolved_blocker_count"] == 0
    else:
        assert declarations["declarations"] == []
        assert candidates["candidate_count"] == 0
        assert review_gate["decision"] == "blocked"
        assert manifest["unresolved_blocker_count"] >= 1


def test_nontrivial_closed_theorem_benchmark_cli_writes_bundle(tmp_path: Path, monkeypatch, capsys) -> None:
    output = tmp_path / "cli-nontrivial-bundle"
    monkeypatch.setenv("AMRA_REPO_ROOT", str(tmp_path))

    exit_code = main(
        [
            "--json",
            "run-nontrivial-closed-theorem-benchmark",
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
    assert payload["backend"] == "deterministic_benchmark"
    assert (output / "artifact_manifest.json").exists()
    assert (output / "library_harvest_candidates.json").exists()
    assert (output / "nontrivial_benchmark_report.json").exists()
