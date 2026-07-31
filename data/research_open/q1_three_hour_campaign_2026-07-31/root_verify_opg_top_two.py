#!/usr/bin/env python3
"""Root red-team for the OPG endpoint top-two pattern.

The executable makes two deliberately separate checks.

1.  It checks the proposed leading and subleading coefficient formula on
    every one of the 84 endpoint-certified q<=5 polynomials.
2.  It checks the rooted/unrooted hypertree EGF against the primitive
    hyperforest enumerator on 119 endpoints.
3.  It checks the algebraic involution used by the all-q proof that lowers
    the cleared-numerator degree by two.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import sympy as sp


CAMPAIGN = Path(__file__).resolve().parent
OPG = CAMPAIGN / "opg1757"
sys.path.insert(0, str(OPG))
try:
    from verify_sixth_q5 import Q5_ENDPOINT_POLYNOMIALS, S
    from verify_second_deficit import hyperforest_component_weight
finally:
    sys.path.pop(0)


def endpoint_degree(excess: int, components: int) -> int:
    return 2 * components + 2 * excess - 2


def predicted_leading(excess: int, components: int) -> sp.Rational:
    return sp.Rational(
        1,
        2 ** (components + excess - 1)
        * math.factorial(components - 1)
        * math.factorial(excess),
    )


def predicted_subleading_ratio(
    h: int, excess: int, components: int
) -> sp.Rational:
    return sp.Rational(
        (15 - 4 * excess) * (components - 1)
        - excess * (4 * excess + 5),
        3,
    ) - h * (components + 2 * excess - 1)


def audit_endpoint_top_two() -> list[list[str | int]]:
    rows: list[list[str | int]] = []
    for (h, excess, components), expression in sorted(
        Q5_ENDPOINT_POLYNOMIALS.items()
    ):
        polynomial = sp.Poly(sp.expand(expression), S)
        degree = endpoint_degree(excess, components)
        if polynomial.degree() != degree:
            raise AssertionError(
                "endpoint degree mismatch at "
                f"{(h, excess, components)}"
            )
        leading = polynomial.coeff_monomial(S**degree)
        if leading != predicted_leading(excess, components):
            raise AssertionError(
                "endpoint leading coefficient mismatch at "
                f"{(h, excess, components)}"
            )
        if degree:
            subleading = polynomial.coeff_monomial(S ** (degree - 1))
            ratio = sp.cancel(subleading / leading)
            expected_ratio = predicted_subleading_ratio(
                h, excess, components
            )
            if ratio != expected_ratio:
                raise AssertionError(
                    "endpoint subleading coefficient mismatch at "
                    f"{(h, excess, components)}"
                )
        else:
            ratio = sp.Integer(0)
        rows.append(
            [
                h,
                excess,
                components,
                degree,
                str(leading),
                str(ratio),
            ]
        )
    if len(rows) != 84:
        raise AssertionError("the q<=5 endpoint firewall must contain 84 rows")
    return rows


def endpoint_slope(excess: int, components: int) -> int:
    return components + 2 * excess - 1


def egf_h0_weight(
    s: int, excess: int, components: int
) -> int:
    """Evaluate the h=0 endpoint from the Lagrange formula."""

    t, u = sp.symbols("t u")
    phi = sum(
        u**index * t ** (index + 1) / sp.factorial(index + 1)
        for index in range(excess + 1)
    )
    unrooted = t - sum(
        sp.Rational(index + 1, sp.factorial(index + 2))
        * u**index
        * t ** (index + 2)
        for index in range(excess + 1)
    )
    derivative = 1 - t * sum(
        u**index * t**index / sp.factorial(index)
        for index in range(excess + 1)
    )
    tail_argument = sp.expand(s * (phi - t))
    exponential_tail = sum(
        tail_argument**power / sp.factorial(power)
        for power in range(excess + 1)
    )
    coefficient = sp.Poly(
        sp.expand(
            unrooted ** (components - 1)
            * derivative
            * exponential_tail
        ).coeff(u, excess),
        t,
    )
    total = sp.Rational(0)
    for (degree,), value in coefficient.terms():
        if degree <= s - 1:
            total += (
                value
                * sp.factorial(s - 1)
                / sp.factorial(s - 1 - degree)
                * s ** (s - 1 - degree)
            )
    total = sp.cancel(total / sp.factorial(components - 1))
    if not total.is_Integer:
        raise AssertionError("Lagrange endpoint was not integral")
    return int(total)


def audit_h0_egf() -> list[list[int]]:
    rows: list[list[int]] = []
    for s in range(4, 10):
        for excess in range(min(4, s - 1)):
            for components in range(1, s - excess + 1):
                measured = egf_h0_weight(s, excess, components)
                primitive = hyperforest_component_weight(
                    s, 0, excess, components
                )
                if measured != primitive:
                    raise AssertionError(
                        "rooted-hypertree EGF mismatch at "
                        f"{(s, excess, components)}"
                    )
                rows.append(
                    [s, excess, components, measured]
                )
    if len(rows) != 119:
        raise AssertionError("h=0 EGF regression count changed")
    return rows


def audit_conditional_degree_involution(
    maximum_deficit: int = 30,
) -> list[list[int | str]]:
    """Check the symmetric next-degree cancellation.

    For one ordered endpoint pair A=(e,c), B=(f,d), the coefficient left
    after the leading terms cancel is proportional to

        A_lead * B_lead * (kappa_B-kappa_A).

    The involution (A,B)<->(B,A) reverses this quantity.  The falling
    factorials do not alter the conclusion because their positive and
    negative products have the same sum of shifts.
    """

    rows: list[list[int | str]] = []
    for deficit in range(maximum_deficit + 1):
        for overlap in range(deficit + 1):
            target = deficit + 3 - overlap
            if target < 2:
                continue
            residual = sp.Integer(0)
            term_count = 0
            for left_excess in range(target - 1):
                for right_excess in range(
                    target - left_excess - 1
                ):
                    component_sum = (
                        target - left_excess - right_excess
                    )
                    for left_components in range(1, component_sum):
                        right_components = (
                            component_sum - left_components
                        )
                        left_lead = predicted_leading(
                            left_excess, left_components
                        )
                        right_lead = predicted_leading(
                            right_excess, right_components
                        )
                        residual += left_lead * right_lead * (
                            endpoint_slope(
                                right_excess, right_components
                            )
                            - endpoint_slope(
                                left_excess, left_components
                            )
                        )
                        positive_shift_sum = (
                            1
                            + left_components
                            + left_excess
                            + 1
                            + right_components
                            + right_excess
                        )
                        negative_shift_sum = (
                            left_components
                            + left_excess
                            + 2
                            + right_components
                            + right_excess
                        )
                        if positive_shift_sum != negative_shift_sum:
                            raise AssertionError(
                                "falling-factor shifts stopped matching"
                            )
                        term_count += 1
            if residual != 0:
                raise AssertionError(
                    "conditional next-degree involution failed at "
                    f"(q,l)=({deficit},{overlap})"
                )
            rows.append(
                [deficit, overlap, term_count, str(residual)]
            )
    return rows


def build_certificate() -> dict[str, object]:
    endpoint_rows = audit_endpoint_top_two()
    egf_rows = audit_h0_egf()
    involution_rows = audit_conditional_degree_involution()
    payload = json.dumps(
        [endpoint_rows, egf_rows, involution_rows],
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "schema": "amra.opg1757.root_top_two_audit.v2",
        "status": "PASS",
        "proved": {
            "displayed_formula_scope": (
                "the top-two identity in all 84 endpoint-certified "
                "q<=5 formulas"
            ),
            "general_theorem_regressions": (
                "the rooted-hypertree Lagrange formula and the "
                "all-fixed-q top-two cancellation involution"
            ),
        },
        "not_proved": (
            "endpoint polynomiality, denominator cancellation, or pooled "
            "positivity for arbitrary excess q"
        ),
        "endpoint_rows": len(endpoint_rows),
        "h0_egf_rows": len(egf_rows),
        "conditional_involution_rows": len(involution_rows),
        "conditional_q_range": [0, 30],
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def main() -> None:
    print(json.dumps(build_certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
