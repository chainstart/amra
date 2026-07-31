#!/usr/bin/env python3
"""Exact certificate for the all-fixed-deficit leading symbol.

The proof itself is algebraic and is written in
``ALL_FIXED_DEFICIT_EVENTUAL_POSITIVITY_THEOREM.md``.  This program keeps
four independent regression firewalls around the delicate parts:

1. the marked one-block Lagrange expansion;
2. the endpoint-curvature identity on every endpoint in the q=6 table;
3. the four-Poisson/profile generating-function collapse;
4. agreement with every already proved complete layer q=0,...,6.

No q=7 or q=8 interpolation is used.
"""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import sys
import argparse

import sympy as sp


HERE = pathlib.Path(__file__).resolve().parent
OLD = (
    HERE.parents[1]
    / "q1_three_hour_campaign_2026-07-31"
    / "opg1757"
)
sys.path.insert(0, str(OLD))


S, T, V, Z = sp.symbols("s t v z")


def endpoint_leading(excess: int, components: int) -> sp.Rational:
    return sp.Rational(
        1,
        2 ** (components + excess - 1)
        * math.factorial(components - 1)
        * math.factorial(excess),
    )


def endpoint_subleading_zero(excess: int, components: int) -> sp.Rational:
    return sp.Rational(
        (15 - 4 * excess) * (components - 1)
        - excess * (4 * excess + 5),
        3,
    )


def kappa(excess: int, components: int) -> int:
    return components + 2 * excess - 1


def curvature(excess: int, components: int) -> int:
    """Second h-difference of the relative s^{-2} endpoint term."""

    return (
        components**2
        + (4 * excess - 5) * components
        + 4 * excess**2
        - 6 * excess
        + 4
    )


def marked_one_block_symbolic_audit() -> str:
    """Recompute the first two Lagrange terms for one block of weight a."""

    a, c = sp.symbols("a c", positive=True)
    v0 = T - T**2 / 2
    v1 = -V * T**3 / 3

    b0 = a * v0 ** (c - 1) + (c - 1) * v0 ** (c - 2) * (1 - T)
    b1 = a * (
        V * T * v0 ** (c - 1)
        + (c - 1) * v0 ** (c - 2) * v1
    ) + (c - 1) * (
        (c - 2) * v0 ** (c - 3) * v1 * (1 - T)
        - V * T**2 * v0 ** (c - 2)
    )

    exponential0 = sp.exp(V * T**2 / 2)
    exponential1 = exponential0 * V**2 * T**3 / 6
    p0 = exponential0 * b0
    p1 = exponential0 * b1 + exponential1 * b0

    def euler(expression: sp.Expr) -> sp.Expr:
        return T * sp.diff(expression, T)

    functional1 = -sp.Rational(1, 2) * (
        euler(euler(p0)) + (2 * a + 1) * euler(p0)
    )
    measured = sp.simplify((p1 + functional1).subs(T, 1) / a)
    base = 2 ** (1 - c) * sp.exp(V / 2)
    measured_ratio = sp.factor(measured / base)

    unmarked_ratio = -(
        4 * c * V - 30 * c + 2 * V**2 + 5 * V + 30
    ) / 6
    expected_ratio = unmarked_ratio - (a - 1) * (
        a * V + 2 * c - 2
    ) / a
    if sp.simplify(measured_ratio - expected_ratio) != 0:
        raise AssertionError("marked one-block Lagrange expansion failed")
    return str(sp.factor(expected_ratio))


def curvature_table_audit(extended_q6: bool = False) -> int:
    """Check curvature on q=5, optionally on the larger q=6 table."""

    if extended_q6:
        from verify_seventh_q6 import Q6_ENDPOINT_POLYNOMIALS as table

        maximum_excess = 7
        maximum_total = 8
        expected_checks = 36
    else:
        from verify_sixth_q5 import Q5_ENDPOINT_POLYNOMIALS as table

        maximum_excess = 6
        maximum_total = 7
        expected_checks = 28
    from verify_second_deficit import S as OLD_S

    checked = 0
    for excess in range(maximum_excess + 1):
        for components in range(1, maximum_total + 1 - excess):
            degree = 2 * components + 2 * excess - 2
            leading = endpoint_leading(excess, components)
            relative = []
            for h in range(3):
                expression = table[(h, excess, components)]
                numerator = sp.Poly(
                    expression * OLD_S**excess, OLD_S
                )
                target_degree = degree - 2 + excess
                coefficient = (
                    sp.Integer(0)
                    if target_degree < 0
                    else numerator.nth(target_degree)
                )
                relative.append(sp.cancel(coefficient / leading))
            measured = sp.cancel(relative[2] - 2 * relative[1] + relative[0])
            expected = curvature(excess, components)
            if measured != expected:
                raise AssertionError(
                    "endpoint curvature mismatch at "
                    f"{(excess, components)}: {measured} != {expected}"
                )
            checked += 1
    if checked != expected_checks:
        raise AssertionError("endpoint curvature count changed")
    return checked


