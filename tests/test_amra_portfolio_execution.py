from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from amra.portfolio_campaign import PortfolioCampaignRunner
from ara_math.models import ProblemRecord
from ara_math.problem_bank import save_problem_bank


class FakeScoutRunner:
    def run(self, **kwargs: Any) -> dict[str, Any]:
        payload = {
            "schema_version": "ara_math.math_scout_report.v1",
            "generated_at": "2026-05-19T00:00:00+00:00",
            "status": "completed",
            "stop_reason": "fake_scout",
            "backend": "none",
            "entries": [],
            "ranked_candidates": [],
            "processed_problem_count": 0,
        }
        output_path = kwargs.get("output_path")
        if isinstance(output_path, Path):
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return payload


class FakeAttackRunner:
    def __init__(self, outcomes: dict[str, str]) -> None:
        self.outcomes = outcomes
        self.calls: list[dict[str, Any]] = []

    def run(
        self,
        *,
        assignment: dict[str, Any],
        problem: Any,
        project_dir: Path,
        problem_dir: Path,
        campaign_dir: Path,
        budget_seconds: int,
        run_id: str,
    ) -> dict[str, Any]:
        del problem, problem_dir, campaign_dir
        problem_id = str(assignment["problem_id"])
        outcome = self.outcomes[problem_id]
        self.calls.append(
            {
                "problem_id": problem_id,
                "run_id": run_id,
                "project_dir": project_dir,
                "budget_seconds": budget_seconds,
                "isolated_workspace": assignment["isolated_workspace"],
            }
        )
        base = {
            "problem_id": problem_id,
            "run_id": run_id,
            "status": outcome,
            "outcome": outcome,
            "summary": f"fake outcome {outcome}",
        }
        if outcome == "verified":
            return {
                **base,
                "verified": True,
                "verified_declarations": [
                    {"name": "main_verified", "full_name": f"{problem_id}.main_verified", "kind": "theorem"}
                ],
            }
        if outcome == "failed":
            return {
                **base,
                "stop_reason": "fake_failure",
                "failed_routes": [
                    {
                        "route_id": f"{problem_id}-route",
                        "failure_mode": "proof_gap",
                        "failed_assertion": "fake blocker",
                        "resume_condition": "fake new lemma is available",
                    }
                ],
            }
        if outcome == "library_candidate":
            return {
                **base,
                "verified": True,
                "library_candidate": True,
                "verified_declarations": [
                    {"name": "reusable", "full_name": f"{problem_id}.reusable", "kind": "lemma"}
                ],
                "library_candidates": [{"module": "AmraLibrary.Test", "declarations": [f"{problem_id}.reusable"]}],
            }
        return {**base, "parking_reason": "fake parked"}


def _write_bank(path: Path, problem_ids: list[str]) -> None:
    save_problem_bank(
        [
            ProblemRecord(
                problem_id=problem_id,
                title=problem_id.replace("-", " ").title(),
                source="unit",
                statement=f"Prove the exact identity for {problem_id}.",
                domain="number_theory",
                tags=["number theory"],
                references=[f"https://example.test/{problem_id}"],
            )
            for problem_id in problem_ids
        ],
        path,
    )


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_portfolio_campaign_runs_fake_active_attempts_for_budgeted_promotions(tmp_path: Path) -> None:
    outcomes = {
        "p-verified": "verified",
        "p-failed": "failed",
        "p-parked": "parked",
        "p-library": "library_candidate",
    }
    bank_path = tmp_path / "bank.yaml"
    _write_bank(bank_path, list(outcomes))
    attack_runner = FakeAttackRunner(outcomes)

    result = PortfolioCampaignRunner(
        repo_root=tmp_path,
        math_scout_runner=FakeScoutRunner(),
        attack_runner=attack_runner,
    ).run_portfolio_campaign(
        bank=bank_path,
        run_name="active execution unit",
        scout_limit=4,
        promote_top=4,
        attack_budget=300,
    )

    campaign_dir = tmp_path / result["campaign_dir"]
    active = _read_json(campaign_dir / "active_execution_report.json")
    assignments = _read_json(campaign_dir / "active_assignments.json")["assignments"]

    assert active["outcome_counts"] == {"failed": 1, "library_candidate": 1, "parked": 1, "verified": 1}
    assert len(attack_runner.calls) == 4
    assert {call["budget_seconds"] for call in attack_runner.calls} == {300}
    assert all("/workspaces/" in call["isolated_workspace"] for call in attack_runner.calls)
    assert {item["outcome"] for item in assignments} == {"verified", "failed", "parked", "library_candidate"}

    expected_states = {
        "p-verified": "verified",
        "p-failed": "failed",
        "p-parked": "parked",
        "p-library": "library_candidate",
    }
    for item in active["results"]:
        problem_id = item["problem_id"]
        project = tmp_path / item["project"]
        report = _read_json(tmp_path / item["report"])
        state = _read_json(project / "state.json")
        assert item["state"] == expected_states[problem_id]
        assert state["state"] == expected_states[problem_id]
        assert report["workspace_policy"] == "isolated"
        assert (project / "workspaces" / item["run_id"] / "formal").exists()

    failed_project = campaign_dir / "projects" / "p-failed"
    failed_routes = _read_json(failed_project / "memory" / "failed_routes.json")
    assert failed_routes["failed_routes"][0]["failure_mode"] == "proof_gap"

    verified_project = campaign_dir / "projects" / "p-verified"
    verified_declarations = _read_json(verified_project / "verified_declarations.json")
    assert verified_declarations["declarations"][0]["full_name"] == "p-verified.main_verified"

    library_project = campaign_dir / "projects" / "p-library"
    assert (library_project / "review" / next(path.name for path in (library_project / "review").glob("library_candidate_*.json"))).exists()


def test_portfolio_campaign_does_not_call_active_runner_without_attack_budget(tmp_path: Path) -> None:
    bank_path = tmp_path / "bank.yaml"
    _write_bank(bank_path, ["p-no-budget"])
    attack_runner = FakeAttackRunner({"p-no-budget": "verified"})

    result = PortfolioCampaignRunner(
        repo_root=tmp_path,
        math_scout_runner=FakeScoutRunner(),
        attack_runner=attack_runner,
    ).run_portfolio_campaign(
        bank=bank_path,
        run_name="no budget unit",
        scout_limit=1,
        promote_top=1,
        attack_budget=0,
    )

    campaign_dir = tmp_path / result["campaign_dir"]
    state = _read_json(campaign_dir / "campaign_state.json")
    assignments = _read_json(campaign_dir / "active_assignments.json")["assignments"]

    assert attack_runner.calls == []
    assert state["status"] == "planned"
    assert assignments[0]["status"] == "queued"
    assert assignments[0]["budget_seconds"] == 0
    assert not (campaign_dir / "active_execution_report.json").exists()
