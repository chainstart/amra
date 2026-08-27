#!/usr/bin/env python3
"""Discovery-only exact witnesses against two over-strong remaining-c certificates."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
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
from verify_negative_c_direct_chambers import add, multiply, schur_substitute  # noqa: E402
from verify_negative_c_schur_endpoint import (  # noqa: E402
    schur_substitute as uniform_schur_substitute,
    uniform_state_polynomial,
)
from verify_nonnegative_route_chambers import state_polynomial  # noqa: E402
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


def evaluate(poly, values):
    return sum(
        coefficient_value
        * product_value(
            value ** exponent for value, exponent in zip(values, monomial)
        )
        for monomial, coefficient_value in poly.items()
    )


def product_value(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


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
    llr_H = uniform_schur_substitute(uniform_state_polynomial(H, tuple("LLR")))

    q_values = (Fraction(1, 4), Fraction(1), Fraction(4), Fraction(16))
    bounded_values = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4))
    llr_witness = None
    for q0, q3, q4 in product(q_values, repeat=3):
        for s0, t3, t4, tau in product(bounded_values, repeat=4):
            values = (Fraction(0), q0, s0, q3, t3, q4, t4, tau)
            value = evaluate(llr_H, values)
            if value < 0:
                llr_witness = (values, value)
                break
        if llr_witness:
            break

    pll_F = schur_substitute(state_polynomial(delta, tuple("PLL")), tuple("PLL"))
    a0, a1, a2 = (coefficient(pll_F, 7, degree) for degree in range(3))
    beta0 = a0
    beta1 = add(a0, scale(a1, Fraction(1, 2)))
    beta2 = add(add(a0, a1), a2)
    gram = add(multiply(beta0, beta2), multiply(beta1, beta1), -1)
    pll_witness = None
    direct_values = (
        Fraction(1, 100), Fraction(1, 10), Fraction(1), Fraction(10)
    )
    direct_bounded = (
        Fraction(1, 100), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)
    )
    for x01, x02, q3, q4 in product(direct_values, repeat=4):
        for t3, t4 in product(direct_bounded, repeat=2):
            values = (Fraction(0), x01, x02, q3, t3, q4, t4, Fraction(0))
            b0 = evaluate(beta0, values)
            b1 = evaluate(beta1, values)
            b2 = evaluate(beta2, values)
            determinant = b0 * b2 - b1 * b1
            if b0 > 0 and b1 > 0 and b2 > 0 and determinant < 0:
                pll_witness = (values, b0, b1, b2, determinant)
                break
        if pll_witness:
            break

    print({"LLR_H_negative": llr_witness})
    print({"PLL_positive_middle_negative_gram": pll_witness})
    original_llr_values = (
        Fraction(-1, 4),
        Fraction(2, 3),
        Fraction(0),
        Fraction(-1, 52),
        Fraction(-1, 2),
        Fraction(2, 3),
        Fraction(3, 2),
        Fraction(-1, 4),
    )
    print({
        "LLR_original": {
            "values": original_llr_values,
            "A2": evaluate(A2, original_llr_values),
            "H": evaluate(H, original_llr_values),
            "discriminant": evaluate(discriminant, original_llr_values),
            "Delta_b": evaluate(delta, original_llr_values),
        }
    })


if __name__ == "__main__":
    main()
