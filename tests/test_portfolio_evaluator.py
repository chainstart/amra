import json
from pathlib import Path

from amra.portfolio_campaign import PortfolioCampaignRunner
from amra.portfolio_evaluator import DIFFICULTY_SCHEMA_VERSION, PortfolioEvaluator
from amra.portfolio_memory import record_failed_route, upsert_claim, upsert_route
from ara_math.cli import main


def _init_project(tmp_path: Path, problem_id: str, *, state: str = "scouted", manifest: bool = True) -> Path:
    project = tmp_path / "projects" / problem_id
    PortfolioCampaignRunner(repo_root=tmp_path).initialize_problem_project(project=project, problem_id=problem_id, state=state)
    if manifest:
        (project / "problem.yaml").write_text(
            "\n".join(
                [
                    f"problem_id: {problem_id}",
                    "statement: Prove that every integer equals itself.",
                    "source: unit-test-source",
                    "references:",
                    "  - https://example.test/source",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    return project


def test_evaluator_promotes_easy_known_theorem_without_writing_inputs(tmp_path: Path) -> None:
    project = _init_project(tmp_path, "easy-known", state="scouted")
    (project / "proof" / "sketches").mkdir(parents=True, exist_ok=True)
    (project / "proof" / "sketches" / "known.md").write_text(
        "Known theorem: this follows by reflexivity.\nProof sketch: apply rfl.\n",
        encoding="utf-8",
    )
    upsert_claim(
        project,
        {
            "claim_id": "main",
            "statement_nl": "Every integer equals itself.",
            "status": "route_supported",
            "known_theorem": True,
            "proof_evidence": ["proof/sketches/known.md"],
        },
    )

    report = PortfolioEvaluator(repo_root=tmp_path).evaluate_project(project=project, run_name="dry-eval")

    assert report["schema_version"] == DIFFICULTY_SCHEMA_VERSION
    assert report["recommendation"] == "promote"
    assert report["mode"] == "read_only_durable_artifacts"
    assert report["long_budget_allowed"] is True
    assert "projects/easy-known/memory/claim_ledger.json" in report["evidence"]
    assert not (project / "runs" / "dry-eval" / "difficulty.json").exists()


def test_counterexample_suspected_route_requires_review_before_long_budget(tmp_path: Path) -> None:
    project = _init_project(tmp_path, "counterexample-review", state="active_attack")
    record_failed_route(
        project,
        {
            "route_id": "diagonal-bound",
            "failure_mode": "counterexample_candidate",
            "resume_condition": "Refute or formalize the candidate first.",
            "evidence": [{"type": "counterexample_candidate", "path": "proof/blockers/diagonal.md"}],
        },
    )

    report = PortfolioEvaluator(repo_root=tmp_path).evaluate_project(project=project, run_name="eval")

    assert report["recommendation"] == "counterexample_review"
    assert report["long_budget_allowed"] is False
    assert report["budget_gate"]["reason"] == "counterexample_suspected_route_requires_review"
    assert "counterexample_candidate" in report["risk_flags"]


def test_strong_counterexample_candidate_freezes_route(tmp_path: Path) -> None:
    project = _init_project(tmp_path, "freeze-me", state="active_attack")
    record_failed_route(
        project,
        {
            "route_id": "false-inequality",
            "failure_mode": "counterexample_candidate",
            "strength": "strong",
            "formal_counterexample": "Lean witness sketch exists",
        },
    )

    report = PortfolioEvaluator(repo_root=tmp_path).evaluate_project(project=project, run_name="eval")

    assert report["recommendation"] == "freeze"
    assert report["long_budget_allowed"] is False
    assert "strong_counterexample" in report["risk_flags"]


def test_missing_statement_or_source_routes_to_source_recovery(tmp_path: Path) -> None:
    project = _init_project(tmp_path, "needs-source", state="scouted", manifest=False)

    report = PortfolioEvaluator(repo_root=tmp_path).evaluate_project(project=project, run_name="eval")

    assert report["recommendation"] == "source_recover"
    assert report["primary_blocker"] == "missing_exact_statement"
    assert report["long_budget_allowed"] is False


def test_partial_active_route_continues_but_repeated_stall_parks(tmp_path: Path) -> None:
    continue_project = _init_project(tmp_path, "continue-route", state="active_attack")
    upsert_route(
        continue_project,
        {
            "route_id": "main-route",
            "status": "promising",
            "attempt_history": [{"attempt_id": "a1", "progress_delta": 0.25}],
        },
    )

    continue_report = PortfolioEvaluator(repo_root=tmp_path).evaluate_project(project=continue_project, run_name="eval")

    parked_project = _init_project(tmp_path, "park-route", state="active_attack")
    for index in range(3):
        record_failed_route(
            parked_project,
            {
                "route_id": f"blocked-{index}",
                "failure_mode": "proof_gap",
                "failed_assertion": f"missing lemma {index}",
            },
        )
    attempt_dir = parked_project / "runs" / "stall" / "attempts" / "attempt_001"
    attempt_dir.mkdir(parents=True, exist_ok=True)
    (attempt_dir / "attempt_report.json").write_text(
        json.dumps({"progress_delta": 0.0, "verified": False}) + "\n",
        encoding="utf-8",
    )

    parked_report = PortfolioEvaluator(repo_root=tmp_path).evaluate_project(project=parked_project, run_name="eval")

    assert continue_report["recommendation"] == "continue"
    assert continue_report["long_budget_allowed"] is True
    assert continue_report["progress_signal"]["positive_progress_events"] == 1
    assert parked_report["recommendation"] == "park"
    assert "repeated_failed_routes" in parked_report["risk_flags"]


def test_parked_target_with_exhausted_routes_is_abandoned(tmp_path: Path) -> None:
    project = _init_project(tmp_path, "abandon-route", state="parked")
    for index in range(5):
        record_failed_route(
            project,
            {
                "route_id": f"blocked-{index}",
                "failure_mode": "proof_gap",
                "failed_assertion": f"missing independent lemma {index}",
            },
        )
    attempt_dir = project / "runs" / "stall" / "attempts" / "attempt_001"
    attempt_dir.mkdir(parents=True, exist_ok=True)
    (attempt_dir / "attempt_report.json").write_text(
        json.dumps({"progress_delta": 0.0, "verified": False}) + "\n",
        encoding="utf-8",
    )

    report = PortfolioEvaluator(repo_root=tmp_path).evaluate_project(project=project, run_name="eval")

    assert report["recommendation"] == "abandon"
    assert report["long_budget_allowed"] is False
    assert "abandon" in report["allowed_recommendations"]


def test_campaign_runner_and_cli_write_independent_difficulty_report(tmp_path: Path, monkeypatch) -> None:
    project = _init_project(tmp_path, "cli-eval", state="active_attack")
    record_failed_route(project, {"route_id": "route-main", "failure_mode": "counterexample_candidate"})
    monkeypatch.setenv("AMRA_REPO_ROOT", str(tmp_path))

    exit_code = main(["--json", "evaluate-problem", "--project", str(project), "--run-name", "eval-1"])
    report = json.loads((project / "runs" / "eval-1" / "difficulty.json").read_text(encoding="utf-8"))

    assert exit_code == 0
    assert report["schema_version"] == DIFFICULTY_SCHEMA_VERSION
    assert report["recommendation"] == "counterexample_review"
    assert (tmp_path / "artifacts" / "global_memory" / "failed_route_index.json").exists()
    assert (project / "difficulty.json").exists()
