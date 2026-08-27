#!/usr/bin/env python3
"""Discovery-only corrected shared-discriminant scan of the open c<0 orbits."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
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
    required_denominator_degrees,
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
ORIENTATIONS = (2, 4, 6)


def row(poly, bounded_slots):
    transformed = bernstein_transform(poly, bounded_slots)
    values = tuple(transformed.values())
    return {
        "terms": len(poly),
        "bernstein": len(transformed),
        "positive": sum(value > 0 for value in values),
        "negative": sum(value < 0 for value in values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
    }


def common_monomial(poly):
    return tuple(min(monomial[slot] for monomial in poly) for slot in range(8))


def divide_monomial(poly, factor):
    result = {}
    for monomial, value in poly.items():
        reduced = tuple(degree - removed for degree, removed in zip(monomial, factor))
        assert all(degree >= 0 for degree in reduced)
        result[reduced] = value
    return result


def maximal_one_minus_factors(poly):
    quotient = poly
    removed = {}
    for slot in ORIENTATIONS:
        count = 0
        while True:
            try:
                candidate = divide_one_minus_variable(quotient, slot)
            except AssertionError:
                break
            quotient = candidate
            count += 1
        removed[slot] = count
    return quotient, removed


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

    for state in ("PPP", "PLL", "LLP"):
        states = tuple(state)
        A2_degrees = required_denominator_degrees(A2, states)
        H_degrees = required_denominator_degrees(H, states)
        schur_A2 = schur_substitute(uniform_state_polynomial(A2, states))
        raw_H = schur_substitute(uniform_state_polynomial(H, states))
        reduced_H, removed = maximal_one_minus_factors(raw_H)
        print({
            "state": state,
            "A2_degrees": A2_degrees,
            "H_degrees": H_degrees,
            "A2": row(schur_A2, [2, 4, 6, 7]),
            "raw_H_terms": len(raw_H),
            "removed_one_minus": removed,
            "reduced_H_terms": len(reduced_H),
            "reduced_degrees": [
                max(monomial[slot] for monomial in reduced_H)
                for slot in range(8)
            ],
            "direct_H": row(reduced_H, [2, 4, 6, 7]),
        }, flush=True)

        for direction in ORIENTATIONS:
            if max(monomial[direction] for monomial in reduced_H) != 2:
                continue
            a0, a1, a2 = (
                coefficient(reduced_H, direction, degree) for degree in range(3)
            )
            gamma0 = a0
            gamma1 = add(a0, scale(a1, Fraction(1, 2)))
            gamma2 = add(add(a0, a1), a2)
            determinant = add(
                multiply(gamma0, gamma2),
                multiply(gamma1, gamma1),
                -1,
            )
            common = common_monomial(determinant)
            residual = divide_monomial(determinant, common)
            other_slots = [slot for slot in (*ORIENTATIONS, 7) if slot != direction]
            print({
                "state": state,
                "direction": direction,
                "gamma0": row(gamma0, other_slots),
                "gamma1": row(gamma1, other_slots),
                "gamma2": row(gamma2, other_slots),
                "determinant_terms": len(determinant),
                "determinant_common": common,
                "determinant": row(residual, other_slots),
            }, flush=True)


if __name__ == "__main__":
    main()
