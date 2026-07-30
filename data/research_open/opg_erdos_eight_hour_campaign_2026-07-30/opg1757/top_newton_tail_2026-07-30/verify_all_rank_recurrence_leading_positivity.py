#!/usr/bin/env python3
"""Exact certificate for all-rank leading long-band positivity.

The script checks the finite prefix and every rational constant in the
Rouche/Jensen argument.  The complex-analytic implications are proved in
the accompanying theorem, not by numerical root finding.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction

from verify_long_recurrence_leading_reduction import (
    falling_leading_coefficients,
    recurrence_leading_coefficients,
)


def coefficient_majorant(rank: int) -> Fraction:
    return Fraction(
        6**rank * math.factorial(rank + 1),
        math.factorial(3 * rank),
    )


def geometric_tail(radius: Fraction, start: int = 4) -> Fraction:
    first = coefficient_majorant(start) * radius**start
    ratio = Fraction(
        6 * radius.numerator * (start + 2),
        radius.denominator
        * (3 * start + 1)
        * (3 * start + 2)
        * (3 * start + 3),
    )
    return first / (1 - ratio)


def audit() -> dict[str, object]:
    radius = Fraction(21, 10)
    lam1 = Fraction(11, 18)
    lam2 = Fraction(143, 2592)
    lam3 = Fraction(3169, 1679616)

    ratio_at_four = Fraction(9, 325)
    computed_ratio = Fraction(
        6 * radius.numerator * 6,
        radius.denominator * 13 * 14 * 15,
    )
    assert computed_ratio == ratio_at_four

    rouche_tail = (
        lam2 * radius**2
        + lam3 * radius**3
        + geometric_tail(radius)
    )
    expected_rouche_tail = Fraction(
        14448059591,
        54058752000,
    )
    assert rouche_tail == expected_rouche_tail
    rouche_margin = lam1 * radius - 1 - rouche_tail
    assert rouche_margin == Fraction(
        868586809,
        54058752000,
    )
    assert rouche_margin > 0

    radius_two = Fraction(2)
    h_two_upper = (
        1
        - 2 * lam1
        + 4 * lam2
        - 8 * lam3
        + geometric_tail(radius_two)
    )
    assert h_two_upper == Fraction(
        -11562637,
        1023096096,
    )
    assert h_two_upper < 0

    binomial_lower = sum(
        Fraction(math.comb(100, index), 20**index)
        for index in range(5)
    )
    assert binomial_lower == Fraction(403809, 6400)
    assert binomial_lower > 63

    falling = falling_leading_coefficients(99)
    recurrence = recurrence_leading_coefficients(falling)
    assert len(recurrence) == 99
    nonpositive = [
        index
        for index, value in enumerate(recurrence)
        if value <= 0
    ]
    assert not nonpositive

    return {
        "schema": (
            "amra.opg1757.all-rank-recurrence-leading-positivity.v1"
        ),
        "status": "PASS",
        "finite_prefix": {
            "minimum_band": 0,
            "maximum_band": 98,
            "nonpositive_bands": nonpositive,
        },
        "rouche": {
            "radius": str(radius),
            "absolute_tail_upper": str(rouche_tail),
            "strict_margin": str(rouche_margin),
            "h_at_two_upper": str(h_two_upper),
            "conclusion": (
                "one zero rho in |z|<21/10, with 0<rho<2"
            ),
        },
        "jensen_tail": {
            "zero_count_bound": "N(s) < 15*sqrt(s)",
            "other_zero_power_sum_bound": (
                "sum_{k != 1}|rho_k|^(-n) < "
                "63*(21/10)^(-n)"
            ),
            "analytic_start_index": 100,
            "binomial_lower_bound": str(binomial_lower),
        },
        "conclusion": (
            "G_q>0 for every q>=0; deg(g_q)=3q+2"
        ),
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
