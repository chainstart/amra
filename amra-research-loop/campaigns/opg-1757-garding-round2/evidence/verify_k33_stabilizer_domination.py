#!/usr/bin/env python3
"""Exact K3,3 marked-edge two-orbit domination certificate."""

from itertools import combinations
import json
import sympy as sp


a, b = sp.symbols("a b")
x, y = sp.symbols("x y")
left = (0, 1, 2)
right = (3, 4, 5)
marked = (0, 3)
edges = []
for u in left:
    for v in right:
        if (u, v) == marked:
            continue
        # Four edges touch one marked endpoint; the other four do not.
        label = a if u == marked[0] or v == marked[1] else b
        edges.append((u, v, label))


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
for size in range(len(edges) + 1):
    for selected in combinations(range(len(edges)), size):
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
assert forest_count == 194 and connected_count == 60
assert P.subs({a: 1, b: 1}) == 194
assert Q.subs({a: 1, b: 1}) == 60

Ps = sp.factor(P.subs({a: x - 1, b: y - 1}))
Qs = sp.factor(Q.subs({a: x - 1, b: y - 1}))
F = sp.factor(Ps / (y - 1))
G = sp.factor(Qs / (4*(y - 1)))
assert sp.expand(Ps - (y - 1)*F) == 0
assert sp.expand(Qs - 4*(y - 1)*G) == 0

# Pseudo-division in y uses lc_y(G)^2=x^4.  The exact remainder is the
# component barrier: on G=0 and x!=0, F=-(x-1)^4(y-1).
remainder = sp.factor(sp.prem(F, G, y))
assert remainder == -x**4*(x - 1)**4*(y - 1)
quotient = sp.cancel((x**4*F - remainder) / G)
assert sp.expand(x**4*F - quotient*G - remainder) == 0

# The exceptional x=0 fibre is also outside F>0 when G=0.
assert sp.factor(G.subs(x, 0)) == 5 - y
assert F.subs({x: 0, y: 5}) == -4
assert F.subs({x: 2, y: 2}) == 194
assert G.subs({x: 2, y: 2}) == 15

print(json.dumps({
    "schema": "amra.opg1757.k33-two-orbit-domination.v1",
    "host": "K3,3",
    "marked_edge": [0, 3],
    "unmarked_edge_orbits": {"incident_to_marked_endpoint": 4, "other": 4},
    "reconstruction": {"forests": forest_count, "endpoint_connected_forests": connected_count},
    "shift": "x=a+1,y=b+1",
    "P": "(y-1)*F",
    "xi": "4*(y-1)*G",
    "pseudo_remainder": "prem_y(F,G)=-x^4*(x-1)^4*(y-1)",
    "component_argument": "anchor component has y>1 and F>0; G=0 forces F<=0 (including x=0 separately), so G keeps its positive anchor sign",
    "conclusion": "xi>0 on the distinguished component in the complete marked-edge stabilizer-variable specialization",
    "scope": "two stabilizer variables only; not eight independent unmarked-edge variables",
    "public_problem_closed": False
}, indent=2, sort_keys=True))
