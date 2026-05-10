import json
from pathlib import Path

from ara_math.cli import main
from ara_math.comath_capabilities import (
    create_computation_certificate,
    refine_intake_project,
    run_comath_evaluation,
    update_theory_memory,
    verify_computation_certificate,
)
from ara_math.comath_specialists import run_specialist
from ara_math.coordinator import comath_paths, initialize_comath_project
from ara_math.workstreams import WorkstreamKind, WorkstreamStatus


def test_intake_refines_goal_and_installs_specialist_contracts(tmp_path: Path) -> None:
    project_dir = tmp_path / "intake-project"
    context = tmp_path / "context.md"
    context.write_text("Known source note.\n", encoding="utf-8")

    payload = refine_intake_project(
        project_dir,
        goal="classify dense block obstructions",
        project_name="Intake",
        domain="additive combinatorics",
        context_files=[context],
    )
    paths = comath_paths(project_dir)
    state = json.loads(paths.project_state.read_text(encoding="utf-8"))
    intake = json.loads((paths.root / "intake_plan.json").read_text(encoding="utf-8"))
    roles = json.loads((paths.root / "specialist_roles.json").read_text(encoding="utf-8"))
    ledger = json.loads(paths.uncertainty_ledger.read_text(encoding="utf-8"))
    dashboard = paths.dashboard.read_text(encoding="utf-8")

    assert payload["intake_plan"]["refined_goal"] == "classify dense block obstructions"
    assert state["status"] == "goals_planned"
    assert {item["kind"] for item in state["workstreams"]} >= {
        WorkstreamKind.PROOF.value,
        WorkstreamKind.SOURCE.value,
        WorkstreamKind.COMPUTE.value,
        WorkstreamKind.LEAN.value,
        WorkstreamKind.REVIEW.value,
    }
    assert "source-literature-audit" in intake["workstream_ids"]
    assert {role["role_id"] for role in roles["roles"]} >= {"project_coordinator", "theory_builder"}
    assert {item["item_id"] for item in ledger["items"]} >= {
        "intake-source-certification",
        "intake-computation-reproducibility",
    }
    assert "## Refined Goal" in dashboard
    assert "## Specialist Roles" in dashboard


def test_computation_certificate_records_hashes_and_verifies(tmp_path: Path) -> None:
    project_dir = tmp_path / "compute-project"
    refine_intake_project(project_dir, goal="Prove by certified search.", project_name="Compute")

    payload = create_computation_certificate(
        project_dir,
        workstream_id="computation-exploration",
        command=["python3", "-c", "from pathlib import Path; Path('out.txt').write_text('42\\n')"],
        cwd=project_dir,
        output_paths=[Path("out.txt")],
        seed="seed-1",
    )
    verification = verify_computation_certificate(
        project_dir,
        manifest_path=Path(payload["manifest_path"]),
        rerun=True,
    )
    state = json.loads(comath_paths(project_dir).project_state.read_text(encoding="utf-8"))
    compute_ws = next(item for item in state["workstreams"] if item["workstream_id"] == "computation-exploration")

    assert payload["certificate"]["verified"] is True
    assert payload["certificate"]["output_hashes"]["out.txt"]
    assert verification["report"]["verified"] is True
    assert compute_ws["status"] == WorkstreamStatus.NEEDS_REVIEW.value
    assert compute_ws["metadata"]["latest_computation_certificate"]["verified"] is True


def test_failed_computation_manifest_does_not_verify_without_rerun(tmp_path: Path) -> None:
    project_dir = tmp_path / "failed-compute-project"
    refine_intake_project(project_dir, goal="Reject failed computation.", project_name="Failed Compute")

    payload = create_computation_certificate(
        project_dir,
        workstream_id="computation-exploration",
        command=["python3", "-c", "raise SystemExit(7)"],
        cwd=project_dir,
    )
    verification = verify_computation_certificate(project_dir, manifest_path=Path(payload["manifest_path"]))

    assert payload["certificate"]["verified"] is False
    assert verification["report"]["verified"] is False


