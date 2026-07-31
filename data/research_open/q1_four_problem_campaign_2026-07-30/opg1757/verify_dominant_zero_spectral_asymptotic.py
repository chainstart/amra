#!/usr/bin/env python3
"""Exact rational audit of the sharpened dominant-zero asymptotic."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
INHERITED = (
    HERE.parents[1]
    / "opg_erdos_eight_hour_campaign_2026-07-30"
    / "opg1757"
    / "top_newton_tail_2026-07-30"
)
sys.path.insert(0, str(INHERITED))

from verify_long_recurrence_leading_reduction import (  # noqa: E402
    falling_leading_coefficients,
)


LEFT = Fraction(1961, 1000)
RIGHT = Fraction(1962, 1000)
ZERO_FREE_RADIUS = Fraction(21, 10)
RELATIVE_RATE = Fraction(327, 350)


def partial_sum(coefficients, value: Fraction, degree: int) -> Fraction:
    return sum(
        coefficients[index] * value**index
        for index in range(degree + 1)
    )


def first_threshold(bound: Fraction) -> int:
    for exponent in range(1, 1000):
        if 63 * RELATIVE_RATE**exponent < bound:
            return exponent
    raise AssertionError("threshold search range exhausted")


def audit() -> dict[str, object]:
    coefficients = falling_leading_coefficients(12)
    if coefficients[:4] != [
        Fraction(1),
        -Fraction(11, 18),
        Fraction(143, 2592),
        -Fraction(3169, 1679616),
    ]:
        raise AssertionError("leading H coefficients changed")

    # From degree one onward the alternating terms decrease at both
    # endpoints.  The only non-uniform first ratio is checked exactly;
    # the inherited recurrence gives lambda_(r+1)/lambda_r < 1/r^2
    # for every r>=1.
    first_tail_ratio = (
        abs(coefficients[2] / coefficients[1]) * RIGHT
    )
    if first_tail_ratio >= 1:
        raise AssertionError("alternating-tail decrease failed")
    if RIGHT >= 2:
        raise AssertionError("uniform r>=2 decrease constant failed")

    left_lower = partial_sum(coefficients, LEFT, 5)
    right_upper = partial_sum(coefficients, RIGHT, 4)
    if left_lower <= 0 or right_upper >= 0:
        raise AssertionError("rational dominant-zero bracket failed")

    if RIGHT / ZERO_FREE_RADIUS != RELATIVE_RATE:
        raise AssertionError("relative convergence rate changed")
    thresholds = {
        "relative_error_lt_1": first_threshold(Fraction(1)),
        "relative_error_lt_1_over_2": first_threshold(Fraction(1, 2)),
        "relative_error_lt_1_over_10": first_threshold(Fraction(1, 10)),
        "relative_error_lt_1_over_100": first_threshold(Fraction(1, 100)),
    }
    if thresholds != {
        "relative_error_lt_1": 61,
        "relative_error_lt_1_over_2": 72,
        "relative_error_lt_1_over_10": 95,
        "relative_error_lt_1_over_100": 129,
    }:
        raise AssertionError("explicit convergence thresholds changed")

    return {
        "schema": "amra.opg1757.dominant-zero-spectral-asymptotic.v1",
        "status": "PASS",
        "dominant_zero_interval": ["1961/1000", "1962/1000"],
        "left_odd_partial_lower_bound": str(left_lower),
        "right_even_partial_upper_bound": str(right_upper),
        "other_zero_modulus_lower_bound": "21/10",
        "relative_error_bound": (
            "abs(G_(n-1)/(3*rho^(-n))-1)"
            " < 63*(327/350)^n"
        ),
        "thresholds": thresholds,
        "limit_statements": [
            "lim_(q->infinity) G_(q+1)/G_q = 1/rho",
            "lim_(q->infinity) G_q^(1/(q+1)) = 1/rho",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
