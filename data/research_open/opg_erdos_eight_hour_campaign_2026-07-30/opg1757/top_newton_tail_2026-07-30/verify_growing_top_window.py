#!/usr/bin/env python3
"""Exact finite audit for the growing top Newton-window theorem."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from verify_top_six_newton_tail import (
    K,
    S,
    direct_newton_row,
    profile,
)


def four_stirling(n: int, q: int) -> int:
    """Coefficient of (s-4)_q in s^n."""
    if q < 0 or q > n:
        return 0
    row = [0] * (n + 1)
    row[0] = 4**0
    for power in range(1, n + 1):
        updated = [0] * (n + 1)
        for index in range(power + 1):
            stay = (index + 4) * row[index]
            enter = row[index - 1] if index else 0
            updated[index] = stay + enter
        row = updated
    return row[q]


def four_stirling_table(maximum_n: int) -> list[list[int]]:
    rows = [[1]]
    for n in range(1, maximum_n + 1):
        previous = rows[-1]
        row = [0] * (n + 1)
        for q in range(n + 1):
            row[q] = (
                (q + 4) * (previous[q] if q < len(previous) else 0)
                + (previous[q - 1] if q else 0)
            )
        rows.append(row)
    return rows


def exact_c_polynomial(page_count: int) -> sp.Expr:
    determinant = sp.S.Zero
    for left in range(page_count + 1):
        determinant += (
            profile(1, left) * profile(1, page_count - left)
            - profile(0, left) * profile(2, page_count - left)
        )
    return sp.expand(
        sp.factorial(page_count)
        * determinant
        / (2 * page_count * (page_count - 1))
    )


def audit(
    maximum_stirling_n: int = 48,
    maximum_page_count: int = 10,
) -> dict[str, object]:
    table = four_stirling_table(maximum_stirling_n)
    recurrence_checks = 0
    bound_checks = 0
    for n in range(maximum_stirling_n + 1):
        assert table[n][n] == 1
        for q, value in enumerate(table[n]):
            assert value == four_stirling(n, q)
            recurrence_checks += 1
        for depth in range(n // 4 + 1):
            value = table[n][n - depth]
            lower = sp.Rational(n ** (2 * depth), 8**depth * sp.factorial(depth))
            upper = sp.Rational(
                (n + 4) ** (2 * depth),
                2**depth * sp.factorial(depth),
            )
            assert lower <= value <= upper
            bound_checks += 1

    linearity_records = []
    for page_count in range(2, maximum_page_count + 1):
        polynomial = sp.Poly(exact_c_polynomial(page_count), S)
        degree = 2 * page_count - 4
        newton_row = direct_newton_row(page_count)
        for depth in range(degree + 1):
            reconstructed = sp.S.Zero
            for ordinary_depth in range(depth + 1):
                coefficient = polynomial.coeff_monomial(
                    S ** (degree - ordinary_depth)
                )
                reconstructed += (
                    coefficient
                    * table[degree - ordinary_depth][degree - depth]
                )
            assert reconstructed == sp.Rational(
                newton_row[degree - depth],
                sp.factorial(degree - depth),
            )
        linearity_records.append(
            {
                "k": page_count,
                "degree": degree,
                "identity_checks": degree + 1,
            }
        )

    return {
        "schema": "amra.opg1757.growing-top-window.v1",
        "scope": (
            "Finite exact audit of the 4-Stirling recurrence, the two "
            "combinatorial bounds, and the monomial-to-Newton linearity "
            "identity. The uniform coefficient-norm lemma is proved "
            "in the accompanying human argument."
        ),
        "maximum_stirling_n": maximum_stirling_n,
        "recurrence_checks": recurrence_checks,
        "bound_checks": bound_checks,
        "linearity_records": linearity_records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-stirling-n", type=int, default=48)
    parser.add_argument("--maximum-page-count", type=int, default=10)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_stirling_n, args.maximum_page_count),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
