#!/usr/bin/env python3
"""Independent certificate for beta_(d,6) and its Newton inequality."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from independent_verify_all_fixed_rank_ordinary_symbol_algorithm import (
    D,
    K,
    T,
    determinant_kernels,
    exact_ordinary_polynomial,
    profile_functions,
)
from independent_verify_ordinary_rank_four_symbol import (
    rank_four_polynomial,
)
from independent_verify_ordinary_rank_five_symbol import (
    central_rank,
    expected_b5,
    profile_filtration_audit,
    rank_five_polynomial,
)


X = sp.symbols("x")
RANK_SIX_DENOMINATOR = sp.Integer(2764687709306880000)
RANK_SIX_COEFFICIENTS = (
    7301929250,
    153379721250,
    2431268137725,
    2874784928400,
    -80975845704300,
    -935374628777400,
    3592457053926440,
    19939081990290120,
    -117051403660829448,
    -390355621772659110,
    3565087697695904835,
    15186099809099153160,
    -139123168520225939854,
    129786516909791432460,
    43553643530874118200,
    3926765129917260384720,
    -11165053968083036288448,
    13833562112789217292800,
    -18754809088236550963200,
)


def rank_six_polynomial(variable=D):
    return sum(
        coefficient * variable ** (18 - index)
        for index, coefficient in enumerate(RANK_SIX_COEFFICIENTS)
    ) / RANK_SIX_DENOMINATOR


def expected_h8():
    polynomial = (
        5468059639079 * T**19 - 98425073503422 * T**18
        + 832166041491657 * T**17 - 4386391163231004 * T**16
        + 16131986564398785 * T**15 - 43895988773511894 * T**14
        + 91460251525777407 * T**13 - 149080189693453272 * T**12
        + 192876273599662584 * T**11 - 200404423224844200 * T**10
        + 169391623321654920 * T**9 - 117375238792050480 * T**8
        + 66995289814356720 * T**7 - 26873881152249600 * T**6
        + 9672918137406720 * T**5 + 437297380128000 * T**4
        + 8356871743516800 * T**3 + 4715036594956800 * T**2
        + 1054989778348800 * T + 65474119065600
    )
    return T**9 * polynomial / (587865600 * (1 - T) ** 19)


def expected_b6():
    polynomial = (
        5468059639079 * T**18 - 96707287173402 * T**17
        + 801767610507177 * T**16 - 4134187624467924 * T**15
        + 14830405816091625 * T**14 - 39221892759811734 * T**13
        + 79082500484277927 * T**12 - 124083480256039152 * T**11
        + 153583463986914384 * T**10 - 151678254909239820 * T**9
        + 121207591660577760 * T**8 - 78908761803359520 * T**7
        + 41937232067473680 * T**6 - 13707502253383680 * T**5
        + 4613598230169600 * T**4 + 1516898143656000 * T**3
        + 8047513105228800 * T**2 + 5084915163955200 * T
        + 1000541372544000
    )
    return T**6 * polynomial / (1175731200 * (1 - T) ** 19)


def euler_generating_function():
    base = T**6 / (1 - T)
    derivatives = [base]
    for _ in range(18):
        derivatives.append(
            sp.factor(T * sp.diff(derivatives[-1], T))
        )
    return sp.factor(
        sum(
            sp.Rational(
                RANK_SIX_COEFFICIENTS[18 - power],
                RANK_SIX_DENOMINATOR,
            )
            * derivatives[power]
            for power in range(19)
        )
    )


def positive_shift(expression, shift):
    numerator = sp.cancel(expression).as_numer_denom()[0]
    coefficients = sp.Poly(
        sp.expand(numerator.subs(D, X + shift)), X
    ).all_coeffs()
    assert all(value > 0 for value in coefficients)
    return coefficients


def normalized_symbols():
    e4 = rank_four_polynomial()
    e5 = -rank_five_polynomial()
    e6 = rank_six_polynomial()
    a4 = (
        24 * e4
        / (D * (D - 1) * (D - 2) * (D - 3))
    )
    a5 = (
        120 * e5
        / (D * (D - 1) * (D - 2) * (D - 3) * (D - 4))
    )
    a6 = (
        720 * e6
        / (
            D * (D - 1) * (D - 2) * (D - 3)
            * (D - 4) * (D - 5)
        )
    )
    return a4, a5, a6


def fast_audit():
    assert sp.simplify(euler_generating_function() - expected_b6()) == 0

    e6 = rank_six_polynomial()
    e6_shift = positive_shift(e6, 6)
    a4, a5, a6 = normalized_symbols()
    newton_difference = sp.factor(a5**2 - a4 * a6)
    newton_shift = positive_shift(newton_difference, 6)
    c3_gap = sp.factor((3 * D**2) ** 6 - a6)
    c3_shift = positive_shift(c3_gap, 6)

    finite_checks = 0
    for depth in range(6, 13):
        polynomial = exact_ordinary_polynomial(depth)
        actual = polynomial.coeff_monomial(K ** (depth - 6))
        assert actual == e6.subs(D, depth)
        finite_checks += 1

    return {
        "schema": "amra.opg1757.ordinary-rank-six-symbol.v1",
        "status": "PASS",
        "logical_basis": (
            "all-depth when full_symbolic_recurrence is true; "
            "finite checks alone are redundant"
        ),
        "rank_six_degree": 18,
        "rank_six_sign_shift_coefficients": [
            str(value) for value in e6_shift
        ],
        "fifth_newton_shift_coefficients": [
            str(value) for value in newton_shift
        ],
        "rank_six_C3_gap_shift_coefficients": [
            str(value) for value in c3_shift
        ],
        "euler_generating_function_identity": True,
        "finite_exact_ordinary_checks": finite_checks,
        "full_symbolic_recurrence": False,
    }


def full_symbolic_audit():
    result = fast_audit()
    profiles = profile_functions(8)
    filtration_checks = profile_filtration_audit(profiles, 8)
    kernels = determinant_kernels(profiles, 8)
    h8 = central_rank(kernels, 8)
    assert sp.simplify(h8 - expected_h8()) == 0
    derived_b6 = sp.factor(
        expected_b5() + h8 / (2 * T**4)
    )
    assert sp.simplify(derived_b6 - expected_b6()) == 0
    result["full_symbolic_recurrence"] = True
    result["profile_maximum_rank"] = 8
    result["profile_filtration_and_jet_checks"] = filtration_checks
    result["H8_identity"] = True
    result["B6_identity_from_B5_and_H8"] = True
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
