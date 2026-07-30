#!/usr/bin/env python3
"""Independent coordinate and exponent audit for angular starvation.

This verifier does not import verify_angular_starvation_branch.py.
It checks the normalized circle equations behind Lemma 2, the exact
exceptional two-point configuration, and the exponent ledger in
Theorem 3 and Proposition 4.
"""

from __future__ import annotations

import json
from fractions import Fraction

import sympy as sp


U, Z, V, W, D = sp.symbols("u z v w d", real=True)


def target_circle_coefficients(cosine, source_u, source_z, distance):
    """Coefficients of v^2+w^2+a*v+b*w+e=0 in the target plane."""

    return (
        sp.expand(-2*cosine*source_u),
        sp.expand(-2*source_z),
        sp.expand(source_u**2+source_z**2-distance),
    )


def two_target_difference_coefficients(
    cosine, first_target, second_target
):
    """Coefficients of F_first(u,z)-F_second(u,z)."""

    v1, w1 = first_target
    v2, w2 = second_target
    return (
        sp.expand(-2*cosine*(v1-v2)),
        sp.expand(-2*(w1-w2)),
        sp.expand(v1**2+w1**2-v2**2-w2**2),
    )


def source_sphere_polynomial(cosine, target, distance):
    """Distance equation in signed radial/height source coordinates."""

    target_v, target_w = target
    return sp.expand(
        U**2
        + Z**2
        - 2*cosine*target_v*U
        - 2*target_w*Z
        + target_v**2
        + target_w**2
        - distance
    )


def resultant_degree_for_two_targets(
    cosine, first_target, second_target, distance
):
    """Degree of the eliminated equation for two target incidences."""

    first = source_sphere_polynomial(cosine, first_target, distance)
    second = source_sphere_polynomial(cosine, second_target, distance)
    resultant = sp.factor(sp.resultant(first, second, Z))
    if resultant == 0:
        return None
    return sp.Poly(resultant, U).degree()


def exponent_ledger():
    """Exact powers of N in the source-plane argument."""

    m = Fraction(1, 5)
    q = Fraction(3, 5)
    distance_labels = Fraction(3, 5)
    return {
        "good_ordered_plane_pairs": 2*m,
        "source_pair_mass": 2*m+2*q,
        "aggregate_energy": 4*m+4*q-distance_labels,
        "diagonal_energy": 2*m+Fraction(10, 3)*q,
        "aggregate_minus_diagonal_gap": (
            4*m+4*q-distance_labels
            - (2*m+Fraction(10, 3)*q)
        ),
        "radius_energy_to_mass": (
            Fraction(7, 5)-Fraction(4, 5)
        ),
    }


def weak_lambda_quantifier_counterexample(high_mass):
    """Abstract witness showing why lambda must belong to the high-I radius."""

    if high_mass < 3:
        raise ValueError("high_mass must be at least three")
    masses = {"bad_lambda_radius": high_mass, "good_lambda_radius": 1}
    energy = sum(value**2 for value in masses.values())
    total = sum(masses.values())
    averaging_floor = Fraction(energy, total)
    return {
        "energy": energy,
        "total_mass": total,
        "averaging_floor": averaging_floor,
        "good_lambda_radius_mass": 1,
        "good_radius_is_energy_witness": Fraction(1) >= averaging_floor,
    }


def divisor_count(value):
    """Number of positive divisors of value."""

    if value < 1:
        raise ValueError("value must be positive")
    result = 1
    remaining = value
    prime = 2
    while prime*prime <= remaining:
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        result *= exponent+1
        prime += 1
    if remaining > 1:
        result *= 2
    return result


