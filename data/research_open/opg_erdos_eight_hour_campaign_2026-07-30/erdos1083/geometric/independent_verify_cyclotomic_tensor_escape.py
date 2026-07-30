#!/usr/bin/env python3
"""Independent exact audit of the cyclotomic tensor escape theorem."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from itertools import combinations

import mpmath


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def real_basis_label(
    prime: int,
    radius_squared: Fraction,
    chord_index: int,
    anchored_height_square: Fraction,
) -> tuple[Fraction, ...]:
    """Canonical vector in 1,b_1,...,b_{m-1}, not the author's quotient."""
    if prime < 7 or prime % 2 == 0 or not is_prime(prime):
        raise ValueError("prime must be an odd prime at least 7")
    degree = (prime - 1) // 2
    if radius_squared <= 0:
        raise ValueError("squared radius must be positive")
    if not 1 <= chord_index <= degree:
        raise ValueError("chord index out of range")
    if anchored_height_square < 0:
        raise ValueError("anchored height square must be nonnegative")

    constant = anchored_height_square + 2 * radius_squared
    coefficients = [Fraction(0) for _ in range(degree - 1)]
    if chord_index < degree:
        coefficients[chord_index - 1] = -radius_squared
    else:
        # b_m=-1-b_1-...-b_{m-1}, so 2q-qb_m=3q+q sum b_j.
        constant += radius_squared
        coefficients = [radius_squared for _ in coefficients]
    return (constant, *coefficients)


def selected_label_vectors(
    prime: int,
    fibres: tuple[tuple[Fraction, tuple[Fraction, ...]], ...],
) -> dict[tuple[Fraction, ...], tuple[Fraction, int, Fraction]]:
    """Enumerate varying radius fibres by their anchored height squares."""
    if not fibres:
        raise ValueError("at least one radius fibre is required")
    radius_squares = tuple(radius_squared for radius_squared, _ in fibres)
    if len(set(radius_squares)) != len(radius_squares):
        raise ValueError("squared radii must be distinct")
    degree = (prime - 1) // 2
    vectors: dict[
        tuple[Fraction, ...], tuple[Fraction, int, Fraction]
    ] = {}
    expected = 0
    for radius_squared, anchored_squares in fibres:
        if not anchored_squares:
            raise ValueError("every radius must have a nonempty height fibre")
        if Fraction(0) not in anchored_squares:
            raise ValueError("the minimum height must contribute square zero")
        if len(set(anchored_squares)) != len(anchored_squares):
            raise ValueError("anchored height squares must be distinct")
        if any(value < 0 for value in anchored_squares):
            raise ValueError("anchored height squares must be nonnegative")
        expected += degree * len(anchored_squares)
        for chord_index in range(1, degree + 1):
            for anchored_square in anchored_squares:
                vector = real_basis_label(
                    prime,
                    radius_squared,
                    chord_index,
                    anchored_square,
                )
                triple = (radius_squared, chord_index, anchored_square)
                if vector in vectors:
                    raise AssertionError(
                        f"collision between {vectors[vector]} and {triple}"
                    )
                vectors[vector] = triple
    assert len(vectors) == expected
    return vectors


def numerical_label(
    prime: int,
    radius_squared: Fraction,
    chord_index: int,
    anchored_height_square: Fraction,
) -> mpmath.mpf:
    mpmath.mp.dps = 100
    chord = 2 - 2 * mpmath.cos(
        2 * mpmath.pi * chord_index / prime
    )
    return (
        mpmath.mpf(radius_squared.numerator)
        / radius_squared.denominator
        * chord
        + mpmath.mpf(anchored_height_square.numerator)
        / anchored_height_square.denominator
    )


