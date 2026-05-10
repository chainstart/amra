import json
import threading
import time
from pathlib import Path

from ara_math.coordinator import add_workstream, initialize_comath_project, run_comath_loop
from ara_math.workstreams import WorkstreamKind, WorkstreamRecord, WorkstreamStatus
from ara_math.workspace import write_text


def _recording_executor(events: list[tuple[str, str, float]], lock: threading.Lock, delay: float = 0.2):
    def executor(context):
        with lock:
            events.append(("start", context.workstream.workstream_id, time.monotonic()))
        time.sleep(delay)
        run_dir = context.paths.workstream_dir(context.workstream.workstream_id) / "runs" / "parallel-fake"
        artifact_path = run_dir / "artifact.txt"
        write_text(artifact_path, context.workstream.workstream_id + "\n")
        with lock:
            events.append(("end", context.workstream.workstream_id, time.monotonic()))
        return {"status": "completed", "run_dir": str(run_dir), "artifact_path": str(artifact_path)}

    return executor


def _times(events: list[tuple[str, str, float]], kind: str) -> dict[str, float]:
    return {workstream_id: at for event_kind, workstream_id, at in events if event_kind == kind}


def test_parallel_loop_overlaps_independent_workstreams(tmp_path: Path) -> None:
    project_dir = tmp_path / "parallel-independent"
    initialize_comath_project(project_dir, project_name="Parallel", original_goal="Run independent workstreams.")
    for workstream_id in ["proof-a", "proof-b"]:
        add_workstream(
            project_dir,
            WorkstreamRecord(
                workstream_id=workstream_id,
                kind=WorkstreamKind.PROOF,
                goal=f"Run {workstream_id}.",
            ),
        )
    events: list[tuple[str, str, float]] = []
    lock = threading.Lock()

    payload = run_comath_loop(
        project_dir,
        max_workstreams=2,
        max_parallel_workstreams=2,
        time_budget_seconds=60,
        executor=_recording_executor(events, lock),
        run_name="parallel-smoke",
    )
    starts = _times(events, "start")
    ends = _times(events, "end")

    assert payload["executed_count"] == 2
    assert payload["parallelism"]["max_parallel_workstreams"] == 2
    assert set(starts) == {"proof-a", "proof-b"}
    assert max(starts.values()) < min(ends.values())
    assert {item["decision"] for item in payload["resource_decisions"] if item["workstream_id"] in starts} == {"selected"}


def test_parallel_loop_serializes_same_lean_write_target(tmp_path: Path) -> None:
    project_dir = tmp_path / "parallel-lean-target"
    initialize_comath_project(project_dir, project_name="Lean Parallel", original_goal="Serialize Lean writes.")
    for workstream_id in ["lean-a", "lean-b"]:
        add_workstream(
            project_dir,
            WorkstreamRecord(
                workstream_id=workstream_id,
                kind=WorkstreamKind.LEAN,
                goal=f"Run {workstream_id}.",
                metadata={"workspace": str(project_dir / "formal"), "target_file": "MathProject/Main.lean"},
            ),
        )
    events: list[tuple[str, str, float]] = []
    lock = threading.Lock()

    payload = run_comath_loop(
        project_dir,
        max_workstreams=2,
        max_parallel_workstreams=2,
        max_concurrent_lean_builds=2,
        time_budget_seconds=60,
        executor=_recording_executor(events, lock, delay=0.12),
        run_name="lean-serialize-smoke",
    )
    starts = _times(events, "start")
    ends = _times(events, "end")
    state = json.loads((project_dir / "comath" / "project_state.json").read_text(encoding="utf-8"))

    assert payload["executed_count"] == 2
    assert any(item["decision"] == "queued_same_write_target" for item in payload["resource_decisions"])
    assert starts["lean-b"] >= ends["lean-a"]
    assert {item["status"] for item in state["workstreams"]} == {WorkstreamStatus.NEEDS_REVIEW.value}


def test_parallel_loop_reports_llm_and_lean_resource_slots(tmp_path: Path) -> None:
    project_dir = tmp_path / "parallel-resource-report"
    initialize_comath_project(project_dir, project_name="Resources", original_goal="Report resources.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="lean-main",
            kind=WorkstreamKind.LEAN,
            goal="Run one Lean workstream.",
            metadata={"workspace": str(project_dir / "formal"), "target_file": "MathProject/Main.lean"},
        ),
    )

    payload = run_comath_loop(
        project_dir,
        max_workstreams=1,
        max_parallel_workstreams=2,
        max_concurrent_llm_calls=1,
        max_concurrent_lean_builds=1,
        executor_options={"backend": "codex"},
        executor=lambda context: {"status": "completed"},
        run_name="resource-report-smoke",
    )
    result = payload["executed"][0]

    assert result["resource_slots"] == {
        "llm": True,
        "lean": True,
        "write_key": str(project_dir / "formal" / "MathProject/Main.lean"),
    }
    assert payload["parallelism"] == {
        "max_parallel_workstreams": 2,
        "max_concurrent_llm_calls": 1,
        "max_concurrent_lean_builds": 1,
    }
