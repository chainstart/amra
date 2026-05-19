from __future__ import annotations

import json
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from amra.orchestration.workstreams import ClaimStatus, DependencyStatus, utc_now_iso


class _StringEnum(str, Enum):
    @classmethod
    def coerce(cls, value: Any) -> Any:
        if isinstance(value, cls):
            return value
        normalized = str(value).strip().lower()
        for item in cls:
            if normalized in {item.value, item.name.lower()}:
                return item
        raise ValueError(f"Invalid {cls.__name__}: {value}")


class ArtifactKind(_StringEnum):
    CLAIM = "claim"
    FILE = "file"
    SOURCE = "source"
    LEAN_DECLARATION = "lean_declaration"
    COMPUTATION_CERTIFICATE = "computation_certificate"


class DependencyRelation(_StringEnum):
    DEPENDS_ON = "depends_on"
    SUPPORTS = "supports"
    PRODUCES = "produces"
    CITES = "cites"
    FORMALIZES = "formalizes"
    CERTIFIES = "certifies"
    BLOCKS = "blocks"


def _string_list(values: list[Any] | None) -> list[str]:
    return [str(value) for value in values or []]


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


@dataclass(slots=True)
class ArtifactNode:
    node_id: str
    kind: ArtifactKind
    label: str
    path: str = ""
    workstream_id: str = ""
    claim_id: str = ""
    claim_status: ClaimStatus | None = None
    source_url: str = ""
    lean_name: str = ""
    certificate_hash: str = ""
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.kind = ArtifactKind.coerce(self.kind)
        if self.claim_status:
            self.claim_status = ClaimStatus.coerce(self.claim_status)
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ArtifactNode":
        raw_claim_status = payload.get("claim_status")
        return cls(
            node_id=str(payload["node_id"]),
            kind=ArtifactKind.coerce(payload.get("kind", ArtifactKind.FILE)),
            label=str(payload.get("label", "")),
            path=str(payload.get("path", "")),
            workstream_id=str(payload.get("workstream_id", "")),
            claim_id=str(payload.get("claim_id", "")),
            claim_status=ClaimStatus.coerce(raw_claim_status) if raw_claim_status else None,
            source_url=str(payload.get("source_url", "")),
            lean_name=str(payload.get("lean_name", "")),
            certificate_hash=str(payload.get("certificate_hash", "")),
            created_at=str(payload.get("created_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "kind": self.kind.value,
            "label": self.label,
            "path": self.path,
            "workstream_id": self.workstream_id,
            "claim_id": self.claim_id,
            "claim_status": self.claim_status.value if self.claim_status else "",
            "source_url": self.source_url,
            "lean_name": self.lean_name,
            "certificate_hash": self.certificate_hash,
            "created_at": self.created_at,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class DependencyEdge:
    source_id: str
    target_id: str
    relation: DependencyRelation = DependencyRelation.DEPENDS_ON
    status: DependencyStatus = DependencyStatus.PENDING
    rationale: str = ""
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.relation = DependencyRelation.coerce(self.relation)
        self.status = DependencyStatus.coerce(self.status)
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DependencyEdge":
        return cls(
            source_id=str(payload["source_id"]),
            target_id=str(payload["target_id"]),
            relation=DependencyRelation.coerce(payload.get("relation", DependencyRelation.DEPENDS_ON)),
            status=DependencyStatus.coerce(payload.get("status", DependencyStatus.PENDING)),
            rationale=str(payload.get("rationale", "")),
            created_at=str(payload.get("created_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation": self.relation.value,
            "status": self.status.value,
            "rationale": self.rationale,
            "created_at": self.created_at,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ArtifactGraph:
    graph_id: str
    nodes: list[ArtifactNode] = field(default_factory=list)
    edges: list[DependencyEdge] = field(default_factory=list)
    generated_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.nodes = [ArtifactNode.from_dict(item) if isinstance(item, dict) else item for item in self.nodes]
        self.edges = [DependencyEdge.from_dict(item) if isinstance(item, dict) else item for item in self.edges]
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any] | None) -> "ArtifactGraph":
        payload = payload or {}
        return cls(
            graph_id=str(payload.get("graph_id", "artifact-graph")),
            nodes=[ArtifactNode.from_dict(item) for item in payload.get("nodes", [])],
            edges=[DependencyEdge.from_dict(item) for item in payload.get("edges", [])],
            generated_at=str(payload.get("generated_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    @classmethod
    def load(cls, path: Path) -> "ArtifactGraph":
        if not path.exists():
            return cls(graph_id="artifact-graph")
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "generated_at": self.generated_at,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "metadata": dict(self.metadata),
        }

    def get_node(self, node_id: str) -> ArtifactNode | None:
        return next((node for node in self.nodes if node.node_id == node_id), None)

    def nodes_for_workstream(self, workstream_id: str) -> list[ArtifactNode]:
        return [node for node in self.nodes if node.workstream_id == workstream_id]

    def node_ids_for_workstream(self, workstream_id: str) -> list[str]:
        return [node.node_id for node in self.nodes_for_workstream(workstream_id)]

    def add_node(self, node: ArtifactNode | dict[str, Any]) -> ArtifactNode:
        if isinstance(node, dict):
            node = ArtifactNode.from_dict(node)
        existing = self.get_node(node.node_id)
        if existing:
            return existing
        self.nodes.append(node)
        self.generated_at = utc_now_iso()
        return node

    def upsert_node(self, node: ArtifactNode | dict[str, Any]) -> ArtifactNode:
        if isinstance(node, dict):
            node = ArtifactNode.from_dict(node)
        for index, existing in enumerate(self.nodes):
            if existing.node_id == node.node_id:
                if not node.created_at:
                    node.created_at = existing.created_at
                self.nodes[index] = node
                self.generated_at = utc_now_iso()
                return node
        return self.add_node(node)

    def add_edge(
        self,
        edge: DependencyEdge | dict[str, Any] | None = None,
        *,
        source_id: str = "",
        target_id: str = "",
        relation: DependencyRelation | str = DependencyRelation.DEPENDS_ON,
        status: DependencyStatus | str = DependencyStatus.PENDING,
        rationale: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> DependencyEdge:
        if edge is None:
            edge = DependencyEdge(
                source_id=source_id,
                target_id=target_id,
                relation=relation,
                status=status,
                rationale=rationale,
                metadata=metadata or {},
            )
        elif isinstance(edge, dict):
            edge = DependencyEdge.from_dict(edge)
        for existing in self.edges:
            if (
                existing.source_id == edge.source_id
                and existing.target_id == edge.target_id
                and existing.relation == edge.relation
            ):
                return existing
        self.edges.append(edge)
        self.generated_at = utc_now_iso()
        return edge

    def set_dependency_status(
        self,
        source_id: str,
        target_id: str,
        status: DependencyStatus | str,
        *,
        relation: DependencyRelation | str = DependencyRelation.DEPENDS_ON,
    ) -> DependencyEdge:
        relation_value = DependencyRelation.coerce(relation)
        for edge in self.edges:
            if edge.source_id == source_id and edge.target_id == target_id and edge.relation == relation_value:
                edge.status = DependencyStatus.coerce(status)
                self.generated_at = utc_now_iso()
                return edge
        return self.add_edge(
            DependencyEdge(
                source_id=source_id,
                target_id=target_id,
                relation=relation_value,
                status=DependencyStatus.coerce(status),
            )
        )

    def record_claim(
        self,
        *,
        claim_id: str,
        title: str,
        statement: str = "",
        status: ClaimStatus | str = ClaimStatus.HYPOTHESIS,
        workstream_id: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> ArtifactNode:
        return self.upsert_node(
            ArtifactNode(
                node_id=claim_id,
                kind=ArtifactKind.CLAIM,
                label=title,
                workstream_id=workstream_id,
                claim_id=claim_id,
                claim_status=ClaimStatus.coerce(status),
                metadata={**(metadata or {}), "statement": statement},
            )
        )

    def record_file(
        self,
        *,
        node_id: str,
        path: str,
        label: str = "",
        workstream_id: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> ArtifactNode:
        return self.upsert_node(
            ArtifactNode(
                node_id=node_id,
                kind=ArtifactKind.FILE,
                label=label or path,
                path=path,
                workstream_id=workstream_id,
                metadata=metadata or {},
            )
        )

    def record_source(
        self,
        *,
        node_id: str,
        label: str,
        source_url: str = "",
        path: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> ArtifactNode:
        return self.upsert_node(
            ArtifactNode(
                node_id=node_id,
                kind=ArtifactKind.SOURCE,
                label=label,
                source_url=source_url,
                path=path,
                metadata=metadata or {},
            )
        )

    def record_lean_declaration(
        self,
        *,
        node_id: str,
        lean_name: str,
        path: str = "",
        claim_id: str = "",
        workstream_id: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> ArtifactNode:
        return self.upsert_node(
            ArtifactNode(
                node_id=node_id,
                kind=ArtifactKind.LEAN_DECLARATION,
                label=lean_name,
                path=path,
                workstream_id=workstream_id,
                claim_id=claim_id,
                lean_name=lean_name,
                metadata=metadata or {},
            )
        )

    def record_computation_certificate(
        self,
        *,
        node_id: str,
        label: str,
        path: str = "",
        certificate_hash: str = "",
        workstream_id: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> ArtifactNode:
        return self.upsert_node(
            ArtifactNode(
                node_id=node_id,
                kind=ArtifactKind.COMPUTATION_CERTIFICATE,
                label=label,
                path=path,
                workstream_id=workstream_id,
                certificate_hash=certificate_hash,
                metadata=metadata or {},
            )
        )

    def dependencies_of(self, node_id: str) -> list[DependencyEdge]:
        return [
            edge
            for edge in self.edges
            if edge.source_id == node_id and edge.relation in {DependencyRelation.DEPENDS_ON, DependencyRelation.CITES}
        ]

    def dependents_of(self, node_id: str) -> list[DependencyEdge]:
        return [
            edge
            for edge in self.edges
            if edge.target_id == node_id and edge.relation in {DependencyRelation.DEPENDS_ON, DependencyRelation.CITES}
        ]

    def unresolved_dependencies_of(self, node_id: str) -> list[DependencyEdge]:
        resolved = {DependencyStatus.SATISFIED, DependencyStatus.RESOLVED}
        return [edge for edge in self.dependencies_of(node_id) if edge.status not in resolved]

    def dependency_path(self, source_id: str, target_id: str) -> list[str]:
        if source_id == target_id:
            return [source_id]
        queue: deque[tuple[str, list[str]]] = deque([(source_id, [source_id])])
        seen = {source_id}
        adjacency: dict[str, list[str]] = {}
        for edge in self.edges:
            if edge.relation in {DependencyRelation.DEPENDS_ON, DependencyRelation.CITES, DependencyRelation.FORMALIZES}:
                adjacency.setdefault(edge.source_id, []).append(edge.target_id)

        while queue:
            current, path = queue.popleft()
            for next_id in adjacency.get(current, []):
                if next_id in seen:
                    continue
                next_path = [*path, next_id]
                if next_id == target_id:
                    return next_path
                seen.add(next_id)
                queue.append((next_id, next_path))
        return []

    def has_dependency_path(self, source_id: str, target_id: str) -> bool:
        return bool(self.dependency_path(source_id, target_id))

    def counts_by_kind(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for node in self.nodes:
            counts[node.kind.value] = counts.get(node.kind.value, 0) + 1
        return counts

    def unresolved_edges(self) -> list[DependencyEdge]:
        return [edge for edge in self.edges if edge.status not in {DependencyStatus.SATISFIED, DependencyStatus.RESOLVED}]


def load_artifact_graph(path: Path) -> ArtifactGraph:
    return ArtifactGraph.load(path)


def save_artifact_graph(path: Path, graph: ArtifactGraph) -> None:
    graph.save(path)
