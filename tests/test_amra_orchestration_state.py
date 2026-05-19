import importlib
import json
from pathlib import Path

from amra.core.artifact_graph import DependencyRelation, load_artifact_graph, save_artifact_graph
from amra.orchestration.coordinator import (
    add_workstream,
    comath_paths,
    initialize_comath_project,
    review_workstream_gate,
    run_comath_loop,
    select_next_workstreams,
)
from amra.orchestration.uncertainty import (
    SourceDebtStatus,
    UncertaintyItem,
    UncertaintyKind,
    load_uncertainty_ledger,
    save_uncertainty_ledger,
)
from amra.orchestration.workstreams import DependencyStatus, WorkstreamKind, WorkstreamRecord, WorkstreamStatus
from amra.review.gates import evaluate_workstream_review_gate
from amra.scheduler.executors import WorkstreamExecutionContext


def test_canonical_orchestration_creates_dashboard_graph_and_ledger(tmp_path: Path) -> None:
    project_dir = tmp_path / "canonical-project"

    state = initialize_comath_project(
        project_dir,
        project_name="Canonical Project",
        original_goal="Prove the canonical theorem.",
    )
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="source-main",
            kind=WorkstreamKind.SOURCE,
            goal="Source-check the theorem.",
            claim_ids=["source-claim"],
        ),
    )

    paths = comath_paths(project_dir)
    graph = load_artifact_graph(paths.artifact_graph)
    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)

    assert state.project_id == "canonical-project"
    assert (project_dir / "comath" / "project_dashboard.md").exists()
    assert graph.get_node("original-theorem") is not None
    assert ledger.ledger_id == "canonical-project-uncertainty-ledger"
    assert select_next_workstreams(project_dir)[0].workstream_id == "source-main"


def test_canonical_review_gate_and_scheduler_are_local_and_legacy_compatible(tmp_path: Path) -> None:
    project_dir = tmp_path / "canonical-loop"
    initialize_comath_project(project_dir, project_name="Loop", original_goal="Prove the loop theorem.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="proof-main",
            kind=WorkstreamKind.PROOF,
            goal="Close the loop theorem.",
            claim_ids=["main-claim"],
        ),
    )
    paths = comath_paths(project_dir)
    graph = load_artifact_graph(paths.artifact_graph)
    graph.record_claim(claim_id="main-claim", title="Main claim", workstream_id="proof-main")
    graph.add_edge(
        source_id="main-claim",
        target_id="original-theorem",
        relation=DependencyRelation.DEPENDS_ON,
        status=DependencyStatus.SATISFIED,
    )
    save_artifact_graph(paths.artifact_graph, graph)

    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    ledger.upsert_item(
        UncertaintyItem(
            item_id="source-gap",
            kind=UncertaintyKind.SOURCE_DEBT,
            title="Source evidence still pending",
            owner_workstream_id="proof-main",
            source_debt_status=SourceDebtStatus.EXTERNAL_THEOREM_NEEDED,
        )
    )
    save_uncertainty_ledger(paths.uncertainty_ledger, ledger)

    report = evaluate_workstream_review_gate(
        state=importlib.import_module("amra.orchestration.coordinator").load_project_state(project_dir),
        workstream=importlib.import_module("amra.orchestration.coordinator").load_project_state(project_dir).get_workstream("proof-main"),
        graph=graph,
        ledger=ledger,
        project_dir=project_dir,
    )
    assert report.approved is False
    assert {blocker.code for blocker in report.blockers} == {"source_debt"}

    def fake_executor(context: WorkstreamExecutionContext) -> dict[str, str]:
        assert context.workstream.workstream_id == "proof-main"
        return {"status": "completed"}

    payload = run_comath_loop(project_dir, max_workstreams=1, executor=fake_executor, run_name="canonical-smoke")
    gate_payload = review_workstream_gate(project_dir, "proof-main")
    persisted = json.loads((paths.workstream_dir("proof-main") / "status.json").read_text(encoding="utf-8"))

    assert payload["executed_count"] == 1
    assert gate_payload["approved"] is False
    assert persisted["status"] == WorkstreamStatus.REVISION.value
    assert importlib.import_module("ara_math.coordinator") is importlib.import_module("amra.orchestration.coordinator")
    assert importlib.import_module("ara_math.review_gate") is importlib.import_module("amra.review.gates")
    assert importlib.import_module("ara_math.comath_runners") is importlib.import_module("amra.scheduler.executors")
