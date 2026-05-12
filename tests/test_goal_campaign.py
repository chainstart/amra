from __future__ import annotations

import json
import sys
from pathlib import Path

from ara_math.cli import main
from ara_math.goal_campaign import GoalDrivenCampaignRunner, normalize_goal_manifest
from ara_math.workspace import write_json


def _write_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject\n", encoding="utf-8")
    (workspace / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem child_goal : True := by",
                "  trivial",
                "",
                "theorem root_goal : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return workspace


def _manifest(workspace: Path) -> dict:
    return normalize_goal_manifest(
        {
            "root_goal_id": "root",
            "settings": {
                "workspace": str(workspace),
                "build_command": [sys.executable, "-c", "print('mock build passed')"],
            },
            "goals": [
                {
                    "id": "root",
                    "kind": "root",
                    "statement": "Prove the original theorem.",
                    "target_theorem": "root_goal",
                    "target_file": "MathProject/MainClaim.lean",
                    "dependencies": ["child"],
                    "priority": 10_000,
                },
                {
                    "id": "child",
                    "kind": "subgoal",
                    "statement": "Prove the child theorem needed by the root theorem.",
                    "target_theorem": "child_goal",
                    "target_file": "MathProject/MainClaim.lean",
                    "dependencies": [],
                    "priority": 10,
                },
            ],
        }
    )


def test_goal_driven_campaign_verifies_child_before_root(tmp_path: Path) -> None:
    workspace = _write_workspace(tmp_path)
    manifest_path = tmp_path / "goal_manifest.json"
    write_json(manifest_path, _manifest(workspace))
    runner = GoalDrivenCampaignRunner(repo_root=tmp_path)

    report = runner.run(
        manifest_path=manifest_path,
        backend="none",
        rounds=4,
        time_budget_sec=120,
        child_rounds=1,
        child_time_budget_sec=30,
        child_attempts=0,
        child_build_timeout_sec=10,
        output_root=tmp_path / "runs",
        run_name="root-loop",
    )

    updated = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert report["status"] == "verified"
    assert report["stop_reason"] == "root_goal_verified"
    assert [entry["goal_id"] for entry in report["rounds"]] == ["child", "root"]
    assert {goal["id"]: goal["status"] for goal in updated["goals"]} == {
        "root": "verified",
        "child": "verified",
    }
    assert len(updated["gap_reviews"]) >= 2


def test_goal_driven_campaign_blocks_root_until_dependency_verified(tmp_path: Path) -> None:
    workspace = _write_workspace(tmp_path)
    manifest = _manifest(workspace)
    manifest["goals"][1]["target_theorem"] = "missing_child_goal"
    manifest_path = tmp_path / "goal_manifest.json"
    write_json(manifest_path, manifest)
    runner = GoalDrivenCampaignRunner(repo_root=tmp_path)

    report = runner.run(
        manifest_path=manifest_path,
        backend="none",
        rounds=1,
        time_budget_sec=120,
        child_rounds=1,
        child_time_budget_sec=30,
        child_attempts=0,
        child_build_timeout_sec=10,
        output_root=tmp_path / "runs",
        run_name="blocked-loop",
    )

    updated = json.loads(manifest_path.read_text(encoding="utf-8"))
    statuses = {goal["id"]: goal["status"] for goal in updated["goals"]}

    assert report["status"] == "partial"
    assert report["rounds"][0]["goal_id"] == "child"
    assert statuses["child"] == "partial"
    assert statuses["root"] == "pending"


def test_goal_campaign_cli_init_and_run(tmp_path: Path) -> None:
    workspace = _write_workspace(tmp_path)
    manifest_path = tmp_path / "cli_goal_manifest.json"

    init_exit = main(
        [
            "--json",
            "init-goal-campaign",
            "--output",
            str(manifest_path),
            "--root-statement",
            "Prove the CLI root theorem.",
            "--root-target-theorem",
            "root_goal",
            "--root-target-file",
            "MathProject/MainClaim.lean",
            "--workspace",
            str(workspace),
            "--build-command",
            f"{sys.executable} -c \"print('mock build passed')\"",
        ]
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["goals"].append(
        {
            "id": "child",
            "kind": "subgoal",
            "statement": "Prove child first.",
            "target_theorem": "child_goal",
            "target_file": "MathProject/MainClaim.lean",
            "dependencies": [],
            "status": "pending",
            "priority": 10,
            "run_history": [],
        }
    )
    manifest["goals"][0]["dependencies"] = ["child"]
    write_json(manifest_path, manifest)

    run_exit = main(
        [
            "--json",
            "run-goal-campaign",
            "--manifest",
            str(manifest_path),
            "--backend",
            "none",
            "--rounds",
            "4",
            "--time-budget",
            "120",
            "--child-rounds",
            "1",
            "--child-time-budget",
            "30",
            "--child-attempts",
            "0",
            "--child-build-timeout",
            "10",
            "--output-root",
            str(tmp_path / "cli-runs"),
        ]
    )
    updated = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert init_exit == 0
    assert run_exit == 0
    assert {goal["id"]: goal["status"] for goal in updated["goals"]} == {
        "root": "verified",
        "child": "verified",
    }
