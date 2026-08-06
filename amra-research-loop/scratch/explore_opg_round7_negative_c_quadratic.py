#!/usr/bin/env python3
"""Discovery diagnostics for the six unresolved c-negative chamber orbits."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns/opg-1757-transverse-lift-round7/evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_c_zero_fibre import (  # noqa: E402
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    multiply,
    schur_substitute,
)
from verify_nonnegative_route_chambers import state_polynomial  # noqa: E402


B_EDGE = (0, 4)
TAU = 7


def coefficient(poly, slot, degree):
    result = {}
    for monomial, value in poly.items():
        if monomial[slot] != degree:
            continue
        reduced = list(monomial)
        reduced[slot] = 0
        result[tuple(reduced)] = value
    return result


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {monomial: scalar * value for monomial, value in poly.items() if value}


def sign_row(poly):
    values = tuple(poly.values())
    gcd = [min(monomial[slot] for monomial in poly) for slot in range(8)]
    return {
        "terms": len(values),
        "negative": sum(value < 0 for value in values),
        "positive": sum(value > 0 for value in values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
        "monomial_gcd": gcd,
    }


def main():
    deletion, connectivity, _, _ = reconstruct_original()
    A = derivative(deletion, (B_EDGE,))
    C = restrict_original_zero(deletion, B_EDGE)
    D = derivative(connectivity, (B_EDGE,))
    E = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(multiply_original(A, E), multiply_original(D, C), -1)

    for state in ("PPP", "PLP", "PLL", "LLP", "LLL", "LLR"):
        states = tuple(state)
        raw = schur_substitute(state_polynomial(delta, states), states)
        activity_slots = [
            2 + 2 * index for index, sign in enumerate(states) if sign != "P"
        ]
        poly = bernstein_transform(raw, activity_slots)
        assert max(monomial[TAU] for monomial in poly) == 2
        a0, a1, a2 = (coefficient(poly, TAU, degree) for degree in range(3))
        beta0 = a0
        beta1 = add(a0, scale(a1, Fraction(1, 2)))
        beta2 = add(add(a0, a1), a2)
        derivative_at_one = add(a1, scale(a2, 2))
        print({
            "state": state,
            "activity_bernstein_terms": len(poly),
            "beta0": sign_row(beta0),
            "beta1": sign_row(beta1),
            "beta2": sign_row(beta2),
            "tau_quadratic_coefficient": sign_row(a2),
            "tau_derivative_at_zero": sign_row(a1),
            "tau_derivative_at_one": sign_row(derivative_at_one),
        }, flush=True)

        endpoint_c = schur_substitute(state_polynomial(C, states), states)
        endpoint_c = add(
            add(coefficient(endpoint_c, TAU, 0), coefficient(endpoint_c, TAU, 1)),
            coefficient(endpoint_c, TAU, 2),
        )
        negative_c_endpoint = bernstein_transform(
            scale(endpoint_c, -1),
            activity_slots,
        )
        print({
            "state": state,
            "minus_C_at_detK_zero": sign_row(negative_c_endpoint),
        }, flush=True)

        if state == "PLL":
            raw_a0, raw_a1, raw_a2 = (
                coefficient(raw, TAU, degree) for degree in range(3)
            )
            raw_beta0 = raw_a0
            raw_beta1 = add(raw_a0, scale(raw_a1, Fraction(1, 2)))
            raw_beta2 = add(add(raw_a0, raw_a1), raw_a2)
            determinant = add(
                multiply(raw_beta0, raw_beta2),
                multiply(raw_beta1, raw_beta1),
                -1,
            )
            transformed_determinant = bernstein_transform(
                determinant,
                activity_slots,
            )
            print({
                "state": state,
                "tau_gram_determinant": sign_row(transformed_determinant),
                "ordinary_determinant_terms": len(determinant),
            }, flush=True)


if __name__ == "__main__":
    main()
