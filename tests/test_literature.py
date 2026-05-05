import json
from pathlib import Path

from ara_math.literature import LiteratureHarvester, _HTMLTextExtractor
from ara_math.cli import main
from ara_math.orchestrator import MathResearchOrchestrator
from ara_math.planning import MathPlanner
from ara_math.problem_bank import save_problem_bank
from ara_math.models import ProblemRecord


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_html_text_extractor_ignores_script_content() -> None:
    parser = _HTMLTextExtractor()
    parser.feed(
        """
        <html><head><title>Example</title><script>window.location.href = clean;</script></head>
        <body><h1>Problem Statement</h1><p>For which values of n can an equilateral triangle be dissected?</p></body>
        </html>
        """
    )

    extracted = parser.text()

    assert "window.location.href" not in extracted
    assert "equilateral triangle" in extracted


def test_normalize_evidence_line_rejects_javascript_fragments() -> None:
    harvester = LiteratureHarvester()

    assert harvester._normalize_evidence_line("window.location.href = searchUrl;") == ""
    assert harvester._normalize_evidence_line("const parts = input.split(/\\s+/).filter(Boolean);") == ""
    assert harvester._normalize_evidence_line("python3 src/unitary_perfect_search.py") == ""
    assert harvester._normalize_evidence_line("read problem_1052_research.md") == ""
    assert harvester._normalize_evidence_line("Create a formalisation here") == ""
    assert harvester._normalize_evidence_line("Impossibility of n = 7") == "Impossibility of n = 7"


