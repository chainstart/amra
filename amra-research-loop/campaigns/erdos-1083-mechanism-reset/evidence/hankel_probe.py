#!/usr/bin/env python3
"""Exact finite Hankel-rank probes for known #1083 signed residuals.

This is route-search evidence only.  It neither proves a uniform rank theorem nor
changes the public distinct-distance exponent.
"""

from fractions import Fraction
import json


def matrix_rank(rows: list[list[int]]) -> int:
    a = [[Fraction(x) for x in row] for row in rows]
    rank = 0
    cols = len(a[0]) if a else 0
    for col in range(cols):
        pivot = next((r for r in range(rank, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [x / scale for x in a[rank]]
        for r in range(len(a)):
            if r != rank and a[r][col]:
                scale = a[r][col]
                a[r] = [x - scale * y for x, y in zip(a[r], a[rank])]
        rank += 1
    return rank


def moments(poly: dict[int, int], degree: int) -> list[int]:
    return [sum(coefficient * exponent**k for exponent, coefficient in poly.items()) for k in range(degree + 1)]


def hankel_profile(poly: dict[int, int]) -> list[int]:
    support = len(poly)
    ms = moments(poly, 2 * support)
    return [matrix_rank([[ms[i + j] for j in range(h)] for i in range(h)]) for h in range(1, support + 1)]


def q_s(s: int) -> dict[tuple[int, int], int]:
    # Q_S=x+y-xy+xy^S+x^Sy.  Project with base > S so exponents are injective.
    base = s + 2
    terms = {(1, 0): 1, (0, 1): 1, (1, 1): -1, (1, s): 1, (s, 1): 1}
    return {i + base * j: coefficient for (i, j), coefficient in terms.items()}


def main() -> None:
    fixed_escape = {0: 1, 5: -1, 8: 1, 10: 1, 13: -1, 18: 1}
    result = {
        "schema": "amra.erdos1083.hankel-probe.v1",
        "evidence_level": 6,
        "scope": "finite exact route-search probe only",
        "fixed_five_point_escape": {
            "support": len(fixed_escape),
            "augmentation": sum(fixed_escape.values()),
            "hankel_rank_profile": hankel_profile(fixed_escape),
        },
        "simultaneous_positive_QS": {
            str(s): {
                "support": len(q_s(s)),
                "augmentation": sum(q_s(s).values()),
                "hankel_rank_profile": hankel_profile(q_s(s)),
            }
            for s in range(4, 13)
        },
        "interpretation": "Known signed escapes have full eventual Hankel rank equal to support size; this supports testing reconstruction but supplies no common-mask complexity bound.",
        "public_exponent_changed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
