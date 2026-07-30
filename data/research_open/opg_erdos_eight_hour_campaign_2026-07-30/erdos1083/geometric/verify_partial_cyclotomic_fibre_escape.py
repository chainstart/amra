#!/usr/bin/env python3
"""Exact finite audit for the partial cyclotomic fibre escape theorem."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


Quadratic = tuple[Fraction, Fraction]


def canonical_vector(
    prime: int,
    radius_squared: Fraction,
    step: int,
    height_square: Fraction,
) -> tuple[Fraction, ...]:
    """Represent r^2(2-zeta^d-zeta^-d)+h^2 modulo Phi_p."""
    coefficients = [Fraction(0) for _ in range(prime)]
    coefficients[0] = 2 * radius_squared + height_square
    coefficients[step] -= radius_squared
    coefficients[prime - step] -= radius_squared
    pivot = coefficients[-1]
    return tuple(value - pivot for value in coefficients[:-1])


def canonical_quadratic_vector(
    prime: int,
    radius_squared: Quadratic,
    step: int,
    height_square: Quadratic,
) -> tuple[Quadratic, ...]:
    """The same quotient vector over Q(sqrt(2)), coefficientwise."""
    coefficients = [
        (Fraction(0), Fraction(0)) for _ in range(prime)
    ]
    coefficients[0] = (
        2 * radius_squared[0] + height_square[0],
        2 * radius_squared[1] + height_square[1],
    )
    for exponent in (step, prime - step):
        coefficients[exponent] = (
            coefficients[exponent][0] - radius_squared[0],
            coefficients[exponent][1] - radius_squared[1],
        )
    pivot = coefficients[-1]
    return tuple(
        (value[0] - pivot[0], value[1] - pivot[1])
        for value in coefficients[:-1]
    )


def sign_classes(
    prime: int,
    anchor: set[int],
    fibre: set[int],
) -> set[int]:
    """Canonical representatives of nonzero differences modulo sign."""
    result = set()
    for upper in fibre:
        for lower in anchor:
            difference = (upper - lower) % prime
            if difference:
                result.add(min(difference, prime - difference))
    return result


def audit() -> dict[str, object]:
    cases = [
        (
            11,
            {
                Fraction(1): [
                    (Fraction(0), {0, 1, 4}),
                    (Fraction(1), {2, 3, 7}),
                    (Fraction(9, 4), {0, 5}),
                ],
                Fraction(9, 4): [
                    (Fraction(0), {1, 2}),
                    (Fraction(4, 9), {0, 3, 6, 8}),
                ],
            },
        ),
        (
            13,
            {
                Fraction(2): [
                    (Fraction(0), {0, 2, 5, 9}),
                    (Fraction(1, 4), {1, 4, 8}),
                    (Fraction(25, 16), {0, 6, 10, 11, 12}),
                ],
                Fraction(25, 9): [
                    (Fraction(0), {3, 7, 8}),
                    (Fraction(9, 16), {0, 2}),
                    (Fraction(49, 16), {1, 5, 9, 12}),
                ],
            },
        ),
    ]

    rows = []
    total_labels = 0
    for prime, radii in cases:
        labels: dict[tuple[Fraction, ...], tuple[object, ...]] = {}
        cauchy_lower_total = 0
        exact_class_total = 0
        point_count = 0
        fibre_sizes = []

        for radius_squared, fibres in radii.items():
            anchor = fibres[0][1]
            for height_index, (height_square, angular_set) in enumerate(
                fibres
            ):
                classes = sign_classes(prime, anchor, angular_set)
                minimum_difference_count = min(
                    prime,
                    len(anchor) + len(angular_set) - 1,
                )
                cauchy_lower = (minimum_difference_count - 1 + 1) // 2
                if len(classes) < cauchy_lower:
                    raise AssertionError("Cauchy--Davenport bound failed")

                for step in classes:
                    vector = canonical_vector(
                        prime,
                        radius_squared,
                        step,
                        height_square,
                    )
                    key = (radius_squared, height_index, step)
                    if vector in labels:
                        raise AssertionError(
                            f"label collision: {labels[vector]} and {key}"
                        )
                    labels[vector] = key

                exact_class_total += len(classes)
                cauchy_lower_total += cauchy_lower
                point_count += len(angular_set)
                fibre_sizes.append(len(angular_set))

        if len(labels) != exact_class_total:
            raise AssertionError("exact class ledger mismatch")
        if exact_class_total < cauchy_lower_total:
            raise AssertionError("aggregate lower bound failed")

        total_labels += exact_class_total
        rows.append(
            {
                "prime": prime,
                "radius_count": len(radii),
                "fibre_sizes": fibre_sizes,
                "point_count": point_count,
                "cauchy_davenport_lower_bound": cauchy_lower_total,
                "exact_audited_labels": exact_class_total,
            }
        )

    # A non-rational base-field audit.  Q(sqrt(2)) is disjoint from
    # Q(zeta_7), so Phi_7 remains irreducible.  The pairs below encode
    # a+b*sqrt(2); all chosen radius and height squares are positive.
    quadratic_fibres = {
        (Fraction(2), Fraction(1)): [
            ((Fraction(0), Fraction(0)), {0, 1, 3}),
            ((Fraction(1), Fraction(1, 2)), {1, 2, 5}),
        ],
        (Fraction(3), Fraction(1, 2)): [
            ((Fraction(0), Fraction(0)), {0, 2}),
            ((Fraction(2), Fraction(1, 3)), {1, 4, 6}),
        ],
    }
    quadratic_labels: dict[
        tuple[Quadratic, ...], tuple[object, ...]
    ] = {}
    for radius_squared, fibres in quadratic_fibres.items():
        anchor = fibres[0][1]
        for height_index, (height_square, angular_set) in enumerate(
            fibres
        ):
            for step in sign_classes(7, anchor, angular_set):
                vector = canonical_quadratic_vector(
                    7,
                    radius_squared,
                    step,
                    height_square,
                )
                key = (radius_squared, height_index, step)
                if vector in quadratic_labels:
                    raise AssertionError(
                        "quadratic-base label collision: "
                        f"{quadratic_labels[vector]} and {key}"
                    )
                quadratic_labels[vector] = key

    return {
        "schema": "amra.erdos1083.partial-cyclotomic-fibre-escape.v1",
        "exact_quotient_arithmetic": True,
        "quadratic_base_field": "Q(sqrt(2))",
        "quadratic_base_distinct_label_checks": len(quadratic_labels),
        "cases": rows,
        "total_distinct_label_checks": total_labels,
        "status": "finite_audit_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
