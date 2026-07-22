#!/usr/bin/env python3
"""Exact finite regression for the all-parameter Mahler formula in the note.

The formula itself is proved algebraically in MAHLER_COEFFICIENT_REDUCTION.md;
this script is only a falsifier for indexing and endpoint arithmetic.
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import factorial
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(
    ROOT / "artifacts/erdos_campaign_20260722_round10_4h/work/mixed"
))

from higher_cartier_mahler_certificates import (  # noqa: E402
    c_polynomial,
    mahler_coefficients,
    oddpart,
    sqrt_product_coefficients,
    v2_fraction,
    v2_integer,
)


def mul(left: list[Fraction], right: list[Fraction], degree: int) -> list[Fraction]:
    answer = [Fraction(0)] * (degree + 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if i + j <= degree:
                answer[i + j] += a * b
    return answer


def inverse_linear_product(r: int, degree: int) -> list[Fraction]:
    answer = [Fraction(1)] + [Fraction(0)] * degree
    for j in range(1, r + 1):
        factor = [Fraction(j) ** k for k in range(degree + 1)]
        answer = mul(answer, factor, degree)
    return answer


def formula_coefficients(m: int) -> list[Fraction]:
    h = sqrt_product_coefficients(
        [j * (j - 1) // 2 for j in range(1, 2 * m + 1)], m
    )
    answer = []
    for r in range(m + 1):
        degree = m - r
        reciprocal = inverse_linear_product(r, degree)
        coefficient = sum(h[k] * reciprocal[degree - k] for k in range(degree + 1))
        answer.append(Fraction(factorial(r)) * coefficient)
    return answer


def main() -> None:
    rows = []
    for m in range(1, 33):
        direct = mahler_coefficients(c_polynomial(m))
        formula = formula_coefficients(m)
        assert direct == formula
        endpoint = -Fraction(factorial(m) * (4 * m * m - 3 * m + 2), 6)
        endpoint_two = Fraction(
            factorial(m - 2) * m
            * (80 * m**5 - 264 * m**4 + 365 * m**3 - 360 * m**2 + 230 * m - 96),
            360,
        ) if m >= 2 else None
        endpoint_three_polynomial = (
            2240 * m**8 - 17136 * m**7 + 53652 * m**6 - 98721 * m**5
            + 137886 * m**4 - 137844 * m**3 + 108388 * m**2
            - 60984 * m + 21024
        )
        endpoint_three = -Fraction(
            factorial(m - 3) * m * endpoint_three_polynomial, 45360
        ) if m >= 3 else None
        assert direct[m] == factorial(m)
        if m >= 2:
            assert direct[m - 1] == endpoint
            assert direct[m - 2] == endpoint_two
        if m >= 3:
            assert direct[m - 3] == endpoint_three
        if m % 4 == 0 and m // 4 % 2 == 1:
            target = m - 2 * oddpart(m) - v2_integer(factorial(oddpart(m)))
            assert v2_fraction(direct[m]) >= target + 1
            assert v2_fraction(direct[m - 1]) >= target + 1
            assert v2_fraction(direct[m - 2]) >= target + 1
            assert v2_fraction(direct[m - 3]) >= target + 1
        rows.append({"m": m, "coefficients_checked": m + 1})
    print(json.dumps({
        "schema": "amra.erdos686.mahler-coefficient-reduction.v1",
        "status": "PASS",
        "rows": rows,
        "scope_warning": "Finite regression only; the displayed formula has a separate algebraic proof.",
    }, indent=2))


if __name__ == "__main__":
    main()
