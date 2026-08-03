#!/usr/bin/env python3
"""Exact rejection of the last numerical projection-lift path candidate."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
data = json.loads(
    (ROOT / "opg-1757-k5-cross-round3/evidence/k5_cross_orbit_probe.json").read_text()
)["enumeration"]

a, b, c, d, e, t = sp.symbols("a b c d e t")
base = (a, c, d, e)
P = sp.sympify(data["P"], locals={v.name: v for v in (a, b, c, d, e)})
A = sp.diff(P, b)
C = P.subs(b, 0)
M = sp.Integer(10) ** 6

points = [
    (sp.Integer(1), sp.Integer(1), sp.Integer(1), sp.Integer(1)),
    (sp.Integer(1), sp.Rational(-7, 4), sp.Integer(2), sp.Rational(7, 8)),
    (sp.Rational(-3, 5), sp.Rational(-41, 10), sp.Rational(4, 5), sp.Rational(-5, 2)),
    (sp.Rational(-7, 5), sp.Integer(-5), sp.Integer(-3), sp.Integer(-5)),
]

certificate = []
for index, (left, right) in enumerate(zip(points, points[1:]), start=1):
    substitution = {
        variable: left[i] + t * (right[i] - left[i])
        for i, variable in enumerate(base)
    }
    At = sp.expand(A.subs(substitution))
    Ct = sp.expand(C.subs(substitution))
    Qt = sp.Poly(sp.expand(M * At**2 + Ct), t, domain=sp.QQ)
    roots = Qt.count_roots(0, 1)
    endpoints = (Qt.eval(0), Qt.eval(1))

    # The proposed lift is b(t)=M*A(t), hence P=Q exactly.
    assert sp.expand(P.subs({**substitution, b: M * At}) - Qt.as_expr()) == 0
    certificate.append(
        {
            "segment": index,
            "degree": Qt.degree(),
            "roots_in_open_unit_interval": int(roots),
            "left_value": str(endpoints[0]),
            "right_value": str(endpoints[1]),
        }
    )

# The first segment has positive endpoints but two exact interior zeros.
# Therefore the lifted path meets P=0 and cannot certify component membership.
assert certificate[0]["roots_in_open_unit_interval"] == 2
assert sp.Rational(certificate[0]["left_value"]) > 0
assert sp.Rational(certificate[0]["right_value"]) > 0

print(json.dumps({
    "schema": "amra.opg1757.round6.rejected-projection-path.v1",
    "verdict": "REJECTED",
    "reason": "the first lifted segment contains two exact P=0 roots",
    "segments": certificate,
    "component_membership": "OPEN",
}, indent=2))
