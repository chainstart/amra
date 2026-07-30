#!/usr/bin/env python3
"""Independent audit of partial prime-cyclotomic fibre escape."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def difference_set(modulus: int, target: frozenset[int], anchor: frozenset[int]):
    return frozenset((target_value - anchor_value) % modulus
                     for target_value in target
                     for anchor_value in anchor)


def nonzero_sign_classes(modulus: int, values: frozenset[int]):
    """Canonical representatives for nonzero classes d~-d."""
    return frozenset(
        min(value, (-value) % modulus)
        for value in values
        if value % modulus
    )


def cauchy_davenport_audit(
    prime: int, target: frozenset[int], anchor: frozenset[int]
) -> dict:
    if not is_prime(prime):
        raise ValueError("Cauchy-Davenport audit requires a prime modulus")
    if not target or not anchor:
        raise ValueError("sets must be nonempty")
    difference = difference_set(prime, target, anchor)
    classes = nonzero_sign_classes(prime, difference)
    cd_bound = min(prime, len(target) + len(anchor) - 1)
    quotient_bound = math.ceil((cd_bound - 1) / 2)
    assert len(difference) >= cd_bound
    assert len(classes) >= math.ceil((len(difference) - 1) / 2)
    assert len(classes) >= quotient_bound
    return {
        "target_size": len(target),
        "anchor_size": len(anchor),
        "difference_size": len(difference),
        "sign_classes": len(classes),
        "cauchy_davenport_bound": cd_bound,
        "quotient_bound": quotient_bound,
    }


def exhaustive_prime_difference_audit(prime: int) -> dict:
    """Exhaust all nonempty ordered subset pairs for a small prime."""
    if not is_prime(prime):
        raise ValueError("prime required")
    subsets = [
        frozenset(index for index in range(prime) if mask & (1 << index))
        for mask in range(1, 1 << prime)
    ]
    minimum_slack = prime
    pairs = 0
    for target in subsets:
        for anchor in subsets:
            result = cauchy_davenport_audit(prime, target, anchor)
            minimum_slack = min(
                minimum_slack,
                result["sign_classes"] - result["quotient_bound"],
            )
            pairs += 1
    return {
        "prime": prime,
        "ordered_nonempty_subset_pairs": pairs,
        "minimum_quotient_slack": minimum_slack,
    }


def real_cyclotomic_label(
    prime: int,
    radius_squared: Fraction,
    chord_class: int,
    anchored_height_square: Fraction,
) -> tuple[Fraction, ...]:
    """Canonical vector in 1,b_1,...,b_{m-1}, independent of author code."""
    if prime < 7 or not is_prime(prime):
        raise ValueError("odd prime at least 7 required")
    degree = (prime - 1) // 2
    if radius_squared <= 0 or anchored_height_square < 0:
        raise ValueError("invalid squared parameter")
    if not 1 <= chord_class <= degree:
        raise ValueError("invalid unoriented chord class")
    constant = anchored_height_square + 2 * radius_squared
    coefficients = [Fraction(0) for _ in range(degree - 1)]
    if chord_class < degree:
        coefficients[chord_class - 1] = -radius_squared
    else:
        constant += radius_squared
        coefficients = [radius_squared for _ in coefficients]
    return (constant, *coefficients)


def partial_fibre_audit(
    prime: int,
    fibres: tuple[
        tuple[
            Fraction,
            tuple[tuple[Fraction, frozenset[int]], ...],
        ],
        ...,
    ],
) -> dict:
    """Check direction, sign quotient, CD bound, and global injection."""
    radius_squares = [radius_squared for radius_squared, _ in fibres]
    if len(radius_squares) != len(set(radius_squares)):
        raise ValueError("radii must be distinct")
    selected: dict[tuple[Fraction, ...], tuple] = {}
    layer_records = []
    total_points = 0
    total_classes = 0
    for radius_squared, layers in fibres:
        zero_layers = [angular for square, angular in layers if square == 0]
        if len(zero_layers) != 1:
            raise ValueError("each radius needs exactly one anchored layer")
        anchor = zero_layers[0]
        seen_squares = set()
        for anchored_square, target in layers:
            if anchored_square < 0 or anchored_square in seen_squares:
                raise ValueError("anchored height squares must be distinct")
            if not target:
                raise ValueError("angular fibres must be nonempty")
            if any(not 0 <= value < prime for value in target):
                raise ValueError("angular index outside the prime group")
            seen_squares.add(anchored_square)
            difference = difference_set(prime, target, anchor)
            classes = nonzero_sign_classes(prime, difference)
            cd = cauchy_davenport_audit(prime, target, anchor)
            for chord_class in classes:
                # Explicitly confirm the direction j-i or its negative.
                assert any(
                    (target_value - anchor_value) % prime
                    in (chord_class, (-chord_class) % prime)
                    for target_value in target
                    for anchor_value in anchor
                )
                vector = real_cyclotomic_label(
                    prime,
                    radius_squared,
                    chord_class,
                    anchored_square,
                )
                token = (
                    radius_squared,
                    anchored_square,
                    chord_class,
                )
                if vector in selected:
                    raise AssertionError(
                        f"selected-label collision: {selected[vector]} and {token}"
                    )
                selected[vector] = token
            total_classes += len(classes)
            total_points += len(target)
            layer_records.append(
                {
                    "radius_squared": str(radius_squared),
                    "anchored_height_square": str(anchored_square),
                    **cd,
                }
            )
    assert len(selected) == total_classes
    return {
        "prime": prime,
        "radii": len(fibres),
        "layers": len(layer_records),
        "points": total_points,
        "selected_distances": len(selected),
        "sum_sign_classes": total_classes,
        "layer_records": layer_records,
    }


def equal_size_linear_constant_audit(prime: int, size: int) -> dict:
    if not 2 <= size <= (prime + 1) // 2:
        raise ValueError("size outside the linear-corollary range")
    cd_bound = min(prime, 2 * size - 1)
    quotient_bound = math.ceil((cd_bound - 1) / 2)
    assert cd_bound == 2 * size - 1
    assert quotient_bound == size - 1
    return {
        "prime": prime,
        "fibre_size": size,
        "cd_bound": cd_bound,
        "unoriented_bound": quotient_bound,
        "distance_per_point_constant": str(Fraction(size - 1, size)),
    }


def smallest_composite_cyclic_counterexample(limit: int = 40) -> dict:
    """Find a subgroup fibre violating the unchanged S-1 conclusion."""
    for modulus in range(7, limit + 1):
        if is_prime(modulus):
            continue
        for size in range(2, (modulus + 1) // 2 + 1):
            if modulus % size:
                continue
            step = modulus // size
            angular = frozenset(step * index for index in range(size))
            differences = difference_set(modulus, angular, angular)
            chord_classes = nonzero_sign_classes(modulus, differences)
            if len(chord_classes) < size - 1:
                return {
                    "modulus": modulus,
                    "subgroup_size": size,
                    "angular_set": sorted(angular),
                    "distinct_chord_distances": len(chord_classes),
                    "false_prime_analogue_bound": size - 1,
                }
    raise AssertionError("no composite counterexample found")


def composite_algebraic_injection_collision() -> dict:
    """At n=8, a_2=2 and a_4=4 give a rational scaling collision."""
    first_radius_squared = Fraction(1)
    second_radius_squared = Fraction(1, 2)
    first_chord_squared = Fraction(2)
    second_chord_squared = Fraction(4)
    first_label = first_radius_squared * first_chord_squared
    second_label = second_radius_squared * second_chord_squared
    assert first_label == second_label
    return {
        "modulus": 8,
        "first": {"radius_squared": "1", "chord_class": 2},
        "second": {"radius_squared": "1/2", "chord_class": 4},
        "common_squared_distance": str(first_label),
    }


def audit() -> dict:
    fibres = (
        (
            Fraction(1),
            (
                (Fraction(0), frozenset({0, 1, 3})),
                (Fraction(1, 2), frozenset({2, 4})),
                (Fraction(7, 3), frozenset({0, 5, 6, 8})),
            ),
        ),
        (
            Fraction(5, 3),
            (
                (Fraction(0), frozenset({1, 4})),
                (Fraction(2), frozenset({0, 2, 3, 7, 9})),
            ),
        ),
    )
    return {
        "schema": "amra.erdos1083.partial-cyclotomic-fibre-independent-audit.v1",
        "verdict": "PASS",
        "scope": (
            "Independent sign-class, Cauchy-Davenport, and real-basis "
            "injection audit for prime angular groups. The unchanged "
            "statement is false for general cyclic order."
        ),
        "exhaustive_prime_7": exhaustive_prime_difference_audit(7),
        "partial_fibre_case": partial_fibre_audit(11, fibres),
        "linear_constant_checks": [
            equal_size_linear_constant_audit(7, size)
            for size in (2, 3, 4)
        ] + [
            equal_size_linear_constant_audit(11, size)
            for size in (2, 4, 6)
        ],
        "smallest_composite_counterexample": (
            smallest_composite_cyclic_counterexample()
        ),
        "composite_injection_collision": (
            composite_algebraic_injection_collision()
        ),
        "author_verifier_imported": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
