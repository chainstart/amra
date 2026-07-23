#!/usr/bin/env python3
"""Symbolic QA for the critical-constant far-cutoff expansion."""

import sympy as sp


t, M, c = sp.symbols("t M c", positive=True)

# t=1/L.  After the exact leading cancellation, if
# log(C_X/C_0)=q*D*M/L, then S/D is the expression below.
def reduced_excess(q):
    a = (M + c + q * M * t) * t
    return q * M * t - sp.log(1 + a)


at_equality = sp.series(reduced_excess(0), t, 0, 3)
moving = sp.series(reduced_excess(3), t, 0, 3)

eq_poly = at_equality.removeO().expand()
moving_poly = moving.removeO().expand()

assert sp.simplify(eq_poly.coeff(t, 1) + M + c) == 0
assert sp.simplify(moving_poly.coeff(t, 1) - (2 * M - c)) == 0

print("PASS: literal C=C0 has S/D =", at_equality)
print("PASS: C_X/C0=exp(3*D*M/L) has S/D =", moving)
print("PASS: leading signs are negative at equality and positive for moving C_X")
