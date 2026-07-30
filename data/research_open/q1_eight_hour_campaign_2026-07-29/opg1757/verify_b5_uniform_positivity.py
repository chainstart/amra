#!/usr/bin/env python3
"""Symbolic certificate for coefficientwise positivity of the B5 bracket."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

from five_page_union_formula import (
    b5_bracket_coefficients,
    k3_coefficients,
    k4_coefficients,
    k5_coefficients,
)


BETA, S, N = sp.symbols("beta s n", integer=True, nonnegative=True)


def falling_choose(top: sp.Expr, lower: int) -> sp.Expr:
    if lower < 0:
        return sp.S.Zero
    return sp.prod(top - index for index in range(lower)) / sp.factorial(
        lower
    )


def powered_choose(
    top: sp.Expr, lower: int, base: int
) -> sp.Expr:
    if lower < 0:
        return sp.S.Zero
    return base**lower * falling_choose(top, lower)


def f_coefficient_formula(s: sp.Expr, degree: int) -> sp.Expr:
    """The exact four-term binomial formula [beta^degree] F_s."""

    term5 = sum(
        coefficient * powered_choose(2 * s - 12, degree - order, 5)
        for order, coefficient in enumerate(k5_coefficients(s))
    )
    term4 = sum(
        sp.binomial(2, q)
        * s**q
        * sum(
            coefficient
            * powered_choose(
                2 * s - 10,
                degree - q - order,
                4,
            )
            for order, coefficient in enumerate(k4_coefficients(s))
        )
        for q in range(3)
    )
    term3 = sum(
        sp.binomial(4, q)
        * s**q
        * sum(
            coefficient
            * powered_choose(
                2 * s - 8,
                degree - q - order,
                3,
            )
            for order, coefficient in enumerate(k3_coefficients(s))
        )
        for q in range(5)
    )
    term2 = sum(
        sp.binomial(6, q)
        * s**q
        * powered_choose(2 * s - 6, degree - q, 2)
        for q in range(7)
    )
    return sp.expand(term5 - 3 * term4 + 3 * term3 - term2)


def g_coefficient_formula(s: sp.Expr, degree: int) -> sp.Expr:
    """Coefficient of G_s=A_s-3B_s."""

    term5 = sum(
        coefficient * powered_choose(2 * s - 12, degree - order, 5)
        for order, coefficient in enumerate(k5_coefficients(s))
    )
    term4 = sum(
        sp.binomial(2, q)
        * s**q
        * sum(
            coefficient
            * powered_choose(
                2 * s - 10,
                degree - q - order,
                4,
            )
            for order, coefficient in enumerate(k4_coefficients(s))
        )
        for q in range(3)
    )
    return sp.expand(term5 - 3 * term4)


def all_coefficients_nonnegative(expression: sp.Expr, variable: sp.Symbol) -> bool:
    return all(
        coefficient >= 0
        for coefficient in sp.Poly(sp.expand(expression), variable).all_coeffs()
    )


def symbolic_tail_recurrence_data() -> dict[str, object]:
    """Construct the finite positive certificate for the G_s tail."""

    lam = 1 + S * BETA
    lam_next = 1 + (S + 1) * BETA
    u4 = 1 + 4 * BETA
    u5 = 1 + 5 * BETA
    k4 = sum(
        coefficient * BETA**degree
        for degree, coefficient in enumerate(k4_coefficients(S))
    )
    k4_next = k4.subs(S, S + 1)
    k5 = sum(
        coefficient * BETA**degree
        for degree, coefficient in enumerate(k5_coefficients(S))
    )
    k5_next = k5.subs(S, S + 1)
    delta = sp.expand(k5_next - k5)
    shifted_delta = sp.Poly(
        sp.expand(delta.subs(S, N + 8) / BETA**2),
        BETA,
    )
    for coefficient in shifted_delta.all_coeffs():
        if not all_coefficients_nonnegative(coefficient, N):
            raise AssertionError("Delta_s is not coefficientwise positive")
    h = sp.expand(u5**2 * lam**2 * k4 - u4**2 * lam_next**2 * k4_next)
    exponent = 2 * S - 10
    initial = sp.expand(u4 * (delta + 3 * h) + exponent * BETA * delta)
    shifted_initial = sp.Poly(
        sp.expand(initial.subs(S, N + 8) / BETA**2),
        BETA,
    )
    initial_rows: list[list[object]] = []
    for (degree,), coefficient in reversed(shifted_initial.terms()):
        if not all_coefficients_nonnegative(coefficient, N):
            raise AssertionError("the merged G-tail layer is not positive")
        initial_rows.append([degree, str(sp.factor(coefficient))])

    low_rows: list[list[object]] = []
    for degree in range(6):
        if sp.expand(f_coefficient_formula(S, degree)) != 0:
            raise AssertionError(f"coefficient beta^{degree} should vanish")
    for degree in range(6, 14):
        coefficient = sp.factor(
            f_coefficient_formula(S, degree).subs(S, N + 6)
        )
        if not all_coefficients_nonnegative(coefficient, N):
            raise AssertionError(f"low coefficient beta^{degree} is not positive")
        low_rows.append([degree, str(coefficient)])

    u14 = sp.factor(
        (
            g_coefficient_formula(S + 1, 14)
            - g_coefficient_formula(S, 14)
        ).subs(S, N + 8)
    )
    u15 = sp.factor(
        (
            g_coefficient_formula(S + 1, 15)
            - g_coefficient_formula(S, 15)
            - 10 * g_coefficient_formula(S, 14)
        ).subs(S, N + 8)
    )
    if not all_coefficients_nonnegative(u14, N):
        raise AssertionError("the beta^14 tail boundary is not positive")
    if not all_coefficients_nonnegative(u15, N):
        raise AssertionError("the beta^15 tail boundary is not positive")

    base = b5_bracket_coefficients(8)
    # G_8 is reconstructed independently from its two defining terms.
    g8 = [
        int(g_coefficient_formula(sp.Integer(8), degree))
        for degree in range(17)
    ]
    tail_base = [
        [degree, str(coefficient)]
        for degree, coefficient in enumerate(g8)
        if degree >= 14 and coefficient
    ]
    if not tail_base or any(int(row[1]) <= 0 for row in tail_base):
        raise AssertionError("the G_8 tail base is not positive")
    if any(g8[degree] < 0 for degree in range(14, len(g8))):
        raise AssertionError("the G_8 tail changed sign")

    # Regression of the four-term formula against independent convolution.
    for s in range(6, 21):
        direct = b5_bracket_coefficients(s)
        reconstructed = [
            int(f_coefficient_formula(sp.Integer(s), degree))
            for degree in range(len(direct))
        ]
        if direct != reconstructed:
            raise AssertionError(f"four-term coefficient mismatch at s={s}")

    payload = json.dumps(
        [initial_rows, low_rows, str(u14), str(u15), tail_base],
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "schema": "amra.complete_split.b5_uniform_positivity.v1",
        "theorem": (
            "For every integer s>=6, F_s is coefficientwise nonnegative; "
            "therefore B5 is coefficientwise nonnegative for every s."
        ),
        "four_term_coefficient_formula": (
            "[beta^d]F_s is the exact four-term powered-binomial sum "
            "implemented by f_coefficient_formula."
        ),
        "proof_split": (
            "F_s=G_s+lambda^4*(3*u3^(2s-8)*K3"
            "-lambda^2*u2^(2s-6)). The second summand is positive by "
            "the proved B3 bracket. Degrees 6..13 of F_s have positive "
            "n=s-6 expansions. The degree>=14 tail of G_s has the "
            "positive truncated recurrence certified below."
        ),
        "tail_recurrence": (
            "Q_s=G_(s+1)-u5^2*G_s. Put Delta=K5_(s+1)-K5_s and "
            "H=u5^2*lambda_s^2*K4_s-u4^2*lambda_(s+1)^2*K4_(s+1). "
            "For s>=8, Q_s=u4^(2s-11)*I_s+sum_(r=2)^(2s-10) "
            "C(2s-10,r)*beta^r*u4^(2s-10-r)*Delta, where "
            "I_s=u4*(Delta+3H)+(2s-10)*beta*Delta."
        ),
        "merged_initial_I_over_beta2_coefficients": initial_rows,
        "low_degree_F_coefficients_in_n_s_minus_6": low_rows,
        "truncated_tail_boundary_beta14": str(u14),
        "truncated_tail_boundary_beta15": str(u15),
        "tail_base_G8_degree_coefficient": tail_base,
        "sha256_symbolic_payload": hashlib.sha256(payload).hexdigest(),
        "failed_direct_layer_route": (
            "Expanding the original four-term R_s directly about u2 "
            "leaves negative monomials in every tested single layer; "
            "the successful proof instead splits off the already-proved "
            "B3 bracket and truncates G_s below degree 14."
        ),
        "status": "proved",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audit = symbolic_tail_recurrence_data()
    rendered = json.dumps(audit, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
