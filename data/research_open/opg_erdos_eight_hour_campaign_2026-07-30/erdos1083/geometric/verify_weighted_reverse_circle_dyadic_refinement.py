#!/usr/bin/env python3
"""Exact exponent audit for the weighted reverse-circle refinement."""

from __future__ import annotations

import json
from fractions import Fraction


def term_exponents(
    kappa: Fraction, multiplicity: Fraction
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return (
        6 - Fraction(4, 3) * kappa + multiplicity / 3,
        Fraction(72, 11)
        - Fraction(18, 11) * kappa
        + Fraction(2, 11) * multiplicity,
        3 + multiplicity,
        6 - 2 * kappa,
    )


def multiplicity_thresholds(
    kappa: Fraction,
) -> tuple[Fraction, Fraction, Fraction]:
    return (
        3 - 5 * kappa,
        Fraction(5 - 15 * kappa, 2),
        4 - 3 * kappa,
    )


def sharp_threshold(kappa: Fraction) -> Fraction:
    return Fraction(5 - 15 * kappa, 2)


def audit() -> dict[str, object]:
    checked = 0
    for denominator in range(2, 15):
        for numerator in range(1, denominator):
            kappa = Fraction(numerator, denominator)
            hub = 7 - 3 * kappa
            thresholds = multiplicity_thresholds(kappa)
            if thresholds[1] != min(thresholds):
                raise AssertionError("6/11,9/11 threshold is not minimal")
            trial = thresholds[1] - Fraction(1, 1000)
            if max(term_exponents(kappa, trial)) >= hub:
                raise AssertionError("subthreshold multiplicity reaches hub mass")
            checked += 1

    if sharp_threshold(Fraction(1, 5)) != 1:
        raise AssertionError("one-fifth endpoint failed")
    if sharp_threshold(Fraction(1, 3)) != 0:
        raise AssertionError("one-third endpoint failed")
    if sharp_threshold(Fraction(1, 4)) != Fraction(5, 8):
        raise AssertionError("interior threshold failed")

    return {
        "schema": "amra.erdos1083.weighted-reverse-circle-dyadic.v1",
        "status": "PASS",
        "rational_kappa_cases": checked,
        "kappa_one_fifth_threshold": "1",
        "kappa_one_fourth_threshold": "5/8",
        "kappa_one_third_threshold": "0",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
