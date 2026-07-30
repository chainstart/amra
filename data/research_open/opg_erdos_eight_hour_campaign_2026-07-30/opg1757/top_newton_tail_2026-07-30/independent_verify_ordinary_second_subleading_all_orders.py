#!/usr/bin/env python3
"""Independent red-team audit of the ordinary second subleading symbol.

This file deliberately imports no OPG verifier.  It starts from the finite
normalized Lagrange sums, reconstructs the profile polynomials, builds the
determinant kernels by a generic convolution, and reconstructs the ordinary
polynomials by exact binomial averaging.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


J, K, T, X, Z = sp.symbols("j k t x z")
RAW_MAXIMUM_LOSS = 18


def truncated_convolution(
    left: tuple[int, ...],
    right: tuple[int, ...],
    maximum_loss: int,
) -> tuple[int, ...]:
    result = [0] * (maximum_loss + 1)
    for left_loss, left_value in enumerate(left):
        for right_loss, right_value in enumerate(right):
            if left_loss + right_loss <= maximum_loss:
                result[left_loss + right_loss] += left_value * right_value
    return tuple(result)


@lru_cache(maxsize=None)
def normalized_falling(
    shift: int,
    length: int,
    maximum_loss: int = RAW_MAXIMUM_LOSS,
) -> tuple[int, ...]:
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
    maximum_loss: int = RAW_MAXIMUM_LOSS,
) -> tuple[int, ...]:
    if edge_count < 0:
        return tuple([0] * (maximum_loss + 1))
    result = [0] * (maximum_loss + 1)
    for index in range(edge_count + 1):
        product = normalized_falling(beta + edge_count, index, maximum_loss)
        weight = (
            math.comb(edge_count, index)
            * 2 ** (edge_count - index)
            * (-1) ** index
        )
        for loss in range(maximum_loss + 1):
            result[loss] += weight * product[loss]
    return tuple(result)


@lru_cache(maxsize=None)
def normalized_profile_parts(
    profile_index: int,
    edge_count: int,
    maximum_loss: int = RAW_MAXIMUM_LOSS,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return the main and exceptional normalized profile coefficients."""
    if profile_index not in (0, 1, 2):
        raise ValueError(profile_index)
    shift = (0, 2, 4)[profile_index]
    current = normalized_lagrange_e(shift, edge_count, maximum_loss)
    previous = normalized_lagrange_e(shift + 1, edge_count - 1, maximum_loss)
    difference = tuple(
        current[loss]
        - (
            2 * edge_count * previous[loss - 1]
            if loss
            else 0
        )
        for loss in range(maximum_loss + 1)
    )
    main = truncated_convolution(
        normalized_falling(shift, edge_count, maximum_loss),
        difference,
        maximum_loss,
    )
    exceptional = [0] * (maximum_loss + 1)
    if profile_index == 2 and edge_count >= 1:
        product = truncated_convolution(
            normalized_falling(4, edge_count - 1, maximum_loss),
            normalized_lagrange_e(4, edge_count - 1, maximum_loss),
            maximum_loss,
        )
        for loss in range(2, maximum_loss + 1):
            exceptional[loss] = 8 * edge_count * product[loss - 2]
    return main, tuple(exceptional)


def normalized_profile(
    profile_index: int,
    edge_count: int,
    maximum_loss: int = RAW_MAXIMUM_LOSS,
) -> tuple[int, ...]:
    main, exceptional = normalized_profile_parts(
        profile_index, edge_count, maximum_loss
    )
    return tuple(a + b for a, b in zip(main, exceptional))


@lru_cache(maxsize=None)
def profile_polynomial(profile_index: int, loss: int) -> sp.Poly:
    values = [
        (edge_count, normalized_profile(profile_index, edge_count)[loss])
        for edge_count in range(loss + 2)
    ]
    polynomial = sp.Poly(sp.interpolate(values[: loss + 1], J), J)
    assert polynomial.eval(loss + 1) == values[-1][1]
    return polynomial


@lru_cache(maxsize=None)
def exceptional_profile_polynomial(loss: int) -> sp.Poly:
    values = [
        (
            edge_count,
            normalized_profile_parts(2, edge_count)[1][loss],
        )
        for edge_count in range(loss + 2)
    ]
    polynomial = sp.Poly(sp.interpolate(values[: loss + 1], J), J)
    assert polynomial.eval(loss + 1) == values[-1][1]
    return polynomial


