#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

old = Path(__file__).parents[2] / "opg-1757-mechanism-reset" / "evidence" / "w4_garding_orbit_probe.json"
data = json.loads(old.read_text())["rim_orbit"]
a, b, c, d, t = sp.symbols("a b c d t")
P = sp.sympify(data["C_delete"])
Q = sp.sympify(data["xi"])
point = [sp.Rational(-33, 20), sp.Rational(-13, 25), sp.Rational(9, 2), sp.Rational(69, 10)]
at = dict(zip((a, b, c, d), point))
assert P.subs(at) == sp.Rational(161582787, 5000000)
assert Q.subs(at) == sp.Rational(-346833, 500000)
path = dict(zip((a, b, c, d), [1 + (x - 1) * t for x in point]))
poly = sp.Poly(sp.expand(5000000 * P.subs(path)), t)
assert poly.count_roots(0, 1) == 2
print("pass: endpoint signs exact; straight path has two roots in (0,1)")
