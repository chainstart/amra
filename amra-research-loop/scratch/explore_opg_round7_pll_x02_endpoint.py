#!/usr/bin/env python3
"""Exact discovery helpers for the remaining PLL x02 certificate.

This is scratch-space code: it reconstructs the small endpoint obstruction
from the original graph polynomials and prints exact Bernstein diagnostics.
"""

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
    constant,
    multiply,
    variable,
)
from verify_negative_c_schur_endpoint import (  # noqa: E402
    schur_substitute,
    uniform_state_polynomial,
)
from verify_mixed_three_negative import divide_polynomial  # noqa: E402
from verify_shared_page_discriminant import (  # noqa: E402
    X02,
    coefficient as original_coefficient,
)


B_EDGE = (0, 4)


def divide_monomial(poly, factor):
    result = {}
    for monomial, value in poly.items():
        reduced = tuple(degree - removed for degree, removed in zip(monomial, factor))
        assert all(degree >= 0 for degree in reduced)
        result[reduced] = value
    return result


def gram(poly, slot):
    assert max(monomial[slot] for monomial in poly) == 2
    a0, a1, a2 = (coefficient(poly, slot, degree) for degree in range(3))
    gamma0 = a0
    gamma1 = add(a0, scale(a1, Fraction(1, 2)))
    gamma2 = add(add(a0, a1), a2)
    determinant = add(
        multiply(gamma0, gamma2),
        multiply(gamma1, gamma1),
        -1,
    )
    return gamma0, gamma1, gamma2, determinant


def row(poly, bounded_slots):
    transformed = bernstein_transform(poly, bounded_slots)
    values = tuple(transformed.values())
    return {
        "terms": len(poly),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
        "bernstein": len(transformed),
        "positive": sum(value > 0 for value in values),
        "negative": sum(value < 0 for value in values),
        "minimum": str(min(values)),
    }


def build():
    deletion, connectivity, _, _ = reconstruct_original()
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(
        multiply_original(a_slope, e_zero),
        multiply_original(d_slope, c_zero),
        -1,
    )

    x02_quadratic = original_coefficient(delta, X02, 2)
    raw = schur_substitute(
        uniform_state_polynomial(
            x02_quadratic,
            tuple("PLL"),
            denominator_degrees=(0, 2, 2),
        )
    )
    reduced = divide_one_minus_variable(divide_one_minus_variable(raw, 4), 6)

    gamma0, gamma1, gamma2, determinant = gram(reduced, 4)
    determinant_common = (0, 4, 2, 3, 0, 2, 0, 0)
    residual = divide_monomial(determinant, determinant_common)

    q0, q3, q4, tau = (variable(slot) for slot in (1, 3, 5, 7))
    schur_factor = add(
        multiply(
            multiply(add(constant(1), tau, -1), q0),
            add(add(multiply(q3, q4), q3), q4),
        ),
        multiply(q3, q4),
    )
    core = divide_polynomial(residual, schur_factor)
    assert residual == multiply(schur_factor, core)

    beta0, beta1, beta2, beta_determinant = gram(core, 2)
    return {
        "delta": delta,
        "x02_quadratic": x02_quadratic,
        "raw": raw,
        "reduced": reduced,
        "t3_gamma0": gamma0,
        "t3_gamma1": gamma1,
        "t3_gamma2": gamma2,
        "t3_determinant": determinant,
        "t3_residual": residual,
        "schur_factor": schur_factor,
        "core": core,
        "s0_beta0": beta0,
        "s0_beta1": beta1,
        "s0_beta2": beta2,
        "s0_determinant": beta_determinant,
    }


def main():
    data = build()
    for name in (
        "reduced",
        "t3_gamma0",
        "t3_gamma2",
        "t3_residual",
        "core",
        "s0_beta0",
        "s0_beta1",
        "s0_beta2",
        "s0_determinant",
    ):
        print(name, row(data[name], [2, 4, 6, 7]), flush=True)

    endpoint = data["s0_beta2"]
    transformed = bernstein_transform(endpoint, [6, 7])
    negative = sorted(
        (monomial, value)
        for monomial, value in transformed.items()
        if value < 0
    )
    print("endpoint_negative_bernstein", negative, flush=True)


if __name__ == "__main__":
    main()
