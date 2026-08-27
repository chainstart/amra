#!/usr/bin/env python3
"""Discovery-only factor scan for the OPG-1757 round-7 coordinate walls.

This script is intentionally not evidence: it uses SymPy to discover small
factorizations.  Any retained identity must be replayed by a standard-library
verifier before it is cited by the campaign.
"""

from __future__ import annotations

from itertools import combinations
import os
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

from verify_falsification_witnesses import EDGES, reconstruct_complements  # noqa: E402


NAMES = ("x01", "x02", "b", "c", "x13", "x14", "x23", "x24")
SYMBOLS = sp.symbols(" ".join(NAMES))
SYMBOL_BY_EDGE = dict(zip(EDGES, SYMBOLS))


def derivative_polynomial(complements, differentiated):
    differentiated = frozenset(differentiated)
    total = sp.Integer(0)
    for complement in complements:
        if not differentiated.issubset(complement):
            continue
        term = sp.Integer(1)
        for edge in complement:
            if edge not in differentiated:
                term *= SYMBOL_BY_EDGE[edge]
        total += term
    return sp.expand(total)


def main():
    deletion, connectivity = reconstruct_complements()
    c = SYMBOL_BY_EDGE[(1, 2)]
    p_wall = derivative_polynomial(deletion, ()).subs(c, 0)
    xi_wall = derivative_polynomial(connectivity, ()).subs(c, 0)
    print(f"P|c=0 :: {sp.factor(p_wall)}")
    print(f"xi|c=0 :: {sp.factor(xi_wall)}")
    print()
    full_scan = os.environ.get("AMRA_FULL_DERIVATIVES") == "1"
    rows = []
    for size in range(len(EDGES) + 1):
        for differentiated in combinations(EDGES, size):
            polynomial = derivative_polynomial(deletion, differentiated)
            restricted = sp.expand(polynomial if full_scan else polynomial.subs(c, 0))
            if restricted == 0:
                continue
            factored = sp.factor(restricted)
            terms = len(sp.Poly(restricted, *SYMBOLS).terms())
            if (factored != restricted or terms <= 5) and (not full_scan or size >= 3):
                rows.append((size, differentiated, terms, factored))

    rows.sort(key=lambda row: (row[2], -row[0], row[1]))
    for size, differentiated, terms, factored in rows:
        labels = ",".join(NAMES[EDGES.index(edge)] for edge in differentiated)
        print(f"order={size} terms={terms} d=[{labels}] :: {factored}")


if __name__ == "__main__":
    main()
