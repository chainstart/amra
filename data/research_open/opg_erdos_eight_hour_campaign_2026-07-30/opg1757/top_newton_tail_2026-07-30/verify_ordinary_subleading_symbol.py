#!/usr/bin/env python3
"""Exact finite audit of the ordinary subleading symbol."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction

import sympy as sp

from independent_verify_top_nine import normalized_profile


K, J, X, T, Z = sp.symbols("k j x t z")


def profile_polynomial(profile_index: int, loss: int) -> sp.Poly:
    values = [
        (
            edge_count,
            normalized_profile(
                profile_index, edge_count, loss
            )[loss],
        )
        for edge_count in range(loss + 2)
    ]
    polynomial = sp.Poly(
        sp.interpolate(values[: loss + 1], J), J
    )
    if polynomial.eval(loss + 1) != values[-1][1]:
        raise AssertionError("redundant profile interpolation failed")
    return polynomial


def source_series(maximum_loss: int = 14):
    sequences = {
        profile_index: {rank: [] for rank in range(4)}
        for profile_index in range(3)
    }
    for profile_index in range(3):
        for loss in range(maximum_loss + 1):
            polynomial = profile_polynomial(profile_index, loss)
            for rank in range(4):
                sequences[profile_index][rank].append(
                    polynomial.coeff_monomial(
                        J ** (loss - rank)
                    )
                    if loss >= rank
                    else 0
                )
    return sequences


def claimed_functions():
    w = 1 - 2 * Z
    a = sp.sqrt(w)
    p = [
        -Z * (4 * Z**2 - 3) / (6 * w ** sp.Rational(5, 2)),
        -Z
        * (52 * Z**2 - 48 * Z + 9)
        / (6 * w ** sp.Rational(5, 2)),
        -Z
        * (100 * Z**2 - 96 * Z + 21)
        / (6 * w ** sp.Rational(5, 2)),
    ]
    q = [
        Z
        * (16 * Z**5 - 24 * Z**3 + 153 * Z - 144)
        / (72 * w ** sp.Rational(11, 2)),
        Z**2
        * (
            5008 * Z**4
            - 11904 * Z**3
            + 10152 * Z**2
            - 3168 * Z
            + 81
        )
        / (72 * w ** sp.Rational(11, 2)),
        Z
        * (
            5392 * Z**5
            - 14592 * Z**4
            + 13416 * Z**3
            - 4032 * Z**2
            - 279 * Z
            + 144
        )
        / (72 * w ** sp.Rational(11, 2)),
    ]
    s = [
        Z
        * (
            8896 * Z**8
            - 41472 * Z**7
            + 83664 * Z**6
            - 79488 * Z**5
            + 11556 * Z**4
            + 116640 * Z**3
            - 183465 * Z**2
            + 3240 * Z
            + 80460
        )
        / (6480 * w ** sp.Rational(17, 2)),
        -Z
        * (
            3596864 * Z**8
            - 13932288 * Z**7
            + 22711536 * Z**6
            - 19498752 * Z**5
            + 8751564 * Z**4
            - 2032560 * Z**3
            + 884925 * Z**2
            - 502200 * Z
            + 36180
        )
        / (6480 * w ** sp.Rational(17, 2)),
        Z
        * (
            32886976 * Z**8
            - 111992832 * Z**7
            + 157083984 * Z**6
            - 116581248 * Z**5
            + 49790916 * Z**4
            - 12121920 * Z**3
            + 474255 * Z**2
            + 793800 * Z
            - 126900
        )
        / (6480 * w ** sp.Rational(17, 2)),
    ]
    return a, p, q, s


def ordinary_coefficient(page_count: int, depth: int) -> Fraction:
    total_loss = depth + 4
    numerator = 0
    for left in range(page_count + 1):
        right = page_count - left
        kernel = 0
        for loss in range(total_loss + 1):
            other = total_loss - loss
            kernel += (
                normalized_profile(1, left, total_loss)[loss]
                * normalized_profile(1, right, total_loss)[other]
                - normalized_profile(0, left, total_loss)[loss]
                * normalized_profile(2, right, total_loss)[other]
            )
        numerator += math.comb(page_count, left) * kernel
    return Fraction(
        numerator,
        2**page_count * 2 * page_count * (page_count - 1),
    )


def audit(maximum_loss: int = 14, maximum_depth: int = 12):
    sequences = source_series(maximum_loss)
    a, p, q, s = claimed_functions()
    functions = {0: [a, a, a], 1: p, 2: q, 3: s}
    profile_checks = 0
    for rank in range(4):
        for profile_index in range(3):
            series = sp.series(
                functions[rank][profile_index],
                Z,
                0,
                maximum_loss - rank + 1,
            ).removeO()
            for loss in range(rank, maximum_loss + 1):
                actual = sequences[profile_index][rank][loss]
                expected = sp.expand(series).coeff(
                    Z, loss - rank
                )
                if actual != expected:
                    raise AssertionError("profile symbol mismatch")
                profile_checks += 1

    u = T * X
    v = T * (1 - X)
    sub = lambda expression, value: expression.subs(Z, value)
    g2 = T**2 * (
        (sub(q[1], u) - sub(q[0], u)) * sub(a, v)
        + sub(a, u) * (sub(q[1], v) - sub(q[2], v))
        + sub(p[1], u) * sub(p[1], v)
        - sub(p[0], u) * sub(p[2], v)
    )
    g3 = T**3 * (
        (sub(s[1], u) - sub(s[0], u)) * sub(a, v)
        + sub(a, u) * (sub(s[1], v) - sub(s[2], v))
        + sub(p[1], u) * sub(q[1], v)
        + sub(q[1], u) * sub(p[1], v)
        - sub(p[0], u) * sub(q[2], v)
        - sub(q[0], u) * sub(p[2], v)
    )
    h2 = sp.factor(g2.subs(X, sp.Rational(1, 2)))
    h3 = sp.factor(
        g3.subs(X, sp.Rational(1, 2))
        + sp.diff(g2, X, 2).subs(X, sp.Rational(1, 2)) / 8
    )
    if sp.simplify(h2 - 2 * T**4 / (1 - T)) != 0:
        raise AssertionError("H2 simplification failed")
    expected_h3 = (
        -T**4
        * (
            43 * T**4
            - 129 * T**3
            + 108 * T**2
            - 6 * T
            + 6
        )
        / (3 * (1 - T) ** 4)
    )
    if sp.simplify(h3 - expected_h3) != 0:
        raise AssertionError("H3 simplification failed")

    polynomial_checks = 0
    rows = []
    for depth in range(1, maximum_depth + 1):
        start = max(2, (depth + 5) // 2)
        points = []
        for page_count in range(start, start + depth + 3):
            value = ordinary_coefficient(page_count, depth)
            points.append(
                (
                    page_count,
                    sp.Rational(value.numerator, value.denominator),
                )
            )
        polynomial = sp.Poly(
            sp.interpolate(points[: depth + 1], K), K
        )
        if not all(
            polynomial.eval(page_count) == value
            for page_count, value in points[depth + 1 :]
        ):
            raise AssertionError("ordinary polynomial spare check failed")
        actual = polynomial.coeff_monomial(K ** (depth - 1))
        expected = -sp.Rational(
            22 * depth**3
            + 147 * depth**2
            + 161 * depth
            - 258,
            36,
        )
        if actual != expected:
            raise AssertionError("subleading coefficient mismatch")
        polynomial_checks += 1
        rows.append(
            {
                "depth": depth,
                "subleading": str(actual),
                "spare_checks": 2,
            }
        )

    return {
        "schema": "amra.opg1757.ordinary-subleading-symbol.v1",
        "scope": (
            "Exact source-profile extraction through the requested loss, "
            "formal H2/H3 simplification, and redundant ordinary-polynomial "
            "checks. The all-orders claim is the coefficientwise proof."
        ),
        "maximum_loss": maximum_loss,
        "profile_checks": profile_checks,
        "maximum_depth": maximum_depth,
        "ordinary_polynomial_checks": polynomial_checks,
        "H2": str(h2),
        "H3": str(h3),
        "rows": rows,
        "status": "finite_checks_passed",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-loss", type=int, default=14)
    parser.add_argument("--maximum-depth", type=int, default=12)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_loss, args.maximum_depth),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
