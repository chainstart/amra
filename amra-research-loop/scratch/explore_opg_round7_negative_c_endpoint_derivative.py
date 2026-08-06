#!/usr/bin/env python3
"""Discovery diagnostics for the c-Schur endpoint derivative."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


EVIDENCE = Path(__file__).parents[1] / "campaigns/opg-1757-transverse-lift-round7/evidence"
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


def common_monomial(poly):
    return tuple(min(monomial[slot] for monomial in poly) for slot in range(8))


def divide_monomial(poly, factor):
    return {
        tuple(degree - removed for degree, removed in zip(monomial, factor)): coefficient
        for monomial, coefficient in poly.items()
    }


def row(poly):
    values = tuple(poly.values())
    return {
        "terms": len(poly),
        "negative": sum(value < 0 for value in values),
        "positive": sum(value > 0 for value in values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
        "gcd": common_monomial(poly),
    }


def main():
    deletion, connectivity, _, _ = reconstruct_original()
    A = derivative(deletion, (B_EDGE,))
    C = restrict_original_zero(deletion, B_EDGE)
    D = derivative(connectivity, (B_EDGE,))
    E = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(multiply_original(A, E), multiply_original(D, C), -1)

    for state in ("PLL", "LLP", "PPP"):
        states = tuple(state)
        poly = schur_substitute(state_polynomial(delta, states), states)
        a1 = coefficient(poly, TAU, 1)
        a2 = coefficient(poly, TAU, 2)
        H = scale(add(a1, scale(a2, 2)), -1)
        factor = common_monomial(H)
        H = divide_monomial(H, factor)
        activity_slots = [
            2 + 2 * index for index, sign in enumerate(states) if sign != "P"
        ]
        transformed = bernstein_transform(H, activity_slots)
        print({"state": state, "H=-F'(1)": row(H), "activity_bernstein": row(transformed)}, flush=True)
        for slot in range(1, 7):
            degree = max(monomial[slot] for monomial in H)
            slices = [
                row(bernstein_transform(coefficient(H, slot, exponent), activity_slots))
                for exponent in range(degree + 1)
            ]
            print({"state": state, "slot": slot, "degree": degree, "slices": slices}, flush=True)


if __name__ == "__main__":
    main()
