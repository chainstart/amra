import json
from pathlib import Path

from ara_math.models import ProblemRecord
from ara_math.orchestrator import MathResearchOrchestrator
from ara_math.problem_bank import save_problem_bank


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _make_project(tmp_path: Path, *, problem_id: str = "closure") -> tuple[MathResearchOrchestrator, Path]:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id=problem_id,
                title="Closure Test",
                source="test",
                statement="A small target theorem.",
                domain="logic",
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
    project_dir = orchestrator.create_project(problem_id=problem_id, name=f"{problem_id}-project")
    return orchestrator, project_dir


def _write_main_claim(project_dir: Path, body: str) -> None:
    (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").write_text(
        "\n".join(
            [
                "import MathProject.Basic",
                "",
                "namespace MathProject",
                "",
                "theorem helper_claim : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(body, encoding="utf-8")


def _passed_build(project_dir: Path) -> dict[str, object]:
    return {
        "status": "passed",
        "returncode": 0,
        "sorry_count": 0,
        "diagnostics": [],
        "summary": "mock build passed",
        "system_guard": {"status": "ready"},
    }


def test_closure_prover_verifies_clean_target(tmp_path: Path, monkeypatch) -> None:
    orchestrator, project_dir = _make_project(tmp_path, problem_id="closure-clean")
    _write_main_claim(
        project_dir,
        "\n".join(
            [
                "import MathProject.GeneratedClaims",
                "",
                "namespace MathProject",
                "",
                "theorem closure_clean_main : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    monkeypatch.setattr(orchestrator, "build_lean", lambda project_dir, timeout_sec=None: _passed_build(project_dir))

    result = orchestrator.run_closure_prover(
        project_dir,
        target_theorem="closure_clean_main",
        backend="none",
        max_attempts=0,
    )

    assert result["status"] == "verified"
    assert result["attempts_completed"] == 0
    assert result["best_audit"]["verified"] is True
    status_path = project_dir / "proof" / "closure_prover" / "closure_status.json"
    assert json.loads(status_path.read_text(encoding="utf-8"))["status"] == "verified"


def test_closure_prover_requires_explicit_target(tmp_path: Path, monkeypatch) -> None:
    orchestrator, project_dir = _make_project(tmp_path, problem_id="closure-needs-target")
    _write_main_claim(
        project_dir,
        "\n".join(
            [
                "import MathProject.GeneratedClaims",
                "",
                "namespace MathProject",
                "",
                "theorem some_clean_main : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    monkeypatch.setattr(orchestrator, "build_lean", lambda project_dir, timeout_sec=None: _passed_build(project_dir))

    result = orchestrator.run_closure_prover(project_dir, target_theorem=None, backend="none", max_attempts=0)

    assert result["status"] == "needs_target"
    assert "explicit target theorem" in result["message"]


def test_closure_prover_rejects_sorry_even_if_build_payload_passes(tmp_path: Path, monkeypatch) -> None:
    orchestrator, project_dir = _make_project(tmp_path, problem_id="closure-incomplete")
    _write_main_claim(
        project_dir,
        "\n".join(
            [
                "import MathProject.GeneratedClaims",
                "",
                "namespace MathProject",
                "",
                "theorem closure_unfinished_main : True := by",
                "  sorry",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    monkeypatch.setattr(orchestrator, "build_lean", lambda project_dir, timeout_sec=None: _passed_build(project_dir))

    result = orchestrator.run_closure_prover(
        project_dir,
        target_theorem="closure_unfinished_main",
        backend="none",
        max_attempts=0,
    )

    assert result["status"] == "exhausted"
    assert result["best_audit"]["verified"] is False
    assert result["best_audit"]["counts"]["sorry"] == 1


def test_closure_prover_stops_after_no_progress(tmp_path: Path, monkeypatch) -> None:
    orchestrator, project_dir = _make_project(tmp_path, problem_id="closure-stalled")
    _write_main_claim(
        project_dir,
        "\n".join(
            [
                "import MathProject.GeneratedClaims",
                "",
                "namespace MathProject",
                "",
                "theorem closure_stalled_main : True := by",
                "  sorry",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    monkeypatch.setattr(orchestrator, "build_lean", lambda project_dir, timeout_sec=None: _passed_build(project_dir))
    monkeypatch.setattr(
        orchestrator.closure_prover_runner,
        "_wait_for_headroom",
        lambda: {"status": "ready", "snapshot": {}, "blockers": [], "thresholds": {}},
    )

    result = orchestrator.run_closure_prover(
        project_dir,
        target_theorem="closure_stalled_main",
        backend="none",
        max_attempts=2,
        max_stalled_attempts=1,
    )

    assert result["status"] == "blocked"
    assert result["attempts_completed"] == 1
    attempt_report = json.loads(
        (project_dir / "proof" / "closure_prover" / "attempts" / "attempt_001" / "attempt_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert attempt_report["progress_delta"] == 0
    assert attempt_report["accepted"] is False
