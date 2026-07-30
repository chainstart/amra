#!/usr/bin/env python3
"""Independent certificate for beta_(d,4) and its Newton inequality."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from independent_verify_all_fixed_rank_ordinary_symbol_algorithm import (
    D,
    K,
    T,
    central_kernels,
    determinant_kernels,
    exact_ordinary_polynomial,
    profile_functions,
)


X = sp.symbols("x")
RANK_FOUR_DENOMINATOR = sp.Integer(169305292800)
RANK_FOUR_COEFFICIENTS = (
    5672590,
    111345780,
    940800098,
    1247424360,
    -19928038791,
    -49386060432,
    332001672380,
    627890141256,
    -5187992393129,
    -5254056336228,
    25894282085892,
    59075314211664,
    -31756394113920,
)


def rank_four_polynomial(variable=D):
    return sum(
        coefficient * variable ** (12 - index)
        for index, coefficient in enumerate(RANK_FOUR_COEFFICIENTS)
    ) / RANK_FOUR_DENOMINATOR


def expected_h6():
    polynomial = (
        69010973 * T**13 - 828131676 * T**12
        + 4500844542 * T**11 - 14591534844 * T**10
        + 31260693837 * T**9 - 46346440896 * T**8
        + 48607255008 * T**7 - 36796779360 * T**6
        + 21341475216 * T**5 - 10053253440 * T**4
        + 3647118960 * T**3 + 984234240 * T**2
        + 650592000 * T + 50855040
    )
    return T**7 * polynomial / (77760 * (1 - T) ** 13)


def expected_b4():
    polynomial = (
        69010973 * T**12 - 808314420 * T**11
        + 4268197710 * T**10 - 13359121428 * T**9
        + 27385842717 * T**8 - 38351424456 * T**7
        + 37307986992 * T**6 - 25675484328 * T**5
        + 13629418560 * T**4 - 6085860480 * T**3
        + 1956966480 * T**2 + 1499316480 * T
        + 659404800
    )
    return T**4 * polynomial / (155520 * (1 - T) ** 13)


def euler_generating_function():
    base = T**4 / (1 - T)
    derivatives = [base]
    for _ in range(12):
        derivatives.append(
            sp.factor(T * sp.diff(derivatives[-1], T))
        )
    return sp.factor(
        sum(
            sp.Rational(
                RANK_FOUR_COEFFICIENTS[12 - power],
                RANK_FOUR_DENOMINATOR,
            )
            * derivatives[power]
            for power in range(13)
        )
    )


def lower_elementary_symbols():
    e2 = (
        286 * D**6 + 3546 * D**5 + 12721 * D**4
        - 7812 * D**3 - 86231 * D**2 + 40338 * D
        + 209160
    ) / sp.Integer(5184)
    e3 = (
        158450 * D**9 + 2651625 * D**8 + 15805020 * D**7
        + 6658380 * D**6 - 213815208 * D**5
        - 151402725 * D**4 + 2063879770 * D**3
        + 1562087520 * D**2 - 10631426832 * D
        - 6142443840
    ) / sp.Integer(83980800)
    return e2, e3


def positive_shift(expression, shift):
    numerator = sp.cancel(expression).as_numer_denom()[0]
    coefficients = sp.Poly(
        sp.expand(numerator.subs(D, X + shift)), X
    ).all_coeffs()
    assert all(value > 0 for value in coefficients)
    return coefficients


def fast_audit():
    b4 = expected_b4()
    assert sp.simplify(euler_generating_function() - b4) == 0

    e4 = rank_four_polynomial()
    e4_shift = positive_shift(e4, 4)
    e2, e3 = lower_elementary_symbols()
    a2 = 2 * e2 / (D * (D - 1))
    a3 = 6 * e3 / (D * (D - 1) * (D - 2))
    a4 = 24 * e4 / (D * (D - 1) * (D - 2) * (D - 3))
    newton_difference = sp.factor(a3**2 - a2 * a4)
    newton_shift = positive_shift(newton_difference, 4)
    c3_gap = sp.factor((3 * D**2) ** 4 - a4)
    c3_shift = positive_shift(c3_gap, 4)

    finite_checks = 0
    for depth in range(4, 13):
        polynomial = exact_ordinary_polynomial(depth)
        actual = polynomial.coeff_monomial(K ** (depth - 4))
        assert actual == e4.subs(D, depth)
        finite_checks += 1

    return {
        "schema": "amra.opg1757.ordinary-rank-four-symbol.v1",
        "status": "PASS",
        "logical_basis": (
            "all-depth when full_symbolic_recurrence is true; "
            "finite checks alone are redundant"
        ),
        "rank_four_degree": 12,
        "rank_four_shift_coefficients": [
            str(value) for value in e4_shift
        ],
        "third_newton_shift_coefficients": [
            str(value) for value in newton_shift
        ],
        "rank_four_C3_gap_shift_coefficients": [
            str(value) for value in c3_shift
        ],
        "euler_generating_function_identity": True,
        "finite_exact_ordinary_checks": finite_checks,
        "full_symbolic_recurrence": False,
    }


def full_symbolic_audit():
    result = fast_audit()
    profiles = profile_functions(6)
    kernels = determinant_kernels(profiles, 6)
    central = central_kernels(kernels, 6)
    assert sp.simplify(central[6] - expected_h6()) == 0
    derived_b4 = sp.factor(
        sum(central[rank] for rank in range(2, 7))
        / (2 * T**4)
    )
    assert sp.simplify(derived_b4 - expected_b4()) == 0
    result["full_symbolic_recurrence"] = True
    result["profile_maximum_rank"] = 6
    result["H6_identity"] = True
    result["B4_identity_from_H2_through_H6"] = True
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-symbolic", action="store_true")
    arguments = parser.parse_args()
    result = (
        full_symbolic_audit()
        if arguments.full_symbolic
        else fast_audit()
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
