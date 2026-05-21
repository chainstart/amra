from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, TypeVar


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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


class ProjectStatus(_StringEnum):
    INTAKE = "intake"
    GOALS_PLANNED = "goals_planned"
    WORKSTREAMS_RUNNING = "workstreams_running"
    REVIEW_GATE = "review_gate"
    FINAL_ASSEMBLY = "final_assembly"
    VERIFIED = "verified"
    PARTIAL = "partial"
    FROZEN = "frozen"
    ESCALATED = "escalated"


class WorkstreamKind(_StringEnum):
    PROOF = "proof"
    LEAN = "lean"
    SOURCE = "source"
    COMPUTE = "compute"
    REVIEW = "review"
    DISCOVERY = "discovery"
    EXPERIMENT = "experiment"
    ALGORITHM = "algorithm"
    MODELING = "modeling"
    CRYPTO = "crypto"
    ML_THEORY = "ml_theory"
    BENCHMARK = "benchmark"
    DATA = "data"
    THEORY_BUILDING = "theory_building"


class WorkstreamStatus(_StringEnum):
    PLANNED = "planned"
    RUNNING = "running"
    NEEDS_REVIEW = "needs_review"
    REVISION = "revision"
    APPROVED = "approved"
    FROZEN = "frozen"
    ESCALATED = "escalated"
    TESTING = "testing"
    EMPIRICALLY_SUPPORTED = "empirically_supported"
    STATISTICALLY_SUPPORTED = "statistically_supported"
    COUNTEREXAMPLE_FOUND = "counterexample_found"
    MODEL_CALIBRATED = "model_calibrated"
    MODEL_VALIDATED = "model_validated"
    BENCHMARKED = "benchmarked"
    OPTIMIZED = "optimized"
    SECURITY_GAME_DEFINED = "security_game_defined"
    ATTACK_FOUND = "attack_found"
    REDUCTION_CANDIDATE = "reduction_candidate"
    NOVELTY_CHECKED = "novelty_checked"
    REPRODUCED = "reproduced"
    REJECTED_BY_EVIDENCE = "rejected_by_evidence"
    ARCHIVED = "archived"


class ClaimStatus(_StringEnum):
    HYPOTHESIS = "hypothesis"
    ROUTE_CANDIDATE = "route_candidate"
    PROOF_CANDIDATE = "proof_candidate"
    SOURCE_GROUNDED = "source_grounded"
    LEAN_STUBBED = "lean_stubbed"
    LEAN_VERIFIED = "lean_verified"
    ASSEMBLED = "assembled"
    CONJECTURED = "conjectured"
    EMPIRICALLY_SUPPORTED = "empirically_supported"
    STATISTICALLY_SUPPORTED = "statistically_supported"
    COUNTEREXAMPLE_FOUND = "counterexample_found"
    MODEL_CALIBRATED = "model_calibrated"
    MODEL_VALIDATED = "model_validated"
    BENCHMARKED = "benchmarked"
    OPTIMIZED = "optimized"
    SECURITY_GAME_DEFINED = "security_game_defined"
    ATTACK_FOUND = "attack_found"
    REDUCTION_CANDIDATE = "reduction_candidate"
    NOVELTY_CHECKED = "novelty_checked"
    REPRODUCED = "reproduced"
    REJECTED_BY_EVIDENCE = "rejected_by_evidence"


class ReviewKind(_StringEnum):
    LOGIC = "logic"
    SOURCE = "source"
    LEAN = "lean"
    COMPUTATION = "computation"
    GLOBAL = "global"
    REPRODUCIBILITY = "reproducibility"
    GLOBAL_STRATEGY = "global_strategy"


class ReviewDecision(_StringEnum):
    PENDING = "pending"
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"
    REJECTED = "rejected"


class DependencyStatus(_StringEnum):
    UNKNOWN = "unknown"
    PENDING = "pending"
    READY = "ready"
    SATISFIED = "satisfied"
    RESOLVED = "resolved"
    BLOCKED = "blocked"


EnumT = TypeVar("EnumT", bound=_StringEnum)


def _enum_list(enum_type: type[EnumT], values: list[Any] | None) -> list[EnumT]:
    return [enum_type.coerce(value) for value in values or []]


def _string_list(values: list[Any] | None) -> list[str]:
    return [str(value) for value in values or []]


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


