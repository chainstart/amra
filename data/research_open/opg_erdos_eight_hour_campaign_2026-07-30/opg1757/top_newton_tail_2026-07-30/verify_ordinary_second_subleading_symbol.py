#!/usr/bin/env python3
"""Exact certificate for the ordinary second-subleading symbol.

This file deliberately does not alter the first-subleading verifier.  It
checks the new rank-four profile formula, the H4 determinant reduction, and
independent finite-depth values using exact rational arithmetic.
"""

from __future__ import annotations

import argparse
import json
from functools import lru_cache

import sympy as sp

from verify_ordinary_subleading_symbol import (
    claimed_functions,
    ordinary_coefficient,
    profile_polynomial,
)


D, J, K, T, X, Z = sp.symbols("d j k t x z")


def rank_four_functions():
    """Return the three conjectured rank-four profile generating functions."""
    w = 1 - 2 * Z
    numerators = [
        -Z
        * (
            146176 * Z**11
            - 663552 * Z**10
            + 1220352 * Z**9
            - 774144 * Z**8
            - 736992 * Z**7
            + 2750976 * Z**6
            - 8160912 * Z**5
            + 13685760 * Z**4
            + 47385675 * Z**3
            - 112674240 * Z**2
            + 40091760 * Z
            + 17729280
        ),
        Z
        * (
            690451712 * Z**11
            - 3711086592 * Z**10
            + 8894124288 * Z**9
            - 12380967936 * Z**8
            + 10858590432 * Z**7
            - 6111072000 * Z**6
            + 2540586384 * Z**5
            - 1519300800 * Z**4
            + 1006618725 * Z**3
            - 199208160 * Z**2
            - 73347120 * Z
            + 4976640
        ),
        -Z
        * (
            38115777280 * Z**11
            - 189099147264 * Z**10
            + 412563816192 * Z**9
            - 516716734464 * Z**8
            + 407929881888 * Z**7
            - 212168180736 * Z**6
            + 75677948784 * Z**5
            - 19289301120 * Z**4
            + 3340767915 * Z**3
            - 487969920 * Z**2
            + 184051440 * Z
            - 23950080
        ),
    ]
    return [
        numerator / (155520 * w ** sp.Rational(23, 2))
        for numerator in numerators
    ]


def second_symbol(depth):
    """Closed form proposed for [k^(d-2)] b_(k,d), d >= 2."""
    return sp.Rational(1, 5184) * (
        286 * depth**6
        + 3546 * depth**5
        + 12721 * depth**4
        - 7812 * depth**3
        - 86231 * depth**2
        + 40338 * depth
        + 209160
    )


def first_defect(depth):
    """Positive A_d in b_(k,d) = k^d - A_d k^(d-1) + ... ."""
    return sp.Rational(1, 36) * (
        22 * depth**3
        + 147 * depth**2
        + 161 * depth
        - 258
    )


def claimed_h4():
    return (
        T**5
        * (
            2389 * T**7
            - 14334 * T**6
            + 34245 * T**5
            - 40008 * T**4
            + 22152 * T**3
            - 5400 * T**2
            + 3672 * T
            + 144
        )
        / (36 * (1 - T) ** 7)
    )


@lru_cache(maxsize=1)
def determinant_functions():
    """Build G2, G3, G4 and H4 from the profile symbols."""
    a, p, q, s = claimed_functions()
    v4 = rank_four_functions()
    u = T * X
    v = T * (1 - X)
    at = lambda expression, value: expression.subs(Z, value)

    g2 = T**2 * (
        (at(q[1], u) - at(q[0], u)) * at(a, v)
        + at(a, u) * (at(q[1], v) - at(q[2], v))
        + at(p[1], u) * at(p[1], v)
        - at(p[0], u) * at(p[2], v)
    )
    g3 = T**3 * (
        (at(s[1], u) - at(s[0], u)) * at(a, v)
        + at(a, u) * (at(s[1], v) - at(s[2], v))
        + at(p[1], u) * at(q[1], v)
        + at(q[1], u) * at(p[1], v)
        - at(p[0], u) * at(q[2], v)
        - at(q[0], u) * at(p[2], v)
    )
    g4 = T**4 * (
        (at(v4[1], u) - at(v4[0], u)) * at(a, v)
        + at(a, u) * (at(v4[1], v) - at(v4[2], v))
        + at(p[1], u) * at(s[1], v)
        + at(s[1], u) * at(p[1], v)
        + at(q[1], u) * at(q[1], v)
        - at(p[0], u) * at(s[2], v)
        - at(s[0], u) * at(p[2], v)
        - at(q[0], u) * at(q[2], v)
    )
    half = sp.Rational(1, 2)
    h4 = (
        g4.subs(X, half)
        + sp.diff(g3, X, 2).subs(X, half) / 8
        + sp.diff(g2, X, 4).subs(X, half) / 128
    )
    return g2, g3, g4, sp.factor(h4)


