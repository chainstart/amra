#!/usr/bin/env python3
"""Exact certificate for the universal even second-active Newton row.

The written proof is in ``EVEN_SECOND_ACTIVE_UNIVERSAL_THEOREM.md``.
Finite expansions here audit the fixed kernels and transcription; the
all-parameter step comes from the displayed four-layer decomposition.
"""

from __future__ import annotations

import sympy as sp

from verify_even_second_active_partial import (
    BETA,
    N,
    S,
    X,
    certify_low_bulk_columns,
    certify_top_six,
    choose_fixed,
    coefficients,
    j3_direct,
    j_coefficient,
    k3,
    k4,
    k5,
    power_kernel_coefficient,
)


def y_recurrence_kernels() -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    """Return A5, A4, T3, T2 in the recurrence for Y_s."""

    b = BETA
    u2, u3, u4, u5 = (1 + j * b for j in range(2, 6))
    lam = lambda value: 1 + value * b
    a5 = sp.expand(k5(S + 1) - k5(S))
    a4 = sp.expand(
        3
        * (
            u5**2 * lam(S) ** 2 * k4(S)
            - u4**2 * lam(S + 1) ** 2 * k4(S + 1)
        )
    )
    t3 = sp.expand(
        -6 * (S - 3) * S**2 * b**4 * lam(S) ** 2 * u3**2 * k3(S)
        + 6
        * (S - 4)
        * (S - 1) ** 2
        * b**4
        * u5**2
        * lam(S - 1) ** 2
        * k3(S - 1)
    )
    t2 = sp.expand(
        6 * (S - 3) * S**2 * b**4 * lam(S) ** 4 * u2**4
        - 6
        * (S - 4)
        * (S - 1) ** 2
        * b**4
        * u5**2
        * lam(S - 1) ** 4
        * u2**2
    )
    return a5, a4, t3, t2


def positive_shift_count(expression: sp.Expr, start: int = 8) -> int:
    polynomial = sp.Poly(sp.expand(expression), BETA)
    count = 0
    for degree in range(polynomial.degree() + 1):
        coefficient = polynomial.coeff_monomial(BETA**degree)
        if coefficient == 0:
            continue
        shifted = sp.Poly(sp.expand(coefficient.subs(S, X + start)), X)
        if any(value <= 0 for value in shifted.all_coeffs()):
            raise AssertionError((degree, shifted.as_expr()))
        count += len(shifted.all_coeffs())
    return count


def initial_four_layer_kernel(
    a5: sp.Expr, a4: sp.Expr, t3: sp.Expr, t2: sp.Expr
) -> sp.Expr:
    u2 = 1 + 2 * BETA
    length = 2 * S - 10
    result = sp.expand(u2**4 * t2)
    for r in range(4):
        layer = sp.expand(3**r * a5 + 2**r * a4 + t3)
        result += (
            choose_fixed(length, r)
            * BETA**r
            * u2 ** (4 - r)
            * layer
        )
    return sp.expand(result)


def audit_four_layer_recurrence() -> dict[str, int]:
    a5, a4, t3, t2 = y_recurrence_kernels()
    layer4 = sp.expand(81 * a5 + 16 * a4 + t3)
    growth = sp.expand(81 * a5 + 8 * a4)
    initial = initial_four_layer_kernel(a5, a4, t3, t2)

    counts = {
        "delta_k5_positive_monomials": positive_shift_count(a5),
        "layer4_positive_monomials": positive_shift_count(layer4),
        "layer_growth_positive_monomials": positive_shift_count(growth),
        "initial_kernel_positive_monomials": positive_shift_count(initial),
    }
    expected = {
        "delta_k5_positive_monomials": 36,
        "layer4_positive_monomials": 59,
        "layer_growth_positive_monomials": 52,
        "initial_kernel_positive_monomials": 112,
    }
    if counts != expected:
        raise AssertionError((counts, expected))
    return counts