def direct_profile_leading_polynomial(deficit: int) -> sp.Expr:
    """Evaluate the finite profile sum before its closed-form collapse."""

    answer = sp.Integer(0)
    for overlap in range(deficit + 2):
        total_profile_size = deficit + 1 - overlap
        if total_profile_size < 0:
            continue
        for rho in range(total_profile_size + 1):
            for excess in range(total_profile_size - rho + 1):
                for sigma in range(
                    total_profile_size - rho - excess + 1
                ):
                    right_excess = (
                        total_profile_size - rho - excess - sigma
                    )
                    left_components = rho + 1
                    right_components = sigma + 1
                    left_leading = endpoint_leading(
                        excess, left_components
                    )
                    right_leading = endpoint_leading(
                        right_excess, right_components
                    )
                    left_kappa = kappa(excess, left_components)
                    right_kappa = kappa(
                        right_excess, right_components
                    )
                    kernel = (
                        left_kappa * right_kappa
                        + overlap
                        - sp.Rational(
                            curvature(excess, left_components)
                            + curvature(
                                right_excess, right_components
                            ),
                            2,
                        )
                    )
                    profile_weight = left_leading * right_leading
                    for lambda_degree in range(total_profile_size + 1):
                        offset = (
                            2 * overlap
                            + excess
                            + right_excess
                            + lambda_degree
                        )
                        answer += (
                            sp.Rational(4, math.factorial(overlap))
                            * math.comb(
                                total_profile_size, lambda_degree
                            )
                            * profile_weight
                            * kernel
                            * Z**offset
                        )
    return sp.factor(sp.expand(answer))


def profile_collapse_audit(maximum_deficit: int = 7) -> int:
    checked = 0
    atom = 1 + 2 * Z + 2 * Z**2
    for deficit in range(maximum_deficit + 1):
        measured = direct_profile_leading_polynomial(deficit)
        expected = sp.Rational(4, math.factorial(deficit)) * atom**deficit
        if sp.expand(measured - expected) != 0:
            raise AssertionError(
                f"profile collapse failed at q={deficit}"
            )
        checked += 1
    return checked


def proved_layer_audit(extended_q6: bool = False) -> int:
    """Compare with exact layers q=0,...,5, optionally also q=6."""

    import verify_fifth_q4 as q4
    import verify_fourth_q3 as q3
    import verify_second_deficit as q2
    import verify_sixth_q5 as q5

    old_s = q2.S
    arrays: dict[int, tuple[sp.Expr, ...]] = {
        0: (sp.Integer(4),),
        1: (
            4 * (old_s**2 + 4 * old_s - 24),
            8 * (old_s**2 - old_s - 8),
            4 * (old_s - 2) * (2 * old_s - 7),
        ),
        2: q2.EXPECTED_NORMALIZED_LAYERS,
        3: q3.EXPECTED_Q3_NORMALIZED_LAYERS,
        4: q4.EXPECTED_Q4_NORMALIZED_LAYERS,
        5: q5.EXPECTED_Q5_NORMALIZED_LAYERS,
    }
    if extended_q6:
        import verify_seventh_q6 as q6

        arrays[6] = q6.EXPECTED_Q6_NORMALIZED_LAYERS

    checked = 0
    for deficit, expressions in arrays.items():
        measured = sp.Integer(0)
        for offset, expression in enumerate(expressions):
            rational = sp.cancel(expression)
            numerator, denominator = sp.fraction(rational)
            numerator_poly = sp.Poly(numerator, old_s)
            denominator_poly = sp.Poly(denominator, old_s)
            leading = sp.cancel(
                numerator_poly.LC() / denominator_poly.LC()
            )
            degree = numerator_poly.degree() - denominator_poly.degree()
            if degree != 2 * deficit:
                raise AssertionError(
                    f"unexpected exact-layer degree at {(deficit, offset)}"
                )
            measured += leading * Z**offset
            checked += 1
        expected = sp.Rational(4, math.factorial(deficit)) * (
            1 + 2 * Z + 2 * Z**2
        ) ** deficit
        if sp.expand(measured - expected) != 0:
            raise AssertionError(
                f"proved-layer symbol mismatch at q={deficit}"
            )
    maximum_deficit = 6 if extended_q6 else 5
    if checked != sum(2 * q + 1 for q in range(maximum_deficit + 1)):
        raise AssertionError("proved-layer comparison count changed")
    return checked


def build_certificate(extended_q6: bool = False) -> dict[str, object]:
    marked_formula = marked_one_block_symbolic_audit()
    endpoint_checks = curvature_table_audit(extended_q6)
    profile_checks = profile_collapse_audit()
    layer_checks = proved_layer_audit(extended_q6)
    payload = {
        "schema": "amra.opg1757.fixed-deficit-leading-symbol.v1",
        "status": "PASS",
        "theorem_status": "PROVED",
        "marked_one_block_subleading_ratio": marked_formula,
        "endpoint_curvature_checks": endpoint_checks,
        "profile_collapse_checks": profile_checks,
        "proved_layer_coefficients_checked": layer_checks,
        "extended_q6_regression": extended_q6,
        "leading_symbol": "4/q! * (1 + 2*z + 2*z^2)^q",
        "consequence": (
            "every fixed deficit q is strictly positive on its natural "
            "support for all sufficiently large s"
        ),
        "scope": (
            "complete-split pooled disjoint-core alpha^2 layer only; "
            "no uniform threshold in q and no arbitrary-host claim"
        ),
    }
    digest_payload = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    payload["sha256"] = hashlib.sha256(digest_payload).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--extended-q6",
        action="store_true",
        help="also import and audit the slower full q=6 endpoint table",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            build_certificate(extended_q6=args.extended_q6),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
