#!/usr/bin/env python3
"""Exact exponent and finite-ledger checks for high-rich concentration."""

from __future__ import annotations

import json
from fractions import Fraction


HIGH_RICH_EXPONENT = Fraction(9, 4)


def ms_mixed_exponent(left: Fraction, right: Fraction) -> Fraction:
    return min(
        Fraction(2, 3) * (left + right),
        2 * left,
        2 * right,
    )


def exponent_ledger(kappa: Fraction, eta: Fraction) -> dict[str, Fraction]:
    return {
        "ms_high_pair": ms_mixed_exponent(
            HIGH_RICH_EXPONENT + eta,
            HIGH_RICH_EXPONENT + eta,
        ),
        "distance_budget": Fraction(3),
        "high_weighted_mass": Fraction(4),
        "hub_mass": Fraction(7) - 3 * kappa,
        "zero_radius_mass": Fraction(6) - 2 * kappa,
        "high_to_hub_gap": 3 * (1 - kappa),
        "zero_to_hub_gap": 1 - kappa,
    }


def finite_weighted_partition(
    *,
    source_size: int,
    plane_count: int,
    incidence_sizes: tuple[int, ...],
    multiplicities: tuple[int, ...],
) -> int:
    if len(incidence_sizes) != len(multiplicities):
        raise ValueError("ledger lengths differ")
    if sum(incidence_sizes) > source_size:
        raise ValueError("concentric incidence sets must be disjoint")
    if any(weight < 0 or weight > plane_count for weight in multiplicities):
        raise ValueError("one merged circle has at most one triple per plane")
    weighted = sum(
        size * weight for size, weight in zip(incidence_sizes, multiplicities)
    )
    if weighted > source_size * plane_count:
        raise AssertionError("weighted partition cap failed")
    return weighted


def audit() -> dict[str, object]:
    checked_ledgers = 0
    for denominator in range(2, 10):
        for numerator in range(1, denominator):
            kappa = Fraction(numerator, denominator)
            eta = Fraction(1, 100)
            ledger = exponent_ledger(kappa, eta)
            if ledger["ms_high_pair"] <= ledger["distance_budget"]:
                raise AssertionError("MS high-pair exponent does not separate")
            if ledger["high_to_hub_gap"] <= 0:
                raise AssertionError("high-rich mass is not negligible")
            if ledger["zero_to_hub_gap"] <= 0:
                raise AssertionError("zero-radius mass is not negligible")
            checked_ledgers += 1

    finite_cases = (
        (100, 7, (31, 29, 20), (7, 4, 6)),
        (53, 11, (13, 17, 19), (11, 8, 3)),
        (20, 3, (20,), (3,)),
    )
    for source_size, planes, sizes, weights in finite_cases:
        finite_weighted_partition(
            source_size=source_size,
            plane_count=planes,
            incidence_sizes=sizes,
            multiplicities=weights,
        )

    return {
        "schema": "amra.erdos1083.high-rich-circle-concentration.v1",
        "status": "PASS",
        "high_rich_exponent": str(HIGH_RICH_EXPONENT),
        "exponent_ledgers": checked_ledgers,
        "finite_partition_cases": len(finite_cases),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
