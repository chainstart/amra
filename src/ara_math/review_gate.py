from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from ara_math.artifact_graph import ArtifactGraph, ArtifactKind
from ara_math.lean_audit import audit_lean_source_file
from ara_math.uncertainty import (
    SourceDebtStatus,
    UncertaintyItem,
    UncertaintyKind,
    UncertaintyLedger,
    UncertaintyStatus,
)
from ara_math.workstreams import (
    ProjectState,
    ReviewDecision,
    ReviewKind,
    ReviewRecord,
    WorkstreamRecord,
    WorkstreamStatus,
    utc_now_iso,
)


DEFAULT_REVIEW_KINDS: tuple[ReviewKind, ...] = (
    ReviewKind.LOGIC,
    ReviewKind.SOURCE,
    ReviewKind.LEAN,
    ReviewKind.COMPUTATION,
    ReviewKind.GLOBAL,
)

_REVIEW_KIND_ALIASES = {
    "compute": ReviewKind.COMPUTATION.value,
    "repro": ReviewKind.COMPUTATION.value,
    "reproducibility": ReviewKind.COMPUTATION.value,
    "strategy": ReviewKind.GLOBAL.value,
    "global_strategy": ReviewKind.GLOBAL.value,
}

_OPEN_UNCERTAINTY_STATUSES = {UncertaintyStatus.OPEN, UncertaintyStatus.IN_PROGRESS}
_BLOCKING_SOURCE_STATUSES = {
    SourceDebtStatus.SOURCE_FORMALIZATION_NEEDED,
    SourceDebtStatus.EXTERNAL_THEOREM_NEEDED,
    SourceDebtStatus.RESEARCH_GAP,
}
_LEAN_BLOCKING_COUNTS = ("sorry", "admit", "axiom", "placeholder")


@dataclass(slots=True)
class ReviewGateBlocker:
    blocker_id: str
    kind: ReviewKind
    code: str
    message: str
    severity: str = "high"
    source_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.kind = normalize_review_kind(self.kind)
        self.metadata = dict(self.metadata)

    def to_dict(self) -> dict[str, Any]:
        return {
            "blocker_id": self.blocker_id,
            "kind": self.kind.value,
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "source_id": self.source_id,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ReviewGateKindDecision:
    kind: ReviewKind
    decision: ReviewDecision
    blocker_ids: list[str] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self) -> None:
        self.kind = normalize_review_kind(self.kind)
        self.decision = ReviewDecision.coerce(self.decision)
        self.blocker_ids = [str(item) for item in self.blocker_ids]

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "decision": self.decision.value,
            "blocker_ids": list(self.blocker_ids),
            "notes": self.notes,
        }


@dataclass(slots=True)
class ReviewGateReport:
    workstream_id: str
    approved: bool
    decision: ReviewDecision
    workstream_status: WorkstreamStatus
    review_decisions: list[ReviewGateKindDecision]
    blockers: list[ReviewGateBlocker] = field(default_factory=list)
    dependency_path: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.decision = ReviewDecision.coerce(self.decision)
        self.workstream_status = WorkstreamStatus.coerce(self.workstream_status)
        self.review_decisions = [
            item if isinstance(item, ReviewGateKindDecision) else ReviewGateKindDecision(**item)
            for item in self.review_decisions
        ]
        self.blockers = [
            item if isinstance(item, ReviewGateBlocker) else ReviewGateBlocker(**item)
            for item in self.blockers
        ]
        self.dependency_path = [str(item) for item in self.dependency_path]
        self.metadata = dict(self.metadata)

    def to_dict(self) -> dict[str, Any]:
        return {
            "workstream_id": self.workstream_id,
            "approved": self.approved,
            "decision": self.decision.value,
            "workstream_status": self.workstream_status.value,
            "review_decisions": [item.to_dict() for item in self.review_decisions],
            "blockers": [item.to_dict() for item in self.blockers],
            "dependency_path": list(self.dependency_path),
            "generated_at": self.generated_at,
            "metadata": dict(self.metadata),
        }


def normalize_review_kind(kind: ReviewKind | str) -> ReviewKind:
    if isinstance(kind, ReviewKind):
        raw = kind.value
    else:
        raw = str(kind).strip().lower().replace("-", "_")
    return ReviewKind.coerce(_REVIEW_KIND_ALIASES.get(raw, raw))


def normalize_review_kinds(kinds: Iterable[ReviewKind | str] | None) -> list[ReviewKind]:
    seen: set[str] = set()
    normalized: list[ReviewKind] = []
    for kind in kinds or DEFAULT_REVIEW_KINDS:
        review_kind = normalize_review_kind(kind)
        if review_kind.value in seen:
            continue
        normalized.append(review_kind)
        seen.add(review_kind.value)
    return normalized