def test_theory_memory_and_evaluation_cover_public_paper_capabilities(tmp_path: Path) -> None:
    project_dir = tmp_path / "eval-project"
    refine_intake_project(project_dir, goal="Prove the evaluation theorem.", project_name="Eval")
    create_computation_certificate(
        project_dir,
        workstream_id="computation-exploration",
        command=["python3", "-c", "print('stable certificate')"],
        cwd=project_dir,
        seed="eval-seed",
    )
    memory = update_theory_memory(
        project_dir,
        conjecture="A density increment closes the hard case.",
        lemma="Every certified block has a reusable interval decomposition.",
        failed_hypothesis="A parity-only split proves only a weaker theorem.",
        novelty_note="The interval decomposition suggests a separate lemma inventory.",
        new_direction="Try a source-first dense interval theorem.",
    )
    run_specialist(
        project_dir,
        role_id="theory_builder",
        workstream_id="theory-building-memory",
        backend="fake",
        run_name="eval-theory-specialist",
    )
    evaluation = run_comath_evaluation(project_dir)
    statuses = {item["capability"]: item["status"] for item in evaluation["report"]["checks"]}

    assert len(memory["memory"]["conjectures"]) == 1
    assert len(memory["memory"]["lemmas"]) == 1
    assert len(memory["memory"]["failed_hypotheses"]) == 1
    assert statuses["intent_refinement"] == "implemented"
    assert statuses["specialist_agents"] == "implemented"
    assert statuses["llm_specialist_orchestration"] == "implemented"
    assert statuses["computational_exploration"] == "implemented"
    assert statuses["theory_building"] == "implemented"
    assert statuses["review_gates"] == "partial"
    assert evaluation["report"]["scope_note"].startswith("Local architecture parity")


def test_comath_capability_cli_smoke(tmp_path: Path, capsys) -> None:
    project_dir = tmp_path / "cli-capabilities"
    initialize_comath_project(project_dir, project_name="CLI Cap", original_goal="Prove the CLI capability theorem.")

    intake_exit = main(
        [
            "--json",
            "intake-comath-project",
            "--project",
            str(project_dir),
            "--goal",
            "Prove the CLI capability theorem.",
            "--domain",
            "number theory",
        ]
    )
    intake_payload = json.loads(capsys.readouterr().out)

    compute_exit = main(
        [
            "--json",
            "record-computation-certificate",
            "--project",
            str(project_dir),
            "--workstream",
            "computation-exploration",
            "--command",
            "python3 -c \"print('cli cert')\"",
            "--seed",
            "cli-seed",
        ]
    )
    compute_payload = json.loads(capsys.readouterr().out)

    theory_exit = main(
        [
            "--json",
            "update-theory-memory",
            "--project",
            str(project_dir),
            "--new-direction",
            "Use a source-first proof route.",
        ]
    )
    theory_payload = json.loads(capsys.readouterr().out)

    specialist_exit = main(
        [
            "--json",
            "run-comath-specialist",
            "--project",
            str(project_dir),
            "--role",
            "source_auditor",
            "--workstream",
            "source-literature-audit",
            "--backend",
            "fake",
            "--run-name",
            "cli-source-specialist",
        ]
    )
    specialist_payload = json.loads(capsys.readouterr().out)

    eval_exit = main(["--json", "run-comath-evaluation", "--project", str(project_dir)])
    eval_payload = json.loads(capsys.readouterr().out)

    assert intake_exit == 0
    assert compute_exit == 0
    assert theory_exit == 0
    assert specialist_exit == 0
    assert eval_exit == 0
    assert "source-literature-audit" in intake_payload["intake_plan"]["workstream_ids"]
    assert compute_payload["certificate"]["verified"] is True
    assert theory_payload["memory"]["new_direction_candidates"]
    assert specialist_payload["provider"]["provider"] == "fake"
    assert eval_payload["report"]["score"]["missing"] == 0
