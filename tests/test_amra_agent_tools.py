from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from amra.agents import (
    AMRA_AGENT_RUN_DIR_ENV,
    AMRA_AGENT_WORKSPACE_ENV,
    LEGACY_AGENT_RUN_DIR_ENV,
    LEGACY_AGENT_WORKSPACE_ENV,
    CodexEpisodeConfig,
    CodexEpisodeLoopAgent,
    ProofArtifactTracker,
    ToolRegistry,
    ToolSpec,
    agent_environment,
)
from amra.agents import tools as canonical_tools


def test_amra_agents_package_exports_agent_tool_contracts() -> None:
    assert ToolRegistry is canonical_tools.ToolRegistry
    assert ToolSpec is canonical_tools.ToolSpec

    env = agent_environment(run_dir=Path("/tmp/amra-run"), workspace=Path("/tmp/amra-workspace"))
    assert env == {
        AMRA_AGENT_RUN_DIR_ENV: "/tmp/amra-run",
        AMRA_AGENT_WORKSPACE_ENV: "/tmp/amra-workspace",
        LEGACY_AGENT_RUN_DIR_ENV: "/tmp/amra-run",
        LEGACY_AGENT_WORKSPACE_ENV: "/tmp/amra-workspace",
    }


def test_episode_loop_sets_amra_and_legacy_env_for_fake_backend(tmp_path: Path, monkeypatch) -> None:
    config = CodexEpisodeConfig(
        name="env-test",
        system_prompt="Run fake episode.",
        workspace=tmp_path / "workspace",
        output_root=tmp_path / "runs",
        backend="codex",
        run_name="env",
        max_episodes=1,
    )
    config.workspace.mkdir()
    loop = CodexEpisodeLoopAgent(config)
    captured: dict[str, object] = {}

    def fake_which(name: str) -> str | None:
        return "/usr/bin/codex" if name == "codex" else None

    def fake_run(**kwargs):
        captured["command"] = kwargs["args"] if "args" in kwargs else kwargs.get("command")
        captured["env"] = kwargs["env"]
        return SimpleNamespace(returncode=0, stdout="STATUS: partial\nNEXT: stop\n", stderr="")

    def fake_subprocess_run(command, **kwargs):
        kwargs["command"] = command
        return fake_run(**kwargs)

    monkeypatch.setattr("amra.agents.episode_loop.shutil.which", fake_which)
    monkeypatch.setattr("amra.agents.episode_loop.subprocess.run", fake_subprocess_run)

    output_path = loop.run_dir / "episode.md"
    report = loop._call_codex(
        prompt="Use fake backend.",
        cwd=loop.run_dir,
        output_path=output_path,
        timeout_sec=3,
    )

    env = captured["env"]
    assert report["status"] == "completed"
    assert env[AMRA_AGENT_RUN_DIR_ENV] == str(loop.run_dir)
    assert env[AMRA_AGENT_WORKSPACE_ENV] == str(loop.workspace)
    assert env[LEGACY_AGENT_RUN_DIR_ENV] == str(loop.run_dir)
    assert env[LEGACY_AGENT_WORKSPACE_ENV] == str(loop.workspace)
    assert output_path.read_text(encoding="utf-8").startswith("STATUS: partial")


def test_proof_artifact_tracker_is_available_from_amra_agents(tmp_path: Path) -> None:
    registry = ToolRegistry()
    registry.write_artifacts(tmp_path, workspace=None)
    tracker = ProofArtifactTracker(tmp_path)

    payload = tracker.bootstrap(
        statement="theorem t : True",
        workspace=None,
        build_command=["lake", "build"],
        target_name="t",
        tool_registry_path=tmp_path / "tool_registry.md",
    )

    assert payload["mode"] == "unified_proof_development"
    assert (tmp_path / "proof_state.json").exists()
    assert (tmp_path / "proof_notes.md").read_text(encoding="utf-8") == "# Proof Notes\n\n"
