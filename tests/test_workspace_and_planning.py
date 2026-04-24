import json
from pathlib import Path
from subprocess import CompletedProcess

from ara_math.orchestrator import MathResearchOrchestrator
from ara_math.problem_bank import save_problem_bank
from ara_math.models import ProblemRecord


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_create_project_and_generate_plan(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="toy-problem",
                title="Toy Problem",
                source="test",
                statement="Prove or refute the toy problem.",
                domain="number_theory",
                tags=["computational_search"],
                open_problem=True,
                formalized="no",
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )

    project_dir = orchestrator.create_project(problem_id="toy-problem", name="toy-problem-20260421")
    plan = orchestrator.plan_project(project_dir)

    assert (project_dir / "formal" / "MathProject" / "Basic.lean").exists()
    assert (project_dir / "proof" / "proof_plan.json").exists()
    assert (project_dir / "proof" / "theorem_inventory.json").exists()
    assert (project_dir / "proof" / "theorem_graph.json").exists()
    assert (project_dir / "proof" / "proof_path_frameworks.json").exists()
    assert (project_dir / "proof" / "route_candidates.json").exists()
    assert (project_dir / "proof" / "proof_route_scaffold.json").exists()
    assert (project_dir / "proof" / "route_discovery_brief.json").exists()
    assert (project_dir / "proof" / "mathematical_blockers.json").exists()
    assert (project_dir / "proof" / "selected_route.md").exists()
    assert (project_dir / "idea" / "exact_statement.md").exists()
    assert (project_dir / "idea" / "proof_path_assessment.json").exists()
    assert (project_dir / "idea" / "math_idea_ledger.json").exists()
    assert '"path":' in (project_dir / "project_manifest.json").read_text(encoding="utf-8")
    assert '"mode": "auto"' in (project_dir / "idea" / "deliverable_override.json").read_text(encoding="utf-8")
    assert len(plan["tasks"]) >= 6
    assert any(task["task_type"] == "counterexample_search" for task in plan["tasks"])


