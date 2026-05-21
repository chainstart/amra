from __future__ import annotations

from amra.core.artifact_graph import ArtifactGraph, ArtifactKind, ArtifactNode, DependencyRelation
from amra.research.evidence import EvidenceKind, EvidenceRecord
from amra.research.objects import ResearchObjectRecord, ResearchObjectType


OBJECT_TYPE_ARTIFACT_KIND = {
    ResearchObjectType.CONJECTURE: ArtifactKind.CONJECTURE,
    ResearchObjectType.HYPOTHESIS: ArtifactKind.HYPOTHESIS,
    ResearchObjectType.EXPERIMENT: ArtifactKind.EXPERIMENT,
    ResearchObjectType.DATASET: ArtifactKind.DATASET,
    ResearchObjectType.ALGORITHM: ArtifactKind.ALGORITHM,
    ResearchObjectType.MODEL: ArtifactKind.MODEL,
    ResearchObjectType.BENCHMARK: ArtifactKind.BENCHMARK,
    ResearchObjectType.COUNTEREXAMPLE: ArtifactKind.COUNTEREXAMPLE,
    ResearchObjectType.CONSTRUCTION: ArtifactKind.CONSTRUCTION,
    ResearchObjectType.SECURITY_GAME: ArtifactKind.SECURITY_GAME,
    ResearchObjectType.SECURITY_ASSUMPTION: ArtifactKind.SECURITY_ASSUMPTION,
    ResearchObjectType.ML_THEORY_CLAIM: ArtifactKind.CLAIM,
    ResearchObjectType.NEGATIVE_RESULT: ArtifactKind.NEGATIVE_RESULT,
    ResearchObjectType.THEORY_NODE: ArtifactKind.THEORY_NODE,
}

EVIDENCE_RELATION = {
    EvidenceKind.PROOF_EVIDENCE: DependencyRelation.SUPPORTS,
    EvidenceKind.LEAN_VERIFIED: DependencyRelation.CERTIFIES,
    EvidenceKind.COMPUTATION_CERTIFICATE: DependencyRelation.CERTIFIES,
    EvidenceKind.EMPIRICAL_EVIDENCE: DependencyRelation.EMPIRICALLY_SUPPORTS,
    EvidenceKind.STATISTICAL_EVIDENCE: DependencyRelation.STATISTICALLY_SUPPORTS,
    EvidenceKind.BENCHMARK_EVIDENCE: DependencyRelation.BENCHMARKS,
    EvidenceKind.COUNTEREXAMPLE_EVIDENCE: DependencyRelation.REFUTES,
    EvidenceKind.SOURCE_EVIDENCE: DependencyRelation.CITES,
    EvidenceKind.SECURITY_EVIDENCE: DependencyRelation.SUPPORTS,
    EvidenceKind.NEGATIVE_EVIDENCE: DependencyRelation.INVALIDATES,
}


def artifact_kind_for_object_type(object_type: ResearchObjectType | str) -> ArtifactKind:
    return OBJECT_TYPE_ARTIFACT_KIND[ResearchObjectType.coerce(object_type)]


def relation_for_evidence_kind(evidence_kind: EvidenceKind | str) -> DependencyRelation:
    return EVIDENCE_RELATION[EvidenceKind.coerce(evidence_kind)]


def record_research_object(
    graph: ArtifactGraph,
    record: ResearchObjectRecord,
    *,
    workstream_id: str = "",
    path: str = "",
) -> ArtifactNode:
    return graph.record_research_object(
        node_id=record.object_id,
        kind=artifact_kind_for_object_type(record.object_type),
        label=record.title,
        workstream_id=workstream_id,
        path=path,
        metadata=record.to_dict(),
    )


def record_research_evidence(
    graph: ArtifactGraph,
    evidence: EvidenceRecord,
    *,
    artifact_node_id: str | None = None,
) -> None:
    source_id = artifact_node_id or evidence.evidence_id
    if artifact_node_id is None:
        graph.record_research_object(
            node_id=evidence.evidence_id,
            kind=ArtifactKind.FILE,
            label=evidence.summary or evidence.evidence_id,
            metadata=evidence.to_dict(),
        )
    graph.add_edge(
        source_id=source_id,
        target_id=evidence.target_object_id,
        relation=relation_for_evidence_kind(evidence.kind),
        status="satisfied" if evidence.status in {"reviewed", "accepted", "reproducible"} else "pending",
        rationale=evidence.summary,
        metadata=evidence.to_dict(),
    )
