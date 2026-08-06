#!/usr/bin/env python3
"""Discovery-only numerical falsification of direct tau-Gram candidates."""

from __future__ import annotations

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
from verify_negative_c_direct_chambers import add, schur_substitute  # noqa: E402
from verify_nonnegative_route_chambers import state_polynomial  # noqa: E402


B_EDGE = (0, 4)


def evaluate(poly, values):
    degrees = [max(monomial[slot] for monomial in poly) for slot in range(8)]
    powers = [
        [value ** exponent for exponent in range(degree + 1)]
        for value, degree in zip(values, degrees)
    ]
    return sum(
        float(coefficient_value)
        * math.prod(powers[slot][exponent] for slot, exponent in enumerate(monomial))
        for monomial, coefficient_value in poly.items()
    )


def main():
    deletion, connectivity, _, _ = reconstruct_original()
    A = derivative(deletion, (B_EDGE,))
    C = restrict_original_zero(deletion, B_EDGE)
    D = derivative(connectivity, (B_EDGE,))
    E = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(multiply_original(A, E), multiply_original(D, C), -1)
    rng = random.Random(1757)

    for state in ("PLL",):
        states = tuple(state)
        raw = schur_substitute(state_polynomial(delta, states), states)
        a0, a1, a2 = (coefficient(raw, 7, degree) for degree in range(3))
        beta0 = a0
        beta1 = add(a0, scale(a1, 1 / 2))
        beta2 = add(add(a0, a1), a2)
        minimum = (float("inf"), None)
        negative_middle_count = 0
        negative_middle_minimum_determinant = (float("inf"), None)
        minimum_middle = (float("inf"), None)
        minimum_quadratic = (float("inf"), None)
        for _ in range(12000):
            values = [
                0.0,
                10 ** rng.uniform(-4, 4),
                rng.random(),
                10 ** rng.uniform(-4, 4),
                rng.random(),
                10 ** rng.uniform(-4, 4),
                rng.random(),
                0.0,
            ]
            b0 = evaluate(beta0, values)
            b1 = evaluate(beta1, values)
            b2 = evaluate(beta2, values)
            determinant = b0 * b2 - b1 * b1
            normalized = determinant / max(abs(b0 * b2), b1 * b1, 1e-300)
            if normalized < minimum[0]:
                minimum = (normalized, (b0, b1, b2, determinant, values))
            middle_normalized = b1 / max(math.sqrt(abs(b0 * b2)), 1e-300)
            if middle_normalized < minimum_middle[0]:
                minimum_middle = (middle_normalized, (b0, b1, b2, values))
            if b1 < 0:
                negative_middle_count += 1
                if normalized < negative_middle_minimum_determinant[0]:
                    negative_middle_minimum_determinant = (
                        normalized,
                        (b0, b1, b2, determinant, values),
                    )
            tau_star = max(0.0, min(1.0, (b0 - b1) / (b0 - 2 * b1 + b2)))
            value_star = (
                (1 - tau_star) ** 2 * b0
                + 2 * tau_star * (1 - tau_star) * b1
                + tau_star ** 2 * b2
            )
            normalized_star = value_star / max(abs(b0), abs(b1), abs(b2), 1e-300)
            if normalized_star < minimum_quadratic[0]:
                minimum_quadratic = (
                    normalized_star,
                    (tau_star, value_star, b0, b1, b2, values),
                )
        print({
            "state": state,
            "minimum_normalized_determinant": minimum,
            "negative_middle_count": negative_middle_count,
            "negative_middle_minimum_determinant": negative_middle_minimum_determinant,
            "minimum_normalized_middle": minimum_middle,
            "minimum_normalized_quadratic": minimum_quadratic,
        }, flush=True)


if __name__ == "__main__":
    main()
