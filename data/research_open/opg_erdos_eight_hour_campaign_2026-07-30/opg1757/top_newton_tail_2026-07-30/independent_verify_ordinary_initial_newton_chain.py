#!/usr/bin/env python3
"""Exact symbolic certificate for the initial ordinary Newton chain.

This uses only the published closed formulas for beta_(d,1..3).  It
imports no finite-profile or real-root verifier.
"""

from __future__ import annotations

import json

import sympy as sp


D, X = sp.symbols("d x")


def elementary_symbols():
    e1 = (
        22 * D**3 + 147 * D**2 + 161 * D - 258
    ) / sp.Integer(36)
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
    return e1, e2, e3


def positive_shift_coefficients(expression, shift):
    numerator = sp.together(expression).as_numer_denom()[0]
    polynomial = sp.Poly(sp.expand(numerator.subs(D, X + shift)), X)
    coefficients = polynomial.all_coeffs()
    assert all(value > 0 for value in coefficients)
    return coefficients


def audit():
    e1, e2, e3 = elementary_symbols()
    sign_certificates = {
        "e1_shift_d_minus_1": positive_shift_coefficients(e1, 1),
        "e2_shift_d_minus_2": positive_shift_coefficients(e2, 2),
        "e3_shift_d_minus_3": positive_shift_coefficients(e3, 3),
    }

    a1 = e1 / D
    a2 = 2 * e2 / (D * (D - 1))
    a3 = 6 * e3 / (D * (D - 1) * (D - 2))
    first_difference = sp.factor(a1**2 - a2)
    second_difference = sp.factor(a2**2 - a1 * a3)
    first_coefficients = positive_shift_coefficients(
        first_difference, 2
    )
    second_coefficients = positive_shift_coefficients(
        second_difference, 3
    )

    expected_first_denominator = 2592 * D**2 * (D - 1)
    expected_second_denominator = (
        503884800 * D**2 * (D - 2) * (D - 1) ** 2
    )
    assert sp.factor(
        sp.together(first_difference).as_numer_denom()[1]
        - expected_first_denominator
    ) == 0
    assert sp.factor(
        sp.together(second_difference).as_numer_denom()[1]
        - expected_second_denominator
    ) == 0

    defect_gap = sp.factor(3 * D**3 - e1)
    gap_coefficients = positive_shift_coefficients(defect_gap, 2)
    assert defect_gap.subs(D, 1) > 0

    # Direct exact redundancy at a broad finite range.
    finite_checks = 0
    for depth in range(3, 1001):
        values = [value.subs(D, depth) for value in (a1, a2, a3)]
        assert all(value > 0 for value in values)
        assert values[0] ** 2 > values[1]
        assert values[1] ** 2 > values[0] * values[2]
        assert values[0] <= 3 * depth**2
        finite_checks += 1

    return {
        "schema": "amra.opg1757.ordinary-initial-newton-chain.v1",
        "status": "PROVED",
        "finite_root_evidence_used": False,
        "positive_symbol_shifts": {
            name: [str(value) for value in coefficients]
            for name, coefficients in sign_certificates.items()
        },
        "first_newton_shift_coefficients": [
            str(value) for value in first_coefficients
        ],
        "second_newton_shift_coefficients": [
            str(value) for value in second_coefficients
        ],
        "defect_gap_shift_coefficients": [
            str(value) for value in gap_coefficients
        ],
        "unconditional_weighted_C3_ranks": [0, 1, 2, 3],
        "finite_redundancy_depths": finite_checks,
        "minimal_remaining_target": (
            "normalized signed symbol log-concavity for every rank"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