def test_harvest_literature_recovers_find_statement_and_skips_foreign_problem_lines(tmp_path: Path) -> None:
    source_doc = tmp_path / "erdos36_notes.md"
    source_doc.write_text(
        "\n".join(
            [
                "OPEN",
                "Find the optimal constant c > 0 such that the following holds.",
                "For all sufficiently large N, every balanced partition contains a large overlap witness.",
                "**问题 #86** - 标签: graph theory",
                "**问题 #36** - 标签: number theory, additive combinatorics",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="36",
                title="Erdős Problem #36",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                open_problem=True,
                references=[str(source_doc)],
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

    project_dir = orchestrator.create_project(problem_id="36", name="erdos-36-20260421")

    report = orchestrator.harvest_literature(project_dir)

    assert report["recovered_statement"]["status"] == "recovered"
    assert report["recovered_statement"]["statement"].startswith("Find the optimal constant")
    assert "For all sufficiently large N" in report["recovered_statement"]["statement"]
    proof_ingredients = report["evidence"]["proof_ingredients"]
    assert not any("#86" in item["statement"] for item in proof_ingredients)


def test_extract_evidence_items_skips_cross_problem_source_lines() -> None:
    harvester = LiteratureHarvester()
    problem = ProblemRecord(
        problem_id="1052",
        title="Erdős Problem #1052",
        source="Erdős Problems",
        statement="Detailed statement should be imported from the full problem source before theorem work begins.",
        domain="number_theory",
        open_problem=True,
        metadata={"source_catalog": "erdosproblems"},
    )

    items = harvester._extract_evidence_items(
        "网站标记为未知，但文献暗示可能已被证明不可行",
        problem=problem,
        source="/tmp/problem_634_research.md",
        title="problem_634_research.md",
        candidate_statements=[],
    )

    assert items == []


def test_harvest_literature_prefers_open_target_over_definition_for_unitary_perfect(tmp_path: Path) -> None:
    definition_doc = tmp_path / "problem_1052_research.md"
    definition_doc.write_text(
        "\n".join(
            [
                "# Problem 1052",
                "",
                "1. **Definition**: d is a unitary divisor of n iff d | n and gcd(d, n/d) = 1.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    theorem_doc = tmp_path / "README.md"
    theorem_doc.write_text(
        "\n".join(
            [
                "# Unitary Perfect Numbers",
                "",
                "1. **Finiteness**: There are finitely many unitary perfect numbers (via Goto's bound).",
                "2. **Parity**: No odd unitary perfect numbers exist.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="1052",
                title="Erdős Problem #1052",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["number theory"],
                open_problem=True,
                references=[str(definition_doc), str(theorem_doc)],
                metadata={"source_catalog": "erdosproblems", "comments": "unitary perfect numbers"},
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )

    project_dir = orchestrator.create_project(problem_id="1052", name="erdos-1052-20260425")
    report = orchestrator.harvest_literature(project_dir)

    assert report["recovered_statement"]["status"] == "recovered"
    assert "finitely many unitary perfect numbers" in report["recovered_statement"]["statement"].lower()
    assert "unitary divisor" not in report["recovered_statement"]["statement"].lower()


def test_harvest_literature_keeps_non_placeholder_bank_statement(tmp_path: Path) -> None:
    source_doc = tmp_path / "README.md"
    source_doc.write_text(
        "\n".join(
            [
                "# Local Notes",
                "",
                "1. **Finiteness**: There are finitely many unitary perfect numbers (via Goto's bound).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="odd-unitary-perfect-exclusion",
                title="No Odd Unitary Perfect Numbers",
                source="test",
                statement="Prove that no odd unitary perfect numbers exist.",
                domain="number_theory",
                tags=["unitary_perfect"],
                open_problem=False,
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

    project_dir = orchestrator.create_project(
        problem_id="odd-unitary-perfect-exclusion",
        name="odd-unitary-perfect-exclusion-20260425",
    )
    report = orchestrator.harvest_literature(project_dir)
    exact_statement = (project_dir / "idea" / "exact_statement.md").read_text(encoding="utf-8").strip()

    assert exact_statement == "Prove that no odd unitary perfect numbers exist."
    assert report["recovered_statement"]["status"] == "candidate_found_existing_statement_kept"
    assert "finitely many unitary perfect numbers" in report["recovered_statement"]["statement"].lower()


def test_harvest_literature_recovers_statement_from_local_markdown(tmp_path: Path) -> None:
    source_doc = tmp_path / "triangle_notes.md"
    source_doc.write_text(
        "\n".join(
            [
                "# Local Notes",
                "",
                "**Problem Statement**: For which values of n can an equilateral triangle be dissected into n congruent triangles?",
                "",
                "Further notes go here.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="triangle-local",
                title="Triangle Local Problem",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                tags=["geometry", "finite_case"],
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

    project_dir = orchestrator.create_project(problem_id="triangle-local", name="triangle-local-20260421")
    report = orchestrator.harvest_literature(project_dir)

    exact_statement = (project_dir / "idea" / "exact_statement.md").read_text(encoding="utf-8")
    recovery = json.loads((project_dir / "idea" / "statement_recovery.json").read_text(encoding="utf-8"))

    assert report["snapshot_count"] == 1
    assert report["recovered_statement"]["status"] == "recovered"
    assert "equilateral triangle be dissected" in exact_statement
    assert "ARA_MATH_PLACEHOLDER_EXACT_STATEMENT" not in exact_statement
    assert recovery["status"] == "recovered"


def test_plan_project_runs_local_literature_harvest(tmp_path: Path) -> None:
    source_doc = tmp_path / "weird_notes.md"
    source_doc.write_text(
        "\n".join(
            [
                "# Weird Numbers",
                "",
                "**Conjecture**: Every weird number has abundance index C = 3.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="weird-local",
                title="Weird Local Problem",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["weird_numbers", "computational_search"],
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

    project_dir = orchestrator.create_project(problem_id="weird-local", name="weird-local-20260421")
    plan = orchestrator.plan_project(project_dir)

    snapshots = json.loads((project_dir / "idea" / "reference_snapshots.json").read_text(encoding="utf-8"))
    proof_path_assessment = json.loads(
        (project_dir / "idea" / "proof_path_assessment.json").read_text(encoding="utf-8")
    )
    assert snapshots["snapshot_count"] == 1
    assert any(task["task_type"] == "historical_foundation_audit" for task in plan["tasks"])
    assert proof_path_assessment["literature"]["snapshot_count"] == 1
    assert proof_path_assessment["literature"]["recovered_statement_status"] == "recovered"
    assert proof_path_assessment["local_literature_signal"]["statement_recoverable"] is True
    assert proof_path_assessment["literature"]["open_gaps"]
    assert not any("placeholder statement" in blocker for blocker in proof_path_assessment["blockers"])
    assert any(
        "Harvested literature already provides a working target statement" in item
        for item in proof_path_assessment["opportunities"]
    )
    assert any("Recovered target statement:" in note for note in plan["notes"])


def test_harvest_literature_cli_works_with_local_sources(tmp_path: Path) -> None:
    source_doc = tmp_path / "amicable_notes.md"
    source_doc.write_text(
        "\n".join(
            [
                "# Amicable Notes",
                "",
                "**Problem Statement**: Determine whether there exists an amicable pair in which both numbers are odd.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="amicable-local",
                title="Amicable Local Problem",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["amicable_numbers", "parity"],
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
    project_dir = orchestrator.create_project(problem_id="amicable-local", name="amicable-local-20260421")

    exit_code = main(
        [
            "--json",
            "harvest-literature",
            "--project",
            str(project_dir),
            "--bank",
            str(bank_path),
        ]
    )

    report = json.loads((project_dir / "idea" / "reference_snapshots.json").read_text(encoding="utf-8"))

    assert exit_code == 0
    assert report["snapshot_count"] == 1


def test_harvest_literature_reads_directory_assets_via_readme(tmp_path: Path) -> None:
    source_dir = tmp_path / "local_project"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "README.md").write_text(
        "\n".join(
            [
                "# Local Project",
                "",
                "**Problem Statement**: Prove that no odd unitary perfect numbers exist.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="unitary-dir-local",
                title="Unitary Directory Problem",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["divisors"],
                open_problem=True,
                references=[str(source_dir)],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )

    project_dir = orchestrator.create_project(problem_id="unitary-dir-local", name="unitary-dir-local-20260421")
    report = orchestrator.harvest_literature(project_dir)

    assert report["snapshot_count"] == 1
    assert report["recovered_statement"]["status"] == "recovered"


def test_extract_theorem_snippets_from_text_like_paper_content() -> None:
    harvester = LiteratureHarvester()

    snippets = harvester._extract_theorem_snippets(
        "\n".join(
            [
                "Theorem 1.2. If N is a UPN with k distinct prime factors, then it follows that N ≤ 2^(2^k).",
                "",
                "Lemma 3.4. Let m1, ..., mr be positive integers. If ...",
                "Then every admissible tuple satisfies the displayed inequality.",
                "",
            ]
        )
    )

    assert len(snippets) >= 2
    assert snippets[0]["kind"] == "theorem"
    assert "UPN" in snippets[0]["statement"]
    assert snippets[1]["kind"] == "lemma"
    assert "displayed inequality" in snippets[1]["statement"]


def test_planner_builds_inventory_from_paper_theorem_snippets() -> None:
    planner = MathPlanner()
    problem = ProblemRecord(
        problem_id="erdos-1052",
        title="Finite Number of Unitary Perfect Numbers",
        source="Erdős Problems",
        statement="Determine whether there are only finitely many unitary perfect numbers.",
        domain="number_theory",
        tags=["divisors", "unitary_perfect"],
        open_problem=True,
    )

    theorem_inventory = planner.build_theorem_inventory(
        problem=problem,
        proof_path_assessment={},
        paper_inventory={
            "records": [
                {
                    "title": "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers",
                    "local_path": "/tmp/goto2007.pdf",
                    "status": "existing_local_copy",
                    "theorem_snippets": [
                        {
                            "kind": "theorem",
                            "label": "1.2",
                            "statement": "If N is a UPN with k distinct prime factors, then N is bounded above by an explicit function of k.",
                        }
                    ],
                }
            ]
        },
    )

    assert theorem_inventory["entry_count"] >= 1
    assert any("UPN with k distinct prime factors" in entry["statement"] for entry in theorem_inventory["entries"])
    assert any(entry["bucket"] == "paper_theorem" for entry in theorem_inventory["entries"])


def test_unitary_perfect_candidate_scoring_penalizes_cayley_graph_noise() -> None:
    harvester = LiteratureHarvester()
    problem = ProblemRecord(
        problem_id="erdos-1052",
        title="Finite Number of Unitary Perfect Numbers",
        source="Erdős Problems",
        statement="Determine whether there are only finitely many unitary perfect numbers.",
        domain="number_theory",
        tags=["divisors", "unitary_perfect"],
        open_problem=True,
    )
    evidence = {"known_results": [], "proof_ingredients": [], "modern_tools": []}
    family = harvester._infer_problem_family(problem, recovered_statement=problem.statement, evidence=evidence)
    keywords = harvester._query_tokens("unitary perfect number odd unitary perfect numbers")

    relevant = {
        "title": "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers",
        "venue": "Rocky Mountain Journal of Mathematics",
        "summary": "Unitary perfect numbers and unitary harmonic numbers are bounded.",
        "authors": ["Takeshi Goto"],
    }
    noise = {
        "title": "A complete classification of perfect unitary Cayley graphs",
        "venue": "arXiv",
        "summary": "Perfect unitary Cayley graphs over finite rings.",
        "authors": ["Someone Else"],
    }

    assert harvester._candidate_overlap_score(relevant, keywords=keywords, family=family) > harvester._candidate_overlap_score(
        noise,
        keywords=keywords,
        family=family,
    )


def test_planner_prefers_specific_paper_theorem_over_generic_route_notes() -> None:
    planner = MathPlanner()
    problem = ProblemRecord(
        problem_id="634",
        title="Triangle Dissection Problem",
        source="Erdős Problems",
        statement="For which values of n can an equilateral triangle be dissected into n congruent triangles?",
        domain="geometry",
        tags=["geometry", "triangle_dissection"],
        open_problem=True,
    )

    theorem_inventory = planner.build_theorem_inventory(
        problem=problem,
        proof_path_assessment={
            "literature": {
                "known_results": [
                    {"statement": "Show no valid configuration exists", "source": "STRATEGY.md", "title": "STRATEGY.md"},
                ],
                "proof_ingredients": [],
                "modern_tools": [],
            }
        },
        paper_inventory={
            "records": [
                {
                    "title": "Triangle Tiling Slides",
                    "local_path": "/tmp/slides.pdf",
                    "status": "existing_local_copy",
                    "theorem_snippets": [
                        {
                            "kind": "theorem",
                            "label": "",
                            "statement": "There is no 7-tiling or 11-tiling of any triangle by any tile.",
                        }
                    ],
                }
            ]
        },
    )

    assert theorem_inventory["entries"][0]["bucket"] == "paper_theorem"
    assert "7-tiling" in theorem_inventory["entries"][0]["statement"]


def test_planner_filters_unitary_group_noise_from_unitary_perfect_routes() -> None:
    planner = MathPlanner()
    problem = ProblemRecord(
        problem_id="erdos-1052",
        title="Finite Number of Unitary Perfect Numbers",
        source="Erdős Problems",
        statement="Determine whether there are only finitely many unitary perfect numbers.",
        domain="number_theory",
        tags=["divisors", "unitary_perfect"],
        open_problem=True,
    )

    theorem_inventory = planner.build_theorem_inventory(
        problem=problem,
        proof_path_assessment={},
        paper_inventory={
            "records": [
                {
                    "title": "Conjugacy classes of centralizers in unitary groups",
                    "local_path": "/tmp/unitary-groups.pdf",
                    "status": "existing_local_copy",
                    "theorem_snippets": [
                        {
                            "kind": "proposition",
                            "label": "2.1",
                            "statement": "Let F be a field with a non-trivial Galois automorphism of order 2. Then there are only finitely many non-equivalent hermitian forms on V.",
                        }
                    ],
                },
                {
                    "title": "An analog of perfect numbers involving the unitary totient function",
                    "local_path": "/tmp/unitary-totient.pdf",
                    "status": "existing_local_copy",
                    "theorem_snippets": [
                        {
                            "kind": "theorem",
                            "label": "1.3",
                            "statement": "There exist only finitely many integers N divisible by ϕ∗(N) which are products of consecutive primes.",
                        }
                    ],
                },
            ]
        },
    )

    statements = [entry["statement"] for entry in theorem_inventory["entries"]]
    assert any("ϕ∗" in statement for statement in statements)
    assert not any("hermitian forms" in statement for statement in statements)


def test_harvest_literature_recovers_numbered_bold_statement(tmp_path: Path) -> None:
    source_doc = tmp_path / "unitary_notes.md"
    source_doc.write_text(
        "\n".join(
            [
                "# Unitary Perfect Numbers",
                "",
                "1. **Finiteness**: There are finitely many unitary perfect numbers (via Goto's bound).",
                "2. **Parity**: No odd unitary perfect numbers exist.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="unitary-local",
                title="Unitary Local Problem",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["divisors"],
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
    project_dir = orchestrator.create_project(problem_id="unitary-local", name="unitary-local-20260421")

    report = orchestrator.harvest_literature(project_dir)

    assert report["recovered_statement"]["status"] == "recovered"
    assert "finitely many unitary perfect numbers" in report["recovered_statement"]["statement"].lower()


def test_harvest_literature_builds_structured_evidence(tmp_path: Path) -> None:
    source_doc = tmp_path / "evidence_notes.md"
    source_doc.write_text(
        "\n".join(
            [
                "# Evidence Notes",
                "",
                "Theorem: No odd unitary perfect numbers exist.",
                "This proof uses an explicit bound and a Lean formalization.",
                "Open question: Does every weird number have abundance index C = 3?",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="evidence-local",
                title="Evidence Local Problem",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["divisors", "weird_numbers"],
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
    project_dir = orchestrator.create_project(problem_id="evidence-local", name="evidence-local-20260421")

    orchestrator.harvest_literature(project_dir)
    evidence = json.loads((project_dir / "idea" / "literature_evidence.json").read_text(encoding="utf-8"))

    assert evidence["counts"]["known_results"] >= 1
    assert evidence["counts"]["proof_ingredients"] >= 1
    assert evidence["counts"]["modern_tools"] >= 1
    assert evidence["counts"]["open_gaps"] >= 1
    assert evidence["source_attribution_count"] == 1


def test_harvest_literature_preserves_existing_paper_inventory_without_network(tmp_path: Path) -> None:
    source_doc = tmp_path / "triangle_notes.md"
    source_doc.write_text(
        "\n".join(
            [
                "# Triangle Notes",
                "",
                "**Problem Statement**: For which values of n can an equilateral triangle be dissected into n congruent triangles?",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="triangle-local",
                title="Triangle Local Problem",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                tags=["geometry", "triangle_dissection"],
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
    project_dir = orchestrator.create_project(problem_id="triangle-local", name="triangle-local-20260422")
    inventory = {
        "generated_at": "2026-04-22T00:00:00+00:00",
        "problem_id": "triangle-local",
        "query_count": 1,
        "candidate_count": 1,
        "downloaded_pdf_count": 1,
        "manual_followup_count": 0,
        "records": [
            {
                "title": "Triangle Tiling II: Nonexistence theorems",
                "status": "existing_local_copy",
                "local_path": "/tmp/beeson.pdf",
                "source_url": "https://example.com/beeson",
            }
        ],
    }
    (project_dir / "idea" / "paper_inventory.json").write_text(json.dumps(inventory), encoding="utf-8")

    report = orchestrator.harvest_literature(project_dir, allow_network=False)
    persisted = json.loads((project_dir / "idea" / "paper_inventory.json").read_text(encoding="utf-8"))

    assert report["paper_inventory"]["downloaded_pdf_count"] == 1
    assert len(persisted["records"]) == 1
    assert persisted["records"][0]["title"] == "Triangle Tiling II: Nonexistence theorems"


def test_plan_project_bootstraps_erdos_docs_and_local_assets(tmp_path: Path) -> None:
    formal_math_root = tmp_path / "formal-math"
    docs_dir = formal_math_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "simple_problems_analysis.md").write_text(
        "\n".join(
            [
                "# Erdős Focus Notes",
                "",
                "### 问题 #633",
                "**问题陈述**: 找出所有只能被分割成平方数个全等三角形的三角形。",
                "",
                "This track reuses the same finite-certificate geometry machinery as problem #634.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    triangle_root = formal_math_root / "erdos-634-triangle"
    triangle_root.mkdir(parents=True, exist_ok=True)
    (triangle_root / "README.md").write_text(
        "\n".join(
            [
                "# Triangle Family",
                "",
                "### Problem #634",
                "**Problem Statement**: For which values of n can an equilateral triangle be dissected into n congruent triangles?",
                "",
                "Problem #633 and Problem #634 share triangle-dissection infrastructure.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="633",
                title="Erdős Problem #633",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                tags=["geometry"],
                open_problem=True,
                formalized="no",
                references=["https://www.erdosproblems.com/633"],
                metadata={"source_catalog": "erdosproblems", "prize": "$25", "statement_quality": "placeholder"},
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
        formal_math_root=formal_math_root,
    )

    project_dir = orchestrator.create_project(problem_id="633", name="633-campaign-20260421")
    initial_assessment = json.loads((project_dir / "idea" / "proof_path_assessment.json").read_text(encoding="utf-8"))
    plan = orchestrator.plan_project(project_dir)
    recovery = json.loads((project_dir / "idea" / "statement_recovery.json").read_text(encoding="utf-8"))
    snapshots = json.loads((project_dir / "idea" / "reference_snapshots.json").read_text(encoding="utf-8"))

    assert initial_assessment["local_assets"]
    assert any(asset["kind"].startswith("companion_") for asset in initial_assessment["local_assets"])
    assert recovery["status"] == "recovered"
    assert "平方数个全等三角形" in recovery["statement"]
    assert "equilateral triangle" not in recovery["statement"].lower()
    assert snapshots["snapshot_count"] >= 2
    assert any(task["task_type"] == "historical_foundation_audit" for task in plan["tasks"])
    assert any(claim["claim_id"] == "633:main" and "平方数个全等三角形" in claim["statement"] for claim in plan["claims"])
    assert not any("placeholder statement" in note for note in plan["notes"])


def test_harvest_literature_updates_prior_auto_recovery_when_better_candidate_appears(tmp_path: Path) -> None:
    formal_math_root = tmp_path / "formal-math"
    docs_dir = formal_math_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "simple_problems_analysis.md").write_text(
        "\n".join(
            [
                "# Erdős Focus Notes",
                "",
                "### 问题 #633",
                "**问题陈述**: 找出所有只能被分割成平方数个全等三角形的三角形。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    triangle_root = formal_math_root / "erdos-634-triangle"
    triangle_root.mkdir(parents=True, exist_ok=True)
    (triangle_root / "README.md").write_text(
        "\n".join(
            [
                "# Triangle Family",
                "",
                "### Problem #634",
                "**Problem Statement**: For which values of n can an equilateral triangle be dissected into n congruent triangles?",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="633",
                title="Erdős Problem #633",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                tags=["geometry"],
                open_problem=True,
                formalized="no",
                references=["https://www.erdosproblems.com/633"],
                metadata={"source_catalog": "erdosproblems", "prize": "$25", "statement_quality": "placeholder"},
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
        formal_math_root=formal_math_root,
    )
    project_dir = orchestrator.create_project(problem_id="633", name="633-campaign-20260421")
    orchestrator.set_project_statement(
        project_dir,
        "For which values of n can an equilateral triangle be dissected into n congruent triangles?",
        source=f"literature recovery from {triangle_root / 'README.md'}",
    )


def test_harvest_literature_scans_project_papers_directory(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="papers-local",
                title="Papers Local Problem",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                open_problem=True,
                references=[],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="papers-local", name="papers-local-20260421")
    papers_dir = project_dir / "idea" / "papers"
    papers_dir.mkdir(parents=True, exist_ok=True)
    (papers_dir / "partial-result.md").write_text(
        "\n".join(
            [
                "# Partial Result",
                "",
                "**Problem Statement**: Determine whether every sufficiently large admissible integer belongs to the target spectrum.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = orchestrator.harvest_literature(project_dir)

    assert report["snapshot_count"] == 1
    assert report["recovered_statement"]["status"] == "recovered"
    assert "sufficiently large admissible integer" in report["recovered_statement"]["statement"]


def test_harvest_literature_reads_project_pdf_via_pdftotext_hook(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="pdf-local",
                title="PDF Local Problem",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                open_problem=True,
                references=[],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="pdf-local", name="pdf-local-20260421")
    pdf_path = project_dir / "idea" / "papers" / "paper.pdf"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.write_bytes(b"%PDF-1.4 fake")

    statement_text = "\n".join(
        [
            "Triangle Tiling Notes",
            "",
            "Problem Statement: For which values of n can an equilateral triangle be dissected into n congruent triangles?",
        ]
    )

    monkeypatch.setattr(
        LiteratureHarvester,
        "_extract_pdf_text",
        lambda self, path: statement_text if path == pdf_path else "",
    )

    report = orchestrator.harvest_literature(project_dir)

    assert report["snapshot_count"] == 1
    assert report["recovered_statement"]["status"] == "recovered"
    assert "equilateral triangle" in report["recovered_statement"]["statement"].lower()


def test_harvest_literature_keeps_only_current_problem_section_from_multi_problem_notes(tmp_path: Path) -> None:
    source_doc = tmp_path / "simple_problems_analysis.md"
    source_doc.write_text(
        "\n".join(
            [
                "# Simple Erdős Problems",
                "",
                "### 问题 #5",
                "**问题陈述**: 对任意 C≥0，是否存在无穷序列使得 lim (p_{n+1}-p_n)/log(n) = C？",
                "研究方向：利用筛法和素数间隙工具。",
                "",
                "### 问题 #9",
                "**问题陈述**: 设 A 为所有不能表示为 p + 2^k + 2^l 形式的奇数集合（p是素数，k,l≥0），A的上密度是否为正？",
                "研究方向：通过加法组合和有限证书分析。",
                "",
                "python3 src/unitary_perfect_search.py",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="5",
                title="Erdős Problem #5",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                open_problem=True,
                references=[str(source_doc)],
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
    project_dir = orchestrator.create_project(problem_id="5", name="erdos-5-20260422")

    report = orchestrator.harvest_literature(project_dir)
    evidence = report["evidence"]

    assert "p_{n+1}" in report["recovered_statement"]["statement"]
    assert not any("不能表示为 p + 2^k + 2^l" in item["statement"] for item in evidence["proof_ingredients"])
    assert not any("unitary_perfect_search.py" in item["statement"] for item in evidence["proof_ingredients"])


def test_harvest_literature_downloads_linked_project_papers(tmp_path: Path, monkeypatch) -> None:
    page_url = "https://example.test/problem/634"
    pdf_url = "https://example.test/papers/triangle-nonexistence.pdf"
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="634",
                title="Erdős Problem #634",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                open_problem=True,
                references=[page_url],
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
    project_dir = orchestrator.create_project(problem_id="634", name="634-local-20260422")

    def fake_fetch_remote_payload(self: LiteratureHarvester, url: str) -> dict[str, object]:
        assert url == page_url
        return {
            "title": "Problem #634",
            "text": "Problem Statement: For which values of n can an equilateral triangle be dissected into n congruent triangles?",
            "content_kind": "html",
            "links": [{"href": pdf_url, "text": "Triangle Tiling II"}],
            "raw_bytes": b"",
        }

    monkeypatch.setattr(LiteratureHarvester, "_fetch_remote_payload", fake_fetch_remote_payload)
    monkeypatch.setattr(LiteratureHarvester, "_search_openalex", lambda self, query, max_results=5: [])
    monkeypatch.setattr(LiteratureHarvester, "_search_arxiv", lambda self, query, max_results=4: [])
    monkeypatch.setattr(
        LiteratureHarvester,
        "_download_binary",
        lambda self, url: (b"%PDF-1.4 linked paper", "application/pdf"),
    )
    monkeypatch.setattr(
        LiteratureHarvester,
        "_extract_pdf_text",
        lambda self, path: "Triangle Tiling II\nProblem Statement: For which values of n can an equilateral triangle be dissected into n congruent triangles?",
    )

    report = orchestrator.harvest_literature(project_dir, allow_network=True)
    inventory = json.loads((project_dir / "idea" / "paper_inventory.json").read_text(encoding="utf-8"))

    assert report["paper_inventory"]["downloaded_pdf_count"] == 1
    assert inventory["downloaded_pdf_count"] == 1
    assert any(record["status"] == "downloaded_pdf" for record in inventory["records"])
    assert any(record["provider"] == "linked_reference" for record in inventory["records"])
    assert any(Path(record["local_path"]).exists() for record in inventory["records"] if record["local_path"])


def test_harvest_literature_searches_and_downloads_related_open_access_papers(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="weird-search",
                title="Odd Weird Numbers",
                source="test",
                statement="Determine whether every sufficiently large weird number has abundance index C = 3.",
                domain="number_theory",
                tags=["weird_numbers", "abundance_index"],
                open_problem=True,
                references=[],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="weird-search", name="weird-search-20260422")

    monkeypatch.setattr(
        LiteratureHarvester,
        "_search_openalex",
        lambda self, query, max_results=5: [
            {
                "provider": "openalex",
                "query": query,
                "title": "Weird numbers and abundance index bounds",
                "authors": ["A. Author"],
                "year": 2024,
                "venue": "Open Journal",
                "doi": "10.1000/test-doi",
                "source_url": "https://example.test/landing",
                "landing_page_url": "https://example.test/landing",
                "pdf_url": "https://example.test/weird.pdf",
                "metadata_only": False,
            }
        ],
    )
    monkeypatch.setattr(LiteratureHarvester, "_search_arxiv", lambda self, query, max_results=4: [])
    monkeypatch.setattr(
        LiteratureHarvester,
        "_download_binary",
        lambda self, url: (b"%PDF-1.4 weird paper", "application/pdf"),
    )
    monkeypatch.setattr(
        LiteratureHarvester,
        "_extract_pdf_text",
        lambda self, path: "Weird numbers and abundance index bounds\nProblem Statement: Determine whether every sufficiently large weird number has abundance index C = 3.",
    )

    report = orchestrator.harvest_literature(project_dir, allow_network=True)
    inventory = json.loads((project_dir / "idea" / "paper_inventory.json").read_text(encoding="utf-8"))

    assert report["paper_inventory"]["candidate_count"] >= 1
    assert report["paper_inventory"]["downloaded_pdf_count"] == 1
    assert inventory["query_count"] >= 1
    assert inventory["downloaded_pdf_count"] == 1
    assert any(record["provider"] == "openalex" for record in inventory["records"])
    assert report["snapshot_count"] >= 1
