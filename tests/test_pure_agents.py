from __future__ import annotations

import json
from pathlib import Path

from ara_math.pure_agents import (
    CodexEpisodeConfig,
    CodexEpisodeLoopAgent,
    LeanFromNaturalProofAgent,
    NaturalLanguageTheoremProverAgent,
    UnifiedProofAgentLoop,
    _extract_lean_target_name,
)


def test_codex_episode_loop_lets_backend_own_actions(tmp_path: Path, monkeypatch) -> None:
    config = CodexEpisodeConfig(
        name="episode-test",
        system_prompt="Run one autonomous episode.",
        workspace=tmp_path,
        output_root=tmp_path / "runs",
        backend="codex",
        run_name="scripted",
        max_episodes=3,
    )
    loop = CodexEpisodeLoopAgent(config)

    def fake_codex(*, prompt: str, cwd: Path, output_path: Path, timeout_sec: int) -> dict[str, object]:
        assert "Do not return JSON tool actions" in prompt
        assert cwd == loop.run_dir
        (cwd / "proof_package.md").write_text("Proof candidate.\n", encoding="utf-8")
        output_path.write_text("STATUS: proved_candidate\nNEXT: stop\n", encoding="utf-8")
        return {"backend": "fake", "status": "completed", "returncode": 0, "elapsed_seconds": 0.01}

    monkeypatch.setattr(loop, "_call_codex", fake_codex)

    def observe(episode: int, episode_dir: Path, last_message: str, backend_report: dict[str, object]) -> dict[str, object]:
        del episode_dir, backend_report
        return {
            "episode": episode,
            "status": "proved_candidate",
            "terminal": (loop.run_dir / "proof_package.md").exists() and "STATUS: proved_candidate" in last_message,
        }

    report = loop.run(goal="Write a proof package.", episode_cwd=loop.run_dir, observer=observe)

    assert report["status"] == "proved_candidate"
    assert report["episodes_completed"] == 1
    assert (Path(report["run_dir"]) / "proof_package.md").read_text(encoding="utf-8") == "Proof candidate.\n"


def test_natural_language_theorem_agent_backend_none_writes_artifacts(tmp_path: Path) -> None:
    agent = NaturalLanguageTheoremProverAgent(repo_root=tmp_path)

    report = agent.run(
        statement="Prove that True is true.",
        backend="none",
        output_root=tmp_path / "nl-runs",
        run_name="none",
    )

    run_dir = Path(report["run_dir"])
    assert report["status"] == "blocked"
    assert report["episodes_completed"] == 1
    assert (run_dir / "statement.md").exists()
    assert (run_dir / "context_bundle.md").exists()
    assert (run_dir / "observations.json").exists()


def test_natural_language_agent_writes_fallback_blocker_after_unproductive_episode(tmp_path: Path) -> None:
    agent = NaturalLanguageTheoremProverAgent(repo_root=tmp_path)
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "dependency_graph.md").write_text("Known graph only.\n", encoding="utf-8")

    observation = agent._artifact_observation(
        run_dir,
        "STATUS: partial\nNEXT: continue\n",
        {"status": "timeout"},
        episode=1,
    )

    blocker = run_dir / "blocker.md"
    assert blocker.exists()
    assert "did not leave a complete proof package" in blocker.read_text(encoding="utf-8")
    assert observation["artifacts"]["blocker.md"]["exists"] is True
    assert observation["terminal"] is False
    assert "existing recovery artifacts" in observation["next_episode_directive"]


def test_natural_language_blocked_can_continue_when_backend_available(tmp_path: Path) -> None:
    agent = NaturalLanguageTheoremProverAgent(repo_root=tmp_path)
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "blocker.md").write_text("Need a sharper invariant.\n", encoding="utf-8")

    observation = agent._artifact_observation(
        run_dir,
        "STATUS: blocked\nNEXT: continue\n",
        {"status": "completed"},
        episode=1,
    )

    assert observation["status"] == "blocked"
    assert observation["terminal"] is False
    assert observation["next"] == "continue"


def test_natural_language_agent_writes_failed_routes_after_repeated_thin_recovery(tmp_path: Path) -> None:
    agent = NaturalLanguageTheoremProverAgent(repo_root=tmp_path)
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "blocker.md").write_text("Need a sharper invariant.\n", encoding="utf-8")

    observation = agent._artifact_observation(
        run_dir,
        "STATUS: partial\nNEXT: continue\n",
        {"status": "timeout"},
        episode=2,
    )

    failed_routes = run_dir / "failed_routes.md"
    assert failed_routes.exists()
    assert "did not leave partial lemmas" in failed_routes.read_text(encoding="utf-8")
    assert observation["artifacts"]["failed_routes.md"]["exists"] is True