def y_direct(s: int) -> sp.Poly:
    b = BETA
    u = s - 1
    expression = (
        (1 + 5 * b) ** (2 * s - 12) * k5(s)
        - 3 * (1 + s * b) ** 2 * (1 + 4 * b) ** (2 * s - 10) * k4(s)
        - 6
        * (s - 4)
        * u**2
        * b**4
        * (1 + u * b) ** 2
        * j3_direct(u).as_expr()
    )
    return sp.Poly(sp.expand(expression), b)


def y_coefficient(degree: int) -> sp.Expr:
    """Exact fixed-degree coefficient [beta^degree] Y_s."""

    u = S - 1
    leading = power_kernel_coefficient(
        5, 2 * S - 12, coefficients(k5(S)), degree
    )
    fourth = 3 * power_kernel_coefficient(
        4,
        2 * S - 10,
        coefficients((1 + S * BETA) ** 2 * k4(S)),
        degree,
    )
    boundary_kernel = (
        j_coefficient(u, degree - 4)
        + 2 * u * j_coefficient(u, degree - 5)
        + u**2 * j_coefficient(u, degree - 6)
    )
    return sp.cancel(
        leading - fourth - 6 * (S - 4) * u**2 * boundary_kernel
    )


def audit_tail_induction() -> dict[str, int]:
    boundary_monomials = 0
    for degree in (14, 15):
        shifted = sp.Poly(
            sp.expand(y_coefficient(degree).subs(S, N + 8)), N
        )
        if any(value <= 0 for value in shifted.all_coeffs()):
            raise AssertionError((degree, shifted.as_expr()))
        boundary_monomials += len(shifted.all_coeffs())
    if boundary_monomials != 31:
        raise AssertionError(boundary_monomials)

    base7 = y_direct(7)
    if base7.coeff_monomial(BETA**14) != 6462889978:
        raise AssertionError("Y_7 top boundary changed")
    base8 = y_direct(8)
    expected = {
        14: 774777037056,
        15: 1034570170784,
        16: 600055653616,
    }
    for degree, value in expected.items():
        if base8.coeff_monomial(BETA**degree) != value:
            raise AssertionError((degree, base8.coeff_monomial(BETA**degree)))

    # Direct full-polynomial recurrence checks guard all signs and shifts in
    # the four fixed kernels.  The universal identity is derived in the text.
    a5, a4, t3, t2 = y_recurrence_kernels()
    u2, u3, u4, u5 = (1 + j * BETA for j in range(2, 6))
    recurrence_coefficients = 0
    for s in range(8, 13):
        length = 2 * s - 10
        direct = sp.Poly(
            sp.expand(
                y_direct(s + 1).as_expr() - u5**2 * y_direct(s).as_expr()
            ),
            BETA,
        )
        reconstructed = sp.Poly(
            sp.expand(
                u5**length * a5.subs(S, s)
                + u4**length * a4.subs(S, s)
                + u3**length * t3.subs(S, s)
                + u2**length * t2.subs(S, s)
            ),
            BETA,
        )
        if direct != reconstructed:
            raise AssertionError((s, "recurrence transcription"))
        if any(value < 0 for value in direct.all_coeffs()):
            raise AssertionError((s, "finite recurrence sign"))
        recurrence_coefficients += len(
            [value for value in direct.all_coeffs() if value > 0]
        )

    return {
        "boundary_polynomial_monomials": boundary_monomials,
        "base_values": 4,
        "direct_recurrence_coefficients": recurrence_coefficients,
    }


def main() -> None:
    recurrence = audit_four_layer_recurrence()
    tail = audit_tail_induction()
    low = certify_low_bulk_columns(7)
    top = certify_top_six()
    print("OPG EVEN SECOND-ACTIVE UNIVERSAL CERTIFICATE: PASS")
    for section in (recurrence, tail, low, top):
        for name, value in section.items():
            print(f"{name}: {value}")
    print("status_even_second_active: PROVED")
    print("status_full_base4_newton: OPEN")


if __name__ == "__main__":
    main()
