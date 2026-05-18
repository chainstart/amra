from __future__ import annotations

import json
import sys
from pathlib import Path

from ara_math.cli import main
from ara_math.focused_attack import FocusedLeanAttackAgent, load_expected_target_headers
from ara_math.pure_agents import CodexEpisodeLoopAgent


def _write_workspace(tmp_path: Path, body: str) -> Path:
    workspace = tmp_path / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject\n", encoding="utf-8")
    (workspace / "MathProject" / "MainClaim.lean").write_text(body, encoding="utf-8")
    return workspace


def test_focused_attack_initially_verifies_all_required_targets(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "namespace MathProject\n\n"
        "theorem t : True := by\n"
        "  trivial\n\n"
        "lemma u : True := by\n"
        "  trivial\n\n"
        "end MathProject\n",
    )
    agent = FocusedLeanAttackAgent(repo_root=tmp_path)

    report = agent.run(
        workspace=workspace,
        attack_targets=["MathProject.t", "u"],
        build_command=[sys.executable, "-c", "print('ok')"],
        backend="none",
        output_root=tmp_path / "runs",
        run_name="clean",
    )

    assert report["status"] == "verified"
    assert report["episodes_completed"] == 0
    assert report["final_observation"]["contract_satisfied"] is True
    assert report["stop_reason"] == "initial_observation_terminal"


def test_focused_attack_backend_none_reports_missing_target(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "namespace MathProject\n\n"
        "theorem other : True := by\n"
        "  trivial\n\n"
        "end MathProject\n",
    )
    agent = FocusedLeanAttackAgent(repo_root=tmp_path)

    report = agent.run(
        workspace=workspace,
        attack_targets=["missing_target"],
        build_command=[sys.executable, "-c", "print('ok')"],
        backend="none",
        output_root=tmp_path / "runs",
        run_name="missing",
    )

    run_dir = Path(report["run_dir"])
    contract = json.loads((run_dir / "focus_contract.json").read_text(encoding="utf-8"))

    assert report["status"] == "blocked"
    assert report["episodes_completed"] == 1
    assert report["final_observation"]["missing_targets"] == ["missing_target"]
    assert contract["attack_targets"] == ["missing_target"]


def test_focused_attack_flags_disallowed_lean_file_changes(tmp_path: Path, monkeypatch) -> None:
    workspace = _write_workspace(tmp_path, "namespace MathProject\n\nend MathProject\n")
    agent = FocusedLeanAttackAgent(repo_root=tmp_path)

    def fake_codex(
        self: CodexEpisodeLoopAgent,
        *,
        prompt: str,
        cwd: Path,
        output_path: Path,
        timeout_sec: int,
    ) -> dict[str, object]:
        del self, prompt, timeout_sec
        (cwd / "MathProject" / "MainClaim.lean").write_text(
            "namespace MathProject\n\n"
            "theorem t : True := by\n"
            "  trivial\n\n"
            "end MathProject\n",
            encoding="utf-8",
        )
        (cwd / "MathProject" / "Other.lean").write_text(
            "namespace MathProject\n\n"
            "theorem extra : True := by\n"
            "  trivial\n\n"
            "end MathProject\n",
            encoding="utf-8",
        )
        output_path.write_text("STATUS: verified\nNEXT: stop\n", encoding="utf-8")
        return {"backend": "fake", "status": "completed", "returncode": 0, "elapsed_seconds": 0.01}

    monkeypatch.setattr(CodexEpisodeLoopAgent, "_call_codex", fake_codex)

    report = agent.run(
        workspace=workspace,
        attack_targets=["t"],
        allowed_files=[Path("MathProject/MainClaim.lean")],
        build_command=[sys.executable, "-c", "print('ok')"],
        backend="codex",
        max_steps=1,
        output_root=tmp_path / "runs",
        run_name="disallowed-file",
    )

    assert report["status"] == "partial"
    assert report["final_observation"]["disallowed_file_changes"] == [
        {"path": "MathProject/Other.lean", "change": "added"}
    ]


