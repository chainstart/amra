from __future__ import annotations

import json
from pathlib import Path

import pytest

from amra.portfolio_scheduler import LockAcquisitionError, PortfolioAttackScheduler


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_portfolio_lock_files_record_owner_pid_started_at_and_timeout(tmp_path: Path) -> None:
    scheduler = PortfolioAttackScheduler(repo_root=tmp_path, owner="worker-a", lock_timeout_seconds=120)
    project = tmp_path / "projects" / "p1"

    lock = scheduler.state_lock(project)
    payload = lock.acquire()
    lock_payload = json.loads((project / ".locks" / "state.lock").read_text(encoding="utf-8"))

    assert lock_payload["owner"] == "worker-a"
    assert lock_payload["pid"] == payload["pid"]
    assert lock_payload["started_at"]
    assert lock_payload["timeout"] == 120
    assert lock_payload["timeout_seconds"] == 120

    with pytest.raises(LockAcquisitionError):
        scheduler.state_lock(project, owner="worker-b").acquire()

    lock.release()
    assert not (project / ".locks" / "state.lock").exists()


def test_scheduler_assigns_budget_only_to_promoted_targets(tmp_path: Path) -> None:
    campaign_dir = tmp_path / "artifacts" / "portfolio_campaigns" / "unit"
    _write_json(
        campaign_dir / "promotion_queue.json",
        {
            "schema_version": "amra.promotion_queue.v1",
            "items": [
                {"problem_id": "promoted-problem", "priority": 42.0, "recommendation": "promote"},
            ],
        },
    )
    _write_json(
        campaign_dir / "parked_queue.json",
        {
            "schema_version": "amra.parked_queue.v1",
            "items": [
                {"problem_id": "parked-problem", "priority": 1.0, "recommendation": "park"},
            ],
        },
    )
    scheduler = PortfolioAttackScheduler(repo_root=tmp_path)

    active = scheduler.schedule_from_campaign(
        campaign_dir=campaign_dir,
        campaign_id="unit",
        attack_budget_seconds=900,
    )

    assignments = active["assignments"]
    assert [item["problem_id"] for item in assignments] == ["promoted-problem"]
    assert assignments[0]["budget_seconds"] == 900
    assert assignments[0]["workspace_policy"] == "isolated"
    assert assignments[0]["isolated_workspace"].endswith(
        "artifacts/portfolio_campaigns/unit/projects/promoted-problem/workspaces/unit-001-promoted-problem/formal"
    )
    assert "parked-problem" not in json.dumps(active)
    assert scheduler.can_allocate_attack_budget(
        problem_id="promoted-problem",
        promoted_problem_ids=scheduler.promoted_problem_ids(campaign_dir),
    )
    assert not scheduler.can_allocate_attack_budget(
        problem_id="parked-problem",
        promoted_problem_ids=scheduler.promoted_problem_ids(campaign_dir),
    )
    assert (campaign_dir / "projects" / "promoted-problem" / "workspaces" / "unit-001-promoted-problem" / "formal").exists()


def test_reviewed_verified_workspace_is_required_before_canonical_merge(tmp_path: Path) -> None:
    project = tmp_path / "projects" / "p1"
    canonical = project / "formal" / "MathProject" / "MainClaim.lean"
    isolated = project / "workspaces" / "run-1" / "formal" / "MathProject" / "MainClaim.lean"
    canonical.parent.mkdir(parents=True)
    isolated.parent.mkdir(parents=True)
    canonical.write_text("theorem t : True := by\n  trivial\n", encoding="utf-8")
    isolated.write_text("theorem t : True := by\n  trivial\n\nlemma u : True := by\n  trivial\n", encoding="utf-8")
    scheduler = PortfolioAttackScheduler(repo_root=tmp_path)

    unreviewed = scheduler.merge_reviewed_formal_workspace(
        project_dir=project,
        run_id="run-1",
        status="verified",
        review_status="pending",
        library_module="MathProject.MainClaim",
    )

    assert unreviewed["merged"] is False
    assert "review_not_approved" in unreviewed["blockers"]
    assert "lemma u" not in canonical.read_text(encoding="utf-8")

    merged = scheduler.merge_reviewed_formal_workspace(
        project_dir=project,
        run_id="run-1",
        status="verified",
        review_status="approved",
        library_module="MathProject.MainClaim",
    )

    assert merged["merged"] is True
    assert "lemma u" in canonical.read_text(encoding="utf-8")
    assert not (project / ".locks" / "formal.lock").exists()
    assert not (project / ".locks" / "library-promotion.lock").exists()
