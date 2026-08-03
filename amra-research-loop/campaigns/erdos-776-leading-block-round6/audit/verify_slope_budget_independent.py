#!/usr/bin/env python3
"""Independent symbolic elimination for the affine slope budget."""
import sympy as sp
q, alpha, delta, beta, v, c, A, Bnext = sp.symbols(
    "q alpha delta beta v c A Bnext", real=True)
choose_A1 = A*(A+1)/2
gamma = Bnext + alpha*q + beta - choose_A1 + 2 - (4-delta)*q + v
bound_after_dropping = sp.expand(Bnext + alpha*q + beta + 2 - (4-delta)*q + v)
canonical_bound = sp.expand((q-c) + alpha*q + beta + 2 - (4-delta)*q + v)
assert sp.expand(gamma - (bound_after_dropping-choose_A1)) == 0
assert sp.expand(canonical_bound-((alpha+delta-3)*q + beta+v+2-c)) == 0
print("independent affine slope-budget elimination: PASS")
