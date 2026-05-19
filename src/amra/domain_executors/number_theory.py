from __future__ import annotations

from math import isqrt
from typing import Any

from amra.domain_executors.base import (
    DomainSearchRequest,
    DomainSearchResult,
    ExecutorMetadata,
    SearchBudget,
    coerce_request,
    positive_int_parameter,
)


def _factorization(n: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    remaining = n
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = isqrt(n)
    divisor = 3
    while divisor <= limit:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def _proper_divisor_sum(n: int) -> int:
    if n <= 1:
        return 0
    total = 1
    limit = isqrt(n)
    for divisor in range(2, limit + 1):
        if n % divisor != 0:
            continue
        paired = n // divisor
        total += divisor
        if paired != divisor:
            total += paired
    return total


def _unitary_sigma(n: int) -> int:
    product = 1
    for prime, exponent in _factorization(n).items():
        product *= 1 + prime**exponent
    return product


def _is_squarefree_from_factors(factors: dict[int, int]) -> bool:
    return all(exponent == 1 for exponent in factors.values())


def _is_carmichael_by_korselt(n: int) -> bool:
    if n < 3 or _is_prime(n):
        return False
    factors = _factorization(n)
    if not _is_squarefree_from_factors(factors):
        return False
    return all((n - 1) % (prime - 1) == 0 for prime in factors)


def _request_parameters(
    request: DomainSearchRequest,
    defaults: dict[str, Any],
    runtime_parameters: dict[str, Any],
) -> dict[str, Any]:
    parameters = {**defaults, **request.parameters, **runtime_parameters}
    if request.budget.max_n is not None and "max_n" not in runtime_parameters and "max_n" not in request.parameters:
        parameters["max_n"] = request.budget.max_n
    if request.budget.max_candidates is not None and "max_candidates" not in runtime_parameters and "max_candidates" not in request.parameters:
        parameters["max_candidates"] = request.budget.max_candidates
    return parameters


class BoundedUnitaryPerfectExecutor:
    metadata = ExecutorMetadata(
        executor_id="unitary_perfect.bounded_divisor_scan.v1",
        name="Bounded unitary perfect divisor scan",
        family="unitary_perfect_numbers",
        domains=["number_theory"],
        tags=["unitary_perfect", "divisors", "multiplicative_functions", "computational_search"],
        result_kinds=["unitary_perfect_candidates"],
        default_parameters={"max_n": 1000, "hard_max_n": 100000},
        description="Enumerates n <= max_n and reports values satisfying sigma_star(n) = 2n.",
        safety_notes=["Requires an explicit finite max_n or uses the executor default bound."],
    )

    def run(self, request: DomainSearchRequest | Any = None, **parameters: Any) -> DomainSearchResult:
        search_request = coerce_request(request, parameters=parameters)
        merged = _request_parameters(search_request, self.metadata.default_parameters, parameters)
        max_n, truncated = positive_int_parameter(
            merged,
            "max_n",
            default=int(self.metadata.default_parameters["max_n"]),
            minimum=1,
            hard_max=int(self.metadata.default_parameters["hard_max_n"]),
        )
        witnesses: list[int] = []
        observations: list[dict[str, Any]] = []
        for n in range(1, max_n + 1):
            sigma_star = _unitary_sigma(n)
            if sigma_star == 2 * n:
                witnesses.append(n)
                observations.append(
                    {
                        "n": n,
                        "unitary_sigma": sigma_star,
                        "factorization": _factorization(n),
                        "certificate": "sigma_star(n) = 2n",
                    }
                )
        status = "completed_truncated" if truncated else "completed"
        return DomainSearchResult(
            executor_id=self.metadata.executor_id,
            problem_id=search_request.problem_id,
            status=status,
            result_kind="unitary_perfect_candidates",
            parameters={"max_n": max_n},
            bounds={"max_n": max_n, "hard_max_n": self.metadata.default_parameters["hard_max_n"]},
            candidate_count=max_n,
            witnesses=witnesses,
            observations=observations,
            exhausted=not truncated,
            summary="Bounded scan completed; witnesses are examples, not a finiteness proof.",
            metadata={"deterministic": True, "bounded": True},
        )


class BoundedAmicableExecutor:
    metadata = ExecutorMetadata(
        executor_id="amicable.bounded_divisor_sum_scan.v1",
        name="Bounded amicable divisor-sum scan",
        family="amicable_numbers",
        domains=["number_theory"],
        tags=["amicable_numbers", "proper_divisor_sum", "computational_search"],
        result_kinds=["amicable_pairs"],
        default_parameters={"max_n": 1000, "hard_max_n": 100000, "pair_parity": "any"},
        description="Enumerates amicable pairs a < b <= max_n by proper divisor sums.",
        safety_notes=["Finite max_n bound is always applied; pair_parity may be any, odd_odd, even_even, or mixed."],
    )

    def run(self, request: DomainSearchRequest | Any = None, **parameters: Any) -> DomainSearchResult:
        search_request = coerce_request(request, parameters=parameters)
        merged = _request_parameters(search_request, self.metadata.default_parameters, parameters)
        if "odd-odd" in f"{search_request.problem_id} {search_request.title}".lower() and "pair_parity" not in parameters:
            merged["pair_parity"] = "odd_odd"
        max_n, truncated = positive_int_parameter(
            merged,
            "max_n",
            default=int(self.metadata.default_parameters["max_n"]),
            minimum=2,
            hard_max=int(self.metadata.default_parameters["hard_max_n"]),
        )
        parity = str(merged.get("pair_parity", "any")).strip().lower().replace("-", "_")
        divisor_sums = {n: _proper_divisor_sum(n) for n in range(1, max_n + 1)}
        pairs: list[tuple[int, int]] = []
        observations: list[dict[str, Any]] = []
        for a in range(2, max_n + 1):
            b = divisor_sums[a]
            if b <= a or b > max_n:
                continue
            if divisor_sums.get(b) != a:
                continue
            if parity == "odd_odd" and (a % 2 == 0 or b % 2 == 0):
                continue
            if parity == "even_even" and (a % 2 == 1 or b % 2 == 1):
                continue
            if parity == "mixed" and (a % 2) == (b % 2):
                continue
            pairs.append((a, b))
            observations.append(
                {
                    "pair": [a, b],
                    "proper_divisor_sum": {str(a): b, str(b): a},
                    "parity": "odd_odd" if a % 2 and b % 2 else "even_even" if a % 2 == b % 2 else "mixed",
                }
            )
        status = "completed_truncated" if truncated else "completed"
        return DomainSearchResult(
            executor_id=self.metadata.executor_id,
            problem_id=search_request.problem_id,
            status=status,
            result_kind="amicable_pairs",
            parameters={"max_n": max_n, "pair_parity": parity},
            bounds={"max_n": max_n, "hard_max_n": self.metadata.default_parameters["hard_max_n"]},
            candidate_count=max(0, max_n - 1),
            witnesses=[list(pair) for pair in pairs],
            observations=observations,
            exhausted=not truncated,
            summary="Bounded divisor-sum scan completed; absence of pairs only covers the requested range.",
            metadata={"deterministic": True, "bounded": True},
        )


class BoundedCarmichaelExecutor:
    metadata = ExecutorMetadata(
        executor_id="carmichael.korselt_scan.v1",
        name="Bounded Carmichael Korselt scan",
        family="carmichael_numbers",
        domains=["number_theory"],
        tags=["carmichael_numbers", "korselt", "squarefree", "computational_search"],
        result_kinds=["carmichael_candidates"],
        default_parameters={"max_n": 1000, "hard_max_n": 100000},
        description="Enumerates composite squarefree n <= max_n satisfying Korselt's divisibility criterion.",
        safety_notes=["Finite max_n bound is always applied; the executor certifies only checked candidates."],
    )

    def run(self, request: DomainSearchRequest | Any = None, **parameters: Any) -> DomainSearchResult:
        search_request = coerce_request(request, parameters=parameters)
        merged = _request_parameters(search_request, self.metadata.default_parameters, parameters)
        max_n, truncated = positive_int_parameter(
            merged,
            "max_n",
            default=int(self.metadata.default_parameters["max_n"]),
            minimum=3,
            hard_max=int(self.metadata.default_parameters["hard_max_n"]),
        )
        witnesses: list[int] = []
        observations: list[dict[str, Any]] = []
        for n in range(3, max_n + 1):
            if not _is_carmichael_by_korselt(n):
                continue
            factors = _factorization(n)
            witnesses.append(n)
            observations.append(
                {
                    "n": n,
                    "prime_factors": sorted(factors),
                    "squarefree": True,
                    "korselt_divisibility": {str(prime): (n - 1) // (prime - 1) for prime in sorted(factors)},
                    "certificate": "composite squarefree and p - 1 divides n - 1 for every p | n",
                }
            )
        status = "completed_truncated" if truncated else "completed"
        return DomainSearchResult(
            executor_id=self.metadata.executor_id,
            problem_id=search_request.problem_id,
            status=status,
            result_kind="carmichael_candidates",
            parameters={"max_n": max_n},
            bounds={"max_n": max_n, "hard_max_n": self.metadata.default_parameters["hard_max_n"]},
            candidate_count=max(0, max_n - 2),
            witnesses=witnesses,
            observations=observations,
            exhausted=not truncated,
            summary="Bounded Korselt scan completed; witnesses are finite-range examples.",
            metadata={"deterministic": True, "bounded": True},
        )


__all__ = [
    "BoundedAmicableExecutor",
    "BoundedCarmichaelExecutor",
    "BoundedUnitaryPerfectExecutor",
    "SearchBudget",
]
