import json
import subprocess
from pathlib import Path

from ara_math.cli import main
from ara_math.comath_capabilities import refine_intake_project, run_comath_evaluation
from ara_math.comath_runners import execute_workstream
from ara_math.comath_specialists import (
    CodexCliSpecialistProvider,
    FakeSpecialistProvider,
    build_specialist_prompt_bundle,
    run_specialist,
    run_specialist_loop,
)
from ara_math.coordinator import comath_paths


def test_fake_specialist_run_persists_prompt_output_and_workstream_state(tmp_path: Path) -> None:
    project_dir = tmp_path / "specialist-project"
    refine_intake_project(project_dir, goal="Prove a source-grounded theorem.", project_name="Specialist")

    payload = run_specialist(
        project_dir,
        role_id="source_auditor",
        workstream_id="source-literature-audit",
        backend="fake",
        run_name="source-round-1",
        task="Check whether the source theorem is certified.",
    )
    paths = comath_paths(project_dir)
    state = json.loads(paths.project_state.read_text(encoding="utf-8"))
    source_ws = next(item for item in state["workstreams"] if item["workstream_id"] == "source-literature-audit")
    graph = json.loads(paths.artifact_graph.read_text(encoding="utf-8"))
    dashboard = paths.dashboard.read_text(encoding="utf-8")

    assert payload["provider"]["provider"] == "fake"
    assert Path(payload["prompt_path"]).exists()
    assert Path(payload["output_path"]).read_text(encoding="utf-8").startswith("Status: completed")
    assert source_ws["status"] == "needs_review"
    assert source_ws["metadata"]["latest_specialist_run"]["role_id"] == "source_auditor"
    assert any(node["node_id"].startswith("specialist:source_auditor:source-round-1") for node in graph["nodes"])
    assert "## Specialist Runs" in dashboard


def test_specialist_loop_runs_selected_fake_roles(tmp_path: Path) -> None:
    project_dir = tmp_path / "specialist-loop-project"
    refine_intake_project(project_dir, goal="Prove a theorem with several specialist roles.", project_name="Loop")

    report = run_specialist_loop(
        project_dir,
        roles=["ideation_specialist", "source_auditor"],
        backend="fake",
        max_specialists=2,
        max_parallel_specialists=2,
        run_name="loop-smoke",
    )

    assert report["executed_count"] == 2
    assert {item["role_id"] for item in report["selected"]} == {"ideation_specialist", "source_auditor"}
    assert (project_dir / "comath" / "specialist_loops" / "loop-smoke" / "report.json").exists()
    assert len(list((project_dir / "comath" / "specialists").glob("*/runs/*/result.json"))) == 2


def test_codex_cli_provider_builds_command_without_real_service(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "codex-command-project"
    refine_intake_project(project_dir, goal="Inspect Codex provider command.", project_name="Codex Command")
    bundle = build_specialist_prompt_bundle(
        project_dir,
        role_id="proof_reviewer",
        task="Review the current proof route.",
        run_name="proof-review-command",
    )
    seen: dict[str, object] = {}

    def fake_runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        seen["command"] = command
        seen["cwd"] = kwargs["cwd"]
        output_path = Path(command[command.index("--output-last-message") + 1])
        output_path.write_text("Status: completed\nBlockers: none\n", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, "codex stdout", "")

    monkeypatch.setattr("ara_math.comath_specialists.shutil.which", lambda name: "/usr/bin/codex")
    provider = CodexCliSpecialistProvider(
        model="gpt-5.5",
        reasoning_effort="xhigh",
        timeout_seconds=123,
        allow_search=True,
        command_runner=fake_runner,
    )
    result = provider.run(bundle)
    command = seen["command"]

    assert result.status == "completed"
    assert command[:5] == ["/usr/bin/codex", "-s", "read-only", "-a", "never"]
    assert "--search" in command
    assert ["-m", "gpt-5.5"] == command[command.index("-m") : command.index("-m") + 2]
    assert 'model_reasoning_effort="xhigh"' in command
    assert "exec" in command
    assert seen["cwd"] == bundle.run_dir


def test_llm_specialist_workstream_executor_uses_fake_backend(tmp_path: Path) -> None:
    project_dir = tmp_path / "executor-project"
    refine_intake_project(project_dir, goal="Run source specialist through workstream executor.", project_name="Executor")

    payload = execute_workstream(
        project_dir,
        "source-literature-audit",
        executor_name="llm_specialist",
        options={"backend": "fake", "run_name": "executor-source-specialist"},
    )

    assert payload["executor"] == "llm_specialist"
    assert payload["workstream"]["status"] == "needs_review"
    assert payload["workstream"]["metadata"]["latest_specialist_run"]["role_id"] == "source_auditor"


def test_specialist_cli_and_evaluation_smoke(tmp_path: Path, capsys) -> None:
    project_dir = tmp_path / "cli-specialist-project"
    refine_intake_project(project_dir, goal="Prove a CLI specialist theorem.", project_name="CLI Specialist")

    run_exit = main(
        [
            "--json",
            "run-comath-specialist",
            "--project",
            str(project_dir),
            "--role",
            "theory_builder",
            "--workstream",
            "theory-building-memory",
            "--backend",
            "fake",
            "--run-name",
            "cli-theory-specialist",
        ]
    )
    run_payload = json.loads(capsys.readouterr().out)
    loop_exit = main(
        [
            "--json",
            "run-comath-specialist-loop",
            "--project",
            str(project_dir),
            "--roles",
            "ideation_specialist,source_auditor",
            "--backend",
            "fake",
            "--max-parallel-specialists",
            "2",
            "--run-name",
            "cli-specialist-loop",
        ]
    )
    loop_payload = json.loads(capsys.readouterr().out)
    evaluation = run_comath_evaluation(project_dir)
    statuses = {item["capability"]: item["status"] for item in evaluation["report"]["checks"]}

    assert run_exit == 0
    assert loop_exit == 0
    assert run_payload["provider"]["provider"] == "fake"
    assert loop_payload["executed_count"] == 2
    assert statuses["llm_specialist_orchestration"] == "implemented"
