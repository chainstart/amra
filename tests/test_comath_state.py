from pathlib import Path

from ara_math.artifact_graph import ArtifactGraph, DependencyEdge
from ara_math.uncertainty import SourceDebtStatus, UncertaintyLedger
from ara_math.workspace import write_json
from ara_math.workstreams import (
    ClaimRecord,
    ClaimStatus,
    DependencyStatus,
    ProjectState,
    WorkstreamKind,
    WorkstreamRecord,
    WorkstreamStatus,
)


def test_comath_dataclasses_round_trip_with_enum_values() -> None:
    state = ProjectState(
        project_id="toy",
        project_name="Toy",
        original_goal="Prove the toy statement.",
    )
    state.add_workstream(
        WorkstreamRecord(
            workstream_id="source-main",
            kind=WorkstreamKind.SOURCE,
            goal="Check the source theorem.",
            dependencies=["proof-main"],
        )
    )
    state.add_claim(
        ClaimRecord(
            claim_id="claim-main",
            title="Main claim",
            statement="The toy statement holds.",
            status=ClaimStatus.ROUTE_CANDIDATE,
        )
    )

    payload = state.to_dict()
    restored = ProjectState.from_dict(payload)

    assert payload["status"] == "goals_planned"
    assert restored.workstreams[0].kind == WorkstreamKind.SOURCE
    assert restored.workstreams[0].status == WorkstreamStatus.PLANNED
    assert restored.claims[0].status == ClaimStatus.ROUTE_CANDIDATE
    assert restored.open_workstreams()[0].workstream_id == "source-main"


def test_artifact_graph_records_dependencies_and_persists(tmp_path: Path) -> None:
    graph = ArtifactGraph(graph_id="toy-graph")
    graph.record_claim(claim_id="original-theorem", title="Original theorem")
    graph.record_claim(claim_id="source-lemma", title="Source lemma")
    graph.record_source(node_id="paper-theorem", label="Paper theorem", source_url="https://example.test/paper")
    graph.add_edge(
        DependencyEdge(
            source_id="original-theorem",
            target_id="source-lemma",
            status=DependencyStatus.BLOCKED,
        )
    )
    graph.add_edge(
        DependencyEdge(
            source_id="source-lemma",
            target_id="paper-theorem",
            status=DependencyStatus.PENDING,
        )
    )

    assert graph.dependency_path("original-theorem", "paper-theorem") == [
        "original-theorem",
        "source-lemma",
        "paper-theorem",
    ]
    assert len(graph.unresolved_dependencies_of("original-theorem")) == 1

    path = tmp_path / "artifact_graph.json"
    graph.save(path)
    restored = ArtifactGraph.load(path)

    assert restored.counts_by_kind()["claim"] == 2
    assert restored.has_dependency_path("original-theorem", "paper-theorem")


def test_uncertainty_ledger_tracks_source_debt_and_failed_route_suppression() -> None:
    ledger = UncertaintyLedger(ledger_id="toy-ledger")
    ledger.add_source_debt(
        item_id="source-gap",
        title="Dense central block theorem has no accepted source",
        source_debt_status=SourceDebtStatus.RESEARCH_GAP,
        owner_workstream_id="source-main",
        claim_id="original-theorem",
    )
    first_route = ledger.add_failed_route(
        route_id="route-1",
        summary="Use a parity split over dense blocks",
        failure_reason="Only proves an easier variant.",
        owner_workstream_id="proof-main",
    )
    duplicate = ledger.add_failed_route(
        route_id="route-2",
        summary="Use a parity split over dense blocks",
        failure_reason="Repeated route.",
        owner_workstream_id="proof-main",
    )

    assert len(ledger.blocking_items()) == 1
    assert first_route.route_id == duplicate.route_id
    assert ledger.should_suppress_route("Use a parity split over dense blocks")
    assert not ledger.should_suppress_route("Use a parity split over dense blocks", changed_note="New lemma added.")


def test_initialize_comath_project_creates_phase_one_files(tmp_path: Path) -> None:
    project_dir = tmp_path / "projects" / "toy"
    (project_dir / "idea").mkdir(parents=True)
    write_json(
        project_dir / "project_manifest.json",
        {
            "project_name": "Toy Project",
            "project_slug": "toy-project",
            "problem": {"statement": "Prove the toy statement."},
        },
    )

    from ara_math.coordinator import initialize_comath_project

    state = initialize_comath_project(project_dir)

    assert state.project_id == "toy-project"
    assert (project_dir / "comath" / "project_state.json").exists()
    assert (project_dir / "comath" / "artifact_graph.json").exists()
    assert (project_dir / "comath" / "uncertainty_ledger.json").exists()
    assert (project_dir / "comath" / "failed_routes.jsonl").exists()
    assert (project_dir / "comath" / "workstreams").is_dir()
