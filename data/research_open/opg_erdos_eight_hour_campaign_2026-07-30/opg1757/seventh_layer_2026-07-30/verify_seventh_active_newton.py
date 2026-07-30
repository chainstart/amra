#!/usr/bin/env python3
"""Exact verifier for the seventh active base-four Newton layer."""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp


SIXTH_DIR = Path(__file__).resolve().parents[1] / "sixth_layer_2026-07-30"
sys.path.insert(0, str(SIXTH_DIR))
import verify_sixth_active_newton as base  # noqa: E402


N = base.N


def p15(x):
    return (
        x**18 + 87*x**17 + 3800*x**16 + 105360*x**15
        + 1891421*x**14 + 17289777*x**13 - 118116085*x**12
        - 6505709265*x**11 - 86775284431*x**10 - 38284278087*x**9
        + 14371618346075*x**8 + 155474888000475*x**7
        - 622230464754476*x**6 - 21941798038092942*x**5
        - 34808916839991345*x**4 + 1685933108025287175*x**3
        + 3008726132139045000*x**2 - 82118619319287127500*x
        + 197196338202113250000
    )


def p16(x):
    return (
        x**20 + 91*x**19 + 4172*x**18 + 121628*x**17
        + 2284643*x**16 + 20698691*x**15 - 230561653*x**14
        - 11319430447*x**13 - 162404702239*x**12
        - 80646884461*x**11 + 34321800795503*x**10
        + 457838031840137*x**9 - 1167527280504428*x**8
        - 82905605421055196*x**7 - 398108708754400437*x**6
        + 8161447984576101657*x**5 + 64714964045818304358*x**4
        - 630805618098807641100*x**3 - 3720646386150579275400*x**2
        + 41502191820112083060000*x - 86322277727720274240000
    )


def expected_layer(total):
    if total == 15:
        return (
            base.falling(N - 4, 6)
            * p15(N)
            * N ** (2*N - 32)
            / 119750400
        )
    if total == 16:
        return (
            base.falling(N - 4, 6)
            * p16(N)
            * N ** (2*N - 34)
            / 1556755200
        )
    raise ValueError(total)


def seventh_coefficient(k):
    if k < 6:
        raise ValueError("the seventh active layer starts at k=6")
    if k % 2:
        n = (k + 17) // 2
        bracket = (
            Fraction(p15(n), 119750400) * base.power(n, 2*n - 32)
            - Fraction(base.p13(n-1), 907200)
            * base.power(n-1, 2*n - 30)
            + Fraction(base.p11(n-2), 20160)
            * base.power(n-2, 2*n - 28)
            - Fraction(base.p9(n-3), 1080)
            * base.power(n-3, 2*n - 26)
            + Fraction(base.p7(n-4), 144)
            * base.power(n-4, 2*n - 24)
            - Fraction(base.p5(n-5), 60)
            * base.power(n-5, 2*n - 22)
            + Fraction(1, 180) * base.power(n-6, 2*n - 20)
        )
    else:
        n = (k + 18) // 2
        bracket = (
            Fraction(p16(n), 1556755200) * base.power(n, 2*n - 34)
            - Fraction(base.p14(n-1), 9979200)
            * base.power(n-1, 2*n - 32)
            + Fraction(base.p12(n-2), 181440)
            * base.power(n-2, 2*n - 30)
            - Fraction(base.p10(n-3), 7560)
            * base.power(n-3, 2*n - 28)
            + Fraction(base.p8(n-4), 720)
            * base.power(n-4, 2*n - 26)
            - Fraction(base.q6(n-5), 180)
            * base.power(n-5, 2*n - 24)
            + Fraction(n*n - 8*n - 12, 180)
            * base.power(n-6, 2*n - 22)
        )
    result = (
        Fraction(math.factorial(k - 2), 2)
        * math.prod(n - value for value in range(4, 10))
        * bracket
    )
    assert result.denominator == 1
    return result.numerator


def positive_shift(expression, shift):
    m = sp.symbols("m")
    coefficients = [
        int(value)
        for value in sp.Poly(
            sp.expand(expression.subs(N, m + shift)), m
        ).all_coeffs()
    ]
    assert all(value > 0 for value in coefficients)
    return coefficients


