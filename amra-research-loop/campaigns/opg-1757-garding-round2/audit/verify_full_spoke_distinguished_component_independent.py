#!/usr/bin/env python3
"""Blind reconstruction of the W4 marked-spoke component certificate."""

from itertools import combinations
import json
import sympy as sp


a, b, c, d = sp.symbols("a b c d")
x, y, z, w, r = sp.symbols("x y z w r", positive=True)

# W4 has centre 0, rim 1-2-3-4-1, and marked spoke 01 is deleted.
# This edge list and its orbit labels are reconstructed directly from the
# stabilizer of 01; no author polynomial is imported.
edges = (
    (0, 2, a), (0, 3, b), (0, 4, a),
    (1, 2, c), (2, 3, d), (3, 4, d), (4, 1, c),
)


def classify(selected):
    parent = list(range(5))

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for index in selected:
        u, v, _ = edges[index]
        ru, rv = root(u), root(v)
        if ru == rv:
            return None
        parent[ru] = rv
    selected_set = set(selected)
    # The C-polynomial uses the complement-of-forest monomial.
    monomial = sp.prod(label for index, (_, _, label) in enumerate(edges)
                       if index not in selected_set)
    return sp.expand(monomial), root(0) == root(1)


P = sp.Integer(0)
Q = sp.Integer(0)
forest_count = connected_count = 0
for size in range(8):
    for selected in combinations(range(7), size):
        result = classify(selected)
        if result is None:
            continue
        monomial, connected = result
        forest_count += 1
        P += monomial
        if connected:
            connected_count += 1
            Q += monomial

P = sp.expand(P)
Q = sp.expand(Q)
assert forest_count == 86 and connected_count == 38
assert P.subs({a: 1, b: 1, c: 1, d: 1}) == 86
assert Q.subs({a: 1, b: 1, c: 1, d: 1}) == 38

shift = {a: x - 1, b: y - 1, c: z - 1, d: w - 1}
Ps = sp.expand(P.subs(shift))
Qs = sp.expand(Q.subs(shift))

# Recover the fibre coefficients from the reconstructed polynomials rather
# than copying them into the calculation.
Pz = sp.Poly(Ps, z)
Qz = sp.Poly(Qs, z)
assert Pz.degree() == 2 and Pz.coeff_monomial(z) == 0
assert Qz.degree() == 1
A = sp.factor(Pz.coeff_monomial(z**2))
H = sp.factor(-Pz.coeff_monomial(1))
C = sp.factor(Qz.coeff_monomial(z))
E = sp.factor(Qz.coeff_monomial(1))
assert A == (w*x - 1)*(w*x*y + y - 2)

J = sp.factor((H*C**2 - A*E**2) /
              (4*(w - 1)**2*(x - 1)**4*(y - 1)**2))
assert J == w**2*y + 2*w*x + 2*w*y - 4*w + y - 2
assert sp.expand(H*C**2 - A*E**2 -
                 4*(w - 1)**2*(x - 1)**4*(y - 1)**2*J) == 0

# Independent boundary reductions for the two base walls.
Jr = sp.factor(J.subs(x, r/w))
Cr = sp.factor((C/2).subs(x, r/w))
y0 = 2/(r + 1)
assert sp.factor(Jr.subs(y, y0)) == 2*(r-w)**2/(r+1)
assert sp.factor(Cr.subs(y, y0)) == (r-1)*(r-w)**2/(w*(r+1))
assert sp.factor(sp.diff(Jr, y)) == (w+1)**2
assert sp.factor(sp.diff(Cr, y) - (r*(w**2+1)-2*w)/w) == 0
assert sp.factor((r*(w**2+1)-2*w) - (w-1)**2) == (r-1)*(w**2+1)

Hr = sp.factor(H.subs(w, 1/x))
assert sp.factor(Hr - (x-1)**2*(y*(x+1)**2-4*x)/x**2) == 0
Hy = sp.factor(H.subs(y, 2/(w*x+1)))
assert sp.factor(Hy - 2*(w-1)**2*(x-1)**2/(w*x+1)) == 0
assert sp.factor(H.subs(w, 1) - A.subs(w, 1)) == 0
assert sp.factor(H.subs(x, 1) - A.subs(x, 1)) == 0
assert sp.factor(H.subs(y, 1) - (w+x-2)**2) == 0

print(json.dumps({
    "schema": "amra.opg1757.full-w4-spoke-independent-audit.v1",
    "reconstruction": {
        "forest_count": forest_count,
        "endpoint_connected_forest_count": connected_count,
        "P_at_anchor": 86,
        "xi_at_anchor": 38
    },
    "fibre": {
        "P": "A*z^2-H",
        "xi": "C*z+E",
        "A": str(A),
        "H": str(H),
        "C": str(C),
        "E": str(E),
        "J": str(J),
        "identity_verified": True
    },
    "wall_reductions_verified": True,
    "scope": "W4 marked-spoke four-stabilizer-variable component only",
    "public_problem_closed": False
}, indent=2, sort_keys=True))
