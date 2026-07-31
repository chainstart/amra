#!/usr/bin/env python3
"""Exact finite probe for the all-deficit base-four Newton conjecture.

This is evidence only.  It imports the independently frozen q=0,...,6
normalized layers and the q=6 endpoint table.  The universal reduction is
recorded in BASE4_NEWTON_GLOBAL_ATTACK.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


OLD_DIR = (
    Path(__file__).resolve().parents[2]
    / "q1_three_hour_campaign_2026-07-31"
    / "opg1757"
)
sys.path.insert(0, str(OLD_DIR))
try:
    import verify_fifth_q4 as q4  # type: ignore
    import verify_fourth_q3 as q3  # type: ignore
    import verify_second_deficit as q2  # type: ignore
    import verify_seventh_q6 as q6  # type: ignore
    import verify_sixth_q5 as q5  # type: ignore
finally:
    sys.path.pop(0)


S = q2.S


def forward_coefficients(expression: sp.Expr, base: int = 4) -> list[sp.Expr]:
    polynomial = sp.Poly(sp.cancel(expression), S)
    level = [
        polynomial.eval(base + offset)
        for offset in range(polynomial.degree() + 1)
    ]
    answer: list[sp.Expr] = []
    for _ in range(polynomial.degree() + 1):
        answer.append(sp.cancel(level[0]))
        level = [
            level[index + 1] - level[index]
            for index in range(len(level) - 1)
        ]
    return answer


def exact_layers() -> dict[int, tuple[sp.Expr, ...]]:
    return {
        0: (sp.Integer(4),),
        1: (
            4 * (S**2 + 4 * S - 24),
            8 * (S**2 - S - 8),
            4 * (S - 2) * (2 * S - 7),
        ),
        2: q2.EXPECTED_NORMALIZED_LAYERS,
        3: q3.EXPECTED_Q3_NORMALIZED_LAYERS,
        4: q4.EXPECTED_Q4_NORMALIZED_LAYERS,
        5: q5.EXPECTED_Q5_NORMALIZED_LAYERS,
        6: q6.EXPECTED_Q6_NORMALIZED_LAYERS,
    }


def audit_layers() -> tuple[int, int, int]:
    positive = zero = negative = 0
    for deficit, layer in exact_layers().items():
        first_active = deficit // 2
        for expression in layer:
            coefficients = forward_coefficients(expression)
            if len(coefficients) != 2 * deficit + 1:
                raise AssertionError("unexpected normalized layer degree")
            for order, coefficient in enumerate(coefficients):
                if coefficient > 0:
                    positive += 1
                elif coefficient == 0:
                    zero += 1
                else:
                    negative += 1
                if (coefficient == 0) != (order < first_active):
                    raise AssertionError(
                        "boundary-factor/Newton-support mismatch at "
                        f"{(deficit, order, coefficient)}"
                    )
    if (positive, zero, negative) != (364, 91, 0):
        raise AssertionError("frozen layer census changed")
    return positive, zero, negative


def falling(shift: int, order: int) -> sp.Expr:
    answer = sp.Integer(1)
    for index in range(order):
        answer *= S - shift - index
    return sp.expand(answer)


def audit_endpoint_active_factors() -> tuple[int, int, int]:
    """Probe (s-h-c-e)_ell Q for every frozen endpoint and ell<=6."""

    positive = zero = negative = 0
    for (marking, excess, components), endpoint in (
        q6.Q6_ENDPOINT_POLYNOMIALS.items()
    ):
        shift = marking + components + excess
        for overlap in range(7):
            active = falling(shift, overlap) * endpoint
            for coefficient in forward_coefficients(active):
                if coefficient > 0:
                    positive += 1
                elif coefficient == 0:
                    zero += 1
                else:
                    negative += 1
    if (positive, zero, negative) != (5695, 4385, 0):
        raise AssertionError("frozen active-endpoint census changed")
    return positive, zero, negative


def audit() -> dict[str, object]:
    return {
        "layer_newton_positive_zero_negative": audit_layers(),
        "active_endpoint_positive_zero_negative": (
            audit_endpoint_active_factors()
        ),
        "status": "FINITE_EVIDENCE_ONLY__GLOBAL_SIGN_CONVOLUTION_OPEN",
    }


if __name__ == "__main__":
    result = audit()
    print("OPG BASE-FOUR NEWTON PROBE: PASS")
    for key, value in result.items():
        print(f"{key}: {value}")
