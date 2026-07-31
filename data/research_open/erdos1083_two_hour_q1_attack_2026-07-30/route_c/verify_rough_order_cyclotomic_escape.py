#!/usr/bin/env python3
"""Exact audit for rough-order cyclotomic fibre escape."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import gcd

import sympy as sp

from verify_prime_power_cyclotomic_escape import (
    canonical_label as prime_power_label,
)
from verify_prime_power_cyclotomic_escape import kneser_row, sign_classes


X = sp.Symbol("x")


def to_fraction(value: sp.Rational) -> Fraction:
    rational = sp.Rational(value)
    return Fraction(int(rational.p), int(rational.q))


def canonical_label(
    order: int,
    radius_squared: Fraction,
    step: int,
    height_square: Fraction,
) -> tuple[Fraction, ...]:
    """Reduce a selected label modulo Phi_m using exact arithmetic."""
    cyclotomic = sp.Poly(sp.cyclotomic_poly(order, X), X, domain=sp.QQ)
    polynomial = sp.Poly(
        sp.Rational(2 * radius_squared + height_square)
        - sp.Rational(radius_squared) * X ** (step % order)
        - sp.Rational(radius_squared) * X ** ((-step) % order),
        X,
        domain=sp.QQ,
    )
    remainder = polynomial.rem(cyclotomic)
    return tuple(
        to_fraction(remainder.nth(index))
        for index in range(cyclotomic.degree())
    )


def polynomial_remainder(
    order: int,
    exponents: set[int],
) -> tuple[Fraction, ...]:
    cyclotomic = sp.Poly(sp.cyclotomic_poly(order, X), X, domain=sp.QQ)
    polynomial = sp.Poly(
        sum(X ** (exponent % order) for exponent in exponents),
        X,
        domain=sp.QQ,
    )
    remainder = polynomial.rem(cyclotomic)
    return tuple(
        to_fraction(remainder.nth(index))
        for index in range(cyclotomic.degree())
    )


def mann_arithmetic_row(order: int) -> dict[str, object]:
    primorials = {1: 1, 2: 2, 3: 6, 4: 6, 5: 30}
    coprime_checks = {
        terms: gcd(order, primorial) == 1
        for terms, primorial in primorials.items()
    }
    if not all(coprime_checks.values()):
        raise AssertionError("order does not satisfy five-term Mann rigidity")
    return {
        "order": order,
        "gcd_with_30": gcd(order, 30),
        "short_relation_coprime_checks": coprime_checks,
    }


def injection_audit(
    order: int,
    configurations: list[
        tuple[Fraction, list[tuple[Fraction, set[int]]]]
    ],
) -> dict[str, object]:
    labels: dict[tuple[Fraction, ...], tuple[object, ...]] = {}
    exact_class_total = 0
    kneser_lower_total = 0
    point_count = 0

    for radius_squared, fibres in configurations:
        anchor = fibres[0][1]
        for height_index, (height_square, angular_set) in enumerate(fibres):
            classes = sign_classes(order, anchor, angular_set)
            row = kneser_row(order, angular_set, anchor)
            for step in classes:
                vector = canonical_label(
                    order,
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
            exact_class_total += len(classes)
            kneser_lower_total += int(row["sign_class_lower"])
            point_count += len(angular_set)

    if len(labels) != exact_class_total:
        raise AssertionError("selected-label ledger mismatch")
    return {
        "order": order,
        "point_count": point_count,
        "exact_selected_labels": exact_class_total,
        "kneser_class_lower_total": kneser_lower_total,
    }


def audit() -> dict[str, object]:
    rough_orders = [77, 91, 143]
    mann_rows = [mann_arithmetic_row(order) for order in rough_orders]

    configurations = {
        77: [
            (
                Fraction(1),
                [
                    (Fraction(0), {0, 1, 7, 19}),
                    (Fraction(1, 4), {2, 8, 31, 54}),
                    (Fraction(9, 4), {0, 14, 33}),
                ],
            ),
            (
                Fraction(9, 4),
                [
                    (Fraction(0), {3, 12, 29}),
                    (Fraction(4, 9), {0, 5, 24, 48}),
                ],
            ),
        ],
        91: [
            (
                Fraction(2),
                [
                    (Fraction(0), {0, 1, 13, 37}),
                    (Fraction(1, 9), {4, 19, 44}),
                ],
            ),
            (
                Fraction(25, 9),
                [
                    (Fraction(0), {2, 15, 52}),
                    (Fraction(16, 25), {0, 7, 29, 63}),
                ],
            ),
        ],
        143: [
            (
                Fraction(3, 2),
                [
                    (Fraction(0), {0, 11, 28}),
                    (Fraction(4, 25), {3, 42, 97, 121}),
                ],
            ),
        ],
    }
    injection_rows = [
        injection_audit(order, configurations[order])
        for order in rough_orders
    ]

    # The general quotient implementation agrees with the elementary
    # prime-power reducer on every unoriented order-49 chord.
    comparisons = 0
    for step in range(1, 25):
        general = canonical_label(49, Fraction(9, 4), step, Fraction(4, 9))
        elementary = prime_power_label(
            7,
            2,
            Fraction(9, 4),
            step,
            Fraction(4, 9),
        )
        if general != elementary:
            raise AssertionError("general and prime-power quotients disagree")
        comparisons += 1

    # The order-ell subgroup gives equality in the uniform constant.
    subgroup_77 = set(range(0, 77, 11))
    periodic = kneser_row(77, subgroup_77, subgroup_77)
    if periodic["stabilizer_size"] != 7:
        raise AssertionError("least-prime subgroup stabilizer missing")
    if periodic["sign_classes"] != 3:
        raise AssertionError("sharp sign-class constant missing")

    # At order 35 the embedded order-5 polygon is a five-term relation.
    five_term_support = set(range(0, 35, 7))
    five_term_remainder = polynomial_remainder(35, five_term_support)
    if any(five_term_remainder):
        raise AssertionError("order-35 five-term boundary did not vanish")

    return {
        "schema": "amra.erdos1083.rough-order-cyclotomic-escape.v1",
        "exact_quotient_arithmetic": True,
        "mann_arithmetic_checks": mann_rows,
        "injection_checks": injection_rows,
        "prime_power_quotient_comparisons": comparisons,
        "periodic_sharpness": periodic,
        "order_35_five_term_boundary_support": len(five_term_support),
        "status": "finite_audit_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
