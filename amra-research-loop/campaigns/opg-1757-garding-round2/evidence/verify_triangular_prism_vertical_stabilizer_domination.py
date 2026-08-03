#!/usr/bin/env python3
"""Exact triangular-prism vertical-edge stabilizer domination certificate."""

from itertools import combinations
import json
import sympy as sp


a, b, c = sp.symbols("a b c")
x, y, z = sp.symbols("x y z")
marked = (0, 3)
all_edges = (
    (0, 1), (1, 2), (2, 0),
    (3, 4), (4, 5), (5, 3),
    (0, 3), (1, 4), (2, 5),
)


def orbit_label(edge):
    if edge in {(1, 4), (2, 5)}:
        return a
    if edge in {(1, 2), (4, 5)}:
        return c
    return b


edges = tuple((u, v, orbit_label((u, v))) for u, v in all_edges
              if (u, v) != marked)


def classify(selected):
    parent = list(range(6))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for index in selected:
        u, v, _ = edges[index]
        ru, rv = root(u), root(v)
        if ru == rv:
            return None
        parent[ru] = rv
    selected_set = set(selected)
    monomial = sp.prod(label for index, (_, _, label) in enumerate(edges)
                       if index not in selected_set)
    return monomial, root(marked[0]) == root(marked[1])


P = sp.Integer(0)
Q = sp.Integer(0)
forest_count = connected_count = 0
for size in range(9):
    for selected in combinations(range(8), size):
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
assert forest_count == 180 and connected_count == 46
assert P.subs({a: 1, b: 1, c: 1}) == 180
assert Q.subs({a: 1, b: 1, c: 1}) == 46

Ps = sp.factor(P.subs({a: x - 1, b: y - 1, c: z - 1}))
Qs = sp.factor(Q.subs({a: x - 1, b: y - 1, c: z - 1}))
T = y**2*z - 1
V = y**2 + z - 2
A = y*(z + 1) - 2
B = 2*y + z - 3
assert sp.expand(Ps - ((x*T)**2 - V**2)) == 0
assert sp.expand(Qs - 2*(x*A**2 - B**2)) == 0
assert sp.factor(V*A**2 - T*B**2) == (y - 1)**4*(z - 1)**2

print(json.dumps({
    "schema": "amra.opg1757.triangular-prism-vertical-stabilizer.v1",
    "host": "triangular prism",
    "marked_edge": [0, 3],
    "unmarked_edge_orbits": {"other_vertical": 2, "incident_triangle": 4, "opposite_triangle": 2},
    "reconstruction": {"forests": forest_count, "endpoint_connected_forests": connected_count},
    "shift": "x=a+1,y=b+1,z=c+1",
    "P_identity": "P=(x*T)^2-V^2, T=y^2*z-1, V=y^2+z-2",
    "xi_identity": "xi=2*(x*A^2-B^2), A=y*(z+1)-2, B=2*y+z-3",
    "barrier_identity": "V*A^2-T*B^2=(y-1)^4*(z-1)^2",
    "distinguished_component": "x,y,z>0; T>0; x*T>V (and V>0 follows by AM-GM)",
    "conclusion": "xi>0 on the complete three-variable marked-vertical-edge stabilizer component",
    "scope": "three stabilizer variables only; not eight independent unmarked-edge variables or the triangle-edge orbit",
    "public_problem_closed": False
}, indent=2, sort_keys=True))