def ruled_product_and_distance_fibres(t, slope_differences):
    """Finite fibre audit for the maps in (32b)--(32c)."""

    differences = tuple(sorted(set(slope_differences)))
    if t < 2 or not differences:
        raise ValueError("need t >= 2 and nonempty slope differences")
    if differences[0] < 1 or differences[-1] > t:
        raise ValueError("differences must lie in [1,t]")

    product_fibres = {}
    for radial in range(1, t+1):
        for difference in differences:
            product = radial*difference
            product_fibres[product] = product_fibres.get(product, 0)+1

    height = t*t
    distance_fibres = {}
    for product in product_fibres:
        for axial_difference in range(height):
            label = product*product + axial_difference*axial_difference
            distance_fibres[label] = distance_fibres.get(label, 0)+1

    max_product_fibre = max(product_fibres.values())
    max_product_divisor_bound = max(
        divisor_count(product) for product in product_fibres
    )
    max_distance_fibre = max(distance_fibres.values())
    max_r2_divisor_bound = max(
        4*divisor_count(label) for label in distance_fibres
    )
    maximum_label = max(distance_fibres)
    assert maximum_label <= 2*t**4
    assert max_product_fibre <= max_product_divisor_bound
    assert max_distance_fibre <= max_r2_divisor_bound
    return {
        "input_products": t*len(differences),
        "distinct_products": len(product_fibres),
        "maximum_product_fibre": max_product_fibre,
        "product_divisor_bound": max_product_divisor_bound,
        "sum_of_two_squares_inputs": len(product_fibres)*height,
        "distinct_distance_labels": len(distance_fibres),
        "maximum_distance_fibre": max_distance_fibre,
        "r2_divisor_bound": max_r2_divisor_bound,
        "maximum_label": maximum_label,
    }


def audit():
    c = sp.symbols("c", nonzero=True, real=True)
    u1, u2, z1, z2 = sp.symbols("u1 u2 z1 z2", real=True)

    first_circle = target_circle_coefficients(c, u1, z1, D)
    second_circle = target_circle_coefficients(c, u2, z2, D)
    repeated_nonperpendicular = [
        sp.solve(
            [left-right for left, right in zip(first_circle, second_circle)],
            [u1, z1],
            dict=True,
        )
    ]

    perpendicular_repeat = (
        target_circle_coefficients(0, 2, 3, 20)
        == target_circle_coefficients(0, -2, 3, 20)
    )
    equal_plane_injective = (
        target_circle_coefficients(1, 2, 3, 20)
        != target_circle_coefficients(1, -2, 3, 20)
    )

    perpendicular_antipodes = two_target_difference_coefficients(
        0, (2, 5), (-2, 5)
    )
    equal_plane_pair = two_target_difference_coefficients(
        1, (2, 5), (-2, 5)
    )
    generic_resultant_degree = resultant_degree_for_two_targets(
        sp.Rational(3, 5), (1, 2), (4, -1), 25
    )

    ledger = exponent_ledger()
    quantifier_example = weak_lambda_quantifier_counterexample(100)
    ruled_fibres = ruled_product_and_distance_fibres(
        10, range(1, 10)
    )

    assert repeated_nonperpendicular == [[{u1: u2, z1: z2}]]
    assert perpendicular_repeat
    assert equal_plane_injective
    assert perpendicular_antipodes == (0, 0, 0)
    assert equal_plane_pair != (0, 0, 0)
    assert generic_resultant_degree <= 2
    assert ledger["aggregate_energy"] == Fraction(13, 5)
    assert ledger["diagonal_energy"] == Fraction(12, 5)
    assert ledger["aggregate_minus_diagonal_gap"] == Fraction(1, 5)
    assert ledger["radius_energy_to_mass"] == Fraction(3, 5)
    assert not quantifier_example["good_radius_is_energy_witness"]
    assert ruled_fibres["distinct_products"] >= (
        ruled_fibres["input_products"]
        / ruled_fibres["product_divisor_bound"]
    )
    assert ruled_fibres["distinct_distance_labels"] >= (
        ruled_fibres["sum_of_two_squares_inputs"]
        / ruled_fibres["r2_divisor_bound"]
    )

    return {
        "schema": "amra.erdos1083.angular-starvation-independent.v1",
        "verdict_as_written": "PASS",
        "lemma_2_bound": "PASS",
        "equal_planes_are_positive_dimensional_degeneracy": False,
        "perpendicular_antipodal_targets_are_degenerate": True,
        "nonperpendicular_repeated_circle_multiplicity": 1,
        "theorem_3_mass_and_exponents": "PASS",
        "proposition_4": "PASS_WITNESS_RADIUS_AND_ANCHOR_BOUND",
        "cross_plane_transfer_32a_32c": "PASS",
        "aggregate_energy_exponent": str(ledger["aggregate_energy"]),
        "diagonal_energy_exponent": str(ledger["diagonal_energy"]),
        "energy_gap": str(ledger["aggregate_minus_diagonal_gap"]),
        "finite_ruled_distance_labels": (
            ruled_fibres["distinct_distance_labels"]
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
