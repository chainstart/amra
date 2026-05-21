from __future__ import annotations

from pathlib import Path

from amra.core.artifact_graph import ArtifactGraph, ArtifactKind, DependencyRelation
from amra.orchestration.workstreams import DependencyStatus
from amra.research import ConjectureRecord, EvidenceKind, EvidenceRecord, record_research_evidence, record_research_object


def test_research_artifact_kinds_and_relations_round_trip(tmp_path: Path) -> None:
    graph = ArtifactGraph(graph_id="research-graph")
    conjecture = ConjectureRecord(
        object_id="conjecture-001",
        title="Candidate invariant",
        statement="All tested examples satisfy the invariant.",
    )

    node = record_research_object(graph, conjecture, workstream_id="discovery-main")
    graph.record_research_object(
        node_id="experiment-001",
        kind=ArtifactKind.EXPERIMENT,
        label="Bounded search",
        workstream_id="experiment-main",
        metadata={"limit": 1000},
    )
    graph.add_edge(
        source_id="experiment-001",
        target_id="conjecture-001",
        relation=DependencyRelation.EMPIRICALLY_SUPPORTS,
        status=DependencyStatus.SATISFIED,
        rationale="No counterexample found for n <= 1000.",
    )

    path = tmp_path / "graph.json"
    graph.save(path)
    restored = ArtifactGraph.load(path)

    assert node.kind == ArtifactKind.CONJECTURE
    assert restored.counts_by_kind() == {"conjecture": 1, "experiment": 1}
    assert restored.has_dependency_path("experiment-001", "conjecture-001") is True
    assert restored.edges[0].relation == DependencyRelation.EMPIRICALLY_SUPPORTS
    assert restored.edges[0].status == DependencyStatus.SATISFIED


def test_research_evidence_maps_to_non_proof_graph_relations() -> None:
    graph = ArtifactGraph(graph_id="evidence-graph")
    record_research_object(graph, ConjectureRecord(object_id="conjecture-001", title="Candidate"))

    record_research_evidence(
        graph,
        EvidenceRecord(
            evidence_id="counterexample-001",
            kind=EvidenceKind.COUNTEREXAMPLE_EVIDENCE,
            target_object_id="conjecture-001",
            summary="n = 12 violates the candidate statement.",
            status="reviewed",
        ),
    )

    assert graph.get_node("counterexample-001") is not None
    assert graph.edges[0].relation == DependencyRelation.REFUTES
    assert graph.edges[0].status == DependencyStatus.SATISFIED
