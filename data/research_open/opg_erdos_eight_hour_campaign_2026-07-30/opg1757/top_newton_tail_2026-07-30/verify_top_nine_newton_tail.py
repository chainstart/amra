#!/usr/bin/env python3
"""Exact certificate for OPG-1757 top Newton depths six, seven, and eight."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


K, X = sp.symbols("k x", integer=True)


def lagrange_e(s: int, component_parameter: int, degree: int) -> Fraction:
    """[u^degree] (1-u/2)^component_parameter exp(su)."""
    if degree < 0 or component_parameter < 0:
        return Fraction(0)
    return sum(
        (
            Fraction(
                (-1) ** index
                * math.comb(component_parameter, index)
                * s ** (degree - index),
                2**index * math.factorial(degree - index),
            )
        )
        for index in range(min(component_parameter, degree) + 1)
    )


def lagrange_d(s: int, component_parameter: int, degree: int) -> Fraction:
    return lagrange_e(s, component_parameter, degree) - lagrange_e(
        s, component_parameter, degree - 1
    )


@lru_cache(maxsize=None)
def profile(profile_index: int, degree: int, s: int) -> int:
    """The exact coefficient U_(h,degree)(s), with impossible cases zero."""
    if profile_index == 0:
        parameter = s - degree
        if parameter < 0:
            return 0
        value = (
            math.factorial(s)
            // math.factorial(parameter)
            * lagrange_d(s, parameter, degree)
        )
    elif profile_index == 1:
        parameter = s - 2 - degree
        if parameter < 0:
            return 0
        value = (
            math.factorial(s - 2)
            // math.factorial(parameter)
            * lagrange_d(s, parameter, degree)
        )
    elif profile_index == 2:
        separate_parameter = s - 4 - degree
        joined_parameter = s - 3 - degree
        separate = Fraction(0)
        joined = Fraction(0)
        if separate_parameter >= 0:
            separate = (
                math.factorial(s - 4)
                // math.factorial(separate_parameter)
                * lagrange_d(s, separate_parameter, degree)
            )
        if degree >= 1 and joined_parameter >= 0:
            joined = (
                4
                * math.factorial(s - 4)
                // math.factorial(joined_parameter)
                * lagrange_e(s, joined_parameter, degree - 1)
            )
        value = separate + joined
    else:
        raise ValueError("only h=0,1,2 occur")
    if value.denominator != 1:
        raise AssertionError("profile coefficient is not integral")
    return value.numerator


@lru_cache(maxsize=None)
def leading_polynomial_value(page_count: int, vertex_count: int) -> int:
    """Evaluate c_k(s) exactly from the two-profile determinant."""
    rows = [
        [
            profile(profile_index, edge_count, vertex_count)
            for edge_count in range(page_count + 1)
        ]
        for profile_index in range(3)
    ]
    determinant = sum(
        rows[1][left] * rows[1][page_count - left]
        - rows[0][left] * rows[2][page_count - left]
        for left in range(page_count + 1)
    )
    numerator = math.factorial(page_count) * determinant
    denominator = 2 * page_count * (page_count - 1)
    if numerator % denominator:
        raise AssertionError("c_k(s) is not integral")
    return numerator // denominator


@lru_cache(maxsize=None)
def newton_row(page_count: int) -> tuple[int, ...]:
    """Return Delta^q c_k(4), q=0,...,2k-4."""
    degree = 2 * page_count - 4
    current = [
        leading_polynomial_value(page_count, 4 + offset)
        for offset in range(degree + 1)
    ]
    row: list[int] = []
    while current:
        row.append(current[0])
        current = [
            current[index + 1] - current[index]
            for index in range(len(current) - 1)
        ]
    return tuple(row)


def normalized_tail_value(page_count: int, depth: int) -> Fraction:
    index = 2 * page_count - 4 - depth
    if index < 0:
        raise ValueError("the requested layer does not exist")
    return Fraction(newton_row(page_count)[index], math.factorial(index))


Q6 = (
    4032 * K**8
    - 24192 * K**7
    + 9072 * K**6
    - 319760 * K**5
    - 296716 * K**4
    + 3115760 * K**3
    + 29380477 * K**2
    + 103674567 * K
    + 153772290
)
Q7 = (
    576 * K**9
    - 4608 * K**8
    + 9744 * K**7
    - 75488 * K**6
    - 66724 * K**5
    + 254944 * K**4
    + 6661499 * K**3
    + 37990606 * K**2
    + 117200435 * K
    + 160178004
)
Q8 = (
    34560 * K**11
    - 599040 * K**10
    + 3893760 * K**9
    - 17736960 * K**8
    + 55219360 * K**7
    - 15634240 * K**6
    + 657272176 * K**5
    + 682878800 * K**4
    - 9060987065 * K**3
    - 88234978600 * K**2
    - 335731520391 * K
    - 533577731400
)

FORMULAS = {
    6: (
        (K - 5)
        * (K - 4)
        * (K - 3)
        * (K - 2)
        * Q6
        / 45360
    ),
    7: (
        (K - 6)
        * (K - 5)
        * (K - 4)
        * (K - 3)
        * (K - 2)
        * Q7
        / 22680
    ),
    8: (
        (K - 6)
        * (K - 5)
        * (K - 4)
        * (K - 3)
        * (K - 2)
        * Q8
        / 5443200
    ),
}


def interpolate_from_exact_rows(depth: int, start: int) -> sp.Expr:
    """Use exactly degree-bound+1 determinant values, not the formula."""
    points = [
        (page_count, sp.Rational(normalized_tail_value(page_count, depth)))
        for page_count in range(start, start + 2 * depth + 1)
    ]
    return sp.factor(sp.interpolate(points, K))


def audit(maximum_k: int = 27) -> dict[str, object]:
    if maximum_k < 25:
        raise ValueError("maximum_k must be at least 25 for redundant checks")

    starts = {6: 6, 7: 7, 8: 7}
    interpolation: dict[str, str] = {}
    exact_checks = 0
    redundant_checks = 0
    for depth, formula in FORMULAS.items():
        reconstructed = interpolate_from_exact_rows(depth, starts[depth])
        if sp.cancel(reconstructed - formula) != 0:
            raise AssertionError(f"depth {depth} interpolation mismatch")
        if sp.Poly(reconstructed, K).degree() != 2 * depth:
            raise AssertionError(f"depth {depth} degree mismatch")
        interpolation[str(depth)] = str(reconstructed)

        interpolation_end = starts[depth] + 2 * depth
        first_existing = math.ceil((depth + 4) / 2)
        for page_count in range(first_existing, maximum_k + 1):
            actual = sp.Rational(normalized_tail_value(page_count, depth))
            expected = formula.subs(K, page_count)
            if actual != expected:
                raise AssertionError(
                    f"depth {depth}, k={page_count}: formula mismatch"
                )
            exact_checks += 1
            if page_count > interpolation_end:
                redundant_checks += 1

    shifted_q6 = sp.Poly(sp.expand(Q6.subs(K, X + 6)), X)
    shifted_q7 = sp.Poly(sp.expand(Q7.subs(K, X + 7)), X)
    shifted_q8 = sp.Poly(sp.expand(Q8.subs(K, X + 7)), X)
    if not all(value > 0 for value in shifted_q6.all_coeffs()):
        raise AssertionError("Q6 shifted-coefficient positivity failed")
    if not all(value > 0 for value in shifted_q7.all_coeffs()):
        raise AssertionError("Q7 shifted-coefficient positivity failed")

    q8_coefficients = dict(shifted_q8.terms())
    if any(
        coefficient <= 0
        for (power,), coefficient in q8_coefficients.items()
        if power != 2
    ):
        raise AssertionError("Q8 has an unexpected nonpositive coefficient")
    a = q8_coefficients[(3,)]
    b = q8_coefficients[(2,)]
    c = q8_coefficients[(1,)]
    discriminant = sp.expand(b**2 - 4 * a * c)
    if not (a > 0 and discriminant < 0):
        raise AssertionError("Q8 positive quadratic block failed")

    expected_leads = {
        depth: sp.Rational(2**depth, math.factorial(depth))
        for depth in FORMULAS
    }
    actual_leads = {
        depth: sp.Poly(formula, K).LC()
        for depth, formula in FORMULAS.items()
    }
    if actual_leads != expected_leads:
        raise AssertionError("fixed-depth leading asymptotic mismatch")

    boundary = {
        "p_5_6": str(normalized_tail_value(5, 6)),
        "p_6_6": str(normalized_tail_value(6, 6)),
        "p_6_7": str(normalized_tail_value(6, 7)),
        "p_6_8": str(normalized_tail_value(6, 8)),
        "p_7_7": str(normalized_tail_value(7, 7)),
        "p_7_8": str(normalized_tail_value(7, 8)),
    }
    if boundary != {
        "p_5_6": "0",
        "p_6_6": "31104",
        "p_6_7": "0",
        "p_6_8": "0",
        "p_7_7": "2331720",
        "p_7_8": "155520",
    }:
        raise AssertionError("boundary activity check failed")

    return {
        "schema": "amra.opg1757.top-nine-newton-tail.v1",
        "method": (
            "Exact finite Lagrange sums -> determinant values -> "
            "base-four forward differences.  The proved degree bound "
            "deg_k p_(k,d)<=2d turns 2d+1 values into a polynomial "
            "identity; later k values are redundant checks."
        ),
        "interpolated_formulas": interpolation,
        "exact_formula_checks": exact_checks,
        "redundant_checks": redundant_checks,
        "maximum_k": maximum_k,
        "boundary": boundary,
        "shifted_Q6_coefficients": [
            str(value) for value in shifted_q6.all_coeffs()
        ],
        "shifted_Q7_coefficients": [
            str(value) for value in shifted_q7.all_coeffs()
        ],
        "shifted_Q8_coefficients": [
            str(value) for value in shifted_q8.all_coeffs()
        ],
        "Q8_quadratic_block_discriminant": str(discriminant),
        "leading_coefficients": {
            str(depth): str(value)
            for depth, value in actual_leads.items()
        },
        "status": "proved_exact_top_depths_0_through_8",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-k", type=int, default=27)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_k), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