def evaluate_workstream_review_gate(
    *,
    state: ProjectState,
    workstream: WorkstreamRecord,
    graph: ArtifactGraph,
    ledger: UncertaintyLedger,
    project_dir: Path | None = None,
    original_node_id: str = "original-theorem",
    required_review_kinds: Iterable[ReviewKind | str] | None = None,
    require_existing_reviews: bool = False,
) -> ReviewGateReport:
    """Evaluate whether a workstream can leave the review gate.

    The evaluator is intentionally local: it only inspects persisted CoMath
    state, artifact graph edges, uncertainty ledger entries, and recorded files.
    """

    required_kinds = normalize_review_kinds(required_review_kinds)
    associated = _associated_ids(state, workstream, graph)
    blockers: list[ReviewGateBlocker] = []

    blockers.extend(_uncertainty_blockers(workstream, ledger, associated))
    blockers.extend(_statement_metadata_blockers(state, workstream, graph, associated))
    blockers.extend(_lean_blockers(workstream, graph, associated, project_dir))
    blockers.extend(_computation_blockers(workstream, graph, associated))

    dependency_path = _dependency_path_to_original(graph, associated["node_ids"], original_node_id)
    if not dependency_path:
        blockers.append(
            _blocker(
                workstream.workstream_id,
                ReviewKind.LOGIC,
                "missing_original_dependency_path",
                f"No dependency path connects workstream `{workstream.workstream_id}` to `{original_node_id}`.",
                source_id=original_node_id,
                metadata={"candidate_node_ids": sorted(associated["node_ids"])},
            )
        )

    blockers.extend(
        _review_decision_blockers(
            workstream,
            state.reviews,
            required_kinds,
            require_existing_reviews=require_existing_reviews,
        )
    )

    decisions = _kind_decisions(required_kinds, blockers)
    approved = all(item.decision == ReviewDecision.APPROVED for item in decisions)
    return ReviewGateReport(
        workstream_id=workstream.workstream_id,
        approved=approved,
        decision=ReviewDecision.APPROVED if approved else ReviewDecision.NEEDS_REVISION,
        workstream_status=WorkstreamStatus.APPROVED if approved else WorkstreamStatus.REVISION,
        review_decisions=decisions,
        blockers=blockers,
        dependency_path=dependency_path,
        metadata={
            "required_review_kinds": [kind.value for kind in required_kinds],
            "associated_claim_ids": sorted(associated["claim_ids"]),
            "associated_artifact_ids": sorted(associated["artifact_ids"]),
            "associated_node_ids": sorted(associated["node_ids"]),
        },
    )


def _associated_ids(
    state: ProjectState,
    workstream: WorkstreamRecord,
    graph: ArtifactGraph,
) -> dict[str, set[str]]:
    claim_ids = set(workstream.claim_ids)
    artifact_ids = set(workstream.artifact_ids)
    node_ids = set(workstream.claim_ids) | set(workstream.artifact_ids)

    for claim in state.claims:
        if claim.owner_workstream_id == workstream.workstream_id:
            claim_ids.add(claim.claim_id)
            node_ids.add(claim.claim_id)

    for node in graph.nodes:
        if node.workstream_id == workstream.workstream_id:
            node_ids.add(node.node_id)
            artifact_ids.add(node.node_id)
            if node.claim_id:
                claim_ids.add(node.claim_id)
        elif node.claim_id and node.claim_id in claim_ids:
            node_ids.add(node.node_id)
            artifact_ids.add(node.node_id)

    for artifact_id in list(artifact_ids):
        node = graph.get_node(artifact_id)
        if node and node.claim_id:
            claim_ids.add(node.claim_id)

    return {"claim_ids": claim_ids, "artifact_ids": artifact_ids, "node_ids": node_ids}


