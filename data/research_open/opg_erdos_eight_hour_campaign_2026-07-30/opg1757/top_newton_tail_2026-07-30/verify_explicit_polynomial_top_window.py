#!/usr/bin/env python3
"""Exact ledger and growth checks for the explicit one-eighth window."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from verify_ordinary_subleading_symbol import (
    ordinary_coefficient,
    profile_polynomial,
)


K = sp.symbols("k")
PROFILE_BASE = 2**16
ORDINARY_BASE = 2**320
SYMBOL_POWER = 6
ETA_DENOMINATOR = 8


def ordinary_polynomial(depth: int) -> sp.Poly:
    """Reconstruct b_(k,depth), retaining two interpolation holdouts."""
    start = max(2, (depth + 5) // 2)
    points = []
    for page_count in range(start, start + depth + 3):
        value = ordinary_coefficient(page_count, depth)
        points.append(
            (
                page_count,
                sp.Rational(value.numerator, value.denominator),
            )
        )
    polynomial = sp.Poly(
        sp.interpolate(points[: depth + 1], K),
        K,
    )
    assert polynomial.degree() == depth
    assert all(
        polynomial.eval(page_count) == value
        for page_count, value in points[depth + 1 :]
    )
    return polynomial


def first_defect(depth: int) -> sp.Rational:
    return sp.Rational(
        22 * depth**3
        + 147 * depth**2
        + 161 * depth
        - 258,
        36,
    )


def ledger_checks(maximum_index: int = 256) -> dict[str, int]:
    """Finite sanity checks of the elementary inequalities used in proof."""
    difference_checks = 0
    for loss in range(1, maximum_index + 1):
        moment = (2**11 * loss**5) ** loss
        previous = (
            (2**11 * (loss - 1) ** 5) ** (loss - 1)
            if loss > 1
            else 1
        )
        difference = moment + 2 * previous
        bound = (2**14 * (loss + 1) ** 5) ** loss
        assert difference <= bound
        difference_checks += 1

    offset_checks = 0
    for depth in range(1, maximum_index + 1):
        raw = (2**18 * (depth + 5) ** 6) ** (depth + 4)
        weighted = ORDINARY_BASE**depth * depth ** (
            SYMBOL_POWER * depth
        )
        assert raw <= weighted
        offset_checks += 1

    return {
        "difference_ledger_checks": difference_checks,
        "fixed_offset_absorption_checks": offset_checks,
    }


def profile_norm_checks(maximum_loss: int = 24) -> int:
    checks = 0
    for loss in range(1, maximum_loss + 1):
        bound = (PROFILE_BASE * (loss + 1) ** 5) ** loss
        for profile_index in range(3):
            polynomial = profile_polynomial(profile_index, loss)
            actual = sum(
                abs(coefficient)
                for coefficient in polynomial.all_coeffs()
            )
            assert actual <= bound
            checks += 1
    return checks


def audit(
    maximum_depth: int = 30,
    maximum_profile_loss: int = 24,
) -> dict[str, object]:
    ledger = ledger_checks()
    profile_checks = profile_norm_checks(maximum_profile_loss)
    weighted_checks = 0
    leading_checks = 0
    subleading_checks = 0
    worst_ratio = sp.S.Zero
    worst_depth = 0
    worst_rank = 0
    required_constants = []

    for depth in range(1, maximum_depth + 1):
        polynomial = ordinary_polynomial(depth)
        assert polynomial.LC() == 1
        leading_checks += 1

        actual_first = -polynomial.coeff_monomial(K ** (depth - 1))
        assert actual_first == first_defect(depth)
        subleading_checks += 1

        required = 0.0
        required_rank = 0
        for rank in range(1, depth + 1):
            coefficient = abs(
                polynomial.coeff_monomial(K ** (depth - rank))
            )
            proposed = (
                sp.binomial(depth, rank)
                * (3 * depth**2) ** rank
            )
            assert coefficient <= proposed
            ratio = sp.Rational(coefficient, proposed)
            if ratio > worst_ratio:
                worst_ratio = ratio
                worst_depth = depth
                worst_rank = rank
            if coefficient:
                local_constant = float(
                    (
                        coefficient / sp.binomial(depth, rank)
                    )
                    ** sp.Rational(1, rank)
                    / depth**2
                )
                if local_constant > required:
                    required = local_constant
                    required_rank = rank
            weighted_checks += 1
        required_constants.append(
            {
                "depth": depth,
                "required_C": required,
                "maximizing_rank": required_rank,
            }
        )

    assert worst_ratio == sp.Rational(23, 24)
    assert (worst_depth, worst_rank) == (2, 1)

    return {
        "schema": "amra.opg1757.explicit-polynomial-window.v1",
        "proved_eta": "1/8",
        "explicit_profile_base": PROFILE_BASE,
        "explicit_ordinary_base": "2^320",
        "ordinary_base_power_of_two": 320,
        "ordinary_symbol_power": SYMBOL_POWER,
        "maximum_profile_loss": maximum_profile_loss,
        "exact_profile_norm_checks": profile_checks,
        "leading_symbol_checks": leading_checks,
        "all_d_subleading_checks": subleading_checks,
        "maximum_experimental_depth": maximum_depth,
        "weighted_C_candidate": 3,
        "weighted_symbol_checks": weighted_checks,
        "worst_weighted_ratio": str(worst_ratio),
        "worst_weighted_location": {
            "depth": worst_depth,
            "rank": worst_rank,
        },
        "required_constants": required_constants,
        **ledger,
        "classification": {
            "eta_one_eighth": "proved",
            "weighted_C_equals_3": "finite_evidence_only",
            "eta_one_third": "open",
        },
        "status": "explicit_eta_certificate_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-depth", type=int, default=30)
    parser.add_argument("--maximum-profile-loss", type=int, default=24)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_depth, args.maximum_profile_loss),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
