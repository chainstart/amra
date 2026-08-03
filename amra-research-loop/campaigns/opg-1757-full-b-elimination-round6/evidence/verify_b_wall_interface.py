#!/usr/bin/env python3
"""Exact codimension-one interface after eliminating the singleton b.

This verifier deliberately proves only wall identities.  It does not infer
that two points belong to the same component from a floating-point path.
"""
import json
from pathlib import Path

import sympy as sp


source = (
    Path(__file__).parents[2]
    / "opg-1757-k5-cross-round3/evidence/k5_cross_orbit_probe.json"
)
data = json.loads(source.read_text())["enumeration"]
a, b, c, d, e, t = sp.symbols("a b c d e t")
local = {str(x): x for x in (a, b, c, d, e)}
P = sp.sympify(data["P"], locals=local)
xi = sp.sympify(data["xi"], locals=local)
A, C = sp.diff(P, b), P.subs(b, 0)
D, E = sp.diff(xi, b), xi.subs(b, 0)
Ac, A0 = sp.diff(A, c), A.subs(c, 0)
Cc, C0 = sp.diff(C, c), C.subs(c, 0)
Dc, D0 = sp.diff(D, c), D.subs(c, 0)

# On the generic A=0 sheet c=-A0/Ac.  The numerators below give C and D.
C_wall_numerator = sp.factor(C0 * Ac - Cc * A0)
D_wall_numerator = sp.factor(D0 * Ac - Dc * A0)
assert C_wall_numerator == (
    -2 * a**2 * d**2 * e**2 * (d + 2) ** 2 * (a * e + a + e)
)
assert D_wall_numerator == (
    2 * a**2 * d**2 * e**2 * (e + 2) ** 2 * (a * d + a + d)
)
assert sp.factor(sp.resultant(A, C, c)) == C_wall_numerator
assert sp.factor(sp.resultant(A, D, c)) == D_wall_numerator

# A rational ray illustrates why sampled continuation is unsafe.  Before the
# first robust, C-positive A crossing, it has two very close A crossings with
# C<0.  They are genuine projection barriers for P=A*b+C>0.
start = (sp.Integer(1),) * 4
far = (
    sp.Rational(-1983, 100),
    sp.Rational(-1973, 100),
    sp.Rational(-207, 50),
    sp.Rational(-479, 25),
)
base_vars = (a, c, d, e)
ray = {v: x + t * (y - x) for v, x, y in zip(base_vars, start, far)}
A_ray = sp.Poly(sp.expand(A.subs(ray)), t, domain=sp.QQ)
C_ray = sp.Poly(sp.expand(C.subs(ray)), t, domain=sp.QQ)
window = sp.Rational(3, 20)
assert sp.count_roots(A_ray, 0, window) == 3
isolated = [
    interval
    for interval, multiplicity in sp.intervals(A_ray, eps=sp.Rational(1, 10) ** 25)
    if interval[0] >= 0 and interval[1] <= window
]
assert len(isolated) == 3
wall_C_signs = []
for lo, hi in isolated:
    clo, chi = C_ray.eval(lo), C_ray.eval(hi)
    assert clo * chi > 0
    wall_C_signs.append(1 if clo > 0 else -1)
assert wall_C_signs == [-1, -1, 1]

print("full-b wall interface: PASS")
print("generic A=0 crossing signs reduce to Ac, ae+a+e, and ad+a+d")
print("exact rational ray A-wall C signs:", wall_C_signs)
print("this wall replay infers no path membership; fixed-space domination is proved separately, global OPG-1757 remains OPEN")