def test_focused_attack_flags_new_conditional_wrapper(tmp_path: Path, monkeypatch) -> None:
    workspace = _write_workspace(tmp_path, "namespace MathProject\n\nend MathProject\n")
    agent = FocusedLeanAttackAgent(repo_root=tmp_path)

    def fake_codex(
        self: CodexEpisodeLoopAgent,
        *,
        prompt: str,
        cwd: Path,
        output_path: Path,
        timeout_sec: int,
    ) -> dict[str, object]:
        del self, prompt, timeout_sec
        (cwd / "MathProject" / "MainClaim.lean").write_text(
            "namespace MathProject\n\n"
            "theorem t : True := by\n"
            "  trivial\n\n"
            "theorem weak_wrapper : True -> True := by\n"
            "  intro h\n"
            "  exact h\n\n"
            "end MathProject\n",
            encoding="utf-8",
        )
        output_path.write_text("STATUS: verified\nNEXT: stop\n", encoding="utf-8")
        return {"backend": "fake", "status": "completed", "returncode": 0, "elapsed_seconds": 0.01}

    monkeypatch.setattr(CodexEpisodeLoopAgent, "_call_codex", fake_codex)

    report = agent.run(
        workspace=workspace,
        attack_targets=["t"],
        allowed_files=[Path("MathProject/MainClaim.lean")],
        forbid_new_conditional_wrappers=True,
        build_command=[sys.executable, "-c", "print('ok')"],
        backend="codex",
        max_steps=1,
        output_root=tmp_path / "runs",
        run_name="wrapper",
    )

    violations = report["final_observation"]["new_declaration_violations"]

    assert report["status"] == "partial"
    assert len(violations) == 1
    assert violations[0]["full_name"] == "MathProject.weak_wrapper"
    assert violations[0]["violation_reason"] == "new_conditional_wrapper"


def test_load_expected_target_headers_matches_attack_targets(tmp_path: Path) -> None:
    header_file = tmp_path / "target.lean"
    header_file.write_text(
        "theorem t : True := by\n"
        "  trivial\n",
        encoding="utf-8",
    )

    headers = load_expected_target_headers([header_file], ["MathProject.t"])

    assert headers == {"MathProject.t": "theorem t : True"}


def test_focused_attack_cli_smoke(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "namespace MathProject\n\n"
        "theorem t : True := by\n"
        "  trivial\n\n"
        "end MathProject\n",
    )

    exit_code = main(
        [
            "--json",
            "run-focused-lean-attack",
            "--workspace",
            str(workspace),
            "--attack-target",
            "t",
            "--build-command",
            f"{sys.executable} -c \"print('ok')\"",
            "--backend",
            "none",
            "--output-root",
            str(tmp_path / "cli-runs"),
            "--run-name",
            "cli",
        ]
    )
    report = json.loads((tmp_path / "cli-runs" / "cli" / "report.json").read_text(encoding="utf-8"))

    assert exit_code == 0
    assert report["status"] == "verified"


def test_focused_attack_can_run_in_isolated_portfolio_workspace(tmp_path: Path) -> None:
    project = tmp_path / "projects" / "focused-problem"
    workspace = project / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject\n", encoding="utf-8")
    (workspace / "MathProject" / "MainClaim.lean").write_text(
        "namespace MathProject\n\n"
        "theorem t : True := by\n"
        "  trivial\n\n"
        "end MathProject\n",
        encoding="utf-8",
    )
    agent = FocusedLeanAttackAgent(repo_root=tmp_path)

    report = agent.run(
        workspace=workspace,
        attack_targets=["t"],
        build_command=[sys.executable, "-c", "print('ok')"],
        backend="none",
        output_root=tmp_path / "runs",
        run_name="isolated-focused",
        project_dir=project,
        problem_id="focused-problem",
        workspace_run_id="run-a",
        use_isolated_workspace=True,
    )

    assert report["status"] == "verified"
    assert report["workspace_isolated"] is True
    assert Path(report["workspace"]) == project / "workspaces" / "run-a" / "formal"
    assert report["canonical_workspace"] == str(workspace.resolve())
    assert report["progress_velocity"]["schema_version"] == "amra.progress_velocity.v1"
