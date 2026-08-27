#!/usr/bin/env python3
"""Exact fourth Newton face in the difficult below/v third-root chart."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_third_newton_root import (  # noqa: E402
    ROOT_SLOTS,
    parameterized,
)
from verify_pnl_double_corner_blowup import radial_projective_chart, row  # noqa: E402


def main():
    poly = parameterized("below")
    third_v = radial_projective_chart(poly, ROOT_SLOTS, 6, 1)
    order = min(sum(m[slot] for slot in ROOT_SLOTS) for m in third_v)
    face = {
        monomial: coefficient
        for monomial, coefficient in third_v.items()
        if sum(monomial[slot] for slot in ROOT_SLOTS) == order
    }
    print("third_v", row(third_v), "fourth_order", order, "face", row(face), flush=True)

    symbols = sp.symbols("q y H b v d")
    slots = (0, 2, 4, 5, 6, 7)
    expression = 0
    for monomial, coefficient in face.items():
        term = sp.Rational(coefficient.numerator, coefficient.denominator)
        for symbol, slot in zip(symbols, slots):
            term *= symbol ** monomial[slot]
        expression += term
    factored = sp.factor(expression)
    print("factor", factored, flush=True)
    q, y, _, b, v, _ = symbols
    primitive = sp.cancel(
        factored
        / (
            28
            * (b - 1) ** 2
            * (2 * b + 7) ** 2
            * (4 * b + 7)
            * (y - 1) ** 2
            * (14 * b * y - 36 * b - 14 * y - 63) ** 2
        )
    )
    A = sp.expand(primitive).coeff(q)
    V = sp.expand(primitive).coeff(v)
    print("A", sp.factor(A), flush=True)
    print("A_discriminant_y", sp.factor(sp.discriminant(A, y)), flush=True)
    print("V", sp.factor(V), flush=True)


if __name__ == "__main__":
    main()
