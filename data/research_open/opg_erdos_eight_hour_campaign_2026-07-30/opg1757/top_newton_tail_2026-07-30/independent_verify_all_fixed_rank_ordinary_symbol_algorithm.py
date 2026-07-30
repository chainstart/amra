#!/usr/bin/env python3
"""Independent rank-five audit of the all-fixed-rank symbol algorithm.

This module imports no OPG verifier and no stored profile function.  It
implements both sides independently:

* the parameterized saddle/Gamma recurrence through profile rank five;
* exact normalized finite Lagrange profiles and exact binomial averages.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


X, T, Z, J, K, D = sp.symbols("x t z j k d")
W = 1 - 2 * X


def polynomial_add(left, right):
    result = left.copy()
    for degree, value in right.items():
        result[degree] = result.get(degree, 0) + value
    return result


def polynomial_multiply(left, right):
    result = {}
    for left_degree, left_value in left.items():
        for right_degree, right_value in right.items():
            degree = left_degree + right_degree
            result[degree] = (
                result.get(degree, 0)
                + left_value * right_value
            )
    return result


def polynomial_scale(polynomial, scalar):
    return {
        degree: scalar * value
        for degree, value in polynomial.items()
    }


def phase_derivative(order: int):
    return (
        sp.factorial(order - 1)
        / 2**order
        * (
            -(1 - X) ** (1 - order)
            + (-1) ** order * X ** (1 - order)
        )
    )


def phase_exponential(maximum_rank: int):
    maximum_epsilon = 2 * maximum_rank
    phase = {
        order: phase_derivative(order)
        for order in range(2, maximum_epsilon + 3)
    }
    terms = [{} for _ in range(maximum_epsilon + 1)]
    for power in range(1, maximum_epsilon + 1):
        terms[power] = {
            power + 2: (
                phase[power + 2]
                / sp.factorial(power + 2)
            )
        }
    result = [{} for _ in range(maximum_epsilon + 1)]
    result[0] = {0: sp.S.One}
    for degree in range(1, maximum_epsilon + 1):
        total = {}
        for power in range(1, degree + 1):
            total = polynomial_add(
                total,
                polynomial_scale(
                    polynomial_multiply(
                        terms[power],
                        result[degree - power],
                    ),
                    power,
                ),
            )
        result[degree] = polynomial_scale(
            total,
            sp.Rational(1, degree),
        )
    return result, sp.cancel(-1 / phase[2])


def gaussian_moment(polynomial, variance, degree_shift=0):
    result = sp.S.Zero
    for degree, coefficient in polynomial.items():
        degree += degree_shift
        if degree % 2:
            continue
        half = degree // 2
        moment = sp.factorial2(2 * half - 1) if half else 1
        result += coefficient * moment * variance**half
    return sp.factor(result)


def main_amplitude(shift: int, order: int):
    result = sp.S.Zero
    for first_order in range(order + 1):
        if first_order == 0:
            first = 1 / (2 * X) - 1
        else:
            first = (
                (-1) ** first_order
                / (2 * X) ** (first_order + 1)
            )
        second_order = order - first_order
        second = (
            sp.rf(shift, second_order)
            / (
                sp.factorial(second_order)
                * 2**second_order
            )
            * (1 - X) ** (-shift - second_order)
        )
        result += first * second
    return sp.factor(result)


def exceptional_amplitude(order: int):
    return sp.factor(
        sp.rf(3, order)
        / (sp.factorial(order) * 2**order)
        * (1 - X) ** (-3 - order)
    )


def gamma_exponential(arguments, maximum_rank: int):
    logarithm = [None]
    for order in range(1, maximum_rank + 1):
        value = sum(
            sign
            * sp.bernoulli(order + 1, shift)
            / scale**order
            for sign, scale, shift in arguments
        )
        logarithm.append(
            sp.factor(
                (-1) ** (order + 1)
                * value
                / (order * (order + 1))
            )
        )
    result = [sp.S.One]
    for degree in range(1, maximum_rank + 1):
        result.append(
            sp.factor(
                sum(
                    order
                    * logarithm[order]
                    * result[degree - order]
                    for order in range(1, degree + 1)
                )
                / degree
            )
        )
    return result


def saddle_corrections(
    amplitude,
    arguments,
    maximum_rank: int,
):
    phase, variance = phase_exponential(maximum_rank)
    integral = []
    for rank in range(maximum_rank + 1):
        integral.append(
            sp.factor(
                sum(
                    amplitude(order)
                    * gaussian_moment(
                        phase[2 * rank - order],
                        variance,
                        order,
                    )
                    for order in range(2 * rank + 1)
                )
            )
        )
    relative = [
        sp.factor(value / integral[0])
        for value in integral
    ]
    gamma = gamma_exponential(arguments, maximum_rank)
    return [
        sp.factor(
            sum(
                gamma[index] * relative[rank - index]
                for index in range(rank + 1)
            )
        )
        for rank in range(maximum_rank + 1)
    ]


@lru_cache(maxsize=None)
def profile_functions(maximum_rank: int = 5):
    primary = {}
    for shift in (0, 2, 4):
        arguments = [
            (1, X, 1),
            (1, 1, 1 - shift),
            (-1, 1 - X, 1 - shift),
        ]
        primary[shift] = [
            sp.factor(sp.sqrt(W) * value)
            for value in saddle_corrections(
                lambda order, shift=shift: main_amplitude(
                    shift,
                    order,
                ),
                arguments,
                maximum_rank,
            )
        ]

    exceptional_arguments = [
        (1, X, 1),
        (1, 1, -3),
        (-1, 1 - X, -2),
    ]
    exceptional = [
        sp.factor(8 * X / sp.sqrt(W) * value)
        for value in saddle_corrections(
            exceptional_amplitude,
            exceptional_arguments,
            maximum_rank - 1,
        )
    ]
    return [
        primary[0],
        primary[2],
        [
            primary[4][0],
            *[
                sp.factor(
                    primary[4][rank] + exceptional[rank - 1]
                )
                for rank in range(1, maximum_rank + 1)
            ],
        ],
    ]


@lru_cache(maxsize=None)
def normalized_falling(shift, length, maximum_loss):
    result = [1] + [0] * maximum_loss
    for offset in range(length):
        root = shift + offset
        for loss in range(maximum_loss, 0, -1):
            result[loss] -= root * result[loss - 1]
    return tuple(result)


def convolution(left, right, maximum_loss):
    result = [0] * (maximum_loss + 1)
    for left_loss, left_value in enumerate(left):
        for right_loss, right_value in enumerate(right):
            if left_loss + right_loss <= maximum_loss:
                result[left_loss + right_loss] += (
                    left_value * right_value
                )
    return tuple(result)


@lru_cache(maxsize=None)
def normalized_lagrange(beta, edge_count, maximum_loss):
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
def source_profile(profile_index, edge_count, maximum_loss):
    shift = (0, 2, 4)[profile_index]
    current = normalized_lagrange(
        shift,
        edge_count,
        maximum_loss,
    )
    previous = normalized_lagrange(
        shift + 1,
        edge_count - 1,
        maximum_loss,
    )
    difference = tuple(
        current[loss]
        - (
            2 * edge_count * previous[loss - 1]
            if loss
            else 0
        )
        for loss in range(maximum_loss + 1)
    )
    result = list(
        convolution(
            normalized_falling(
                shift,
                edge_count,
                maximum_loss,
            ),
            difference,
            maximum_loss,
        )
    )
    if profile_index == 2 and edge_count:
        exceptional = convolution(
            normalized_falling(
                4,
                edge_count - 1,
                maximum_loss,
            ),
            normalized_lagrange(
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


def source_profile_polynomial(profile_index, loss):
    values = [
        (
            edge_count,
            source_profile(
                profile_index,
                edge_count,
                loss,
            )[loss],
        )
        for edge_count in range(loss + 2)
    ]
    polynomial = sp.Poly(
        sp.interpolate(values[: loss + 1], J),
        J,
    )
    assert polynomial.eval(loss + 1) == values[-1][1]
    return polynomial


@lru_cache(maxsize=None)
def central_moment(moment: int):
    if moment == 0:
        return sp.S.One
    raw = sp.S.Zero
    for power in range(moment + 1):
        raw_moment = sum(
            sp.functions.combinatorial.numbers.stirling(
                power,
                falling_degree,
                kind=2,
            )
            * sp.ff(K, falling_degree)
            / 2**falling_degree
            for falling_degree in range(power + 1)
        )
        raw += (
            sp.binomial(moment, power)
            * (-K / 2) ** (moment - power)
            * raw_moment
        )
    return sp.factor(raw / K**moment)


def central_moment_coefficient(moment: int, inverse_rank: int):
    expression = sp.expand(central_moment(moment).subs(K, 1 / Z))
    return expression.coeff(Z, inverse_rank)


def determinant_kernels(profiles, maximum_rank: int):
    kernels = {}
    at = lambda expression, value: expression.subs(X, value)
    for rank in range(maximum_rank + 1):
        value = sp.S.Zero
        for left_rank in range(rank + 1):
            right_rank = rank - left_rank
            value += (
                at(profiles[1][left_rank], T * X)
                * at(profiles[1][right_rank], T * (1 - X))
                - at(profiles[0][left_rank], T * X)
                * at(profiles[2][right_rank], T * (1 - X))
            )
        kernels[rank] = sp.factor(T**rank * value)
    return kernels


def central_kernels(kernels, maximum_rank: int):
    result = {}
    half = sp.Rational(1, 2)
    for total_rank in range(2, maximum_rank + 1):
        value = sp.S.Zero
        for determinant_rank in range(2, total_rank + 1):
            inverse_rank = total_rank - determinant_rank
            for moment in range(0, 2 * inverse_rank + 1, 2):
                coefficient = central_moment_coefficient(
                    moment,
                    inverse_rank,
                )
                if coefficient:
                    value += (
                        coefficient
                        / sp.factorial(moment)
                        * sp.diff(
                            kernels[determinant_rank],
                            X,
                            moment,
                        ).subs(X, half)
                    )
        result[total_rank] = sp.factor(value)
    return result


def rank_three_polynomial(depth):
    return -sp.Rational(1, 83980800) * (
        158450 * depth**9
        + 2651625 * depth**8
        + 15805020 * depth**7
        + 6658380 * depth**6
        - 213815208 * depth**5
        - 151402725 * depth**4
        + 2063879770 * depth**3
        + 1562087520 * depth**2
        - 10631426832 * depth
        - 6142443840
    )


def rank_three_polynomial_generating_function():
    basis = [T**3 / (1 - T)]
    for _ in range(9):
        basis.append(sp.factor(T * sp.diff(basis[-1], T)))
    polynomial = sp.Poly(rank_three_polynomial(D), D)
    return sp.factor(
        sum(
            polynomial.coeff_monomial(D**power) * basis[power]
            for power in range(10)
        )
    )


def exact_ordinary_value(page_count, depth):
    total_loss = depth + 4
    numerator = 0
    for left in range(page_count + 1):
        right = page_count - left
        kernel = 0
        for loss in range(total_loss + 1):
            other = total_loss - loss
            kernel += (
                source_profile(1, left, total_loss)[loss]
                * source_profile(1, right, total_loss)[other]
                - source_profile(0, left, total_loss)[loss]
                * source_profile(2, right, total_loss)[other]
            )
        numerator += math.comb(page_count, left) * kernel
    return Fraction(
        numerator,
        2**page_count * 2 * page_count * (page_count - 1),
    )


def exact_ordinary_polynomial(depth):
    start = max(2, (depth + 5) // 2)
    points = []
    for page_count in range(start, start + depth + 3):
        value = exact_ordinary_value(page_count, depth)
        points.append(
            (
                page_count,
                sp.Rational(value.numerator, value.denominator),
            )
        )
    polynomial = sp.Poly(
        sp.interpolate(points[: depth + 1], K),
        K,
    )
    assert all(
        polynomial.eval(page_count) == value
        for page_count, value in points[depth + 1 :]
    )
    return polynomial


def audit(maximum_loss=12, maximum_depth=9):
    maximum_profile_rank = 5
    profiles = profile_functions(maximum_profile_rank)

    profile_checks = 0
    exceptional_rank_five_checks = 0
    for profile_index in range(3):
        for rank in range(maximum_profile_rank + 1):
            series = sp.series(
                profiles[profile_index][rank],
                X,
                0,
                maximum_loss - rank + 1,
            ).removeO().expand()
            for loss in range(rank, maximum_loss + 1):
                source = source_profile_polynomial(
                    profile_index,
                    loss,
                )
                actual = source.coeff_monomial(
                    J ** (loss - rank)
                )
                expected = series.coeff(X, loss - rank)
                assert actual == expected
                profile_checks += 1
                if profile_index == 2 and rank == 5:
                    exceptional_rank_five_checks += 1

    kernels = determinant_kernels(profiles, maximum_profile_rank)
    assert kernels[0] == 0
    assert sp.simplify(
        kernels[1] + kernels[1].subs(X, 1 - X)
    ) == 0
    central = central_kernels(kernels, maximum_profile_rank)

    expected_h2 = 2 * T**4 / (1 - T)
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
    expected_h4 = (
        T**5
        * (
            2389 * T**7
            - 14334 * T**6
            + 34245 * T**5
            - 40008 * T**4
            + 22152 * T**3
            - 5400 * T**2
            + 3672 * T
            + 144
        )
        / (36 * (1 - T) ** 7)
    )
    expected_h5 = (
        -T**6
        * (
            825719 * T**10
            - 7431471 * T**9
            + 29112669 * T**8
            - 64490751 * T**7
            + 87663474 * T**6
            - 74537550 * T**5
            + 40641750 * T**4
            - 17199000 * T**3
            + 8377560 * T**2
            + 1202040 * T
            + 272160
        )
        / (3240 * (1 - T) ** 10)
    )
    assert sp.simplify(central[2] - expected_h2) == 0
    assert sp.simplify(central[3] - expected_h3) == 0
    assert sp.simplify(central[4] - expected_h4) == 0
    assert sp.simplify(central[5] - expected_h5) == 0

    rank_three_generating_function = sp.factor(
        sum(central[rank] for rank in range(2, 6))
        / (2 * T**4)
    )
    expected_b3 = (
        -T**3
        * (
            825719 * T**9
            - 7216461 * T**8
            + 27224019 * T**7
            - 57304971 * T**6
            + 72322254 * T**5
            - 54697140 * T**4
            + 25024140 * T**3
            - 9849600 * T**2
            + 5989680 * T
            + 2118960
        )
        / (6480 * (1 - T) ** 10)
    )
    assert sp.simplify(
        rank_three_generating_function - expected_b3
    ) == 0
    assert sp.simplify(
        rank_three_generating_function
        - rank_three_polynomial_generating_function()
    ) == 0
    symbol_series = {}
    for symbol_rank in range(4):
        generating_function = sp.factor(
            sum(
                central[rank]
                for rank in range(2, symbol_rank + 3)
            )
            / (2 * T**4)
        )
        symbol_series[symbol_rank] = sp.series(
            generating_function,
            T,
            0,
            maximum_depth + 1,
        ).removeO().expand()

    ordinary_checks = 0
    rank_three_checks = 0
    rows = []
    for depth in range(maximum_depth + 1):
        polynomial = exact_ordinary_polynomial(depth)
        for symbol_rank in range(min(3, depth) + 1):
            actual = polynomial.coeff_monomial(
                K ** (depth - symbol_rank)
            )
            expected = symbol_series[symbol_rank].coeff(T, depth)
            assert actual == expected
            ordinary_checks += 1
            if symbol_rank == 3:
                rank_three_checks += 1
                rows.append(
                    {
                        "depth": depth,
                        "rank_three_symbol": str(actual),
                    }
                )
                assert actual == rank_three_polynomial(depth)

    moment_checks = 0
    for inverse_rank in range(4):
        for moment in range(0, 2 * inverse_rank + 3, 2):
            coefficient = central_moment_coefficient(
                moment,
                inverse_rank,
            )
            if moment > 2 * inverse_rank:
                assert coefficient == 0
            moment_checks += 1
    for moment in range(1, 9, 2):
        assert central_moment(moment) == 0
        moment_checks += 1

    return {
        "schema": "amra.opg1757.independent-all-fixed-rank-symbol.v1",
        "imports_existing_opg_verifier": False,
        "maximum_profile_rank": maximum_profile_rank,
        "phase_derivative_order": 12,
        "maximum_bernoulli_index": 6,
        "maximum_loss": maximum_loss,
        "profile_symbol_checks": profile_checks,
        "exceptional_rank_five_checks": exceptional_rank_five_checks,
        "central_moment_checks": moment_checks,
        "H2": str(sp.factor(central[2])),
        "H3": str(sp.factor(central[3])),
        "H4": str(sp.factor(central[4])),
        "H5": str(sp.factor(central[5])),
        "B3": str(rank_three_generating_function),
        "rank_three_polynomial": str(
            sp.factor(rank_three_polynomial(D))
        ),
        "rank_three_generating_identity": True,
        "maximum_depth": maximum_depth,
        "ordinary_symbol_checks_r_le_3": ordinary_checks,
        "rank_three_ordinary_checks": rank_three_checks,
        "rank_three_rows": rows,
        "verdict": "PASS",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-loss", type=int, default=12)
    parser.add_argument("--maximum-depth", type=int, default=9)
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
