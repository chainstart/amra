#!/usr/bin/env python3
"""Exact audit for the six-coprime cyclotomic fibre theorem."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import gcd

import sympy as sp

from verify_prime_power_cyclotomic_escape import kneser_row
from verify_rough_order_cyclotomic_escape import canonical_label


Quadratic = tuple[Fraction, Fraction]


def quadratic_label(
    order: int,
    radius_squared: Quadratic,
    step: int,
    height_square: Quadratic,
) -> tuple[Quadratic, ...]:
    """Coefficientwise quotient vector over Q(sqrt(2))."""
    rational_part = canonical_label(
        order,
        radius_squared[0],
        step,
        height_square[0],
    )
    radical_part = canonical_label(
        order,
        radius_squared[1],
        step,
        height_square[1],
    )
    return tuple(zip(rational_part, radical_part))


def signed_relation_grid(order: int) -> dict[str, int]:
    """Exhaust a small positive-rational grid of collision equations."""
    if gcd(order, 6) != 1:
        raise ValueError("the audit order must be coprime to six")
    positives = [Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2)]
    constants = [Fraction(value, 2) for value in range(-12, 13)]
    zero = (Fraction(0),) * int(sp.totient(order))
    checked = 0
    base_labels = {
        (radius, step): canonical_label(
            order,
            radius,
            step,
            Fraction(0),
        )
        for radius in positives
        for step in range(1, (order + 1) // 2)
    }

    # A relation C-R(zeta^d+zeta^-d)+S(zeta^e+zeta^-e)=0
    # is equivalent, up to the rational constant 2R-2S, to equality
    # of two canonical chord-plus-height labels.
    for step_left in range(1, (order + 1) // 2):
        for step_right in range(1, (order + 1) // 2):
            for left in positives:
                for right in positives:
                    for constant in constants:
                        left_label = base_labels[(left, step_left)]
                        right_label_list = list(
                            base_labels[(right, step_right)]
                        )
                        right_label_list[0] += (
                            constant + 2 * left - 2 * right
                        )
                        right_label = tuple(right_label_list)
                        collision = tuple(
                            a - b for a, b in zip(left_label, right_label)
                        )
                        if collision == zero:
                            if not (
                                step_left == step_right
                                and left == right
                                and constant == 0
                            ):
                                raise AssertionError(
                                    "unexpected signed chord relation: "
                                    f"m={order}, d={step_left}, e={step_right}, "
                                    f"R={left}, S={right}, C={constant}"
                                )
                        checked += 1
    return {"order": order, "signed_relations_checked": checked}


def injection_grid(order: int) -> dict[str, int]:
    radii = [Fraction(1), Fraction(3, 2), Fraction(2)]
    heights = [Fraction(0), Fraction(1, 4), Fraction(1), Fraction(9, 4)]
    labels: dict[tuple[Fraction, ...], tuple[Fraction, Fraction, int]] = {}
    for radius in radii:
        for height in heights:
            for step in range(1, (order + 1) // 2):
                vector = canonical_label(order, radius, step, height)
                key = (radius, height, step)
                if vector in labels:
                    raise AssertionError(
                        f"label collision: {labels[vector]} and {key}"
                    )
                labels[vector] = key
    return {"order": order, "distinct_labels_checked": len(labels)}


def quadratic_injection_grid(order: int) -> dict[str, int]:
    radii: list[Quadratic] = [
        (Fraction(2), Fraction(1)),
        (Fraction(3), Fraction(1, 2)),
    ]
    heights: list[Quadratic] = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(1, 2)),
        (Fraction(2), Fraction(1, 3)),
    ]
    labels: dict[tuple[Quadratic, ...], tuple[Quadratic, Quadratic, int]] = {}
    for radius in radii:
        for height in heights:
            for step in range(1, (order + 1) // 2):
                vector = quadratic_label(order, radius, step, height)
                key = (radius, height, step)
                if vector in labels:
                    raise AssertionError(
                        f"quadratic-base collision: {labels[vector]} and {key}"
                    )
                labels[vector] = key
    return {
        "order": order,
        "quadratic_base_distinct_labels_checked": len(labels),
    }


def audit() -> dict[str, object]:
    orders = [5, 25, 35, 55, 65]
    injection_rows = [injection_grid(order) for order in orders]
    quadratic_rows = [
        quadratic_injection_grid(order) for order in (5, 25, 35)
    ]
    relation_rows = [signed_relation_grid(order) for order in (5, 25, 35)]

    subgroup_35 = set(range(0, 35, 7))
    periodic = kneser_row(35, subgroup_35, subgroup_35)
    if periodic["stabilizer_size"] != 5:
        raise AssertionError("order-five stabilizer was not detected")
    if periodic["sign_classes"] != 2:
        raise AssertionError("2/5 sharpness was not detected")

    # Explicit failure at order nine: a_3=3.
    order_nine_left = canonical_label(9, Fraction(2), 3, Fraction(0))
    order_nine_right = canonical_label(9, Fraction(1), 3, Fraction(3))
    if order_nine_left != order_nine_right:
        raise AssertionError("order-nine boundary collision missing")

    # Explicit failure at order eight: a_4=4.
    order_eight_left = canonical_label(8, Fraction(2), 4, Fraction(0))
    order_eight_right = canonical_label(8, Fraction(1), 4, Fraction(4))
    if order_eight_left != order_eight_right:
        raise AssertionError("order-eight boundary collision missing")

    return {
        "schema": "amra.erdos1083.six-coprime-cyclotomic-escape.v1",
        "exact_quotient_arithmetic": True,
        "injection_checks": injection_rows,
        "quadratic_base_field": "Q(sqrt(2))",
        "quadratic_injection_checks": quadratic_rows,
        "signed_relation_checks": relation_rows,
        "order_35_periodic_sharpness": periodic,
        "order_8_collision_verified": True,
        "order_9_collision_verified": True,
        "status": "finite_audit_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
