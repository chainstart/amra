#!/usr/bin/env python3
"""Symbolic certificate for coefficientwise positivity of the B7 bracket."""

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
from seven_page_union_formula import (
    b7_bracket_coefficients,
    k7_coefficients,
)
from six_page_union_formula import k6_coefficients


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
    kernels = [
        k7_coefficients(s),
        k6_coefficients(s),
        k5_coefficients(s),
        k4_coefficients(s),
        k3_coefficients(s),
        [1],
    ]
    multipliers = [1, -5, 10, -10, 5, -1]
    lambda_degrees = [0, 2, 4, 6, 8, 10]
    bases = [7, 6, 5, 4, 3, 2]
    exponents = [
        2 * s - 16,
        2 * s - 14,
        2 * s - 12,
        2 * s - 10,
        2 * s - 8,
        2 * s - 6,
    ]
    return sp.expand(
        sum(
            multipliers[index]
            * sum(
                sp.binomial(lambda_degrees[index], q)
                * s**q
                * sum(
                    coefficient
                    * powered_choose(
                        exponents[index],
                        degree - q - order,
                        bases[index],
                    )
                    for order, coefficient in enumerate(kernels[index])
                )
                for q in range(lambda_degrees[index] + 1)
            )
            for index in range(6)
        )
    )


def g_coefficient_formula(s: sp.Expr, degree: int) -> sp.Expr:
    term7 = sum(
        coefficient * powered_choose(2 * s - 16, degree - order, 7)
        for order, coefficient in enumerate(k7_coefficients(s))
    )
    term6 = sum(
        sp.binomial(2, q)
        * s**q
        * sum(
            coefficient
            * powered_choose(2 * s - 14, degree - q - order, 6)
            for order, coefficient in enumerate(k6_coefficients(s))
        )
        for q in range(3)
    )
    return sp.expand(term7 - 5 * term6)


def coefficients_nonnegative(expression: sp.Expr, variable: sp.Symbol) -> bool:
    return all(
        coefficient >= 0
        for coefficient in sp.Poly(sp.expand(expression), variable).all_coeffs()
    )


