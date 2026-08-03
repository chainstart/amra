#!/usr/bin/env python3
"""Exact reconstruction for the triangular-prism triangle-edge routing."""
from itertools import combinations
import sympy as s

u = s.symbols("u0:5")
x, y, z = s.symbols("x y z")
marked = (0, 1)
all_edges = ((0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5))
orbits = (
    {(0,2),(1,2)}, {(3,4)}, {(3,5),(4,5)},
    {(0,3),(1,4)}, {(2,5)},
)

def edge_key(e):
    return tuple(sorted(e))

def label(e):
    e = edge_key(e)
    for i, orbit in enumerate(orbits):
        if e in {edge_key(q) for q in orbit}:
            return u[i]
    raise AssertionError(e)

edges = tuple((a,b,label((a,b))) for a,b in all_edges
              if edge_key((a,b)) != marked)
P = s.Integer(0)
Q = s.Integer(0)
nf = nc = 0
for size in range(9):
    for selected in combinations(range(8), size):
        parent = list(range(6))
        def root(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        ok = True
        for i in selected:
            a, b, _ = edges[i]
            ra, rb = root(a), root(b)
            if ra == rb:
                ok = False
                break
            parent[ra] = rb
        if not ok:
            continue
        nf += 1
        chosen = set(selected)
        monomial = s.prod(v for i,(_,_,v) in enumerate(edges) if i not in chosen)
        P += monomial
        if root(0) == root(1):
            nc += 1
            Q += monomial

P, Q = s.expand(P), s.expand(Q)
assert (nf, nc) == (190, 66)
assert (len(s.Poly(P, *u).terms()), len(s.Poly(Q, *u).terms())) == (79, 35)
subs = {u[0]:x-1, u[2]:x-1, u[1]:y-1, u[4]:y-1, u[3]:z-1}
Ps, Qs = s.expand(P.subs(subs)), s.expand(Q.subs(subs))
P_expected = x**4*y**2*z**2-x**2*y*z**2-2*x**2*y*z-x**2*y-2*x**2*z+4*x*z+4*x-y**2+4*y-6
Q_expected = x**4*y+x**2*y**2*z**2+x**2*y**2+2*x**2*y*z-4*x**2*y+2*x**2*z-8*x**2-4*x*y*z-4*x*y-8*x*z+24*x-2*y**2-y*z**2+10*y+8*z-18
assert s.expand(Ps-P_expected) == 0
assert s.expand(Qs-Q_expected) == 0
assert Ps.subs({x:2,y:2,z:2}) == 190
assert Qs.subs({x:2,y:2,z:2}) == 66
assert Ps.subs({x:s.Rational(3,2),y:s.Rational(1,2),z:1}) == s.Rational(1,64)
assert Qs.subs({x:s.Rational(3,2),y:s.Rational(1,2),z:1}) == -s.Rational(3,32)
R = s.factor(s.resultant(Ps, Qs, x))
known = y**2*(y-1)**4*(z-1)**2*(y*z+y-2)**2
residual = s.cancel(R/known)
assert s.rem(R, known, y) == 0
assert s.Poly(R, y, z).total_degree() == 28
assert len(s.Poly(R, y, z).terms()) == 166
assert s.Poly(residual, y, z).total_degree() == 16
assert len(s.Poly(residual, y, z).terms()) == 52
assert s.factor(Ps.subs(z,1)).has(x-1)
assert s.factor(Qs.subs(z,1)).has(x-1)
print("prism triangle-edge routing: PASS (190/66; resultant 28/166, residual 16/52)")
