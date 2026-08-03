#!/usr/bin/env python3
"""Independent verifier for the K5-e upper-root theorem.

This script does not import or execute the author verifier.  Forests are
recognized by incidence-matrix rank, independently of its union-find route.
"""

from itertools import combinations

import sympy as sp


vertices = range(5)
marked = (0, 1)
host = [e for e in combinations(vertices, 2) if e != (3, 4)]
edges = [e for e in host if e != marked]
orbit_a = {(0, 2), (1, 2)}
orbit_b = {(0, 3), (0, 4), (1, 3), (1, 4)}
orbit_c = {(2, 3), (2, 4)}


def incidence_rank(selected):
    matrix = sp.zeros(4, len(selected))
    for col, (u, v) in enumerate(selected):
        if u < 4:
            matrix[u, col] = 1
        if v < 4:
            matrix[v, col] = -1
    return matrix.rank()


def endpoints_connected(selected):
    adjacent = {v: set() for v in vertices}
    for u, v in selected:
        adjacent[u].add(v)
        adjacent[v].add(u)
    reached = {marked[0]}
    frontier = [marked[0]]
    while frontier:
        u = frontier.pop()
        for v in adjacent[u] - reached:
            reached.add(v)
            frontier.append(v)
    return marked[1] in reached


aa, bb, cc = sp.symbols("aa bb cc", real=True)
P = 0
XI = 0
forest_count = 0
connected_count = 0
for mask in range(1 << len(edges)):
    selected = [edges[i] for i in range(len(edges)) if mask & (1 << i)]
    if incidence_rank(selected) != len(selected):
        continue
    forest_count += 1
    complement = set(edges) - set(selected)
    monomial = aa**len(complement & orbit_a) * bb**len(complement & orbit_b) * cc**len(complement & orbit_c)
    P += monomial
    if endpoints_connected(selected):
        connected_count += 1
        XI += monomial

assert (forest_count, connected_count) == (134, 70)
P = sp.expand(P)
XI = sp.expand(XI)
assert sp.rem(P, bb) == 0 and sp.rem(XI, bb) == 0

a, y, z, ell = sp.symbols("a y z ell", real=True)
F = sp.expand(sp.cancel(P/bb).subs({aa: a, bb: y-1, cc: z-1}))
G = sp.expand(sp.cancel(XI/bb).subs({aa: a, bb: y-1, cc: z-1}))
Q = y**2 + 1
L = (y+1)*z - 2
M = Q*z - 2
J = Q*z**2 - 2
A = (y+1)*J
D = (y+1)*z**2 + y - 3
N = (y**2-3)*z + (y-2)**2 + 1

assert sp.expand(F - (A*a**2 + 2*L*M*a + (y-1)*L**2)) == 0
disc_F = sp.factor(sp.discriminant(F, a))
assert sp.factor(disc_F - 8*Q*(z-1)**2*L**2) == 0
S = sp.diff(F, a)
assert sp.factor(S**2 - disc_F - 4*A*F) == 0
assert S.subs({a: 1, y: 2, z: 2}) == 172

# Exact positive-A boundary and D lower bound.
assert sp.expand(2*Q - (y+1)**2 - (y-1)**2) == 0
assert sp.factor(D.subs(z**2, 2/Q) - (y-1)**3/Q) == 0

assert sp.factor(sp.Poly(G, a).coeff_monomial(a**2) - 2*D) == 0
disc_G = sp.factor(sp.discriminant(G, a))
assert sp.factor(disc_G + 8*(z-1)*L**2*N) == 0
assert disc_G.subs({y: 2, z: 2}) == -384
assert G.subs({a: 1, y: 2, z: 2}) == 70

# All G double-root walls lie on or below the upper F wall.
assert sp.factor(F.subs(z, 1) - (y-1)*(a*(y+1)+y-1)**2) == 0
assert sp.factor(G.subs(z, 1) - (y-1)*(2*a+y-1)**2) == 0
zL = 2/(y+1)
assert sp.factor(F.subs(z, zL) - 2*a**2*(y-1)**2/(y+1)) == 0
assert sp.factor(G.subs(z, zL) - 2*a**2*(y-1)**2/(y+1)) == 0

zN = -((y-2)**2+1)/(y**2-3)
aN = (y-1)*Q/(2*(y**2-2*y-1))
FN = (y-1)**5*(y**2-7)*Q**3/(4*(y**2-3)**2*(y**2-2*y-1)**2)
assert sp.factor(N.subs(z, zN)) == 0
assert sp.factor(sp.diff(G, a).subs({z: zN, a: aN})) == 0
assert sp.factor(F.subs({z: zN, a: aN}) - FN) == 0

# Independent resultant reconstruction and H-wall lower-root derivative.
H = L**2 + 8*(z-1)
assert sp.factor(sp.resultant(F, G, a) - (y-1)**4*L**6*H) == 0
zH = 1-ell**2/8
yH = -(ell**2+8*ell+8)/(ell**2-8)
aH = -2*ell/(ell+4)
assert sp.factor(L.subs({y: yH, z: zH}) - ell) == 0
assert sp.factor(H.subs({y: yH, z: zH})) == 0
derivative_H = ell**3*(ell**2+4*ell+8)/(2*(ell**2-8))
assert sp.factor(sp.diff(F, a).subs({a: aH, y: yH, z: zH}) - derivative_H) == 0

print("PASS: independent K5-e upper-root theorem audit")
print("counts: 134 forests, 70 marked-endpoint-connected forests")
print("scope: local 2,4,2 stabilizer slice only")
