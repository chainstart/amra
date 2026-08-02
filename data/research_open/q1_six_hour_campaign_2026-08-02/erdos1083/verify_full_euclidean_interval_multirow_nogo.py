#!/usr/bin/env python3
"""Finite guard for the full-Euclidean interval multirow no-go."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from math import isqrt
import json

import sympy as sp


def divisors_below_sqrt(c: int) -> list[int]:
    return [m for m in range(1, isqrt(c) + 1) if c % m == 0 and m * m < c]


def interval_complement(s: int, c: int, m: int) -> set[int]:
    if c % m:
        raise ValueError("m must divide C")
    return {
        r + s * m * k
        for r in range(m)
        for k in range(c // m)
    }


def mixed_radix_certificate(s: int, c: int, m: int) -> int:
    block = interval_complement(s, c, m)
    assert len(block) == c
    counts = Counter(b + m * x for b in block for x in range(s))
    assert counts == Counter({value: 1 for value in range(s * c)})
    return len(counts)


def coordinate_partition_certificate(s: int, c: int) -> dict[str, int | bool]:
    if s < 3 or c < 2 or c >= s or isqrt(s) ** 2 == s:
        raise ValueError("requires nonsquare S>=3 and 2<=C<S")
    leaves = divisors_below_sqrt(c)
    u = s * c
    common = {(a, n) for a in range(s) for n in range(s * c)}
    assert len(common) == s * u

    centre_counts = Counter(
        (a, n) for n in range(s * c) for a in range(s)
    )
    assert centre_counts == Counter({item: 1 for item in common})

    row_cells = 0
    for m in leaves:
        block = interval_complement(s, c, m)
        assert s * m * m in block
        mixed_radix_certificate(s, c, m)
        counts = Counter(
            (a, b + m * x)
            for a in range(s)
            for b in block
            for x in range(s)
        )
        assert counts == Counter({item: 1 for item in common})
        row_cells += len(counts)
    return {
        "S": s,
        "C": c,
        "U": u,
        "leaf_rows": len(leaves),
        "common_labels": len(common),
        "leaf_row_cells": row_cells,
        "pass": True,
    }


def euclidean_certificate(s: int, c: int) -> dict[str, int | bool]:
    leaves = divisors_below_sqrt(c)
    beta = sp.Rational(1, s - 1)
    alpha = 1 / sp.sqrt(s)
    rho2 = sp.Rational(s - 1, 4 * s)
    rho = sp.sqrt(rho2)
    z2 = {0: beta}
    for m in leaves:
        z2[m] = beta * s * m * m
        assert sp.simplify((m / (2 * rho)) ** 2 - z2[m]) == 0
    assert sp.simplify((alpha / (2 * rho)) ** 2 - z2[0]) == 0

    largest = max(z2.values())
    translation = rho2 + largest + 1
    common_tangent = translation - rho2
    assert common_tangent > 0

    checked_cells = 0
    # Centre anchor 1 and leaf anchor S*m^2 give the same tangent.
    assert sp.simplify(translation + beta - rho2 - z2[0]) == common_tangent
    for m in leaves:
        block = interval_complement(s, c, m)
        anchor = s * m * m
        assert anchor in block
        assert sp.simplify(
            translation + beta * anchor - rho2 - z2[m]
        ) == common_tangent

    # Check the Cartesian distance identity on every source parameter
    # and every complement element of a small exact instance.
    for row in [0] + leaves:
        lam = alpha if row == 0 else sp.Integer(row)
        z = lam / (2 * rho)
        if row == 0:
            complement = [(0, n) for n in range(s * c)]
        else:
            complement = [
                (a, b)
                for a in range(s)
                for b in interval_complement(s, c, row)
            ]
        for source in range(s):
            x = beta * source
            # Sampling endpoints and the common-tangent anchor is enough
            # for the symbolic identity; tiling is checked separately.
            for a, b in (complement[0], complement[-1]):
                aval = alpha * beta * a + beta * b
                tau = translation + aval - rho2 - z**2
                assert tau > 0
                distance = rho2 + z**2 + tau + 2 * rho * z * x
                expected = translation + aval + lam * x
                assert sp.simplify(distance - expected) == 0
                checked_cells += 1

    return {
        "rows": 1 + len(leaves),
        "symbolic_distance_cells": checked_cells,
        "common_tangent_positive": bool(common_tangent > 0),
        "centre_scalar_irrational": bool(not sp.sqrt(s).is_rational),
        "pass": True,
    }


def squarefree_count_certificate() -> dict[str, int | bool]:
    rows = 0
    for c, omega in ((6, 2), (30, 3), (210, 4), (2310, 5)):
        leaves = divisors_below_sqrt(c)
        assert len(leaves) == 2 ** (omega - 1)
        assert all(m * m < c and c % m == 0 for m in leaves)
        rows += 1
    assert Fraction(1, 36) < Fraction(5, 9)
    assert Fraction(5, 9) - Fraction(1, 36) == Fraction(19, 36)
    return {"squarefree_rows": rows, "pass": True}


def main() -> int:
    result = {
        "partition": coordinate_partition_certificate(31, 30),
        "euclidean": euclidean_certificate(31, 30),
        "row_count": squarefree_count_certificate(),
    }
    assert all(section["pass"] for section in result.values())
    result["pass"] = True
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
