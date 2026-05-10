import json
from pathlib import Path

from ara_math.coordinator import (
    add_workstream,
    comath_paths,
    initialize_comath_project,
    run_comath_loop,
    select_next_workstreams,
)
from ara_math.uncertainty import SourceDebtStatus, UncertaintyItem, UncertaintyKind, save_uncertainty_ledger
from ara_math.uncertainty import load_uncertainty_ledger
from ara_math.workstreams import WorkstreamKind, WorkstreamRecord, WorkstreamStatus
from ara_math.workspace import write_text


def test_scheduler_prioritizes_active_bottleneck_and_ready_dependencies(tmp_path: Path) -> None:
    project_dir = tmp_path / "scheduler-priority"
    initialize_comath_project(project_dir, project_name="Priority", original_goal="Prove the priority theorem.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="proof-main",
            kind=WorkstreamKind.PROOF,
            goal="Find a route after source alignment.",
        ),
    )
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="source-main",
            kind=WorkstreamKind.SOURCE,
            goal="Resolve the source debt.",
        ),
    )
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="lean-main",
            kind=WorkstreamKind.LEAN,
            goal="Formalize the route after source work.",
            dependencies=["source-main"],
        ),
    )
    paths = comath_paths(project_dir)
    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    ledger.upsert_item(
        UncertaintyItem(
            item_id="source-gap",
            kind=UncertaintyKind.SOURCE_DEBT,
            title="Central theorem needs source certification",
            owner_workstream_id="source-main",
            source_debt_status=SourceDebtStatus.EXTERNAL_THEOREM_NEEDED,
            severity="critical",
        )
    )
    save_uncertainty_ledger(paths.uncertainty_ledger, ledger)

    selected = select_next_workstreams(project_dir, limit=3)

    assert [item.workstream_id for item in selected] == ["source-main", "proof-main"]


def test_run_comath_loop_executes_bounded_ready_workstreams_and_writes_report(tmp_path: Path) -> None:
    project_dir = tmp_path / "scheduler-loop"
    initialize_comath_project(project_dir, project_name="Loop", original_goal="Prove the loop theorem.")
    for workstream_id in ["proof-a", "proof-b"]:
        add_workstream(
            project_dir,
            WorkstreamRecord(
                workstream_id=workstream_id,
                kind=WorkstreamKind.PROOF,
                goal=f"Run {workstream_id}.",
            ),
        )

    def fake_executor(context):
        run_dir = context.paths.workstream_dir(context.workstream.workstream_id) / "runs" / "fake"
        artifact_path = run_dir / "artifact.txt"
        write_text(artifact_path, "local artifact\n")
        return {"status": "completed", "run_dir": str(run_dir), "artifact_path": str(artifact_path)}

    payload = run_comath_loop(
        project_dir,
        max_workstreams=1,
        time_budget_seconds=60,
        executor=fake_executor,
        run_name="scheduler-smoke",
    )
    state = json.loads((project_dir / "comath" / "project_state.json").read_text(encoding="utf-8"))
    by_id = {item["workstream_id"]: item for item in state["workstreams"]}

    assert payload["executed_count"] == 1
    assert payload["stop_reason"] == "max_workstreams_reached"
    assert payload["executed"][0]["workstream_id"] == "proof-a"
    assert by_id["proof-a"]["status"] == WorkstreamStatus.NEEDS_REVIEW.value
    assert by_id["proof-b"]["status"] == WorkstreamStatus.PLANNED.value
    assert (project_dir / "comath" / "loop_runs" / "scheduler-smoke" / "report.json").exists()
    assert "proof-a" in (project_dir / "comath" / "project_dashboard.md").read_text(encoding="utf-8")


def test_run_comath_loop_freezes_repeated_stalled_revision_workstream(tmp_path: Path) -> None:
    project_dir = tmp_path / "scheduler-freeze"
    initialize_comath_project(project_dir, project_name="Freeze", original_goal="Prove the freeze theorem.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="proof-stalled",
            kind=WorkstreamKind.PROOF,
            goal="Repeatedly stalled proof route.",
            status=WorkstreamStatus.REVISION,
            blockers=["[runner:proof_strategy] Missing bridge lemma."],
            metadata={
                "runner_runs": [
                    {
                        "status": "blocked",
                        "workstream_status": "revision",
                        "blockers": ["Missing bridge lemma."],
                    },
                    {
                        "status": "blocked",
                        "workstream_status": "revision",
                        "blockers": ["Missing bridge lemma."],
                    },
                ]
            },
        ),
    )

    payload = run_comath_loop(
        project_dir,
        max_workstreams=1,
        time_budget_seconds=60,
        executor=lambda context: {"status": "completed"},
        freeze_stalled_after=2,
        run_name="freeze-smoke",
    )
    paths = comath_paths(project_dir)
    status = json.loads((paths.workstream_dir("proof-stalled") / "status.json").read_text(encoding="utf-8"))
    freeze_payload = json.loads(
        (paths.workstream_dir("proof-stalled") / "freeze_package" / "freeze.json").read_text(encoding="utf-8")
    )
    ledger = json.loads(paths.uncertainty_ledger.read_text(encoding="utf-8"))

    assert payload["executed_count"] == 0
    assert payload["frozen_count"] == 1
    assert status["status"] == WorkstreamStatus.FROZEN.value
    assert freeze_payload["stalled_run_count"] == 2
    assert any(item["kind"] == "failed_route" for item in ledger["items"])