def build_audit() -> dict[str, object]:
    for degree in range(10):
        if sp.expand(f_coefficient_formula(S, degree)) != 0:
            raise AssertionError(f"beta^{degree} should vanish")

    low_rows: list[list[object]] = []
    for degree in range(10, 26):
        coefficient = sp.factor(
            f_coefficient_formula(S, degree).subs(S, N + 8)
        )
        divisor = sp.S.One
        if degree == 22:
            divisor = N * (N + 1) * (N + 2) * (N + 3) * (N + 4) * (2 * N - 1)
        elif degree == 23:
            divisor = (
                N
                * (N - 1)
                * (N + 1)
                * (N + 2)
                * (N + 3)
                * (N + 4)
                * (2 * N - 1)
            )
        elif degree == 24:
            divisor = (
                N
                * (N - 1)
                * (N + 1)
                * (N + 2)
                * (N + 3)
                * (N + 4)
                * (2 * N - 3)
                * (2 * N - 1)
            )
        elif degree == 25:
            divisor = (
                N
                * (N - 2)
                * (N - 1)
                * (N + 1)
                * (N + 2)
                * (N + 3)
                * (N + 4)
                * (2 * N - 3)
                * (2 * N - 1)
            )
        quotient = sp.cancel(coefficient / divisor)
        if not coefficients_nonnegative(quotient, N):
            raise AssertionError(f"low beta^{degree} certificate failed")
        low_rows.append([degree, str(coefficient)])

    lam = 1 + S * BETA
    lam_next = 1 + (S + 1) * BETA
    u6 = 1 + 6 * BETA
    u7 = 1 + 7 * BETA
    k6 = sum(
        coefficient * BETA**degree
        for degree, coefficient in enumerate(k6_coefficients(S))
    )
    k6_next = k6.subs(S, S + 1)
    k7 = sum(
        coefficient * BETA**degree
        for degree, coefficient in enumerate(k7_coefficients(S))
    )
    delta = sp.expand(k7.subs(S, S + 1) - k7)
    for coefficient in sp.Poly(delta, BETA).all_coeffs():
        if not coefficients_nonnegative(coefficient, S):
            raise AssertionError("Delta K7 coefficientwise monotonicity failed")
    h = sp.expand(
        u7**2 * lam**2 * k6 - u6**2 * lam_next**2 * k6_next
    )
    exponent = 2 * S - 14
    p0 = sp.expand(delta + 5 * h)
    initial = sp.expand(
        u6**2 * p0
        + exponent * BETA * u6 * delta
        + exponent * (exponent - 1) * BETA**2 * delta / 2
    )
    initial_poly = sp.Poly(
        sp.expand(initial.subs(S, N + 26) / BETA**2),
        BETA,
    )
    initial_rows: list[list[object]] = []
    for (degree,), coefficient in reversed(initial_poly.terms()):
        if not coefficients_nonnegative(coefficient, N):
            raise AssertionError("merged B7 three-layer certificate failed")
        initial_rows.append([degree, str(sp.factor(coefficient))])

    u26 = sp.factor(
        (
            g_coefficient_formula(S + 1, 26)
            - g_coefficient_formula(S, 26)
        ).subs(S, N + 26)
    )
    u27 = sp.factor(
        (
            g_coefficient_formula(S + 1, 27)
            - g_coefficient_formula(S, 27)
            - 14 * g_coefficient_formula(S, 26)
        ).subs(S, N + 26)
    )
    if not coefficients_nonnegative(u26, N):
        raise AssertionError("beta^26 boundary failed")
    if not coefficients_nonnegative(u27, N):
        raise AssertionError("beta^27 boundary failed")

    base_tail = [
        [degree, str(int(g_coefficient_formula(sp.Integer(26), degree)))]
        for degree in range(26, 57)
    ]
    if any(int(row[1]) <= 0 for row in base_tail):
        raise AssertionError("G26 tail base failed")

    early: list[list[object]] = []
    for s in range(8, 26):
        values = [
            int(g_coefficient_formula(sp.Integer(s), degree))
            for degree in range(26, 2 * s + 5)
        ]
        if any(value < 0 for value in values):
            raise AssertionError(f"early B7 tail failed at s={s}")
        early.append([s, len(values), str(min(values)) if values else "empty"])

    for s in range(8, 15):
        direct = b7_bracket_coefficients(s)
        reconstructed = [
            int(f_coefficient_formula(sp.Integer(s), degree))
            for degree in range(len(direct))
        ]
        if direct != reconstructed:
            raise AssertionError(f"six-term formula mismatch at s={s}")

    payload = json.dumps(
        [low_rows, initial_rows, str(u26), str(u27), base_tail, early],
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "schema": "amra.complete_split.b7_uniform_positivity.v1",
        "theorem": (
            "For every integer s>=8, the B7 bracket is coefficientwise "
            "nonnegative; with the s=7 boundary, B7 is coefficientwise "
            "nonnegative for every admissible s."
        ),
        "proof_split": (
            "The last four terms equal 6*B5_bracket+8*B4_bracket"
            "+3*B3_bracket+4*C. Thus only G=A-5B needs a tail proof. "
            "Degrees 10..25 of F have positive n=s-8 factorizations; "
            "the degree>=26 tail of G has a positive truncated recurrence."
        ),
        "low_degree_F_coefficients_in_n_s_minus_8": low_rows,
        "tail_recurrence": (
            "For Q=G_(s+1)-u7^2G_s, Delta=K7_(s+1)-K7_s, "
            "H=u7^2 lambda_s^2 K6_s-u6^2 lambda_(s+1)^2 K6_(s+1), "
            "M=2s-14. For s>=26, merge r=0,1,2; all later layers "
            "are positive Delta layers."
        ),
        "merged_three_layer_I_over_beta2_coefficients": initial_rows,
        "truncated_tail_boundary_beta26": str(u26),
        "truncated_tail_boundary_beta27": str(u27),
        "tail_base_G26_degree_coefficient": base_tail,
        "finite_early_tail_s_count_minimum": early,
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
