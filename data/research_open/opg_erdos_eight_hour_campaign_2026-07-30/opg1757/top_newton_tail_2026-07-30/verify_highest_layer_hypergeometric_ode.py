#!/usr/bin/env python3
"""Exact certificate for the highest-layer hypergeometric/ODE structure."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction

import sympy as sp


Z = sp.symbols("z")


def hypergeometric_2f0_coefficients(first, second, scale, count):
    result = [sp.S.One]
    for rank in range(count - 1):
        result.append(sp.factor(
            result[-1]
            * scale
            * (rank + first)
            * (rank + second)
            / (rank + 1)
        ))
    return result


def ode_recurrence(coefficients):
    b = [sp.Rational(value) for value in coefficients]
    for rank in range(len(b) - 1):
        previous_one = b[rank - 1] if rank >= 1 else 0
        previous_two = b[rank - 2] if rank >= 2 else 0
        predicted = (
            (54 * rank**2 + 69 * rank + 22) * b[rank]
            - (108 * rank**3 - 27 * rank**2 - 21 * rank - 5)
            * previous_one
            - 6 * (rank - 1) * (3 * rank - 5) * (3 * rank - 4)
            * previous_two
        ) / (6 * (rank + 1))
        if sp.cancel(predicted - b[rank + 1]):
            raise AssertionError("third-order ODE recurrence failed")


def differential_elimination():
    """Reduce the claimed B ODE modulo the second-order U equation."""
    u0, u1 = sp.symbols("u0 u1")
    u2 = sp.factor(
        (u0 / 6 - (6 * Z - 1) * u1) / (6 * Z**2)
    )

    def derivative(expression):
        return sp.factor(
            sp.diff(expression, Z)
            + sp.diff(expression, u0) * u1
            + sp.diff(expression, u1) * u2
        )

    v = u0 - 6 * Z * u1
    b = sp.expand(v**2 - 6 * u0 * u1)
    b1 = derivative(b)
    b2 = derivative(b1)
    b3 = derivative(b2)
    residual = sp.factor(
        54 * Z**4 * (Z + 2) * b3
        + 27 * Z**2 * (10 * Z**2 + 23 * Z - 2) * b2
        + 3 * (76 * Z**3 + 218 * Z**2 - 41 * Z + 2) * b1
        + (12 * Z**2 + 55 * Z - 22) * b
    )
    if residual != 0:
        raise AssertionError("differential elimination did not vanish")
    return True


def audit(maximum_band=100):
    count = maximum_band + 5
    u = hypergeometric_2f0_coefficients(
        sp.Rational(1, 6),
        sp.Rational(-1, 6),
        6,
        count,
    )
    v_direct = hypergeometric_2f0_coefficients(
        sp.Rational(1, 6),
        sp.Rational(5, 6),
        6,
        count,
    )
    v_contiguous = [
        (1 - 6 * rank) * u[rank]
        for rank in range(count)
    ]
    assert v_direct == v_contiguous

    # B=(U-6zU')^2-6UU'.  Coefficients are exact signed highest
    # Laurent layers S_(r+2)=(-1)^(r+2) A_(r+2).
    derivative_u = [
        (rank + 1) * u[rank + 1]
        for rank in range(count - 1)
    ]
    b = []
    for rank in range(maximum_band + 1):
        square = sum(
            v_direct[left] * v_direct[rank - left]
            for left in range(rank + 1)
        )
        mixed = sum(
            u[left] * derivative_u[rank - left]
            for left in range(rank + 1)
        )
        b.append(sp.factor(square - 6 * mixed))
    assert b[:6] == [
        2,
        sp.Rational(22, 3),
        sp.Rational(715, 9),
        sp.Rational(110915, 81),
        sp.Rational(31199245, 972),
        sp.Rational(2766939175, 2916),
    ]
    ode_recurrence(b)
    assert differential_elimination()
    for rank, value in enumerate(b):
        bound = 7 * 6 ** (rank + 1) * math.factorial(rank + 1)
        if not (0 < value <= bound):
            raise AssertionError("explicit entire-function bound failed")

    h_positive = [
        sp.Rational(b[rank], 2 * math.factorial(3 * rank))
        for rank in range(len(b))
    ]
    # Original leading series is H_positive(-z).
    long_leading = []
    signed_h = [
        (-1) ** rank * value
        for rank, value in enumerate(h_positive)
    ]
    for band in range(maximum_band):
        value = -3 * (band + 1) * signed_h[band + 1]
        value -= sum(
            long_leading[index] * signed_h[band - index]
            for index in range(band)
        )
        long_leading.append(sp.factor(value))

    counterexamples = [
        rank
        for rank, value in enumerate(long_leading)
        if value <= 0
    ]
    return {
        "schema": "amra.opg1757.highest-layer-hypergeometric-ode.v1",
        "status": "PASS",
        "U": "_2F_0(1/6,-1/6;;6z)",
        "Q_over_z": "_2F_0(1/6,5/6;;6z)",
        "contiguous_identity": "Q=z*(1-6*theta)*U",
        "exact_differential_elimination": True,
        "explicit_coefficient_bound_checks": len(b),
        "entire_order_upper_bound": "1/2",
        "B_coefficient_recurrence": (
            "6(n+1)b[n+1]=(54n^2+69n+22)b[n]"
            "-(108n^3-27n^2-21n-5)b[n-1]"
            "-6(n-1)(3n-5)(3n-4)b[n-2]"
        ),
        "maximum_redundant_sign_band": maximum_band - 1,
        "long_leading_counterexamples": counterexamples,
        "first_B_coefficients": [str(value) for value in b[:8]],
        "first_long_leading_coefficients": [
            str(value) for value in long_leading[:8]
        ],
        "scope": (
            "Hypergeometric identities, ODE, and recurrence are exact. "
            "The finite long-leading sign scan is not an all-rank proof."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-band", type=int, default=99)
    arguments = parser.parse_args()
    print(json.dumps(
        audit(arguments.maximum_band + 1),
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
