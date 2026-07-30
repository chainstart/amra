#!/usr/bin/env python3
"""Independent symbolic audit of the fixed-depth asymptotic theorem."""

from __future__ import annotations

import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction

import sympy as sp


U = sp.symbols("u")
RHO, SIGMA = sp.symbols("rho sigma", integer=True, nonnegative=True)


def product_prefix(low: int, high: int) -> tuple[int, int, int]:
    values = tuple(range(low, high + 1))
    first = sum(values)
    second = (first * first - sum(value * value for value in values)) // 2
    return 1, -first, second


def finite_sum_prefix(components: int, adjacent: bool) -> tuple[Fraction, ...]:
    """Expand the finite products in (5)--(6), independently of source code."""

    result = [Fraction(), Fraction(), Fraction()]
    for index in range(components):
        scalar = Fraction(
            (-1) ** index
            * (components + index + (2 if adjacent else 0)),
            2**index
            * math.factorial(index)
            * math.factorial(components - index - 1),
        )
        low = 3 if adjacent else 1
        high = components + index + (1 if adjacent else -1)
        for degree, coefficient in enumerate(product_prefix(low, high)):
            result[degree] += scalar * coefficient
    return tuple(result)


def predicted_w0_prefix(components: int) -> tuple[Fraction, ...]:
    rho = components - 1
    weight = Fraction(1, 2**rho * math.factorial(rho))
    return (
        weight,
        5 * rho * weight,
        Fraction(rho * (35 * rho - 47), 2) * weight,
    )


def predicted_adjacent_prefix(components: int) -> tuple[Fraction, ...]:
    rho = components - 1
    weight = Fraction(1, 2**rho * math.factorial(rho))
    return (
        3 * weight,
        11 * rho * weight,
        Fraction(5 * rho * (13 * rho - 37), 2) * weight,
    )


def truncate(expression: sp.Expr, degree: int = 3) -> sp.Expr:
    return sp.series(expression, U, 0, degree).removeO().expand()


def symbolic_matching_prefixes() -> dict[str, sp.Expr]:
    w0 = 1 + 5 * RHO * U + RHO * (35 * RHO - 47) * U**2 / 2
    adjacent = (
        3
        + 11 * RHO * U
        + 5 * RHO * (13 * RHO - 37) * U**2 / 2
    )

    w1_factor = 2 * (1 - (RHO + 1) * U) / (1 - U)
    w1 = truncate(w1_factor * w0)
    expected_w1 = (
        2
        + 8 * RHO * U
        + RHO * (25 * RHO - 49) * U**2
    )
    assert sp.expand(w1 - expected_w1) == 0

    # After division by n^(n-4), the two factors in the pair identity are:
    choose_factor = (
        4
        * (1 - (RHO + 1) * U)
        * (1 - (RHO + 2) * U)
        / ((1 - U) * (1 - 2 * U) * (1 - 3 * U))
    )
    adjacent_factor = 4 * U / (1 - 3 * U)
    w2 = truncate(choose_factor * w0 - adjacent_factor * adjacent)
    expected_w2 = (
        4
        + 12 * RHO * U
        + 2 * RHO * (17 * RHO - 57) * U**2
    )
    assert sp.expand(w2 - expected_w2) == 0
    return {"w1": w1, "w2": w2}


def symmetrized_determinant_coefficient() -> sp.Expr:
    def w0(rho: sp.Expr) -> sp.Expr:
        return 1 + 5 * rho * U + rho * (35 * rho - 47) * U**2 / 2

    def w1(rho: sp.Expr) -> sp.Expr:
        return 2 + 8 * rho * U + rho * (25 * rho - 49) * U**2

    def w2(rho: sp.Expr) -> sp.Expr:
        return 4 + 12 * rho * U + 2 * rho * (17 * rho - 57) * U**2

    ordered = truncate(w1(RHO) * w1(SIGMA) - w0(RHO) * w2(SIGMA))
    assert sp.expand(ordered.coeff(U, 1) + 4 * (RHO - SIGMA)) == 0
    averaged = sp.expand(
        (
            ordered.coeff(U, 2)
            + ordered.xreplace({RHO: SIGMA, SIGMA: RHO}).coeff(U, 2)
        )
        / 2
    )
    expected = 2 * (3 * (RHO + SIGMA) - (RHO - SIGMA) ** 2)
    assert sp.expand(averaged - expected) == 0
    return averaged


