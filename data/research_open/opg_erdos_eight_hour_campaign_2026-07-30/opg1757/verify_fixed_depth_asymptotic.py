#!/usr/bin/env python3
"""Exact regression for the fixed-depth OPG Newton theorem."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction


def product_prefix_coefficients(low: int, high: int) -> tuple[int, int, int]:
    """Coefficients through u^2 of product(low <= j <= high) (1-j*u)."""

    values = list(range(low, high + 1))
    first_sum = sum(values)
    square_sum = sum(value * value for value in values)
    return 1, -first_sum, (first_sum * first_sum - square_sum) // 2


def normalized_prefix(component_count: int, adjacent: bool) -> tuple[Fraction, ...]:
    """First three normalized coefficients in (5) or (6)."""

    c = component_count
    result = [Fraction(0), Fraction(0), Fraction(0)]
    for index in range(c):
        scalar = Fraction(
            (-1) ** index * (c + index + (2 if adjacent else 0)),
            2**index
            * math.factorial(index)
            * math.factorial(c - index - 1),
        )
        low = 3 if adjacent else 1
        high = c + index + (1 if adjacent else -1)
        coefficients = product_prefix_coefficients(low, high)
        for degree in range(3):
            result[degree] += scalar * coefficients[degree]
    return tuple(result)


def predicted_prefix(component_count: int, adjacent: bool) -> tuple[Fraction, ...]:
    rho = component_count - 1
    g = Fraction(1, 2**rho * math.factorial(rho))
    if adjacent:
        return (
            3 * g,
            11 * rho * g,
            Fraction(5 * rho * (13 * rho - 37), 2) * g,
        )
    return (
        g,
        5 * rho * g,
        Fraction(rho * (35 * rho - 47), 2) * g,
    )


def leading_determinant_constant(total_components: int) -> Fraction:
    total = Fraction(0)
    R = total_components - 2
    for rho in range(R + 1):
        sigma = R - rho
        weight = Fraction(
            1,
            2**R * math.factorial(rho) * math.factorial(sigma),
        )
        total += 2 * weight * (3 * R - (rho - sigma) ** 2)
    return total


def w0(n: int, components: int) -> int:
    total = Fraction(0)
    maximum = min(components - 1, n - components)
    for index in range(maximum + 1):
        exponent = n - components - 1 - index
        power = (
            Fraction(n**exponent)
            if exponent >= 0
            else Fraction(1, n ** (-exponent))
        )
        total += Fraction(
            (-1) ** index
            * (components + index)
            * math.factorial(n - 1),
            2**index
            * math.factorial(index)
            * math.factorial(components - index - 1)
            * math.factorial(n - components - index),
        ) * power
    if total.denominator != 1:
        raise AssertionError(("w0", n, components, total))
    return total.numerator


def adjacent_pair(n: int, components: int) -> int:
    total = Fraction(0)
    for index in range(components):
        factorial_index = n - components - index - 2
        if factorial_index < 0:
            continue
        exponent = n - components - index - 3
        power = Fraction(n**exponent) if exponent >= 0 else Fraction(1, n ** (-exponent))
        total += Fraction(
            (-1) ** index
            * (components + index + 2)
            * math.factorial(n - 3),
            2**index
            * math.factorial(index)
            * math.factorial(components - index - 1)
            * math.factorial(factorial_index),
        ) * power
    if total.denominator != 1:
        raise AssertionError(("adjacent", n, components, total))
    return total.numerator


def component_count(n: int, forced_matching: int, components: int) -> int:
    if components < 1 or components > n - forced_matching:
        return 0
    base = w0(n, components)
    if forced_matching == 0:
        return base
    if forced_matching == 1:
        value = Fraction(
            2 * (n - components) * base,
            n * (n - 1),
        )
    elif forced_matching == 2:
        adjacent = adjacent_pair(n, components)
        numerator = (
            math.comb(n - components, 2) * base
            - n * (n - 1) * (n - 2) // 2 * adjacent
        )
        value = Fraction(
            numerator,
            n * (n - 1) * (n - 2) * (n - 3) // 8,
        )
    else:
        raise ValueError(forced_matching)
    if value.denominator != 1:
        raise AssertionError(
            ("matching", n, forced_matching, components, value)
        )
    return value.numerator


def determinant(n: int, total_components: int) -> int:
    result = 0
    for left in range(1, total_components):
        right = total_components - left
        result += component_count(n, 1, left) * component_count(n, 1, right)
        result -= component_count(n, 0, left) * component_count(n, 2, right)
    return result


def newton_coefficient(k: int, depth: int) -> int:
    q0 = (k - 2) // 2
    n0 = q0 + 4
    total0 = 3 if k % 2 else 4
    raw = 0
    for offset in range(depth + 1):
        raw += (
            (-1) ** (depth - offset)
            * math.comb(q0 + depth, depth - offset)
            * determinant(n0 + offset, total0 + 2 * offset)
        )
    value = Fraction(math.factorial(k - 2) * raw, 2)
    if value.denominator != 1:
        raise AssertionError(("newton", k, depth, value))
    return value.numerator


def audit(
    maximum_component_count: int = 12,
    maximum_k: int = 28,
    maximum_depth: int = 4,
) -> dict[str, object]:
    expansion_checks = []
    for components in range(1, maximum_component_count + 1):
        for adjacent in (False, True):
            direct = normalized_prefix(components, adjacent)
            predicted = predicted_prefix(components, adjacent)
            if direct != predicted:
                raise AssertionError(
                    ("prefix", components, adjacent, direct, predicted)
                )
            expansion_checks.append((components, adjacent))

    determinant_checks = []
    for total_components in range(3, maximum_component_count + 1):
        direct = leading_determinant_constant(total_components)
        predicted = Fraction(4, math.factorial(total_components - 3))
        if direct != predicted:
            raise AssertionError(
                ("constant", total_components, direct, predicted)
            )
        determinant_checks.append(total_components)

    coefficient_checks = []
    for depth in range(maximum_depth + 1):
        positive_from = None
        checked = []
        for k in range(2, maximum_k + 1):
            value = newton_coefficient(k, depth)
            checked.append((k, value))
        for candidate in range(2, maximum_k + 1):
            if all(value > 0 for k, value in checked if k >= candidate):
                positive_from = candidate
                break
        coefficient_checks.append(
            {
                "depth": depth,
                "checked_through_k": maximum_k,
                "positive_from_in_checked_range": positive_from,
                "minimum_sign": min(
                    (value > 0) - (value < 0) for _, value in checked
                ),
            }
        )

    return {
        "schema": "amra.opg1757.fixed-depth-asymptotic.v1",
        "scope": (
            "Finite exact regressions for a human fixed-depth asymptotic "
            "theorem; finite positivity is not used as its proof."
        ),
        "expansion_checks": len(expansion_checks),
        "determinant_constant_checks": determinant_checks,
        "coefficient_checks": coefficient_checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-component-count", type=int, default=12)
    parser.add_argument("--maximum-k", type=int, default=28)
    parser.add_argument("--maximum-depth", type=int, default=4)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(
                args.maximum_component_count,
                args.maximum_k,
                args.maximum_depth,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
