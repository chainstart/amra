#!/usr/bin/env python3
"""Exact finite replay for the recursive CRT covering-radius lemma.

This tests arbitrary nonempty local subsets, not merely intervals.  The proof
is in evidence/recursive_gap_lemma.md; finite replay is not its proof.
"""

from __future__ import annotations

import json
from itertools import permutations, product
from math import prod


def covering_radius(moduli: tuple[int, ...], allowed: tuple[frozenset[int], ...]) -> int:
    period = prod(moduli)
    points = [
        n
        for n in range(period)
        if all(n % q in local for q, local in zip(moduli, allowed))
    ]
    assert points
    distances = [points[i + 1] - points[i] - 1 for i in range(len(points) - 1)]
    distances.append(period + points[0] - points[-1] - 1)
    return max(distances)


def recursive_rhs(moduli: tuple[int, ...], sizes: tuple[int, ...], order: tuple[int, ...]) -> int:
    prefix = 1
    ans = 0
    for i in order:
        ans += (moduli[i] - sizes[i]) * prefix
        prefix *= moduli[i]
    return ans


def sorted_order(moduli: tuple[int, ...], sizes: tuple[int, ...]) -> tuple[int, ...]:
    # Exact comparison of (q-1)/(q-d), avoiding floating point.
    from functools import cmp_to_key

    def compare(i: int, j: int) -> int:
        left = (moduli[i] - 1) * (moduli[j] - sizes[j])
        right = (moduli[j] - 1) * (moduli[i] - sizes[i])
        return (left > right) - (left < right)

    return tuple(sorted(range(len(moduli)), key=cmp_to_key(compare)))


def nonempty_subsets(q: int):
    for mask in range(1, 1 << q):
        yield frozenset(i for i in range(q) if mask & (1 << i))


def exhaustive_arbitrary_subset_replay() -> dict[str, object]:
    moduli = (3, 5, 7)
    tested = 0
    max_slack_ratio = 0.0
    equality_cases = 0
    for allowed in product(*[list(nonempty_subsets(q)) for q in moduli]):
        sizes = tuple(len(local) for local in allowed)
        actual = covering_radius(moduli, allowed)
        values = {
            order: recursive_rhs(moduli, sizes, order)
            for order in permutations(range(len(moduli)))
        }
        best = min(values.values())
        assert actual <= best
        claimed_order = sorted_order(moduli, sizes)
        assert values[claimed_order] == best
        tested += 1
        if best == actual:
            equality_cases += 1
        if best:
            max_slack_ratio = max(max_slack_ratio, actual / best)
        else:
            assert actual == 0
    return {
        "moduli": list(moduli),
        "arbitrary_local_subset_systems_tested": tested,
        "all_covering_radius_inequalities_passed": True,
        "all_sorted_orders_attained_minimum_rhs": True,
        "equality_cases": equality_cases,
        "maximum_actual_over_best_rhs": max_slack_ratio,
    }


def interval_primes(k: int) -> list[int]:
    ans = []
    for n in range(k + 1, 2 * k):
        if n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1)):
            ans.append(n)
    return ans


def actual_451_replay() -> list[dict[str, object]]:
    rows = []
    for k in (10, 15, 20):
        ps = tuple(interval_primes(k))
        allowed = tuple(frozenset([0] + list(range(k + 1, p))) for p in ps)
        actual = covering_radius(ps, allowed)
        sizes = tuple(p - k for p in ps)
        order = tuple(range(len(ps)))
        rhs = recursive_rhs(ps, sizes, order)
        rows.append(
            {
                "k": k,
                "primes": list(ps),
                "period": prod(ps),
                "actual_covering_radius": actual,
                "recursive_rhs": rhs,
                "inequality_passed": actual <= rhs,
            }
        )
    return rows


def main() -> None:
    print(
        json.dumps(
            {
                "schema_version": "erdos451.recursive_gap_replay.v1",
                "arbitrary_subset_replay": exhaustive_arbitrary_subset_replay(),
                "erdos451_rows": actual_451_replay(),
                "interpretation": "Exact finite replay and sorting check; the natural-language induction is the universal proof.",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