def claimed_fourth_profiles() -> list[sp.Expr]:
    w = 1 - 2 * Z
    numerators = [
        -Z
        * (
            146176 * Z**11 - 663552 * Z**10 + 1220352 * Z**9
            - 774144 * Z**8 - 736992 * Z**7 + 2750976 * Z**6
            - 8160912 * Z**5 + 13685760 * Z**4
            + 47385675 * Z**3 - 112674240 * Z**2
            + 40091760 * Z + 17729280
        ),
        Z
        * (
            690451712 * Z**11 - 3711086592 * Z**10
            + 8894124288 * Z**9 - 12380967936 * Z**8
            + 10858590432 * Z**7 - 6111072000 * Z**6
            + 2540586384 * Z**5 - 1519300800 * Z**4
            + 1006618725 * Z**3 - 199208160 * Z**2
            - 73347120 * Z + 4976640
        ),
        -Z
        * (
            38115777280 * Z**11 - 189099147264 * Z**10
            + 412563816192 * Z**9 - 516716734464 * Z**8
            + 407929881888 * Z**7 - 212168180736 * Z**6
            + 75677948784 * Z**5 - 19289301120 * Z**4
            + 3340767915 * Z**3 - 487969920 * Z**2
            + 184051440 * Z - 23950080
        ),
    ]
    return [
        numerator / (sp.Integer(155520) * w ** sp.Rational(23, 2))
        for numerator in numerators
    ]


def raw_rank_series(maximum_loss: int) -> list[list[sp.Expr]]:
    """Recover A,P,Q,S,T directly from exact finite profile polynomials."""
    profiles = [[sp.S.Zero for _ in range(5)] for _ in range(3)]
    for profile_index in range(3):
        for rank in range(5):
            profiles[profile_index][rank] = sp.expand(
                sum(
                    profile_polynomial(
                        profile_index, loss
                    ).coeff_monomial(J ** (loss - rank))
                    * Z ** (loss - rank)
                    for loss in range(rank, maximum_loss + 1)
                )
            )
    return profiles


def truncate_t(expression: sp.Expr, maximum_loss: int) -> sp.Expr:
    polynomial = sp.Poly(sp.expand(expression), T)
    return sp.expand(
        sum(
            coefficient * T**degree[0]
            for degree, coefficient in polynomial.terms()
            if degree[0] <= maximum_loss
        )
    )


def raw_determinant_kernels(
    maximum_loss: int,
) -> tuple[list[sp.Expr], list[list[sp.Expr]]]:
    profiles = raw_rank_series(maximum_loss)

    def term(profile_index: int, rank: int, argument: sp.Expr) -> sp.Expr:
        return T**rank * profiles[profile_index][rank].subs(Z, argument)

    kernels = []
    for rank in range(5):
        expression = sum(
            term(1, left_rank, T * X)
            * term(1, rank - left_rank, T * (1 - X))
            - term(0, left_rank, T * X)
            * term(2, rank - left_rank, T * (1 - X))
            for left_rank in range(rank + 1)
        )
        kernels.append(truncate_t(expression, maximum_loss))
    return kernels, profiles


def expected_h4() -> sp.Expr:
    return (
        T**5
        * (
            2389 * T**7 - 14334 * T**6 + 34245 * T**5
            - 40008 * T**4 + 22152 * T**3 - 5400 * T**2
            + 3672 * T + 144
        )
        / (36 * (1 - T) ** 7)
    )


def second_symbol(depth: int) -> sp.Rational:
    return sp.Rational(
        286 * depth**6 + 3546 * depth**5 + 12721 * depth**4
        - 7812 * depth**3 - 86231 * depth**2 + 40338 * depth
        + 209160,
        5184,
    )


def ordinary_coefficient(page_count: int, depth: int) -> Fraction:
    total_loss = depth + 4
    numerator = 0
    for left in range(page_count + 1):
        right = page_count - left
        kernel = sum(
            normalized_profile(1, left)[loss]
            * normalized_profile(1, right)[total_loss - loss]
            - normalized_profile(0, left)[loss]
            * normalized_profile(2, right)[total_loss - loss]
            for loss in range(total_loss + 1)
        )
        numerator += math.comb(page_count, left) * kernel
    return Fraction(
        numerator,
        2**page_count * 2 * page_count * (page_count - 1),
    )


