#!/usr/bin/env python3
"""Exact audit of the leading long-recurrence log derivative."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction

import sympy as sp


def reciprocal_series(values: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0)] * len(values)
    result[0] = 1 / values[0]
    for degree in range(1, len(values)):
        result[degree] = -sum(
            values[index] * result[degree - index]
            for index in range(1, degree + 1)
        ) / values[0]
    return result


def audit(maximum_rank: int = 120, continued_fraction_depth: int = 12):
    p = [Fraction(0)] * (maximum_rank + 4)
    q = [Fraction(0)] * (maximum_rank + 4)
    p[1] = Fraction(1, 6)
    for rank in range(1, maximum_rank + 3):
        if rank > 1:
            previous = rank - 1
            p[rank] = p[previous] * Fraction(
                (6 * previous + 3)
                * (6 * previous + 1)
                * (6 * previous - 1),
                9 * (2 * previous + 2) * (2 * previous + 1),
            )
        q[rank] = p[rank] * Fraction(6 * rank, 6 * rank - 5)

    signed_layers = [Fraction(0)] * (maximum_rank + 4)
    for central_rank in range(2, maximum_rank + 4):
        signed_layers[central_rank] = (
            sum(
                q[left] * q[central_rank - left]
                for left in range(1, central_rank)
            )
            + 6 * (central_rank - 1) * p[central_rank - 1]
            - 3
            * (central_rank - 1)
            * sum(
                p[left] * p[central_rank - 1 - left]
                for left in range(1, central_rank - 1)
            )
        )
        if signed_layers[central_rank] <= 0:
            raise AssertionError("highest Laurent layer lost positivity")

    h = [
        signed_layers[rank + 2] / (2 * math.factorial(3 * rank))
        for rank in range(maximum_rank + 2)
    ]
    if h[:2] != [Fraction(1), Fraction(11, 18)]:
        raise AssertionError("initial leading coefficients changed")

    recurrence_records = []
    for rank in range(maximum_rank):
        middle = (
            162 * rank**3
            + 675 * rank**2
            + 885 * rank
            + 361
        )
        upper = (
            9
            * (rank + 2) ** 2
            * (3 * rank + 4)
            * (3 * rank + 5)
            * (6 * rank + 5)
        )
        residual = (
            2 * (6 * rank + 11) * h[rank]
            - middle * h[rank + 1]
            + upper * h[rank + 2]
        )
        if residual:
            raise AssertionError("second-order h recurrence failed")
        if rank >= 0:
            ratio = h[rank + 2] / h[rank + 1]
            if ratio >= Fraction(1, (rank + 1) ** 2):
                raise AssertionError("entire-function ratio bound failed")
        if rank < 8:
            recurrence_records.append(
                {
                    "rank": rank,
                    "h_rank": str(h[rank]),
                    "h_next": str(h[rank + 1]),
                    "h_next_ratio": str(h[rank + 1] / h[rank]),
                }
            )

    # H(z)=sum (-1)^j h_j z^j and G=-3zH'/H.
    ordinary_leading = [
        (-1) ** rank * h[rank] for rank in range(maximum_rank + 1)
    ]
    logarithmic = [Fraction(0)] * (maximum_rank + 1)
    for degree in range(1, maximum_rank + 1):
        logarithmic[degree] = (
            -3 * degree * ordinary_leading[degree]
            - sum(
                ordinary_leading[index]
                * logarithmic[degree - index]
                for index in range(1, degree)
            )
        )
        if logarithmic[degree] <= 0:
            raise AssertionError("finite logarithmic coefficient failed")

    # Redundant Stieltjes evidence for G_(n+1)/(3G_1).
    normalized_moments = [
        logarithmic[degree + 1] / logarithmic[1]
        for degree in range(maximum_rank - 1)
    ]
    stieltjes_coefficients = []
    current = normalized_moments
    for _ in range(continued_fraction_depth):
        inverse = reciprocal_series(current)
        coefficient = -inverse[1]
        if coefficient <= 0:
            raise AssertionError("finite S-fraction coefficient failed")
        stieltjes_coefficients.append(coefficient)
        current = [
            -inverse[degree + 1] / coefficient
            for degree in range(len(inverse) - 1)
        ]

    hankel_records = []
    for size in range(1, 8):
        matrix = sp.Matrix(
            [
                [
                    sp.Rational(
                        logarithmic[row + column + 1].numerator,
                        logarithmic[row + column + 1].denominator,
                    )
                    for column in range(size)
                ]
                for row in range(size)
            ]
        )
        determinant = sp.factor(matrix.det())
        if determinant <= 0:
            raise AssertionError("finite Hankel determinant failed")
        hankel_records.append(
            {"size": size, "determinant": str(determinant)}
        )

    # Symbolic algebra behind the recurrence and the order bound.
    rank = sp.symbols("rank", integer=True, nonnegative=True)
    middle = 162 * rank**3 + 675 * rank**2 + 885 * rank + 361
    upper = (
        9
        * (rank + 2) ** 2
        * (3 * rank + 4)
        * (3 * rank + 5)
        * (6 * rank + 5)
    )
    order_margin = sp.factor(upper - (rank + 1) ** 2 * middle)
    expected_margin = (
        324 * rank**5
        + 2808 * rank**4
        + 9294 * rank**3
        + 14726 * rank**2
        + 11173 * rank
        + 3239
    )
    if sp.expand(order_margin - expected_margin):
        raise AssertionError("symbolic order margin failed")

    # Independent differential derivation.  For
    # S=(F-6zF')^2-6FF' and
    # 36z^2F''+(36z-6)F'-F=0, the quadratic vector
    # (F^2,FF',F'^2) has a first-order 3-by-3 system.
    z = sp.symbols("z")
    second_coefficient = (1 - 6 * z) / (6 * z**2)
    zeroth_coefficient = 1 / (36 * z**2)
    system = sp.Matrix(
        [
            [0, 2, 0],
            [zeroth_coefficient, second_coefficient, 1],
            [0, 2 * zeroth_coefficient, 2 * second_coefficient],
        ]
    )
    row = sp.Matrix([[1, -12 * z - 6, 36 * z**2]])
    derivative_rows = [row]
    for _ in range(3):
        row = row.applyfunc(lambda value: sp.diff(value, z)) + row * system
        derivative_rows.append(row.applyfunc(sp.factor))
    ode_coefficients = [
        12 * z**2 + 55 * z - 22,
        3 * (76 * z**3 + 218 * z**2 - 41 * z + 2),
        27 * z**2 * (10 * z**2 + 23 * z - 2),
        54 * z**4 * (z + 2),
    ]
    ode_row = sum(
        (
            ode_coefficients[index] * derivative_rows[index]
            for index in range(4)
        ),
        sp.zeros(1, 3),
    )
    if any(sp.cancel(value) for value in ode_row):
        raise AssertionError("symmetric-square differential equation failed")

    return {
        "schema": "amra.opg1757.long-leading-log-derivative.v1",
        "scope": (
            "Exact coefficient recurrence and finite positivity audit. "
            "Finite G, Hankel, and S-fraction checks are evidence, not an "
            "all-rank PF proof."
        ),
        "maximum_exact_rank": maximum_rank,
        "h_recurrence": (
            "9(n+2)^2(3n+4)(3n+5)(6n+5)h_(n+2)"
            "-(162n^3+675n^2+885n+361)h_(n+1)"
            "+2(6n+11)h_n=0"
        ),
        "symmetric_square_ode": (
            "54z^4(z+2)S'''+27z^2(10z^2+23z-2)S''"
            "+3(76z^3+218z^2-41z+2)S'"
            "+(12z^2+55z-22)S=0"
        ),
        "entire_order_margin": str(order_margin),
        "recurrence_records": recurrence_records,
        "first_logarithmic_coefficients": [
            str(value) for value in logarithmic[1:11]
        ],
        "positive_logarithmic_coefficients_checked": maximum_rank,
        "positive_stieltjes_coefficients": [
            str(value) for value in stieltjes_coefficients
        ],
        "positive_hankel_determinants": hankel_records,
        "status": "exact_leading_log_derivative_audit_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-rank", type=int, default=120)
    parser.add_argument("--continued-fraction-depth", type=int, default=12)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_rank, args.continued_fraction_depth),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
