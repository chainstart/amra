#!/usr/bin/env python3
"""Exact finite audit for the cyclotomic tensor escape theorem."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


def canonical_cyclotomic_vector(
    prime: int,
    radius_squared: Fraction,
    angular_step: int,
    height_term: Fraction,
) -> tuple[Fraction, ...]:
    """Return coefficients modulo 1+zeta+...+zeta^(p-1)=0."""
    coefficients = [Fraction(0) for _ in range(prime)]
    coefficients[0] = 2 * radius_squared + height_term
    coefficients[angular_step] -= radius_squared
    coefficients[prime - angular_step] -= radius_squared

    # Subtract the last coordinate times the all-ones relation.
    pivot = coefficients[-1]
    return tuple(value - pivot for value in coefficients[:-1])


def audit() -> dict[str, object]:
    cases = [
        (
            7,
            {
                Fraction(1): [Fraction(0), Fraction(1), Fraction(4)],
                Fraction(4): [Fraction(0), Fraction(1, 4)],
                Fraction(9, 4): [
                    Fraction(0),
                    Fraction(9, 16),
                    Fraction(25, 16),
                    Fraction(49, 16),
                ],
            },
        ),
        (
            11,
            {
                Fraction(1): [Fraction(0), Fraction(4, 9)],
                Fraction(2): [Fraction(0), Fraction(1), Fraction(9)],
                Fraction(25, 9): [Fraction(0), Fraction(1, 9)],
            },
        ),
        (
            13,
            {
                Fraction(1, 4): [
                    Fraction(0),
                    Fraction(9, 16),
                    Fraction(81, 16),
                ],
                Fraction(9, 4): [
                    Fraction(0),
                    Fraction(1),
                    Fraction(4),
                    Fraction(9),
                ],
            },
        ),
    ]
    rows = []
    total_labels = 0
    for prime, fibres in cases:
        labels = {}
        for radius_squared, anchored_height_squares in fibres.items():
            for step in range(1, (prime - 1) // 2 + 1):
                for height_index, height_term in enumerate(
                    anchored_height_squares
                ):
                    vector = canonical_cyclotomic_vector(
                        prime,
                        radius_squared,
                        step,
                        height_term,
                    )
                    key = (radius_squared, step, height_index)
                    if vector in labels:
                        raise AssertionError(
                            f"collision: {labels[vector]} and {key}"
                        )
                    labels[vector] = key

        total_heights = sum(len(heights) for heights in fibres.values())
        expected = (prime - 1) // 2 * total_heights
        if len(labels) != expected:
            raise AssertionError("label count does not match theorem")
        total_labels += expected
        rows.append(
            {
                "prime": prime,
                "radius_count": len(fibres),
                "radius_dependent_height_counts": [
                    len(heights) for heights in fibres.values()
                ],
                "distinct_audited_labels": expected,
                "point_count": prime * total_heights,
            }
        )

    return {
        "schema": "amra.erdos1083.cyclotomic-tensor-escape.v1",
        "exact_quotient_arithmetic": True,
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
