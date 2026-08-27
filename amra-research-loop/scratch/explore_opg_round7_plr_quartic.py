#!/usr/bin/env python3
"""Discovery-only exact analysis of the PLR/PRL route chamber."""

from __future__ import annotations

from fractions import Fraction
from math import comb
from pathlib import Path
import sys


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_c_zero_fibre import (  # noqa: E402
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_nonnegative_route_chambers import (  # noqa: E402
    B_EDGE,
    add,
    coefficient,
    multiply,
    scale,
    state_polynomial,
)


def divide_one_minus_variable(poly, slot):
    grouped = {}
    for monomial, value in poly.items():
        key = monomial[:slot] + monomial[slot + 1 :]
        grouped.setdefault(key, {})[monomial[slot]] = value
    quotient = {}
    for key, coefficients in grouped.items():
        degree = max(coefficients)
        previous = Fraction()
        for exponent in range(degree):
            value = coefficients.get(exponent, Fraction()) + previous
            if value:
                monomial = key[:slot] + (exponent,) + key[slot:]
                quotient[monomial] = value
            previous = value
        assert coefficients.get(degree, Fraction()) == -previous
    return quotient


def bernstein_entries(poly, slot, degree):
    power_entries = [coefficient(poly, slot, index) for index in range(degree + 1)]
    return [
        sum_polys(
            scale(power_entries[power], Fraction(comb(index, power), comb(degree, power)))
            for power in range(index + 1)
        )
        for index in range(degree + 1)
    ]


def sum_polys(polys):
    result = {}
    for poly in polys:
        result = add(result, poly)
    return result


def common_monomial(poly):
    return tuple(min(monomial[slot] for monomial in poly) for slot in range(7))


def divide_monomial(poly, divisor):
    return {
        tuple(degree - factor for degree, factor in zip(monomial, divisor)): value
        for monomial, value in poly.items()
    }


def build():
    deletion, connectivity, _, _ = reconstruct_original()
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(
        multiply_original(a_slope, e_zero),
        multiply_original(d_slope, c_zero),
        -1,
    )
    cleared = state_polynomial(delta, tuple("PLR"))
    quotient = divide_one_minus_variable(divide_one_minus_variable(cleared, 4), 6)
    assert max(monomial[4] for monomial in quotient) == 2
    assert max(monomial[6] for monomial in quotient) == 2
    f0, f1, f2 = bernstein_entries(quotient, 4, 2)
    determinant = add(multiply(f0, f2), multiply(f1, f1), -1)
    s_bernstein = bernstein_entries(determinant, 6, 4)
    return delta, cleared, quotient, (f0, f1, f2), determinant, s_bernstein


def main():
    _, cleared, quotient, entries, determinant, s_bernstein = build()
    print("cleared", len(cleared), "quotient", len(quotient))
    print("u entries", [(len(poly), sum(v < 0 for v in poly.values())) for poly in entries])
    print("D", len(determinant), "common", common_monomial(determinant))
    print("D Bernstein", [(len(poly), sum(v < 0 for v in poly.values())) for poly in s_bernstein])
    residual = divide_monomial(determinant, common_monomial(determinant))
    print("D residual", len(residual), "negative", sum(v < 0 for v in residual.values()))


if __name__ == "__main__":
    main()
