#!/usr/bin/env python3
"""Fixed-column certificates for the third-active transport bulk."""

from __future__ import annotations

import math
import sys
from functools import cache
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


S = sp.symbols("s", integer=True, positive=True)
X = sp.symbols("x", integer=True, nonnegative=True)


KERNELS = {
    3: k3_coefficients,
    4: k4_coefficients,
    5: k5_coefficients,
    6: k6_coefficients,
    7: k7_coefficients,
}


def choose_fixed(top: sp.Expr, bottom: int) -> sp.Expr:
    if bottom < 0:
        return sp.S.Zero
    return sp.prod(top - index for index in range(bottom)) / sp.factorial(bottom)


def convolution(left: list[sp.Expr], right: list[sp.Expr]) -> list[sp.Expr]:
    result = [sp.S.Zero] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return [sp.expand(value) for value in result]


def linear_power_kernel(power: int, parameter: sp.Expr) -> list[sp.Expr]:
    return [sp.binomial(power, degree) * parameter**degree for degree in range(power + 1)]


def power_kernel_coefficient(
    base: int,
    exponent: sp.Expr,
    kernel: list[sp.Expr],
    degree: int,
) -> sp.Expr:
    value = sp.S.Zero
    for index, entry in enumerate(kernel):
        residual = degree - index
        if residual < 0:
            continue
        value += entry * choose_fixed(exponent, residual) * base**residual
    return sp.expand(value)


@cache
def f_coefficient(page: int, parameter: sp.Expr, degree: int) -> sp.Expr:
    value = sp.S.Zero
    for base in range(2, page + 1):
        multiplier = (-1) ** (page - base) * math.comb(page - 2, base - 2)
        lambda_power = 2 * (page - base)
        page_kernel = [sp.S.One] if base == 2 else KERNELS[base](parameter)
        full_kernel = convolution(
            linear_power_kernel(lambda_power, parameter), page_kernel
        )
        exponent = 2 * parameter - 2 * base - 2
        value += multiplier * power_kernel_coefficient(
            base, exponent, full_kernel, degree
        )
    return sp.expand(value)


@cache
def p_coefficient(page: int, parameter: sp.Expr, degree: int) -> sp.Expr:
    if degree < 0:
        return sp.S.Zero
    return f_coefficient(page, parameter, degree + 2 * page - 4)


def multiplied_p_coefficient(
    page: int,
    parameter: sp.Expr,
    degree: int,
    factor: list[sp.Expr],
) -> sp.Expr:
    return sp.expand(
        sum(
            entry * p_coefficient(page, parameter, degree - index)
            for index, entry in enumerate(factor)
            if degree >= index
        )
    )


@cache
def page_recurrence_coefficient(page: int, parameter: sp.Expr, degree: int) -> sp.Expr:
    return sp.expand(
        p_coefficient(page, parameter + 1, degree)
        - multiplied_p_coefficient(
            page,
            parameter,
            degree,
            linear_power_kernel(2, page),
        )
    )


@cache
def odd_lower_kernel_numerator(degree: int) -> sp.Expr:
    """Return 12*s times the sufficient odd bulk coefficient."""

    p6_next = p_coefficient(6, S + 1, degree)
    transported = multiplied_p_coefficient(
        6, S, degree, linear_power_kernel(2, 6)
    )
    recurrence = p6_next - transported
    middle = multiplied_p_coefficient(
        4, S, degree, linear_power_kernel(2, S)
    )
    bottom_kernel = convolution(
        convolution(linear_power_kernel(2, 6), linear_power_kernel(4, S)),
        [sp.S.One],
    )
    bottom = power_kernel_coefficient(
        2, 2 * S - 10, bottom_kernel, degree
    )
    return sp.factor(
        sp.expand(
            S * recurrence
            + (2 * S - 12 - degree) * transported
            - 12 * S**3 * (S - 3) * middle
            - 12 * S**5 * (S - 4) * (S - 5) * bottom
        )
    )


@cache
def even_lower_kernel_numerator(degree: int) -> sp.Expr:
    """Return 60*s times the sufficient even bulk coefficient."""

    p7_next = p_coefficient(7, S + 1, degree)
    transported = multiplied_p_coefficient(
        7, S, degree, linear_power_kernel(2, 7)
    )
    recurrence = p7_next - transported
    middle = multiplied_p_coefficient(
        5, S, degree, linear_power_kernel(2, S)
    )
    bottom_factor = convolution(
        linear_power_kernel(2, 7), linear_power_kernel(4, S - 2)
    )
    bottom = multiplied_p_coefficient(3, S - 2, degree, bottom_factor)
    return sp.factor(
        sp.expand(
            S * recurrence
            + (2 * S - 14 - degree) * transported
            - 20 * S**3 * (S - 3) * middle
            - 60 * S**5 * (S - 4) * (S - 5) * bottom
        )
    )


