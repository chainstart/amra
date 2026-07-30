#!/usr/bin/env python3
"""Independent certificate for beta_(d,5) and its Newton inequality."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from independent_verify_all_fixed_rank_ordinary_symbol_algorithm import (
    D,
    K,
    T,
    X as PROFILE_X,
    central_moment_coefficient,
    determinant_kernels,
    exact_ordinary_polynomial,
    profile_functions,
)
from independent_verify_ordinary_rank_four_symbol import (
    expected_b4,
    lower_elementary_symbols,
    rank_four_polynomial,
)


X = sp.symbols("x")
RANK_FIVE_DENOMINATOR = sp.Integer(42664933785600)
RANK_FIVE_COEFFICIENTS = (
    -15479380,
    -325941210,
    -3742393522,
    -6592418448,
    111326408900,
    573131680737,
    -2606390331587,
    -10630453797180,
    79178201476618,
    110117646980439,
    -1139766102529649,
    -2901603595595082,
    14532178406634252,
    4464839765897784,
    14350329772954848,
    -57046347650960640,
)


def rank_five_polynomial(variable=D):
    return sum(
        coefficient * variable ** (15 - index)
        for index, coefficient in enumerate(RANK_FIVE_COEFFICIENTS)
    ) / RANK_FIVE_DENOMINATOR


def expected_h7():
    polynomial = (
        9543257389 * T**16 - 143148860835 * T**15
        + 994394387070 * T**14 - 4235267606808 * T**13
        + 12338941458459 * T**12 - 25976391558075 * T**11
        + 40729494946896 * T**10 - 48438581343930 * T**9
        + 44391584537658 * T**8 - 32029801985664 * T**7
        + 18828105712416 * T**6 - 8334690418656 * T**5
        + 2529274688640 * T**4 + 694098084960 * T**3
        + 1370090181600 * T**2 + 343631393280 * T
        + 27695001600
    )
    return -T**8 * polynomial / (3265920 * (1 - T) ** 16)


def expected_b5():
    polynomial = (
        9543257389 * T**15 - 140250399969 * T**14
        + 951749798832 * T**13 - 3945460303470 * T**12
        + 11135319369237 * T**11 - 22571194746933 * T**10
        + 33805605333654 * T**9 - 38027667126492 * T**8
        + 32629922959320 * T**7 - 21910689192672 * T**6
        + 12053146354704 * T**5 - 4690002325680 * T**4
        + 1006414204320 * T**3 + 1035063126720 * T**2
        + 1393726461120 * T + 363745105920
    )
    return -T**5 * polynomial / (6531840 * (1 - T) ** 16)


def euler_generating_function():
    base = T**5 / (1 - T)
    derivatives = [base]
    for _ in range(15):
        derivatives.append(
            sp.factor(T * sp.diff(derivatives[-1], T))
        )
    return sp.factor(
        sum(
            sp.Rational(
                RANK_FIVE_COEFFICIENTS[15 - power],
                RANK_FIVE_DENOMINATOR,
            )
            * derivatives[power]
            for power in range(16)
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
    e2, e3 = lower_elementary_symbols()
    e4 = rank_four_polynomial()
    e5 = -rank_five_polynomial()
    a3 = 6 * e3 / (D * (D - 1) * (D - 2))
    a4 = (
        24 * e4
        / (D * (D - 1) * (D - 2) * (D - 3))
    )
    a5 = (
        120 * e5
        / (D * (D - 1) * (D - 2) * (D - 3) * (D - 4))
    )
    return a3, a4, a5


def central_rank(kernels, total_rank):
    """Compute only one central rank, avoiding lower-rank re-expansion."""
    value = sp.S.Zero
    half = sp.Rational(1, 2)
    for determinant_rank in range(2, total_rank + 1):
        inverse_rank = total_rank - determinant_rank
        for moment in range(0, 2 * inverse_rank + 1, 2):
            coefficient = central_moment_coefficient(
                moment,
                inverse_rank,
            )
            if coefficient:
                value += (
                    coefficient
                    / sp.factorial(moment)
                    * sp.diff(
                        kernels[determinant_rank],
                        PROFILE_X,
                        moment,
                    ).subs(PROFILE_X, half)
                )
    return sp.factor(value)


def profile_filtration_audit(profiles, maximum_rank):
    """Check the pole filtration and four leading endpoint jets."""
    endpoint = sp.symbols("w")
    profile_w = 1 - 2 * PROFILE_X
    checks = 0
    for rank in range(maximum_rank + 1):
        jets = []
        for profile_index in range(3):
            normalized = sp.cancel(
                profiles[profile_index][rank] / sp.sqrt(profile_w)
                * profile_w ** (3 * rank)
            )
            assert sp.denom(normalized) == 1
            assert sp.Poly(normalized, PROFILE_X).degree() <= 3 * rank
            endpoint_polynomial = sp.expand(
                normalized.subs(PROFILE_X, (1 - endpoint) / 2)
            )
            jets.append([
                endpoint_polynomial.coeff(endpoint, jet)
                for jet in range(min(4, 3 * rank + 1))
            ])
            checks += 1
        if rank:
            assert jets[0][0] == jets[1][0] == jets[2][0]
            assert jets[0][1] == jets[1][1] == jets[2][1] == 0
            for jet in (2, 3):
                assert 2 * jets[1][jet] == jets[0][jet] + jets[2][jet]
    return checks


def fast_audit():
    b5 = expected_b5()
    assert sp.simplify(euler_generating_function() - b5) == 0

    e5 = -rank_five_polynomial()
    e5_shift = positive_shift(e5, 5)
    a3, a4, a5 = normalized_symbols()
    newton_difference = sp.factor(a4**2 - a3 * a5)
    newton_shift = positive_shift(newton_difference, 5)
    c3_gap = sp.factor((3 * D**2) ** 5 - a5)
    c3_shift = positive_shift(c3_gap, 5)

    finite_checks = 0
    for depth in range(5, 13):
        polynomial = exact_ordinary_polynomial(depth)
        actual = polynomial.coeff_monomial(K ** (depth - 5))
        assert actual == rank_five_polynomial().subs(D, depth)
        finite_checks += 1

    return {
        "schema": "amra.opg1757.ordinary-rank-five-symbol.v1",
        "status": "PASS",
        "logical_basis": (
            "all-depth when full_symbolic_recurrence is true; "
            "finite checks alone are redundant"
        ),
        "rank_five_degree": 15,
        "rank_five_sign_shift_coefficients": [
            str(value) for value in e5_shift
        ],
        "fourth_newton_shift_coefficients": [
            str(value) for value in newton_shift
        ],
        "rank_five_C3_gap_shift_coefficients": [
            str(value) for value in c3_shift
        ],
        "euler_generating_function_identity": True,
        "finite_exact_ordinary_checks": finite_checks,
        "full_symbolic_recurrence": False,
    }


def full_symbolic_audit():
    result = fast_audit()
    profiles = profile_functions(7)
    filtration_checks = profile_filtration_audit(profiles, 7)
    kernels = determinant_kernels(profiles, 7)
    h7 = central_rank(kernels, 7)
    assert sp.simplify(h7 - expected_h7()) == 0

    # The already certified B4 contains (H2+...+H6)/(2*t^4).
    # This avoids recomputing and refactoring six lower central ranks.
    derived_b5 = sp.factor(
        expected_b4() + h7 / (2 * T**4)
    )
    assert sp.simplify(derived_b5 - expected_b5()) == 0
    result["full_symbolic_recurrence"] = True
    result["profile_maximum_rank"] = 7
    result["profile_filtration_and_jet_checks"] = filtration_checks
    result["H7_identity"] = True
    result["B5_identity_from_B4_and_H7"] = True
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
