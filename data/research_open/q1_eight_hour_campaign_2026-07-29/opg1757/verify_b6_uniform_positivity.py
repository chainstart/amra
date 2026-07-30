#!/usr/bin/env python3
"""Symbolic certificate for coefficientwise positivity of the B6 bracket."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

from five_page_union_formula import (
    k3_coefficients,
    k4_coefficients,
    k5_coefficients,
)
from six_page_union_formula import (
    b6_bracket_coefficients,
    k6_coefficients,
)


BETA, S, N = sp.symbols("beta s n", integer=True, nonnegative=True)


def falling_choose(top: sp.Expr, lower: int) -> sp.Expr:
    if lower < 0:
        return sp.S.Zero
    return sp.prod(top - index for index in range(lower)) / sp.factorial(lower)


def powered_choose(top: sp.Expr, lower: int, base: int) -> sp.Expr:
    if lower < 0:
        return sp.S.Zero
    return base**lower * falling_choose(top, lower)


def f_coefficient_formula(s: sp.Expr, degree: int) -> sp.Expr:
    term6 = sum(
        coefficient * powered_choose(2 * s - 14, degree - order, 6)
        for order, coefficient in enumerate(k6_coefficients(s))
    )
    term5 = sum(
        sp.binomial(2, q)
        * s**q
        * sum(
            coefficient
            * powered_choose(2 * s - 12, degree - q - order, 5)
            for order, coefficient in enumerate(k5_coefficients(s))
        )
        for q in range(3)
    )
    term4 = sum(
        sp.binomial(4, q)
        * s**q
        * sum(
            coefficient
            * powered_choose(2 * s - 10, degree - q - order, 4)
            for order, coefficient in enumerate(k4_coefficients(s))
        )
        for q in range(5)
    )
    term3 = sum(
        sp.binomial(6, q)
        * s**q
        * sum(
            coefficient
            * powered_choose(2 * s - 8, degree - q - order, 3)
            for order, coefficient in enumerate(k3_coefficients(s))
        )
        for q in range(7)
    )
    term2 = sum(
        sp.binomial(8, q)
        * s**q
        * powered_choose(2 * s - 6, degree - q, 2)
        for q in range(9)
    )
    return sp.expand(term6 - 4 * term5 + 6 * term4 - 4 * term3 + term2)


def g_coefficient_formula(s: sp.Expr, degree: int) -> sp.Expr:
    term6 = sum(
        coefficient * powered_choose(2 * s - 14, degree - order, 6)
        for order, coefficient in enumerate(k6_coefficients(s))
    )
    term5 = sum(
        sp.binomial(2, q)
        * s**q
        * sum(
            coefficient
            * powered_choose(2 * s - 12, degree - q - order, 5)
            for order, coefficient in enumerate(k5_coefficients(s))
        )
        for q in range(3)
    )
    return sp.expand(term6 - 4 * term5)


def polynomial_coefficients_nonnegative(
    expression: sp.Expr, variable: sp.Symbol
) -> bool:
    return all(
        coefficient >= 0
        for coefficient in sp.Poly(sp.expand(expression), variable).all_coeffs()
    )


def build_audit() -> dict[str, object]:
    for degree in range(8):
        if sp.expand(f_coefficient_formula(S, degree)) != 0:
            raise AssertionError(f"beta^{degree} should vanish")

    low_rows: list[list[object]] = []
    for degree in range(8, 20):
        coefficient = sp.factor(
            f_coefficient_formula(S, degree).subs(S, N + 7)
        )
        if degree <= 17:
            positive = polynomial_coefficients_nonnegative(coefficient, N)
        elif degree == 18:
            divisor = N * (N + 1) * (N + 2) * (N + 3) * (2 * N - 1)
            quotient = sp.cancel(coefficient / divisor)
            positive = polynomial_coefficients_nonnegative(quotient, N)
        else:
            divisor = (
                N
                * (N - 1)
                * (N + 1)
                * (N + 2)
                * (N + 3)
                * (2 * N - 1)
            )
            quotient = sp.cancel(coefficient / divisor)
            positive = polynomial_coefficients_nonnegative(quotient, N)
        if not positive:
            raise AssertionError(f"low coefficient beta^{degree} failed")
        low_rows.append([degree, str(coefficient)])

    lam = 1 + S * BETA
    lam_next = 1 + (S + 1) * BETA
    u5 = 1 + 5 * BETA
    u6 = 1 + 6 * BETA
    k5 = sum(
        coefficient * BETA**degree
        for degree, coefficient in enumerate(k5_coefficients(S))
    )
    k5_next = k5.subs(S, S + 1)
    k6 = sum(
        coefficient * BETA**degree
        for degree, coefficient in enumerate(k6_coefficients(S))
    )
    delta = sp.expand(k6.subs(S, S + 1) - k6)
    if any(
        not polynomial_coefficients_nonnegative(coefficient, S)
        for coefficient in sp.Poly(delta / BETA**2, BETA).all_coeffs()
    ):
        raise AssertionError("Delta K6 is not positive")
    h = sp.expand(
        u6**2 * lam**2 * k5 - u5**2 * lam_next**2 * k5_next
    )
    exponent = 2 * S - 12
    p0 = sp.expand(delta + 4 * h)
    initial = sp.expand(
        u5**2 * p0
        + exponent * BETA * u5 * delta
        + exponent * (exponent - 1) * BETA**2 * delta / 2
    )
    initial_poly = sp.Poly(
        sp.expand(initial.subs(S, N + 15) / BETA**2),
        BETA,
    )
    initial_rows: list[list[object]] = []
    for (degree,), coefficient in reversed(initial_poly.terms()):
        if not polynomial_coefficients_nonnegative(coefficient, N):
            raise AssertionError("the merged three-layer certificate failed")
        initial_rows.append([degree, str(sp.factor(coefficient))])

    u20 = sp.factor(
        (
            g_coefficient_formula(S + 1, 20)
            - g_coefficient_formula(S, 20)
        ).subs(S, N + 15)
    )
    u21 = sp.factor(
        (
            g_coefficient_formula(S + 1, 21)
            - g_coefficient_formula(S, 21)
            - 12 * g_coefficient_formula(S, 20)
        ).subs(S, N + 15)
    )
    if not polynomial_coefficients_nonnegative(u20, N):
        raise AssertionError("beta^20 boundary failed")
    if not polynomial_coefficients_nonnegative(u21, N):
        raise AssertionError("beta^21 boundary failed")

    base_tail = [
        [degree, str(int(g_coefficient_formula(sp.Integer(15), degree)))]
        for degree in range(20, 33)
    ]
    if any(int(row[1]) <= 0 for row in base_tail):
        raise AssertionError("the G15 tail base failed")

    finite_early: list[list[object]] = []
    for s in range(7, 15):
        maximum = 2 * s + 2
        values = [
            int(g_coefficient_formula(sp.Integer(s), degree))
            for degree in range(20, maximum + 1)
        ]
        if any(value < 0 for value in values):
            raise AssertionError(f"early G tail failed at s={s}")
        finite_early.append(
            [s, len(values), str(min(values)) if values else "empty"]
        )

    for s in range(7, 18):
        direct = b6_bracket_coefficients(s)
        reconstructed = [
            int(f_coefficient_formula(sp.Integer(s), degree))
            for degree in range(len(direct))
        ]
        if direct != reconstructed:
            raise AssertionError(f"five-term formula mismatch at s={s}")

    payload = json.dumps(
        [low_rows, initial_rows, str(u20), str(u21), base_tail, finite_early],
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "schema": "amra.complete_split.b6_uniform_positivity.v1",
        "theorem": (
            "For every integer s>=7, the B6 bracket F_s is "
            "coefficientwise nonnegative; with the s=6 boundary, B6 is "
            "coefficientwise nonnegative for every admissible s."
        ),
        "proof_split": (
            "F=G+3*(C-2D+E)+2*(D-E)+3*C, where the two brackets are "
            "the proved B4 and B3 brackets and G=A-4B. Degrees 8..19 "
            "of F have explicit positive n=s-7 formulas. The degree>=20 "
            "tail of G is proved by a positive truncated recurrence."
        ),
        "low_degree_F_coefficients_in_n_s_minus_7": low_rows,
        "tail_recurrence": (
            "For Q=G_(s+1)-u6^2 G_s, Delta=K6_(s+1)-K6_s, "
            "H=u6^2 lambda_s^2 K5_s-u5^2 lambda_(s+1)^2 K5_(s+1), "
            "M=2s-12. For s>=15, Q=u5^(M-2)*I_s+sum_(r=3)^M "
            "C(M,r) beta^r u5^(M-r) Delta; I_s is the merged r=0,1,2 "
            "polynomial certified below."
        ),
        "merged_three_layer_I_over_beta2_coefficients": initial_rows,
        "truncated_tail_boundary_beta20": str(u20),
        "truncated_tail_boundary_beta21": str(u21),
        "tail_base_G15_degree_coefficient": base_tail,
        "finite_early_tail_s_count_minimum": finite_early,
        "sha256_symbolic_payload": hashlib.sha256(payload).hexdigest(),
        "status": "proved",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audit = build_audit()
    rendered = json.dumps(audit, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
