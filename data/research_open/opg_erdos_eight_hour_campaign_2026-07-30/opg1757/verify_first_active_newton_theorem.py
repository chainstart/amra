#!/usr/bin/env python3
"""Independent audit of the first active base-four Newton coefficient."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from functools import lru_cache


def tree_weight(twos: int, ones: int) -> int:
    """Weighted Cayley count for one nonempty component."""
    vertices = twos + ones
    if vertices == 1:
        return 1
    return 2**twos * (2 * twos + ones) ** (vertices - 2)


@lru_cache(maxsize=None)
def forest_row(twos: int, ones: int) -> tuple[int, ...]:
    """Count weighted forests by edges, selecting the first component."""
    vertices = twos + ones
    if vertices == 0:
        return (1,)

    out = [0] * vertices
    if ones:
        # The distinguished vertex has weight one.
        for component_twos in range(twos + 1):
            for other_ones in range(ones):
                component_vertices = component_twos + other_ones + 1
                multiplier = (
                    math.comb(twos, component_twos)
                    * math.comb(ones - 1, other_ones)
                    * tree_weight(component_twos, other_ones + 1)
                )
                remainder = forest_row(
                    twos - component_twos,
                    ones - other_ones - 1,
                )
                shift = component_vertices - 1
                for degree, value in enumerate(remainder):
                    out[shift + degree] += multiplier * value
    else:
        # The distinguished vertex has weight two.
        for other_twos in range(twos):
            component_vertices = other_twos + 1
            multiplier = (
                math.comb(twos - 1, other_twos)
                * tree_weight(other_twos + 1, 0)
            )
            remainder = forest_row(twos - other_twos - 1, 0)
            shift = component_vertices - 1
            for degree, value in enumerate(remainder):
                out[shift + degree] += multiplier * value
    return tuple(out)


def component_count(n: int, h: int, components: int) -> int:
    blocks = n - h
    degree = blocks - components
    if degree < 0:
        return 0
    return forest_row(h, n - 2 * h)[degree]


def scaled_fraction(
    numerator: int,
    base: int,
    exponent: int,
    denominator: int = 1,
) -> Fraction:
    value = Fraction(numerator, denominator)
    if exponent >= 0:
        return value * base**exponent
    return value / base ** (-exponent)


def exact_scaled(
    numerator: int,
    base: int,
    exponent: int,
    denominator: int = 1,
) -> int:
    value = scaled_fraction(numerator, base, exponent, denominator)
    if value.denominator != 1:
        raise AssertionError(
            (numerator, base, exponent, denominator, value)
        )
    return value.numerator


def closed_component_count(n: int, h: int, components: int) -> int:
    if (h, components) == (0, 1):
        return exact_scaled(1, n, n - 2)
    if (h, components) == (0, 2):
        return exact_scaled((n - 1) * (n + 6), n, n - 4, 2)
    if (h, components) == (0, 3):
        return exact_scaled(
            (n - 2)
            * (n - 1)
            * (n * n + 13 * n + 60),
            n,
            n - 6,
            8,
        )
    if (h, components) == (1, 1):
        return exact_scaled(2, n, n - 3)
    if (h, components) == (1, 2):
        return exact_scaled((n - 2) * (n + 6), n, n - 5)
    if (h, components) == (1, 3):
        return exact_scaled(
            (n - 3)
            * (n - 2)
            * (n * n + 13 * n + 60),
            n,
            n - 7,
            4,
        )
    if (h, components) == (2, 1):
        return exact_scaled(4, n, n - 4)
    if (h, components) == (2, 2):
        return exact_scaled(
            2 * (n * n + 3 * n - 20), n, n - 6
        )
    if (h, components) == (2, 3):
        return exact_scaled(
            (n - 4)
            * (n**3 + 10 * n * n + 17 * n - 210),
            n,
            n - 8,
            2,
        )
    raise ValueError((n, h, components))


def determinant_with_total_components(
    n: int, total_components: int
) -> int:
    direct = 0
    for left_components in range(1, total_components):
        right_components = total_components - left_components
        direct += component_count(n, 1, left_components) * component_count(
            n, 1, right_components
        )
        direct -= component_count(n, 0, left_components) * component_count(
            n, 2, right_components
        )
    return direct


def determinant_at_first_support(k: int) -> tuple[int, int]:
    q0 = (k - 2) // 2
    n = 4 + q0
    total_components = 2 * n - 2 - k
    direct = determinant_with_total_components(n, total_components)

    if k % 2:
        closed = exact_scaled(4, n, 2 * n - 8)
    else:
        closed = exact_scaled(
            4 * (n * n + 4 * n - 24), n, 2 * n - 10
        )
    return direct, closed


def normalized_closed(k: int) -> int:
    q0 = (k - 2) // 2
    n = 4 + q0
    if k % 2:
        return exact_scaled(
            2 * math.factorial(k - 2), n, k - 3
        )
    return exact_scaled(
        math.factorial(k - 2) * (k * k + 20 * k - 12),
        n,
        k - 4,
        2,
    )


def direct_first_coefficient(k: int) -> int:
    determinant, _ = determinant_at_first_support(k)
    numerator = math.factorial(k) * determinant
    denominator = 2 * k * (k - 1)
    if numerator % denominator:
        raise AssertionError("normalization is not integral")
    return numerator // denominator


def closed_component_determinant(
    n: int, total_components: int
) -> int:
    if total_components == 3:
        return exact_scaled(4, n, 2 * n - 8)
    if total_components == 4:
        return exact_scaled(
            4 * (n * n + 4 * n - 24), n, 2 * n - 10
        )
    if total_components == 5:
        polynomial = n**3 + 12 * n * n + 20 * n - 225
        return exact_scaled(
            2 * (n - 4) * polynomial, n, 2 * n - 12
        )
    if total_components == 6:
        polynomial = (
            n**5
            + 16 * n**4
            + 52 * n**3
            - 587 * n * n
            - 3063 * n
            + 12240
        )
        return exact_scaled(
            2 * (n - 4) * polynomial,
            n,
            2 * n - 14,
            3,
        )
    raise ValueError(total_components)


def determinant_at_second_support(k: int) -> tuple[int, int]:
    q0 = (k - 2) // 2
    n0 = 4 + q0
    n1 = n0 + 1
    total0 = 2 * n0 - 2 - k
    total1 = total0 + 2
    direct = determinant_with_total_components(
        n1, total1
    ) - (q0 + 1) * determinant_with_total_components(n0, total0)
    closed = closed_component_determinant(
        n1, total1
    ) - (q0 + 1) * closed_component_determinant(n0, total0)
    return direct, closed


def direct_second_coefficient(k: int) -> int:
    determinant, _ = determinant_at_second_support(k)
    value = Fraction(
        math.factorial(k) * determinant,
        2 * k * (k - 1),
    )
    if value.denominator != 1:
        raise AssertionError((k, value))
    return value.numerator


def normalized_second_closed(k: int) -> int:
    q0 = (k - 2) // 2
    n = 5 + q0
    if k % 2:
        polynomial = n**3 + 12 * n * n + 20 * n - 225
        bracket = scaled_fraction(
            polynomial, n, 2 * n - 12
        ) - 2 * scaled_fraction(1, n - 1, 2 * n - 10)
    else:
        polynomial = (
            n**5
            + 16 * n**4
            + 52 * n**3
            - 587 * n * n
            - 3063 * n
            + 12240
        )
        secondary = n * n + 2 * n - 27
        bracket = scaled_fraction(
            polynomial, n, 2 * n - 14, 3
        ) - 2 * secondary * scaled_fraction(
            1, n - 1, 2 * n - 12
        )
    value = math.factorial(k - 2) * (n - 4) * bracket
    if value.denominator != 1:
        raise AssertionError((k, value))
    return value.numerator


def audit(maximum_n: int = 13, maximum_k: int = 20) -> dict[str, object]:
    component_checks = []
    for n in range(4, maximum_n + 1):
        for h in range(3):
            for components in range(1, 4):
                direct = component_count(n, h, components)
                closed = closed_component_count(n, h, components)
                if direct != closed:
                    raise AssertionError((n, h, components, direct, closed))
                component_checks.append((n, h, components))

    coefficient_checks = []
    for k in range(2, maximum_k + 1):
        direct_det, closed_det = determinant_at_first_support(k)
        direct = direct_first_coefficient(k)
        closed = normalized_closed(k)
        if direct_det != closed_det or direct != closed or direct <= 0:
            raise AssertionError(
                (k, direct_det, closed_det, direct, closed)
            )
        coefficient_checks.append(
            {
                "k": k,
                "q0": (k - 2) // 2,
                "first_coefficient": direct,
            }
        )
        if k >= 3:
            direct_second_det, closed_second_det = (
                determinant_at_second_support(k)
            )
            direct_second = direct_second_coefficient(k)
            closed_second = normalized_second_closed(k)
            if (
                direct_second_det != closed_second_det
                or direct_second != closed_second
                or direct_second <= 0
            ):
                raise AssertionError(
                    (
                        k,
                        direct_second_det,
                        closed_second_det,
                        direct_second,
                        closed_second,
                    )
                )
            coefficient_checks[-1]["q1"] = (k - 2) // 2 + 1
            coefficient_checks[-1]["second_coefficient"] = direct_second

    return {
        "schema": "amra.opg1757.first-active-newton-theorem.v1",
        "scope": (
            "Finite regression of a human all-k proof: independent "
            "component recursion versus the closed formulas."
        ),
        "component_checks": len(component_checks),
        "coefficient_checks": coefficient_checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-n", type=int, default=13)
    parser.add_argument("--maximum-k", type=int, default=20)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_n, args.maximum_k),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
