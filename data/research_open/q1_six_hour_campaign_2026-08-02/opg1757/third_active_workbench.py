#!/usr/bin/env python3
"""Exact route-selection workbench for the third active Newton row.

This file deliberately proves nothing by a finite scan.  It has three jobs:

* reconstruct the third forward difference directly from the exact B_p rows;
* verify the stable B6/B4/B2 and B7/B5/B3 reductions coefficientwise;
* falsify simple one-step transport recurrences before they enter a proof.

All arithmetic is exact (``fractions.Fraction`` and integer convolutions).
"""

from __future__ import annotations

import argparse
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Sequence

import sympy as sp


OLD_LANE = (
    Path(__file__).resolve().parents[2]
    / "q1_eight_hour_campaign_2026-07-29"
    / "opg1757"
)
sys.path.insert(0, str(OLD_LANE))

from fixed_page_union_formula import (  # noqa: E402
    b4_bracket_coefficients,
    integer_convolution,
    linear_power,
)
from five_page_union_formula import (  # noqa: E402
    b5_bracket_coefficients,
    combine_polynomials,
    k3_coefficients,
)
from six_page_union_formula import (  # noqa: E402
    b6_bracket_coefficients,
    b6_coefficients,
    k6_coefficients as b6_kernel_coefficients,
)
from seven_page_union_formula import (  # noqa: E402
    b7_bracket_coefficients,
    b7_coefficients,
    k7_coefficients as b7_kernel_coefficients,
)


Number = int | Fraction


def trim(coefficients: Sequence[Number]) -> list[Fraction]:
    result = [Fraction(value) for value in coefficients]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def add(*terms: tuple[Number, Sequence[Number]]) -> list[Fraction]:
    maximum = max(len(coefficients) for _, coefficients in terms)
    return trim(
        [
            sum(
                Fraction(multiplier)
                * (
                    Fraction(coefficients[degree])
                    if degree < len(coefficients)
                    else 0
                )
                for multiplier, coefficients in terms
            )
            for degree in range(maximum)
        ]
    )


def multiply(
    left: Sequence[Number], right: Sequence[Number]
) -> list[Fraction]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += Fraction(x) * Fraction(y)
    return trim(result)


def shifted_power(a: int, b: int, exponent: int) -> list[int]:
    return [
        math.comb(exponent, degree)
        * a ** (exponent - degree)
        * b**degree
        for degree in range(exponent + 1)
    ]


def homogenize(
    coefficients: Sequence[Number], scale: int, degree: int
) -> list[Fraction]:
    """Coefficients of scale**degree P(z/scale)."""

    return [
        Fraction(value) * Fraction(scale, 1) ** (degree - index)
        for index, value in enumerate(coefficients)
    ]


def divide_by_one_plus_z(
    coefficients: Sequence[Number], times: int
) -> list[Fraction]:
    result = trim(coefficients)
    for _ in range(times):
        if len(result) == 1:
            raise AssertionError("zero-degree polynomial is not divisible")
        quotient = [result[0]]
        for degree in range(1, len(result) - 1):
            quotient.append(result[degree] - quotient[-1])
        if quotient[-1] != result[-1]:
            raise AssertionError("claimed (1+z) factor is absent")
        result = trim(quotient)
    return result


def one_plus_z_multiplicity(coefficients: Sequence[Number]) -> int:
    result = trim(coefficients)
    multiplicity = 0
    while len(result) > 1:
        try:
            result = divide_by_one_plus_z(result, 1)
        except AssertionError:
            break
        multiplicity += 1
    return multiplicity


def b2_coefficients(s: int) -> list[int]:
    return [0] * 4 + [
        4 * value
        for value in integer_convolution(
            linear_power(2, 2 * s - 6),
            linear_power(s, 2 * s - 8),
        )
    ]


def b3_reduced_bracket_coefficients(s: int) -> list[int]:
    """J_s/beta**2 in the stable B3 formula, s>=5."""

    if s < 5:
        raise ValueError("the stable B3 bracket starts at s=5")
    bracket = combine_polynomials(
        (
            1,
            integer_convolution(
                linear_power(3, 2 * s - 8), k3_coefficients(s)
            ),
        ),
        (
            -1,
            integer_convolution(
                linear_power(2, 2 * s - 6), linear_power(s, 2)
            ),
        ),
    )
    if bracket[:2] != [0, 0]:
        raise AssertionError("B3 bracket lost its beta**2 factor")
    return bracket[2:]


def b3_coefficients(s: int) -> list[int]:
    if s < 4:
        return [0]
    if s == 4:
        return [0] * 6 + [24]
    reduced = b3_reduced_bracket_coefficients(s)
    bracket = [0, 0] + reduced
    return [0] * 4 + [
        12 * value
        for value in integer_convolution(
            linear_power(s, 2 * s - 10), bracket
        )
    ]


