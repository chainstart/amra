#!/usr/bin/env python3
"""Verify the labelled-C4 radical elimination and capacity ledger."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import product
from math import isqrt


def elimination_polynomial(
    first: int,
    second: int,
    third: int,
    fourth: int,
) -> int:
    """Return the radical-elimination polynomial F(A,B,C,D)."""
    difference = first + second - third - fourth
    core = (
        4 * third * fourth
        - difference**2
        - 4 * first * second
    )
    return core**2 - 16 * difference**2 * first * second


def possible_fourth_values(
    first: int,
    second: int,
    third: int,
) -> tuple[int, ...]:
    """List D from signed roots when A, B and C are integer squares."""
    values = (first, second, third)
    if any(value < 0 for value in values):
        raise ValueError("adjusted cell values must be nonnegative")
    roots = tuple(isqrt(value) for value in values)
    if any(root**2 != value for root, value in zip(roots, values)):
        raise ValueError("this exact verifier expects integer squares")
    fourth_values = {
        (sign_a * roots[0] - sign_b * roots[1] + roots[2]) ** 2
        for sign_a, sign_b in product((-1, 1), repeat=2)
    }
    return tuple(sorted(fourth_values))


def rectangle_certificate(
    hub_first: int,
    hub_second: int,
    partner_first: int,
    partner_second: int,
) -> dict[str, object]:
    """Certify the signed cocycle for one four-coordinate rectangle."""
    signed_differences = (
        hub_first - partner_first,
        hub_second - partner_first,
        hub_second - partner_second,
        hub_first - partner_second,
    )
    adjusted_values = tuple(value**2 for value in signed_differences)
    cocycle = (
        signed_differences[0]
        - signed_differences[1]
        + signed_differences[2]
        - signed_differences[3]
    )
    polynomial = elimination_polynomial(*adjusted_values)
    return {
        "signed_differences": signed_differences,
        "adjusted_values": adjusted_values,
        "cocycle": cocycle,
        "cocycle_closes": cocycle == 0,
        "elimination_polynomial": polynomial,
        "polynomial_vanishes": polynomial == 0,
        "fourth_is_in_signed_root_list": (
            adjusted_values[3]
            in possible_fourth_values(*adjusted_values[:3])
        ),
    }


def degeneracy_certificate(
    hub_first: int,
    hub_second: int,
    partner_first: int,
    partner_second: int,
) -> dict[str, bool]:
    """Record the elementary equal-label degeneracies of a rectangle."""
    certificate = rectangle_certificate(
        hub_first,
        hub_second,
        partner_first,
        partner_second,
    )
    first, second, third, fourth = certificate["adjusted_values"]
    return {
        "first_edge_collapses": first == 0,
        "adjacent_first_pair_equal": first == second,
        "adjacent_second_pair_equal": third == fourth,
        "opposite_pair_ac_equal": first == third,
        "opposite_pair_bd_equal": second == fourth,
        "first_partner_is_vertical_midpoint": (
            2 * partner_first == hub_first + hub_second
        ),
        "second_partner_is_vertical_midpoint": (
            2 * partner_second == hub_first + hub_second
        ),
        "vertical_parallelogram": (
            hub_first + partner_second
            == hub_second + partner_first
        ),
    }


def arithmetic_progression_barrier(length: int) -> dict[str, object]:
    """Enumerate the complete four-class AP rectangle construction."""
    if length <= 0:
        raise ValueError("the progression length must be positive")
    label_quadruples: set[tuple[int, int, int, int]] = set()
    completions: dict[tuple[int, int, int], set[int]] = {}
    polynomial_failures = 0
    parallelograms = 0
    for hub_first, hub_second, partner_first, partner_second in product(
        range(length), repeat=4
    ):
        certificate = rectangle_certificate(
            hub_first,
            hub_second,
            partner_first,
            partner_second,
        )
        adjusted = certificate["adjusted_values"]
        label_quadruples.add(adjusted)
        completions.setdefault(adjusted[:3], set()).add(adjusted[3])
        polynomial_failures += not certificate["polynomial_vanishes"]
        parallelograms += (
            hub_first + partner_second
            == hub_second + partner_first
        )

    additive_energy_formula = (2 * length**3 + length) // 3
    return {
        "length": length,
        "edge_label_count": length,
        "point_rectangle_count": length**4,
        "distinct_label_quadruple_count": len(label_quadruples),
        "label_quadruple_upper_bound": 4 * length**3,
        "maximum_fourth_choices": max(map(len, completions.values())),
        "polynomial_failure_count": polynomial_failures,
        "vertical_parallelogram_count": parallelograms,
        "additive_energy_formula": additive_energy_formula,
        "additive_energy_formula_holds": (
            parallelograms == additive_energy_formula
        ),
    }


def exponent_ledger(
    eta_numerator: int,
    eta_denominator: int,
) -> dict[str, Fraction]:
    """Compare algebraic label capacity with point and KST capacities."""
    eta = Fraction(eta_numerator, eta_denominator)
    cell_universe = Fraction(8, 3) + eta
    maximum_hub = Fraction(5, 6) + 2 * eta
    hub_coordinate_vertices = 1 + maximum_hub
    partner_coordinate_vertices = Fraction(2)
    failed_moment_edges = Fraction(3) - 3 * eta
    kst_edge_threshold = maximum_hub + 2
    algebraic_label_quadruples = 3 * cell_universe
    point_rectangle_capacity = (
        2 * hub_coordinate_vertices
        + 2 * partner_coordinate_vertices
    )
    return {
        "eta": eta,
        "cell_universe_exponent": cell_universe,
        "maximum_hub_exponent": maximum_hub,
        "hub_coordinate_vertex_exponent": hub_coordinate_vertices,
        "partner_coordinate_vertex_exponent": partner_coordinate_vertices,
        "failed_moment_edge_exponent": failed_moment_edges,
        "kst_edge_threshold_exponent": kst_edge_threshold,
        "edge_surplus_over_kst_exponent": (
            failed_moment_edges - kst_edge_threshold
        ),
        "algebraic_label_quadruple_exponent": (
            algebraic_label_quadruples
        ),
        "point_rectangle_capacity_exponent": point_rectangle_capacity,
        "algebraic_excess_over_point_capacity_exponent": (
            algebraic_label_quadruples - point_rectangle_capacity
        ),
        "fourth_label_degree_bound": Fraction(4),
    }


def _fraction_strings(
    values: dict[str, Fraction],
) -> dict[str, str]:
    return {
        key: str(value)
        for key, value in values.items()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=7)
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    args = parser.parse_args()
    output = {
        "generic_rectangle": rectangle_certificate(0, 5, 2, 9),
        "signed_root_example": possible_fourth_values(1, 4, 9),
        "ap_barrier": arithmetic_progression_barrier(args.length),
        "ledger": _fraction_strings(
            exponent_ledger(
                args.eta_numerator,
                args.eta_denominator,
            )
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
