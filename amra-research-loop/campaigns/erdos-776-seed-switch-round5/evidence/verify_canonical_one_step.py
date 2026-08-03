#!/usr/bin/env python3
"""Exact symbolic replay of the canonical one-step reset inequality."""
import sympy as sp

n, q, Bnext = sp.symbols("n q Bnext", integer=True)
upper = sp.expand(Bnext + (20*n - 52) + 2 - 4*q)
canonical_upper = sp.expand((q - (5*n - 11)) + (20*n - 52) + 2 - 4*q)
assert upper == Bnext + 20*n - 50 - 4*q
assert canonical_upper == -3*q + 15*n - 39
assert sp.expand(canonical_upper.subs(q, 5*n - 13)) == 0
print("canonical one-step reset inequality: PASS")
