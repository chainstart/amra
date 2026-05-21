from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from amra.orchestration.workstreams import utc_now_iso


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


class EvidenceKind(_StringEnum):
    PROOF_EVIDENCE = "proof_evidence"
    LEAN_VERIFIED = "lean_verified"
    COMPUTATION_CERTIFICATE = "computation_certificate"
    EMPIRICAL_EVIDENCE = "empirical_evidence"
    STATISTICAL_EVIDENCE = "statistical_evidence"
    BENCHMARK_EVIDENCE = "benchmark_evidence"
    COUNTEREXAMPLE_EVIDENCE = "counterexample_evidence"
    SOURCE_EVIDENCE = "source_evidence"
    SECURITY_EVIDENCE = "security_evidence"
    NEGATIVE_EVIDENCE = "negative_evidence"


class EvidenceStatus(_StringEnum):
    DRAFT = "draft"
    RECORDED = "recorded"
    REPRODUCIBLE = "reproducible"
    REVIEWED = "reviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class EvidenceConfidence(_StringEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    THEOREM_GRADE = "theorem_grade"


THEOREM_GRADE_EVIDENCE = {EvidenceKind.PROOF_EVIDENCE, EvidenceKind.LEAN_VERIFIED}


def _string_list(values: list[Any] | None) -> list[str]:
    return [str(value) for value in values or []]


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


@dataclass(slots=True)
class EvidenceRecord:
    evidence_id: str
    kind: EvidenceKind
    target_object_id: str
    summary: str = ""
    status: EvidenceStatus = EvidenceStatus.RECORDED
    confidence: EvidenceConfidence = EvidenceConfidence.UNKNOWN
    artifact_ids: list[str] = field(default_factory=list)
    source_ids: list[str] = field(default_factory=list)
    command: str = ""
    checksum: str = ""
    notes: str = ""
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.kind = EvidenceKind.coerce(self.kind)
        self.status = EvidenceStatus.coerce(self.status)
        self.confidence = EvidenceConfidence.coerce(self.confidence)
        self.artifact_ids = _string_list(self.artifact_ids)
        self.source_ids = _string_list(self.source_ids)
        self.metadata = _dict_value(self.metadata)
        if self.confidence == EvidenceConfidence.THEOREM_GRADE and self.kind not in THEOREM_GRADE_EVIDENCE:
            raise ValueError(f"{self.kind.value} cannot be marked theorem_grade")

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "EvidenceRecord":
        return cls(
            evidence_id=str(payload["evidence_id"]),
            kind=EvidenceKind.coerce(payload["kind"]),
            target_object_id=str(payload.get("target_object_id", "")),
            summary=str(payload.get("summary", "")),
            status=EvidenceStatus.coerce(payload.get("status", EvidenceStatus.RECORDED)),
            confidence=EvidenceConfidence.coerce(payload.get("confidence", EvidenceConfidence.UNKNOWN)),
            artifact_ids=_string_list(payload.get("artifact_ids")),
            source_ids=_string_list(payload.get("source_ids")),
            command=str(payload.get("command", "")),
            checksum=str(payload.get("checksum", "")),
            notes=str(payload.get("notes", "")),
            created_at=str(payload.get("created_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    @property
    def theorem_grade(self) -> bool:
        return self.kind in THEOREM_GRADE_EVIDENCE and self.confidence == EvidenceConfidence.THEOREM_GRADE

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "kind": self.kind.value,
            "target_object_id": self.target_object_id,
            "summary": self.summary,
            "status": self.status.value,
            "confidence": self.confidence.value,
            "artifact_ids": list(self.artifact_ids),
            "source_ids": list(self.source_ids),
            "command": self.command,
            "checksum": self.checksum,
            "notes": self.notes,
            "created_at": self.created_at,
            "metadata": dict(self.metadata),
            "theorem_grade": self.theorem_grade,
        }
