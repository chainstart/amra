from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Protocol


EXECUTOR_INTERFACE_SCHEMA_VERSION = "amra.domain_search_executor.v1"
RESULT_SCHEMA_VERSION = "amra.domain_search_result.v1"


def _clean_string_list(values: list[Any] | tuple[Any, ...] | set[Any] | None) -> list[str]:
    if values is None:
        return []
    cleaned: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = str(value).strip()
        if not item or item in seen:
            continue
        seen.add(item)
        cleaned.append(item)
    return cleaned


@dataclass(frozen=True, slots=True)
class SearchBudget:
    """Finite bounds for a deterministic domain executor invocation."""

    max_candidates: int = 1000
    max_n: int | None = None

    def normalized(self) -> "SearchBudget":
        max_candidates = max(0, int(self.max_candidates))
        max_n = None if self.max_n is None else max(0, int(self.max_n))
        return SearchBudget(max_candidates=max_candidates, max_n=max_n)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self.normalized())


@dataclass(frozen=True, slots=True)
class DomainSearchRequest:
    """Input envelope accepted by all AMRA domain search executors."""

    problem_id: str
    title: str = ""
    statement: str = ""
    domain: str = ""
    tags: list[str] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)
    candidates: list[Any] = field(default_factory=list)
    budget: SearchBudget = field(default_factory=SearchBudget)

    @classmethod
    def from_problem(
        cls,
        problem: Any,
        *,
        parameters: dict[str, Any] | None = None,
        candidates: list[Any] | None = None,
        budget: SearchBudget | None = None,
    ) -> "DomainSearchRequest":
        return cls(
            problem_id=str(getattr(problem, "problem_id", "")).strip(),
            title=str(getattr(problem, "title", "")).strip(),
            statement=str(getattr(problem, "statement", "")).strip(),
            domain=str(getattr(problem, "domain", "")).strip(),
            tags=_clean_string_list(getattr(problem, "tags", [])),
            parameters=dict(parameters or {}),
            candidates=list(candidates or []),
            budget=budget or SearchBudget(),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["budget"] = self.budget.to_dict()
        return payload


@dataclass(frozen=True, slots=True)
class ExecutorMetadata:
    executor_id: str
    name: str
    family: str
    domains: list[str]
    tags: list[str]
    result_kinds: list[str]
    default_parameters: dict[str, Any]
    description: str
    deterministic: bool = True
    bounded: bool = True
    interface_schema: str = EXECUTOR_INTERFACE_SCHEMA_VERSION
    safety_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["domains"] = _clean_string_list(self.domains)
        payload["tags"] = _clean_string_list(self.tags)
        payload["result_kinds"] = _clean_string_list(self.result_kinds)
        payload["safety_notes"] = _clean_string_list(self.safety_notes)
        return payload


@dataclass(frozen=True, slots=True)
class DomainSearchResult:
    executor_id: str
    problem_id: str
    status: str
    result_kind: str
    parameters: dict[str, Any]
    bounds: dict[str, Any]
    candidate_count: int
    witnesses: list[Any] = field(default_factory=list)
    observations: list[dict[str, Any]] = field(default_factory=list)
    exhausted: bool = True
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = RESULT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DomainSearchExecutor(Protocol):
    metadata: ExecutorMetadata

    def run(self, request: DomainSearchRequest | Any = None, **parameters: Any) -> DomainSearchResult:
        ...


def coerce_request(
    value: DomainSearchRequest | Any = None,
    *,
    parameters: dict[str, Any] | None = None,
    budget: SearchBudget | None = None,
    candidates: list[Any] | None = None,
) -> DomainSearchRequest:
    merged_parameters = dict(parameters or {})
    if isinstance(value, DomainSearchRequest):
        if not merged_parameters and budget is None and candidates is None:
            return value
        return DomainSearchRequest(
            problem_id=value.problem_id,
            title=value.title,
            statement=value.statement,
            domain=value.domain,
            tags=list(value.tags),
            parameters={**value.parameters, **merged_parameters},
            candidates=list(candidates if candidates is not None else value.candidates),
            budget=budget or value.budget,
        )
    if value is None:
        return DomainSearchRequest(problem_id="", parameters=merged_parameters, budget=budget or SearchBudget(), candidates=list(candidates or []))
    if isinstance(value, dict):
        request_budget = budget or SearchBudget(
            max_candidates=int(value.get("max_candidates", 1000) or 1000),
            max_n=value.get("max_n"),
        )
        request_parameters = {**dict(value.get("parameters", {})), **merged_parameters}
        return DomainSearchRequest(
            problem_id=str(value.get("problem_id", "")).strip(),
            title=str(value.get("title", "")).strip(),
            statement=str(value.get("statement", "")).strip(),
            domain=str(value.get("domain", "")).strip(),
            tags=_clean_string_list(value.get("tags", [])),
            parameters=request_parameters,
            candidates=list(candidates if candidates is not None else value.get("candidates", [])),
            budget=request_budget,
        )
    if isinstance(value, str):
        return DomainSearchRequest(problem_id=value, parameters=merged_parameters, budget=budget or SearchBudget(), candidates=list(candidates or []))
    return DomainSearchRequest.from_problem(value, parameters=merged_parameters, candidates=candidates, budget=budget)


def positive_int_parameter(
    parameters: dict[str, Any],
    name: str,
    *,
    default: int,
    minimum: int = 0,
    hard_max: int | None = None,
) -> tuple[int, bool]:
    raw_value = parameters.get(name, default)
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        value = default
    value = max(minimum, value)
    truncated = False
    if hard_max is not None and value > hard_max:
        value = hard_max
        truncated = True
    return value, truncated
