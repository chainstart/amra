#!/usr/bin/env python3
"""Exact q=7 extension of the base-four Newton census.

This is a finite theorem/counterexample probe, not a proof for arbitrary
deficit.  It imports the independently frozen q=6 endpoint table and its
exact hyperforest recurrence, constructs the 27 new rank-nine endpoints
from an Abel degree bound plus one unused check point, then evaluates all
15 normalized q=7 layers and all 225 base-four Newton coefficients.
"""

from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path

import sympy as sp


OLD_DIR = (
    Path(__file__).resolve().parents[2]
    / "q1_three_hour_campaign_2026-07-31"
    / "opg1757"
)
sys.path.insert(0, str(OLD_DIR))
try:
    import verify_seventh_q6 as q6  # type: ignore
finally:
    sys.path.pop(0)


S = q6.S
DEFICIT = 7
SAMPLE_START = 12


def build_q7_endpoints() -> tuple[dict[tuple[int, int, int], sp.Expr], int]:
    table = dict(q6.Q6_ENDPOINT_POLYNOMIALS)
    independent_checks = 0
    boundary_rank = DEFICIT + 2
    for excess in range(boundary_rank):
        components = boundary_rank - excess
        degree_bound = q6.cleared_component_degree_bound(excess, components)
        for marking in range(3):
            points = []
            for sample_s in range(
                SAMPLE_START, SAMPLE_START + degree_bound + 1
            ):
                cleared_value = (
                    sp.Rational(
                        q6.fast_normalized_component_value(
                            sample_s,
                            marking,
                            excess,
                            components,
                        )
                    )
                    * sample_s**excess
                )
                points.append((sample_s, cleared_value))
            cleared = sp.interpolate(points, S)
            if sp.degree(cleared, S) > degree_bound:
                raise AssertionError("q=7 endpoint exceeded degree bound")
            endpoint = sp.factor(sp.cancel(cleared / S**excess))

            # One exact point not used for interpolation.
            check_s = SAMPLE_START + degree_bound + 1
            measured = sp.Rational(
                q6.fast_normalized_component_value(
                    check_s,
                    marking,
                    excess,
                    components,
                )
            )
            if sp.cancel(endpoint.subs(S, check_s) - measured) != 0:
                raise AssertionError(
                    "q=7 independent endpoint point failed at "
                    f"{(marking, excess, components)}"
                )
            independent_checks += 1
            table[(marking, excess, components)] = endpoint

    expected = {
        (marking, excess, components)
        for marking in range(3)
        for excess in range(boundary_rank)
        for components in range(1, boundary_rank + 1 - excess)
    }
    if set(table) != expected:
        raise AssertionError("q=7 endpoint table is incomplete")
    return table, independent_checks


ENDPOINTS, ENDPOINT_CHECKS = build_q7_endpoints()


@lru_cache(maxsize=None)
def normalized_layer(offset: int) -> sp.Expr:
    if not 0 <= offset <= 2 * DEFICIT:
        raise ValueError("q=7 offset must lie in 0..14")
    total = sp.Integer(0)
    for overlap in range(offset // 2 + 1):
        remaining = offset - 2 * overlap
        lambda_exponent = DEFICIT + 1 - overlap
        for left_excess in range(remaining + 1):
            for right_excess in range(remaining - left_excess + 1):
                lambda_degree = (
                    remaining - left_excess - right_excess
                )
                if lambda_degree > lambda_exponent:
                    continue
                prefactor = sp.Rational(
                    math.comb(lambda_exponent, lambda_degree),
                    math.factorial(overlap),
                )
                component_sum = (
                    DEFICIT
                    + 3
                    - overlap
                    - left_excess
                    - right_excess
                )
                for left_components in range(1, component_sum):
                    right_components = component_sum - left_components
                    positive_left = (1, left_excess, left_components)
                    positive_right = (1, right_excess, right_components)
                    negative_left = (0, left_excess, left_components)
                    negative_right = (2, right_excess, right_components)

                    positive = (
                        4
                        * q6.falling(
                            S - 1 - left_components - left_excess,
                            overlap,
                        )
                        * q6.falling(
                            S - 1 - right_components - right_excess,
                            overlap,
                        )
                        * ENDPOINTS[positive_left]
                        * ENDPOINTS[positive_right]
                    )
                    negative = (
                        4
                        * q6.falling(
                            S - left_components - left_excess,
                            overlap,
                        )
                        * q6.falling(
                            S - 2 - right_components - right_excess,
                            overlap,
                        )
                        * ENDPOINTS[negative_left]
                        * ENDPOINTS[negative_right]
                    )
                    total += prefactor * (positive - negative)
    result = sp.cancel(total)
    numerator, denominator = sp.fraction(result)
    if sp.degree(denominator, S) > 0:
        raise AssertionError(f"q=7 layer {offset} retained a denominator")
    polynomial = sp.Poly(sp.expand(numerator / denominator), S)
    if polynomial.degree() != 2 * DEFICIT:
        raise AssertionError(f"q=7 layer {offset} has wrong degree")
    return sp.factor(polynomial.as_expr())


def forward_coefficients(expression: sp.Expr, base: int = 4) -> list[sp.Expr]:
    polynomial = sp.Poly(expression, S)
    level = [
        polynomial.eval(base + offset)
        for offset in range(polynomial.degree() + 1)
    ]
    answer: list[sp.Expr] = []
    while level:
        answer.append(sp.cancel(level[0]))
        level = [
            level[index + 1] - level[index]
            for index in range(len(level) - 1)
        ]
    return answer


def symbol_coefficients() -> list[int]:
    coefficients = [1]
    for _ in range(DEFICIT):
        following = [0] * (len(coefficients) + 2)
        for degree, value in enumerate(coefficients):
            following[degree] += value
            following[degree + 1] += 2 * value
            following[degree + 2] += 2 * value
        coefficients = following
    return coefficients


def audit() -> dict[str, object]:
    symbol = symbol_coefficients()
    positive = zero = negative = 0
    first_active = DEFICIT // 2
    smallest: tuple[sp.Expr, int, int] | None = None
    for offset in range(2 * DEFICIT + 1):
        expression = normalized_layer(offset)
        polynomial = sp.Poly(expression, S)
        expected_leading = sp.Rational(
            4 * symbol[offset], math.factorial(DEFICIT)
        )
        if polynomial.LC() != expected_leading:
            raise AssertionError(f"q=7 leading symbol failed at {offset}")
        coefficients = forward_coefficients(expression)
        for order, coefficient in enumerate(coefficients):
            if coefficient > 0:
                positive += 1
                if smallest is None or coefficient < smallest[0]:
                    smallest = (coefficient, offset, order)
            elif coefficient == 0:
                zero += 1
            else:
                negative += 1
            if order < first_active and coefficient != 0:
                raise AssertionError(
                    f"q=7 boundary zero failed at {(offset, order)}"
                )
            if order >= first_active and coefficient <= 0:
                raise AssertionError(
                    "q=7 active Newton counterexample at "
                    f"{(offset, order, coefficient)}"
                )
    return {
        "endpoint_formulas": len(ENDPOINTS),
        "new_endpoint_check_points": ENDPOINT_CHECKS,
        "normalized_layers": 2 * DEFICIT + 1,
        "newton_positive_zero_negative": (positive, zero, negative),
        "smallest_positive_value_offset_order": smallest,
        "status": "FINITE_Q7_THEOREM_ONLY",
    }


if __name__ == "__main__":
    result = audit()
    print("OPG q=7 FULL NEWTON PROBE: PASS")
    for name, value in result.items():
        print(f"{name}: {value}")
