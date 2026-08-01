#!/usr/bin/env python3
"""Exhaustive small-graph guard for same-star reserve energy."""

from __future__ import annotations

from itertools import combinations
from math import isqrt

from verify_opposite_star_reserve_energy import all_graphs, is_zero_pair


def exhaustive_guard(limit: int = 6) -> dict[str, int]:
    graphs = 0
    stars = 0
    leaf_subsets = 0
    for n in range(2, limit + 1):
        for adjacency in all_graphs(n):
            graphs += 1
            degrees = [len(neighbours) for neighbours in adjacency]
            delta = min(degrees)
            kappa = n - 2 * delta
            for b in range(n):
                leaves = [
                    c
                    for c in range(n)
                    if c != b
                    and is_zero_pair(adjacency, b, c)
                    and bool(adjacency[b] & adjacency[c])
                ]
                if not leaves:
                    continue
                stars += 1
                for size in range(1, len(leaves) + 1):
                    for chosen in combinations(leaves, size):
                        ell = len(chosen)
                        present = sum(
                            1
                            for x, y in combinations(chosen, 2)
                            if y in adjacency[x]
                        )
                        missing = ell * (ell - 1) // 2 - present
                        assert missing >= ell * (ell - 1) // 2 - kappa * ell
                        leaf_subsets += 1
    return {
        "graphs": graphs,
        "same_type_stars": stars,
        "leaf_subsets": leaf_subsets,
    }


def weighted_guard(limit: int = 100) -> int:
    checked = 0
    for kappa in range(2, limit + 1):
        for weight in range(1, limit * limit + 1):
            ell_zero = (weight + kappa - 2) // (kappa - 1)
            if ell_zero < 2 * kappa + 2:
                continue
            lower = ell_zero * (ell_zero - 1) // 2 - kappa * ell_zero
            for ell in range(ell_zero, ell_zero + 20):
                actual = ell * (ell - 1) // 2 - kappa * ell
                assert actual >= lower
                checked += 1
    return checked


def closed_form_guard(limit: int = 100) -> int:
    checked = 0
    for kappa in range(limit + 1):
        for q_size in range(limit * limit + 1):
            discriminant = (2 * kappa + 1) ** 2 + 8 * q_size
            ell_cap = (2 * kappa + 1 + isqrt(discriminant)) // 2
            for ell in range(ell_cap + 1, ell_cap + 4):
                lower = ell * (ell - 1) // 2 - kappa * ell
                assert lower > q_size
                checked += 1
    return checked


def main() -> None:
    report = exhaustive_guard()
    weighted = weighted_guard()
    closed_form = closed_form_guard()
    print(
        {
            "schema": "amra.erdos809.same-star-reserve.v1",
            **report,
            "weighted_parameter_checks": weighted,
            "closed_form_checks": closed_form,
            "status": "PASS",
            "scope": "small-graph and arithmetic guards; Erdos #809 remains open",
        }
    )


if __name__ == "__main__":
    main()
