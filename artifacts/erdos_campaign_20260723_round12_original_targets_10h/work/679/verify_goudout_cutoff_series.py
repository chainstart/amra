#!/usr/bin/env python3
"""Finite symbolic QA for the near-critical Goudout cutoff expansion."""

import sympy as sp


t, A, T, a3, a4 = sp.symbols("t A T a3 a4", positive=True)
s = A * T * t - A**2 * T * (T - 1) * t**2 + a3 * t**3 + a4 * t**4

# L=1/t and kappa=A(1-s)/(L+log(1-s)).
q = (1 - s) / (1 + t * sp.log(1 - s))
kappa = A * t * q

# Since T=log L+1-log A, log(1/(A*t))+1=T.
phi = kappa * (T - sp.log(q))
phi_series = sp.series(phi, t, 0, 5).removeO().expand()
excess_series = sp.series(-s + phi, t, 0, 5).removeO().expand()

c3 = A**2 * T * (2 * A * T**2 - 5 * A * T + 2 * A + 2 * T - 2) / 2
c4 = -A**3 * T * (
    6 * A * T**3 - 26 * A * T**2 + 27 * A * T - 6 * A
    + 15 * T**2 - 33 * T + 12
) / 6

assert sp.simplify(phi_series.coeff(t, 1) - A * T) == 0
assert sp.simplify(phi_series.coeff(t, 2) + A**2 * T * (T - 1)) == 0
assert sp.simplify(phi_series.coeff(t, 3) - c3) == 0
assert sp.simplify(excess_series.coeff(t, 3) - (c3 - a3)) == 0
assert sp.LC(sp.Poly(c3, T)) == A**3
assert sp.simplify(excess_series.coeff(t, 4).subs(a3, c3) - (c4 - a4)) == 0
assert sp.LC(sp.Poly(c4, T)) == -A**4

print("PASS: phi L^-1 coefficient = A*T")
print("PASS: phi L^-2 coefficient = -A^2*T*(T-1)")
print("PASS: phi L^-3 coefficient =", sp.factor(c3))
print("PASS: excess L^-3 coefficient = C3-a3")
print("PASS: leading_T(C3) = A^3*T^3 > 0")
print("PASS: at a3=C3, excess L^-4 coefficient = C4-a4")
print("PASS: leading_T(C4) = -A^4*T^4 < 0")
