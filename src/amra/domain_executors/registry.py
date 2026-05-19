from __future__ import annotations

from typing import Any

from amra.core.models import ProblemRecord
from amra.domain_executors.base import DomainSearchExecutor, DomainSearchResult
from amra.domain_executors.geometry import TriangleDissectionCertificateExecutor
from amra.domain_executors.number_theory import (
    BoundedAmicableExecutor,
    BoundedCarmichaelExecutor,
    BoundedUnitaryPerfectExecutor,
)


DOMAIN_EXECUTOR_METADATA_KEY = "domain_search_executors"


def available_executors() -> dict[str, DomainSearchExecutor]:
    executors: list[DomainSearchExecutor] = [
        BoundedUnitaryPerfectExecutor(),
        BoundedAmicableExecutor(),
        TriangleDissectionCertificateExecutor(),
        BoundedCarmichaelExecutor(),
    ]
    return {executor.metadata.executor_id: executor for executor in executors}


def available_executor_metadata() -> list[dict[str, Any]]:
    return [executor.metadata.to_dict() for executor in available_executors().values()]


def get_executor(executor_id: str) -> DomainSearchExecutor:
    try:
        return available_executors()[executor_id]
    except KeyError as exc:
        raise KeyError(f"Domain executor '{executor_id}' is not registered.") from exc


def _problem_text(problem: Any) -> str:
    fields = [
        getattr(problem, "problem_id", ""),
        getattr(problem, "title", ""),
        getattr(problem, "statement", ""),
        getattr(problem, "domain", ""),
        getattr(problem, "notes", ""),
    ]
    fields.extend(getattr(problem, "tags", []) or [])
    return " ".join(str(field) for field in fields).lower().replace("-", "_")


def _explicit_executor_entries(problem: Any) -> list[dict[str, Any]]:
    metadata = getattr(problem, "metadata", {}) or {}
    raw = metadata.get(DOMAIN_EXECUTOR_METADATA_KEY)
    if raw is None:
        raw = metadata.get("domain_executors")
    if raw is None:
        raw = metadata.get("domain_executor")
    if raw is None:
        return []
    entries = raw if isinstance(raw, list) else [raw]
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entry in entries:
        if isinstance(entry, str):
            item = {"executor_id": entry.strip()}
        elif isinstance(entry, dict):
            item = dict(entry)
            item["executor_id"] = str(item.get("executor_id", "")).strip()
        else:
            continue
        executor_id = str(item.get("executor_id", "")).strip()
        if not executor_id or executor_id in seen:
            continue
        seen.add(executor_id)
        normalized.append(item)
    return normalized


def _explicit_executor_ids(problem: Any) -> list[str]:
    entries = _explicit_executor_entries(problem)
    executor_ids: list[str] = []
    for entry in entries:
        executor_id = str(entry.get("executor_id", "")).strip()
        if executor_id and executor_id not in executor_ids:
            executor_ids.append(executor_id)
    return executor_ids


def infer_executor_ids_for_problem(problem: Any) -> list[str]:
    explicit = _explicit_executor_ids(problem)
    if explicit:
        return [executor_id for executor_id in explicit if executor_id in available_executors()]
    text = _problem_text(problem)
    inferred: list[str] = []
    if "unitary_perfect" in text or "unitary perfect" in text:
        inferred.append("unitary_perfect.bounded_divisor_scan.v1")
    if "amicable_numbers" in text or "amicable" in text:
        inferred.append("amicable.bounded_divisor_sum_scan.v1")
    if "triangle_dissection" in text or ("triangle" in text and ("dissection" in text or "dissected" in text)):
        inferred.append("triangle_dissection.certificate_stub.v1")
    if "carmichael_numbers" in text or "carmichael" in text or "korselt" in text:
        inferred.append("carmichael.korselt_scan.v1")
    return inferred


def select_executors_for_problem(problem: Any) -> list[DomainSearchExecutor]:
    registry = available_executors()
    return [registry[executor_id] for executor_id in infer_executor_ids_for_problem(problem) if executor_id in registry]


def executor_metadata_for_problem(problem: Any) -> list[dict[str, Any]]:
    registry = available_executors()
    explicit_entries = _explicit_executor_entries(problem)
    if explicit_entries:
        metadata: list[dict[str, Any]] = []
        for entry in explicit_entries:
            executor_id = str(entry.get("executor_id", "")).strip()
            if executor_id not in registry:
                continue
            base = registry[executor_id].metadata.to_dict()
            merged = {**base, **entry}
            merged["default_parameters"] = {
                **dict(base.get("default_parameters", {})),
                **dict(entry.get("default_parameters", {}) or {}),
            }
            metadata.append(merged)
        return metadata
    return [executor.metadata.to_dict() for executor in select_executors_for_problem(problem)]


def compact_executor_signal(problem: Any) -> dict[str, Any]:
    metadata = executor_metadata_for_problem(problem)
    return {
        "available": bool(metadata),
        "executor_count": len(metadata),
        "executors": [
            {
                "executor_id": item["executor_id"],
                "family": item["family"],
                "bounded": bool(item["bounded"]),
                "deterministic": bool(item["deterministic"]),
                "result_kinds": list(item.get("result_kinds", [])),
                "default_parameters": dict(item.get("default_parameters", {})),
            }
            for item in metadata
        ],
    }


def _metadata_default_parameters(problem: Any, executor_id: str) -> dict[str, Any]:
    for item in executor_metadata_for_problem(problem):
        if str(item.get("executor_id", "")).strip() == executor_id:
            return dict(item.get("default_parameters", {}) or {})
    return {}


def attach_executor_metadata(problem: ProblemRecord) -> ProblemRecord:
    metadata = dict(problem.metadata or {})
    executor_metadata = executor_metadata_for_problem(problem)
    if executor_metadata:
        metadata[DOMAIN_EXECUTOR_METADATA_KEY] = executor_metadata
    payload = problem.to_dict()
    payload["metadata"] = metadata
    return ProblemRecord.from_dict(payload)


def attach_executor_metadata_to_bank(problems: list[ProblemRecord]) -> list[ProblemRecord]:
    return [attach_executor_metadata(problem) for problem in problems]


def run_domain_executor(
    problem: Any,
    *,
    executor_id: str | None = None,
    **parameters: Any,
) -> DomainSearchResult:
    if executor_id:
        executor = get_executor(executor_id)
        defaults = _metadata_default_parameters(problem, executor.metadata.executor_id)
        return executor.run(problem, **{**defaults, **parameters})
    executors = select_executors_for_problem(problem)
    if not executors:
        problem_id = str(getattr(problem, "problem_id", "")).strip()
        raise KeyError(f"No domain executor is registered for problem '{problem_id}'.")
    executor = executors[0]
    defaults = _metadata_default_parameters(problem, executor.metadata.executor_id)
    return executor.run(problem, **{**defaults, **parameters})


__all__ = [
    "DOMAIN_EXECUTOR_METADATA_KEY",
    "attach_executor_metadata",
    "attach_executor_metadata_to_bank",
    "available_executor_metadata",
    "available_executors",
    "compact_executor_signal",
    "executor_metadata_for_problem",
    "get_executor",
    "infer_executor_ids_for_problem",
    "run_domain_executor",
    "select_executors_for_problem",
]
