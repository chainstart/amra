#!/usr/bin/env python3
"""Symbolic and exact verifier for the third active Newton layer."""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import sympy as sp


N = sp.symbols("n", integer=True, positive=True)


def falling(value: sp.Expr, length: int) -> sp.Expr:
    return sp.prod(value - index for index in range(length))


@lru_cache(maxsize=None)
def w0(components: int) -> sp.Expr:
    """Lagrange-inversion form of the Liu--Chow count."""

    return sp.factor(
        sum(
            sp.Rational((-1) ** r, 2**r)
            * (components + r)
            * falling(N - 1, components + r - 1)
            * N ** (N - components - r - 1)
            / (
                math.factorial(r)
                * math.factorial(components - r - 1)
            )
            for r in range(components)
        )
    )


@lru_cache(maxsize=None)
def adjacent(components: int) -> sp.Expr:
    """Count after contracting a prescribed adjacent pair to weight three."""

    return sp.factor(
        sum(
            sp.Rational((-1) ** r, 2**r)
            * (components + r + 2)
            * falling(N - 3, components + r - 1)
            * N ** (N - components - r - 3)
            / (
                math.factorial(r)
                * math.factorial(components - r - 1)
            )
            for r in range(components)
        )
    )


@lru_cache(maxsize=None)
def w1(components: int) -> sp.Expr:
    return sp.factor(
        2 * (N - components) * w0(components) / (N * (N - 1))
    )


@lru_cache(maxsize=None)
def w2(components: int) -> sp.Expr:
    adjacent_orbits = N * (N - 1) * (N - 2) / 2
    disjoint_orbits = N * (N - 1) * (N - 2) * (N - 3) / 8
    forest_edge_pairs = (N - components) * (N - components - 1) / 2
    return sp.factor(
        (
            forest_edge_pairs * w0(components)
            - adjacent_orbits * adjacent(components)
        )
        / disjoint_orbits
    )


def component_determinant(total_components: int) -> sp.Expr:
    return sp.factor(
        sum(
            w1(left) * w1(total_components - left)
            - w0(left) * w2(total_components - left)
            for left in range(1, total_components)
        )
    )


def p5(value: int | sp.Expr) -> int | sp.Expr:
    return value**3 + 12 * value**2 + 20 * value - 225


def q6(value: int | sp.Expr) -> int | sp.Expr:
    return (
        value**5
        + 16 * value**4
        + 52 * value**3
        - 587 * value**2
        - 3063 * value
        + 12240
    )


def p7(value: int | sp.Expr) -> int | sp.Expr:
    return (
        value**6
        + 25 * value**5
        + 229 * value**4
        + 211 * value**3
        - 10101 * value**2
        - 36081 * value
        + 183330
    )


def p8(value: int | sp.Expr) -> int | sp.Expr:
    return (
        value**8
        + 29 * value**7
        + 321 * value**6
        + 459 * value**5
        - 23239 * value**4
        - 161291 * value**3
        + 565356 * value**2
        + 5972364 * value
        - 18174240
    )


def expected_c7() -> sp.Expr:
    return (N - 4) * (N - 5) * p7(N) * N ** (2 * N - 16) / 6


def expected_c8() -> sp.Expr:
    return (N - 4) * (N - 5) * p8(N) * N ** (2 * N - 18) / 30


def rational_power(base: int, exponent: int) -> Fraction:
    if exponent >= 0:
        return Fraction(base**exponent)
    return Fraction(1, base ** (-exponent))


def third_coefficient(k: int) -> Fraction:
    if k < 3:
        raise ValueError("the third active layer starts at k=3")
    if k % 2:
        n = (k + 9) // 2
        bracket = (
            Fraction(p7(n), 6) * rational_power(n, 2 * n - 16)
            - 2
            * p5(n - 1)
            * rational_power(n - 1, 2 * n - 14)
            + 2 * rational_power(n - 2, 2 * n - 12)
        )
    else:
        n = (k + 10) // 2
        bracket = (
            Fraction(p8(n), 30) * rational_power(n, 2 * n - 18)
            - Fraction(2 * q6(n - 1), 3)
            * rational_power(n - 1, 2 * n - 16)
            + 2
            * (n * n - 28)
            * rational_power(n - 2, 2 * n - 14)
        )
    return (
        Fraction(math.factorial(k - 2), 2)
        * (n - 4)
        * (n - 5)
        * bracket
    )


def small_complete_graph_checks() -> dict[int, dict[str, object]]:
    """Reuse the prior edge-subset enumerator, not the source verifier."""

    audit_directory = (
        Path(__file__).resolve().parents[1]
        / "independent_newton_audit_2026-07-30"
    )
    sys.path.insert(0, str(audit_directory))
    from independent_verify_newton import direct_c, forward_difference

    result = {}
    for k in (3, 4):
        q0 = (k - 2) // 2
        values = [direct_c(4 + offset, k) for offset in range(q0 + 3)]
        third = forward_difference(values)
        assert third == third_coefficient(k)
        result[k] = {
            "c_values": [int(value) for value in values],
            "third_coefficient": int(third),
        }
    return result


def symbolic_audit() -> dict[str, object]:
    c7 = component_determinant(7)
    c8 = component_determinant(8)
    assert sp.simplify(c7 - expected_c7()) == 0
    assert sp.simplify(c8 - expected_c8()) == 0

    odd_gap = sp.expand(p7(N) - 12 * p5(N - 1) * (N - 1) ** 2)
    even_gap = sp.expand(p8(N) - 20 * q6(N - 1) * (N - 1) ** 2)
    shifted_odd = sp.Poly(sp.expand(odd_gap.subs(N, N + 8)), N)
    shifted_even = sp.Poly(sp.expand(even_gap.subs(N, N + 9)), N)
    assert all(coefficient > 0 for coefficient in shifted_odd.all_coeffs())
    assert all(coefficient > 0 for coefficient in shifted_even.all_coeffs())

    values = {k: third_coefficient(k) for k in range(3, 101)}
    assert all(value.denominator == 1 and value > 0 for value in values.values())

    return {
        "schema": "amra.opg1757.third-active-newton.v1",
        "symbolic_layers": [7, 8],
        "odd_shifted_gap_coefficients": [
            int(value) for value in shifted_odd.all_coeffs()
        ],
        "even_shifted_gap_coefficients": [
            int(value) for value in shifted_even.all_coeffs()
        ],
        "small_complete_graph_checks": small_complete_graph_checks(),
        "finite_regression": {
            "k_min": 3,
            "k_max": 100,
            "all_integral_and_positive": True,
            "first_values": {
                k: int(values[k]) for k in range(3, 9)
            },
        },
    }


if __name__ == "__main__":
    print(json.dumps(symbolic_audit(), indent=2, sort_keys=True))
