import json
from pathlib import Path

from ara_math.cli import main
from ara_math.workspace import write_json


def test_init_comath_project_and_project_dashboard_cli(tmp_path: Path, capsys) -> None:
    project_dir = tmp_path / "projects" / "cli-toy"
    (project_dir / "idea").mkdir(parents=True)
    write_json(
        project_dir / "project_manifest.json",
        {
            "project_name": "Manifest Name",
            "project_slug": "manifest-name",
            "problem": {"statement": "Prove the manifest statement."},
        },
    )

    exit_code = main(
        [
            "--json",
            "init-comath-project",
            "--project",
            str(project_dir),
            "--project-name",
            "CLI Toy",
            "--original-goal",
            "Prove the CLI toy statement.",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["state"]["project_name"] == "CLI Toy"
    assert payload["state"]["original_goal"] == "Prove the CLI toy statement."
    assert (project_dir / "comath" / "project_state.json").exists()
    assert (project_dir / "comath" / "project_dashboard.md").exists()

    exit_code = main(["project-dashboard", "--project", str(project_dir)])
    dashboard = capsys.readouterr().out

    assert exit_code == 0
    assert "# CoMath Dashboard: CLI Toy" in dashboard
    assert "Prove the CLI toy statement." in dashboard


def test_add_and_review_workstream_cli_are_state_only(tmp_path: Path, capsys) -> None:
    project_dir = tmp_path / "projects" / "cli-review"
    goal_file = tmp_path / "goal.md"
    goal_file.write_text("Prove the main route or record the missing lemma.\n", encoding="utf-8")

    add_exit = main(
        [
            "--json",
            "add-workstream",
            "--project",
            str(project_dir),
            "--workstream-id",
            "proof-main",
            "--kind",
            "proof",
            "--goal-file",
            str(goal_file),
            "--dependency",
            "source-main",
            "--blocker",
            "Needs source alignment.",
        ]
    )
    add_payload = json.loads(capsys.readouterr().out)

    assert add_exit == 0
    assert add_payload["workstream"]["workstream_id"] == "proof-main"
    assert add_payload["workstream"]["kind"] == "proof"
    assert add_payload["workstream"]["dependencies"] == ["source-main"]
    assert (project_dir / "comath" / "workstreams" / "proof-main" / "goal.md").read_text(
        encoding="utf-8"
    ) == "Prove the main route or record the missing lemma.\n"

    review_exit = main(
        [
            "--json",
            "review-workstream",
            "--project",
            str(project_dir),
            "--workstream",
            "proof-main",
            "--reviewers",
            "logic,source,lean",
            "--notes",
            "Manual review pending.",
            "--state-only",
        ]
    )
    review_payload = json.loads(capsys.readouterr().out)
    state = json.loads((project_dir / "comath" / "project_state.json").read_text(encoding="utf-8"))
    status = json.loads(
        (project_dir / "comath" / "workstreams" / "proof-main" / "status.json").read_text(encoding="utf-8")
    )

    assert review_exit == 0
    assert review_payload["mode"] == "state_only"
    assert review_payload["round_id"] == "round-001"
    assert [item["kind"] for item in review_payload["reviews"]] == ["logic", "source", "lean"]
    assert {item["decision"] for item in review_payload["reviews"]} == {"pending"}
    assert state["status"] == "review_gate"
    assert len(state["reviews"]) == 3
    assert status["status"] == "needs_review"
    assert (
        project_dir
        / "comath"
        / "workstreams"
        / "proof-main"
        / "reviews"
        / "round-001"
        / "decision.json"
    ).exists()

    dashboard_exit = main(["--json", "project-dashboard", "--project", str(project_dir)])
    dashboard_payload = json.loads(capsys.readouterr().out)

    assert dashboard_exit == 0
    assert "| proof-main | proof | needs_review | Prove the main route or record the missing lemma. | 1 |" in dashboard_payload[
        "dashboard"
    ]
    assert "- Reviews: 3" in dashboard_payload["dashboard"]


def test_add_workstream_cli_can_derive_stable_id(tmp_path: Path, capsys) -> None:
    project_dir = tmp_path / "projects" / "cli-derived-id"

    exit_code = main(
        [
            "--json",
            "add-workstream",
            "--project",
            str(project_dir),
            "--kind",
            "source",
            "--goal",
            "Source certify the central theorem.",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["workstream"]["workstream_id"] == "source-source-certify-the-central-theorem"
    assert (project_dir / "comath" / "workstreams" / "source-source-certify-the-central-theorem").is_dir()
