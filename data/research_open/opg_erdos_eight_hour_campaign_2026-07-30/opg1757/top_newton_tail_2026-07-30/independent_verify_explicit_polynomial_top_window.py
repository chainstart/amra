#!/usr/bin/env python3
"""Independent red-team certificate for the explicit one-eighth window.

No existing OPG verifier is imported.  Exact finite Lagrange profiles,
Faulhaber/Newton transformations, determinant numerators, 4-Stirling
numbers, and all numerical absorptions are rebuilt here.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


A_INDEX, J, K, R, T = sp.symbols("a j k r t")
PROFILE_BASE = 2**16
ORDINARY_EXPONENT = 320
RAW_MAXIMUM_LOSS = 14


def coefficient_norm(expression: sp.Expr, *variables: sp.Symbol) -> int:
    polynomial = sp.Poly(sp.expand(expression), *variables)
    return int(sum(abs(value) for value in polynomial.coeffs()))


def faulhaber(power: int) -> sp.Expr:
    return sp.expand(
        sum(
            (-1) ** index
            * sp.bernoulli(index)
            * sp.binomial(power + 1, index)
            * T ** (power + 1 - index)
            for index in range(power + 1)
        )
        / (power + 1)
    )


@lru_cache(maxsize=None)
def power_sum(beta: int, power: int) -> sp.Expr:
    if power == 0:
        return T
    return sp.expand(
        sum(
            sp.binomial(power, q)
            * (beta + R) ** (power - q)
            * faulhaber(q)
            for q in range(power + 1)
        )
    )


@lru_cache(maxsize=None)
def falling_loss(beta: int, loss: int) -> sp.Expr:
    """P_(beta,loss)=(-1)^loss e_loss via Newton's recurrence."""
    elementary = [sp.S.One]
    for degree in range(1, loss + 1):
        elementary.append(
            sp.expand(
                sum(
                    (-1) ** (power - 1)
                    * elementary[degree - power]
                    * power_sum(beta, power)
                    for power in range(1, degree + 1)
                )
                / degree
            )
        )
    return sp.expand((-1) ** loss * elementary[loss])


