import json
from pathlib import Path

import pytest

from ara_math.orchestrator import MathResearchOrchestrator
from ara_math.problem_bank import save_problem_bank
from ara_math.models import ProblemRecord
from ara_math.workspace import write_json


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_plan_convergence_identifies_unitary_perfect_external_requirements(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="erdos-1052",
                title="Finite Number of Unitary Perfect Numbers",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["number theory"],
                open_problem=True,
                references=["https://example.com/ref1"],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="erdos-1052", name="erdos-1052-20260422")
    orchestrator.set_project_statement(
        project_dir,
        "There are finitely many unitary perfect numbers (via Goto's bound).",
        source="manual",
    )
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)
    write_json(
        project_dir / "artifacts" / "lean_build_report.json",
        {
            "status": "blocked",
            "diagnostics": [
                "Lean dependency cache is not build-ready.",
                "Refusing a cold-cache build in guarded mode to avoid large local compiles.",
            ],
            "sorry_count": 0,
        },
    )
    write_json(
        project_dir / "artifacts" / "review_report.json",
        {
            "status": "blocked",
            "blockers": ["Lean build status is `blocked` instead of `passed`."],
            "warnings": [],
        },
    )

    plan = orchestrator.plan_convergence(project_dir)
    requirements = json.loads((project_dir / "artifacts" / "external_requirements.json").read_text(encoding="utf-8"))

    assert plan["phase"] == "unblock_verifier"
    assert plan["ready_for_long_run"] is False
    titles = {item["title"] for item in requirements["requirements"]}
    assert any("Goto" in title for title in titles)
    assert any("Wall" in title for title in titles)
    assert any(item["kind"] == "lean_cache" for item in requirements["requirements"])


