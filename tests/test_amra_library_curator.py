from __future__ import annotations

import json
from pathlib import Path

from amra.cli import main as amra_main
from amra.library_curator import (
    LIBRARY_CURATOR_REPORT_SCHEMA_VERSION,
    REUSABLE_LEMMA_METADATA_SCHEMA_VERSION,
    curate_library_candidates,
)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _faithfulness_candidate_dir(tmp_path: Path) -> Path:
    bundle = tmp_path / "bundle"
    _write_json(
        bundle / "verified_declarations.json",
        {
            "schema_version": "amra.verified_declarations.v1",
            "declarations": [
                {
                    "name": "identity_self",
                    "full_name": "AMRA.Test.identity_self",
                    "kind": "theorem",
                    "status": "lean_verified",
                    "lean_verified": True,
                    "statement": "theorem identity_self (n : Nat) : n = n",
                    "relative_path": "formal/Test.lean",
                    "lean_build_report_status": "passed",
                    "verification_basis": "verified_declarations.json",
                },
                {
                    "name": "sketch_only",
                    "full_name": "AMRA.Test.sketch_only",
                    "status": "sketch",
                    "statement": "theorem sketch_only (n : Nat) : n = n",
                },
                {
                    "name": "missing_statement",
                    "full_name": "AMRA.Test.missing_statement",
                    "status": "lean_verified",
                    "lean_verified": True,
                },
            ],
        },
    )
    candidates = tmp_path / "faithfulness"
    _write_json(
        candidates / "faithfulness_report.json",
        {
            "schema_version": "amra.nl_lean_faithfulness.report.v1",
            "status": "passed",
            "bundle_kind": "amra_result_bundle",
            "bundle_dir": str(bundle),
            "taxonomy_counts": {"faithfully_modeled": 1},
            "checks": [
                {
                    "kind": "formal_statement_to_verified_declaration",
                    "status": "matched",
                    "taxonomy": "faithfully_modeled",
                    "declaration": "AMRA.Test.identity_self",
                    "matched": True,
                }
            ],
        },
    )
    return candidates


def test_library_curator_promotes_only_verified_reusable_declarations(tmp_path: Path) -> None:
    report = curate_library_candidates(
        candidates=_faithfulness_candidate_dir(tmp_path),
        output_dir=tmp_path / "curator",
    )

    metadata = json.loads((tmp_path / "curator" / "reusable_lemma_metadata.json").read_text(encoding="utf-8"))
    rejection = json.loads((tmp_path / "curator" / "rejection_reasons.json").read_text(encoding="utf-8"))
    records = [
        json.loads(line)
        for line in (tmp_path / "curator" / "curator_review_records.jsonl").read_text(encoding="utf-8").splitlines()
    ]

    assert report["schema_version"] == LIBRARY_CURATOR_REPORT_SCHEMA_VERSION
    assert report["promoted_count"] == 1
    assert report["rejected_count"] == 2
    assert report["promotion_policy"]["verified_only"] is True
    assert metadata["schema_version"] == REUSABLE_LEMMA_METADATA_SCHEMA_VERSION
    assert metadata["lemmas"][0]["full_name"] == "AMRA.Test.identity_self"
    assert metadata["lemmas"][0]["reusable"] is True
    assert any("not a Lean-verified declaration" in reason for reason in rejection["reason_counts"])
    assert any("reusable Lean statement" in reason for reason in rejection["reason_counts"])
    assert {record["decision"] for record in records} == {"promote", "reject"}


def test_library_curator_cli_writes_review_artifacts(tmp_path: Path, capsys) -> None:
    exit_code = amra_main(
        [
            "--json",
            "library",
            "curate",
            "--candidates",
            str(_faithfulness_candidate_dir(tmp_path)),
            "--out",
            str(tmp_path / "curator"),
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["promoted_count"] == 1
    assert (tmp_path / "curator" / "library_curator_report.json").exists()
    assert (tmp_path / "curator" / "promoted_library_candidates.json").exists()
    assert "Natural-language sketches" in (tmp_path / "curator" / "summary.md").read_text(encoding="utf-8")


def test_library_curator_rejects_unsupported_candidate_directory(tmp_path: Path) -> None:
    report = curate_library_candidates(candidates=tmp_path / "empty", output_dir=tmp_path / "curator")

    assert report["review_count"] == 1
    assert report["promoted_count"] == 0
    assert report["rejected"][0]["candidate_id"] == "unsupported-input"
