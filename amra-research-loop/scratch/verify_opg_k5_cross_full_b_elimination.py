#!/usr/bin/env python3
"""Exploratory full-b determinant computation from the frozen round3 ledger."""
import json
from pathlib import Path
import sympy as sp

source = Path(__file__).parents[1] / "campaigns/opg-1757-k5-cross-round3/evidence/k5_cross_orbit_probe.json"
data = json.loads(source.read_text())["enumeration"]
a,b,c,d,e = sp.symbols("a b c d e")
local = {str(x):x for x in (a,b,c,d,e)}
P = sp.sympify(data["P"], locals=local)
xi = sp.sympify(data["xi"], locals=local)
assert sp.degree(P,b)==sp.degree(xi,b)==1
det = sp.factor(sp.diff(P,b)*xi.subs(b,0)-sp.diff(xi,b)*P.subs(b,0))
R = sp.cancel(det/(2*a**2))
poly = sp.Poly(sp.expand(R),a,c,d,e)
assert poly.total_degree()==10 and len(poly.terms())==41
assert all(coefficient>0 for _,coefficient in poly.terms())
assert sp.expand(det.subs({c:1,d:1,e:1})-2*a**2*(120*a**2+48*a+5)) == 0
assert sp.expand(det.subs({a:1,d:1,e:1})-2*(80*c**2+75*c+18)) == 0
assert sp.expand(det.subs({a:1,c:1,d:1})-2*(44*e**3+94*e**2+32*e+3)) == 0
print("OPG K5-e full-b elimination handoff: PASS")
print("det=2*a^2*R; R total_degree=10 terms=41 all_coefficients_positive")
