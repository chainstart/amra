#!/usr/bin/env python3
"""Verify the rooted-tree/Lagrange formula for the first F_k coefficient."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import sympy as sp

from verify_general_k_low_coefficients import (
    S,
    complete_graph_forest_dp,
    f_coefficient,
    leading_f_from_complete_graph,
)


def falling(value: sp.Expr, degree: int) -> sp.Expr:
    if degree < 0:
        return sp.S.Zero
    return sp.prod(value - offset for offset in range(degree))


def lagrange_e_symbolic(
    s: sp.Expr, component_parameter: sp.Expr, degree: int
) -> sp.Expr:
    """[u^degree] (1-u/2)^component_parameter exp(s*u)."""
    if degree < 0:
        return sp.S.Zero
    return sp.expand(
        sum(
            sp.Rational((-1) ** index, 2**index)
            * falling(component_parameter, index)
            / sp.factorial(index)
            * s ** (degree - index)
            / sp.factorial(degree - index)
            for index in range(degree + 1)
        )
    )


def lagrange_d_symbolic(
    s: sp.Expr, component_parameter: sp.Expr, degree: int
) -> sp.Expr:
    """[u^degree] (1-u)(1-u/2)^component_parameter exp(s*u)."""
    return sp.expand(
        lagrange_e_symbolic(s, component_parameter, degree)
        - lagrange_e_symbolic(s, component_parameter, degree - 1)
    )


def profile_coefficient_symbolic(
    profile: int, degree: int, s: sp.Expr = S
) -> sp.Expr:
    if profile == 0:
        return sp.expand(
            falling(s, degree)
            * lagrange_d_symbolic(s, s - degree, degree)
        )
    if profile == 1:
        return sp.expand(
            falling(s - 2, degree)
            * lagrange_d_symbolic(s, s - 2 - degree, degree)
        )
    if profile != 2:
        raise ValueError("only profiles 0, 1, 2 are used")
    return sp.expand(
        falling(s - 4, degree)
        * lagrange_d_symbolic(s, s - 4 - degree, degree)
        + 4
        * falling(s - 4, degree - 1)
        * lagrange_e_symbolic(s, s - 3 - degree, degree - 1)
    )


def leading_polynomial_symbolic(page_count: int) -> sp.Expr:
    determinant = sum(
        profile_coefficient_symbolic(1, left)
        * profile_coefficient_symbolic(1, page_count - left)
        - profile_coefficient_symbolic(0, left)
        * profile_coefficient_symbolic(2, page_count - left)
        for left in range(page_count + 1)
    )
    return sp.factor(
        sp.cancel(
            sp.factorial(page_count)
            * determinant
            / (2 * page_count * (page_count - 1))
        )
    )


def lagrange_e_numeric(
    s: int, component_parameter: int, degree: int
) -> Fraction:
    if degree < 0 or component_parameter < 0:
        return 0
    value = sum(
        Fraction(
            (-1) ** index
            * math.comb(component_parameter, index)
            * s ** (degree - index),
            2**index * math.factorial(degree - index),
        )
        for index in range(min(component_parameter, degree) + 1)
    )
    return value


def lagrange_d_numeric(
    s: int, component_parameter: int, degree: int
) -> Fraction:
    return lagrange_e_numeric(
        s, component_parameter, degree
    ) - lagrange_e_numeric(s, component_parameter, degree - 1)


def profile_coefficient_numeric(profile: int, degree: int, s: int) -> int:
    result: Fraction
    if profile == 0:
        component_parameter = s - degree
        if component_parameter < 0:
            return 0
        result = (
            math.factorial(s)
            // math.factorial(component_parameter)
            * lagrange_d_numeric(s, component_parameter, degree)
        )
    elif profile == 1:
        component_parameter = s - 2 - degree
        if component_parameter < 0:
            return 0
        result = (
            math.factorial(s - 2)
            // math.factorial(component_parameter)
            * lagrange_d_numeric(s, component_parameter, degree)
        )
    else:
        if profile != 2:
            raise ValueError("only profiles 0, 1, 2 are used")
        separate_parameter = s - 4 - degree
        separate = Fraction(0)
        if separate_parameter >= 0:
            separate = (
                math.factorial(s - 4)
                // math.factorial(separate_parameter)
                * lagrange_d_numeric(s, separate_parameter, degree)
            )
        joined_parameter = s - 3 - degree
        joined = Fraction(0)
        if degree >= 1 and joined_parameter >= 0:
            joined = (
                4
                * math.factorial(s - 4)
                // math.factorial(joined_parameter)
                * lagrange_e_numeric(s, joined_parameter, degree - 1)
            )
        result = separate + joined
    if result.denominator != 1:
        raise AssertionError("profile coefficient unexpectedly nonintegral")
    return result.numerator


def check_rooted_identities(order: int) -> None:
    rooted = [Fraction(0)] + [
        Fraction(n ** (n - 1), math.factorial(n))
        for n in range(1, order + 1)
    ]

    def multiply(
        left: list[Fraction], right: list[Fraction]
    ) -> list[Fraction]:
        result = [Fraction(0)] * (order + 1)
        for i, left_value in enumerate(left):
            for j, right_value in enumerate(right[: order + 1 - i]):
                result[i + j] += left_value * right_value
        return result

    def exponential(series: list[Fraction]) -> list[Fraction]:
        result = [Fraction(0)] * (order + 1)
        result[0] = 1
        for n in range(1, order + 1):
            result[n] = sum(
                k * series[k] * result[n - k] for k in range(1, n + 1)
            ) / n
        return result

    exp_rooted = exponential(rooted)
    if rooted[1:] != exp_rooted[:-1]:
        raise AssertionError("R=z*exp(R) truncation failed")
    unrooted_direct = [Fraction(0)] + [
        Fraction(1 if n == 1 else n ** (n - 2), math.factorial(n))
        for n in range(1, order + 1)
    ]
    rooted_square = multiply(rooted, rooted)
    if unrooted_direct != [
        rooted[n] - rooted_square[n] / 2 for n in range(order + 1)
    ]:
        raise AssertionError("unrooted-tree identity failed")
    one_mark_direct = [
        (
            Fraction(1)
            if n == 0
            else Fraction(2 * (n + 2) ** (n - 1), math.factorial(n))
        )
        for n in range(order + 1)
    ]
    if one_mark_direct != exponential([2 * value for value in rooted]):
        raise AssertionError("A=exp(2R) failed")
    two_mark_direct = [
        Fraction((n + 4) ** n, math.factorial(n))
        for n in range(order + 1)
    ]
    reciprocal = [Fraction(0)] * (order + 1)
    reciprocal[0] = 1
    for n in range(1, order + 1):
        reciprocal[n] = sum(
            rooted[k] * reciprocal[n - k] for k in range(1, n + 1)
        )
    if two_mark_direct != multiply(
        exponential([4 * value for value in rooted]), reciprocal
    ):
        raise AssertionError("B/(4x)=exp(4R)/(1-R) failed")


def symmetrized_contributions(page_count: int, s: int) -> list[int]:
    profiles = [
        complete_graph_forest_dp(profile, s - 2 * profile, page_count)
        for profile in range(3)
    ]
    contributions: list[int] = []
    for left in range(page_count // 2 + 1):
        right = page_count - left
        value = (
            2 * profiles[1][left] * profiles[1][right]
            - profiles[0][left] * profiles[2][right]
            - profiles[0][right] * profiles[2][left]
        )
        if left == right:
            value //= 2
        contributions.append(value)
    return contributions


def leading_coefficient_numeric(page_count: int, s: int) -> int:
    profiles = [
        [
            profile_coefficient_numeric(profile, degree, s)
            for degree in range(page_count + 1)
        ]
        for profile in range(3)
    ]
    determinant = sum(
        profiles[1][left] * profiles[1][page_count - left]
        - profiles[0][left] * profiles[2][page_count - left]
        for left in range(page_count + 1)
    )
    numerator = math.factorial(page_count) * determinant
    denominator = 2 * page_count * (page_count - 1)
    if numerator % denominator:
        raise AssertionError("leading coefficient unexpectedly nonintegral")
    return numerator // denominator


def forward_differences(values: list[int]) -> list[int]:
    result: list[int] = []
    current = values
    while current:
        result.append(current[0])
        current = [
            current[index + 1] - current[index]
            for index in range(len(current) - 1)
        ]
    return result


def build_audit() -> dict[str, object]:
    rooted_identity_order = 12
    check_rooted_identities(rooted_identity_order)

    profile_rows: list[list[object]] = []
    for s in range(4, 13):
        for profile in range(3):
            expected = complete_graph_forest_dp(
                profile, s - 2 * profile, s
            )
            actual = tuple(
                profile_coefficient_numeric(profile, degree, s)
                for degree in range(s + 1)
            )
            if actual != expected:
                raise AssertionError("Lagrange profile formula failed")
            profile_rows.append(
                [s, profile, [str(value) for value in actual]]
            )

    symbolic_rows: list[list[object]] = []
    for page_count in range(2, 8):
        actual = leading_polynomial_symbolic(page_count)
        expected = f_coefficient(page_count, 2 * page_count - 4)
        if sp.expand(actual - expected) != 0:
            raise AssertionError("symbolic leading-F formula failed")
        symbolic_rows.append([page_count, str(actual)])

    obstruction_rows: list[list[object]] = []
    for page_count, s in ((3, 4), (4, 4), (5, 5), (6, 6)):
        contributions = symmetrized_contributions(page_count, s)
        if sum(contributions) < 0:
            raise AssertionError("total determinant unexpectedly negative")
        if page_count >= 3 and not any(value < 0 for value in contributions):
            raise AssertionError("expected termwise sign obstruction vanished")
        obstruction_rows.append(
            [page_count, s, [str(value) for value in contributions]]
        )

    base4_newton_rows: list[list[object]] = []
    base4_dp_rows: list[list[object]] = []
    for page_count in range(2, 31):
        polynomial_degree = 2 * page_count - 4
        values = [
            leading_coefficient_numeric(page_count, 4 + offset)
            for offset in range(polynomial_degree + 1)
        ]
        coefficients = forward_differences(values)
        first_expected = (page_count - 2) // 2
        first_actual = next(
            (
                index
                for index, coefficient in enumerate(coefficients)
                if coefficient
            ),
            None,
        )
        if first_actual != first_expected:
            raise AssertionError("base-4 Newton support pattern failed")
        if any(coefficient < 0 for coefficient in coefficients):
            raise AssertionError("base-4 Newton coefficient failed")
        if coefficients[-1] != math.factorial(polynomial_degree):
            raise AssertionError("base-4 Newton leading coefficient failed")
        base4_newton_rows.append(
            [
                page_count,
                first_actual,
                [str(coefficient) for coefficient in coefficients],
            ]
        )
        for s in (
            4,
            4 + first_expected,
            4 + polynomial_degree,
        ):
            actual = leading_coefficient_numeric(page_count, s)
            expected = leading_f_from_complete_graph(page_count, s)
            if actual != expected:
                raise AssertionError("base-4 DP crosscheck failed")
            base4_dp_rows.append([page_count, s, str(actual)])

    payload = json.dumps(
        [
            profile_rows,
            symbolic_rows,
            obstruction_rows,
            base4_newton_rows,
            base4_dp_rows,
        ],
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "schema": "amra.complete_split.f_leading_lagrange.v1",
        "rooted_identity_order": rooted_identity_order,
        "rooted_identities": {
            "R": "R=z*exp(R)",
            "U": "U=(R-R^2/2)/x, with z=v*x",
            "A": "A=exp(2*R)",
            "B": "B=4*x*exp(4*R)/(1-R)",
        },
        "lagrange_kernels": {
            "E_c_d": (
                "[u^d](1-u/2)^c*exp(s*u)"
                "=sum_r(-1)^r*binom(c,r)*s^(d-r)/(2^r*(d-r)!)"
            ),
            "D_c_d": "E_c_d-E_c_(d-1)",
            "laguerre": (
                "E_c_d=(-1)^d*2^(-d)*LaguerreL(d,c-d,2*s)"
            ),
        },
        "profile_formula": {
            "Phi0_j": "(s)_j*D_(s-j,j)",
            "Phi1_j": "(s-2)_j*D_(s-2-j,j)",
            "Phi2_j": (
                "(s-4)_j*D_(s-4-j,j)"
                "+4*(s-4)_(j-1)*E_(s-3-j,j-1)"
            ),
            "C_k": (
                "sum_(i=0)^k(Phi1_i*Phi1_(k-i)"
                "-Phi0_i*Phi2_(k-i))"
            ),
        },
        "profile_dp_crosscheck_rows_s4_to_s12": profile_rows,
        "symbolic_crosscheck_rows_k2_to_k7": symbolic_rows,
        "termwise_sign_obstruction_rows": obstruction_rows,
        "base4_newton_rows_k2_to_k30": base4_newton_rows,
        "base4_lagrange_vs_dp_rows": base4_dp_rows,
        "base4_support_theorem": (
            "For s=4+r, each Phi1 factor has degree at most s-2, "
            "while Phi0 and Phi2 have degrees at most s-1 and s-3. "
            "At total degree 2s-4 the unique top products cancel by "
            "the weighted Cayley tree values T_h=2^h*s^(s-h-2). "
            "Thus C_k(s)=0 for k>2s-5, proving that every base-4 "
            "Newton coefficient below floor((k-2)/2) vanishes. "
            "Equality of the first support index and nonnegativity "
            "through k=30 are finite exact evidence, not a general proof."
        ),
        "scope": (
            "The rooted-tree reduction and finite Laguerre convolution "
            "are exact. Base-4 Newton nonnegativity is audited only for "
            "k=2..30. The formulas do not prove general positivity: already "
            "at (k,s)=(3,4), the symmetrized i=0,3 summand is -16 and "
            "is rescued by the +20 i=1,2 summand."
        ),
        "sha256_payload": hashlib.sha256(payload).hexdigest(),
        "status": "proved_formula_not_general_positivity",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rendered = json.dumps(build_audit(), indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