def _uncertainty_blockers(
    workstream: WorkstreamRecord,
    ledger: UncertaintyLedger,
    associated: dict[str, set[str]],
) -> list[ReviewGateBlocker]:
    blockers: list[ReviewGateBlocker] = []
    for item in ledger.items:
        if not _open_uncertainty_item(item) or not _item_applies_to_workstream(item, workstream, associated):
            continue
        if item.kind == UncertaintyKind.SOURCE_DEBT and _source_debt_blocks(item):
            blockers.append(
                _blocker(
                    workstream.workstream_id,
                    ReviewKind.SOURCE,
                    "source_debt",
                    f"Open source debt `{item.item_id}` blocks approval: {item.title}",
                    source_id=item.item_id,
                    severity=item.severity,
                    metadata=item.to_dict(),
                )
            )
        elif item.kind == UncertaintyKind.THEOREM_DEBT:
            blockers.append(
                _blocker(
                    workstream.workstream_id,
                    ReviewKind.LOGIC,
                    "theorem_debt",
                    f"Open theorem debt `{item.item_id}` blocks approval: {item.title}",
                    source_id=item.item_id,
                    severity=item.severity,
                    metadata=item.to_dict(),
                )
            )
        elif item.kind == UncertaintyKind.STATEMENT_DRIFT:
            blockers.append(
                _blocker(
                    workstream.workstream_id,
                    ReviewKind.LOGIC,
                    "statement_drift",
                    f"Open statement drift `{item.item_id}` blocks approval: {item.title}",
                    source_id=item.item_id,
                    severity=item.severity,
                    metadata=item.to_dict(),
                )
            )
        elif item.kind == UncertaintyKind.COMPUTATION_DEBT:
            blockers.append(
                _blocker(
                    workstream.workstream_id,
                    ReviewKind.COMPUTATION,
                    "computation_debt",
                    f"Open computation debt `{item.item_id}` blocks approval: {item.title}",
                    source_id=item.item_id,
                    severity=item.severity,
                    metadata=item.to_dict(),
                )
            )
    return blockers


def _statement_metadata_blockers(
    state: ProjectState,
    workstream: WorkstreamRecord,
    graph: ArtifactGraph,
    associated: dict[str, set[str]],
) -> list[ReviewGateBlocker]:
    blockers: list[ReviewGateBlocker] = []
    if _metadata_has_statement_drift(workstream.metadata):
        blockers.append(
            _blocker(
                workstream.workstream_id,
                ReviewKind.LOGIC,
                "statement_drift",
                f"Workstream `{workstream.workstream_id}` records statement drift metadata.",
                metadata=workstream.metadata,
            )
        )

    for claim in state.claims:
        if claim.claim_id in associated["claim_ids"] and _metadata_has_statement_drift(claim.metadata):
            blockers.append(
                _blocker(
                    workstream.workstream_id,
                    ReviewKind.LOGIC,
                    "statement_drift",
                    f"Claim `{claim.claim_id}` records statement drift metadata.",
                    source_id=claim.claim_id,
                    metadata=claim.to_dict(),
                )
            )

    for node_id in associated["node_ids"]:
        node = graph.get_node(node_id)
        if node and _metadata_has_statement_drift(node.metadata):
            blockers.append(
                _blocker(
                    workstream.workstream_id,
                    ReviewKind.LOGIC,
                    "statement_drift",
                    f"Artifact node `{node_id}` records statement drift metadata.",
                    source_id=node_id,
                    metadata=node.to_dict(),
                )
            )
    return blockers


def _lean_blockers(
    workstream: WorkstreamRecord,
    graph: ArtifactGraph,
    associated: dict[str, set[str]],
    project_dir: Path | None,
) -> list[ReviewGateBlocker]:
    total_counts = {key: 0 for key in _LEAN_BLOCKING_COUNTS}
    findings: list[dict[str, Any]] = []

    for source_id, metadata in _associated_metadata_sources(workstream, graph, associated):
        counts = _lean_counts_from_metadata(metadata)
        if not _counts_have_lean_findings(counts):
            continue
        for key in total_counts:
            total_counts[key] += int(counts.get(key, 0) or 0)
        findings.append({"source_id": source_id, "counts": counts})

    for path in _lean_paths(workstream, graph, associated, project_dir):
        audit = audit_lean_source_file(path)
        counts = audit.get("counts", {})
        if not _counts_have_lean_findings(counts):
            continue
        for key in total_counts:
            total_counts[key] += int(counts.get(key, 0) or 0)
        findings.append({"source_id": str(path), "counts": counts})

    if not any(total_counts.values()):
        return []

    count_text = ", ".join(f"{key}={total_counts[key]}" for key in _LEAN_BLOCKING_COUNTS if total_counts[key])
    return [
        _blocker(
            workstream.workstream_id,
            ReviewKind.LEAN,
            "lean_findings",
            f"Lean audit findings block approval for `{workstream.workstream_id}`: {count_text}.",
            metadata={"counts": total_counts, "findings": findings},
        )
    ]


