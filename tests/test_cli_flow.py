import json
from pathlib import Path
from subprocess import TimeoutExpired

from ara_math.cli import main
from ara_math.orchestrator import MathResearchOrchestrator
from ara_math.problem_bank import save_problem_bank
from ara_math.models import ProblemRecord


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_timeout_build_report_is_json_serializable(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="timeout-problem",
                title="Timeout Problem",
                source="test",
                statement="This is a timeout smoke test.",
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
    project_dir = orchestrator.create_project(problem_id="timeout-problem", name="timeout-problem-20260421")
    orchestrator.plan_project(project_dir)
    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")

    def _timeout(command, cwd, timeout):
        raise TimeoutExpired(command, timeout, output=b"partial stdout", stderr=b"partial stderr")

    monkeypatch.setattr(orchestrator.lean_executor, "run_command", _timeout)

    payload = orchestrator.build_lean(project_dir, timeout_sec=1)

    assert payload["status"] == "timeout"
    assert json.loads((project_dir / "artifacts" / "lean_build_report.json").read_text(encoding="utf-8"))["status"] == "timeout"


def test_set_deliverable_cli_updates_override_file(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="cli-problem",
                title="CLI Problem",
                source="test",
                statement="CLI deliverable override.",
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
    project_dir = orchestrator.create_project(problem_id="cli-problem", name="cli-problem-20260421")

    exit_code = main(
        [
            "--json",
            "set-deliverable",
            "--project",
            str(project_dir),
            "--mode",
            "formalization_note",
            "--reason",
            "Manual curation from CLI test.",
        ]
    )

    override = json.loads((project_dir / "idea" / "deliverable_override.json").read_text(encoding="utf-8"))

    assert exit_code == 0
    assert override["mode"] == "formalization_note"
    assert override["reason"] == "Manual curation from CLI test."


def test_discover_proof_route_cli_writes_paper_first_artifacts(tmp_path: Path) -> None:
    source_doc = tmp_path / "route_source.md"
    source_doc.write_text(
        "\n".join(
            [
                "# Route Source",
                "",
                "**Problem Statement**: For which values of n can an equilateral triangle be dissected into n congruent triangles?",
                "Triangle Tiling II: Nonexistence theorems.",
                "There is no 7-tiling or 11-tiling of any triangle by any tile.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="discover-route-problem",
                title="Discover Route Problem",
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
    project_dir = orchestrator.create_project(problem_id="discover-route-problem", name="discover-route-problem-20260424")

    exit_code = main(
        [
            "--json",
            "discover-proof-route",
            "--project",
            str(project_dir),
            "--bank",
            str(bank_path),
        ]
    )

    theorem_graph = json.loads((project_dir / "proof" / "theorem_graph.json").read_text(encoding="utf-8"))
    route_candidates = json.loads((project_dir / "proof" / "route_candidates.json").read_text(encoding="utf-8"))
    selected_route = (project_dir / "proof" / "selected_route.md").read_text(encoding="utf-8")

    assert exit_code == 0
    assert theorem_graph["node_count"] >= 1
    assert route_candidates["candidate_count"] >= 1
    assert "## Theorem Chain" in selected_route
