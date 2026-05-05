import json
from pathlib import Path

from ara_math.orchestrator import MathResearchOrchestrator
from ara_math.problem_bank import save_problem_bank
from ara_math.models import ProblemRecord
from ara_math.review import MathReviewer


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_review_marks_open_problem_checkpoint_as_checkpoint_verified(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="checkpoint-problem",
                title="Checkpoint Problem",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                tags=["geometry"],
                open_problem=True,
                references=["/tmp/local-note.md", "/tmp/second-note.md"],
                metadata={"source_catalog": "erdosproblems"},
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="checkpoint-problem", name="checkpoint-problem-20260421")
    orchestrator.set_project_statement(project_dir, "A staged open-problem statement.", source="manual test")

    (project_dir / "proof").mkdir(exist_ok=True)
    (project_dir / "idea").mkdir(exist_ok=True)
    (project_dir / "formal" / "MathProject").mkdir(parents=True, exist_ok=True)
    (project_dir / "writing").mkdir(exist_ok=True)
    (project_dir / "artifacts").mkdir(exist_ok=True)

    (project_dir / "proof" / "proof_plan.json").write_text('{"tasks":[{"task_id":"t1"}]}\n', encoding="utf-8")
    (project_dir / "proof" / "claim_registry.json").write_text(
        json.dumps(
            {
                "claims": [
                    {
                        "claim_id": "checkpoint-problem:main",
                        "title": "Checkpoint Problem",
                        "statement": "A staged open-problem statement.",
                        "status": "formalization_in_progress",
                        "validation_mode": "lean",
                        "depends_on": [],
                        "evidence_paths": [],
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        json.dumps({"status": "generated", "readiness_tier": "promising"}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "math_idea_ledger.json").write_text(
        json.dumps({"themes": ["checkpoint theorem staging"]}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "literature_evidence.json").write_text(
        json.dumps(
            {
                "counts": {"known_results": 1, "proof_ingredients": 0, "modern_tools": 0, "open_gaps": 1},
                "source_attribution_count": 2,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "formal_preparation.json").write_text(
        json.dumps({"seed_family": "triangle_dissection", "placeholder_claim_count": 1}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "lean_build_report.json").write_text(
        json.dumps({"status": "passed", "sorry_count": 0, "summary": "Checkpoint build passed."}) + "\n",
        encoding="utf-8",
    )
    manuscript_path = project_dir / "writing" / "research_report.md"
    manuscript_path.write_text(
        "\n".join(
            [
                "# Checkpoint Problem",
                "",
                "## Summary",
                "",
                "Checkpoint report.",
                "",
                "## Exact Statement",
                "",
                "A staged open-problem statement.",
                "",
                "## Formalization Status",
                "",
                "- Lean build status: `passed`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "manuscript_report.json").write_text(
        json.dumps({"manuscript_path": str(manuscript_path)}) + "\n",
        encoding="utf-8",
    )

    (project_dir / "formal" / "MathProject" / "Basic.lean").write_text(
        "theorem clean_basic : True := by\n  trivial\n",
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").write_text(
        "theorem clean_generated : True := by\n  trivial\n",
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "/--",
                "ARA_MATH_PLACEHOLDER claim_id=checkpoint-problem:main",
                "Verified checkpoint marker for the open problem.",
                "-/",
                "theorem checkpoint_verified_main : True := by",
                "  trivial",
                "",
                "theorem checkpoint_transport : True := by",
                "  trivial",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    reviewer = MathReviewer()
    report = reviewer.review(project_dir)

    assert report["status"] == "checkpoint_verified"
    assert "placeholder" not in " ".join(report["blockers"]).lower()
    assert any("checkpoint" in warning.lower() for warning in report["warnings"])


def test_review_accepts_literature_recovered_statement_for_open_problem(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="recovered-problem",
                title="Recovered Problem",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                open_problem=True,
                references=["/tmp/local-note.md", "/tmp/second-note.md"],
                metadata={"source_catalog": "erdosproblems"},
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="recovered-problem", name="recovered-problem-20260421")

    (project_dir / "proof" / "proof_plan.json").write_text('{"tasks":[{"task_id":"t1"}]}\n', encoding="utf-8")
    (project_dir / "proof" / "claim_registry.json").write_text(json.dumps({"claims": []}) + "\n", encoding="utf-8")
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        json.dumps({"status": "generated", "readiness_tier": "promising"}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "math_idea_ledger.json").write_text(json.dumps({"themes": ["recovered statement"]}) + "\n", encoding="utf-8")
    (project_dir / "idea" / "statement_recovery.json").write_text(
        json.dumps(
            {
                "status": "recovered",
                "statement": "There are finitely many unitary perfect numbers.",
                "source": "/tmp/research-note.md",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "literature_evidence.json").write_text(
        json.dumps(
            {
                "counts": {"known_results": 1, "proof_ingredients": 1, "modern_tools": 0, "open_gaps": 0},
                "source_attribution_count": 2,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "formal_preparation.json").write_text(json.dumps({"seed_family": "number_theory"}) + "\n", encoding="utf-8")
    (project_dir / "artifacts" / "lean_build_report.json").write_text(
        json.dumps({"status": "passed", "sorry_count": 1, "summary": "Recovered statement build still has placeholders."}) + "\n",
        encoding="utf-8",
    )
    manuscript_path = project_dir / "writing" / "research_report.md"
    manuscript_path.write_text(
        "\n".join(
            [
                "# Recovered Problem",
                "",
                "## Summary",
                "",
                "Recovered statement report.",
                "",
                "## Exact Statement",
                "",
                "There are finitely many unitary perfect numbers.",
                "",
                "## Formalization Status",
                "",
                "- Lean build status: `passed`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "manuscript_report.json").write_text(
        json.dumps({"manuscript_path": str(manuscript_path)}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(
        "theorem placeholder_main : True := by\n  sorry\n",
        encoding="utf-8",
    )

    reviewer = MathReviewer()
    report = reviewer.review(project_dir)

    assert not any("exact mathematical statement has not been supplied yet" in blocker.lower() for blocker in report["blockers"])
    assert any("literature-recovered exact statement" in warning.lower() for warning in report["warnings"])


def test_review_blocks_untrusted_external_main_claim_dependency(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="unsafe-import-problem",
                title="Unsafe Import Problem",
                source="test",
                statement="Determine whether there are finitely many unitary perfect numbers.",
                domain="number_theory",
                tags=["unitary_perfect"],
                open_problem=False,
                references=["/tmp/local-note.md", "/tmp/second-note.md"],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="unsafe-import-problem", name="unsafe-import-problem-20260425")
    orchestrator.set_project_statement(project_dir, "Determine whether there are finitely many unitary perfect numbers.", source="manual test")

    (project_dir / "proof").mkdir(exist_ok=True)
    (project_dir / "idea").mkdir(exist_ok=True)
    (project_dir / "formal" / "MathProject").mkdir(parents=True, exist_ok=True)
    (project_dir / "writing").mkdir(exist_ok=True)
    (project_dir / "artifacts").mkdir(exist_ok=True)

    (project_dir / "proof" / "proof_plan.json").write_text('{"tasks":[{"task_id":"t1"}]}\n', encoding="utf-8")
    (project_dir / "proof" / "claim_registry.json").write_text(json.dumps({"claims": []}) + "\n", encoding="utf-8")
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        json.dumps({"status": "generated", "readiness_tier": "promising"}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "math_idea_ledger.json").write_text(
        json.dumps({"themes": ["unsafe import staging"]}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "literature_evidence.json").write_text(
        json.dumps({"counts": {"known_results": 1}, "source_attribution_count": 2}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "formal_preparation.json").write_text(
        json.dumps({"seed_family": "unitary_perfect", "main_claim_seed": {"name": "unitary_perfect_finite", "trust_level": "unsafe"}})
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "lean_build_report.json").write_text(
        json.dumps({"status": "passed", "sorry_count": 0, "summary": "Imported external theorem builds cleanly."}) + "\n",
        encoding="utf-8",
    )
    manuscript_path = project_dir / "writing" / "research_report.md"
    manuscript_path.write_text(
        "\n".join(
            [
                "# Unsafe Import Problem",
                "",
                "## Summary",
                "",
                "Imported theorem report.",
                "",
                "## Exact Statement",
                "",
                "Determine whether there are finitely many unitary perfect numbers.",
                "",
                "## Formalization Status",
                "",
                "- Lean build status: `passed`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "manuscript_report.json").write_text(
        json.dumps({"manuscript_path": str(manuscript_path)}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "Basic.lean").write_text("theorem clean_basic : True := by\n  trivial\n", encoding="utf-8")
    (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").write_text(
        "theorem clean_generated : True := by\n  trivial\n",
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "import MathProject.GeneratedClaims",
                "import Mathlib.NumberTheory.UnitaryPerfect.Finiteness",
                "",
                "namespace MathProject",
                "",
                "theorem imported_main : Set.Finite {n : ℕ | True} := by",
                "  exact UnitaryPerfect.unitary_perfect_finite",
                "",
                "end MathProject",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    reviewer = MathReviewer()
    report = reviewer.review(project_dir)

    assert report["status"] == "blocked"
    assert any("external companion theorem" in blocker.lower() and "`unsafe`" in blocker for blocker in report["blockers"])


def test_review_does_not_treat_benchmark_shell_as_converged_open_problem(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="benchmark-problem",
                title="Benchmark Problem",
                source="Erdős Problems",
                statement="Determine whether an equilateral triangle can be dissected into 17 congruent triangles.",
                domain="geometry",
                open_problem=True,
                references=["/tmp/local-note.md", "/tmp/second-note.md"],
                metadata={"source_catalog": "erdosproblems"},
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="benchmark-problem", name="benchmark-problem-20260421")
    orchestrator.set_project_statement(project_dir, "Determine whether an equilateral triangle can be dissected into 17 congruent triangles.", source="manual")

    (project_dir / "proof" / "proof_plan.json").write_text('{"tasks":[{"task_id":"t1"}]}\n', encoding="utf-8")
    (project_dir / "proof" / "claim_registry.json").write_text(
        json.dumps(
            {
                "claims": [
                    {
                        "claim_id": "benchmark-problem:main",
                        "title": "Benchmark Problem",
                        "statement": "Determine whether an equilateral triangle can be dissected into 17 congruent triangles.",
                        "status": "lean_verified",
                        "validation_mode": "lean",
                        "depends_on": [],
                        "evidence_paths": [str(project_dir / "formal" / "MathProject" / "MainClaim.lean")],
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        json.dumps({"status": "generated", "readiness_tier": "promising"}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "math_idea_ledger.json").write_text(
        json.dumps({"themes": ["triangle-dissection benchmark"]}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "literature_evidence.json").write_text(
        json.dumps({"counts": {"known_results": 1, "proof_ingredients": 1, "modern_tools": 0, "open_gaps": 1}, "source_attribution_count": 2}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "formal_preparation.json").write_text(json.dumps({"seed_family": "triangle_dissection"}) + "\n", encoding="utf-8")
    (project_dir / "artifacts" / "lean_build_report.json").write_text(
        json.dumps({"status": "passed", "sorry_count": 0, "summary": "Benchmark shell passes Lean."}) + "\n",
        encoding="utf-8",
    )
    manuscript_path = project_dir / "writing" / "research_report.md"
    manuscript_path.write_text(
        "\n".join(
            [
                "# Benchmark Problem",
                "",
                "## Summary",
                "",
                "Benchmark shell report.",
                "",
                "## Exact Statement",
                "",
                "Determine whether an equilateral triangle can be dissected into 17 congruent triangles.",
                "",
                "## Formalization Status",
                "",
                "- Lean build status: `passed`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "manuscript_report.json").write_text(json.dumps({"manuscript_path": str(manuscript_path)}) + "\n", encoding="utf-8")
    (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").write_text("theorem seeded_lemma : True := by\n  trivial\n", encoding="utf-8")
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "def triangle_dissection_17_problem : Prop :=",
                "  True",
                "",
                "theorem triangle_dissection_17_one_possible : True := by",
                "  trivial",
                "",
                "theorem triangle_dissection_17_square_benchmark : True := by",
                "  trivial",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    reviewer = MathReviewer()
    report = reviewer.review(project_dir)
    registry = json.loads((project_dir / "proof" / "claim_registry.json").read_text(encoding="utf-8"))

    assert report["status"] == "checkpoint_verified"
    assert any("benchmark/checkpoint shell" in warning.lower() for warning in report["warnings"])
    assert registry["claims"][0]["status"] == "formalization_in_progress"


def test_review_treats_proof_contract_marker_as_checkpoint(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="contract-problem",
                title="Contract Problem",
                source="Erdős Problems",
                statement="Open problem contract statement.",
                domain="number_theory",
                open_problem=True,
                references=["/tmp/local-note.md", "/tmp/second-note.md"],
                metadata={"source_catalog": "erdosproblems"},
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="contract-problem", name="contract-problem-20260422")
    orchestrator.set_project_statement(project_dir, "Open problem contract statement.", source="manual")

    (project_dir / "proof" / "proof_plan.json").write_text('{"tasks":[{"task_id":"t1"}]}\n', encoding="utf-8")
    (project_dir / "proof" / "claim_registry.json").write_text(
        json.dumps(
            {
                "claims": [
                    {
                        "claim_id": "contract-problem:main",
                        "title": "Contract Problem",
                        "statement": "Open problem contract statement.",
                        "status": "formalization_in_progress",
                        "validation_mode": "lean",
                        "depends_on": [],
                        "evidence_paths": [str(project_dir / "formal" / "MathProject" / "MainClaim.lean")],
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        json.dumps({"status": "generated", "readiness_tier": "needs_statement_recovery"}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "math_idea_ledger.json").write_text(
        json.dumps({"themes": ["proof contract checkpoint"]}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "literature_evidence.json").write_text(
        json.dumps({"counts": {"known_results": 1, "proof_ingredients": 1, "modern_tools": 0, "open_gaps": 0}, "source_attribution_count": 2}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "formal_preparation.json").write_text(
        json.dumps({"seed_family": "prime_gap_spectrum", "placeholder_claim_count": 1}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "lean_build_report.json").write_text(
        json.dumps({"status": "passed", "sorry_count": 0, "summary": "Proof contract checkpoint passes Lean."}) + "\n",
        encoding="utf-8",
    )
    manuscript_path = project_dir / "writing" / "research_report.md"
    manuscript_path.write_text(
        "\n".join(
            [
                "# Contract Problem",
                "",
                "## Summary",
                "",
                "Proof contract report.",
                "",
                "## Exact Statement",
                "",
                "Open problem contract statement.",
                "",
                "## Formalization Status",
                "",
                "- Lean build status: `passed`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "manuscript_report.json").write_text(
        json.dumps({"manuscript_path": str(manuscript_path)}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").write_text(
        "theorem contract_generated : True := by\n  trivial\n",
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "/--",
                "ARA_MATH_PLACEHOLDER claim_id=contract-problem:main",
                "This attempt records a precise proof contract instead of asserting the open problem.",
                "A future proof of `ContractTarget` can be threaded through this theorem.",
                "-/",
                "def ContractTarget : Prop :=",
                "  True",
                "",
                "theorem contract_problem_main (hTarget : ContractTarget) : ContractTarget := by",
                "  exact hTarget",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    reviewer = MathReviewer()
    report = reviewer.review(project_dir)

    assert report["status"] == "checkpoint_verified"
    assert not any("generated placeholder claims" in blocker.lower() for blocker in report["blockers"])
    assert any("checkpoint" in warning.lower() for warning in report["warnings"])


def test_review_treats_reduction_main_theorem_as_checkpoint(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    (project_dir / "formal" / "MathProject").mkdir(parents=True)
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "proof").mkdir(parents=True)
    (project_dir / "writing").mkdir(parents=True)
    (project_dir / "artifacts").mkdir(parents=True)
    (project_dir / "project_manifest.json").write_text(
        json.dumps(
            {
                "project_name": "reduction-problem",
                "problem": {
                    "problem_id": "erdos-1052",
                    "title": "Finite Number of Unitary Perfect Numbers",
                    "source": "Erdős Problems",
                    "statement": "There are finitely many unitary perfect numbers.",
                    "open_problem": True,
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "problem_context.json").write_text(
        json.dumps({"exact_statement_status": "provided", "exact_statement_source": "manual"}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "exact_statement.md").write_text(
        "There are finitely many unitary perfect numbers.\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "references.json").write_text(
        json.dumps({"references": ["https://example.com/ref1", "https://example.com/ref2"]}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "proof" / "proof_plan.json").write_text(
        json.dumps({"tasks": [{"title": "main", "task_type": "lemma_formalization", "validation_mode": "lean", "success_contract": "pass", "description": "desc"}]}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "proof" / "claim_registry.json").write_text(
        json.dumps({"claims": [{"claim_id": "erdos-1052:main", "title": "Main", "statement": "There are finitely many unitary perfect numbers.", "validation_mode": "lean", "status": "formalization_in_progress"}]}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        json.dumps({"status": "generated", "readiness_tier": "promising"}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "math_idea_ledger.json").write_text(
        json.dumps({"themes": ["unitary perfect reduction"]}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "literature_evidence.json").write_text(
        json.dumps({"counts": {"known_results": 2, "proof_ingredients": 1, "modern_tools": 1, "open_gaps": 0}, "source_attribution_count": 2}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "formal_preparation.json").write_text(
        json.dumps({"seed_family": "unitary_perfect", "placeholder_claim_count": 0}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "lean_build_report.json").write_text(
        json.dumps({"status": "passed", "sorry_count": 0, "summary": "Reduction theorem passes Lean."}) + "\n",
        encoding="utf-8",
    )
    manuscript_path = project_dir / "writing" / "research_report.md"
    manuscript_path.write_text(
        "\n".join(
            [
                "# Reduction Problem",
                "",
                "## Summary",
                "",
                "Reduction theorem report.",
                "",
                "## Exact Statement",
                "",
                "There are finitely many unitary perfect numbers.",
                "",
                "## Formalization Status",
                "",
                "- Lean build status: `passed`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "manuscript_report.json").write_text(
        json.dumps({"manuscript_path": str(manuscript_path)}) + "\n",
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").write_text(
        "theorem reduction_generated : True := by\n  trivial\n",
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "def erdos_1052_main_statement : Prop :=",
                "  True",
                "",
                "/-- Boundedness reduction for the main claim. -/",
                "theorem erdos_1052_main_of_bounded (hB : erdos_1052_main_statement) :",
                "    erdos_1052_main_statement := by",
                "  exact hB",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    reviewer = MathReviewer()
    report = reviewer.review(project_dir)

    assert report["status"] == "checkpoint_verified"
    assert any("checkpoint" in warning.lower() or "shell" in warning.lower() for warning in report["warnings"])
