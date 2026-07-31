#!/usr/bin/env python3
"""Exact algebra certificate for the universal second Laurent symbol."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import sympy as sp
from sympy.functions.combinatorial.numbers import stirling


E, R, H, F, W, L, X, Z = sp.symbols(
    "e rho h f sigma ell x z"
)


def endpoint_b(e: sp.Expr, rho: sp.Expr, h: sp.Expr) -> sp.Expr:
    return (
        ((15 - 4 * e) * rho - e * (4 * e + 5)) / 3
        - h * (rho + 2 * e)
    )


def endpoint_g(e: sp.Expr, r: sp.Expr, h: sp.Expr) -> sp.Expr:
    return sp.expand(
        (
            16 * e**4 + 48 * e**3 * h + 32 * e**3 * r + 30 * e**3
            + 36 * e**2 * h**2 + 72 * e**2 * h * r
            + 36 * e**2 * h + 16 * e**2 * r**2
            - 106 * e**2 * r + 5 * e**2 + 36 * e * h**2 * r
            - 18 * e * h**2 + 24 * e * h * r**2
            - 186 * e * h * r - 30 * e * h - 136 * e * r**2
            - 256 * e * r - 15 * e + 9 * h**2 * r**2
            - 27 * h**2 * r - 99 * h * r**2 + 9 * h * r
            + 315 * r**2 - 423 * r
        ) / 18
    )


def endpoint_j(e: sp.Expr, r: sp.Expr, h: sp.Expr) -> sp.Expr:
    return sp.expand(
        -(
            320 * e**6 + 1440 * e**5 * h + 960 * e**5 * r
            + 600 * e**5 + 2160 * e**4 * h**2
            + 3600 * e**4 * h * r + 1260 * e**4 * h
            + 960 * e**4 * r**2 - 3360 * e**4 * r - 178 * e**4
            + 4320 * e**3 * h**2 * r + 2700 * e**3 * h**2
            + 2880 * e**3 * h * r**2 - 11790 * e**3 * h * r
            - 4410 * e**3 * h + 320 * e**3 * r**3
            - 8520 * e**3 * r**2 - 13928 * e**3 * r
            - 1017 * e**3 + 2700 * e**2 * h**2 * r**2
            - 7560 * e**2 * h**2 * r - 7830 * e**2 * h**2
            + 720 * e**2 * h * r**3 - 19710 * e**2 * h * r**2
            - 22545 * e**2 * h * r + 1440 * e**2 * h
            - 4560 * e**2 * r**3 + 9390 * e**2 * r**2
            - 35541 * e**2 * r - 313 * e**2
            + 540 * e * h**2 * r**3 - 9045 * e * h**2 * r**2
            - 7155 * e * h**2 * r + 2970 * e * h**2
            - 6660 * e * h * r**3 + 24795 * e * h * r**2
            - 21510 * e * h * r + 270 * e * h
            + 23140 * e * r**3 + 34215 * e * r**2
            - 57616 * e * r + 588 * e - 2025 * h**2 * r**3
            + 3645 * h**2 * r**2 - 1620 * h**2 * r
            + 16200 * h * r**3 - 18630 * h * r**2
            + 2430 * h * r - 42525 * r**3 + 189945 * r**2
            - 147420 * r
        ) / 810
    )


def falling_coefficients(shift: sp.Expr, ell: sp.Expr) -> list[sp.Expr]:
    p1 = ell * shift + ell * (ell - 1) / 2
    p2 = (
        ell * shift**2
        + shift * ell * (ell - 1)
        + ell * (ell - 1) * (2 * ell - 1) / 6
    )
    p3 = (
        ell * shift**3
        + sp.Rational(3, 2) * shift**2 * ell * (ell - 1)
        + sp.Rational(1, 2)
        * shift * ell * (ell - 1) * (2 * ell - 1)
        + (ell * (ell - 1) / 2) ** 2
    )
    return [
        sp.Integer(1),
        -p1,
        (p1**2 - p2) / 2,
        -(p1**3 - 3 * p1 * p2 + 2 * p3) / 6,
    ]


def effective_endpoint(
    e: sp.Expr,
    rho: sp.Expr,
    h: int,
    shift: sp.Expr,
    ell: sp.Expr,
) -> list[sp.Expr]:
    endpoint = [
        sp.Integer(1),
        endpoint_b(e, rho, h),
        endpoint_g(e, rho, h),
        endpoint_j(e, rho, h),
    ]
    falling = falling_coefficients(shift, ell)
    return [
        sp.expand(
            sum(endpoint[k] * falling[n - k] for k in range(n + 1))
        )
        for n in range(4)
    ]


def product_third(left: list[sp.Expr], right: list[sp.Expr]) -> sp.Expr:
    return (
        left[3] + right[3] + left[2] * right[1]
        + left[1] * right[2]
    )


def oriented_kernel(
    e: sp.Expr,
    rho: sp.Expr,
    f: sp.Expr,
    sigma: sp.Expr,
    ell: sp.Expr,
) -> sp.Expr:
    positive_left = effective_endpoint(
        e, rho, 1, rho + e + 2, ell
    )
    positive_right = effective_endpoint(
        f, sigma, 1, sigma + f + 2, ell
    )
    negative_left = effective_endpoint(
        e, rho, 0, rho + e + 1, ell
    )
    negative_right = effective_endpoint(
        f, sigma, 2, sigma + f + 3, ell
    )
    return sp.expand(
        product_third(positive_left, positive_right)
        - product_third(negative_left, negative_right)
    )


def symmetric_third_kernel() -> sp.Expr:
    forward = oriented_kernel(E, R, F, W, L)
    backward = oriented_kernel(F, W, E, R, L)
    result = sp.factor((forward + backward) / 2)
    if sp.Poly(result, E, R, F, W, L).total_degree() != 4:
        raise AssertionError("third kernel did not collapse to degree four")
    return result


def touchard(power: int, mean: sp.Expr) -> sp.Expr:
    return sum(
        stirling(power, k, kind=2) * mean**k
        for k in range(power + 1)
    )


def moment_polynomial(kernel: sp.Expr) -> sp.Expr:
    mu_r = X * (1 + Z) / 2
    mu_e = X * Z * (1 + Z) / 2
    mu_l = X * Z**2
    answer = sp.Integer(0)
    for powers, coefficient in sp.Poly(
        kernel, E, R, F, W, L
    ).terms():
        pe, pr, pf, pw, pl = powers
        answer += coefficient * (
            touchard(pe, mu_e)
            * touchard(pr, mu_r)
            * touchard(pf, mu_e)
            * touchard(pw, mu_r)
            * touchard(pl, mu_l)
        )
    return sp.factor(answer)


def audit_symbol() -> tuple[sp.Expr, sp.Expr]:
    kernel = symmetric_third_kernel()
    measured = sp.factor(4 * moment_polynomial(kernel))
    atom = 1 + 2 * Z + 2 * Z**2
    p0 = (
        4 + sp.Rational(20, 3) * Z - 4 * Z**2
        - 22 * Z**3 - sp.Rational(58, 3) * Z**4
    )
    p1 = (
        -sp.Rational(2, 3) * Z - 3 * Z**2
        - 4 * Z**3 - sp.Rational(8, 3) * Z**4
    )
    expected = sp.factor(
        4 * X**2 / atom * (p0 + p1 + p1 * atom * X)
    )
    # Both sides multiply exp(x*atom), which was removed before comparison.
    if sp.cancel(measured - expected) != 0:
        raise AssertionError("universal second-symbol MGF failed")
    return kernel, measured


def boundary_audit() -> dict[str, object]:
    """Red-team the singular-looking and extreme-offset cases exactly."""
    atom = 1 + 2 * Z + 2 * Z**2

    # q=1 is the only displayed case with A^{-1}: cancel it exactly.
    p_one = 4 + 6 * Z - 7 * Z**2 - 26 * Z**3 - 22 * Z**4
    q_one_quotient = 4 - 2 * Z - 11 * Z**2
    if sp.expand(p_one - atom * q_one_quotient) != 0:
        raise AssertionError("q=1 apparent denominator did not cancel")

    # At e=0,c=1 all relative corrections vanish, for every h.
    for marked in (0, 1, 2):
        values = (
            endpoint_b(0, 0, marked),
            endpoint_g(0, 0, marked),
            endpoint_j(0, 0, marked),
        )
        if any(sp.cancel(value) != 0 for value in values):
            raise AssertionError(
                f"minimal endpoint correction failed for h={marked}"
            )

    checked_coefficients = 0
    for q in range(1, 31):
        p_q = (
            4 - sp.Rational(2 * (q - 10), 3) * Z
            - (3 * q + 4) * Z**2
            - 2 * (2 * q + 11) * Z**3
            - sp.Rational(2 * (4 * q + 29), 3) * Z**4
        )
        symbol = sp.Poly(
            sp.cancel(
                sp.Rational(4 * q, sp.factorial(q))
                * atom ** (q - 2) * p_q
            ),
            Z,
        )
        if symbol.nth(0) != sp.Rational(16, sp.factorial(q - 1)):
            raise AssertionError(f"bottom boundary failed at q={q}")
        expected_top = -sp.Rational(
            2 ** (q + 1) * q * (4 * q + 29),
            3 * sp.factorial(q),
        )
        if symbol.nth(2 * q) != expected_top:
            raise AssertionError(f"top boundary failed at q={q}")

        leading = sp.Poly(4 * atom**q / sp.factorial(q), Z)
        if any(coefficient <= 0 for coefficient in leading.all_coeffs()):
            raise AssertionError(f"leading-symbol sign failed at q={q}")
        checked_coefficients += 2 * q + 1

    if sp.Poly(4 * atom**0, Z).as_expr() != 4:
        raise AssertionError("q=0 leading-symbol boundary failed")

    return {
        "q_one_cancelled_quotient": str(4 * q_one_quotient),
        "minimal_endpoint_corrections_checked": 9,
        "positive_leading_coefficients_checked_q_1_to_30": checked_coefficients,
        "second_symbol_boundary_pairs_checked": 30,
        "q_zero_leading_symbol": 4,
    }


def filtered_functional_first_order_audit() -> int:
    """Guard the unified h=0,1,2 functional behind the degree lemma."""

    t, v, rho, excess = sp.symbols("t v rho excess")
    v0 = t - t**2 / 2
    v1 = -v * t**3 / 3
    exponential0 = sp.exp(v * t**2 / 2)
    exponential1 = exponential0 * v**2 * t**3 / 6
    jacobian0 = 1 - t
    jacobian1 = -v * t**2

    def euler(expression: sp.Expr) -> sp.Expr:
        return sp.expand(t * sp.diff(expression, t))

    def poisson_extract(polynomial: sp.Expr) -> sp.Expr:
        answer = sp.Integer(0)
        for (v_power, rho_power), coefficient in sp.Poly(
            polynomial, v, rho
        ).terms():
            answer += (
                coefficient
                * 2**v_power
                * sp.prod(excess - index for index in range(v_power))
                * rho**rho_power
            )
        return sp.factor(answer)

    checked = 0
    for marked in range(3):
        coefficient = sp.Rational(1, 2**marked)
        shift = marked + 2
        bracket0 = (
            v0**rho
            + coefficient * rho * jacobian0 * v0 ** (rho - 1)
        )
        bracket1 = (
            v * t * v0**rho
            + rho * v0 ** (rho - 1) * v1
            + coefficient
            * rho
            * (
                jacobian1 * v0 ** (rho - 1)
                + jacobian0
                * (rho - 1)
                * v0 ** (rho - 2)
                * v1
            )
        )
        p0 = exponential0 * bracket0
        p1 = exponential0 * bracket1 + exponential1 * bracket0
        functional1 = -sp.Rational(1, 2) * (
            euler(euler(p0)) + (2 * shift - 1) * euler(p0)
        )
        raw_ratio = sp.factor(
            (p1 + functional1).subs(t, 1)
            / (sp.Rational(1, 2) ** rho * sp.exp(v / 2))
        )
        measured = poisson_extract(sp.expand(raw_ratio))
        expected = sp.factor(
            ((15 - 4 * excess) * rho - excess * (4 * excess + 5))
            / 3
            - marked * (rho + 2 * excess)
        )
        if sp.cancel(measured - expected) != 0:
            raise AssertionError(
                f"filtered functional mismatch at h={marked}"
            )
        checked += 1
    return checked


def endpoint_table_audit() -> int:
    here = pathlib.Path(__file__).resolve().parent
    old = (
        here.parents[1]
        / "q1_three_hour_campaign_2026-07-31"
        / "opg1757"
    )
    sys.path.insert(0, str(old))
    try:
        from verify_second_deficit import S
        from verify_seventh_q6 import Q6_ENDPOINT_POLYNOMIALS
    finally:
        sys.path.pop(0)

    checked = 0
    for (h, e, c), expression in Q6_ENDPOINT_POLYNOMIALS.items():
        rho = c - 1
        degree = 2 * c + 2 * e - 2
        leading = sp.Rational(
            1, 2 ** (rho + e) * sp.factorial(rho) * sp.factorial(e)
        )
        polynomial = sp.Poly(expression, S)
        g_measured = (
            sp.Integer(0) if degree < 2 else polynomial.nth(degree - 2) / leading
        )
        j_measured = (
            sp.Integer(0) if degree < 3 else polynomial.nth(degree - 3) / leading
        )
        if sp.cancel(g_measured - endpoint_g(e, rho, h)) != 0:
            raise AssertionError(f"endpoint g mismatch at {(h, e, c)}")
        if sp.cancel(j_measured - endpoint_j(e, rho, h)) != 0:
            raise AssertionError(f"endpoint j mismatch at {(h, e, c)}")
        checked += 2
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extended-endpoints", action="store_true")
    args = parser.parse_args()
    kernel, moment = audit_symbol()
    boundaries = boundary_audit()
    filtered_checks = filtered_functional_first_order_audit()
    endpoint_checks = endpoint_table_audit() if args.extended_endpoints else 0
    print(
        json.dumps(
            {
                "schema": "amra.opg1757.second-symbol-theorem.v1",
                "status": "PASS",
                "theorem_status": "PROVED",
                "symmetric_kernel_total_degree": sp.Poly(
                    kernel, E, R, F, W, L
                ).total_degree(),
                "symmetric_kernel_terms": len(
                    sp.Poly(kernel, E, R, F, W, L).terms()
                ),
                "moment_polynomial": str(moment),
                "boundary_red_team": boundaries,
                "extended_endpoint_coefficients_checked": endpoint_checks,
                "filtered_functional_markings_checked": filtered_checks,
                "second_symbol": (
                    "4/q! * A(z)^(q-2) * q * "
                    "[4-2(q-10)z/3-(3q+4)z^2-2(2q+11)z^3"
                    "-2(4q+29)z^4/3]"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