def test_plan_project_builds_theorem_inventory_and_route_scaffold(tmp_path: Path) -> None:
    source_doc = tmp_path / "triangle_notes.md"
    source_doc.write_text(
        "\n".join(
            [
                "# Triangle Notes",
                "",
                "**Problem Statement**: For which values of n can an equilateral triangle be dissected into n congruent triangles?",
                "Triangle Tiling II: Nonexistence theorems.",
                "Impossibility of n = 7.",
                "Model as triangulation graph.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="triangle-proof-routes",
                title="Triangle Route Problem",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                tags=["geometry"],
                open_problem=True,
                references=[str(source_doc)],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )

    project_dir = orchestrator.create_project(problem_id="triangle-proof-routes", name="triangle-proof-routes-20260422")
    plan = orchestrator.plan_project(project_dir)
    theorem_inventory = json.loads((project_dir / "proof" / "theorem_inventory.json").read_text(encoding="utf-8"))
    theorem_graph = json.loads((project_dir / "proof" / "theorem_graph.json").read_text(encoding="utf-8"))
    frameworks = json.loads((project_dir / "proof" / "proof_path_frameworks.json").read_text(encoding="utf-8"))
    route_candidates = json.loads((project_dir / "proof" / "route_candidates.json").read_text(encoding="utf-8"))
    route_scaffold = json.loads((project_dir / "proof" / "proof_route_scaffold.json").read_text(encoding="utf-8"))
    route_discovery = json.loads((project_dir / "proof" / "route_discovery_brief.json").read_text(encoding="utf-8"))
    mathematical_blockers = json.loads((project_dir / "proof" / "mathematical_blockers.json").read_text(encoding="utf-8"))
    selected_route = (project_dir / "proof" / "selected_route.md").read_text(encoding="utf-8")

    assert theorem_inventory["entry_count"] >= 1
    assert theorem_graph["node_count"] >= theorem_inventory["entry_count"]
    assert theorem_graph["edge_count"] >= 1
    assert any(entry["role"] in {"obstruction", "supporting_lemma"} for entry in theorem_inventory["entries"])
    assert frameworks["framework_count"] >= 2
    assert route_candidates["candidate_count"] >= 2
    assert route_candidates["selected_route_id"] == frameworks["recommended_framework_id"]
    assert frameworks["recommended_framework_id"]
    assert route_scaffold["selected_framework_id"] == frameworks["recommended_framework_id"]
    assert route_scaffold["next_formal_obligations"]
    assert route_discovery["preferred_framework_id"] == frameworks["recommended_framework_id"]
    assert route_discovery["route_candidates"]
    assert route_discovery["anti_patterns"]
    assert mathematical_blockers["blocker_count"] >= 1
    assert "## Mathematical Objective" in selected_route
    assert any(task["task_type"] == "proof_route_scaffold" for task in plan["tasks"])
    assert any(task["task_type"] == "theorem_graph_construction" for task in plan["tasks"])
    assert any(task["task_type"] == "paper_first_route_selection" for task in plan["tasks"])
    assert any("Recommended proof framework:" in note for note in plan["notes"])
    assert any("Paper-first selected route:" in note for note in plan["notes"])


def test_prepare_formal_and_review_report_blocked_on_placeholders(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="proof-problem",
                title="Proof Problem",
                source="test",
                statement="Prove the proof problem exactly.",
                domain="number_theory",
                tags=["formalization_candidate"],
                references=["https://example.com/ref1", "https://example.com/ref2"],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="proof-problem", name="proof-problem-20260421")
    orchestrator.plan_project(project_dir)
    preparation = orchestrator.prepare_formal(project_dir)

    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    build = orchestrator.build_lean(project_dir, timeout_sec=1)
    manuscript = orchestrator.write_manuscript(project_dir)
    review = orchestrator.review_project(project_dir)
    manuscript_text = Path(manuscript["manuscript_path"]).read_text(encoding="utf-8")

    assert preparation["placeholder_claim_count"] > 0
    assert "import MathProject.GeneratedClaims" in (project_dir / "formal" / "MathProject.lean").read_text(encoding="utf-8")
    assert build["status"] == "needs_attention"
    assert manuscript["deliverable_type"] == "research_report"
    assert manuscript["manuscript_path"].endswith("research_report.md")
    assert "## Literature Evidence" in manuscript_text
    assert review["status"] == "blocked"
    assert any("Lean build status is `needs_attention`" in blocker for blocker in review["blockers"])
    assert any("exact mathematical statement" in blocker for blocker in review["blockers"])
    assert any("No structured literature evidence" in warning for warning in review["warnings"])


def test_review_can_become_ready_after_exact_statement_and_clean_formal_sources(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="clean-problem",
                title="Clean Problem",
                source="test",
                statement="Placeholder statement.",
                domain="number_theory",
                open_problem=False,
                references=["https://example.com/ref1", "https://example.com/ref2"],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="clean-problem", name="clean-problem-20260421")
    orchestrator.set_project_statement(project_dir, "For all n, the clean problem holds.", source="manual test")
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)

    (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").write_text(
        "\n".join(
            [
                "import MathProject.Basic",
                "",
                "namespace MathProject",
                "",
                "theorem clean_problem_definitions : True := by",
                "  trivial",
                "",
                "theorem clean_problem_lemmas : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "import MathProject.GeneratedClaims",
                "",
                "namespace MathProject",
                "",
                "theorem clean_problem_main : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    build = orchestrator.build_lean(project_dir, timeout_sec=1)
    manuscript = orchestrator.write_manuscript(project_dir)
    review = orchestrator.review_project(project_dir)
    manuscript_text = Path(manuscript["manuscript_path"]).read_text(encoding="utf-8")

    assert build["status"] == "passed"
    assert manuscript["deliverable_type"] == "formalization_note"
    assert manuscript["manuscript_path"].endswith("formalization_note.md")
    assert "## Literature Evidence" in manuscript_text
    assert review["status"] == "ready_for_human_review"
    claim_registry = (project_dir / "proof" / "claim_registry.json").read_text(encoding="utf-8")
    assert "lean_verified" in claim_registry


def test_prepare_formal_preserves_clean_manual_files(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="preserve-problem",
                title="Preserve Problem",
                source="test",
                statement="Preserve manually written claims.",
                domain="number_theory",
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="preserve-problem", name="preserve-problem-20260421")
    orchestrator.plan_project(project_dir)
    generated_claims = project_dir / "formal" / "MathProject" / "GeneratedClaims.lean"
    main_claim = project_dir / "formal" / "MathProject" / "MainClaim.lean"
    generated_claims.write_text("import MathProject.Basic\n\nnamespace MathProject\n\ntheorem keep_me : True := by\n  trivial\n\nend MathProject\n", encoding="utf-8")
    main_claim.write_text("import MathProject.GeneratedClaims\n\nnamespace MathProject\n\ntheorem keep_main : True := by\n  trivial\n\nend MathProject\n", encoding="utf-8")

    report = orchestrator.prepare_formal(project_dir)

    assert str(generated_claims) in report["preserved_files"]
    assert str(main_claim) in report["preserved_files"]
    assert "keep_me" in generated_claims.read_text(encoding="utf-8")


def test_prepare_formal_overwrites_builtin_empty_templates(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="template-problem",
                title="Template Problem",
                source="test",
                statement="Overwrite the empty built-in template.",
                domain="number_theory",
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="template-problem", name="template-problem-20260421")
    orchestrator.plan_project(project_dir)

    report = orchestrator.prepare_formal(project_dir)
    generated_claims = (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").read_text(encoding="utf-8")
    main_claim = (project_dir / "formal" / "MathProject" / "MainClaim.lean").read_text(encoding="utf-8")
    proof_gap_notes = (project_dir / "proof" / "proof_gap_notes.md").read_text(encoding="utf-8")

    assert report["placeholder_claim_count"] > 0
    assert "ARA_MATH_PLACEHOLDER claim_id=" in generated_claims
    assert "theorem" in main_claim
    assert "## Recommended Route Scaffold" in proof_gap_notes
    assert "## Next Formal Obligation" in proof_gap_notes


def test_prepare_formal_seeds_weird_number_family_from_local_asset(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="erdos-825-weird",
                title="Weird Numbers Abundance Index Conjecture",
                source="test",
                statement="Does every weird number have abundance index C = 3?",
                domain="number_theory",
                tags=["weird_numbers"],
            )
        ],
        bank_path,
    )
    asset_root = tmp_path / "formal-math" / "erdos-825-weird"
    (asset_root / "WeirdNumbers").mkdir(parents=True)
    (asset_root / "WeirdNumbers" / "Basic.lean").write_text(
        "\n".join(
            [
                "import Mathlib.Data.Nat.Divisors",
                "open BigOperators Finset",
                "",
                "namespace Nat",
                "",
                "def properDivisorSum (n : ℕ) : ℕ :=",
                "  (divisors n).sum id - n",
                "",
                "def IsAbundant (n : ℕ) : Prop :=",
                "  properDivisorSum n > n",
                "",
                "def IsSemiperfect (n : ℕ) : Prop :=",
                "  ∃ s : Finset ℕ, s.sum id = n",
                "",
                "def IsWeird (n : ℕ) : Prop :=",
                "  IsAbundant n ∧ ¬ IsSemiperfect n",
                "",
                "def abundanceIndex (n : ℕ) : ℕ :=",
                "  n",
                "",
                    "def weirdNumbers : List ℕ :=",
                    "  [70]",
                    "",
                    "axiom weird_abundance_index_three : ∀ n : ℕ, IsWeird n → abundanceIndex n = 3",
                    "",
                    "/-! ## Basic Properties -/",
                ]
            ),
            encoding="utf-8",
        )

    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="erdos-825-weird", name="erdos-825-weird-20260421")
    orchestrator.plan_project(project_dir)
    proof_path = json.loads((project_dir / "idea" / "proof_path_assessment.json").read_text(encoding="utf-8"))
    proof_path["local_assets"] = [{"kind": "local_project_dir", "path": str(asset_root)}]
    (project_dir / "idea" / "proof_path_assessment.json").write_text(json.dumps(proof_path, indent=2), encoding="utf-8")

    report = orchestrator.prepare_formal(project_dir)
    basic_text = (project_dir / "formal" / "MathProject" / "Basic.lean").read_text(encoding="utf-8")
    main_text = (project_dir / "formal" / "MathProject" / "MainClaim.lean").read_text(encoding="utf-8")
    generated_text = (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").read_text(encoding="utf-8")
    porting_candidates = json.loads((project_dir / "proof" / "porting_candidates.json").read_text(encoding="utf-8"))

    assert report["seed_family"] == "weird_numbers"
    assert "def IsWeird" in basic_text
    assert "theorem erdos_825_weird_definitions" in generated_text
    assert "Nat.abundanceIndex n = 3" in main_text
    assert any(candidate["name"] == "weird_abundance_index_three" for candidate in porting_candidates["candidates"])


def test_prepare_formal_seeds_unitary_family_from_companion_build_root(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="erdos-1052",
                title="Finite Number of Unitary Perfect Numbers",
                source="test",
                statement="Determine whether there are only finitely many unitary perfect numbers.",
                domain="number_theory",
                tags=["unitary_perfect"],
            )
        ],
        bank_path,
    )
    asset_root = tmp_path / "formal-math" / "erdos-1052-unitary-perfect"
    (asset_root / ".lake" / "build" / "lib" / "lean").mkdir(parents=True)
    (asset_root / "lean").mkdir(parents=True)
    (asset_root / "lean" / "GotoBound.lean").write_text(
        "\n".join(
            [
                "namespace Goto",
                "",
                "theorem upn_finite_goto : Set.Finite {N : ℕ | Nat.UnitaryPerfect N} := by",
                "  sorry",
                "",
                "end Goto",
                "",
            ]
        ),
        encoding="utf-8",
    )

    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="erdos-1052", name="erdos-1052-20260421")
    orchestrator.plan_project(project_dir)
    proof_path = json.loads((project_dir / "idea" / "proof_path_assessment.json").read_text(encoding="utf-8"))
    proof_path["local_assets"] = [{"kind": "local_project_dir", "path": str(asset_root)}]
    (project_dir / "idea" / "proof_path_assessment.json").write_text(json.dumps(proof_path, indent=2), encoding="utf-8")

    report = orchestrator.prepare_formal(project_dir)
    basic_text = (project_dir / "formal" / "MathProject" / "Basic.lean").read_text(encoding="utf-8")
    main_text = (project_dir / "formal" / "MathProject" / "MainClaim.lean").read_text(encoding="utf-8")
    generated_text = (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").read_text(encoding="utf-8")
    porting_candidates = json.loads((project_dir / "proof" / "porting_candidates.json").read_text(encoding="utf-8"))

    assert report["seed_family"] == "unitary_perfect"
    assert "import UnitaryPerfect.UnitaryPerfect" in basic_text
    assert "abbrev IsUnitaryPerfect" in basic_text
    assert "Even n" in generated_text
    assert "Set.Finite" in main_text
    assert any(candidate["name"] == "upn_finite_goto" for candidate in porting_candidates["candidates"])


def test_prepare_formal_seeds_prime_gap_spectrum_family(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="erdos-5",
                title="Erdős Problem #5",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["primes"],
                open_problem=True,
            )
        ],
        bank_path,
    )

    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="erdos-5", name="erdos-5-20260422")
    orchestrator.set_project_statement(
        project_dir,
        "For every C ≥ 0, does there exist an infinite sequence with lim (p_{n+1}-p_n)/log(n) = C?",
        source="manual test",
    )
    orchestrator.plan_project(project_dir)

    report = orchestrator.prepare_formal(project_dir)
    basic_text = (project_dir / "formal" / "MathProject" / "Basic.lean").read_text(encoding="utf-8")
    generated_text = (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").read_text(encoding="utf-8")
    main_text = (project_dir / "formal" / "MathProject" / "MainClaim.lean").read_text(encoding="utf-8")

    assert report["seed_family"] == "prime_gap_spectrum"
    assert "structure PrimeSequence" in basic_text
    assert "def GapSpectrumTarget" in basic_text
    assert "theorem log_denominator_pos" in basic_text
    assert "theorem erdos_5_definitions" in generated_text
    assert "theorem erdos_5_lemmas" in generated_text
    assert "GapSpectrumTarget C" in main_text


def test_prepare_formal_seeds_prime_plus_two_powers_family(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="erdos-9",
                title="Erdős Problem #9",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["primes", "additive_basis"],
                open_problem=True,
            )
        ],
        bank_path,
    )

    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="erdos-9", name="erdos-9-20260422")
    orchestrator.set_project_statement(
        project_dir,
        "Let A be the set of odd integers not representable as p + 2^k + 2^l. Does A have positive upper density?",
        source="manual test",
    )
    orchestrator.plan_project(project_dir)

    report = orchestrator.prepare_formal(project_dir)
    basic_text = (project_dir / "formal" / "MathProject" / "Basic.lean").read_text(encoding="utf-8")
    generated_text = (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").read_text(encoding="utf-8")
    main_text = (project_dir / "formal" / "MathProject" / "MainClaim.lean").read_text(encoding="utf-8")

    assert report["seed_family"] == "prime_plus_two_powers"
    assert "def RepresentableByPrimeAndTwoPowers" in basic_text
    assert "def ExceptionalOddSet" in basic_text
    assert "theorem representable_lower_bound" in basic_text
    assert "theorem erdos_9_definitions" in generated_text
    assert "theorem erdos_9_lemmas" in generated_text
    assert "def ExceptionalOddSetUnbounded" in main_text
    assert "Recommended route: first formalize infinitude or local-density lower bounds" in main_text


def test_prepare_formal_seeds_ap_free_bounds_family(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="3",
                title="Erdős Problem #3",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["additive combinatorics", "arithmetic progressions"],
                open_problem=True,
            )
        ],
        bank_path,
    )

    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="3", name="erdos-3-20260422")
    orchestrator.set_project_statement(
        project_dir,
        "This is essentially asking for good bounds on r_k(N), the size of the largest subset of {1,...,N} without a non-trivial k-term arithmetic progression.",
        source="manual test",
    )
    orchestrator.plan_project(project_dir)

    report = orchestrator.prepare_formal(project_dir)
    basic_text = (project_dir / "formal" / "MathProject" / "Basic.lean").read_text(encoding="utf-8")
    main_text = (project_dir / "formal" / "MathProject" / "MainClaim.lean").read_text(encoding="utf-8")

    assert report["seed_family"] == "ap_free_bounds"
    assert "def ThreeTermAPFree" in basic_text
    assert "singleton_threeTermAPFree" in basic_text
    assert "APFreeSingletonCheckpoint" in main_text


