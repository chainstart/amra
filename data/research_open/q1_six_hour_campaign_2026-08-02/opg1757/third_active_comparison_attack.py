#!/usr/bin/env python3
"""Symbolic workbench for the third-active comparison kernels.

This is an exploratory exact-algebra script.  It searches for fixed-layer
recurrences for the dominant two-page part after subtracting the preceding
positive fixed-page bracket.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


OLD_LANE = (
    Path(__file__).resolve().parents[2]
    / "q1_eight_hour_campaign_2026-07-29"
    / "opg1757"
)
sys.path.insert(0, str(OLD_LANE))

from five_page_union_formula import (  # noqa: E402
    k3_coefficients,
    k4_coefficients,
    k5_coefficients,
)
from six_page_union_formula import k6_coefficients  # noqa: E402
from seven_page_union_formula import k7_coefficients  # noqa: E402


B = sp.symbols("b")
S = sp.symbols("s", integer=True, positive=True)
X = sp.symbols("x", integer=True, nonnegative=True)


def poly_from_coefficients(values: list[object]) -> sp.Expr:
    return sp.expand(sum(value * B**degree for degree, value in enumerate(values)))


def kernel(page: int, parameter: sp.Expr) -> sp.Expr:
    table = {
        3: k3_coefficients,
        4: k4_coefficients,
        5: k5_coefficients,
        6: k6_coefficients,
        7: k7_coefficients,
    }
    return poly_from_coefficients(table[page](parameter))


def u(index: int) -> sp.Expr:
    return 1 + index * B


def lam(parameter: sp.Expr) -> sp.Expr:
    return 1 + parameter * B


def choose_fixed(top: sp.Expr, bottom: int) -> sp.Expr:
    if bottom < 0:
        return sp.S.Zero
    return sp.prod(top - index for index in range(bottom)) / sp.factorial(bottom)


def odd_recurrence_kernels() -> tuple[sp.Expr, ...]:
    """Bases u6,u5,u4,u3,u2 in Y_(s+1)-u6^2 Y_s."""

    e6 = kernel(6, S + 1) - kernel(6, S)
    e5 = 4 * (
        u(6) ** 2 * lam(S) ** 2 * kernel(5, S)
        - u(5) ** 2 * lam(S + 1) ** 2 * kernel(5, S + 1)
    )
    e4 = (
        -12
        * (S - 3)
        * S**2
        * B**4
        * lam(S) ** 2
        * u(4) ** 2
        * kernel(4, S)
        + 12
        * (S - 4)
        * (S - 1) ** 2
        * B**4
        * u(6) ** 2
        * lam(S - 1) ** 2
        * kernel(4, S - 1)
    )
    e3 = (
        24
        * (S - 3)
        * S**2
        * B**4
        * lam(S) ** 4
        * u(3) ** 4
        * kernel(3, S)
        - 24
        * (S - 4)
        * (S - 1) ** 2
        * B**4
        * u(6) ** 2
        * lam(S - 1) ** 4
        * u(3) ** 2
        * kernel(3, S - 1)
    )
    e2 = (
        -12
        * (S - 3)
        * S**2
        * B**4
        * lam(S) ** 6
        * u(2) ** 6
        + 12
        * (S - 4)
        * (S - 1) ** 2
        * B**4
        * u(6) ** 2
        * lam(S - 1) ** 6
        * u(2) ** 4
    )
    return tuple(sp.expand(value) for value in (e6, e5, e4, e3, e2))


def odd_full_recurrence_kernels() -> tuple[sp.Expr, ...]:
    """Bases u6,...,u2 for the full odd comparison numerator M_s."""

    e6, e5, boundary4, boundary3, boundary2 = odd_recurrence_kernels()
    f4 = 6 * (
        lam(S + 1) ** 4 * u(4) ** 4 * kernel(4, S + 1)
        - u(6) ** 2 * lam(S) ** 4 * u(4) ** 2 * kernel(4, S)
    )
    f3 = -4 * (
        lam(S + 1) ** 6 * u(3) ** 6 * kernel(3, S + 1)
        - u(6) ** 2 * lam(S) ** 6 * u(3) ** 4 * kernel(3, S)
    )
    f2 = (
        lam(S + 1) ** 8 * u(2) ** 8
        - u(6) ** 2 * lam(S) ** 8 * u(2) ** 6
    )
    return tuple(
        sp.expand(value)
        for value in (e6, e5, boundary4 + f4, boundary3 + f3, boundary2 + f2)
    )


def shifted_nonnegative(expression: sp.Expr, start: int) -> tuple[bool, object]:
    polynomial = sp.Poly(sp.expand(expression), B)
    count = 0
    for degree in range(max(0, polynomial.degree()) + 1):
        coefficient = polynomial.coeff_monomial(B**degree)
        if coefficient == 0:
            continue
        shifted = sp.Poly(sp.expand(coefficient.subs(S, X + start)), X)
        values = shifted.all_coeffs()
        if any(value < 0 for value in values):
            return False, (degree, shifted.as_expr())
        count += sum(int(bool(value > 0)) for value in values)
    return True, count


def initial_kernel(
    kernels: tuple[sp.Expr, ...], bases: tuple[int, ...], depth: int, length: sp.Expr
) -> sp.Expr:
    *moving, bottom = kernels
    result = u(2) ** depth * bottom
    for r in range(depth):
        layer = sum(base**r * value for base, value in zip(bases, moving))
        result += choose_fixed(length, r) * B**r * u(2) ** (depth - r) * layer
    return sp.expand(result)


def search_odd() -> None:
    kernels = odd_full_recurrence_kernels()
    e6, e5, e4, e3, _ = kernels
    length = 2 * S - 12
    for start in (8, 12, 16, 20, 24, 30, 40):
        ok_delta, _ = shifted_nonnegative(e6, start)
        if not ok_delta:
            continue
        for depth in range(4, 13):
            layer = 4**depth * e6 + 3**depth * e5 + 2**depth * e4 + e3
            growth_inner = (
                3 * 2**depth * e6
                + 2 * sp.Rational(3, 2) ** depth * e5
                + e4
            )
            growth_second = (
                3 * sp.Rational(4, 3) ** depth * e6 + e5
            )
            initial = initial_kernel(kernels, (4, 3, 2, 1), depth, length)
            checks = [
                shifted_nonnegative(item, start)
                for item in (layer, growth_inner, growth_second, initial)
            ]
            if all(ok for ok, _ in checks):
                print("odd recurrence candidate", start, depth, [x for _, x in checks])
                return
            print("odd failed", start, depth, [x if ok else x[0] for ok, x in checks])


if __name__ == "__main__":
    search_odd()