def b4_coefficients(s: int) -> list[int]:
    if s < 4:
        return [0]
    if s == 4:
        return [0]
    if s == 5:
        return [0] * 8 + [2016, 11520, 21600]
    return [0] * 4 + [
        24 * value
        for value in integer_convolution(
            linear_power(s, 2 * s - 12),
            b4_bracket_coefficients(s),
        )
    ]


def b5_coefficients(s: int) -> list[int]:
    if s < 5:
        return [0]
    if s == 5:
        return [0] * 10 + [12000]
    if s == 6:
        return [0] * 10 + [
            260640,
            3744000,
            22187520,
            63866880,
            77760000,
        ]
    return [0] * 4 + [
        40 * value
        for value in integer_convolution(
            linear_power(s, 2 * s - 14),
            b5_bracket_coefficients(s),
        )
    ]


def normalized_c_row(
    q: int, s: int, p: int, b_coefficients: Sequence[int]
) -> list[Fraction]:
    """Return [z^r] C_q(s,z) from an exact B_p coefficient list."""

    row: list[Fraction] = []
    for r in range(2 * q + 1):
        beta_degree = 2 * p + r
        coefficient = (
            b_coefficients[beta_degree]
            if beta_degree < len(b_coefficients)
            else 0
        )
        power = 2 * s - 2 - beta_degree
        row.append(
            Fraction(coefficient, math.factorial(p))
            * Fraction(s, 1) ** power
        )
    return trim(row)


def third_active_row(parity: str, m: int) -> list[Fraction]:
    """Exact Delta^(m+2) row at q=2m+1 (odd) or q=2m (even)."""

    if parity == "odd":
        q = 2 * m + 1
        if m < 0:
            raise ValueError("odd branch requires m>=0")
        specifications = (
            (1, m + 6, 6, b6_coefficients(m + 6)),
            (-(m + 2), m + 5, 4, b4_coefficients(m + 5)),
            (
                math.comb(m + 2, 2),
                m + 4,
                2,
                b2_coefficients(m + 4),
            ),
        )
    elif parity == "even":
        q = 2 * m
        if m < 1:
            raise ValueError("the third active even row requires m>=1")
        specifications = (
            (1, m + 6, 7, b7_coefficients(m + 6)),
            (-(m + 2), m + 5, 5, b5_coefficients(m + 5)),
            (
                math.comb(m + 2, 2),
                m + 4,
                3,
                b3_coefficients(m + 4),
            ),
        )
    else:
        raise ValueError("parity must be 'odd' or 'even'")
    return add(
        *(
            (
                multiplier,
                normalized_c_row(q, s, p, coefficients),
            )
            for multiplier, s, p, coefficients in specifications
        )
    )


def stable_odd_reduced_formula(s: int) -> list[Fraction]:
    """Odd third row after its maximal (1+z)^(2s-16) factor, s>=8."""

    if s < 8:
        raise ValueError("stable odd formula starts at s=8")
    f6 = b6_bracket_coefficients(s)
    if f6[:8] != [0] * 8:
        raise AssertionError("B6 bracket lost its beta**8 factor")
    p6 = f6[8:]
    f4 = b4_bracket_coefficients(s - 1)
    if f4[:4] != [0] * 4:
        raise AssertionError("B4 bracket lost its beta**4 factor")
    p4 = f4[4:]
    top = homogenize(p6, s, 2 * s - 14)
    middle = multiply(
        homogenize(p4, s - 1, 2 * s - 12), shifted_power(1, 1, 2)
    )
    bottom = multiply(
        shifted_power(s - 2, 2, 2 * s - 10),
        shifted_power(1, 1, 4),
    )
    return add(
        (Fraction(1, 12), top),
        (-(s - 4), middle),
        ((s - 4) * (s - 5), bottom),
    )


def stable_even_reduced_formula(s: int) -> list[Fraction]:
    """Even third row after its maximal (1+z)^(2s-18) factor, s>=9."""

    if s < 9:
        raise ValueError("stable even formula starts at s=9")
    f7 = b7_bracket_coefficients(s)
    if f7[:10] != [0] * 10:
        raise AssertionError("B7 bracket lost its beta**10 factor")
    p7 = f7[10:]
    f5 = b5_bracket_coefficients(s - 1)
    if f5[:6] != [0] * 6:
        raise AssertionError("B5 bracket lost its beta**6 factor")
    p5 = f5[6:]
    p3 = b3_reduced_bracket_coefficients(s - 2)
    top = homogenize(p7, s, 2 * s - 16)
    middle = multiply(
        homogenize(p5, s - 1, 2 * s - 14), shifted_power(1, 1, 2)
    )
    bottom = multiply(
        homogenize(p3, s - 2, 2 * s - 12), shifted_power(1, 1, 4)
    )
    return add(
        (Fraction(1, 60), top),
        (Fraction(-(s - 4), 3), middle),
        ((s - 4) * (s - 5), bottom),
    )


