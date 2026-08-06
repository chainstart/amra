#!/usr/bin/env python3
"""Discovery test for a negative-part Gram bound in the c<0 PLL chamber."""

from __future__ import annotations

from fractions import Fraction
from math import comb
from pathlib import Path
import math
import random
import sys


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_c_zero_fibre import (  # noqa: E402
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_negative_c_all_negative_gram import coefficient, scale  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    schur_substitute,
    variable,
)
from verify_nonnegative_route_chambers import state_polynomial  # noqa: E402


B_EDGE = (0, 4)
ORIENTATIONS = (4, 6)


def row(poly):
    values = tuple(poly.values())
    return {
        "terms": len(poly),
        "positive": sum(value > 0 for value in values),
        "negative": sum(value < 0 for value in values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
    }


def bernstein_basis(slot, degree, index):
    coordinate = variable(slot)
    one_minus = add(constant(1), coordinate, -1)
    return scale(
        multiply(power(coordinate, index), power(one_minus, degree - index)),
        comb(degree, index),
    )


def bernstein_to_power(poly, slots, degrees):
    bases = {
        (slot, index): bernstein_basis(slot, degree, index)
        for slot, degree in zip(slots, degrees)
        for index in range(degree + 1)
    }
    result = {}
    for monomial, value in poly.items():
        base = list(monomial)
        for slot in slots:
            base[slot] = 0
        term = {tuple(base): value}
        for slot in slots:
            term = multiply(term, bases[(slot, monomial[slot])])
        result = add(result, term)
    return result


def bernstein_at_degrees(poly, slots, degrees):
    result = dict(poly)
    for slot, target_degree in zip(slots, degrees):
        assert max(monomial[slot] for monomial in result) <= target_degree
        grouped = {}
        for monomial, value in result.items():
            key = monomial[:slot] + monomial[slot + 1 :]
            grouped.setdefault(key, {})[monomial[slot]] = value
        transformed = {}
        for key, coefficients in grouped.items():
            for index in range(target_degree + 1):
                value = sum(
                    coefficients.get(power_degree, Fraction())
                    * Fraction(
                        comb(index, power_degree),
                        comb(target_degree, power_degree),
                    )
                    for power_degree in range(index + 1)
                )
                if value:
                    monomial = key[:slot] + (index,) + key[slot:]
                    transformed[monomial] = value
        result = transformed
    return result


def evaluate(poly, values):
    powers = [
        [value ** exponent for exponent in range(max(m[slot] for m in poly) + 1)]
        for slot, value in enumerate(values)
    ]
    return sum(
        float(coefficient_value)
        * math.prod(powers[slot][exponent] for slot, exponent in enumerate(monomial))
        for monomial, coefficient_value in poly.items()
    )


def evaluate_bernstein(poly, slots, degrees, values):
    basis_values = {
        (slot, index): comb(degree, index)
        * values[slot] ** index
        * (1 - values[slot]) ** (degree - index)
        for slot, degree in zip(slots, degrees)
        for index in range(degree + 1)
    }
    return sum(
        float(coefficient_value)
        * math.prod(
            basis_values[(slot, monomial[slot])]
            if slot in slots
            else values[slot] ** monomial[slot]
            for slot in range(8)
        )
        for monomial, coefficient_value in poly.items()
    )


def main():
    deletion, connectivity, _, _ = reconstruct_original()
    A = derivative(deletion, (B_EDGE,))
    C = restrict_original_zero(deletion, B_EDGE)
    D = derivative(connectivity, (B_EDGE,))
    E = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(multiply_original(A, E), multiply_original(D, C), -1)
    F = schur_substitute(state_polynomial(delta, tuple("PLL")), tuple("PLL"))
    a0, a1, a2 = (coefficient(F, 7, degree) for degree in range(3))
    beta0 = a0
    beta1 = add(a0, scale(a1, Fraction(1, 2)))
    beta2 = add(add(a0, a1), a2)

    degrees = tuple(max(monomial[slot] for monomial in beta1) for slot in ORIENTATIONS)
    beta1_bernstein = bernstein_transform(beta1, ORIENTATIONS)
    rng = random.Random(1757)
    sample_values = [[
        0.0,
        10 ** rng.uniform(-4, 4),
        10 ** rng.uniform(-4, 4),
        10 ** rng.uniform(-4, 4),
        rng.random(),
        10 ** rng.uniform(-4, 4),
        rng.random(),
        0.0,
    ] for _ in range(120)]
    sample_values.append([
        0.0,
        5183.054463463671,
        2727.0039414690987,
        0.10726807071952653,
        0.01875278353956089,
        4.278666375740978,
        0.6414444368146872,
        0.0,
    ])
    for split_degree in range(3, 21):
        elevated_beta1 = bernstein_at_degrees(
            beta1, ORIENTATIONS, (split_degree, split_degree)
        )
        elevated_negative = {
            monomial: -value
            for monomial, value in elevated_beta1.items()
            if value < 0
        }
        minimum = (float("inf"), None)
        for values in sample_values:
            b0 = evaluate(beta0, values)
            b2 = evaluate(beta2, values)
            negative_value = evaluate_bernstein(
                elevated_negative,
                ORIENTATIONS,
                (split_degree, split_degree),
                values,
            )
            residual_value = b0 * b2 - negative_value * negative_value
            normalized = residual_value / max(abs(b0 * b2), negative_value ** 2, 1e-300)
            if normalized < minimum[0]:
                minimum = (normalized, values)
        print({
            "split_degree": split_degree,
            "negative_coefficients": len(elevated_negative),
            "sample_minimum": minimum,
        }, flush=True)
    return
    positive_bernstein = {
        monomial: value for monomial, value in beta1_bernstein.items() if value > 0
    }
    negative_bernstein = {
        monomial: -value for monomial, value in beta1_bernstein.items() if value < 0
    }
    positive_part = bernstein_to_power(positive_bernstein, ORIENTATIONS, degrees)
    negative_part = bernstein_to_power(negative_bernstein, ORIENTATIONS, degrees)
    assert beta1 == add(positive_part, negative_part, -1)

    positive_product = multiply(beta0, beta2)
    negative_square = multiply(negative_part, negative_part)
    residual = add(positive_product, negative_square, -1)
    residual_bernstein = bernstein_transform(residual, ORIENTATIONS)
    print({
        "degrees": degrees,
        "beta0": row(bernstein_transform(beta0, ORIENTATIONS)),
        "beta1_positive_part": row(positive_bernstein),
        "beta1_negative_part": row(negative_bernstein),
        "beta2": row(bernstein_transform(beta2, ORIENTATIONS)),
        "residual_terms": len(residual),
        "residual_bernstein": row(residual_bernstein),
    }, flush=True)
    rng = random.Random(1757)
    sample_minimum = (float("inf"), None)
    for _ in range(300):
        values = [
            0.0,
            10 ** rng.uniform(-4, 4),
            10 ** rng.uniform(-4, 4),
            10 ** rng.uniform(-4, 4),
            rng.random(),
            10 ** rng.uniform(-4, 4),
            rng.random(),
            0.0,
        ]
        value = evaluate(residual, values)
        scale_value = max(
            abs(evaluate(positive_product, values)),
            abs(evaluate(negative_square, values)),
            1e-300,
        )
        normalized = value / scale_value
        if normalized < sample_minimum[0]:
            sample_minimum = (normalized, (value, values))
    print({"sample_minimum": sample_minimum}, flush=True)
    for target_degree in (7, 8, 10, 12, 16, 20):
        elevated = bernstein_at_degrees(
            residual, ORIENTATIONS, (target_degree, target_degree)
        )
        print({
            "target_degree": target_degree,
            "residual_bernstein": row(elevated),
        }, flush=True)


if __name__ == "__main__":
    main()
