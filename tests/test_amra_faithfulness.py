from __future__ import annotations

import json
from pathlib import Path

import yaml

from amra.cli import main
from amra.lean.faithfulness import (
    FAITHFULNESS_REPORT_SCHEMA_VERSION,
    MISMATCH_TAXONOMY,
    audit_faithfulness_bundle,
)
from amra.proof.stability import run_proof_stability_benchmark


FIXTURE_CASES = Path(__file__).resolve().parent / "fixtures" / "faithfulness_cases.yaml"
PROOF_STABILITY_SUITE = Path(__file__).resolve().parent / "fixtures" / "proof_stability_suite.yaml"


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def _write_bundle_from_case(case: dict, root: Path) -> Path:
    bundle = root / case["id"]
    problem = case["problem"]
    _write_json(
        bundle / "problem_metadata.json",
        {
            "schema_version": "amra.problem_metadata.v1",
            "problem_id": problem["problem_id"],
            "title": problem["problem_id"].replace("_", " ").title(),
            "statement": problem["statement"],
            "source": "faithfulness fixture",
            "references": [],
            "problem_yaml": {
                "metadata": {
                    "formal_statement": problem["formal_statement"],
                }
            },
        },
    )
    _write_json(
        bundle / "natural_language_proof_sketches.json",
        {
            "schema_version": "amra.natural_language_proof_sketches.v1",
            "problem_id": problem["problem_id"],
            "sketches": [
                {
                    "claim_id": "main",
                    "summary": problem["statement"],
                    "trust_level": "natural_language_proof_sketch",
                    "lean_verified": False,
                }
            ],
        },
    )
    declarations = []
    if "declaration" in case:
        declarations.append(
            {
                **case["declaration"],
                "status": "lean_verified",
                "lean_name": case["declaration"]["full_name"],
            }
        )
    _write_json(
        bundle / "verified_declarations.json",
        {
            "schema_version": "amra.verified_declarations.v1",
            "problem_id": problem["problem_id"],
            "declarations": declarations,
        },
    )
    _write_json(
        bundle / "lean_build_report.json",
        {
            "schema_version": "amra.lean_build_report.v1",
            "status": "passed" if declarations else "blocked",
            "verification_status": "verified" if declarations else "blocked",
            "diagnostics": [case["blocker"]] if case.get("blocker") else [],
        },
    )
    (bundle / "unresolved_blockers.md").write_text(
        "# Unresolved Blockers\n\n" + (f"- {case['blocker']}\n" if case.get("blocker") else "- None recorded.\n"),
        encoding="utf-8",
    )
    return bundle


def test_faithfulness_fixture_taxonomy_distinguishes_match_mismatch_and_blocker(tmp_path: Path) -> None:
    suite = yaml.safe_load(FIXTURE_CASES.read_text(encoding="utf-8"))
    assert suite["schema_version"] == "amra.nl_lean_faithfulness.fixture_suite.v1"
    assert "lean_statement_mismatch" in MISMATCH_TAXONOMY

    by_case: dict[str, dict] = {}
    for case in suite["cases"]:
        bundle = _write_bundle_from_case(case, tmp_path / "bundles")
        report = audit_faithfulness_bundle(bundle=bundle, output_dir=tmp_path / "audits" / case["id"])
        by_case[case["id"]] = report

    assert by_case["faithful_identity"]["schema_version"] == FAITHFULNESS_REPORT_SCHEMA_VERSION
    assert by_case["faithful_identity"]["status"] == "passed"
    assert by_case["faithful_identity"]["taxonomy_counts"]["faithfully_modeled"] == 1
    assert by_case["lean_statement_mismatch"]["status"] == "failed"
    assert by_case["lean_statement_mismatch"]["taxonomy_counts"]["lean_statement_mismatch"] == 1
    assert by_case["blocked_formalization_gap"]["status"] == "passed"
    assert by_case["blocked_formalization_gap"]["taxonomy_counts"]["missing_lean_declaration"] == 1
    assert by_case["blocked_formalization_gap"]["blocked_formalization_evidence_count"] >= 2
    assert (tmp_path / "audits" / "faithful_identity" / "faithfulness_report.json").exists()
    assert (tmp_path / "audits" / "faithful_identity" / "blocked_formalization_evidence.json").exists()


def test_faithfulness_cli_audits_proof_stability_report(tmp_path: Path, capsys) -> None:
    stability_dir = tmp_path / "proof-stability"
    audit_dir = tmp_path / "faithfulness"
    run_proof_stability_benchmark(suite_path=PROOF_STABILITY_SUITE, output_dir=stability_dir, repo_root=tmp_path)

    exit_code = main(
        [
            "--json",
            "formalization",
            "audit-faithfulness",
            "--bundle",
            str(stability_dir),
            "--out",
            str(audit_dir),
        ]
    )

    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["status"] == "passed"
    assert payload["bundle_kind"] == "proof_stability_report"
    assert payload["taxonomy_counts"]["faithfully_modeled"] == 1
    assert payload["taxonomy_counts"]["blocked_formalization_gap"] >= 2
    assert payload["taxonomy_counts"]["budget_guarded"] == 1
    assert payload["blocked_formalization_evidence_count"] == 1
    assert (audit_dir / "faithfulness_summary.md").exists()
