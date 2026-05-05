import json
import sys
from pathlib import Path
from subprocess import CompletedProcess

from ara_math.cli import main
from ara_math.orchestrator import MathResearchOrchestrator
from ara_math.problem_bank import save_problem_bank
from ara_math.models import ProblemRecord
from ara_math.workspace import write_json


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _write_clean_formal_sources(project_dir: Path, theorem_prefix: str) -> None:
    (project_dir / "formal" / "MathProject" / "GeneratedClaims.lean").write_text(
        "\n".join(
            [
                "import MathProject.Basic",
                "",
                "namespace MathProject",
                "",
                f"theorem {theorem_prefix}_definitions : True := by",
                "  trivial",
                "",
                f"theorem {theorem_prefix}_lemmas : True := by",
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
                f"theorem {theorem_prefix}_main : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_run_proof_search_converges_on_clean_project(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="search-clean",
                title="Search Clean Problem",
                source="test",
                statement="A small formalization target.",
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
    project_dir = orchestrator.create_project(problem_id="search-clean", name="search-clean-20260421")
    orchestrator.set_project_statement(project_dir, "For all n, the search-clean property holds.", source="manual")
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)
    _write_clean_formal_sources(project_dir, "search_clean")

    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    result = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    status_payload = json.loads((project_dir / "proof" / "proof_search_status.json").read_text(encoding="utf-8"))
    attempts_log = (project_dir / "proof" / "proof_search_attempts.jsonl").read_text(encoding="utf-8")
    attempt_report = json.loads((project_dir / "proof" / "attempts" / "attempt_01" / "attempt_report.json").read_text(encoding="utf-8"))

    assert result["status"] == "converged"
    assert status_payload["status"] == "converged"
    assert attempt_report["selected_agenda_item_id"]
    assert attempt_report["search_policy"] == "best_first_frontier"
    assert '"outcome": "converged"' in attempts_log


def test_run_proof_search_reuses_previous_attempt_history(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="search-history",
                title="Search History Problem",
                source="test",
                statement="A reusable proof-search target.",
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
    project_dir = orchestrator.create_project(problem_id="search-history", name="search-history-20260421")
    orchestrator.set_project_statement(project_dir, "For all n, the search-history property holds.", source="manual")
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)
    _write_clean_formal_sources(project_dir, "search_history")

    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    first = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )
    second = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    assert first["attempts_completed"] == 1
    assert second["attempts_completed"] == 2
    assert (project_dir / "proof" / "attempts" / "attempt_02" / "attempt_report.json").exists()


def test_run_proof_search_uses_numeric_attempt_ordering_after_99(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="search-numeric-order",
                title="Search Numeric Ordering Problem",
                source="test",
                statement="A proof-search target with many historical attempts.",
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
    project_dir = orchestrator.create_project(problem_id="search-numeric-order", name="search-numeric-order-20260424")
    orchestrator.set_project_statement(project_dir, "For all n, numeric ordering stays stable.", source="manual")
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)
    _write_clean_formal_sources(project_dir, "search_numeric_order")

    attempts_root = project_dir / "proof" / "attempts"
    for attempt_index in range(99, 106):
        attempt_dir = attempts_root / f"attempt_{attempt_index:02d}"
        attempt_dir.mkdir(parents=True, exist_ok=True)
        write_json(
            attempt_dir / "attempt_report.json",
            {
                "attempt_index": attempt_index,
                "outcome": "checkpoint",
                "build_status": "passed",
                "review_status": "checkpoint_verified",
            },
        )

    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    result = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    assert result["attempts_completed"] == 106
    assert (project_dir / "proof" / "attempts" / "attempt_106" / "attempt_report.json").exists()


def test_run_open_campaign_processes_multiple_shortlist_entries(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="campaign-a",
                title="Campaign A",
                source="test",
                statement="Statement A.",
                domain="number_theory",
                open_problem=True,
            ),
            ProblemRecord(
                problem_id="campaign-b",
                title="Campaign B",
                source="test",
                statement="Statement B.",
                domain="geometry",
                open_problem=True,
            ),
        ],
        bank_path,
    )
    scout_report_path = tmp_path / "scout.json"
    write_json(
        scout_report_path,
        {
            "shortlist_candidates": [
                {"problem_id": "campaign-a"},
                {"problem_id": "campaign-b"},
            ]
        },
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )

    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "run_project",
        lambda **kwargs: {
            "status": "exhausted" if kwargs["project_dir"].name.startswith("campaign-a") else "timeout",
            "attempts_completed": 1,
        },
    )

    payload = orchestrator.run_open_problem_campaign(
        scout_report_path=scout_report_path,
        limit=2,
        backend="none",
        max_attempts=1,
        max_runtime_sec=30,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    assert len(payload["entries"]) == 2
    assert {entry["status"] for entry in payload["entries"]} == {"exhausted", "timeout"}


def test_run_open_campaign_matches_existing_project_by_manifest_problem_id(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="17",
                title="Erdős Problem #17",
                source="Erdős Problems",
                statement="Statement 17.",
                domain="number_theory",
                open_problem=True,
            )
        ],
        bank_path,
    )
    scout_report_path = tmp_path / "scout.json"
    write_json(scout_report_path, {"shortlist_candidates": [{"problem_id": "17"}]})
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )
    wrong_project = orchestrator.projects_root / "triangle-dissection-17-campaign-20260421"
    wrong_project.mkdir(parents=True, exist_ok=True)
    write_json(
        wrong_project / "project_manifest.json",
        {
            "project_name": "triangle-dissection-17-campaign-20260421",
            "problem": {"problem_id": "triangle-dissection-17"},
        },
    )

    captured_dirs: list[str] = []

    def _fake_run_project(**kwargs):
        captured_dirs.append(str(kwargs["project_dir"]))
        return {"status": "exhausted", "attempts_completed": 1}

    monkeypatch.setattr(orchestrator.proof_search_runner, "run_project", _fake_run_project)

    payload = orchestrator.run_open_problem_campaign(
        scout_report_path=scout_report_path,
        limit=1,
        backend="none",
        max_attempts=1,
        max_runtime_sec=30,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    assert len(payload["entries"]) == 1
    assert Path(payload["entries"][0]["project_dir"]).name.startswith("17-campaign-")
    assert Path(captured_dirs[0]).name.startswith("17-campaign-")


def test_run_light_sweep_uses_backend_only_for_seeded_entries(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="17",
                title="Erdős Problem #17",
                source="Erdős Problems",
                statement="Placeholder.",
                domain="number_theory",
                open_problem=True,
            ),
            ProblemRecord(
                problem_id="18",
                title="Erdős Problem #18",
                source="Erdős Problems",
                statement="Placeholder.",
                domain="number_theory",
                open_problem=True,
            ),
        ],
        bank_path,
    )
    orchestrator = MathResearchOrchestrator(
        repo_root=_repo_root(),
        projects_root=tmp_path / "projects",
        bank_path=bank_path,
    )

    def _fake_plan(project_dir: Path) -> dict[str, object]:
        manifest = json.loads((project_dir / "project_manifest.json").read_text(encoding="utf-8"))
        problem_id = manifest["problem"]["problem_id"]
        if problem_id == "17":
            write_json(
                project_dir / "idea" / "statement_recovery.json",
                {"status": "recovered", "statement": "Recovered statement 17", "source": "local"},
            )
            write_json(
                project_dir / "idea" / "proof_path_assessment.json",
                {"readiness_tier": "promising", "local_assets": [{"path": "/tmp/asset"}]},
            )
            write_json(
                project_dir / "idea" / "literature_evidence.json",
                {"counts": {"known_results": 1, "proof_ingredients": 1, "modern_tools": 0, "open_gaps": 0}},
            )
        else:
            write_json(
                project_dir / "idea" / "statement_recovery.json",
                {"status": "not_found", "statement": "", "source": ""},
            )
            write_json(
                project_dir / "idea" / "proof_path_assessment.json",
                {"readiness_tier": "needs_statement_recovery", "local_assets": []},
            )
            write_json(
                project_dir / "idea" / "literature_evidence.json",
                {"counts": {"known_results": 0, "proof_ingredients": 0, "modern_tools": 0, "open_gaps": 0}},
            )
        return {"tasks": [{"task_id": f"{problem_id}:task"}]}

    monkeypatch.setattr(orchestrator, "plan_project", _fake_plan)
    monkeypatch.setattr(orchestrator, "prepare_formal", lambda project_dir: {"placeholder_claim_count": 1})
    monkeypatch.setattr(orchestrator, "build_lean", lambda project_dir, timeout_sec=None: {"status": "blocked"})
    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "_wait_for_headroom",
        lambda: {"status": "ready", "snapshot": {}, "blockers": [], "thresholds": {}},
    )
    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "run_project",
        lambda **kwargs: {
            "status": "exhausted",
            "attempts_completed": 1,
            "best_attempt": {"theorem_hint_count": 2},
        },
    )
    monkeypatch.setattr(
        orchestrator,
        "write_manuscript",
        lambda project_dir: {"manuscript_path": str(project_dir / "writing" / "research_report.md"), "deliverable_type": "research_report"},
    )
    monkeypatch.setattr(orchestrator, "review_project", lambda project_dir: {"status": "blocked"})

    payload = orchestrator.run_erdos_light_sweep(
        backend="none",
        problem_limit=2,
        max_runtime_sec=120,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    assert len(payload["entries"]) == 2
    by_id = {entry["problem_id"]: entry for entry in payload["entries"]}
    assert by_id["17"]["proof_search_mode"] == "backend"
    assert by_id["17"]["proof_search_status"] == "exhausted"
    assert by_id["18"]["proof_search_mode"] == "seed_only"
    assert by_id["18"]["proof_search_status"] == "seed_only"
    assert payload["next_focus_candidates"][0]["problem_id"] == "17"


def test_run_proof_search_defers_when_system_headroom_stays_blocked(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="search-deferred",
                title="Search Deferred Problem",
                source="test",
                statement="Deferred search target.",
                domain="number_theory",
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
    project_dir = orchestrator.create_project(problem_id="search-deferred", name="search-deferred-20260421")
    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "_wait_for_headroom",
        lambda: {
            "status": "blocked",
            "snapshot": {"mem_available_mb": 512.0, "load_per_cpu": 2.1},
            "blockers": ["System remained above guarded resource thresholds."],
            "thresholds": {"min_available_memory_mb": 2048, "max_load_per_cpu": 1.5},
            "waited_seconds": 0.0,
            "poll_count": 1,
            "polls": [],
        },
    )

    result = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=2,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    assert result["status"] == "deferred"
    assert result["attempts_completed"] == 0
    assert result["system_guard"]["status"] == "blocked"


def test_run_proof_search_refreshes_placeholder_plan_before_attempt(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="refresh-plan",
                title="Refresh Placeholder Plan",
                source="test",
                statement="Placeholder planning target.",
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
    project_dir = orchestrator.create_project(problem_id="refresh-plan", name="refresh-plan-20260421")
    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "_wait_for_headroom",
        lambda: {"status": "ready", "snapshot": {}, "blockers": [], "thresholds": {}},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    result = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    proof_plan = json.loads((project_dir / "proof" / "proof_plan.json").read_text(encoding="utf-8"))
    claim_registry = json.loads((project_dir / "proof" / "claim_registry.json").read_text(encoding="utf-8"))
    theorem_inventory = json.loads((project_dir / "proof" / "theorem_inventory.json").read_text(encoding="utf-8"))
    frameworks = json.loads((project_dir / "proof" / "proof_path_frameworks.json").read_text(encoding="utf-8"))
    scaffold = json.loads((project_dir / "proof" / "proof_route_scaffold.json").read_text(encoding="utf-8"))
    route_discovery = json.loads((project_dir / "proof" / "route_discovery_brief.json").read_text(encoding="utf-8"))
    search_context = json.loads((project_dir / "proof" / "proof_search_context.json").read_text(encoding="utf-8"))

    assert result["status"] == "exhausted"
    assert len(proof_plan["tasks"]) >= 6
    assert len(claim_registry["claims"]) >= 4
    assert theorem_inventory["entry_count"] >= 1
    assert frameworks["framework_count"] >= 1
    assert scaffold["selected_framework_id"]
    assert route_discovery["route_candidates"]
    assert search_context["focus_mode"] == "default"


def test_run_proof_search_route_discovery_mode_records_focus_mode(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="route-discovery",
                title="Route Discovery Problem",
                source="test",
                statement="Find a route before Lean proof repair.",
                domain="geometry",
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
    project_dir = orchestrator.create_project(problem_id="route-discovery", name="route-discovery-20260422")
    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "_wait_for_headroom",
        lambda: {"status": "ready", "snapshot": {}, "blockers": [], "thresholds": {}},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    result = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
        focus_mode="route_discovery",
    )

    status_payload = json.loads((project_dir / "proof" / "proof_search_status.json").read_text(encoding="utf-8"))
    search_context = json.loads((project_dir / "proof" / "proof_search_context.json").read_text(encoding="utf-8"))
    attempt_report = json.loads(
        (project_dir / "proof" / "attempts" / "attempt_01" / "attempt_report.json").read_text(encoding="utf-8")
    )

    assert result["focus_mode"] == "route_discovery"
    assert status_payload["focus_mode"] == "route_discovery"
    assert search_context["focus_mode"] == "route_discovery"
    assert attempt_report["focus_mode"] == "route_discovery"


def test_run_proof_search_paper_first_mode_records_focus_mode(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="paper-first",
                title="Paper First Problem",
                source="test",
                statement="Find the mathematical route before Lean formalization.",
                domain="geometry",
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
    project_dir = orchestrator.create_project(problem_id="paper-first", name="paper-first-20260424")
    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "_wait_for_headroom",
        lambda: {"status": "ready", "snapshot": {}, "blockers": [], "thresholds": {}},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    result = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
        focus_mode="paper_first",
    )

    status_payload = json.loads((project_dir / "proof" / "proof_search_status.json").read_text(encoding="utf-8"))
    search_context = json.loads((project_dir / "proof" / "proof_search_context.json").read_text(encoding="utf-8"))
    attempt_report = json.loads(
        (project_dir / "proof" / "attempts" / "attempt_01" / "attempt_report.json").read_text(encoding="utf-8")
    )

    assert result["focus_mode"] == "paper_first"
    assert status_payload["focus_mode"] == "paper_first"
    assert search_context["focus_mode"] == "paper_first"
    assert attempt_report["focus_mode"] == "paper_first"


def test_run_proof_search_prompt_and_context_include_strategy_guidance(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="strategy-guidance",
                title="Strategy Guidance Problem",
                source="test",
                statement="Find a literature-backed route before claiming the open problem is solved.",
                domain="number_theory",
                tags=["computational_search"],
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
    project_dir = orchestrator.create_project(problem_id="strategy-guidance", name="strategy-guidance-20260425")
    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "_wait_for_headroom",
        lambda: {"status": "ready", "snapshot": {}, "blockers": [], "thresholds": {}},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    result = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    prompt_text = (
        project_dir / "proof" / "attempts" / "attempt_01" / "prompt.txt"
    ).read_text(encoding="utf-8")
    search_context = json.loads((project_dir / "proof" / "proof_search_context.json").read_text(encoding="utf-8"))
    strategy = json.loads((project_dir / "artifacts" / "open_problem_strategy.json").read_text(encoding="utf-8"))
    retrieval = json.loads((project_dir / "proof" / "premise_retrieval.json").read_text(encoding="utf-8"))
    accessible_graph = json.loads((project_dir / "proof" / "accessible_premise_graph.json").read_text(encoding="utf-8"))
    evaluator_plan = json.loads((project_dir / "proof" / "evaluator_plan.json").read_text(encoding="utf-8"))
    proof_system_benchmark = json.loads((project_dir / "proof" / "proof_system_benchmark.json").read_text(encoding="utf-8"))
    verifier_feedback = json.loads((project_dir / "proof" / "verifier_feedback.json").read_text(encoding="utf-8"))
    agenda = json.loads((project_dir / "proof" / "proof_search_agenda.json").read_text(encoding="utf-8"))

    assert result["status"] == "exhausted"
    assert "Case-study-guided strategy:" in prompt_text
    assert "Proof-system benchmark:" in prompt_text
    assert "Verifier feedback memory:" in prompt_text
    assert "Search agenda:" in prompt_text
    assert "Variant check:" in prompt_text
    assert "adversarial self-review" in prompt_text.lower()
    assert "Retrieval-augmented premise suggestions:" in prompt_text
    assert "Accessible premise graph:" in prompt_text
    assert "Evaluator plan:" in prompt_text
    assert search_context["strategy_profile_id"]
    assert strategy["strategy_profile_id"]
    assert search_context["strategy_required_check_count"] >= 4
    assert "checkpoint_contract_ready" in search_context
    assert search_context["retrieved_local_premise_count"] >= 0
    assert "accessible_premise_count" in search_context
    assert "evaluator_mode" in search_context
    assert search_context["search_policy"] == "best_first_frontier"
    assert search_context["selected_agenda_item_id"]
    assert retrieval["query_token_count"] >= 1
    assert "project_modules" in accessible_graph
    assert evaluator_plan["search_friendly"] is True
    assert evaluator_plan["evaluator_mode"] != "theorem_import_only"
    assert proof_system_benchmark["execution_policy"]["search_policy"] == "best_first_frontier"
    assert verifier_feedback["recommended_mode"]
    assert agenda["selected_item_id"]


def test_run_proof_search_honors_manual_focus_override(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="manual-focus",
                title="Manual Focus Problem",
                source="test",
                statement="Close the formal proof boundary for a narrowed theorem.",
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
    project_dir = orchestrator.create_project(problem_id="manual-focus", name="manual-focus-20260430")
    write_json(
        project_dir / "proof" / "proof_search_focus_override.json",
        {
            "enabled": True,
            "reason": "The automatic agenda is stale; focus on formal closure instead.",
            "selected_item": {
                "item_id": "axiom-cleanup",
                "kind": "formal_closure",
                "label": "Axiom cleanup",
                "target_statement": "Replace project-local axioms with imported theorems or explicit assumptions.",
                "target_files": [
                    "formal/MathProject/GeneratedClaims.lean",
                    "formal/MathProject/MainClaim.lean",
                    "proof/proof_gap_notes.md",
                ],
                "exit_criteria": [
                    "List every remaining axiom and classify it as imported, conditional, or blocked.",
                ],
            },
        },
    )
    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "_wait_for_headroom",
        lambda: {"status": "ready", "snapshot": {}, "blockers": [], "thresholds": {}},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    agenda = json.loads((project_dir / "proof" / "proof_search_agenda.json").read_text(encoding="utf-8"))
    current_focus = (project_dir / "proof" / "current_focus.md").read_text(encoding="utf-8")
    prompt = (project_dir / "proof" / "attempts" / "attempt_01" / "prompt.txt").read_text(encoding="utf-8")
    attempt_report = json.loads(
        (project_dir / "proof" / "attempts" / "attempt_01" / "attempt_report.json").read_text(encoding="utf-8")
    )

    assert agenda["selected_item_id"] == "axiom-cleanup"
    assert agenda["selected_item"]["kind"] == "formal_closure"
    assert agenda["manual_focus_override"]["path"] == "proof/proof_search_focus_override.json"
    assert "Axiom cleanup" in current_focus
    assert "Manual Focus Override" in current_focus
    assert "Axiom cleanup" in prompt
    assert attempt_report["selected_agenda_item_id"] == "axiom-cleanup"


def test_run_proof_search_accessibility_artifact_uses_lean_support(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="access-support",
                title="Accessibility Support Problem",
                source="test",
                statement="Accessibility support target.",
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
    project_dir = orchestrator.create_project(problem_id="access-support", name="access-support-20260425")
    orchestrator.set_project_statement(project_dir, "A bounded accessibility-support statement.", source="manual")
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)
    _write_clean_formal_sources(project_dir, "access_support")

    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "_scan_lean_inventory",
        lambda asset_paths, limit=80: [
            {
                "kind": "theorem",
                "name": "helper_bound",
                "statement": "True",
                "path": str(tmp_path / "assets" / "Companion" / "Helper.lean"),
                "line": 1,
                "source_root": str(tmp_path / "assets"),
            }
        ],
    )
    monkeypatch.setattr(
        orchestrator.proof_search_runner,
        "_select_theorem_hints",
        lambda inventory, recovered_statement, evidence, limit=8: inventory,
    )
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "discover_accessible_premise_support",
        lambda project_path: {
            "project_modules": ["MathProject.Basic", "MathProject.GeneratedClaims", "MathProject.MainClaim"],
            "project_imports": [],
            "compiled_modules": ["Companion.Helper"],
            "compiled_suffixes": {"Helper": ["Companion.Helper"]},
            "stage_plan": {
                "status": "ready",
                "modules": {"UnitaryPerfect.GotoBound": {"kind": "copy"}},
                "unresolved_imports": [],
                "blocked_sources": [],
            },
        },
    )
    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    result = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    accessible_graph = json.loads((project_dir / "proof" / "accessible_premise_graph.json").read_text(encoding="utf-8"))
    search_context = json.loads((project_dir / "proof" / "proof_search_context.json").read_text(encoding="utf-8"))
    prompt_text = (project_dir / "proof" / "attempts" / "attempt_01" / "prompt.txt").read_text(encoding="utf-8")

    assert result["status"] == "converged"
    assert accessible_graph["support_summary"]["compiled_module_count"] == 1
    assert accessible_graph["support_summary"]["staged_module_count"] == 1
    assert search_context["compiled_premise_count"] == 1
    assert search_context["staged_premise_count"] == 1
    assert accessible_graph["accessible_premises"][0]["access_reason"] == "compiled_module"
    assert "Support summary:" in prompt_text


def test_run_evaluator_executes_contract_command_and_writes_report(tmp_path: Path) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="evaluator-manual",
                title="Evaluator Manual Problem",
                source="test",
                statement="A finite computational-search checkpoint.",
                domain="number_theory",
                tags=["computational_search"],
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
    project_dir = orchestrator.create_project(problem_id="evaluator-manual", name="evaluator-manual-20260425")
    orchestrator.set_project_statement(project_dir, "Search odd n <= N for a bounded witness.", source="manual")
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)

    script_path = project_dir / "search_bound.py"
    script_path.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                'output = Path("proof") / "evaluator-output.json"',
                'output.write_text("{\\"status\\": \\"ok\\"}\\n", encoding="utf-8")',
                'print("bounded search complete")',
                "",
            ]
        ),
        encoding="utf-8",
    )
    contract = json.loads((project_dir / "proof" / "counterexample_search_contract.json").read_text(encoding="utf-8"))
    contract.update(
        {
            "status": "ready",
            "search_contract": "Check every odd n <= 25 against the current bounded witness predicate.",
            "command": [sys.executable, str(script_path)],
            "working_directory": "",
            "timeout_sec": 20,
            "auto_run_allowed": True,
            "expected_output_paths": ["proof/evaluator-output.json"],
        }
    )
    write_json(project_dir / "proof" / "counterexample_search_contract.json", contract)

    report = orchestrator.run_evaluator(project_dir, timeout_sec=20)
    refreshed_contract = json.loads((project_dir / "proof" / "counterexample_search_contract.json").read_text(encoding="utf-8"))

    assert report["status"] == "completed"
    assert report["command_source"] == "contract_command"
    assert report["expected_outputs"][0]["exists"] is True
    assert refreshed_contract["last_run_status"] == "completed"
    assert json.loads((project_dir / "proof" / "evaluator_report.json").read_text(encoding="utf-8"))["status"] == "completed"


