#!/usr/bin/env python3
"""Independent exact audit of Newton top depths six, seven, and eight.

No existing OPG verifier, recorded profile symbol, or fitted top-tail
coefficient is imported.  The computation starts from the normalized
finite Lagrange sums, forms the determinant, and performs the
monomial-to-base-four-Newton conversion with exact integer arithmetic.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


K, X = sp.symbols("k x", integer=True)
MAXIMUM_DEPTH = 8
MAXIMUM_LOSS = MAXIMUM_DEPTH + 4


def truncated_convolution(
    left: tuple[int, ...],
    right: tuple[int, ...],
    maximum_loss: int,
) -> tuple[int, ...]:
    result = [0] * (maximum_loss + 1)
    for left_loss, left_value in enumerate(left):
        for right_loss, right_value in enumerate(right):
            if left_loss + right_loss <= maximum_loss:
                result[left_loss + right_loss] += (
                    left_value * right_value
                )
    return tuple(result)


@lru_cache(maxsize=None)
def normalized_falling(
    shift: int,
    length: int,
    maximum_loss: int = MAXIMUM_LOSS,
) -> tuple[int, ...]:
    """Coefficients of s^-u in (s-shift)_length/s^length."""
    result = [1] + [0] * maximum_loss
    for offset in range(length):
        root = shift + offset
        for loss in range(maximum_loss, 0, -1):
            result[loss] -= root * result[loss - 1]
    return tuple(result)


@lru_cache(maxsize=None)
def normalized_lagrange_e(
    beta: int,
    edge_count: int,
    maximum_loss: int = MAXIMUM_LOSS,
) -> tuple[int, ...]:
    """Top-loss coefficients of 2^r r! E(s,s-beta-r,r)/s^r."""
    if edge_count < 0:
        return tuple([0] * (maximum_loss + 1))

    result = [0] * (maximum_loss + 1)
    for index in range(edge_count + 1):
        product = normalized_falling(
            beta + edge_count,
            index,
            maximum_loss,
        )
        weight = (
            math.comb(edge_count, index)
            * 2 ** (edge_count - index)
            * (-1) ** index
        )
        for loss in range(maximum_loss + 1):
            result[loss] += weight * product[loss]
    return tuple(result)


@lru_cache(maxsize=None)
def normalized_profile(
    profile_index: int,
    edge_count: int,
    maximum_loss: int = MAXIMUM_LOSS,
) -> tuple[int, ...]:
    """Return R_(loss,h)(edge_count) directly from the Lagrange profile."""
    if profile_index not in (0, 1, 2):
        raise ValueError(profile_index)

    shift = (0, 2, 4)[profile_index]
    e_current = normalized_lagrange_e(
        shift,
        edge_count,
        maximum_loss,
    )
    e_previous = normalized_lagrange_e(
        shift + 1,
        edge_count - 1,
        maximum_loss,
    )

    # Exact normalized consecutive difference:
    # Dhat_(beta,r) = Ehat_(beta,r) - 2r*s^-1 Ehat_(beta+1,r-1).
    d_profile = tuple(
        e_current[loss]
        - (
            2 * edge_count * e_previous[loss - 1]
            if loss >= 1
            else 0
        )
        for loss in range(maximum_loss + 1)
    )
    result = list(
        truncated_convolution(
            normalized_falling(
                shift,
                edge_count,
                maximum_loss,
            ),
            d_profile,
            maximum_loss,
        )
    )

    if profile_index == 2 and edge_count >= 1:
        # Exact exceptional term:
        # 8r*s^-2 Fhat_(4,r-1) Ehat_(4,r-1).
        exceptional = truncated_convolution(
            normalized_falling(
                4,
                edge_count - 1,
                maximum_loss,
            ),
            normalized_lagrange_e(
                4,
                edge_count - 1,
                maximum_loss,
            ),
            maximum_loss,
        )
        for loss in range(2, maximum_loss + 1):
            result[loss] += (
                8 * edge_count * exceptional[loss - 2]
            )
    return tuple(result)


def ordinary_top_coefficient(page_count: int, depth: int) -> Fraction:
    """Return b_(k,depth) from total profile loss depth+4."""
    total_loss = depth + 4
    numerator = 0
    for left_edges in range(page_count + 1):
        right_edges = page_count - left_edges
        kernel = 0
        for left_loss in range(total_loss + 1):
            right_loss = total_loss - left_loss
            kernel += (
                normalized_profile(1, left_edges)[left_loss]
                * normalized_profile(1, right_edges)[right_loss]
                - normalized_profile(0, left_edges)[left_loss]
                * normalized_profile(2, right_edges)[right_loss]
            )
        numerator += math.comb(page_count, left_edges) * kernel
    return Fraction(
        numerator,
        2 ** page_count * 2 * page_count * (page_count - 1),
    )


@lru_cache(maxsize=None)
def four_stirling(power: int, falling_degree: int) -> int:
    """Coefficient of (s-4)_falling_degree in s^power."""
    if falling_degree < 0 or falling_degree > power:
        return 0
    row = [1]
    for current_power in range(1, power + 1):
        previous = row
        row = [0] * (current_power + 1)
        for index in range(current_power + 1):
            row[index] = (
                (index + 4)
                * (
                    previous[index]
                    if index < len(previous)
                    else 0
                )
                + (previous[index - 1] if index else 0)
            )
    return row[falling_degree]


def newton_top_value(page_count: int, depth: int) -> Fraction:
    """Return p_(k,depth) by exact monomial-to-Newton conversion."""
    total_degree = 2 * page_count - 4
    return sum(
        ordinary_top_coefficient(page_count, ordinary_depth)
        * four_stirling(
            total_degree - ordinary_depth,
            total_degree - depth,
        )
        for ordinary_depth in range(depth + 1)
    )


def active_start(depth: int) -> int:
    """Smallest k for which Newton index 2k-4-depth is nonnegative."""
    return (depth + 5) // 2


def interpolate_depth(
    depth: int,
    spare_points: int = 4,
) -> tuple[sp.Poly, list[tuple[int, int]], list[tuple[int, int]]]:
    """Interpolate at the proven bound 2d and verify spare exact values."""
    start = active_start(depth)
    fitting_count = 2 * depth + 1
    values = []
    for page_count in range(
        start,
        start + fitting_count + spare_points,
    ):
        value = newton_top_value(page_count, depth)
        assert value.denominator == 1
        values.append((page_count, value.numerator))

    fitting_values = values[:fitting_count]
    spare_values = values[fitting_count:]
    polynomial = sp.Poly(
        sp.interpolate(fitting_values, K).expand(),
        K,
    )
    assert polynomial.degree() <= 2 * depth
    for page_count, value in spare_values:
        assert polynomial.eval(page_count) == value
    return polynomial, fitting_values, spare_values


def positivity_certificate(
    depth: int,
    polynomial: sp.Poly,
) -> dict[str, object]:
    """Certify positivity using exact factorization and a positive shift."""
    coefficient, factors = sp.factor_list(polynomial.as_expr())
    nonlinear = [
        factor
        for factor, exponent in factors
        if sp.degree(factor, K) > 1
        for _ in range(exponent)
    ]
    assert len(nonlinear) == 1
    residual = sp.Poly(nonlinear[0], K)

    shift = {6: 6, 7: 7, 8: 8}[depth]
    shifted = sp.Poly(
        sp.expand(residual.as_expr().subs(K, X + shift)),
        X,
    )
    ascending_coefficients = list(
        reversed(shifted.all_coeffs())
    )
    assert all(value > 0 for value in ascending_coefficients)

    start = active_start(depth)
    boundary_value = newton_top_value(start, depth)
    first_positive_value = newton_top_value(start + 1, depth)
    assert boundary_value == 0
    assert first_positive_value > 0

    # For d=8 the positive-coefficient shift begins at k=8, so k=7
    # is the one separate positive active value.
    separately_checked = []
    for page_count in range(start + 1, shift):
        value = newton_top_value(page_count, depth)
        assert value > 0
        separately_checked.append(
            [page_count, value.numerator]
        )

    linear_factors = sorted(
        (
            int(-sp.Poly(factor, K).TC())
            for factor, exponent in factors
            if sp.degree(factor, K) == 1
            for _ in range(exponent)
        )
    )
    assert all(root < shift for root in linear_factors)
    return {
        "active_start": start,
        "boundary_zero": [start, boundary_value.numerator],
        "first_positive": [
            start + 1,
            first_positive_value.numerator,
        ],
        "linear_roots": linear_factors,
        "residual_degree": residual.degree(),
        "residual_shift": shift,
        "residual_shifted_coefficients_ascending": [
            int(value) for value in ascending_coefficients
        ],
        "separately_checked_positive_values": separately_checked,
        "positive_for_all_k_at_least": start + 1,
        "factor_coefficient": str(coefficient),
    }


def audit(spare_points: int = 4) -> dict[str, object]:
    records = {}
    for depth in (6, 7, 8):
        polynomial, fitting_values, spare_values = interpolate_depth(
            depth,
            spare_points,
        )
        expected_leading = sp.Rational(
            2**depth,
            math.factorial(depth),
        )
        assert polynomial.degree() == 2 * depth
        assert polynomial.LC() == expected_leading
        certificate = positivity_certificate(depth, polynomial)
        records[str(depth)] = {
            "degree": polynomial.degree(),
            "degree_bound": 2 * depth,
            "leading_coefficient": str(polynomial.LC()),
            "factorization": str(sp.factor(polynomial.as_expr())),
            "fitting_k_range": [
                fitting_values[0][0],
                fitting_values[-1][0],
            ],
            "fitting_point_count": len(fitting_values),
            "spare_values": [
                [page_count, value]
                for page_count, value in spare_values
            ],
            "positivity": certificate,
        }

    return {
        "schema": "amra.opg1757.independent-top-nine.v1",
        "method": (
            "Exact truncated Lagrange profiles, determinant binomial "
            "average, 4-Stirling conversion, degree-bound interpolation"
        ),
        "imports_existing_opg_verifier": False,
        "maximum_profile_loss": MAXIMUM_LOSS,
        "spare_point_count_per_depth": spare_points,
        "depth_records": records,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