def moment_transform(expression: sp.Expr) -> sp.Expr:
    """Apply the exact signed binomial moment to the variable t."""
    polynomial = sp.Poly(sp.expand(expression), T, R)
    result = sp.S.Zero
    for (t_power, r_power), coefficient in polynomial.terms():
        for falling_degree in range(t_power + 1):
            result += (
                coefficient
                * sp.functions.combinatorial.numbers.stirling(
                    t_power, falling_degree, kind=2
                )
                * (-1) ** falling_degree
                * sp.prod(R - offset for offset in range(falling_degree))
                * R**r_power
            )
    return sp.expand(result)


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
def normalized_lagrange(
    beta: int,
    edge_count: int,
    maximum_loss: int = RAW_MAXIMUM_LOSS,
) -> tuple[int, ...]:
    if edge_count < 0:
        return tuple([0] * (maximum_loss + 1))
    result = [0] * (maximum_loss + 1)
    for index in range(edge_count + 1):
        product = normalized_falling(
            beta + edge_count, index, maximum_loss
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
def normalized_profile_parts(
    profile_index: int,
    edge_count: int,
    maximum_loss: int = RAW_MAXIMUM_LOSS,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    shift = (0, 2, 4)[profile_index]
    current = normalized_lagrange(shift, edge_count, maximum_loss)
    previous = normalized_lagrange(
        shift + 1, edge_count - 1, maximum_loss
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
    main = truncated_convolution(
        normalized_falling(shift, edge_count, maximum_loss),
        difference,
        maximum_loss,
    )
    exceptional = [0] * (maximum_loss + 1)
    if profile_index == 2 and edge_count >= 1:
        product = truncated_convolution(
            normalized_falling(4, edge_count - 1, maximum_loss),
            normalized_lagrange(4, edge_count - 1, maximum_loss),
            maximum_loss,
        )
        for loss in range(2, maximum_loss + 1):
            exceptional[loss] = 8 * edge_count * product[loss - 2]
    return main, tuple(exceptional)


def normalized_profile(
    profile_index: int,
    edge_count: int,
) -> tuple[int, ...]:
    main, exceptional = normalized_profile_parts(
        profile_index, edge_count
    )
    return tuple(a + b for a, b in zip(main, exceptional))


@lru_cache(maxsize=None)
def profile_polynomial(
    profile_index: int,
    loss: int,
    part: str = "total",
) -> sp.Poly:
    def value(edge_count: int) -> int:
        main, exceptional = normalized_profile_parts(
            profile_index, edge_count
        )
        if part == "main":
            return main[loss]
        if part == "exceptional":
            return exceptional[loss]
        return main[loss] + exceptional[loss]

    values = [(edge_count, value(edge_count)) for edge_count in range(loss + 2)]
    polynomial = sp.Poly(sp.interpolate(values[: loss + 1], J), J)
    assert polynomial.eval(loss + 1) == values[-1][1]
    return polynomial


def averaged_numerator(page_count: int, total_loss: int) -> Fraction:
    total = 0
    for left in range(page_count + 1):
        right = page_count - left
        kernel = sum(
            normalized_profile(1, left)[loss]
            * normalized_profile(1, right)[total_loss - loss]
            - normalized_profile(0, left)[loss]
            * normalized_profile(2, right)[total_loss - loss]
            for loss in range(total_loss + 1)
        )
        total += math.comb(page_count, left) * kernel
    return Fraction(total, 2**page_count)


@lru_cache(maxsize=None)
def numerator_polynomial(total_loss: int) -> sp.Poly:
    values = [
        (
            page_count,
            sp.Rational(
                averaged_numerator(page_count, total_loss).numerator,
                averaged_numerator(page_count, total_loss).denominator,
            ),
        )
        for page_count in range(total_loss + 3)
    ]
    polynomial = sp.Poly(
        sp.interpolate(values[: total_loss + 1], K), K
    )
    assert all(
        polynomial.eval(page_count) == value
        for page_count, value in values[total_loss + 1 :]
    )
    return polynomial


def ordinary_polynomial(depth: int) -> sp.Poly:
    numerator = numerator_polynomial(depth + 4)
    quotient, remainder = sp.div(
        numerator,
        sp.Poly(2 * K * (K - 1), K),
    )
    assert remainder.is_zero
    return quotient


def falling_basis_coefficients(polynomial: sp.Poly) -> list[sp.Expr]:
    """Coefficients in P(k)=sum_q c_q (k)_q."""
    result = [sp.S.Zero] * (polynomial.degree() + 1)
    for (power,), coefficient in polynomial.terms():
        for falling_degree in range(power + 1):
            result[falling_degree] += (
                coefficient
                * sp.functions.combinatorial.numbers.stirling(
                    power, falling_degree, kind=2
                )
            )
    return [sp.expand(value) for value in result]


@lru_cache(maxsize=None)
def four_stirling(n: int, deficit: int) -> int:
    """Shifted 4-Stirling number {n \\brace n-deficit}_4."""
    if deficit < 0 or deficit > n:
        return 0
    if n == 0:
        return int(deficit == 0)
    return (
        four_stirling(n - 1, deficit)
        + (n - deficit + 4) * four_stirling(n - 1, deficit - 1)
    )


def audit(maximum_loss: int = 10, maximum_depth: int = 6) -> dict[str, object]:
    if not 4 <= maximum_loss <= RAW_MAXIMUM_LOSS:
        raise ValueError("maximum_loss must lie between 4 and 14")
    if not 1 <= maximum_depth <= maximum_loss - 4:
        raise ValueError("maximum_depth must lie between 1 and loss-4")

    faulhaber_checks = 0
    for power in range(1, 9):
        direct = sp.summation(
            A_INDEX**power, (A_INDEX, 0, T - 1)
        )
        assert sp.expand(direct - faulhaber(power)) == 0
        assert coefficient_norm(faulhaber(power), T) < 8 * math.factorial(power)
        for beta in (0, 5):
            direct_shifted = sp.summation(
                (beta + R + A_INDEX) ** power,
                (A_INDEX, 0, T - 1),
            )
            assert sp.expand(
                direct_shifted - power_sum(beta, power)
            ) == 0
            assert coefficient_norm(
                power_sum(beta, power), T, R
            ) <= (56 * power) ** power
        faulhaber_checks += 1

    newton_checks = 0
    moment_checks = 0
    for beta in range(6):
        for loss in range(1, 6):
            polynomial = falling_loss(beta, loss)
            assert coefficient_norm(polynomial, T, R) <= (112 * loss) ** loss
            transformed = moment_transform(polynomial)
            values = [
                (
                    edge_count,
                    normalized_lagrange(beta, edge_count)[loss],
                )
                for edge_count in range(2 * loss + 2)
            ]
            expected = sp.Poly(
                sp.interpolate(values[: 2 * loss + 1], R), R
            )
            assert expected.eval(2 * loss + 1) == values[-1][1]
            assert sp.expand(transformed - expected.as_expr()) == 0
            assert coefficient_norm(transformed, R) <= (
                2**11 * loss**5
            ) ** loss
            newton_checks += 1
            moment_checks += 1

    profile_checks = 0
    exceptional_checks = 0
    for loss in range(1, maximum_loss + 1):
        bound = (PROFILE_BASE * (loss + 1) ** 5) ** loss
        for profile_index in range(3):
            actual = sum(
                abs(value)
                for value in profile_polynomial(
                    profile_index, loss
                ).all_coeffs()
            )
            assert actual <= bound
            profile_checks += 1
        if loss >= 2:
            exceptional_norm = sum(
                abs(value)
                for value in profile_polynomial(
                    2, loss, "exceptional"
                ).all_coeffs()
            )
            exceptional_bound = (
                8
                * (loss - 1)
                * (2**13 * (loss + 1) ** 5) ** (loss - 2)
            )
            assert exceptional_norm <= exceptional_bound
            exceptional_checks += 1

    determinant_checks = 0
    ordinary_checks = 0
    for depth in range(maximum_depth + 1):
        total_loss = depth + 4
        numerator = numerator_polynomial(total_loss)
        assert numerator.degree() <= total_loss - 2
        norm_bound = (
            2**18 * (total_loss + 1) ** 6
        ) ** total_loss
        falling_coefficients = falling_basis_coefficients(numerator)
        falling_coefficients.extend(
            [sp.S.Zero]
            * (total_loss + 1 - len(falling_coefficients))
        )
        assert sum(abs(value) for value in falling_coefficients) <= norm_bound
        assert falling_coefficients[total_loss] == 0
        assert falling_coefficients[total_loss - 1] == 0
        determinant_checks += 1
        ordinary = ordinary_polynomial(depth)
        assert ordinary.degree() == depth
        if depth:
            raw_bound = (
                2**18 * (depth + 5) ** 6
            ) ** (depth + 4)
            final_bound = (
                2 ** (ORDINARY_EXPONENT * depth)
                * depth ** (6 * depth)
            )
            assert raw_bound <= final_bound
        ordinary_checks += 1

    # Exact finite redundancy for the uniform fixed-offset absorption.
    absorption_checks = 0
    for depth in range(1, 257):
        raw = (2**18 * (depth + 5) ** 6) ** (depth + 4)
        target = (
            2 ** (ORDINARY_EXPONENT * depth)
            * depth ** (6 * depth)
        )
        assert raw <= target
        absorption_checks += 1
    assert 90 + 13 + 217 == ORDINARY_EXPONENT

    # Direct finite checks of the exact 4-Stirling ratio, including all
    # formerly delicate small (d,j) cases.
    ratio_checks = 0
    for n in range(8, 65):
        for deficit in range(n // 4 + 1):
            denominator = four_stirling(n, deficit)
            for shift in range(deficit + 1):
                ratio = sp.Rational(
                    four_stirling(n - shift, deficit - shift),
                    denominator,
                )
                upper = (
                    sp.exp(sp.Rational(6 * deficit**2, n))
                    * sp.Rational(2 * deficit, n**2) ** shift
                    if shift
                    else sp.exp(sp.Rational(6 * deficit**2, n))
                )
                assert ratio <= upper
                ratio_checks += 1

    # The threshold arithmetic can be done on exponents alone:
    # k0=2^2584 and d<=k0^(1/8)=2^323.
    threshold_exponent = 2584
    depth_exponent = threshold_exponent // 8
    theta_exponent = (
        1 + ORDINARY_EXPONENT + 7 * depth_exponent - threshold_exponent
    )
    assert theta_exponent == -2
    assert 2**depth_exponent <= 2 ** (threshold_exponent - 2)
    assert 2 ** (depth_exponent + 1) + 10 <= 2**threshold_exponent
    exponential_argument = sp.Rational(
        6, 2 ** (3 * threshold_exponent // 4)
    )
    assert exponential_argument < sp.Rational(1, 2)
    # exp(1/2)<2 follows, for example, by squaring and using e<4.

    return {
        "schema": (
            "amra.opg1757."
            "independent-explicit-polynomial-window-audit.v1"
        ),
        "status": "PASS",
        "imports_existing_opg_verifier": False,
        "faulhaber_checks": faulhaber_checks,
        "newton_partition_checks": newton_checks,
        "moment_conversion_checks": moment_checks,
        "profile_norm_checks": profile_checks,
        "exceptional_norm_checks": exceptional_checks,
        "determinant_degree_and_norm_checks": determinant_checks,
        "ordinary_division_checks": ordinary_checks,
        "fixed_offset_absorption_checks": absorption_checks,
        "four_stirling_ratio_checks": ratio_checks,
        "effective_threshold": "2^2584",
        "threshold_theta": "1/4",
        "proved_eta": "1/8",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-loss", type=int, default=10)
    parser.add_argument("--maximum-depth", type=int, default=6)
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