def test_lean_agent_initially_verifies_clean_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject\n", encoding="utf-8")
    (workspace / "MathProject" / "MainClaim.lean").write_text(
        "namespace MathProject\n\ntheorem t : True := by\n  trivial\n\nend MathProject\n",
        encoding="utf-8",
    )
    agent = LeanFromNaturalProofAgent(repo_root=tmp_path)

    report = agent.run(
        workspace=workspace,
        proof_package="Proof: trivial.",
        statement="theorem t : True",
        build_command=["python3", "-c", "print('ok')"],
        backend="none",
        output_root=tmp_path / "lean-runs",
        run_name="clean",
    )

    assert report["status"] == "verified"
    assert report["episodes_completed"] == 0
    assert report["stop_reason"] == "initial_observation_terminal"


def test_lean_target_extraction_ignores_prose_theorem_mentions() -> None:
    statement = """The final target theorem must be named:

```lean
theorem imo2025_p1_possible_ks_complete :
    True
```
"""

    assert _extract_lean_target_name(statement) == "imo2025_p1_possible_ks_complete"


def test_lean_agent_backend_none_records_environment_when_unfinished(tmp_path: Path) -> None:
    workspace = tmp_path / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject\n", encoding="utf-8")
    (workspace / "MathProject" / "MainClaim.lean").write_text(
        "namespace MathProject\n\ntheorem t : True := by\n  sorry\n\nend MathProject\n",
        encoding="utf-8",
    )
    agent = LeanFromNaturalProofAgent(repo_root=tmp_path)

    report = agent.run(
        workspace=workspace,
        proof_package="Proof: trivial.",
        statement="theorem t : True",
        build_command=["python3", "-c", "print('ok')"],
        backend="none",
        output_root=tmp_path / "lean-runs",
        run_name="unfinished",
    )

    run_dir = Path(report["run_dir"])
    environment = json.loads((run_dir / "formalizer_environment.json").read_text(encoding="utf-8"))
    assert report["status"] == "blocked"
    assert report["episodes_completed"] == 1
    assert report["final_observation"]["counts"]["sorry"] == 1
    assert environment["build_command"] == ["python3", "-c", "print('ok')"]
    assert (run_dir / "proof_package.md").read_text(encoding="utf-8").strip() == "Proof: trivial."


def test_unified_proof_agent_backend_none_bootstraps_tool_state(tmp_path: Path) -> None:
    agent = UnifiedProofAgentLoop(repo_root=tmp_path)

    report = agent.run(
        statement="Prove that True is true.",
        backend="none",
        build_command=["python3", "-c", "print('ok')"],
        output_root=tmp_path / "proof-runs",
        run_name="none",
    )

    run_dir = Path(report["run_dir"])
    assert report["status"] == "blocked"
    assert report["episodes_completed"] == 1
    assert (run_dir / "tool_registry.md").exists()
    assert "lean_quick_check" in (run_dir / "tool_registry.md").read_text(encoding="utf-8")
    assert (run_dir / "proof_state.json").exists()
    assert (run_dir / "proof_notes.md").exists()
    assert (run_dir / "lemma_backlog.md").exists()


def test_unified_proof_agent_initially_verifies_existing_target(tmp_path: Path) -> None:
    workspace = tmp_path / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject\n", encoding="utf-8")
    (workspace / "MathProject" / "MainClaim.lean").write_text(
        "namespace MathProject\n\ntheorem t : True := by\n  trivial\n\nend MathProject\n",
        encoding="utf-8",
    )
    agent = UnifiedProofAgentLoop(repo_root=tmp_path)

    report = agent.run(
        statement="theorem t : True",
        workspace=workspace,
        build_command=["python3", "-c", "print('ok')"],
        backend="none",
        output_root=tmp_path / "proof-runs",
        run_name="verified",
    )

    assert report["status"] == "verified"
    assert report["episodes_completed"] == 0
    assert report["stop_reason"] == "initial_observation_terminal"
    run_dir = Path(report["run_dir"])
    tool_payload = json.loads((run_dir / "tool_registry.json").read_text(encoding="utf-8"))
    assert tool_payload["environment"]["workspace"]["exists"] is True