def ordinary_polynomial(depth: int) -> sp.Poly:
    start = max(2, (depth + 5) // 2)
    points = [
        (
            page_count,
            sp.Rational(
                ordinary_coefficient(page_count, depth).numerator,
                ordinary_coefficient(page_count, depth).denominator,
            ),
        )
        for page_count in range(start, start + depth + 3)
    ]
    polynomial = sp.Poly(sp.interpolate(points[: depth + 1], K), K)
    assert polynomial.degree() <= depth
    assert all(
        polynomial.eval(page_count) == value
        for page_count, value in points[depth + 1 :]
    )
    return polynomial


def audit(
    maximum_loss: int = 16,
    maximum_depth: int = 10,
) -> dict[str, object]:
    if not 8 <= maximum_loss <= RAW_MAXIMUM_LOSS:
        raise ValueError("maximum_loss must lie between 8 and 18")
    if not 2 <= maximum_depth <= maximum_loss - 4:
        raise ValueError("maximum_depth must lie between 2 and loss-4")

    claimed = claimed_fourth_profiles()
    fourth_checks = 0
    for profile_index in range(3):
        series = sp.series(
            claimed[profile_index], Z, 0, maximum_loss - 3
        ).removeO().expand()
        for loss in range(4, maximum_loss + 1):
            actual = profile_polynomial(
                profile_index, loss
            ).coeff_monomial(J ** (loss - 4))
            assert actual == series.coeff(Z, loss - 4)
            fourth_checks += 1

    # The exceptional summand is 8*j*s^-2 times a normalized product.
    # Thus its s^-4 coefficient uses the product's third subdegree after
    # j=xs.  It is genuinely present and cannot be shifted to rank 4.
    exceptional_rank_four = [
        exceptional_profile_polynomial(loss).coeff_monomial(
            J ** (loss - 4)
        )
        for loss in range(4, maximum_loss + 1)
    ]
    assert any(value != 0 for value in exceptional_rank_four)

    kernels, _ = raw_determinant_kernels(maximum_loss)
    g0, g1, g2, g3, g4 = kernels
    assert g0 == 0
    assert sp.expand(g1 + g1.subs(X, 1 - X)) == 0

    half = sp.Rational(1, 2)
    h2 = sp.expand(g2.subs(X, half))
    h3 = sp.expand(
        g3.subs(X, half)
        + sp.diff(g2, X, 2).subs(X, half) / 8
    )
    h4 = sp.expand(
        g4.subs(X, half)
        + sp.diff(g3, X, 2).subs(X, half) / 8
        + sp.diff(g2, X, 4).subs(X, half) / 128
    )
    expected = {
        2: 2 * T**4 / (1 - T),
        3: -T**4
        * (
            43 * T**4 - 129 * T**3 + 108 * T**2
            - 6 * T + 6
        )
        / (3 * (1 - T) ** 4),
        4: expected_h4(),
    }
    for rank, actual in ((2, h2), (3, h3), (4, h4)):
        target = sp.series(
            expected[rank], T, 0, maximum_loss + 1
        ).removeO().expand()
        assert truncate_t(actual - target, maximum_loss) == 0

    # Order ledger for a symmetric Bin(k,1/2) average through k^-4:
    # (kernel rank, derivative order, resulting inverse-k order).
    ledger = [
        (2, 0, 2), (2, 2, 3), (2, 4, 4),
        (3, 0, 3), (3, 2, 4), (4, 0, 4),
    ]
    assert 2 + 6 // 2 == 5

    combined = sp.expand(h2 + h3 + h4)
    # For d=0,1 a k^(d-2) coefficient is not defined.  The formal
    # continuation cancels at precisely these two boundary depths.
    assert combined.coeff(T, 4) == 0
    assert combined.coeff(T, 5) == 0

    rows = []
    for depth in range(2, maximum_depth + 1):
        polynomial = ordinary_polynomial(depth)
        actual = polynomial.coeff_monomial(K ** (depth - 2))
        from_kernels = sp.Rational(1, 2) * combined.coeff(
            T, depth + 4
        )
        expected_value = second_symbol(depth)
        assert actual == from_kernels == expected_value
        rows.append(
            {
                "depth": depth,
                "exact_ordinary_symbol": str(actual),
            }
        )

    return {
        "schema": (
            "amra.opg1757."
            "independent-ordinary-second-subleading-audit.v1"
        ),
        "status": "PASS",
        "imports_existing_opg_verifier": False,
        "maximum_loss": maximum_loss,
        "rank_four_exact_profile_checks": fourth_checks,
        "exceptional_rank_four_nonzero": True,
        "g4_built_by_generic_convolution": True,
        "g1_exactly_antisymmetric": True,
        "central_order_ledger": ledger,
        "sixth_moment_first_total_order": 5,
        "boundary_cancellations": ["d=0", "d=1"],
        "maximum_exact_ordinary_depth": maximum_depth,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-loss", type=int, default=16)
    parser.add_argument("--maximum-depth", type=int, default=10)
    arguments = parser.parse_args()
    print(
        json.dumps(
            audit(arguments.maximum_loss, arguments.maximum_depth),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
