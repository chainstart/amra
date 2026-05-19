from __future__ import annotations

import json
from pathlib import Path

import yaml

from amra.portfolio_reports import write_portfolio_final_report
from amra.result_bundle import RESULT_BUNDLE_SCHEMA_VERSION, export_amra_result_bundle
from ara_math.cli import main


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _result_project(tmp_path: Path) -> Path:
    project = tmp_path / "projects" / "identity"
    (project / "proof" / "sketches").mkdir(parents=True, exist_ok=True)
    (project / "problem.yaml").write_text(
        "\n".join(
            [
                "problem_id: identity",
                "title: Identity theorem",
                "statement: Prove that every integer equals itself.",
                "source: unit-test-source",
                "references:",
                "  - https://example.test/identity",
                "metadata:",
                "  formal_statement: \"theorem identity_self (n : Nat) : n = n\"",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _write_json(
        project / "state.json",
        {
            "schema_version": "amra.problem_state.v1",
            "problem_id": "identity",
            "state": "verified",
            "reason": "unit test",
        },
    )
    (project / "proof" / "sketches" / "identity.md").write_text(
        "Proof sketch: use reflexivity. This is natural-language evidence only.\n",
        encoding="utf-8",
    )
    (project / "proof_attempt_ledger.jsonl").write_text(
        json.dumps(
            {
                "schema_version": "amra.proof_attempt_ledger.entry.v1",
                "attempt_id": "identity-lean-001",
                "phase": "lean_formalization",
                "status": "lean_verified",
                "backend": "deterministic_fixture",
                "llm_calls": 0,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    _write_json(project / "artifacts" / "lean_build_report.json", {"status": "passed", "sorry_count": 0})
    _write_json(
        project / "verified_declarations.json",
        {
            "schema_version": "amra.verified_declarations.v1",
            "declarations": [
                {
                    "name": "identity_self",
                    "full_name": "MathProject.identity_self",
                    "lean_name": "identity_self",
                    "status": "lean_verified",
                    "relative_path": "MathProject/Main.lean",
                    "statement": "theorem identity_self (n : Nat) : n = n",
                },
                {
                    "name": "sketched_only",
                    "full_name": "MathProject.sketched_only",
                    "status": "sketch",
                },
            ],
        },
    )
    return project


def test_amra_result_bundle_separates_sketches_from_verified_declarations(tmp_path: Path) -> None:
    project = _result_project(tmp_path)

    result = export_amra_result_bundle(project=project, output_dir=tmp_path / "bundle", repo_root=tmp_path)

    bundle_dir = tmp_path / "bundle"
    manifest = json.loads((bundle_dir / "artifact_manifest.json").read_text(encoding="utf-8"))
    declarations = json.loads((bundle_dir / "verified_declarations.json").read_text(encoding="utf-8"))
    proof_summary = (bundle_dir / "proof_summary.md").read_text(encoding="utf-8")
    handoff_notes = (bundle_dir / "handoff_notes.md").read_text(encoding="utf-8")

    assert result["schema_version"] == RESULT_BUNDLE_SCHEMA_VERSION
    assert set(result["required_files"]) <= {path.name for path in bundle_dir.iterdir()}
    assert "handoff_notes.md" in result["required_files"]
    assert declarations["declarations"][0]["full_name"] == "MathProject.identity_self"
    assert [item["full_name"] for item in declarations["declarations"]] == ["MathProject.identity_self"]
    assert "sketched_only" not in json.dumps(declarations)
    assert manifest["verification_policy"]["natural_language_proof_sketches_are_not_lean_verified"] is True
    assert manifest["verification_boundaries"]["formal_claims"]["source"] == "verified_declarations.json"
    assert manifest["lean_status"]["status"] == "passed"
    assert manifest["proof_loop_state"]["informal_claims"]["count"] >= 1
    assert manifest["proof_loop_state"]["lean_verified_declarations"]["count"] == 1
    assert manifest["proof_loop_state"]["blocked_formalization_gaps"]["status"] == "absent"
    assert manifest["faithful_modeling"]["status"] == "faithfully_modeled"
    assert manifest["ara_handoff"]["handoff_notes"] == "handoff_notes.md"
    assert manifest["natural_language_proof_sketches"][0]["lean_verified"] is False
    assert (bundle_dir / "proof_attempt_ledger.jsonl").exists()
    assert "proof_attempt_ledger.jsonl" in {item["path"] for item in manifest["files"]}
    assert {item["path"]: item for item in manifest["files"]}["handoff_notes.md"]["sha256"]
    assert {item["path"]: item for item in manifest["files"]}["proof_attempt_ledger.jsonl"]["lean_verified_claim_source"] is False
    assert "Natural-language proof sketches are research evidence only" in proof_summary
    assert "`MathProject.identity_self` status=`lean_verified`" in proof_summary
    assert "Read `lean_build_report.json` and `verified_declarations.json` before citing any formal claim" in handoff_notes


def test_amra_result_bundle_flags_verified_declaration_model_mismatch(tmp_path: Path) -> None:
    project = _result_project(tmp_path)
    _write_json(
        project / "verified_declarations.json",
        {
            "schema_version": "amra.verified_declarations.v1",
            "declarations": [
                {
                    "name": "identity_self",
                    "full_name": "MathProject.identity_self",
                    "lean_name": "identity_self",
                    "status": "lean_verified",
                    "relative_path": "MathProject/Main.lean",
                    "statement": "theorem identity_self (n : Nat) : n = 0",
                }
            ],
        },
    )

    export_amra_result_bundle(project=project, output_dir=tmp_path / "bundle", repo_root=tmp_path)

    manifest = json.loads((tmp_path / "bundle" / "artifact_manifest.json").read_text(encoding="utf-8"))

    assert manifest["proof_loop_state"]["model_mismatch"]["status"] == "present"
    assert manifest["faithful_modeling"]["status"] == "model_mismatch"
    assert manifest["faithful_modeling"]["checks"][0]["status"] == "model_mismatch"


def test_amra_result_bundle_accepts_formalizer_report_contract(tmp_path: Path) -> None:
    project = _result_project(tmp_path)
    _write_json(
        project / "artifacts" / "lean_build_report.json",
        {
            "schema_version": "amra.lean_formalizer.report.v1",
            "status": "verified",
            "best_audit": {
                "build_status": "passed",
                "verified": True,
                "counts": {"sorry": 0, "axiom": 0, "constant": 0, "admit": 0, "placeholder": 0},
            },
        },
    )

    export_amra_result_bundle(project=project, output_dir=tmp_path / "bundle", repo_root=tmp_path)

    bundle_dir = tmp_path / "bundle"
    manifest = json.loads((bundle_dir / "artifact_manifest.json").read_text(encoding="utf-8"))
    build_report = json.loads((bundle_dir / "lean_build_report.json").read_text(encoding="utf-8"))
    blockers = (bundle_dir / "unresolved_blockers.md").read_text(encoding="utf-8")

    assert manifest["lean_build_report_status"] == "passed"
    assert manifest["verified_declaration_count"] == 1
    assert build_report["best_audit"]["verified"] is True
    assert "Lean build report status" not in blockers


def test_export_amra_result_bundle_cli_and_research_lab_schema(tmp_path: Path, monkeypatch) -> None:
    project = _result_project(tmp_path)
    output = tmp_path / "cli-bundle"
    monkeypatch.setenv("AMRA_REPO_ROOT", str(tmp_path))

    exit_code = main(["--json", "export-amra-result-bundle", "--project", str(project), "--output", str(output)])
    lab = yaml.safe_load((Path(__file__).resolve().parents[1] / "research_lab.yaml").read_text(encoding="utf-8"))

    assert exit_code == 0
    assert (output / "artifact_manifest.json").exists()
    assert lab["interfaces"]["bundle_schema"]["amra_result_bundle"]["schema_version"] == RESULT_BUNDLE_SCHEMA_VERSION
    assert "export-amra-result-bundle" in lab["interfaces"]["portfolio_commands"]
    assert "handoff_notes.md" in lab["interfaces"]["bundle_schema"]["amra_result_bundle"]["required_files"]


def test_portfolio_final_report_explains_every_disposition(tmp_path: Path) -> None:
    campaign = tmp_path / "artifacts" / "portfolio_campaigns" / "demo"
    _write_json(campaign / "campaign_manifest.json", {"campaign_id": "demo", "run_name": "Demo"})
    _write_json(
        campaign / "ranking.json",
        {
            "ranking": [
                {
                    "problem_id": "promote-me",
                    "title": "Promote Me",
                    "recommendation": "promote",
                    "priority": 31.5,
                    "has_exact_statement": True,
                    "risk_flags": [],
                    "primary_blocker": "",
                },
                {
                    "problem_id": "park-me",
                    "title": "Park Me",
                    "recommendation": "source_recover",
                    "priority": 4,
                    "has_exact_statement": False,
                    "risk_flags": ["needs_source"],
                    "primary_blocker": "needs_source",
                },
                {
                    "problem_id": "freeze-me",
                    "title": "Freeze Me",
                    "recommendation": "freeze",
                    "priority": -3,
                    "has_exact_statement": True,
                    "risk_flags": ["strong_counterexample"],
                    "primary_blocker": "counterexample",
                },
            ]
        },
    )
    _write_json(campaign / "promotion_queue.json", {"items": [{"problem_id": "promote-me"}]})
    _write_json(campaign / "parked_queue.json", {"items": [{"problem_id": "park-me"}, {"problem_id": "freeze-me"}]})

    report = write_portfolio_final_report(campaign, repo_root=tmp_path)
    text = (campaign / "final_report.md").read_text(encoding="utf-8")

    assert report["promoted_count"] == 1
    assert report["parked_count"] == 1
    assert report["frozen_count"] == 1
    assert "Disposition: `promoted`" in text
    assert "Disposition: `parked`" in text
    assert "Disposition: `frozen`" in text
    assert "Reason:" in text