def test_run_proof_search_auto_runs_evaluator_when_allowed(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="evaluator-auto",
                title="Evaluator Auto Problem",
                source="test",
                statement="A finite computational-search checkpoint.",
                domain="number_theory",
                tags=["computational_search"],
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
    project_dir = orchestrator.create_project(problem_id="evaluator-auto", name="evaluator-auto-20260425")
    orchestrator.set_project_statement(project_dir, "Search odd n <= N for a bounded witness.", source="manual")
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)
    _write_clean_formal_sources(project_dir, "evaluator_auto")

    script_path = project_dir / "auto_search.py"
    script_path.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                'output = Path("proof") / "auto-evaluator-output.json"',
                'output.write_text("{\\"status\\": \\"ok\\"}\\n", encoding="utf-8")',
                'print("auto evaluator complete")',
                "",
            ]
        ),
        encoding="utf-8",
    )
    contract = json.loads((project_dir / "proof" / "counterexample_search_contract.json").read_text(encoding="utf-8"))
    contract.update(
        {
            "status": "ready",
            "search_contract": "Check every odd n <= 25 against the current bounded witness predicate.",
            "command": [sys.executable, str(script_path)],
            "working_directory": "",
            "timeout_sec": 20,
            "auto_run_allowed": True,
            "expected_output_paths": ["proof/auto-evaluator-output.json"],
        }
    )
    write_json(project_dir / "proof" / "counterexample_search_contract.json", contract)

    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    result = orchestrator.run_proof_search(
        project_dir,
        backend="none",
        max_attempts=1,
        max_runtime_sec=60,
        attempt_timeout_sec=5,
        build_timeout_sec=1,
    )

    search_context = json.loads((project_dir / "proof" / "proof_search_context.json").read_text(encoding="utf-8"))
    attempt_report = json.loads((project_dir / "proof" / "attempts" / "attempt_01" / "attempt_report.json").read_text(encoding="utf-8"))
    prompt_text = (project_dir / "proof" / "attempts" / "attempt_01" / "prompt.txt").read_text(encoding="utf-8")
    evaluator_report = json.loads((project_dir / "proof" / "evaluator_report.json").read_text(encoding="utf-8"))

    assert result["status"] == "converged"
    assert evaluator_report["status"] == "completed"
    assert search_context["evaluator_report_status"] == "completed"
    assert attempt_report["evaluator_report_status"] == "completed"
    assert "Evaluator report:" in prompt_text


