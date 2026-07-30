#!/usr/bin/env python3
"""Raw Liu--Chow audit of layer five and verifier for active layer six."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


N = sp.symbols("n", integer=True, positive=True)
U = sp.symbols("u")


def falling(x, length):
    return sp.prod(x - index for index in range(length))


@lru_cache(maxsize=None)
def raw_w0(c):
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
def raw_adjacent(c):
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
def raw_w1(c):
    return sp.factor(2 * (N - c) * raw_w0(c) / (N * (N - 1)))


@lru_cache(maxsize=None)
def raw_w2(c):
    adjacent_orbits = N * (N - 1) * (N - 2) / 2
    disjoint_orbits = N * (N - 1) * (N - 2) * (N - 3) / 8
    pairs = (N - c) * (N - c - 1) / 2
    return sp.factor(
        (pairs * raw_w0(c) - adjacent_orbits * raw_adjacent(c))
        / disjoint_orbits
    )


@lru_cache(maxsize=None)
def raw_determinant(total):
    return sp.factor(
        sum(
            raw_w1(c) * raw_w1(total - c)
            - raw_w0(c) * raw_w2(total - c)
            for c in range(1, total)
        )
    )


def p5(x):
    return x**3 + 12 * x**2 + 20 * x - 225


def q6(x):
    return x**5 + 16 * x**4 + 52 * x**3 - 587 * x**2 - 3063 * x + 12240


def p7(x):
    return x**6 + 25*x**5 + 229*x**4 + 211*x**3 - 10101*x**2 - 36081*x + 183330


def p8(x):
    return (
        x**8 + 29*x**7 + 321*x**6 + 459*x**5 - 23239*x**4
        - 161291*x**3 + 565356*x**2 + 5972364*x - 18174240
    )


def p9(x):
    return (
        x**9 + 39*x**8 + 667*x**7 + 5064*x**6 - 10918*x**5
        - 512106*x**4 - 2462113*x**3 + 15195399*x**2
        + 108066951*x - 385491960
    )


def p10(x):
    return (
        x**11 + 43*x**10 + 823*x**9 + 7078*x**8 - 20797*x**7
        - 1100827*x**6 - 7668142*x**5 + 39507308*x**4
        + 663343272*x**3 - 563146065*x**2 - 23775670800*x
        + 61440120000
    )


def p11(x):
    return (
        x**12 + 54*x**11 + 1377*x**10 + 19446*x**9 + 107701*x**8
        - 1254774*x**7 - 27736029*x**6 - 128979594*x**5
        + 1411682095*x**4 + 15230717502*x**3 - 33712195581*x**2
        - 584682858630*x + 1716330092400
    )


def p12(x):
    return (
        x**14 + 58*x**13 + 1601*x**12 + 24578*x**11 + 141681*x**10
        - 2309634*x**9 - 56550089*x**8 - 341453834*x**7
        + 3612221555*x**6 + 61253397878*x**5 + 3728325315*x**4
        - 4265925973902*x**3 - 4604924521080*x**2
        + 173451580124400*x - 404699171184000
    )


def p13(x):
    return (
        x**15 + 70*x**14 + 2405*x**13 + 50045*x**12 + 593631*x**11
        + 1071225*x**10 - 94449035*x**9 - 1549919255*x**8
        - 5168791531*x**7 + 141697195355*x**6 + 1627621385085*x**5
        - 3660582507525*x**4 - 131552143027686*x**3
        + 13386402798885*x**2 + 5444743454388450*x
        - 14171594774337000
    )


def p14(x):
    return (
        x**17 + 74*x**16 + 2701*x**15 + 59855*x**14 + 747256*x**13
        + 629309*x**12 - 168601994*x**11 - 3022692475*x**10
        - 12400886366*x**9 + 352146822071*x**8 + 5386103546704*x**7
        - 2201028418405*x**6 - 610742061754071*x**5
        - 2210374509140079*x**4 + 42588028344796389*x**3
        + 134015359118765310*x**2 - 2135313543686815800*x
        + 4656619107268128000
    )


def expected_layer(total):
    data = {
        11: (4, 10080, p11(N), 2*N - 24),
        12: (4, 90720, p12(N), 2*N - 26),
        13: (5, 907200, p13(N), 2*N - 28),
        14: (5, 9979200, p14(N), 2*N - 30),
    }
    depth, denominator, polynomial, exponent = data[total]
    return falling(N - 4, depth) * polynomial * N**exponent / denominator


def power(base, exponent):
    return Fraction(base**exponent) if exponent >= 0 else Fraction(1, base**(-exponent))


def sixth_coefficient(k):
    if k < 5:
        raise ValueError("the sixth active layer starts at k=5")
    if k % 2:
        n = (k + 15) // 2
        bracket = (
            Fraction(p13(n), 907200) * power(n, 2*n - 28)
            - Fraction(p11(n-1), 10080) * power(n-1, 2*n - 26)
            + Fraction(p9(n-2), 360) * power(n-2, 2*n - 24)
            - Fraction(p7(n-3), 36) * power(n-3, 2*n - 22)
            + Fraction(p5(n-4), 12) * power(n-4, 2*n - 20)
            - Fraction(1, 30) * power(n-5, 2*n - 18)
        )
    else:
        n = (k + 16) // 2
        bracket = (
            Fraction(p14(n), 9979200) * power(n, 2*n - 30)
            - Fraction(p12(n-1), 90720) * power(n-1, 2*n - 28)
            + Fraction(p10(n-2), 2520) * power(n-2, 2*n - 26)
            - Fraction(p8(n-3), 180) * power(n-3, 2*n - 24)
            + Fraction(q6(n-4), 36) * power(n-4, 2*n - 22)
            - Fraction(n*n - 6*n - 19, 30) * power(n-5, 2*n - 20)
        )
    return (
        Fraction(math.factorial(k - 2), 2)
        * math.prod(n - value for value in range(4, 9))
        * bracket
    )


def direct_newton(k, depth):
    q0 = (k - 2) // 2
    n0 = q0 + 4
    total0 = 3 if k % 2 else 4
    raw = 0
    for offset in range(depth + 1):
        value = sp.cancel(raw_determinant(total0 + 2*offset).subs(N, n0 + offset))
        assert value.is_Integer
        raw += (
            (-1) ** (depth - offset)
            * math.comb(q0 + depth, depth - offset)
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


def product_coefficient(low, high, degree):
    polynomial = [1]
    for value in range(low, high + 1):
        updated = [0] * (len(polynomial) + 1)
        for index, coefficient in enumerate(polynomial):
            updated[index] += coefficient
            updated[index + 1] -= value * coefficient
        polynomial = updated
    return polynomial[degree] if degree < len(polynomial) else 0


def finite_prefix(c, adjacent_flag, degree):
    result = Fraction()
    for j in range(c):
        scalar = Fraction(
            (-1)**j * (c+j+(2 if adjacent_flag else 0)),
            2**j * math.factorial(j) * math.factorial(c-j-1),
        )
        result += scalar * product_coefficient(
            3 if adjacent_flag else 1,
            c+j+(1 if adjacent_flag else -1),
            degree,
        )
    weight = Fraction(1, 2**(c-1) * math.factorial(c-1))
    return result / weight


def leading_two_lemma_checks():
    rho = sp.symbols("rho", integer=True, nonnegative=True)
    expected_w0_u3 = sp.Rational(7, 2)*rho*(rho-1)*(15*rho-52)
    expected_a_u3 = sp.Rational(1, 2)*rho*(rho-1)*(175*rho-1304)
    for c in range(1, 16):
        assert finite_prefix(c, False, 3) == expected_w0_u3.subs(rho, c-1)
        assert finite_prefix(c, True, 3) == expected_a_u3.subs(rho, c-1)

    w0_series = (
        1 + 5*rho*U + rho*(35*rho-47)*U**2/2 + expected_w0_u3*U**3
    )
    a_series = (
        3 + 11*rho*U + 5*rho*(13*rho-37)*U**2/2 + expected_a_u3*U**3
    )
    truncate = lambda expression: sp.series(expression, U, 0, 4).removeO().expand()
    w1_series = truncate(2*(1-(rho+1)*U)/(1-U)*w0_series)
    w2_series = truncate(
        4*(1-(rho+1)*U)*(1-(rho+2)*U)
        / ((1-U)*(1-2*U)*(1-3*U))*w0_series
        - 4*U/(1-3*U)*a_series
    )
    assert sp.factor(w1_series.coeff(U, 3)) == 2*rho*(rho-1)*(35*rho-181)
    assert sp.factor(w2_series.coeff(U, 3)) == 2*rho*(rho-1)*(45*rho-368)

    sigma = sp.symbols("sigma", integer=True, nonnegative=True)
    ordered = truncate(
        w1_series * w1_series.subs(rho, sigma)
        - w0_series * w2_series.subs(rho, sigma)
    )
    reversed_order = ordered.xreplace({rho: sigma, sigma: rho})
    averaged = sp.factor((ordered.coeff(U, 3) + reversed_order.coeff(U, 3))/2)
    delta = sp.symbols("delta")
    total = sp.symbols("R")
    centered = sp.factor(
        averaged.subs({rho: (total+delta)/2, sigma: (total-delta)/2})
    )
    expected_centered = -2 * (
        5*delta**2*total + 4*delta**2 - 13*total**2 + 4*total
    )
    assert sp.expand(centered - expected_centered) == 0
    return {
        "w0_u3": str(expected_w0_u3),
        "adjacent_u3": str(expected_a_u3),
        "symmetrized_determinant_u3": str(centered),
        "determinant_relative_correction": "4*(t-3)",
        "odd_monic_second": "r*(r+23)/2",
        "even_monic_second": "(r^2+23*r+8)/2",
    }


def audit():
    # Independent fifth-layer audit from the raw sums.
    for total in (11, 12, 13, 14):
        assert sp.simplify(raw_determinant(total) - expected_layer(total)) == 0
    fifth_expected = {
        5: 5040,
        6: 1095840,
        7: 388668240,
        8: 102879564480,
        9: 21371783388480,
        10: 8611754056375680,
        12: 922909252139380800000,
    }
    assert {k: direct_newton(k, 4) for k in fifth_expected} == fifth_expected

    # Recheck every shifted-polynomial and auxiliary-sign assertion used by
    # the human fifth-layer proof, without importing its verifier.
    fifth_certificates = {
        "odd_first_gap_shift_9": positive_shift(
            p11(N) - 56*p9(N-1)*(N-1)**2, 9
        ),
        "p9_shift_11": positive_shift(p9(N), 11),
        "odd_second_gap_shift_9": positive_shift(
            p7(N-2) - 4*p5(N-3)*(N-3)**2, 9
        ),
        "p5_shift_7": positive_shift(p5(N), 7),
        "even_first_gap_shift_14": positive_shift(
            (3*N-26)*p12(N) - 72*N*p10(N-1)*(N-1)**2, 14
        ),
        "p10_shift_12": positive_shift(p10(N), 12),
        "even_second_gap_shift_10": positive_shift(
            3*p8(N-2) - 20*q6(N-3)*(N-3)**2, 10
        ),
        "q6_shift_8": positive_shift(q6(N), 8),
    }

    odd_first = sp.expand(
        (3*N-29)*p13(N) - 90*(N-1)**3*p11(N-1)
    )
    odd_second = sp.expand(p9(N-2) - 10*p7(N-3)*(N-3)**2)
    odd_third = sp.expand(5*p5(N-4) - 2*(N-5)**2)
    even_first = sp.expand(
        (3*N-31)*p14(N) - 110*(N-1)**3*p12(N-1)
    )
    even_second = sp.expand(p10(N-2) - 14*p8(N-3)*(N-3)**2)
    even_third = sp.expand(
        5*q6(N-4) - 6*(N*N-6*N-19)*(N-5)**2
    )
    certificates = {
        "odd_first_shift_16": positive_shift(odd_first, 16),
        "odd_second_shift_10": positive_shift(odd_second, 10),
        "odd_third_shift_10": positive_shift(odd_third, 10),
        "even_first_shift_19": positive_shift(even_first, 19),
        "even_second_shift_11": positive_shift(even_second, 11),
        "even_third_shift_11": positive_shift(even_third, 11),
        "p11_shift_8": positive_shift(p11(N), 8),
        "p12_shift_8": positive_shift(p12(N), 8),
        "p7_shift_6": positive_shift(p7(N), 6),
        "p8_shift_6": positive_shift(p8(N), 6),
    }

    direct = {}
    for k in range(5, 23):
        closed = sixth_coefficient(k)
        exact = direct_newton(k, 5)
        assert closed == exact and closed > 0
        direct[k] = exact
    regression = [sixth_coefficient(k) for k in range(5, 101)]
    assert all(value.denominator == 1 and value > 0 for value in regression)

    return {
        "schema": "amra.opg1757.sixth-active-newton.v1",
        "independent_fifth_audit": {
            "layers": [11, 12],
            "denominators": [10080, 90720],
            "boundary_values": fifth_expected,
            "certificates": fifth_certificates,
            "quantified_ranges": {
                "odd_first_pair": "n>=12",
                "odd_second_pair": "n>=10",
                "odd_residual": "n=9,10,11",
                "even_first_pair": "n>=14",
                "even_second_pair": "n>=11",
                "even_last_term": "n>=10",
                "even_residual": "n=10,11,12,13",
            },
            "bernoulli_ratio": "(1-1/n)^(2n-26) <= n/(3n-26), n>=14",
            "verdict": "PASS",
        },
        "sixth_layers": [13, 14],
        "sixth_denominators": [907200, 9979200],
        "certificates": certificates,
        "leading_two_lemma": leading_two_lemma_checks(),
        "direct_values": direct,
        "finite_regression": [5, 100],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