def test_prepare_formal_seeds_minimum_overlap_family(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="36",
                title="Erdős Problem #36",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["additive combinatorics"],
                open_problem=True,
                metadata={"comments": "minimum overlap problem", "source_catalog": "erdosproblems"},
            )
        ],
        bank_path,
    )

    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="36", name="erdos-36-20260422")
    orchestrator.set_project_statement(
        project_dir,
        "Find the optimal constant c > 0 such that for all sufficiently large N, every balanced partition of {1,...,2N} contains a difference with multiplicity at least cN.",
        source="manual test",
    )
    orchestrator.plan_project(project_dir)

    report = orchestrator.prepare_formal(project_dir)
    basic_text = (project_dir / "formal" / "MathProject" / "Basic.lean").read_text(encoding="utf-8")
    main_text = (project_dir / "formal" / "MathProject" / "MainClaim.lean").read_text(encoding="utf-8")

    assert report["seed_family"] == "minimum_overlap"
    assert "def DifferenceMultiplicity" in basic_text
    assert "singleton_partition_difference" in basic_text
    assert "MinimumOverlapBaseCase" in main_text


def test_manual_deliverable_override_can_downgrade_output(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="override-problem",
                title="Override Problem",
                source="test",
                statement="A verified theorem that would normally become a note.",
                domain="number_theory",
                open_problem=False,
                references=["https://example.com/ref1", "https://example.com/ref2"],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="override-problem", name="override-problem-20260421")
    orchestrator.set_project_statement(project_dir, "For all n, the override problem holds.", source="manual test")
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)

    (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").write_text(
        "\n".join(
            [
                "import MathProject.Basic",
                "",
                "namespace MathProject",
                "",
                "theorem override_problem_definitions : True := by",
                "  trivial",
                "",
                "theorem override_problem_lemmas : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "import MathProject.GeneratedClaims",
                "",
                "namespace MathProject",
                "",
                "theorem override_problem_main : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    orchestrator.build_lean(project_dir, timeout_sec=1)
    override = orchestrator.set_project_deliverable(
        project_dir,
        mode="research_report",
        reason="This is a simple verification and should stay in report form.",
    )
    manuscript = orchestrator.write_manuscript(project_dir)
    review = orchestrator.review_project(project_dir)
    assessment = json.loads((project_dir / "artifacts" / "deliverable_assessment.json").read_text(encoding="utf-8"))

    assert override["mode"] == "research_report"
    assert manuscript["deliverable_type"] == "research_report"
    assert manuscript["manuscript_path"].endswith("research_report.md")
    assert review["deliverable_type"] == "research_report"
    assert review["paper_workflow_recommended"] is False
    assert assessment["override"]["active"] is True
    assert assessment["override"]["reason"] == "This is a simple verification and should stay in report form."
    assert assessment["auto_deliverable_type"] == "formalization_note"
