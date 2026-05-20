from __future__ import annotations

import json
from pathlib import Path

from amra.cli import main
from amra.proof.stability import (
    FAILURE_TAXONOMY,
    PROOF_STABILITY_REPORT_SCHEMA_VERSION,
    PROOF_STABILITY_RESUME_SCHEMA_VERSION,
    PROOF_STABILITY_SUITE_SCHEMA_VERSION,
    load_proof_stability_suite,
    run_proof_stability_benchmark,
)


FIXTURE_SUITE = Path(__file__).resolve().parent / "fixtures" / "proof_stability_suite.yaml"


def _jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_load_proof_stability_suite_fixture() -> None:
    suite = load_proof_stability_suite(FIXTURE_SUITE)

    assert suite["schema_version"] == PROOF_STABILITY_SUITE_SCHEMA_VERSION
    assert suite["requirements"]["min_mixed_cases"] == 2
    assert {case["id"] for case in suite["cases"]} >= {
        "nl_reflexivity_fixture",
        "mixed_proof_search_converged",
        "mixed_closure_blocked_formalization_gap",
        "budget_guard_regression",
    }


def test_proof_stability_benchmark_writes_resume_records_and_taxonomy(tmp_path: Path) -> None:
    output = tmp_path / "proof-stability"

    report = run_proof_stability_benchmark(suite_path=FIXTURE_SUITE, output_dir=output, repo_root=tmp_path)
    resume_records = _jsonl(output / "proof_stability_resume.jsonl")
    written_report = json.loads((output / "proof_stability_report.json").read_text(encoding="utf-8"))
    cases = {case["case_id"]: case for case in report["cases"]}

    assert report["schema_version"] == PROOF_STABILITY_REPORT_SCHEMA_VERSION
    assert written_report["status"] == "passed"
    assert report["status"] == "passed"
    assert report["llm_calls"] == 0
    assert report["live_model_calls"] is False
    assert "budget_exhausted" in FAILURE_TAXONOMY
    assert "blocked_formalization_gap" in report["taxonomy_counts"]
    assert report["taxonomy_counts"]["budget_exhausted"] == 1
    assert report["route_counts"]["proof_search"] == 1
    assert report["mixed_proof_search"]["case_count"] == 2
    assert cases["mixed-proof-search-converged"]["canonical_status"] == "verified"
    assert cases["budget-guard-regression"]["executed"] is False
    assert cases["budget-guard-regression"]["failure_taxon"] == "budget_exhausted"
    assert (output / "cases" / "mixed-proof-search-converged" / "result.json").exists()
    assert (output / "summary.md").exists()

    assert len(resume_records) == 8
    assert {record["schema_version"] for record in resume_records} == {PROOF_STABILITY_RESUME_SCHEMA_VERSION}
    assert [record["event"] for record in resume_records[:2]] == ["case_started", "case_completed"]
    assert all(record["llm_calls"] == 0 for record in resume_records)


def test_proof_stability_cli_benchmark_outputs_json(tmp_path: Path, capsys) -> None:
    output = tmp_path / "cli-proof-stability"

    exit_code = main(["--json", "proof-stability", "benchmark", "--suite", str(FIXTURE_SUITE), "--out", str(output)])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["status"] == "passed"
    assert payload["resume_records"].endswith("proof_stability_resume.jsonl")
    assert payload["case_count"] == 4
    assert payload["route_counts"]["proof_lab"] == 2
    assert (output / "proof_stability_report.json").exists()