def verify_symbolic_maximal_factor_certificates() -> tuple[sp.Expr, sp.Expr]:
    """Prove symbolically that the displayed (1+z) factors are maximal."""

    s = sp.symbols("s", integer=True, positive=True)
    k6_value = sum(
        coefficient * (-sp.S.One / s) ** degree
        for degree, coefficient in enumerate(b6_kernel_coefficients(s))
    )
    k7_value = sum(
        coefficient * (-sp.S.One / s) ** degree
        for degree, coefficient in enumerate(b7_kernel_coefficients(s))
    )
    expected6 = (
        (s - 7)
        * (s - 6)
        * (s - 5) ** 2
        * (s - 4) ** 2
        * (s - 3)
        * (s - 2)
        / s**8
    )
    expected7 = (
        (s - 8)
        * (s - 7)
        * (s - 6) ** 2
        * (s - 5) ** 2
        * (s - 4) ** 2
        * (s - 3)
        * (s - 2)
        / s**10
    )
    if sp.factor(k6_value - expected6) != 0:
        raise AssertionError("K6(-1/s) maximal-factor identity failed")
    if sp.factor(k7_value - expected7) != 0:
        raise AssertionError("K7(-1/s) maximal-factor identity failed")
    return sp.factor(expected6), sp.factor(expected7)


def reduced_third_row(parity: str, m: int) -> list[Fraction]:
    row = third_active_row(parity, m)
    s = m + 6
    exponent = 2 * s - (16 if parity == "odd" else 18)
    return divide_by_one_plus_z(row, max(0, exponent))


def first_nonpositive(
    coefficients: Sequence[Number], strict: bool = True
) -> tuple[int, Fraction] | None:
    for degree, value in enumerate(coefficients):
        exact = Fraction(value)
        if exact < 0 or (strict and exact == 0):
            return degree, exact
    return None


def transport_remainder(parity: str, s: int) -> list[Fraction]:
    """Test H_(s+1)-(s+kz)^2 H_s, k=6 or 7."""

    m = s - 6
    current = reduced_third_row(parity, m)
    following = reduced_third_row(parity, m + 1)
    page = 6 if parity == "odd" else 7
    return add((1, following), (-1, multiply(shifted_power(s, page, 2), current)))


def assert_stable_reductions(maximum_m: int) -> tuple[int, int]:
    odd_checks = 0
    even_checks = 0
    for m in range(2, maximum_m + 1):
        s = m + 6
        direct = reduced_third_row("odd", m)
        formula = stable_odd_reduced_formula(s)
        if direct != formula:
            raise AssertionError(f"stable odd reduction failed at m={m}")
        odd_checks += len(direct)
    for m in range(3, maximum_m + 1):
        s = m + 6
        direct = reduced_third_row("even", m)
        formula = stable_even_reduced_formula(s)
        if direct != formula:
            raise AssertionError(f"stable even reduction failed at m={m}")
        even_checks += len(direct)
    return odd_checks, even_checks


def scan(maximum_m: int) -> dict[str, object]:
    reductions = assert_stable_reductions(maximum_m)
    result: dict[str, object] = {
        "status": "FINITE ROUTE-SELECTION ONLY",
        "maximum_m": maximum_m,
        "stable_reduction_coefficients_checked": {
            "odd": reductions[0],
            "even": reductions[1],
        },
    }
    for parity, minimum in (("odd", 0), ("even", 1)):
        first_row_failure = None
        first_transport_failure = None
        row_count = 0
        transport_count = 0
        multiplicities: list[tuple[int, int]] = []
        for m in range(minimum, maximum_m + 1):
            row = third_active_row(parity, m)
            row_count += len(row)
            multiplicities.append((m, one_plus_z_multiplicity(row)))
            failure = first_nonpositive(row)
            if failure is not None and first_row_failure is None:
                first_row_failure = (m, *failure)
        first_stable_s = 8 if parity == "odd" else 9
        for s in range(first_stable_s, maximum_m + 6):
            remainder = transport_remainder(parity, s)
            transport_count += len(remainder)
            failure = first_nonpositive(remainder, strict=True)
            if failure is not None and first_transport_failure is None:
                first_transport_failure = (s, *failure)
        result[parity] = {
            "row_coefficients_checked": row_count,
            "first_nonpositive_row_coefficient": first_row_failure,
            "one_plus_z_multiplicities": multiplicities,
            "transport_coefficients_checked": transport_count,
            "first_nonpositive_transport_coefficient": first_transport_failure,
        }
    return result


def format_value(value: object) -> str:
    if isinstance(value, Fraction):
        return str(value)
    return repr(value)


def print_nested(mapping: dict[str, object], prefix: str = "") -> None:
    for key, value in mapping.items():
        if isinstance(value, dict):
            print(f"{prefix}{key}:")
            print_nested(value, prefix + "  ")
        else:
            print(f"{prefix}{key}: {format_value(value)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-m", type=int, default=30)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.maximum_m < 3:
        raise SystemExit("--maximum-m must be at least 3")
    print_nested(scan(args.maximum_m))


if __name__ == "__main__":
    main()