def test_invoke_backend_writes_artifact_on_failure(tmp_path: Path, monkeypatch) -> None:
    runner = MathResearchOrchestrator(repo_root=_repo_root()).proof_search_runner
    prompt_path = tmp_path / "prompt.txt"
    output_path = tmp_path / "backend_last_message.txt"
    prompt_path.write_text("hello\n", encoding="utf-8")
    monkeypatch.setattr("ara_math.proof_search.shutil.which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(
        "ara_math.proof_search.run_guarded_command",
        lambda command, cwd, timeout, memory_mb, cpu_seconds, max_processes, niceness: CompletedProcess(
            command,
            1,
            stdout="backend stdout\n",
            stderr="backend stderr\n",
        ),
    )

    report = runner._invoke_backend(
        backend="codex",
        project_dir=tmp_path,
        prompt_path=prompt_path,
        output_path=output_path,
        timeout_sec=5,
    )

    text = output_path.read_text(encoding="utf-8")
    assert report["status"] == "failed"
    assert "backend stdout" in text
    assert "backend stderr" in text


def test_run_proof_search_cli_writes_status_file(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "problem_bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="cli-search",
                title="CLI Search Problem",
                source="test",
                statement="CLI theorem search.",
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
    project_dir = orchestrator.create_project(problem_id="cli-search", name="cli-search-20260421")
    orchestrator.set_project_statement(project_dir, "For all n, cli-search holds.", source="manual")
    orchestrator.plan_project(project_dir)
    orchestrator.prepare_formal(project_dir)
    _write_clean_formal_sources(project_dir, "cli_search")

    monkeypatch.setattr("ara_math.cli.MathResearchOrchestrator", lambda **kwargs: orchestrator)
    monkeypatch.setattr(orchestrator.lean_executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "prepare_package_cache",
        lambda formal_dir: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(orchestrator.lean_executor, "package_cache_state", lambda formal_dir: "ready")
    monkeypatch.setattr(
        orchestrator.lean_executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="ok\n", stderr=""),
    )

    exit_code = main(
        [
            "--json",
            "run-proof-search",
            "--project",
            str(project_dir),
            "--bank",
            str(bank_path),
            "--backend",
            "none",
            "--attempts",
            "1",
            "--time-budget",
            "60",
            "--attempt-timeout",
            "5",
            "--build-timeout",
            "1",
        ]
    )

    status_payload = json.loads((project_dir / "proof" / "proof_search_status.json").read_text(encoding="utf-8"))
    assert exit_code == 0
    assert status_payload["status"] == "converged"