def certify_odd_columns(maximum_degree: int = 30) -> dict[str, object]:
    counts = 0
    recurrence_counts = 0
    starts = []
    for degree in range(maximum_degree + 1):
        start = max(8, math.ceil((degree + 12) / 2))
        shifted = sp.Poly(
            sp.expand(odd_lower_kernel_numerator(degree).subs(S, X + start)),
            X,
        )
        if any(value <= 0 for value in shifted.all_coeffs()):
            raise AssertionError((degree, start, shifted.as_expr()))
        counts += len(shifted.all_coeffs())
        recurrence = sp.Poly(
            sp.expand(
                page_recurrence_coefficient(6, S, degree).subs(S, X + start)
            ),
            X,
        )
        if any(value < 0 for value in recurrence.all_coeffs()):
            raise AssertionError(("B6 recurrence", degree, start, recurrence.as_expr()))
        recurrence_counts += sum(
            int(bool(value > 0)) for value in recurrence.all_coeffs()
        )
        starts.append(start)
    return {
        "columns": maximum_degree + 1,
        "positive_shifted_monomials": counts,
        "nonnegative_recurrence_monomials": recurrence_counts,
        "starts": starts,
    }


def certify_even_columns(maximum_degree: int = 30) -> dict[str, object]:
    counts = 0
    recurrence_counts = 0
    starts = []
    for degree in range(maximum_degree + 1):
        start = max(9, math.ceil((degree + 14) / 2))
        shifted = sp.Poly(
            sp.expand(even_lower_kernel_numerator(degree).subs(S, X + start)),
            X,
        )
        if any(value <= 0 for value in shifted.all_coeffs()):
            raise AssertionError((degree, start, shifted.as_expr()))
        counts += len(shifted.all_coeffs())
        recurrence = sp.Poly(
            sp.expand(
                page_recurrence_coefficient(7, S, degree).subs(S, X + start)
            ),
            X,
        )
        if any(value < 0 for value in recurrence.all_coeffs()):
            raise AssertionError(("B7 recurrence", degree, start, recurrence.as_expr()))
        recurrence_counts += sum(
            int(bool(value > 0)) for value in recurrence.all_coeffs()
        )
        starts.append(start)
    return {
        "columns": maximum_degree + 1,
        "positive_shifted_monomials": counts,
        "nonnegative_recurrence_monomials": recurrence_counts,
        "starts": starts,
    }


def direct_crosschecks() -> int:
    """Guard the sufficient kernels against full exact transports."""

    import third_active_workbench as direct

    checks = 0
    for parity, first, denominator, cutoff_shift, numerator in (
        ("odd", 8, 12, 12, odd_lower_kernel_numerator),
        ("even", 9, 60, 14, even_lower_kernel_numerator),
    ):
        for s in range(first, first + 5):
            row = direct.transport_remainder(parity, s)
            cutoff = 2 * s - cutoff_shift
            for degree in range(min(30, cutoff) + 1):
                sufficient = sp.Rational(
                    numerator(degree).subs(S, s), denominator * s
                )
                if sufficient <= 0:
                    raise AssertionError((parity, s, degree, sufficient))
                lower_bound = s ** (cutoff - degree) * sufficient
                if row[degree] < lower_bound:
                    raise AssertionError(
                        (parity, s, degree, row[degree], lower_bound)
                    )
                checks += 1
    return checks


def certify(maximum_degree: int = 30) -> dict[str, object]:
    return {
        "odd": certify_odd_columns(maximum_degree),
        "even": certify_even_columns(maximum_degree),
        "direct_crosschecks": direct_crosschecks(),
    }


def main() -> None:
    result = certify()
    print("OPG THIRD-ACTIVE TRANSPORT BULK-COLUMN CERTIFICATE: PASS")
    for parity in ("odd", "even"):
        for key, value in result[parity].items():
            print(f"{parity}_{key}: {value}")
    print("direct_crosschecks:", result["direct_crosschecks"])
    print("status_full_transports: OPEN")


if __name__ == "__main__":
    main()
