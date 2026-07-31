#!/usr/bin/env python3
"""Exact audit for prime-power cyclotomic fibre escape."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import ceil


def quotient_vector(
    prime: int,
    exponent: int,
    coefficients: list[Fraction],
) -> tuple[Fraction, ...]:
    """Reduce a degree < p^a polynomial modulo Phi_(p^a)."""
    order = prime**exponent
    block = prime ** (exponent - 1)
    degree = (prime - 1) * block
    if len(coefficients) != order:
        raise ValueError("coefficient vector must have length p^a")
    return tuple(
        coefficients[index]
        - coefficients[(prime - 1) * block + index % block]
        for index in range(degree)
    )


def power_vector(
    prime: int,
    exponent: int,
    power: int,
) -> tuple[Fraction, ...]:
    order = prime**exponent
    coefficients = [Fraction(0) for _ in range(order)]
    coefficients[power % order] = Fraction(1)
    return quotient_vector(prime, exponent, coefficients)


def relation_vector(
    prime: int,
    exponent: int,
    residue: int,
) -> tuple[Fraction, ...]:
    order = prime**exponent
    block = prime ** (exponent - 1)
    coefficients = [Fraction(0) for _ in range(order)]
    for multiplier in range(prime):
        coefficients[residue + multiplier * block] = Fraction(1)
    return quotient_vector(prime, exponent, coefficients)


def canonical_label(
    prime: int,
    exponent: int,
    radius_squared: Fraction,
    step: int,
    height_square: Fraction,
) -> tuple[Fraction, ...]:
    """Represent r^2(2-zeta^d-zeta^-d)+h^2 modulo Phi_(p^a)."""
    order = prime**exponent
    coefficients = [Fraction(0) for _ in range(order)]
    coefficients[0] = 2 * radius_squared + height_square
    coefficients[step % order] -= radius_squared
    coefficients[-step % order] -= radius_squared
    return quotient_vector(prime, exponent, coefficients)


def sign_classes(
    order: int,
    anchor: set[int],
    fibre: set[int],
) -> set[int]:
    """Canonical representatives of nonzero differences modulo sign."""
    result: set[int] = set()
    for upper in fibre:
        for lower in anchor:
            difference = (upper - lower) % order
            if difference:
                result.add(min(difference, order - difference))
    return result


def difference_set(order: int, left: set[int], right: set[int]) -> set[int]:
    return {(a - b) % order for a in left for b in right}


def stabilizer(order: int, subset: set[int]) -> set[int]:
    return {
        shift
        for shift in range(order)
        if {(value + shift) % order for value in subset} == subset
    }


def sum_with(order: int, subset: set[int], subgroup: set[int]) -> set[int]:
    return {(value + shift) % order for value in subset for shift in subgroup}


def kneser_row(order: int, left: set[int], right: set[int]) -> dict[str, object]:
    differences = difference_set(order, left, right)
    subgroup = stabilizer(order, differences)
    lower = (
        len(sum_with(order, left, subgroup))
        + len(sum_with(order, right, subgroup))
        - len(subgroup)
    )
    classes = sign_classes(order, right, left)
    class_lower = ceil((lower - 1) / 2)
    if len(differences) < lower:
        raise AssertionError("Kneser lower bound failed")
    if len(classes) < class_lower:
        raise AssertionError("sign-class lower bound failed")
    return {
        "order": order,
        "left_size": len(left),
        "right_size": len(right),
        "difference_size": len(differences),
        "stabilizer_size": len(subgroup),
        "kneser_lower": lower,
        "sign_classes": len(classes),
        "sign_class_lower": class_lower,
    }


def relation_audit(prime: int, exponent: int) -> dict[str, int]:
    order = prime**exponent
    block = prime ** (exponent - 1)
    degree = (prime - 1) * block

    # The first phi(p^a) power vectors are the standard quotient basis.
    first_basis = [
        power_vector(prime, exponent, power) for power in range(degree)
    ]
    standard_basis = []
    for index in range(degree):
        vector = [Fraction(0) for _ in range(degree)]
        vector[index] = Fraction(1)
        standard_basis.append(tuple(vector))
    if first_basis != standard_basis:
        raise AssertionError("quotient basis normalization failed")

    for residue in range(block):
        if any(relation_vector(prime, exponent, residue)):
            raise AssertionError("p-gon relation did not reduce to zero")

    # The relation supports are pairwise disjoint.  Hence they are
    # independent; their count equals m-phi(m), proving they form a basis.
    supports = [
        {residue + multiplier * block for multiplier in range(prime)}
        for residue in range(block)
    ]
    for left_index, left in enumerate(supports):
        if len(left) != prime:
            raise AssertionError("relation support has wrong size")
        for right in supports[left_index + 1 :]:
            if left & right:
                raise AssertionError("relation supports are not disjoint")
    if len(supports) != order - degree:
        raise AssertionError("relation count does not equal nullity")

    return {
        "prime": prime,
        "exponent": exponent,
        "order": order,
        "cyclotomic_degree": degree,
        "relation_nullity": order - degree,
        "relation_basis_size": len(supports),
        "minimum_nonzero_relation_support": prime,
    }


def injection_audit(
    prime: int,
    exponent: int,
    configurations: list[
        tuple[Fraction, list[tuple[Fraction, set[int]]]]
    ],
) -> dict[str, object]:
    order = prime**exponent
    labels: dict[tuple[Fraction, ...], tuple[object, ...]] = {}
    point_count = 0
    exact_class_total = 0
    kneser_lower_total = 0
    rows: list[dict[str, object]] = []

    for radius_squared, fibres in configurations:
        anchor = fibres[0][1]
        for height_index, (height_square, angular_set) in enumerate(fibres):
            classes = sign_classes(order, anchor, angular_set)
            row = kneser_row(order, angular_set, anchor)
            for step in classes:
                vector = canonical_label(
                    prime,
                    exponent,
                    radius_squared,
                    step,
                    height_square,
                )
                key = (radius_squared, height_index, step)
                if vector in labels:
                    raise AssertionError(
                        f"selected-label collision: {labels[vector]} and {key}"
                    )
                labels[vector] = key
            if len(classes) < row["sign_class_lower"]:
                raise AssertionError("Kneser aggregate ledger failed")
            point_count += len(angular_set)
            exact_class_total += len(classes)
            kneser_lower_total += int(row["sign_class_lower"])
            rows.append(row)

    if len(labels) != exact_class_total:
        raise AssertionError("selected-label ledger mismatch")
    return {
        "order": order,
        "point_count": point_count,
        "fibre_count": len(rows),
        "exact_selected_labels": exact_class_total,
        "kneser_class_lower_total": kneser_lower_total,
        "kneser_rows": rows,
    }


def audit() -> dict[str, object]:
    relation_rows = [
        relation_audit(7, 1),
        relation_audit(7, 2),
        relation_audit(11, 2),
    ]

    configurations_49 = [
        (
            Fraction(1),
            [
                (Fraction(0), {0, 1, 7, 19}),
                (Fraction(1, 4), {2, 8, 17, 31}),
                (Fraction(9, 4), {0, 14, 21}),
            ],
        ),
        (
            Fraction(9, 4),
            [
                (Fraction(0), {3, 10, 22}),
                (Fraction(4, 9), {0, 4, 15, 28, 40}),
            ],
        ),
    ]
    configurations_121 = [
        (
            Fraction(2),
            [
                (Fraction(0), {0, 1, 11, 37}),
                (Fraction(1, 9), {4, 19, 44}),
            ],
        ),
        (
            Fraction(25, 9),
            [
                (Fraction(0), {2, 13, 52}),
                (Fraction(16, 25), {0, 7, 29, 63}),
            ],
        ),
    ]
    injection_rows = [
        injection_audit(7, 2, configurations_49),
        injection_audit(11, 2, configurations_121),
    ]

    # Exact periodic sharpness example: the subgroup 7Z/49Z.
    subgroup_49 = set(range(0, 49, 7))
    periodic = kneser_row(49, subgroup_49, subgroup_49)
    if periodic["stabilizer_size"] != 7:
        raise AssertionError("periodic stabilizer was not detected")
    if periodic["sign_classes"] != 3:
        raise AssertionError("periodic sign-class sharpness failed")

    aperiodic = kneser_row(49, {0, 1, 4, 13}, {0, 2, 9, 21})
    if aperiodic["stabilizer_size"] != 1:
        raise AssertionError("aperiodic example acquired a stabilizer")

    # At p=5 the basic p-gon relation itself has five terms, so the
    # support separation used in the theorem is unavailable.
    five_term = relation_audit(5, 2)
    if five_term["minimum_nonzero_relation_support"] != 5:
        raise AssertionError("p=5 boundary witness failed")

    return {
        "schema": "amra.erdos1083.prime-power-cyclotomic-escape.v1",
        "exact_quotient_arithmetic": True,
        "relation_space_checks": relation_rows,
        "injection_checks": injection_rows,
        "periodic_kneser_sharpness": periodic,
        "aperiodic_kneser_check": aperiodic,
        "five_term_boundary": five_term,
        "status": "finite_audit_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
