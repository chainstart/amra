#!/usr/bin/env python3
"""Finite regression for the #635 full lower-fibre canonical expansion lemma."""

from __future__ import annotations

import argparse
import json
from itertools import combinations


def valuation_oddpart(value: int) -> tuple[int, int]:
    valuation = 0
    while value % 2 == 0:
        valuation += 1
        value //= 2
    return valuation, value


def conflict(left: int, right: int) -> bool:
    difference = abs(left - right)
    return difference >= 2 and left % difference == 0 and right % difference == 0


def lower(value: int) -> int:
    valuation, oddpart = valuation_oddpart(value)
    return (2**valuation - 1) * oddpart


def upper(value: int) -> int:
    valuation, oddpart = valuation_oddpart(value)
    return (2**valuation + 1) * oddpart


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=500)
    args = parser.parse_args()
    vertices = [
        value for value in range(2, args.max_n + 1, 2)
        if valuation_oddpart(value)[1] > 1
    ]
    fibres: dict[int, list[int]] = {}
    for value in vertices:
        fibres.setdefault(lower(value), []).append(value)
    checked = 0
    failures = []
    for base, fibre in fibres.items():
        independent = [
            value for value in fibre
            if all(not conflict(value, other) for other in fibre if other != value)
        ]
        # Audit every independent sub-fibre, not only the maximal one.
        for size in range(1, len(fibre) + 1):
            for chosen in combinations(fibre, size):
                if any(conflict(x, y) for x, y in combinations(chosen, 2)):
                    continue
                ordered = sorted(chosen, key=lambda value: valuation_oddpart(value)[0])
                candidates = [base] + [upper(value) for value in ordered[1:]]
                checked += 1
                if len(set(candidates)) != size or any(
                    candidate > args.max_n for candidate in candidates
                ):
                    failures.append({
                        "base": base,
                        "chosen": chosen,
                        "candidates": candidates,
                    })
    obstruction = (24, 42, 54)
    obstruction_mapping = {42: lower(42), 24: upper(24), 54: lower(54)}
    assert all(not conflict(x, y) for x, y in combinations(obstruction, 2))
    assert len(set(obstruction_mapping.values())) < len(obstruction)
    same_layer_collisions = 0
    same_layer_failures = []
    for left, right in combinations(vertices, 2):
        a, u = valuation_oddpart(left)
        c, v = valuation_oddpart(right)
        if a != c:
            continue
        if u > v:
            left, right, u, v = right, left, v, u
        canonical_intersection = {lower(left), upper(left)} & {lower(right), upper(right)}
        if not canonical_intersection:
            continue
        same_layer_collisions += 1
        scale = 2**a
        expected = (
            upper(left) == lower(right)
            and u % (scale - 1) == 0
            and v == (scale + 1) * (u // (scale - 1))
            and not conflict(left, right)
        )
        if not expected:
            same_layer_failures.append({
                "left": left, "right": right,
                "canonical_intersection": sorted(canonical_intersection),
            })
    print(json.dumps({
        "status": "PASS" if not failures and not same_layer_failures else "FAIL",
        "scope": "finite regression only; general fibre proof is in REPORT.md",
        "max_n": args.max_n,
        "independent_subfibres_checked": checked,
        "failures": failures,
        "fixed_layer_canonical_path_regression": {
            "collisions_checked": same_layer_collisions,
            "failures": same_layer_failures,
        },
        "canonical_global_injection_counterexample": {
            "vertices": obstruction,
            "naive_mapping": obstruction_mapping,
            "explanation": "U(24)=L(54)=27; proper-divisor neighbours of 54 are needed",
        },
    }, indent=2))


if __name__ == "__main__":
    main()
