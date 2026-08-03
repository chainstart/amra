#!/usr/bin/env python3
"""Exact minimal falsification checks for #1083 factor-aware round 3."""

from fractions import Fraction
from itertools import product
import json


def finite_differences(values: list[int]) -> list[list[int]]:
    rows = [values]
    while len(rows[-1]) > 1:
        rows.append([b - a for a, b in zip(rows[-1], rows[-1][1:])])
    return rows


def f(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    # A delta sequence on K equally spaced nodes has interpolation degree K-1.
    interpolation_checks = []
    for K in range(2, 9):
        values = [0] * (K - 1) + [1]
        rows = finite_differences(values)
        top = rows[-1][0]
        assert top == 1
        interpolation_checks.append({
            "K": K,
            "top_difference_order": K - 1,
            "top_difference": top,
            "minimum_polynomial_degree": K - 1,
        })

    # The universal quotient polynomial is multilinear but still realizes
    # every Boolean divisor of D independent formal factor occurrences.
    boolean_checks = []
    for D in range(1, 9):
        specializations = {bits for bits in product((0, 1), repeat=D)}
        assert len(specializations) == 2**D
        boolean_checks.append({
            "D": D,
            "coordinate_degree": 1,
            "total_degree": D,
            "boolean_specializations": len(specializations),
        })

    K = Fraction(5, 9)
    S = Fraction(7, 9)
    U = Fraction(5, 6)
    q = Fraction(13, 18)
    defining_cell_domain = K + S
    common_spectrum = S + U
    native_capacity = K + S + U + q
    formal_two_source_tuple = K + 2 * S + U + q
    all_targets = q + U
    selected_targets = K + U
    source_to_all_targets = S + all_targets
    selected_target_pairs = 2 * selected_targets
    selected_to_all_targets = selected_targets + all_targets
    all_target_pairs = 2 * all_targets
    target = Fraction(3)
    required_fibre = all_target_pairs - target

    assert defining_cell_domain == Fraction(4, 3)
    assert common_spectrum == Fraction(29, 18)
    assert native_capacity == Fraction(26, 9)
    assert native_capacity < target
    assert formal_two_source_tuple == Fraction(11, 3)
    assert all_targets == Fraction(14, 9)
    assert selected_targets == Fraction(25, 18)
    assert source_to_all_targets == Fraction(7, 3)
    assert selected_target_pairs == Fraction(25, 9)
    assert selected_to_all_targets == Fraction(53, 18) < target
    assert all_target_pairs == Fraction(28, 9)
    assert required_fibre == Fraction(1, 9)

    # Same-sign widths do give actual pinned target-target labels, but only K.
    widths = [1, 3, 6, 10, 15, 21]
    anchor = widths[0]
    pinned = {(b - anchor) ** 2 for b in widths[1:]}
    assert len(pinned) == len(widths) - 1

    print(json.dumps({
        "schema": "amra.erdos1083.factor-aware-round3.minimal-falsification.v1",
        "lambda_interpolation": {
            "checks": interpolation_checks,
            "conclusion": "Existence of Q(T) through K samples is vacuous without a sublinear degree/pole theorem; a single coefficient can force degree K-1.",
        },
        "boolean_quotient_family": {
            "checks": boolean_checks,
            "conclusion": "Q(y) is a legal typed multilinear family, but coordinate degree one permits 2^D divisor specializations and total degree D.",
        },
        "exponent_ledger": {
            "K": f(K),
            "S": f(S),
            "U": f(U),
            "q": f(q),
            "defining_cell_domain_KS": f(defining_cell_domain),
            "common_spectrum_V_SU": f(common_spectrum),
            "native_capacity_KSUq": f(native_capacity),
            "formal_untyped_KS2Uq_tuple_capacity": f(formal_two_source_tuple),
            "all_targets_qU": f(all_targets),
            "selected_chart_targets_KU": f(selected_targets),
            "source_to_all_targets_SqU": f(source_to_all_targets),
            "selected_chart_target_pairs": f(selected_target_pairs),
            "selected_to_all_target_cross_pairs": f(selected_to_all_targets),
            "all_target_pairs": f(all_target_pairs),
            "fibre_threshold_to_reach_t_cubed": f(required_fibre),
            "strict_gain_requirement": "maximum or average all-target-pair fibre exponent < 1/9-epsilon",
            "capacity_firewall": "26/9<3 and is not an exponent improvement",
        },
        "actual_label_guard": {
            "same_sign_fixed_extreme": "K-1 actual target-target squared-distance labels",
            "defining_cells": "all lie in the common V, hence their union is at most |V|=SU regardless of K",
            "off_diagonal_requirement": "one point pair carries at most two point indices; KS^2Uq is not a realizable pair domain",
        },
        "survivor_boundary": {
            "factor_moment_route": "survives only if it uses the typed Boolean quotient family plus information beyond subset recovery and width",
            "distance_route": "the proposed two-source M08 is killed; a repaired all-target-pair theorem needs fibre exponent below 1/9-epsilon and must transfer chart information beyond the selected K rows",
        },
        "public_exponent_changed": False,
        "lean_used": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
