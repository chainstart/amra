#!/usr/bin/env python3
"""Finite exact checks for the cross-plane Galois-orbit trichotomy."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction

import sympy as sp


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def label_statistics(weights: list[list[int]]) -> dict:
    """Compute S_d, c_d, support sizes, and the total cross codegree."""
    if not weights or not weights[0]:
        raise ValueError("weights must be a nonempty rectangular matrix")
    label_count = len(weights[0])
    if any(len(row) != label_count for row in weights):
        raise ValueError("weights must be rectangular")
    if any(value < 0 for row in weights for value in row):
        raise ValueError("weights must be nonnegative")

    cell_cap = max(value for row in weights for value in row)
    masses = []
    codegrees = []
    supports = []
    for label in range(label_count):
        column = [row[label] for row in weights]
        mass = sum(column)
        diagonal = sum(value * value for value in column)
        masses.append(mass)
        codegrees.append(mass * mass - diagonal)
        supports.append(sum(value > 0 for value in column))
    return {
        "label_count": label_count,
        "cell_cap": cell_cap,
        "masses": masses,
        "codegrees": codegrees,
        "supports": supports,
        "cross_codegree": sum(codegrees),
    }


def heavy_label_audit(
    weights: list[list[int]], theta: Fraction = Fraction(1, 2)
) -> dict:
    """Check Theorem 1 exactly, without floating-point square roots."""
    if not Fraction(0) < theta < Fraction(1):
        raise ValueError("theta must lie strictly between zero and one")
    stats = label_statistics(weights)
    label_count = stats["label_count"]
    cross = stats["cross_codegree"]
    cap = stats["cell_cap"]
    if cross <= 0 or cap <= 0:
        raise ValueError("positive cross codegree and cell cap required")

    # c_d >= theta*C/L, compared after clearing denominators.
    threshold_numerator = theta.numerator * cross
    threshold_denominator = theta.denominator * label_count
    heavy = [
        label
        for label, codegree in enumerate(stats["codegrees"])
        if codegree * threshold_denominator >= threshold_numerator
    ]
    heavy_energy = sum(stats["codegrees"][label] for label in heavy)
    assert (
        heavy_energy * theta.denominator
        >= (theta.denominator - theta.numerator) * cross
    )
    for label in heavy:
        codegree = stats["codegrees"][label]
        mass = stats["masses"][label]
        support = stats["supports"][label]
        assert mass * mass >= codegree
        assert support * support * cap * cap >= codegree

    return {
        "theta": str(theta),
        "label_count": label_count,
        "cross_codegree": cross,
        "heavy_label_count": len(heavy),
        "heavy_energy": heavy_energy,
        "heavy_energy_fraction": str(Fraction(heavy_energy, cross)),
    }


def orbit_expansion_audit(
    codegrees: list[int],
    complete_orbits: list[list[int]],
    degree_threshold: int,
) -> dict:
    """Check both exact orbit inequalities on a finite label set."""
    if degree_threshold < 1:
        raise ValueError("degree threshold must be positive")
    seen: set[int] = set()
    retained: list[tuple[list[int], int]] = []
    for orbit in complete_orbits:
        if len(orbit) < degree_threshold:
            continue
        if len(set(orbit)) != len(orbit):
            raise ValueError("an orbit contains duplicate labels")
        if seen.intersection(orbit):
            raise ValueError("complete orbits must be disjoint")
        if any(label < 0 or label >= len(codegrees) for label in orbit):
            raise ValueError("orbit label index is out of range")
        seen.update(orbit)
        retained.append((orbit, sum(codegrees[label] for label in orbit)))
    if not retained:
        raise ValueError("at least one retained complete orbit is required")

    energy = sum(value for _, value in retained)
    max_orbit_energy = max(value for _, value in retained)
    orbit_label_count = sum(len(orbit) for orbit, _ in retained)
    lower_bound = Fraction(degree_threshold * energy, max_orbit_energy)
    average_energy_cap = max(
        Fraction(value, len(orbit)) for orbit, value in retained
    )
    density_lower_bound = Fraction(energy, 1) / average_energy_cap
    assert orbit_label_count >= lower_bound
    assert orbit_label_count >= density_lower_bound
    return {
        "degree_threshold": degree_threshold,
        "complete_orbit_count": len(retained),
        "complete_orbit_label_count": orbit_label_count,
        "complete_orbit_energy": energy,
        "max_orbit_energy": max_orbit_energy,
        "degree_orbit_lower_bound": str(lower_bound),
        "density_lower_bound": str(density_lower_bound),
    }


def cyclotomic_tensor(prime: int) -> list[list[int]]:
    """Construct the finite tensor W in equation (9)."""
    if prime < 5 or prime % 2 == 0 or not is_prime(prime):
        raise ValueError("prime must be an odd prime at least 5")
    degree = (prime - 1) // 2
    labels = [
        (chord, shift)
        for chord in range(1, degree + 1)
        for shift in range(prime * prime)
    ]
    return [
        [
            prime**4 if shift % prime == residue else 0
            for _, shift in labels
        ]
        for residue in range(prime)
        for _ in range(prime)
    ]


def cyclotomic_tensor_ledger(prime: int) -> dict:
    """Closed formulas for the full critical cyclotomic tensor."""
    if prime < 5 or prime % 2 == 0 or not is_prime(prime):
        raise ValueError("prime must be an odd prime at least 5")
    degree = (prime - 1) // 2
    plane_pairs = prime**2
    label_count = degree * prime**2
    row_support = degree * prime
    label_support = prime
    cell_weight = prime**4
    support_edges = degree * prime**3
    row_mass = degree * prime**5
    label_mass = prime**5
    total_mass = degree * prime**7
    diagonal_energy = degree * prime**11
    aggregate_energy = degree * prime**12
    cross_codegree = degree * prime**11 * (prime - 1)
    label_codegree = prime**9 * (prime - 1)
    orbit_energy = degree * label_codegree
    orbit_count = prime**2
    orbit_bound = Fraction(
        degree * cross_codegree,
        orbit_energy,
    )
    assert orbit_bound == label_count
    return {
        "prime": prime,
        "field_degree": degree,
        "plane_pairs": plane_pairs,
        "labels": label_count,
        "complete_orbits": orbit_count,
        "row_support": row_support,
        "label_support": label_support,
        "cell_weight": cell_weight,
        "support_edges": support_edges,
        "row_mass": row_mass,
        "label_mass": label_mass,
        "total_mass": total_mass,
        "diagonal_energy": diagonal_energy,
        "aggregate_energy": aggregate_energy,
        "cross_codegree": cross_codegree,
        "label_codegree": label_codegree,
        "orbit_energy": orbit_energy,
        "orbit_lower_bound": str(orbit_bound),
        "orbit_inequality_is_exact": orbit_bound == label_count,
    }


def verify_tensor_against_closed_ledger(prime: int) -> dict:
    """Enumerate a small tensor and compare it with every closed formula."""
    matrix = cyclotomic_tensor(prime)
    stats = label_statistics(matrix)
    ledger = cyclotomic_tensor_ledger(prime)
    row_supports = [sum(value > 0 for value in row) for row in matrix]
    row_masses = [sum(row) for row in matrix]
    assert len(matrix) == ledger["plane_pairs"]
    assert stats["label_count"] == ledger["labels"]
    assert set(row_supports) == {ledger["row_support"]}
    assert set(row_masses) == {ledger["row_mass"]}
    assert set(stats["supports"]) == {ledger["label_support"]}
    assert set(stats["masses"]) == {ledger["label_mass"]}
    assert set(stats["codegrees"]) == {ledger["label_codegree"]}
    assert stats["cross_codegree"] == ledger["cross_codegree"]
    return {
        "prime": prime,
        "matrix_rows": len(matrix),
        "matrix_labels": stats["label_count"],
        "closed_ledger_match": True,
    }


def cyclotomic_label_degree_checks(prime: int, shifts=(0, 1)) -> list[dict]:
    """Check degrees of 5u+a_d for small primes using minimal polynomials."""
    if prime < 5 or prime % 2 == 0 or not is_prime(prime):
        raise ValueError("prime must be an odd prime at least 5")
    degree = (prime - 1) // 2
    checks = []
    for shift in shifts:
        for chord in range(1, degree + 1):
            value = (
                5 * shift
                + 2
                - 2
                * sp.cos(sp.Rational(2 * chord, prime) * sp.pi)
            )
            polynomial = sp.Poly(sp.minimal_polynomial(value))
            assert polynomial.degree() == degree
            checks.append(
                {
                    "prime": prime,
                    "shift": shift,
                    "chord": chord,
                    "degree": polynomial.degree(),
                }
            )
    return checks


def critical_orbit_threshold(
    codegree_exponent: Fraction,
    degree_exponent: Fraction,
    target_distance_exponent: Fraction,
) -> dict:
    """Exponent version H_R <= R*C_R/D_*."""
    orbit_energy_exponent = (
        codegree_exponent + degree_exponent - target_distance_exponent
    )
    average_per_label_exponent = (
        codegree_exponent - target_distance_exponent
    )
    return {
        "codegree_exponent": str(codegree_exponent),
        "degree_exponent": str(degree_exponent),
        "target_distance_exponent": str(target_distance_exponent),
        "orbit_energy_threshold_exponent": str(orbit_energy_exponent),
        "average_per_label_threshold_exponent": str(
            average_per_label_exponent
        ),
    }


def audit() -> dict:
    prime = 5
    matrix = cyclotomic_tensor(prime)
    stats = label_statistics(matrix)
    degree = (prime - 1) // 2
    orbits = [
        [
            chord_index * prime * prime + shift
            for chord_index in range(degree)
        ]
        for shift in range(prime * prime)
    ]
    orbit_audit = orbit_expansion_audit(
        stats["codegrees"], orbits, degree
    )
    ledger = cyclotomic_tensor_ledger(prime)
    assert orbit_audit["degree_orbit_lower_bound"] == str(ledger["labels"])
    return {
        "schema": "amra.erdos1083.cross-plane-galois-orbit-trichotomy.v1",
        "verdict": "PASS",
        "scope": (
            "Rigorous tensor inequalities and a power-sharp abstract "
            "cyclotomic model. No Euclidean realization and no "
            "unconditional Erdős #1083 exponent improvement are claimed."
        ),
        "heavy_label_audit": heavy_label_audit(matrix),
        "orbit_expansion_audit": orbit_audit,
        "cyclotomic_ledgers": [
            cyclotomic_tensor_ledger(value) for value in (5, 7, 11)
        ],
        "explicit_tensor_check": verify_tensor_against_closed_ledger(5),
        "minimal_polynomial_checks": len(
            cyclotomic_label_degree_checks(5)
            + cyclotomic_label_degree_checks(7)
        ),
        "critical_threshold": critical_orbit_threshold(
            Fraction(13), Fraction(1), Fraction(3)
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
