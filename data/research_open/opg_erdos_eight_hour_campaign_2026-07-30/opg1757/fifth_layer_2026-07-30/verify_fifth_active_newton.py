#!/usr/bin/env python3
"""Symbolic verifier for the fifth active Newton layer and general pattern."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


N = sp.symbols("n", integer=True, positive=True)


def falling(value, length):
    return sp.prod(value - index for index in range(length))


@lru_cache(maxsize=None)
def w0(c):
    return sp.factor(
        sum(
            sp.Rational((-1) ** j, 2**j)
            * (c + j)
            * falling(N - 1, c + j - 1)
            * N ** (N - c - j - 1)
            / (math.factorial(j) * math.factorial(c - j - 1))
            for j in range(c)
        )
    )


@lru_cache(maxsize=None)
def adjacent(c):
    return sp.factor(
        sum(
            sp.Rational((-1) ** j, 2**j)
            * (c + j + 2)
            * falling(N - 3, c + j - 1)
            * N ** (N - c - j - 3)
            / (math.factorial(j) * math.factorial(c - j - 1))
            for j in range(c)
        )
    )


@lru_cache(maxsize=None)
def w1(c):
    return sp.factor(2 * (N - c) * w0(c) / (N * (N - 1)))


@lru_cache(maxsize=None)
def w2(c):
    na = N * (N - 1) * (N - 2) / 2
    nd = N * (N - 1) * (N - 2) * (N - 3) / 8
    return sp.factor(
        (((N - c) * (N - c - 1) / 2) * w0(c) - na * adjacent(c)) / nd
    )


@lru_cache(maxsize=None)
def determinant(total):
    return sp.factor(
        sum(
            w1(c) * w1(total - c) - w0(c) * w2(total - c)
            for c in range(1, total)
        )
    )


def p5(x):
    return x**3 + 12 * x**2 + 20 * x - 225


def q6(x):
    return x**5 + 16 * x**4 + 52 * x**3 - 587 * x**2 - 3063 * x + 12240


def p7(x):
    return (
        x**6
        + 25 * x**5
        + 229 * x**4
        + 211 * x**3
        - 10101 * x**2
        - 36081 * x
        + 183330
    )


def p8(x):
    return (
        x**8
        + 29 * x**7
        + 321 * x**6
        + 459 * x**5
        - 23239 * x**4
        - 161291 * x**3
        + 565356 * x**2
        + 5972364 * x
        - 18174240
    )


def p9(x):
    return (
        x**9
        + 39 * x**8
        + 667 * x**7
        + 5064 * x**6
        - 10918 * x**5
        - 512106 * x**4
        - 2462113 * x**3
        + 15195399 * x**2
        + 108066951 * x
        - 385491960
    )


def p10(x):
    return (
        x**11
        + 43 * x**10
        + 823 * x**9
        + 7078 * x**8
        - 20797 * x**7
        - 1100827 * x**6
        - 7668142 * x**5
        + 39507308 * x**4
        + 663343272 * x**3
        - 563146065 * x**2
        - 23775670800 * x
        + 61440120000
    )


def p11(x):
    return (
        x**12
        + 54 * x**11
        + 1377 * x**10
        + 19446 * x**9
        + 107701 * x**8
        - 1254774 * x**7
        - 27736029 * x**6
        - 128979594 * x**5
        + 1411682095 * x**4
        + 15230717502 * x**3
        - 33712195581 * x**2
        - 584682858630 * x
        + 1716330092400
    )


def p12(x):
    return (
        x**14
        + 58 * x**13
        + 1601 * x**12
        + 24578 * x**11
        + 141681 * x**10
        - 2309634 * x**9
        - 56550089 * x**8
        - 341453834 * x**7
        + 3612221555 * x**6
        + 61253397878 * x**5
        + 3728325315 * x**4
        - 4265925973902 * x**3
        - 4604924521080 * x**2
        + 173451580124400 * x
        - 404699171184000
    )


def expected_c11():
    return falling(N - 4, 4) * p11(N) * N ** (2 * N - 24) / 10080


def expected_c12():
    return falling(N - 4, 4) * p12(N) * N ** (2 * N - 26) / 90720


def power(base, exponent):
    return Fraction(base**exponent) if exponent >= 0 else Fraction(1, base ** (-exponent))


def fifth_coefficient(k):
    if k < 5:
        raise ValueError("the fifth active layer starts at k=5")
    if k % 2:
        n = (k + 13) // 2
        bracket = (
            Fraction(p11(n), 10080) * power(n, 2 * n - 24)
            - Fraction(p9(n - 1), 180) * power(n - 1, 2 * n - 22)
            + Fraction(p7(n - 2), 12) * power(n - 2, 2 * n - 20)
            - Fraction(p5(n - 3), 3) * power(n - 3, 2 * n - 18)
            + Fraction(1, 6) * power(n - 4, 2 * n - 16)
        )
    else:
        n = (k + 14) // 2
        bracket = (
            Fraction(p12(n), 90720) * power(n, 2 * n - 26)
            - Fraction(p10(n - 1), 1260) * power(n - 1, 2 * n - 24)
            + Fraction(p8(n - 2), 60) * power(n - 2, 2 * n - 22)
            - Fraction(q6(n - 3), 9) * power(n - 3, 2 * n - 20)
            + Fraction(n * n - 4 * n - 24, 6)
            * power(n - 4, 2 * n - 18)
        )
    return (
        Fraction(math.factorial(k - 2), 2)
        * (n - 4)
        * (n - 5)
        * (n - 6)
        * (n - 7)
        * bracket
    )


def direct_fifth(k):
    q0 = (k - 2) // 2
    n0 = q0 + 4
    total0 = 3 if k % 2 else 4
    raw = 0
    for offset in range(5):
        value = sp.cancel(determinant(total0 + 2 * offset).subs(N, n0 + offset))
        assert value.is_Integer
        raw += (
            (-1) ** (4 - offset)
            * math.comb(q0 + 4, 4 - offset)
            * int(value)
        )
    result = Fraction(math.factorial(k - 2) * raw, 2)
    assert result.denominator == 1
    return result.numerator


def positive_shift(expression, shift):
    m = sp.symbols("m")
    coefficients = [
        int(value)
        for value in sp.Poly(sp.expand(expression.subs(N, m + shift)), m).all_coeffs()
    ]
    assert all(value > 0 for value in coefficients)
    return coefficients


def component_pattern_checks():
    records = []
    m = sp.symbols("m")
    for total in range(3, 13):
        if total % 2:
            depth = (total - 3) // 2
            exponent = 2 * N - 4 * depth - 8
            expected_degree = 3 * depth
        else:
            depth = (total - 4) // 2
            exponent = 2 * N - 4 * depth - 10
            expected_degree = 3 * depth + 2
        remainder = sp.factor(
            sp.powsimp(
                determinant(total)
                / (falling(N - 4, depth) * N**exponent),
                force=True,
            )
        )
        polynomial = sp.Poly(remainder, N)
        assert polynomial.degree() == expected_degree
        assert polynomial.LC() > 0
        shifted = sp.Poly(
            sp.expand(remainder.subs(N, m + depth + 4)), m
        )
        assert all(value > 0 for value in shifted.all_coeffs())
        records.append(
            {
                "total_components": total,
                "falling_depth": depth,
                "remainder_degree": expected_degree,
                "positive_shift": depth + 4,
            }
        )
    return records


def audit():
    assert sp.simplify(determinant(11) - expected_c11()) == 0
    assert sp.simplify(determinant(12) - expected_c12()) == 0

    odd_first = sp.expand(p11(N) - 56 * p9(N - 1) * (N - 1) ** 2)
    odd_second = sp.expand(p7(N - 2) - 4 * p5(N - 3) * (N - 3) ** 2)
    even_first_refined = sp.expand(
        (3 * N - 26) * p12(N)
        - 72 * N * p10(N - 1) * (N - 1) ** 2
    )
    even_second = sp.expand(
        3 * p8(N - 2) - 20 * q6(N - 3) * (N - 3) ** 2
    )

    certificates = {
        "odd_first_shift_9": positive_shift(odd_first, 9),
        "odd_second_shift_9": positive_shift(odd_second, 9),
        "even_first_refined_shift_14": positive_shift(even_first_refined, 14),
        "even_second_shift_10": positive_shift(even_second, 10),
        "p9_shift_11": positive_shift(p9(N), 11),
        "p10_shift_12": positive_shift(p10(N), 12),
        "p5_shift_7": positive_shift(p5(N), 7),
        "q6_shift_8": positive_shift(q6(N), 8),
    }
    pattern_checks = component_pattern_checks()

    direct = {}
    for k in range(5, 15):
        closed = fifth_coefficient(k)
        exact = direct_fifth(k)
        assert closed == exact and closed > 0
        direct[k] = exact

    regression = [fifth_coefficient(k) for k in range(5, 101)]
    assert all(value.denominator == 1 and value > 0 for value in regression)

    return {
        "schema": "amra.opg1757.fifth-active-newton.v1",
        "symbolic_layers": [11, 12],
        "certificates": certificates,
        "component_pattern_checks": pattern_checks,
        "direct_values": direct,
        "finite_regression": [5, 100],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
