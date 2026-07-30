#!/usr/bin/env python3
"""Exact finite pole-order audit for the all-fixed-rank saddle symbols."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from independent_verify_all_fixed_rank_ordinary_symbol_algorithm import (
    T,
    W,
    X,
    central_kernels,
    determinant_kernels,
    profile_functions,
)


def vanishing_order(expression, variable, point) -> int:
    polynomial = sp.Poly(expression, variable)
    order = 0
    while polynomial.is_zero is False and polynomial.eval(point) == 0:
        polynomial = polynomial.diff()
        order += 1
    return order


def pole_order(expression, variable, point) -> int:
    expression = sp.cancel(expression)
    if expression == 0:
        return -1
    numerator, denominator = sp.fraction(expression)
    return (
        vanishing_order(denominator, variable, point)
        - vanishing_order(numerator, variable, point)
    )


def audit(maximum_rank: int = 5) -> dict[str, object]:
    profiles = profile_functions(maximum_rank)
    normalized = [
        [sp.cancel(value / sp.sqrt(W)) for value in row]
        for row in profiles
    ]

    profile_records = []
    for rank in range(maximum_rank + 1):
        ordinary_orders = [
            pole_order(normalized[index][rank], X, sp.Rational(1, 2))
            for index in range(3)
        ]
        expected = 3 * rank
        if ordinary_orders != [expected] * 3:
            raise AssertionError("unexpected profile pole order")

        first_difference_orders = [
            pole_order(
                normalized[1][rank] - normalized[0][rank],
                X,
                sp.Rational(1, 2),
            ),
            pole_order(
                normalized[2][rank] - normalized[1][rank],
                X,
                sp.Rational(1, 2),
            ),
        ]
        second_difference_order = pole_order(
            normalized[2][rank]
            - 2 * normalized[1][rank]
            + normalized[0][rank],
            X,
            sp.Rational(1, 2),
        )
        if rank >= 1 and first_difference_orders != [3 * rank - 2] * 2:
            raise AssertionError("unexpected first marked-difference pole")
        if rank >= 2 and second_difference_order != 3 * rank - 4:
            raise AssertionError("unexpected second marked-difference pole")

        profile_records.append(
            {
                "rank": rank,
                "profile_over_sqrtW_poles": ordinary_orders,
                "first_marked_difference_poles": first_difference_orders,
                "second_marked_difference_pole": second_difference_order,
            }
        )

    kernels = determinant_kernels(profiles, maximum_rank)
    central = central_kernels(kernels, maximum_rank)
    kernel_records = []
    for rank in range(2, maximum_rank + 1):
        determinant_order = pole_order(
            kernels[rank].subs(X, sp.Rational(1, 2)),
            T,
            1,
        )
        central_order = pole_order(central[rank], T, 1)
        expected = 3 * rank - 5
        if determinant_order != expected or central_order != expected:
            raise AssertionError("unexpected determinant/central pole order")
        kernel_records.append(
            {
                "rank": rank,
                "determinant_pole_at_half": determinant_order,
                "central_kernel_pole": central_order,
                "expected_3r_minus_5": expected,
            }
        )

    return {
        "schema": "amra.opg1757.saddle-pole-orders-finite.v1",
        "scope": (
            "Exact finite symbolic pole orders. The all-rank valuation "
            "argument must be supplied separately."
        ),
        "maximum_rank": maximum_rank,
        "profile_records": profile_records,
        "kernel_records": kernel_records,
        "status": "finite_exact_pole_audit_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-rank", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_rank), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