def diagonal_cross_check():
    r = sp.symbols("r", integer=True, nonnegative=True)
    odd_second = r * (r + 23) / 2
    even_second = (r*r + 23*r + 8) / 2
    assert sp.Rational(1, 119750400) == sp.Rational(4, math.factorial(12))
    assert sp.Rational(1, 1556755200) == sp.Rational(4, math.factorial(13))
    assert sp.Poly(p15(N), N).coeff_monomial(N**17) == odd_second.subs(r, 6)
    assert sp.Poly(p16(N), N).coeff_monomial(N**19) == even_second.subs(r, 6)

    # Check the corrected alternating signs in diagonal equation (14).
    u, y, a = sp.symbols("u y a")
    logarithm = sp.series(
        (sp.Rational(1, 1)/u - a) * sp.log(1 + u*y) - y,
        u,
        0,
        5,
    ).removeO().expand()
    expected = (
        -u*(a*y + y**2/2)
        + u**2*(a*y**2/2 + y**3/3)
        - u**3*(a*y**3/3 + y**4/4)
        + u**4*(a*y**4/4 + y**5/5)
    )
    assert sp.expand(logarithm - expected) == 0

    # P2 and P3 of the all-orders diagonal theorem give the same
    # determinant leading and relative subleading terms.
    R = sp.symbols("R", integer=True, positive=True)
    leading = 4 * R / sp.factorial(R)
    subleading = 16 * R * (R - 1) / sp.factorial(R)
    assert sp.simplify(leading - 4/sp.factorial(R-1)) == 0
    assert sp.simplify(subleading - 16/sp.factorial(R-2)) == 0
    return {
        "corrected_equation_14": "PASS",
        "A6_leading_denominator": 119750400,
        "A6_monic_second": 87,
        "B6_leading_denominator": 1556755200,
        "B6_monic_second": 91,
        "diagonal_P2": "4*R",
        "diagonal_P3": "16*R*(R-1)",
    }


def audit():
    for total in (15, 16):
        assert sp.simplify(
            base.raw_determinant(total) - expected_layer(total)
        ) == 0

    odd_first = sp.expand(
        (3*N-33)*p15(N) - 132*(N-1)**3*base.p13(N-1)
    )
    odd_second = sp.expand(
        3*base.p11(N-2) - 56*base.p9(N-3)*(N-3)**2
    )
    odd_third = sp.expand(
        5*base.p7(N-4) - 12*base.p5(N-5)*(N-5)**2
    )
    even_first = sp.expand(
        (3*N-35)*p16(N) - 156*(N-1)**3*base.p14(N-1)
    )
    even_second = sp.expand(
        base.p12(N-2) - 24*base.p10(N-3)*(N-3)**2
    )
    even_third = sp.expand(
        base.p8(N-4) - 4*base.q6(N-5)*(N-5)**2
    )
    certificates = {
        "odd_first_shift_22": positive_shift(odd_first, 22),
        "odd_second_shift_9": positive_shift(odd_second, 9),
        "odd_third_shift_9": positive_shift(odd_third, 9),
        "even_first_shift_26": positive_shift(even_first, 26),
        "even_second_shift_10": positive_shift(even_second, 10),
        "even_third_shift_10": positive_shift(even_third, 10),
        "p13_shift_9": positive_shift(base.p13(N), 9),
        "p14_shift_9": positive_shift(base.p14(N), 9),
        "p9_shift_11": positive_shift(base.p9(N), 11),
        "p10_shift_12": positive_shift(base.p10(N), 12),
        "p5_shift_7": positive_shift(base.p5(N), 7),
        "q6_shift_8": positive_shift(base.q6(N), 8),
    }

    direct = {}
    for k in range(6, 36):
        closed = seventh_coefficient(k)
        exact = base.direct_newton(k, 6)
        assert closed == exact and closed > 0
        direct[k] = exact
    regression = [seventh_coefficient(k) for k in range(6, 101)]
    assert all(value > 0 for value in regression)

    return {
        "schema": "amra.opg1757.seventh-active-newton.v1",
        "layers": [15, 16],
        "denominators": [119750400, 1556755200],
        "certificates": certificates,
        "stable_ranges": {
            "odd": "n>=22 (k>=27 odd)",
            "even": "n>=26 (k>=34 even)",
        },
        "direct_values": direct,
        "finite_regression": [6, 100],
        "diagonal_cross_check": diagonal_cross_check(),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
