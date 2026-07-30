#!/usr/bin/env python3
"""Exact certificate for fixed-band positivity decidability."""

from __future__ import annotations

import json
from fractions import Fraction

import sympy as sp

from independent_verify_ordinary_rank_eight_and_eighth_band import (
    DEPTH,
    derive_triangles,
)


U = sp.symbols("u", integer=True, nonnegative=True)


def ceil_fraction(value: Fraction) -> int:
    return (value.numerator + value.denominator - 1) // value.denominator


def cauchy_bound(polynomial: sp.Poly) -> Fraction:
    coefficients = tuple(
        Fraction(int(value)) for value in polynomial.all_coeffs()
    )
    leading = coefficients[0]
    if leading <= 0:
        raise ValueError("positive leading coefficient required")
    if len(coefficients) == 1:
        return Fraction(0)
    return Fraction(1) + max(
        abs(value / leading) for value in coefficients[1:]
    )


def exact_integer_interval_decision(
    polynomial: sp.Poly,
) -> dict[str, object]:
    """Decide positivity on all nonnegative integers.

    This function executes the finite Cauchy interval for general
    modest-size inputs.  A coefficientwise-positive polynomial uses
    the exact stronger shortcut, which also certifies every integer in
    the finite interval without iterating through a potentially huge
    list.
    """

    bound = cauchy_bound(polynomial)
    endpoint = ceil_fraction(bound)
    coefficients = tuple(int(value) for value in polynomial.all_coeffs())
    coefficientwise_positive = all(value > 0 for value in coefficients)

    if coefficientwise_positive:
        violations = []
        method = "coefficientwise-positive finite-interval shortcut"
    else:
        violations = [
            value
            for value in range(endpoint + 1)
            if polynomial.eval(value) <= 0
        ]
        method = "explicit exact Cauchy-interval enumeration"

    return {
        "positive_on_all_nonnegative_integers": not violations,
        "cauchy_bound": (
            f"{bound.numerator}/{bound.denominator}"
            if bound.denominator != 1
            else str(bound.numerator)
        ),
        "finite_check_endpoint": endpoint,
        "finite_check_count": endpoint + 1,
        "method": method,
        "coefficientwise_positive": coefficientwise_positive,
        "violations": violations,
    }


def band_certificate(band: int, expression) -> dict[str, object]:
    minimum_depth = 2 * band + 1
    shifted = sp.cancel(expression.subs(DEPTH, U + minimum_depth))
    numerator, denominator = shifted.as_numer_denom()
    assert denominator > 0
    polynomial = sp.Poly(sp.expand(numerator), U)
    assert polynomial.degree() == 3 * band + 2
    assert polynomial.LC() > 0

    decision = exact_integer_interval_decision(polynomial)
    assert decision["positive_on_all_nonnegative_integers"]
    return {
        "band": band,
        "minimum_depth": minimum_depth,
        "degree": polynomial.degree(),
        "positive_leading_coefficient": True,
        "shifted_denominator": str(denominator),
        **decision,
    }


def audit() -> dict[str, object]:
    _, bands = derive_triangles()
    certificates = [
        band_certificate(band, expression)
        for band, expression in enumerate(bands)
    ]
    assert [item["band"] for item in certificates] == list(range(8))
    return {
        "schema": (
            "amra.opg1757.all-fixed-band-positivity-"
            "decidability.v1"
        ),
        "status": "PASS",
        "corollary": (
            "For each fixed q, positivity of gamma_(d,q) on all "
            "admissible integer depths is decidable by a finite "
            "exact computation."
        ),
        "logical_inputs": [
            "all-fixed-rank exact ordinary-symbol algorithm",
            "degree beta_(d,r)=3r",
            "exact ordinary-to-falling and long-recurrence triangles",
            "degree gamma_(d,q)=3q+2 with positive leading coefficient",
            "Cauchy complex-root bound",
        ],
        "replayed_positive_bands": certificates,
        "claim_boundary": (
            "A decision procedure for each input q; not a proof that "
            "every q returns TRUE and not a uniform positivity theorem."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