def _computation_blockers(
    workstream: WorkstreamRecord,
    graph: ArtifactGraph,
    associated: dict[str, set[str]],
) -> list[ReviewGateBlocker]:
    blockers: list[ReviewGateBlocker] = []
    for node_id in associated["node_ids"]:
        node = graph.get_node(node_id)
        if not node or node.kind != ArtifactKind.COMPUTATION_CERTIFICATE:
            continue
        status = str(node.metadata.get("status", "")).strip().lower()
        verified = node.metadata.get("verified")
        if _is_falsey(verified) or status in {"failed", "invalid", "unverified", "needs_review"}:
            blockers.append(
                _blocker(
                    workstream.workstream_id,
                    ReviewKind.COMPUTATION,
                    "computation_certificate_unverified",
                    f"Computation certificate `{node_id}` is not verified.",
                    source_id=node_id,
                    metadata=node.to_dict(),
                )
            )
    metadata_status = str(workstream.metadata.get("computation_status", "")).strip().lower()
    if metadata_status in {"failed", "invalid", "unverified", "needs_review"}:
        blockers.append(
            _blocker(
                workstream.workstream_id,
                ReviewKind.COMPUTATION,
                "computation_certificate_unverified",
                f"Workstream `{workstream.workstream_id}` records unverified computation status `{metadata_status}`.",
                metadata=workstream.metadata,
            )
        )
    return blockers


def _review_decision_blockers(
    workstream: WorkstreamRecord,
    reviews: list[ReviewRecord],
    required_kinds: list[ReviewKind],
    *,
    require_existing_reviews: bool,
) -> list[ReviewGateBlocker]:
    blockers: list[ReviewGateBlocker] = []
    latest = _latest_reviews_by_kind(workstream.workstream_id, reviews)

    if require_existing_reviews:
        for kind in required_kinds:
            if kind not in latest:
                blockers.append(
                    _blocker(
                        workstream.workstream_id,
                        kind,
                        "missing_review_decision",
                        f"Missing `{kind.value}` review decision for workstream `{workstream.workstream_id}`.",
                    )
                )

    for kind, review in latest.items():
        if kind not in required_kinds or review.decision == ReviewDecision.APPROVED:
            continue
        code = "review_rejected" if review.decision == ReviewDecision.REJECTED else "review_not_approved"
        blockers.append(
            _blocker(
                workstream.workstream_id,
                kind,
                code,
                f"`{kind.value}` review `{review.review_id}` is `{review.decision.value}`.",
                source_id=review.review_id,
                metadata=review.to_dict(),
            )
        )
    return blockers


def _kind_decisions(
    required_kinds: list[ReviewKind],
    blockers: list[ReviewGateBlocker],
) -> list[ReviewGateKindDecision]:
    decisions: list[ReviewGateKindDecision] = []
    for kind in required_kinds:
        if kind == ReviewKind.GLOBAL:
            relevant = blockers
        else:
            relevant = [blocker for blocker in blockers if blocker.kind == kind]
        if not relevant:
            decisions.append(
                ReviewGateKindDecision(kind=kind, decision=ReviewDecision.APPROVED, notes="No local blockers.")
            )
            continue
        decision = (
            ReviewDecision.REJECTED
            if any(blocker.code == "review_rejected" for blocker in relevant)
            else ReviewDecision.NEEDS_REVISION
        )
        decisions.append(
            ReviewGateKindDecision(
                kind=kind,
                decision=decision,
                blocker_ids=[blocker.blocker_id for blocker in relevant],
                notes=f"{len(relevant)} blocker(s) require revision.",
            )
        )
    return decisions


def _latest_reviews_by_kind(workstream_id: str, reviews: list[ReviewRecord]) -> dict[ReviewKind, ReviewRecord]:
    latest: dict[ReviewKind, ReviewRecord] = {}
    for review in reviews:
        if review.target_id != workstream_id or review.metadata.get("mode") == "review_gate":
            continue
        kind = normalize_review_kind(review.kind)
        existing = latest.get(kind)
        if existing is None or (review.updated_at, review.created_at, review.review_id) >= (
            existing.updated_at,
            existing.created_at,
            existing.review_id,
        ):
            latest[kind] = review
    return latest


def _dependency_path_to_original(
    graph: ArtifactGraph,
    candidate_node_ids: set[str],
    original_node_id: str,
) -> list[str]:
    if original_node_id in candidate_node_ids:
        return [original_node_id]
    for node_id in sorted(candidate_node_ids):
        if not graph.get_node(node_id):
            continue
        forward = graph.dependency_path(node_id, original_node_id)
        if forward:
            return forward
        reverse = graph.dependency_path(original_node_id, node_id)
        if reverse:
            return reverse
    return []


