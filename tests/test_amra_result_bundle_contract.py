from __future__ import annotations

import json
from pathlib import Path

from amra.result_bundle import REQUIRED_BUNDLE_FILES, export_amra_result_bundle
from ara_math.cli import main


FIXTURE_PROJECT = Path(__file__).resolve().parent / "fixtures" / "amra_contract_project"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_contract_fixture_exports_separated_ara_bundle(tmp_path: Path) -> None:
    output = tmp_path / "bundle"

    result = export_amra_result_bundle(project=FIXTURE_PROJECT, output_dir=output, repo_root=FIXTURE_PROJECT.parents[2])

    manifest = _load_json(output / "artifact_manifest.json")
    sketches = _load_json(output / "natural_language_proof_sketches.json")
    declarations = _load_json(output / "verified_declarations.json")
    proof_summary = (output / "proof_summary.md").read_text(encoding="utf-8")
    blockers = (output / "unresolved_blockers.md").read_text(encoding="utf-8")
    limitations = (output / "limitations.md").read_text(encoding="utf-8")
    writing_brief = (output / "writing_brief.md").read_text(encoding="utf-8")

    assert set(REQUIRED_BUNDLE_FILES) == set(result["required_files"])
    assert set(REQUIRED_BUNDLE_FILES) <= {path.name for path in output.iterdir()}

    assert manifest["verification_policy"]["only_lean_verified_claim_source"] == "verified_declarations.json"
    assert manifest["verification_policy"]["natural_language_proof_sketches_source"] == "natural_language_proof_sketches.json"
    assert manifest["verification_policy"]["natural_language_proof_sketches_are_not_lean_verified"] is True
    assert manifest["verified_declaration_count"] == 1
    assert manifest["natural_language_proof_sketch_count"] >= 1
    assert manifest["unresolved_blocker_count"] >= 1
    assert manifest["limitation_count"] >= 1

    file_contract = {item["path"]: item for item in manifest["files"]}
    assert file_contract["verified_declarations.json"]["lean_verified_claim_source"] is True
    assert file_contract["natural_language_proof_sketches.json"]["lean_verified_claim_source"] is False
    assert file_contract["proof_summary.md"]["lean_verified_claim_source"] is False
    assert file_contract["writing_brief.md"]["lean_verified_claim_source"] is False

    assert sketches["lean_verified"] is False
    assert sketches["ara_contract_role"] == "research_evidence_only"
    assert all(item["lean_verified"] is False for item in sketches["sketches"])
    assert "ContractFixture.sketch_claim is Lean verified" in json.dumps(sketches)

    exported_names = [item["full_name"] for item in declarations["declarations"]]
    assert exported_names == ["ContractFixture.verified_identity"]
    assert "ContractFixture.sketch_claim" not in json.dumps(declarations)

    assert "ContractFixture.sketch_claim is Lean verified" not in proof_summary
    assert "natural_language_proof_sketches.json" in proof_summary
    assert "The normalization lemma needed by the sketch has not been proved in Lean." in blockers
    assert "Natural-language proof sketches are research evidence only" in limitations
    assert "Unresolved blockers remain" in limitations
    assert "Do not cite a natural-language proof sketch as a Lean-verified theorem" in writing_brief


def test_contract_fixture_cli_export_preserves_amra_entrypoint(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "cli-bundle"
    monkeypatch.setenv("AMRA_REPO_ROOT", str(FIXTURE_PROJECT.parents[2]))

    exit_code = main(["export-amra-result-bundle", "--project", str(FIXTURE_PROJECT), "--output", str(output), "--json"])

    assert exit_code == 0
    assert (output / "artifact_manifest.json").exists()
    assert (output / "natural_language_proof_sketches.json").exists()
    assert (output / "limitations.md").exists()
