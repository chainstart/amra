#!/usr/bin/env python3
"""Independent reconstruction of the OPG third-active reduction.

This audit deliberately does not import ``third_active_workbench``.  Its
finite rows come straight from the original pooled Newton enumerator, and
its symbolic endpoint check comes straight from the frozen K6/K7 kernels.
Finite checks are reported only as checks, never as a universal sign proof.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import sympy as sp


OLD_LANE = (
    Path(__file__).resolve().parents[2]
    / "q1_eight_hour_campaign_2026-07-29"
    / "opg1757"
)
sys.path.insert(0, str(OLD_LANE))

from six_page_union_formula import k6_coefficients  # noqa: E402
from seven_page_union_formula import k7_coefficients  # noqa: E402
from tp2_barrier_search import pooled_t_newton_rows  # noqa: E402


@lru_cache(maxsize=None)
def pooled_rows(s: int, maximum_beta: int) -> dict[int, dict[int, int]]:
    rows: dict[int, dict[int, int]] = {}
    for order, degree, coefficient in pooled_t_newton_rows(s, maximum_beta):
        rows.setdefault(int(order), {})[int(degree)] = int(coefficient)
    return rows


def c_row(q: int, t: int) -> list[Fraction]:
    """Reconstruct C_q(t,z) directly from the pooled B_p definition."""

    p = 2 * t - 5 - q
    if p < 0:
        return [Fraction(0)] * (2 * q + 1)
    coefficients = pooled_rows(t, 2 * p + 2 * q).get(p, {})
    return [
        Fraction(coefficients.get(2 * p + r, 0), math.factorial(p))
        * Fraction(t) ** (2 * t - 2 - 2 * p - r)
        for r in range(2 * q + 1)
    ]


def full_forward_row(q: int) -> list[Fraction]:
    """Compute Delta^(floor(q/2)+2) C_q(4,z), including zero terms."""

    j = q // 2 + 2
    result = [Fraction(0)] * (2 * q + 1)
    for i in range(j + 1):
        multiplier = (-1) ** (j - i) * math.comb(j, i)
        result = [
            left + multiplier * right
            for left, right in zip(result, c_row(q, 4 + i))
        ]
    return result


def collapsed_row(q: int) -> list[Fraction]:
    """Compute the claimed three surviving boundary terms only."""

    m = q // 2
    j = m + 2
    terms = (
        (1, m + 6),
        (-j, m + 5),
        (math.comb(j, 2), m + 4),
    )
    result = [Fraction(0)] * (2 * q + 1)
    for multiplier, t in terms:
        result = [
            left + multiplier * right
            for left, right in zip(result, c_row(q, t))
        ]
    return result


def divide_by_one_plus_z(coefficients: list[Fraction], times: int) -> list[Fraction]:
    result = list(coefficients)
    for _ in range(times):
        quotient = [result[0]]
        for degree in range(1, len(result) - 1):
            quotient.append(result[degree] - quotient[-1])
        if quotient[-1] != result[-1]:
            raise AssertionError("the independently reconstructed factor is absent")
        result = quotient
        while len(result) > 1 and result[-1] == 0:
            result.pop()
    return result


def reduced_row(parity: str, s: int) -> list[Fraction]:
    q = 2 * (s - 6) + (1 if parity == "odd" else 0)
    exponent = 2 * s - (16 if parity == "odd" else 18)
    return divide_by_one_plus_z(full_forward_row(q), exponent)


def multiply_quadratic(row: list[Fraction], a: int, b: int) -> list[Fraction]:
    factor = [Fraction(a * a), Fraction(2 * a * b), Fraction(b * b)]
    result = [Fraction(0)] * (len(row) + 2)
    for i, value in enumerate(row):
        for j, coefficient in enumerate(factor):
            result[i + j] += value * coefficient
    return result


def transport(parity: str, s: int) -> list[Fraction]:
    current = reduced_row(parity, s)
    following = reduced_row(parity, s + 1)
    page = 6 if parity == "odd" else 7
    shifted = multiply_quadratic(current, s, page)
    length = max(len(following), len(shifted))
    return [
        (following[i] if i < len(following) else 0)
        - (shifted[i] if i < len(shifted) else 0)
        for i in range(length)
    ]


EXPECTED_BASES = {
    1: (8, 16, 16),
    2: (360, 1184, 1872, 1392, 464),
    3: (24044, 94336, 170092, 175968, 109396, 38752, 6196),
    4: (
        741044, 3941792, 9854608, 14916288, 14852376,
        9939424, 4370752, 1159072, 143076,
    ),
    5: (
        14207112, 88847152, 257302408, 454890592, 543963464,
        459988784, 278846744, 119841856, 35017744, 6296512, 530304,
    ),
    6: (
        577839736, 4411248016, 15850877164, 35459528480,
        55004522340, 62337009504, 52951321624, 33998782656,
        16397772960, 5802781200, 1432657948, 221972128, 16350372,
    ),
}


def symbolic_certificate() -> dict[str, str]:
    """Check page numbers, normalization constants, and z=-1 kernels."""

    s = sp.symbols("s", integer=True, positive=True)
    m = s - 6
    assert [2 * t - 5 - (2 * m + 1) for t in (s, s - 1, s - 2)] == [6, 4, 2]
    assert [2 * t - 5 - 2 * m for t in (s, s - 1, s - 2)] == [7, 5, 3]

    odd_constants = (
        sp.Rational(60, math.factorial(6)),
        -(s - 4) * sp.Rational(24, math.factorial(4)),
        sp.binomial(s - 4, 2) * sp.Rational(4, math.factorial(2)),
    )
    even_constants = (
        sp.Rational(84, math.factorial(7)),
        -(s - 4) * sp.Rational(40, math.factorial(5)),
        sp.binomial(s - 4, 2) * sp.Rational(12, math.factorial(3)),
    )
    assert tuple(map(sp.simplify, odd_constants)) == (
        sp.Rational(1, 12), -(s - 4), (s - 4) * (s - 5),
    )
    assert tuple(map(sp.simplify, even_constants)) == (
        sp.Rational(1, 60), -(s - 4) / 3, (s - 4) * (s - 5),
    )

    beta = -sp.S.One / s
    k6 = sp.factor(sum(c * beta**i for i, c in enumerate(k6_coefficients(s))))
    k7 = sp.factor(sum(c * beta**i for i, c in enumerate(k7_coefficients(s))))
    expected6 = (
        (s - 7) * (s - 6) * (s - 5) ** 2 * (s - 4) ** 2
        * (s - 3) * (s - 2) / s**8
    )
    expected7 = (
        (s - 8) * (s - 7) * (s - 6) ** 2 * (s - 5) ** 2
        * (s - 4) ** 2 * (s - 3) * (s - 2) / s**10
    )
    assert sp.factor(k6 - expected6) == 0
    assert sp.factor(k7 - expected7) == 0
    return {"K6_at_minus_1_over_s": str(k6), "K7_at_minus_1_over_s": str(k7)}


def audit(maximum_q: int = 20, maximum_s: int = 20) -> dict[str, object]:
    symbolic = symbolic_certificate()
    row_coefficients = 0
    for q in range(1, maximum_q + 1):
        full = full_forward_row(q)
        assert full == collapsed_row(q)
        assert all(value > 0 for value in full)
        row_coefficients += len(full)
    for q, expected in EXPECTED_BASES.items():
        assert full_forward_row(q) == list(map(Fraction, expected))

    transport_coefficients = 0
    for parity, first in (("odd", 8), ("even", 9)):
        for s in range(first, maximum_s + 1):
            remainder = transport(parity, s)
            assert all(value > 0 for value in remainder)
            transport_coefficients += len(remainder)
    return {
        "status": "INDEPENDENT FINITE/SYMBOLIC AUDIT PASS",
        "maximum_q": maximum_q,
        "maximum_s": maximum_s,
        "row_coefficients_checked": row_coefficients,
        "transport_coefficients_checked": transport_coefficients,
        "six_exact_bases_checked": True,
        "symbolic": symbolic,
        "firewall": "transport positivity beyond the finite range remains open",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
