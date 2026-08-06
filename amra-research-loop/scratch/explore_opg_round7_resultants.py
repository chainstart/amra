#!/usr/bin/env python3
"""Discovery-only SymPy scan of round-7 q-resultant coordinate walls."""

from __future__ import annotations

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

from verify_q_fibre_ledger import add, multiply, q_coefficients  # noqa: E402
from verify_transverse_expansion import reconstruct  # noqa: E402


NAMES = "abcdeuv"
SYMBOLS = sp.symbols(" ".join(NAMES))


def to_sympy(poly):
    result = sp.Integer(0)
    for monomial, coefficient in poly.items():
        term = sp.Integer(coefficient)
        for symbol, degree in zip(SYMBOLS, monomial):
            term *= symbol**degree
        result += term
    return sp.expand(result)


def main():
    deletion, connectivity, _, _ = reconstruct()
    p0, p1, p2 = q_coefficients(deletion)
    x0, x1, x2 = q_coefficients(connectivity)
    d0 = add(multiply(p2, x0), multiply(x2, p0), -1)
    d1 = add(multiply(p2, x1), multiply(x2, p1), -1)
    d2 = add(multiply(p1, x0), multiply(x1, p0), -1)
    result = add(multiply(d0, d0), multiply(d1, d2), -1)

    u = SYMBOLS[NAMES.index("u")]
    for name, poly in (("D0", d0), ("D1", d1), ("D2", d2), ("Res", result)):
        restricted = to_sympy(poly).subs(u, 0)
        print(f"{name}|u=0 terms={len(sp.Poly(restricted, *SYMBOLS).terms())}")
        print(sp.factor(restricted))


if __name__ == "__main__":
    main()