def test_write_manuscript_includes_convergence_sections(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="write-problem",
                title="Write Problem",
                source="test",
                statement="A small open target.",
                domain="number_theory",
                open_problem=True,
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
    project_dir = orchestrator.create_project(problem_id="write-problem", name="write-problem-20260422")
    orchestrator.set_project_statement(project_dir, "A small open target.", source="manual")
    orchestrator.plan_project(project_dir)
    write_json(project_dir / "artifacts" / "lean_build_report.json", {"status": "passed", "sorry_count": 0})
    write_json(project_dir / "artifacts" / "review_report.json", {"status": "checkpoint_verified", "blockers": [], "warnings": []})
    write_json(
        project_dir / "artifacts" / "convergence_plan.json",
        {
            "phase": "checkpoint_extension",
            "ready_for_long_run": True,
            "current_milestone": "A verified checkpoint exists.",
            "next_formal_objectives": ["Import one literature-backed lemma."],
        },
    )
    write_json(
        project_dir / "artifacts" / "external_requirements.json",
        {
            "requirements": [
                {
                    "kind": "paper",
                    "title": "Example external paper",
                    "status": "manual_acquisition_required",
                    "reason": "Needed for the next theorem import.",
                }
            ]
        },
    )

    report = orchestrator.write_manuscript(project_dir)
    manuscript = Path(report["manuscript_path"]).read_text(encoding="utf-8")

    assert "## Convergence Plan" in manuscript
    assert "## External Requirements" in manuscript
    assert "Example external paper" in manuscript


def test_run_convergence_campaign_prioritizes_ready_checkpoint_projects(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="checkpoint-problem",
                title="Checkpoint Problem",
                source="test",
                statement="Checkpoint target.",
                domain="number_theory",
                open_problem=True,
                references=["https://example.com/ref1", "https://example.com/ref2"],
            ),
            ProblemRecord(
                problem_id="blocked-problem",
                title="Blocked Problem",
                source="test",
                statement="Blocked target.",
                domain="geometry",
                open_problem=True,
                references=["https://example.com/ref1", "https://example.com/ref2"],
            ),
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    checkpoint_project = orchestrator.create_project(problem_id="checkpoint-problem", name="checkpoint-problem-20260422")
    blocked_project = orchestrator.create_project(problem_id="blocked-problem", name="blocked-problem-20260422")

    review_statuses = {
        str(checkpoint_project): "checkpoint_verified",
        str(blocked_project): "blocked",
    }
    convergence_plans = {
        str(checkpoint_project): {
            "phase": "checkpoint_extension",
            "ready_for_long_run": True,
            "recommended_run_profile": {
                "backend": "codex",
                "attempts": 2,
                "time_budget_sec": 100,
                "attempt_timeout_sec": 40,
                "build_timeout_sec": 20,
                "reasoning_effort": "high",
                "allow_network": True,
            },
            "external_requirement_count": 0,
        },
        str(blocked_project): {
            "phase": "statement_recovery_required",
            "ready_for_long_run": False,
            "recommended_run_profile": {
                "backend": "codex",
                "attempts": 1,
                "time_budget_sec": 60,
                "attempt_timeout_sec": 20,
                "build_timeout_sec": 20,
                "reasoning_effort": "medium",
                "allow_network": False,
            },
            "external_requirement_count": 1,
        },
    }
    calls: list[dict[str, object]] = []

    def fake_review(project_dir: Path) -> dict[str, object]:
        status = review_statuses[str(project_dir)]
        report = {
            "status": status,
            "deliverable_type": "research_report",
            "blockers": [] if status == "checkpoint_verified" else ["needs statement"],
            "warnings": [],
        }
        write_json(project_dir / "artifacts" / "review_report.json", report)
        write_json(project_dir / "artifacts" / "convergence_plan.json", convergence_plans[str(project_dir)])
        return report

    def fake_plan_convergence(project_dir: Path) -> dict[str, object]:
        write_json(project_dir / "artifacts" / "convergence_plan.json", convergence_plans[str(project_dir)])
        return convergence_plans[str(project_dir)]

    def fake_run_proof_search(
        project_dir: Path,
        *,
        backend: str,
        max_attempts: int,
        max_runtime_sec: int,
        attempt_timeout_sec: int,
        build_timeout_sec: int,
    ) -> dict[str, object]:
        calls.append(
            {
                "project_dir": str(project_dir),
                "backend": backend,
                "max_attempts": max_attempts,
                "max_runtime_sec": max_runtime_sec,
                "attempt_timeout_sec": attempt_timeout_sec,
                "build_timeout_sec": build_timeout_sec,
            }
        )
        return {"status": "checkpoint", "attempts_completed": max_attempts}

    monkeypatch.setattr(orchestrator, "review_project", fake_review)
    monkeypatch.setattr(orchestrator, "plan_convergence", fake_plan_convergence)
    monkeypatch.setattr(orchestrator, "run_proof_search", fake_run_proof_search)

    payload = orchestrator.run_convergence_campaign(
        limit=1,
        runtime_multiplier=2.0,
        attempt_multiplier=1.5,
    )

    assert payload["candidate_count"] == 1
    assert payload["selected_count"] == 1
    assert len(calls) == 1
    assert calls[0]["project_dir"] == str(checkpoint_project)
    assert calls[0]["backend"] == "codex"
    assert calls[0]["max_attempts"] == 3
    assert calls[0]["max_runtime_sec"] == 200
    assert calls[0]["attempt_timeout_sec"] == 80
    assert calls[0]["build_timeout_sec"] == 40
    assert payload["entries"][0]["rounds_requested"] == 1
    assert payload["entries"][0]["rounds_completed"] == 1


def test_run_convergence_campaign_can_continue_across_checkpoint_rounds(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="checkpoint-loop-problem",
                title="Checkpoint Loop Problem",
                source="test",
                statement="Checkpoint target.",
                domain="number_theory",
                open_problem=True,
                references=["https://example.com/ref1"],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="checkpoint-loop-problem", name="checkpoint-loop-problem-20260422")

    review_state = {"status": "checkpoint_verified"}
    convergence_state = {
        "phase": "checkpoint_extension",
        "ready_for_long_run": True,
        "recommended_run_profile": {
            "backend": "codex",
            "attempts": 1,
            "time_budget_sec": 120,
            "attempt_timeout_sec": 40,
            "build_timeout_sec": 20,
            "reasoning_effort": "high",
            "allow_network": True,
        },
        "external_requirement_count": 0,
    }
    run_results = [
        {"status": "checkpoint", "attempts_completed": 1, "elapsed_seconds": 12.0},
        {"status": "converged", "attempts_completed": 2, "elapsed_seconds": 18.0},
    ]
    calls: list[dict[str, object]] = []

    def fake_review(project_path: Path) -> dict[str, object]:
        report = {
            "status": review_state["status"],
            "deliverable_type": "research_report",
            "blockers": [],
            "warnings": [],
        }
        write_json(project_path / "artifacts" / "review_report.json", report)
        write_json(project_path / "artifacts" / "convergence_plan.json", convergence_state)
        return report

    def fake_plan_convergence(project_path: Path) -> dict[str, object]:
        write_json(project_path / "artifacts" / "convergence_plan.json", convergence_state)
        return convergence_state

    def fake_run_proof_search(
        project_path: Path,
        *,
        backend: str,
        max_attempts: int,
        max_runtime_sec: int,
        attempt_timeout_sec: int,
        build_timeout_sec: int,
    ) -> dict[str, object]:
        index = len(calls)
        calls.append(
            {
                "project_dir": str(project_path),
                "backend": backend,
                "max_attempts": max_attempts,
                "max_runtime_sec": max_runtime_sec,
                "attempt_timeout_sec": attempt_timeout_sec,
                "build_timeout_sec": build_timeout_sec,
            }
        )
        result = run_results[index]
        if result["status"] == "converged":
            review_state["status"] = "ready_for_human_review"
        return result

    monkeypatch.setattr(orchestrator, "review_project", fake_review)
    monkeypatch.setattr(orchestrator, "plan_convergence", fake_plan_convergence)
    monkeypatch.setattr(orchestrator, "run_proof_search", fake_run_proof_search)

    payload = orchestrator.run_convergence_campaign(
        limit=1,
        rounds=3,
        continue_on_checkpoint=True,
        runtime_multiplier=1.0,
        attempt_multiplier=1.0,
    )

    assert len(calls) == 2
    assert payload["entries"][0]["rounds_requested"] == 3
    assert payload["entries"][0]["rounds_completed"] == 2
    assert payload["entries"][0]["result"]["status"] == "converged"
    assert payload["entries"][0]["round_entries"][0]["status"] == "checkpoint"
    assert payload["entries"][0]["round_entries"][1]["status"] == "converged"


def test_plan_convergence_marks_local_pdf_requirements_as_available(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="erdos-1052",
                title="Finite Number of Unitary Perfect Numbers",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["number theory"],
                open_problem=True,
                references=["https://example.com/ref1"],
            )
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    project_dir = orchestrator.create_project(problem_id="erdos-1052", name="erdos-1052-local-pdf")
    orchestrator.set_project_statement(
        project_dir,
        "There are finitely many unitary perfect numbers (via Goto's bound).",
        source="manual",
    )
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)

    local_asset_root = tmp_path / "local_assets"
    local_asset_root.mkdir(parents=True, exist_ok=True)
    (local_asset_root / "goto2007.pdf").write_bytes(b"%PDF-1.4")
    (local_asset_root / "the-fifth-unitary-perfect-number.pdf").write_bytes(b"%PDF-1.4")
    write_json(
        project_dir / "idea" / "proof_path_assessment.json",
        {
            "status": "generated",
            "readiness_tier": "promising",
            "local_assets": [{"path": str(local_asset_root)}],
        },
    )
    write_json(
        project_dir / "artifacts" / "lean_build_report.json",
        {
            "status": "needs_attention",
            "diagnostics": ["Companion theorem source remains unfinished."],
            "sorry_count": 0,
        },
    )
    write_json(
        project_dir / "artifacts" / "review_report.json",
        {
            "status": "blocked",
            "blockers": ["Lean build status is `needs_attention` instead of `passed`."],
            "warnings": [],
        },
    )

    orchestrator.plan_convergence(project_dir)
    requirements = json.loads((project_dir / "artifacts" / "external_requirements.json").read_text(encoding="utf-8"))
    statuses = {item["title"]: item["status"] for item in requirements["requirements"]}

    assert statuses["Goto (2007), Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers"] == "local_copy_available"
    assert statuses["Wall (1975), The Fifth Unitary Perfect Number"] == "local_copy_available"
