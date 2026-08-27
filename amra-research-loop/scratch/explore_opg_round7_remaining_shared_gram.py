#!/usr/bin/env python3
"""Discovery-only shared-discriminant Gram scan for the four open c<0 orbits."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
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
from verify_negative_c_all_negative_gram import (  # noqa: E402
    coefficient,
    divide_one_minus_variable,
    scale,
)
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    multiply,
)
from verify_negative_c_schur_endpoint import (  # noqa: E402
    schur_substitute,
    uniform_state_polynomial,
)
from verify_shared_page_discriminant import (  # noqa: E402
    C_EDGE,
    X01,
    X02,
    X13,
    X14,
    coefficient as original_coefficient,
    divide_monomial as original_divide_monomial,
)


B_EDGE = (0, 4)


def row(poly):
    values = tuple(poly.values())
    return {
        "terms": len(values),
        "positive": sum(value > 0 for value in values),
        "negative": sum(value < 0 for value in values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
    }


def common_monomial(poly):
    return tuple(min(monomial[slot] for monomial in poly) for slot in range(8))


def divide_monomial(poly, factor):
    return {
        tuple(degree - removed for degree, removed in zip(monomial, factor)): value
        for monomial, value in poly.items()
    }


def evaluate(poly, values):
    return sum(
        float(coefficient_value)
        * __import__("math").prod(
            value ** exponent for value, exponent in zip(values, monomial)
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
    A2 = original_coefficient(delta, X01, 2)
    A1 = original_coefficient(delta, X01, 1)
    A0 = original_coefficient(delta, X01, 0)
    discriminant = add_original(
        multiply_original(A1, A1),
        multiply_original(A2, A0),
        -4,
    )
    divided = original_divide_monomial(
        discriminant,
        {C_EDGE: 2, X02: 2, X13: 2, X14: 2},
    )
    H = {monomial: -value // 4 for monomial, value in divided.items()}

    for state in ("LLR",):
        states = tuple(state)
        schur_A2 = schur_substitute(uniform_state_polynomial(A2, states))
        A2_bernstein = bernstein_transform(schur_A2, [2, 4, 6, 7])
        raw_H = schur_substitute(uniform_state_polynomial(H, states))
        reduced_H = raw_H
        if state[0] == "R":
            reduced_H = divide_one_minus_variable(
                divide_one_minus_variable(reduced_H, 2), 2
            )
        degree = max(monomial[2] for monomial in reduced_H)
        print({
            "state": state,
            "A2": row(A2_bernstein),
            "H_terms": len(reduced_H),
            "s0_degree": degree,
        }, flush=True)
        if state == "LLR":
            rng = random.Random(1757)
            minimum = (float("inf"), None)
            for _ in range(3000):
                values = [
                    0.0,
                    10 ** rng.uniform(-3, 3),
                    rng.random(),
                    10 ** rng.uniform(-3, 3),
                    rng.random(),
                    10 ** rng.uniform(-3, 3),
                    rng.random(),
                    rng.random(),
                ]
                value = evaluate(reduced_H, values)
                if value < minimum[0]:
                    minimum = (value, values)
            print({"state": state, "H_sample_minimum": minimum}, flush=True)
            tau0, tau1, tau2 = (
                coefficient(reduced_H, 7, index) for index in range(3)
            )
            tau_beta0 = tau0
            tau_beta1 = add(tau0, scale(tau1, Fraction(1, 2)))
            tau_beta2 = add(add(tau0, tau1), tau2)
            print({
                "state": state,
                "direction": "tau",
                "beta0": row(bernstein_transform(tau_beta0, [2, 4, 6])),
                "beta1": row(bernstein_transform(tau_beta1, [2, 4, 6])),
                "beta2": row(bernstein_transform(tau_beta2, [2, 4, 6])),
            }, flush=True)
        if degree != 2:
            continue
        a0, a1, a2 = (coefficient(reduced_H, 2, index) for index in range(3))
        beta0 = a0
        beta1 = add(a0, scale(a1, Fraction(1, 2)))
        beta2 = add(add(a0, a1), a2)
        determinant = add(multiply(beta0, beta2), multiply(beta1, beta1), -1)
        common = common_monomial(determinant)
        residual = divide_monomial(determinant, common)
        print({
            "state": state,
            "beta0": row(bernstein_transform(beta0, [4, 6, 7])),
            "beta1": row(bernstein_transform(beta1, [4, 6, 7])),
            "beta2": row(bernstein_transform(beta2, [4, 6, 7])),
            "determinant_terms": len(determinant),
            "determinant_common": common,
            "determinant_bernstein": row(bernstein_transform(residual, [4, 6, 7])),
        }, flush=True)

        if state == "LLR":
            for direction, name in ((4, "t3"), (6, "t4")):
                directional_H = reduced_H
                removed = 0
                while True:
                    try:
                        candidate = divide_one_minus_variable(
                            directional_H, direction
                        )
                    except AssertionError:
                        break
                    directional_H = candidate
                    removed += 1
                direction_degree = max(
                    monomial[direction] for monomial in directional_H
                )
                if direction_degree != 2:
                    print({
                        "state": state,
                        "direction": name,
                        "removed_one_minus": removed,
                        "degree": direction_degree,
                    })
                    continue
                d0, d1, d2 = (
                    coefficient(directional_H, direction, index)
                    for index in range(3)
                )
                gamma0 = d0
                gamma1 = add(d0, scale(d1, Fraction(1, 2)))
                gamma2 = add(add(d0, d1), d2)
                gamma_determinant = add(
                    multiply(gamma0, gamma2),
                    multiply(gamma1, gamma1),
                    -1,
                )
                gamma_common = common_monomial(gamma_determinant)
                gamma_residual = divide_monomial(
                    gamma_determinant, gamma_common
                )
                other_slots = [slot for slot in (2, 4, 6, 7) if slot != direction]
                print({
                    "state": state,
                    "direction": name,
                    "removed_one_minus": removed,
                    "gamma0": row(bernstein_transform(gamma0, other_slots)),
                    "gamma1": row(bernstein_transform(gamma1, other_slots)),
                    "gamma2": row(bernstein_transform(gamma2, other_slots)),
                    "determinant_terms": len(gamma_determinant),
                    "determinant_common": gamma_common,
                    "determinant_bernstein": row(
                        bernstein_transform(gamma_residual, other_slots)
                    ),
                }, flush=True)


if __name__ == "__main__":
    main()
