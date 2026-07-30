#!/usr/bin/env python3
"""Exact finite checks for the growing cyclotomic chart no-go."""

from __future__ import annotations

import argparse
import json
import math

import mpmath
import sympy as sp


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def prism_ledger(prime: int, height: int):
    if prime < 5 or prime % 2 == 0 or not is_prime(prime):
        raise ValueError("prime must be an odd prime at least 5")
    if height < 3:
        raise ValueError("height must be at least 3")
    chord_types = (prime - 1) // 2
    points = prime * height
    omega = prime * (prime - 1) * height
    distance_upper = chord_types * height + height - 1
    separated_cross_labels = chord_types * (height - 2)
    # Ordered cross-pair energy on the separated layers u=2,...,H-1.
    separated_energy = (
        chord_types
        * (2 * prime) ** 2
        * sum((2 * (height - u)) ** 2 for u in range(2, height))
    )
    closed_energy = (
        8
        * prime**2
        * (prime - 1)
        * (height - 2)
        * (height - 1)
        * (2 * height - 3)
        // 6
    )
    assert separated_energy == closed_energy
    return {
        "prime": prime,
        "height": height,
        "points": points,
        "chord_types": chord_types,
        "Omega": omega,
        "distance_upper": distance_upper,
        "separated_cross_labels": separated_cross_labels,
        "separated_ordered_energy": separated_energy,
        "chord_squared_field_degree": chord_types,
        "bounded_degree_chart_overlap": 0,
    }


def enumerate_prism_distances(prime: int, height: int):
    """Numerically enumerate labels, using high precision and rounding."""
    mpmath.mp.dps = 80
    chord_values = [
        2 - 2 * mpmath.cos(2 * mpmath.pi * distance / prime)
        for distance in range(1, (prime - 1) // 2 + 1)
    ]
    labels = {
        round(float(vertical * vertical), 12)
        for vertical in range(1, height)
    }
    separated = set()
    for chord in chord_values:
        for vertical in range(height):
            label = round(float(chord + vertical * vertical), 12)
            labels.add(label)
            if vertical >= 2:
                separated.add(label)
    ledger = prism_ledger(prime, height)
    assert len(labels) <= ledger["distance_upper"]
    assert len(separated) == ledger["separated_cross_labels"]
    return {
        "distinct_labels": len(labels),
        "separated_labels": len(separated),
    }


def chord_squared_minimal_degree(prime: int, distance: int = 1):
    if not is_prime(prime) or prime < 5:
        raise ValueError("odd prime at least 5 required")
    if not 1 <= distance <= (prime - 1) // 2:
        raise ValueError("invalid chord type")
    expression = (
        2
        - 2 * sp.cos(
            sp.Rational(2 * distance, prime) * sp.pi
        )
    )
    polynomial = sp.Poly(sp.minimal_polynomial(expression))
    expected = (prime - 1) // 2
    assert polynomial.degree() == expected
    return {
        "prime": prime,
        "distance": distance,
        "degree": polynomial.degree(),
        "minimal_polynomial": str(polynomial.as_expr()),
    }


def circular_unit_log_determinant(prime: int):
    """Numerical regulator check for the standard independent units."""
    if not is_prime(prime) or prime < 5:
        raise ValueError("odd prime at least 5 required")
    rank = (prime - 3) // 2
    mpmath.mp.dps = 100
    matrix = mpmath.matrix(rank)
    for row, embedding in enumerate(range(1, rank + 1)):
        denominator = abs(
            mpmath.sin(mpmath.pi * embedding / prime)
        )
        for column, chord_type in enumerate(range(2, rank + 2)):
            numerator = abs(
                mpmath.sin(
                    mpmath.pi * embedding * chord_type / prime
                )
            )
            matrix[row, column] = mpmath.log(numerator / denominator)
    determinant = mpmath.det(matrix)
    assert abs(determinant) > mpmath.mpf("1e-60")
    return {
        "prime": prime,
        "rank": rank,
        "absolute_log_determinant": str(abs(determinant)),
    }


def low_rank_capture_bound(prime: int, multiplicative_rank: int):
    if multiplicative_rank < 0:
        raise ValueError("rank must be nonnegative")
    chord_types = (prime - 1) // 2
    captured_types = min(chord_types, multiplicative_rank + 1)
    fraction = sp.Rational(captured_types, chord_types)
    return {
        "prime": prime,
        "multiplicative_rank": multiplicative_rank,
        "captured_chord_types": captured_types,
        "captured_overlap_fraction": str(fraction),
    }


def palette_exponent_ledger(
    overlap_exponent,
    ray_exponent,
    palette_exponent,
    chord_multiplicity_exponent,
):
    """Conditional finite-palette terminal exponent."""
    distance_exponent = (
        overlap_exponent
        - ray_exponent
        - palette_exponent
        - chord_multiplicity_exponent
    )
    return {
        "overlap_exponent": str(overlap_exponent),
        "ray_exponent": str(ray_exponent),
        "palette_exponent": str(palette_exponent),
        "chord_multiplicity_exponent": str(
            chord_multiplicity_exponent
        ),
        "distance_exponent": str(distance_exponent),
    }


def audit():
    ledgers = [
        prism_ledger(prime, prime * prime)
        for prime in (5, 7, 11, 13)
    ]
    enumerations = [
        {
            "prime": prime,
            "height": 8,
            **enumerate_prism_distances(prime, 8),
        }
        for prime in (5, 7, 11, 13)
    ]
    degree_checks = [
        chord_squared_minimal_degree(prime, distance)
        for prime in (5, 7, 11)
        for distance in range(1, (prime - 1) // 2 + 1)
    ]
    regulator_checks = [
        circular_unit_log_determinant(prime)
        for prime in (5, 7, 11, 13)
    ]
    return {
        "schema": "amra.erdos1083.growing-cyclotomic-chart-nogo.v1",
        "verdict": "PASS",
        "scope": (
            "Rigorous local no-go: distance-label cardinality and weighted "
            "overlap do not force a bounded-degree or subpolynomial-rank "
            "number-field chart. This is not an N=t^5 global few-distance "
            "configuration."
        ),
        "critical_local_ledgers": ledgers,
        "finite_distance_enumerations": enumerations,
        "minimal_polynomial_checks": len(degree_checks),
        "circular_unit_regulator_checks": regulator_checks,
        "rank_capture_sample": low_rank_capture_bound(101, 3),
        "conditional_palette_ledger": palette_exponent_ledger(
            5, 1, sp.Rational(1, 3), sp.Rational(1, 4)
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
