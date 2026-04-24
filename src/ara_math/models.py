from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _dict_value(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}


@dataclass(slots=True)
class ProblemRecord:
    problem_id: str
    title: str
    source: str
    statement: str
    domain: str
    tags: list[str] = field(default_factory=list)
    open_problem: bool = True
    formalized: str = "no"
    notes: str = ""
    references: list[str] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    recommended_strategy: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProblemRecord":
        formalized = payload.get("formalized", "no")
        if isinstance(formalized, bool):
            formalized = "yes" if formalized else "no"
        return cls(
            problem_id=str(payload["problem_id"]),
            title=str(payload["title"]),
            source=str(payload.get("source", "")),
            statement=str(payload.get("statement", "")).strip(),
            domain=str(payload.get("domain", "unknown")),
            tags=_string_list(payload.get("tags")),
            open_problem=bool(payload.get("open_problem", True)),
            formalized=str(formalized),
            notes=str(payload.get("notes", "")).strip(),
            references=_string_list(payload.get("references")),
            hypotheses=_string_list(payload.get("hypotheses")),
            recommended_strategy=_string_list(payload.get("recommended_strategy")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ClaimRecord:
    claim_id: str
    title: str
    statement: str
    status: str
    validation_mode: str
    depends_on: list[str] = field(default_factory=list)
    evidence_paths: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ProofTask:
    task_id: str
    task_type: str
    title: str
    description: str
    success_contract: str
    validation_mode: str
    depends_on: list[str] = field(default_factory=list)
    claim_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ProofPlan:
    project_name: str
    generated_at: str
    problem: dict[str, Any]
    tasks: list[ProofTask] = field(default_factory=list)
    claims: list[ClaimRecord] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["tasks"] = [task.to_dict() for task in self.tasks]
        payload["claims"] = [claim.to_dict() for claim in self.claims]
        return payload


@dataclass(slots=True)
class LeanBuildReport:
    status: str
    command: list[str]
    workdir: str
    generated_at: str
    build_seconds: float
    returncode: int | None
    sorry_count: int
    diagnostics: list[str] = field(default_factory=list)
    stdout_tail: str = ""
    stderr_tail: str = ""
    toolchain: dict[str, str | None] = field(default_factory=dict)
    reuse_report: dict[str, Any] = field(default_factory=dict)
    resource_policy: dict[str, Any] = field(default_factory=dict)
    system_guard: dict[str, Any] = field(default_factory=dict)
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