def _associated_metadata_sources(
    workstream: WorkstreamRecord,
    graph: ArtifactGraph,
    associated: dict[str, set[str]],
) -> list[tuple[str, dict[str, Any]]]:
    sources = [(workstream.workstream_id, workstream.metadata)]
    for node_id in associated["node_ids"]:
        node = graph.get_node(node_id)
        if node:
            sources.append((node_id, node.metadata))
    return sources


def _lean_paths(
    workstream: WorkstreamRecord,
    graph: ArtifactGraph,
    associated: dict[str, set[str]],
    project_dir: Path | None,
) -> list[Path]:
    paths: list[Path] = []
    for raw_path in workstream.metadata.get("lean_paths", []) or []:
        if str(raw_path).strip():
            paths.append(_resolve_path(project_dir, str(raw_path)))
    for artifact_id in workstream.artifact_ids:
        if artifact_id.endswith(".lean"):
            paths.append(_resolve_path(project_dir, artifact_id))
    for node_id in associated["node_ids"]:
        node = graph.get_node(node_id)
        if not node or not node.path:
            continue
        if node.kind == ArtifactKind.LEAN_DECLARATION or node.path.endswith(".lean"):
            paths.append(_resolve_path(project_dir, node.path))

    deduped: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path)
        if key not in seen:
            deduped.append(path)
            seen.add(key)
    return deduped


def _resolve_path(project_dir: Path | None, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute() or project_dir is None:
        return path
    return Path(project_dir) / path


def _lean_counts_from_metadata(metadata: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for source in (
        metadata.get("counts"),
        metadata.get("lean_counts"),
        _nested_counts(metadata.get("lean_audit")),
        _nested_counts(metadata.get("source_audit")),
        _nested_counts(metadata.get("audit")),
    ):
        if isinstance(source, dict):
            for key in _LEAN_BLOCKING_COUNTS:
                counts[key] = counts.get(key, 0) + int(source.get(key, 0) or 0)
    for key in _LEAN_BLOCKING_COUNTS:
        metadata_key = f"{key}_count"
        if metadata_key in metadata:
            counts[key] = counts.get(key, 0) + int(metadata.get(metadata_key, 0) or 0)
    return counts


def _nested_counts(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        counts = value.get("counts")
        if isinstance(counts, dict):
            return counts
    return {}


def _counts_have_lean_findings(counts: dict[str, Any]) -> bool:
    return any(int(counts.get(key, 0) or 0) > 0 for key in _LEAN_BLOCKING_COUNTS)


def _open_uncertainty_item(item: UncertaintyItem) -> bool:
    return item.status in _OPEN_UNCERTAINTY_STATUSES


def _item_applies_to_workstream(
    item: UncertaintyItem,
    workstream: WorkstreamRecord,
    associated: dict[str, set[str]],
) -> bool:
    if item.owner_workstream_id == workstream.workstream_id:
        return True
    if item.claim_id and item.claim_id in associated["claim_ids"]:
        return True
    if set(item.related_artifact_ids) & associated["artifact_ids"]:
        return True
    return False


def _source_debt_blocks(item: UncertaintyItem) -> bool:
    if item.source_debt_status is None:
        return True
    return item.source_debt_status in _BLOCKING_SOURCE_STATUSES


def _metadata_has_statement_drift(metadata: dict[str, Any]) -> bool:
    if _is_truthy(metadata.get("statement_drift")):
        return True
    if _is_falsey(metadata.get("aligned_with_original")):
        return True
    alignment = str(metadata.get("statement_alignment", "")).strip().lower()
    return alignment in {"drift", "drifted", "mismatch", "misaligned", "not_aligned"}


def _is_truthy(value: Any) -> bool:
    if value is True:
        return True
    return str(value).strip().lower() in {"1", "true", "yes", "y", "drift", "drifted"}


def _is_falsey(value: Any) -> bool:
    if value is False:
        return True
    return str(value).strip().lower() in {"0", "false", "no", "n", "unverified", "not_verified"}


def _blocker(
    workstream_id: str,
    kind: ReviewKind,
    code: str,
    message: str,
    *,
    source_id: str = "",
    severity: str = "high",
    metadata: dict[str, Any] | None = None,
) -> ReviewGateBlocker:
    suffix = source_id or code
    return ReviewGateBlocker(
        blocker_id=f"{workstream_id}:{code}:{_slug_id(suffix)}",
        kind=kind,
        code=code,
        message=message,
        severity=severity,
        source_id=source_id,
        metadata=metadata or {},
    )


def _slug_id(value: str) -> str:
    cleaned = "".join(char if char.isalnum() else "-" for char in value.strip().lower())
    cleaned = "-".join(part for part in cleaned.split("-") if part)
    return cleaned[:80] or "blocker"
