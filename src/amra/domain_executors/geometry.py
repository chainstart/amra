from __future__ import annotations

import re
from math import isqrt
from typing import Any

from amra.domain_executors.base import (
    DomainSearchRequest,
    DomainSearchResult,
    ExecutorMetadata,
    coerce_request,
    positive_int_parameter,
)


def _is_square(n: int) -> bool:
    if n < 0:
        return False
    root = isqrt(n)
    return root * root == n


def _integer_candidates(request: DomainSearchRequest, parameters: dict[str, Any]) -> list[int]:
    raw_candidates: list[Any] = []
    raw_candidates.extend(request.candidates)
    raw_candidates.extend(parameters.get("triangle_counts", []) or [])
    raw_candidates.extend(parameters.get("candidate_counts", []) or [])
    if not raw_candidates:
        raw_candidates.extend(re.findall(r"\d+", f"{request.problem_id} {request.title}"))
    candidates: list[int] = []
    seen: set[int] = set()
    for raw in raw_candidates:
        try:
            candidate = int(raw)
        except (TypeError, ValueError):
            continue
        if candidate <= 0 or candidate in seen:
            continue
        seen.add(candidate)
        candidates.append(candidate)
    return candidates


class TriangleDissectionCertificateExecutor:
    metadata = ExecutorMetadata(
        executor_id="triangle_dissection.certificate_stub.v1",
        name="Triangle dissection finite-certificate stub",
        family="triangle_dissections",
        domains=["geometry", "discrete_geometry"],
        tags=["triangle_dissection", "finite_case", "geometry", "computational_search"],
        result_kinds=["triangle_dissection_cases"],
        default_parameters={"max_cases": 20},
        description=(
            "Classifies supplied triangle-count cases without launching geometric search; "
            "square counts receive the elementary grid certificate and all other cases remain open for external certificates."
        ),
        safety_notes=["Does not enumerate dissections; it only validates a finite supplied candidate list."],
    )

    def run(self, request: DomainSearchRequest | Any = None, **parameters: Any) -> DomainSearchResult:
        search_request = coerce_request(request, parameters=parameters, candidates=parameters.get("candidates"))
        merged = {**self.metadata.default_parameters, **search_request.parameters, **parameters}
        max_cases, truncated = positive_int_parameter(
            merged,
            "max_cases",
            default=int(self.metadata.default_parameters["max_cases"]),
            minimum=0,
        )
        candidates = _integer_candidates(search_request, merged)
        if len(candidates) > max_cases:
            candidates = candidates[:max_cases]
            truncated = True
        observations: list[dict[str, Any]] = []
        witnesses: list[dict[str, Any]] = []
        known_impossible = {int(value) for value in merged.get("known_impossible_counts", []) or []}
        for n in candidates:
            square = _is_square(n)
            if square:
                root = isqrt(n)
                status = "constructible_by_square_grid"
                certificate = {
                    "kind": "square_grid",
                    "side_subdivision": root,
                    "congruent_triangle_count": n,
                }
                witnesses.append({"triangle_count": n, "certificate": certificate})
            elif n in known_impossible:
                status = "impossible_by_supplied_catalog"
                certificate = {"kind": "supplied_known_impossible_catalog", "congruent_triangle_count": n}
            else:
                status = "requires_external_certificate"
                certificate = {"kind": "not_evaluated", "congruent_triangle_count": n}
            observations.append(
                {
                    "triangle_count": n,
                    "status": status,
                    "certificate": certificate,
                    "bounded_stub": True,
                }
            )
        status = "completed_truncated" if truncated else "completed"
        if not candidates:
            status = "no_candidates"
        return DomainSearchResult(
            executor_id=self.metadata.executor_id,
            problem_id=search_request.problem_id,
            status=status,
            result_kind="triangle_dissection_cases",
            parameters={"max_cases": max_cases, "candidate_counts": candidates},
            bounds={"max_cases": max_cases},
            candidate_count=len(candidates),
            witnesses=witnesses,
            observations=observations,
            exhausted=not truncated,
            summary="Finite certificate stub completed; unresolved counts require a separate checked certificate pipeline.",
            metadata={"deterministic": True, "bounded": True, "does_not_enumerate_dissections": True},
        )


__all__ = ["TriangleDissectionCertificateExecutor"]
