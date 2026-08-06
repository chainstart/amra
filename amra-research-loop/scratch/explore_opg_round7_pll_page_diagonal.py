#!/usr/bin/env python3
"""Discovery-only nonshared-page diagonal scan in the c<0 PLL chamber."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys

import sympy as sp


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
from verify_negative_c_direct_chambers import bernstein_transform  # noqa: E402
from verify_negative_c_schur_endpoint import (  # noqa: E402
    schur_substitute,
    uniform_state_polynomial,
)


B_EDGE = (0, 4)


def merge_nonshared_pages(poly):
    result = {}
    for monomial, value in poly.items():
        merged = list(monomial)
        merged[3] += merged[5]
        merged[4] += merged[6]
        merged[5] = 0
        merged[6] = 0
        merged = tuple(merged)
        result[merged] = result.get(merged, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def row(poly):
    values = tuple(poly.values())
    return {
        "terms": len(poly),
        "positive": sum(value > 0 for value in values),
        "negative": sum(value < 0 for value in values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
    }


def main():
    deletion, connectivity, _, _ = reconstruct_original()
    A = derivative(deletion, (B_EDGE,))
    C = restrict_original_zero(deletion, B_EDGE)
    D = derivative(connectivity, (B_EDGE,))
    E = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(multiply_original(A, E), multiply_original(D, C), -1)
    F = schur_substitute(uniform_state_polynomial(delta, tuple("PLL")))
    diagonal = merge_nonshared_pages(F)
    transformed = bernstein_transform(diagonal, [2, 4, 7])
    print({
        "raw": row(F),
        "page_diagonal": row(diagonal),
        "page_diagonal_bernstein": row(transformed),
    }, flush=True)
    symbols = sp.symbols("c q0 s0 q t q4 t4 tau")
    expression = sum(
        sp.Rational(value.numerator, value.denominator)
        * sp.prod(symbol ** exponent for symbol, exponent in zip(symbols, monomial))
        for monomial, value in diagonal.items()
    )
    print("factor", sp.factor(expression), flush=True)


if __name__ == "__main__":
    main()