def binomial_moment_checks(maximum_total: int = 30) -> None:
    for total in range(1, maximum_total + 1):
        mass = Fraction()
        second = Fraction()
        for rho in range(total + 1):
            sigma = total - rho
            weight = Fraction(
                1,
                2**total * math.factorial(rho) * math.factorial(sigma),
            )
            mass += weight
            second += weight * (rho - sigma) ** 2
        assert mass == Fraction(1, math.factorial(total))
        assert second == Fraction(total, math.factorial(total))


def equation_20_symbolic_series() -> sp.Expr:
    """Exact formal expansion after removing the e^(-2 ell) constant."""

    x, ell = sp.symbols("x ell")
    logarithm = sp.series(
        (2 / x - 2 * ell - 8) * sp.log(1 - ell * x) + 2 * ell,
        x,
        0,
        3,
    ).removeO()
    ratio = sp.series(sp.exp(logarithm), x, 0, 3).removeO().expand()
    assert sp.factor(ratio.coeff(x, 1)) == ell * (ell + 8)
    assert sp.factor(ratio.coeff(x, 2)) == (
        ell**2 * (3 * ell**2 + 50 * ell + 216) / 6
    )
    return ratio


def high_precision_constant_check(n: int, ell: int) -> tuple[Decimal, Decimal]:
    """Return the base ratio and Newton-scaled ratio with 80-digit arithmetic."""

    with localcontext() as context:
        context.prec = 80
        decimal_n = Decimal(n)
        decimal_ell = Decimal(ell)
        base = (Decimal(1) - decimal_ell / decimal_n) ** (
            2 * (n - ell) - 8
        )

        binomial = Decimal(math.comb(n - 4, ell))
        base_power_ratio = (
            (Decimal(n - ell) / decimal_n) ** (2 * (n - ell) - 8)
            / decimal_n ** (2 * ell)
        )
        newton_scaled = (
            binomial * base_power_ratio * decimal_n**ell
        )
        return +base, +newton_scaled


def capacity_boundary_check(maximum_n: int = 30) -> None:
    for n in range(4, maximum_n + 1):
        w01 = n ** (n - 2)
        w11 = 2 * n ** (n - 3)
        w21 = 4 * n ** (n - 4)
        assert w11 * w11 - w01 * w21 == 0


def audit() -> dict[str, object]:
    prefix_checks = 0
    for components in range(1, 16):
        assert finite_sum_prefix(components, False) == predicted_w0_prefix(
            components
        )
        assert finite_sum_prefix(components, True) == predicted_adjacent_prefix(
            components
        )
        prefix_checks += 2

    matching = symbolic_matching_prefixes()
    symmetrized = symmetrized_determinant_coefficient()
    equation_20_series = equation_20_symbolic_series()
    binomial_moment_checks()
    capacity_boundary_check()

    constant_checks = []
    for ell in range(1, 6):
        n = 10_000_000
        raw, scaled_newton = high_precision_constant_check(n, ell)
        with localcontext() as context:
            context.prec = 80
            expected = Decimal(-2 * ell).exp()
            first_correction = Decimal(ell * ell + 8 * ell)
            observed_correction = Decimal(n) * (raw / expected - 1)
            assert abs(observed_correction - first_correction) < Decimal("0.01")

            expected_newton = expected / Decimal(math.factorial(ell))
            assert abs(scaled_newton / expected_newton - 1) < Decimal("0.00001")
        constant_checks.append(
            {
                "ell": ell,
                "base_limit": str(expected),
                "observed_first_correction": str(observed_correction),
                "newton_scaled_limit": str(expected_newton),
            }
        )

    return {
        "schema": "amra.opg1757.fixed-depth-independent-audit.v1",
        "finite_product_prefix_checks": prefix_checks,
        "matching_prefixes": {
            key: str(value) for key, value in matching.items()
        },
        "symmetrized_u2": str(symmetrized),
        "equation_20_symbolic_series": str(equation_20_series),
        "binomial_moments_checked_through": 30,
        "capacity_boundary_checked_through_n": 30,
        "equation_20_constant_checks": constant_checks,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
