#!/usr/bin/env python3
"""Exact symbolic verifier for the fourth active Newton layer."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


N = sp.symbols("n", integer=True, positive=True)


def falling(value: sp.Expr, length: int) -> sp.Expr:
    return sp.prod(value - index for index in range(length))


@lru_cache(maxsize=None)
def w0(components: int) -> sp.Expr:
    return sp.factor(
        sum(
            sp.Rational((-1) ** index, 2**index)
            * (components + index)
            * falling(N - 1, components + index - 1)
            * N ** (N - components - index - 1)
            / (
                math.factorial(index)
                * math.factorial(components - index - 1)
            )
            for index in range(components)
        )
    )


@lru_cache(maxsize=None)
def adjacent(components: int) -> sp.Expr:
    return sp.factor(
        sum(
            sp.Rational((-1) ** index, 2**index)
            * (components + index + 2)
            * falling(N - 3, components + index - 1)
            * N ** (N - components - index - 3)
            / (
                math.factorial(index)
                * math.factorial(components - index - 1)
            )
            for index in range(components)
        )
    )


@lru_cache(maxsize=None)
def w1(components: int) -> sp.Expr:
    return sp.factor(
        2 * (N - components) * w0(components) / (N * (N - 1))
    )


@lru_cache(maxsize=None)
def w2(components: int) -> sp.Expr:
    adjacent_orbits = N * (N - 1) * (N - 2) / 2
    disjoint_orbits = N * (N - 1) * (N - 2) * (N - 3) / 8
    forest_pairs = (N - components) * (N - components - 1) / 2
    return sp.factor(
        (
            forest_pairs * w0(components)
            - adjacent_orbits * adjacent(components)
        )
        / disjoint_orbits
    )


def component_determinant(total_components: int) -> sp.Expr:
    return sp.factor(
        sum(
            w1(left) * w1(total_components - left)
            - w0(left) * w2(total_components - left)
            for left in range(1, total_components)
        )
    )


def p5(value):
    return value**3 + 12 * value**2 + 20 * value - 225


def q6(value):
    return (
        value**5
        + 16 * value**4
        + 52 * value**3
        - 587 * value**2
        - 3063 * value
        + 12240
    )


def p7(value):
    return (
        value**6
        + 25 * value**5
        + 229 * value**4
        + 211 * value**3
        - 10101 * value**2
        - 36081 * value
        + 183330
    )


def p8(value):
    return (
        value**8
        + 29 * value**7
        + 321 * value**6
        + 459 * value**5
        - 23239 * value**4
        - 161291 * value**3
        + 565356 * value**2
        + 5972364 * value
        - 18174240
    )


def p9(value):
    return (
        value**9
        + 39 * value**8
        + 667 * value**7
        + 5064 * value**6
        - 10918 * value**5
        - 512106 * value**4
        - 2462113 * value**3
        + 15195399 * value**2
        + 108066951 * value
        - 385491960
    )


def p10(value):
    return (
        value**11
        + 43 * value**10
        + 823 * value**9
        + 7078 * value**8
        - 20797 * value**7
        - 1100827 * value**6
        - 7668142 * value**5
        + 39507308 * value**4
        + 663343272 * value**3
        - 563146065 * value**2
        - 23775670800 * value
        + 61440120000
    )


def expected_c9() -> sp.Expr:
    return (
        (N - 4)
        * (N - 5)
        * (N - 6)
        * p9(N)
        * N ** (2 * N - 20)
        / 180
    )


def expected_c10() -> sp.Expr:
    return (
        (N - 4)
        * (N - 5)
        * (N - 6)
        * p10(N)
        * N ** (2 * N - 22)
        / 1260
    )


def rational_power(base: int, exponent: int) -> Fraction:
    return (
        Fraction(base**exponent)
        if exponent >= 0
        else Fraction(1, base ** (-exponent))
    )


def fourth_coefficient(k: int) -> Fraction:
    if k < 4:
        raise ValueError("the fourth active layer starts at k=4")
    if k % 2:
        n = (k + 11) // 2
        bracket = (
            Fraction(p9(n), 180) * rational_power(n, 2 * n - 20)
            - Fraction(p7(n - 1), 6)
            * rational_power(n - 1, 2 * n - 18)
            + p5(n - 2) * rational_power(n - 2, 2 * n - 16)
            - Fraction(2, 3) * rational_power(n - 3, 2 * n - 14)
        )
    else:
        n = (k + 12) // 2
        bracket = (
            Fraction(p10(n), 1260) * rational_power(n, 2 * n - 22)
            - Fraction(p8(n - 1), 30)
            * rational_power(n - 1, 2 * n - 20)
            + Fraction(q6(n - 2), 3)
            * rational_power(n - 2, 2 * n - 18)
            - Fraction(2 * (n * n - 2 * n - 27), 3)
            * rational_power(n - 3, 2 * n - 16)
        )
    return (
        Fraction(math.factorial(k - 2), 2)
        * (n - 4)
        * (n - 5)
        * (n - 6)
        * bracket
    )


def numeric_scaled(expression: sp.Expr, n: int) -> int:
    value = expression.subs(N, n)
    value = sp.cancel(value)
    if not value.is_Integer:
        raise AssertionError((expression, n, value))
    return int(value)


def direct_newton_coefficient(k: int) -> int:
    q0 = (k - 2) // 2
    n0 = q0 + 4
    total0 = 3 if k % 2 else 4
    raw = 0
    for offset in range(4):
        raw += (
            (-1) ** (3 - offset)
            * math.comb(q0 + 3, 3 - offset)
            * numeric_scaled(
                component_determinant(total0 + 2 * offset),
                n0 + offset,
            )
        )
    result = Fraction(math.factorial(k - 2) * raw, 2)
    if result.denominator != 1:
        raise AssertionError((k, result))
    return result.numerator


def shifted_coefficients(expression: sp.Expr, shift: int) -> list[int]:
    variable = sp.symbols("m")
    polynomial = sp.Poly(sp.expand(expression.subs(N, variable + shift)), variable)
    coefficients = [int(value) for value in polynomial.all_coeffs()]
    assert all(value > 0 for value in coefficients)
    return coefficients


def audit() -> dict[str, object]:
    assert sp.simplify(component_determinant(9) - expected_c9()) == 0
    assert sp.simplify(component_determinant(10) - expected_c10()) == 0

    odd_first_gap = sp.expand(p9(N) - 30 * p7(N - 1) * (N - 1) ** 2)
    odd_second_gap = sp.expand(3 * p5(N - 2) - 2 * (N - 3) ** 2)
    even_first_gap = sp.expand(p10(N) - 42 * p8(N - 1) * (N - 1) ** 2)
    even_second_gap = sp.expand(
        q6(N - 2) - 2 * (N * N - 2 * N - 27) * (N - 3) ** 2
    )

    gap_certificates = {
        "odd_first_shift_8": shifted_coefficients(odd_first_gap, 8),
        "odd_second_shift_8": shifted_coefficients(odd_second_gap, 8),
        "even_first_shift_8": shifted_coefficients(even_first_gap, 8),
        "even_second_shift_8": shifted_coefficients(even_second_gap, 8),
        "p7_shift_9": shifted_coefficients(p7(N), 9),
        "p8_shift_10": shifted_coefficients(p8(N), 10),
    }

    direct_values = {}
    for k in range(4, 13):
        closed = fourth_coefficient(k)
        direct = direct_newton_coefficient(k)
        assert closed == direct and closed > 0
        direct_values[k] = direct

    regression = {k: fourth_coefficient(k) for k in range(4, 101)}
    assert all(value.denominator == 1 and value > 0 for value in regression.values())

    return {
        "schema": "amra.opg1757.fourth-active-newton.v1",
        "symbolic_layers": [9, 10],
        "gap_certificates": gap_certificates,
        "direct_values": direct_values,
        "finite_regression": {
            "k_min": 4,
            "k_max": 100,
            "all_integral_and_positive": True,
        },
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