@dataclass(slots=True)
class WorkstreamRecord:
    workstream_id: str
    kind: WorkstreamKind
    goal: str
    status: WorkstreamStatus = WorkstreamStatus.PLANNED
    owner: str = ""
    dependencies: list[str] = field(default_factory=list)
    claim_ids: list[str] = field(default_factory=list)
    artifact_ids: list[str] = field(default_factory=list)
    run_dirs: list[str] = field(default_factory=list)
    artifact_paths: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    budget: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.kind = WorkstreamKind.coerce(self.kind)
        self.status = WorkstreamStatus.coerce(self.status)
        self.dependencies = _string_list(self.dependencies)
        self.claim_ids = _string_list(self.claim_ids)
        self.artifact_ids = _string_list(self.artifact_ids)
        self.run_dirs = _string_list(self.run_dirs)
        self.artifact_paths = _string_list(self.artifact_paths)
        self.blockers = _string_list(self.blockers)
        self.budget = _dict_value(self.budget)
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "WorkstreamRecord":
        return cls(
            workstream_id=str(payload["workstream_id"]),
            kind=WorkstreamKind.coerce(payload.get("kind", WorkstreamKind.PROOF)),
            goal=str(payload.get("goal", "")),
            status=WorkstreamStatus.coerce(payload.get("status", WorkstreamStatus.PLANNED)),
            owner=str(payload.get("owner", "")),
            dependencies=_string_list(payload.get("dependencies")),
            claim_ids=_string_list(payload.get("claim_ids")),
            artifact_ids=_string_list(payload.get("artifact_ids")),
            run_dirs=_string_list(payload.get("run_dirs")),
            artifact_paths=_string_list(payload.get("artifact_paths")),
            blockers=_string_list(payload.get("blockers")),
            budget=_dict_value(payload.get("budget")),
            created_at=str(payload.get("created_at") or utc_now_iso()),
            updated_at=str(payload.get("updated_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "workstream_id": self.workstream_id,
            "kind": self.kind.value,
            "goal": self.goal,
            "status": self.status.value,
            "owner": self.owner,
            "dependencies": list(self.dependencies),
            "claim_ids": list(self.claim_ids),
            "artifact_ids": list(self.artifact_ids),
            "run_dirs": list(self.run_dirs),
            "artifact_paths": list(self.artifact_paths),
            "blockers": list(self.blockers),
            "budget": dict(self.budget),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }

    def mark_status(self, status: WorkstreamStatus | str, *, blocker: str | None = None) -> None:
        self.status = WorkstreamStatus.coerce(status)
        if blocker:
            self.blockers.append(blocker)
        self.updated_at = utc_now_iso()


@dataclass(slots=True)
class ClaimRecord:
    claim_id: str
    title: str
    statement: str
    status: ClaimStatus = ClaimStatus.HYPOTHESIS
    owner_workstream_id: str = ""
    dependency_ids: list[str] = field(default_factory=list)
    artifact_ids: list[str] = field(default_factory=list)
    source_status: str = ""
    confidence: float = 0.0
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.status = ClaimStatus.coerce(self.status)
        self.dependency_ids = _string_list(self.dependency_ids)
        self.artifact_ids = _string_list(self.artifact_ids)
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ClaimRecord":
        return cls(
            claim_id=str(payload["claim_id"]),
            title=str(payload.get("title", "")),
            statement=str(payload.get("statement", "")),
            status=ClaimStatus.coerce(payload.get("status", ClaimStatus.HYPOTHESIS)),
            owner_workstream_id=str(payload.get("owner_workstream_id", "")),
            dependency_ids=_string_list(payload.get("dependency_ids")),
            artifact_ids=_string_list(payload.get("artifact_ids")),
            source_status=str(payload.get("source_status", "")),
            confidence=float(payload.get("confidence", 0.0) or 0.0),
            created_at=str(payload.get("created_at") or utc_now_iso()),
            updated_at=str(payload.get("updated_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "title": self.title,
            "statement": self.statement,
            "status": self.status.value,
            "owner_workstream_id": self.owner_workstream_id,
            "dependency_ids": list(self.dependency_ids),
            "artifact_ids": list(self.artifact_ids),
            "source_status": self.source_status,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }

    def mark_status(self, status: ClaimStatus | str) -> None:
        self.status = ClaimStatus.coerce(status)
        self.updated_at = utc_now_iso()


@dataclass(slots=True)
class ReviewRecord:
    review_id: str
    kind: ReviewKind
    target_id: str
    decision: ReviewDecision = ReviewDecision.PENDING
    reviewer: str = ""
    blocker_ids: list[str] = field(default_factory=list)
    notes: str = ""
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.kind = ReviewKind.coerce(self.kind)
        self.decision = ReviewDecision.coerce(self.decision)
        self.blocker_ids = _string_list(self.blocker_ids)
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ReviewRecord":
        return cls(
            review_id=str(payload["review_id"]),
            kind=ReviewKind.coerce(payload.get("kind", ReviewKind.LOGIC)),
            target_id=str(payload.get("target_id", "")),
            decision=ReviewDecision.coerce(payload.get("decision", ReviewDecision.PENDING)),
            reviewer=str(payload.get("reviewer", "")),
            blocker_ids=_string_list(payload.get("blocker_ids")),
            notes=str(payload.get("notes", "")),
            created_at=str(payload.get("created_at") or utc_now_iso()),
            updated_at=str(payload.get("updated_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "kind": self.kind.value,
            "target_id": self.target_id,
            "decision": self.decision.value,
            "reviewer": self.reviewer,
            "blocker_ids": list(self.blocker_ids),
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }

    def mark_decision(self, decision: ReviewDecision | str, *, notes: str | None = None) -> None:
        self.decision = ReviewDecision.coerce(decision)
        if notes is not None:
            self.notes = notes
        self.updated_at = utc_now_iso()


@dataclass(slots=True)
class ProjectState:
    project_id: str
    project_name: str
    original_goal: str
    status: ProjectStatus = ProjectStatus.INTAKE
    workstreams: list[WorkstreamRecord] = field(default_factory=list)
    claims: list[ClaimRecord] = field(default_factory=list)
    reviews: list[ReviewRecord] = field(default_factory=list)
    top_blocker_id: str = ""
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.status = ProjectStatus.coerce(self.status)
        self.workstreams = [
            WorkstreamRecord.from_dict(item) if isinstance(item, dict) else item for item in self.workstreams
        ]
        self.claims = [ClaimRecord.from_dict(item) if isinstance(item, dict) else item for item in self.claims]
        self.reviews = [ReviewRecord.from_dict(item) if isinstance(item, dict) else item for item in self.reviews]
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProjectState":
        return cls(
            project_id=str(payload["project_id"]),
            project_name=str(payload.get("project_name", payload["project_id"])),
            original_goal=str(payload.get("original_goal", "")),
            status=ProjectStatus.coerce(payload.get("status", ProjectStatus.INTAKE)),
            workstreams=[WorkstreamRecord.from_dict(item) for item in payload.get("workstreams", [])],
            claims=[ClaimRecord.from_dict(item) for item in payload.get("claims", [])],
            reviews=[ReviewRecord.from_dict(item) for item in payload.get("reviews", [])],
            top_blocker_id=str(payload.get("top_blocker_id", "")),
            created_at=str(payload.get("created_at") or utc_now_iso()),
            updated_at=str(payload.get("updated_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "original_goal": self.original_goal,
            "status": self.status.value,
            "workstreams": [workstream.to_dict() for workstream in self.workstreams],
            "claims": [claim.to_dict() for claim in self.claims],
            "reviews": [review.to_dict() for review in self.reviews],
            "top_blocker_id": self.top_blocker_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }

    def add_workstream(self, workstream: WorkstreamRecord | dict[str, Any]) -> None:
        if isinstance(workstream, dict):
            workstream = WorkstreamRecord.from_dict(workstream)
        if any(existing.workstream_id == workstream.workstream_id for existing in self.workstreams):
            raise ValueError(f"Duplicate workstream id: {workstream.workstream_id}")
        self.workstreams.append(workstream)
        if self.status == ProjectStatus.INTAKE:
            self.status = ProjectStatus.GOALS_PLANNED
        self.updated_at = utc_now_iso()

    def upsert_workstream(self, workstream: WorkstreamRecord | dict[str, Any]) -> None:
        if isinstance(workstream, dict):
            workstream = WorkstreamRecord.from_dict(workstream)
        for index, existing in enumerate(self.workstreams):
            if existing.workstream_id == workstream.workstream_id:
                if not workstream.created_at:
                    workstream.created_at = existing.created_at
                self.workstreams[index] = workstream
                self.updated_at = utc_now_iso()
                return
        self.add_workstream(workstream)

    def add_claim(self, claim: ClaimRecord | dict[str, Any]) -> None:
        if isinstance(claim, dict):
            claim = ClaimRecord.from_dict(claim)
        if any(existing.claim_id == claim.claim_id for existing in self.claims):
            raise ValueError(f"Duplicate claim id: {claim.claim_id}")
        self.claims.append(claim)
        self.updated_at = utc_now_iso()

    def add_review(self, review: ReviewRecord | dict[str, Any]) -> None:
        if isinstance(review, dict):
            review = ReviewRecord.from_dict(review)
        if any(existing.review_id == review.review_id for existing in self.reviews):
            raise ValueError(f"Duplicate review id: {review.review_id}")
        self.reviews.append(review)
        self.updated_at = utc_now_iso()

    def upsert_review(self, review: ReviewRecord | dict[str, Any]) -> None:
        if isinstance(review, dict):
            review = ReviewRecord.from_dict(review)
        for index, existing in enumerate(self.reviews):
            if existing.review_id == review.review_id:
                if not review.created_at:
                    review.created_at = existing.created_at
                self.reviews[index] = review
                self.updated_at = utc_now_iso()
                return
        self.add_review(review)

    def get_review(self, review_id: str) -> ReviewRecord | None:
        return next((item for item in self.reviews if item.review_id == review_id), None)

    def get_workstream(self, workstream_id: str) -> WorkstreamRecord | None:
        return next((item for item in self.workstreams if item.workstream_id == workstream_id), None)

    def get_claim(self, claim_id: str) -> ClaimRecord | None:
        return next((item for item in self.claims if item.claim_id == claim_id), None)

    def workstreams_by_status(self, status: WorkstreamStatus | str) -> list[WorkstreamRecord]:
        expected = WorkstreamStatus.coerce(status)
        return [item for item in self.workstreams if item.status == expected]

    def open_workstreams(self) -> list[WorkstreamRecord]:
        closed = {WorkstreamStatus.APPROVED, WorkstreamStatus.FROZEN, WorkstreamStatus.ESCALATED}
        return [item for item in self.workstreams if item.status not in closed]