def numerical_consistency_audit(
    prime: int,
    fibres: tuple[tuple[Fraction, tuple[Fraction, ...]], ...],
) -> dict:
    vectors = selected_label_vectors(prime, fibres)
    numerical = [
        numerical_label(
            prime,
            radius_squared,
            chord_index,
            anchored_square,
        )
        for radius_squared, chord_index, anchored_square in vectors.values()
    ]
    minimum_gap = min(
        abs(left - right) for left, right in combinations(numerical, 2)
    )
    assert minimum_gap > mpmath.mpf("1e-50")
    return {
        "prime": prime,
        "radii": len(fibres),
        "height_counts": [len(squares) for _, squares in fibres],
        "labels": len(vectors),
        "expected_labels": ((prime - 1) // 2)
        * sum(len(squares) for _, squares in fibres),
        "minimum_numerical_gap": str(minimum_gap),
    }


def _anchor_value(tag: str) -> mpmath.mpf:
    """Small fixed menu used only for independent coordinate regression."""
    if tag == "-sqrt(2)":
        return -mpmath.sqrt(2)
    if tag == "pi/7":
        return mpmath.pi / 7
    if tag == "-5/3":
        return -mpmath.mpf(5) / 3
    raise ValueError(f"unknown anchor tag: {tag}")


def direct_coordinate_fibre_audit(
    prime: int,
    fibres: tuple[tuple[Fraction, tuple[Fraction, ...]], ...],
    anchor_tags: tuple[str, ...],
) -> dict:
    """Check actual point-pair coordinates for unequal non-AP height fibres."""
    if len(fibres) != len(anchor_tags):
        raise ValueError("one anchor is required for every radius fibre")
    exact_vectors = selected_label_vectors(prime, fibres)
    mpmath.mp.dps = 100
    coordinate_labels = []
    maximum_formula_error = mpmath.mpf(0)
    for (radius_squared, anchored_squares), anchor_tag in zip(
        fibres, anchor_tags
    ):
        radius = mpmath.sqrt(
            mpmath.mpf(radius_squared.numerator)
            / radius_squared.denominator
        )
        anchor = _anchor_value(anchor_tag)
        actual_heights = [
            anchor
            + mpmath.sqrt(
                mpmath.mpf(square.numerator) / square.denominator
            )
            for square in anchored_squares
        ]
        assert min(actual_heights) == anchor
        for chord_index in range(1, (prime - 1) // 2 + 1):
            angle = 2 * mpmath.pi * chord_index / prime
            for height, anchored_square in zip(
                actual_heights, anchored_squares
            ):
                dx = radius - radius * mpmath.cos(angle)
                dy = -radius * mpmath.sin(angle)
                dz = anchor - height
                coordinate_distance = dx * dx + dy * dy + dz * dz
                formula_distance = numerical_label(
                    prime,
                    radius_squared,
                    chord_index,
                    anchored_square,
                )
                maximum_formula_error = max(
                    maximum_formula_error,
                    abs(coordinate_distance - formula_distance),
                )
                coordinate_labels.append(coordinate_distance)
    assert len(coordinate_labels) == len(exact_vectors)
    assert maximum_formula_error < mpmath.mpf("1e-90")
    minimum_gap = min(
        abs(left - right)
        for left, right in combinations(coordinate_labels, 2)
    )
    assert minimum_gap > mpmath.mpf("1e-50")
    return {
        "prime": prime,
        "radii": len(fibres),
        "height_counts": [len(squares) for _, squares in fibres],
        "anchor_tags": list(anchor_tags),
        "selected_coordinate_distances": len(coordinate_labels),
        "expected_selected_distances": ((prime - 1) // 2)
        * sum(len(squares) for _, squares in fibres),
        "maximum_formula_error": str(maximum_formula_error),
        "minimum_numerical_gap": str(minimum_gap),
    }


def relation_space_dimension(prime: int, intersection_degree: int) -> int:
    """Dimension m+1-m/q from the compositum degree formula."""
    if prime < 7 or prime % 2 == 0 or not is_prime(prime):
        raise ValueError("prime must be an odd prime at least 7")
    degree = (prime - 1) // 2
    if intersection_degree < 1 or degree % intersection_degree:
        raise ValueError("intersection degree must divide (p-1)/2")
    return degree + 1 - degree // intersection_degree


def degree_disjointness_sufficient(
    field_degree: int, prime: int
) -> bool:
    if field_degree < 1:
        raise ValueError("field degree must be positive")
    if prime < 7 or prime % 2 == 0 or not is_prime(prime):
        raise ValueError("prime must be an odd prime at least 7")
    return math.gcd(field_degree, (prime - 1) // 2) == 1


def real_cyclotomic_boundary_collisions(prime: int) -> dict:
    """Formal product-label collision count when F contains every a_d."""
    if prime < 7 or prime % 2 == 0 or not is_prime(prime):
        raise ValueError("prime must be an odd prime at least 7")
    degree = (prime - 1) // 2
    ordered = [(radius, chord) for radius in range(degree) for chord in range(degree)]
    # The formal label a_radius*a_chord is represented by the unordered pair.
    labels = {tuple(sorted(pair)) for pair in ordered}
    assert len(labels) == degree * (degree + 1) // 2
    assert len(labels) < len(ordered)
    return {
        "prime": prime,
        "field_degree": degree,
        "ordered_selected_inputs": len(ordered),
        "distinct_formal_product_labels": len(labels),
        "collision_pair": {
            "first": [0, 1],
            "second": [1, 0],
        },
    }


def audit() -> dict:
    configurations = [
        (
            7,
            (
                (Fraction(1), (Fraction(0), Fraction(1, 2), Fraction(7, 3))),
                (Fraction(3, 2), (Fraction(0), Fraction(2), Fraction(5))),
                (Fraction(11, 5), (Fraction(0), Fraction(1, 7))),
            ),
        ),
        (
            11,
            (
                (Fraction(1, 3), (Fraction(0), Fraction(3), Fraction(11, 2))),
                (Fraction(7, 4), (Fraction(0), Fraction(1, 5))),
            ),
        ),
        (
            13,
            (
                (Fraction(2), (Fraction(0), Fraction(7, 3))),
                (Fraction(13, 7), (Fraction(0), Fraction(1), Fraction(10))),
                (Fraction(9, 5), (Fraction(0),)),
            ),
        ),
    ]
    finite = [
        numerical_consistency_audit(prime, fibres)
        for prime, fibres in configurations
    ]
    direct_coordinates = direct_coordinate_fibre_audit(
        configurations[0][0],
        configurations[0][1],
        ("-sqrt(2)", "pi/7", "-5/3"),
    )
    relation_dimensions = [
        {
            "prime": prime,
            "intersection_degree": intersection,
            "relation_dimension": relation_space_dimension(
                prime, intersection
            ),
        }
        for prime, intersection in (
            (7, 1),
            (7, 3),
            (11, 1),
            (11, 5),
            (13, 1),
            (13, 2),
            (13, 3),
            (13, 6),
        )
    ]
    return {
        "schema": "amra.erdos1083.cyclotomic-tensor-escape-independent-audit.v1",
        "verdict": "PASS",
        "scope": (
            "Independent real-cyclotomic-basis verification of the "
            "radius-dependent stacked-fibre theorem and its base-field "
            "linear-disjointness extension. No general extraction or "
            "unconditional distance exponent is claimed."
        ),
        "finite_rational_checks": finite,
        "direct_radius_dependent_coordinate_check": direct_coordinates,
        "relation_space_dimensions": relation_dimensions,
        "degree_sufficient_samples": [
            {
                "field_degree": field_degree,
                "prime": prime,
                "disjointness_forced": degree_disjointness_sufficient(
                    field_degree, prime
                ),
            }
            for field_degree, prime in ((3, 11), (3, 13), (5, 11), (5, 13))
        ],
        "boundary_collisions": [
            real_cyclotomic_boundary_collisions(prime)
            for prime in (7, 11, 13)
        ],
        "author_verifier_imported": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
