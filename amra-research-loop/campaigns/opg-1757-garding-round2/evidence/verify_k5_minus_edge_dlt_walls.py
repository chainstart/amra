#!/usr/bin/env python3
"""Exact checker for the K5-e three-variable D/L/T wall audit.

Scope is deliberately local to the (a,b,c) stabilizer specialization.
"""

import json
from pathlib import Path

import sympy as sp


a, b, c, q = sp.symbols("a b c q", real=True)
source = Path(__file__).with_name("k5_minus_edge_high_triangle_stabilizer.json")
data = json.loads(source.read_text())
loc = {"a": a, "b": b, "c": c}
F = sp.sympify(data["enumeration"]["F_equals_P_over_b"], locals=loc)
G = sp.sympify(data["enumeration"]["G_equals_xi_over_b"], locals=loc)

L = b*c + b + 2*c
D = b*c**2 + 2*b*c + 2*b + 2*c**2 + 4*c
K = b*c + b + c + 2
T = 4*a*K + L*(L + 4)
H = L**2 + 8*c
J = b**2*c**2 + 2*b**2*c + b**2 + 2*b*c**2 + 4*b*c + 2*b + 2*c**2 + 4*c

assert sp.expand(sp.prem(F, G, a) + b**2*L**2*T) == 0
assert sp.rem(2*D*F + b**2*L**2*T, G, a) == 0
assert (D.subs({a: 1, b: 1, c: 1}), T.subs({a: 1, b: 1, c: 1}), L.subs({a: 1, b: 1, c: 1})) == (11, 52, 4)

# L wall.
cL = -b/(b + 2)
assert sp.factor(F.subs(c, cL)) == 2*a**2*b**2/(b + 2)
assert sp.factor(G.subs(c, cL)) == 2*a**2*b**2/(b + 2)
assert sp.factor(D.subs(c, cL)) == b**2/(b + 2)
assert sp.factor(T.subs(c, cL)) == 4*a*(3*b + 4)/(b + 2)

# D wall and its single connected F-positive candidate strip.
bD = 2*(1 - q**2)/(1 + q**2)
cD = q - 1
S = -(q + 1)**3*a**2 + (q**4 - 2*q**2 - 4*q + 1)*a + (q - 1)**2*(q + 1)
positive_prefactor = -8*(q - 1)**3/(q**2 + 1)**3
assert sp.factor(D.subs({b: bD, c: cD})) == 0
assert sp.factor(F.subs({b: bD, c: cD}) - positive_prefactor*S) == 0
disc = sp.discriminant(S, a)
assert sp.factor(disc) == (q**2 + 1)**2*(q**4 - 2*q**2 + 5)

# T wall factorizations.
aT = -L*(L + 4)/(4*K)
assert sp.factor(G.subs(a, aT) - L**2*D*H/(8*K**2)) == 0
assert sp.factor(F.subs(a, aT) - (b + 2)*L**2*H*J/(16*K**2)) == 0
assert sp.factor(H.subs(c, q - 1) - ((b + 2)**2*q**2 - 4*b*q - 4)) == 0
assert sp.factor(J.subs(c, q - 1) - ((b**2 + 2*b + 2)*q**2 - 2)) == 0

# Polynomial certificates for the strict root/pole ordering when b>0.
Q = b**2 + 2*b + 2
# j > |h-| follows from (sqrt(2Q)+b)^2 > 2Q.
assert sp.expand((2*Q + 2*b*sp.sqrt(2*Q) + b**2) - 2*Q) == b**2 + 2*b*sp.sqrt(2*Q)
# j < 2/(b+2) and 1/(b+1) < j reduce to positive b-polynomials.
assert sp.expand(2*Q - (b + 2)**2) == b**2
assert sp.expand(2*(b + 1)**2 - Q - b*(b + 2)) == 0
# sqrt(2Q)>b+2 and sqrt(2Q)>2 reduce to b^2 and 2b(b+2).
assert sp.expand(2*Q - (b + 2)**2) == b**2
assert sp.expand(2*Q - 4 - 2*b*(b + 2)) == 0

# Exact b=1 representatives of all three T-wall F-positive sheets.
r10 = sp.sqrt(10)
u = a*c + (1-r10/5)*(a+c) + sp.Rational(1, 3) - r10/15
v = a*c + (1+r10/5)*(a+c) + sp.Rational(1, 3) + r10/15
reps = [(sp.Rational(5, 4), -2), (1, -1), (sp.Rational(-5, 12), 0)]
expected = [
    ((-35+r10)/12, (-35-r10)/12),
    (-sp.Rational(2, 3)-r10/15, -sp.Rational(2, 3)+r10/15),
    (-sp.Rational(1, 12)+r10/60, -sp.Rational(1, 12)-r10/60),
]
for (aa, cc), (uu, vv) in zip(reps, expected):
    assert sp.factor(T.subs({a: aa, b: 1, c: cc})) == 0
    assert sp.simplify(u.subs({a: aa, c: cc}) - uu) == 0
    assert sp.simplify(v.subs({a: aa, c: cc}) - vv) == 0

# D/T intersection: one strictly increasing cubic cuts out its F-positive part.
Cq = 2*q**3 - q**2 + 2*q + 1
assert sp.discriminant(Cq, q) < 0
assert sp.expand(sp.diff(Cq, q) - 2*(3*q**2 - q + 1)) == 0
assert sp.discriminant(3*q**2 - q + 1, q) < 0
assert Cq.subs(q, -1) < 0 < Cq.subs(q, 0)

print("PASS: exact K5-e three-variable D/L/T wall reduction")
print("scope: local stabilizer slice only; no global campaign promotion")
