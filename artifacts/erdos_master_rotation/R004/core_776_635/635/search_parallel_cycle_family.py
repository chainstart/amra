#!/usr/bin/env python3
"""Bounded exact search in the R004 parametric parallel-cycle family."""

from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from math import prod

from sympy import divisors, factorint, isprime


def divisors_from_factorization(
    factorization: dict[int, int],
) -> list[int]:
    values = [1]
    for prime, exponent in sorted(factorization.items()):
        values = [
            old * prime**power
            for old in values
            for power in range(exponent + 1)
        ]
    return sorted(values)


def pari_proven_primes(values: set[int]) -> None:
    """Require PARI's proof-producing isprime, not only probable-prime tests."""
    ordered = sorted(values)
    program = "".join(f"print(isprime({value}))\n" for value in ordered)
    completed = subprocess.run(
        ["gp", "-fq"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
    )
    verdicts = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip()
    ]
    assert verdicts == ["1"] * len(ordered), (ordered, verdicts)


def main() -> None:
    cycles: list[dict[str, object]] = []
    parameter_pairs = 0
    factor_pairs = 0
    factor_bases: set[int] = set()
    for b_exponent in range(1, 31):
        B = 1 << b_exponent
        for c_exponent in range(2, 16):
            c = 1 << c_exponent
            parameter_pairs += 1
            for k in divisors(c - 1):
                h = (c - 1) // k
                t = k * B
                product = c * B * B - h
                factorization = {
                    int(prime): int(exponent)
                    for prime, exponent in factorint(product).items()
                }
                assert prod(
                    prime**exponent
                    for prime, exponent in factorization.items()
                ) == product
                factor_bases.update(factorization)
                for left_factor in divisors_from_factorization(
                    factorization
                ):
                    right_factor = product // left_factor
                    if left_factor > right_factor:
                        break
                    factor_pairs += 1
                    if (
                        (left_factor + B) % h
                        or (right_factor + B) % h
                    ):
                        continue
                    p = (left_factor + B) // h
                    q = (right_factor + B) // h
                    translated = (p + t, q + t)
                    if not all(
                        isprime(value) for value in (p, q, *translated)
                    ):
                        continue
                    if p * q % k == 0:
                        continue
                    first_label = c * B * p * q
                    second_label = B * translated[0] * translated[1]
                    assert second_label - first_label == t
                    endpoints = sorted(
                        (first_label - p, first_label - q)
                    )
                    assert endpoints == sorted(
                        (
                            second_label - translated[0],
                            second_label - translated[1],
                        )
                    )
                    cycles.append(
                        {
                            "B": B,
                            "c": c,
                            "k": k,
                            "h": h,
                            "p": p,
                            "q": q,
                            "translation": t,
                            "endpoints": endpoints,
                            "labels": [first_label, second_label],
                        }
                    )

    endpoint_incidence: dict[int, list[int]] = defaultdict(list)
    for index, cycle in enumerate(cycles):
        for endpoint in cycle["endpoints"]:
            endpoint_incidence[int(endpoint)].append(index)
    shared = {
        str(endpoint): indices
        for endpoint, indices in endpoint_incidence.items()
        if len(indices) >= 2
    }

    assert parameter_pairs == 420
    assert len(cycles) == 41
    assert not shared
    candidate_primes = {
        int(value)
        for cycle in cycles
        for value in (
            cycle["p"],
            cycle["q"],
            int(cycle["p"]) + int(cycle["translation"]),
            int(cycle["q"]) + int(cycle["translation"]),
        )
    }
    pari_proven_primes(factor_bases | candidate_primes)
    result = {
        "schema": "amra.erdos635.r004-parallel-family-search.v1",
        "status": "PASS",
        "domain": {
            "B": "2^b, 1<=b<=30",
            "c": "2^j, 2<=j<=15",
            "parameter_pairs": parameter_pairs,
            "factor_pairs_checked": factor_pairs,
            "factorization_prime_bases_proved_by_PARI": len(factor_bases),
        },
        "all_prime_conflict_free_parallel_cycles": len(cycles),
        "nonmaximal_translation_cycles": sum(
            int(cycle["h"]) > 1 for cycle in cycles
        ),
        "cycles": cycles,
        "shared_endpoint_pairs": shared,
        "bicyclic_figure_eight_found": False,
        "primality_backend": {
            "screen": "sympy.isprime",
            "proof": "PARI/GP isprime",
            "distinct_cycle_primes_proved": len(candidate_primes),
        },
        "scope": (
            "Complete only in the displayed parametric family/domain.  "
            "No shared endpoint was found among its 41 cycles; paths outside "
            "the family and arbitrary bicyclic cores remain unrestricted."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
