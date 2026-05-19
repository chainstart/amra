from __future__ import annotations

import importlib
from pathlib import Path

from amra.lean import (
    FormalizationPreparer,
    LeanExecutor,
    LeanFormalizerRunner,
    audit_lean_source_text,
)


def test_canonical_lean_imports_and_legacy_shims_share_identity() -> None:
    module_pairs = {
        "ara_math.lean": "amra.lean.executor",
        "ara_math.formalization": "amra.lean.formalization",
        "ara_math.lean_formalizer": "amra.lean.formalizer",
        "ara_math.lean_audit": "amra.lean.audit",
        "ara_math.lean_contract": "amra.lean.contract",
    }

    for legacy_name, canonical_name in module_pairs.items():
        assert importlib.import_module(legacy_name) is importlib.import_module(canonical_name)

    assert LeanExecutor is importlib.import_module("amra.lean.executor").LeanExecutor
    assert FormalizationPreparer is importlib.import_module("amra.lean.formalization").FormalizationPreparer
    assert LeanFormalizerRunner is importlib.import_module("amra.lean.formalizer").LeanFormalizerRunner


def test_lean_audit_counts_only_active_unsafe_constructs() -> None:
    audit = audit_lean_source_text(
        "\n".join(
            [
                "-- sorry in a line comment is ignored",
                "/- axiom ignored_in_block : False -/",
                "axiom unsafe_axiom : False",
                "theorem active_sorry : True := by",
                "  sorry",
                "theorem active_admit : True := by",
                "  admit",
                "def marker : String := \"ARA_MATH_PLACEHOLDER\"",
                "",
            ]
        )
    )

    assert audit == {
        "trust_level": "unsafe",
        "issue_count": 4,
        "counts": {
            "sorry": 1,
            "axiom": 1,
            "admit": 1,
            "placeholder": 1,
        },
    }


def test_formalizer_audit_output_is_deterministic_without_backend_calls(tmp_path: Path) -> None:
    workspace = tmp_path / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem target_claim : True := by",
                "  sorry",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )
    runner = LeanFormalizerRunner(repo_root=tmp_path)

    report = runner.run(
        workspace=workspace,
        statement="theorem target_claim : True := by\n  trivial",
        target_theorem="target_claim",
        target_file=Path("MathProject/MainClaim.lean"),
        build_command=["python3", "-c", "print('deterministic build')"],
        backend="none",
        attempts=0,
        output_root=tmp_path / "runs",
        run_name="audit-only",
    )

    best_audit = report["best_audit"]
    assert report["status"] == "blocked"
    assert report["attempts_completed"] == 0
    assert best_audit["build_status"] == "passed"
    assert best_audit["counts"]["sorry"] == 1
    assert best_audit["verified"] is False
    assert "Lean workspace still contains 1 `sorry` placeholder(s)." in best_audit["blockers"]