def symbol_generating_function():
    return (
        Z**2
        * (
            2389 * Z**6
            - 13818 * Z**5
            + 31221 * Z**4
            - 32952 * Z**3
            + 14112 * Z**2
            - 1116 * Z
            + 3024
        )
        / (72 * (1 - Z) ** 7)
    )


def formally_summed_second_symbol():
    """Compute sum_(d>=2) q_d z^d using the Euler operator z*d/dz."""
    basis = [Z**2 / (1 - Z)]
    for _ in range(6):
        basis.append(sp.factor(Z * sp.diff(basis[-1], Z)))
    polynomial = sp.Poly(second_symbol(D), D)
    return sp.factor(
        sum(
            polynomial.coeff_monomial(D**power) * basis[power]
            for power in range(7)
        )
    )


def audit(maximum_loss: int = 18, maximum_depth: int = 12):
    if maximum_loss < 4:
        raise ValueError("maximum_loss must be at least 4")
    if maximum_depth < 2:
        raise ValueError("maximum_depth must be at least 2")

    v4 = rank_four_functions()
    profile_checks = 0
    for profile_index in range(3):
        series = sp.series(
            v4[profile_index],
            Z,
            0,
            maximum_loss - 3,
        ).removeO().expand()
        for loss in range(4, maximum_loss + 1):
            polynomial = profile_polynomial(profile_index, loss)
            actual = polynomial.coeff_monomial(J ** (loss - 4))
            expected = series.coeff(Z, loss - 4)
            if actual != expected:
                raise AssertionError(
                    f"rank-four profile mismatch: h={profile_index}, "
                    f"loss={loss}, actual={actual}, expected={expected}"
                )
            profile_checks += 1

    _, _, _, h4 = determinant_functions()
    expected_h4 = claimed_h4()
    if sp.simplify(h4 - expected_h4) != 0:
        raise AssertionError("H4 simplification failed")

    # The proposed d-generating function is checked as a rational identity,
    # not merely by comparing an initial series.
    summed = formally_summed_second_symbol()
    if sp.simplify(summed - symbol_generating_function()) != 0:
        raise AssertionError("second-symbol generating function failed")

    coefficient_checks = 0
    rows = []
    for depth in range(2, maximum_depth + 1):
        start = max(2, (depth + 5) // 2)
        points = []
        for page_count in range(start, start + depth + 3):
            value = ordinary_coefficient(page_count, depth)
            points.append(
                (
                    page_count,
                    sp.Rational(value.numerator, value.denominator),
                )
            )
        polynomial = sp.Poly(sp.interpolate(points[: depth + 1], K), K)
        if polynomial.degree() > depth:
            raise AssertionError("ordinary coefficient has excessive degree")
        if not all(
            polynomial.eval(page_count) == value
            for page_count, value in points[depth + 1 :]
        ):
            raise AssertionError("ordinary polynomial spare check failed")
        actual = polynomial.coeff_monomial(K ** (depth - 2))
        expected = second_symbol(depth)
        if actual != expected:
            raise AssertionError(
                f"second symbol mismatch at depth {depth}: "
                f"{actual} != {expected}"
            )
        coefficient_checks += 1
        rows.append(
            {
                "depth": depth,
                "second_symbol": str(actual),
                "spare_checks": 2,
            }
        )

    # The discriminant of the quadratic truncation is positive for d >= 2:
    # after d=y+2 every coefficient is positive.
    y = sp.symbols("y", nonnegative=True)
    discriminant = sp.factor(first_defect(D) ** 2 - 4 * second_symbol(D))
    shifted_numerator = sp.Poly(
        sp.together(discriminant.subs(D, y + 2)).as_numer_denom()[0],
        y,
    )
    if any(coefficient <= 0 for coefficient in shifted_numerator.all_coeffs()):
        raise AssertionError("shifted discriminant positivity check failed")

    return {
        "schema": "amra.opg1757.ordinary-second-subleading-symbol.v1",
        "scope": (
            "Independent exact finite regression. It verifies the rank-four profile "
            "formula through the requested loss, the H4 rational identity, "
            "and exact ordinary polynomials through the requested depth. "
            "The separate rank-four saddle certificate now supplies the "
            "all-loss profile-resummation proof."
        ),
        "maximum_loss": maximum_loss,
        "rank_four_profile_checks": profile_checks,
        "maximum_depth": maximum_depth,
        "ordinary_polynomial_checks": coefficient_checks,
        "H4": str(expected_h4),
        "second_symbol_generating_function": str(
            symbol_generating_function()
        ),
        "quadratic_discriminant": str(discriminant),
        "rows": rows,
        "status": "finite_certificate_passed",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-loss", type=int, default=18)
    parser.add_argument("--maximum-depth", type=int, default=12)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_loss, args.maximum_depth),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
