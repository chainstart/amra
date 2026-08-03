#!/usr/bin/env python3
"""Exact K5-e cross-edge (b,c) natural-slice component theorem."""

from collections import Counter
from itertools import combinations, permutations
import json
from pathlib import Path

import sympy as sp


V = tuple(range(5))
missing, marked = (3, 4), (0, 3)
host = set(combinations(V, 2)) - {missing}
deleted = sorted(host - {marked})


def image(edge, perm):
    return tuple(sorted((perm[edge[0]], perm[edge[1]])))


stabilizer = [p for p in permutations(V)
              if {image(e, p) for e in host} == host
              and image(marked, p) == marked]
assert len(stabilizer) == 2

orbits = {
    "a": {(0, 1), (0, 2)},
    "b": {(0, 4)},
    "c": {(1, 2)},
    "d": {(1, 3), (2, 3)},
    "e": {(1, 4), (2, 4)},
}
for orbit in orbits.values():
    assert {image(edge, p) for edge in orbit for p in stabilizer} == orbit
assert set().union(*orbits.values()) == set(deleted)


def classify(chosen):
    parent = list(V)

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for u, v in chosen:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False, False
        parent[ru] = rv
    return True, find(marked[0]) == find(marked[1])


edge_class = {edge: name for name, orbit in orbits.items() for edge in orbit}
all_counts, connected_counts = Counter(), Counter()
names = tuple(orbits)
for mask in range(1 << len(deleted)):
    chosen = [deleted[i] for i in range(len(deleted)) if mask & (1 << i)]
    forest, connected = classify(chosen)
    if not forest:
        continue
    complement = set(deleted) - set(chosen)
    exponent = tuple(sum(edge_class[e] == name for e in complement) for name in names)
    all_counts[exponent] += 1
    if connected:
        connected_counts[exponent] += 1

a, b, c, d, e = sp.symbols("a b c d e", real=True)
variables = (a, b, c, d, e)


def make_poly(counts):
    return sp.expand(sum(coefficient * sp.prod(v**power for v, power in zip(variables, exponent))
                         for exponent, coefficient in counts.items()))


P, xi = make_poly(all_counts), make_poly(connected_counts)
assert (sum(all_counts.values()), sum(connected_counts.values())) == (128, 58)
assert (P.subs({v: 1 for v in variables}), xi.subs({v: 1 for v in variables})) == (128, 58)

Pbc = sp.factor(P.subs({a: 1, d: 1, e: 1}))
xibc = sp.factor(xi.subs({a: 1, d: 1, e: 1}))
assert sp.expand(Pbc - (54*b*c + 27*b + 32*c + 15)) == 0
assert sp.expand(xibc - 2*(11*b*c + 6*b + 8*c + 4)) == 0

x, y = sp.symbols("x y", real=True, positive=True)
forward = {x: 54*b + 32, y: c + sp.Rational(1, 2)}
inverse = {b: (x-32)/54, c: y-sp.Rational(1, 2)}
assert sp.expand(Pbc - ((54*b+32)*(c+sp.Rational(1,2))-1)) == 0
assert sp.expand(54*xibc.subs(inverse) - (22*x*y+x+160*y-32)) == 0

# On the anchor component x>0,y>0,xy>1.  Its xi numerator is strictly
# larger than its value with y=1/x, and that boundary value is a square plus
# a positive rational term.
boundary = sp.factor((22*x*y+x+160*y-32).subs(y, 1/x))
square_bound = sp.factor((x-5)**2/x + 135/x)
assert sp.expand(boundary-square_bound) == 0

resultant = sp.factor(sp.resultant(Pbc, xibc, c))
assert sp.expand(resultant - 2*(27*b*b+27*b+8)) == 0
assert sp.discriminant(27*b*b+27*b+8, b) == -135

competing = {a: -5, b: sp.Rational(3, 2), c: 1, d: 1, e: 1}
assert P.subs(competing) == sp.Rational(2113, 2)
assert xi.subs(competing) == -9

result = {
    "schema": "amra.opg1757.k5-cross-bc-component.v1",
    "host": "K5 minus edge 34",
    "marked_edge": list(marked),
    "stabilizer_order": len(stabilizer),
    "orbits": {name: sorted(map(list, orbit)) for name, orbit in orbits.items()},
    "orbit_sizes": {name: len(orbit) for name, orbit in orbits.items()},
    "fixed_dimension": 5,
    "transverse_dimension": 3,
    "forest_reconstruction": {
        "deletion_forests": sum(all_counts.values()),
        "endpoint_connected_forests": sum(connected_counts.values()),
        "P_anchor": int(P.subs({v: 1 for v in variables})),
        "xi_anchor": int(xi.subs({v: 1 for v in variables})),
    },
    "slice": {
        "fixed": "a=d=e=1",
        "free": ["b", "c"],
        "P": str(Pbc),
        "xi": str(xibc),
        "coordinates": "x=54b+32, y=c+1/2",
        "P_normal_form": "xy-1",
        "distinguished_component": "x>0,y>0,xy>1",
        "xi_normal_form": "54xi=22xy+x+160y-32",
        "boundary_lower_bound": "x+160/x-10=(x-5)^2/x+135/x>0",
        "resultant_eliminate_c": str(resultant),
        "resultant_quadratic_discriminant": -135,
        "conclusion": "xi>0 on the complete distinguished P-positive component",
    },
    "competing_component_guard": {
        "slice": "c=d=e=1 with a,b free",
        "point": {"a": "-5", "b": "3/2"},
        "P": "2113/2",
        "xi": "-9",
        "interpretation": "P-positive negative point only; no distinguished-component path is claimed"
    },
    "scope": "two-variable singleton-orbit slice a=d=e=1 only; not the five-variable stabilizer component, eight-independent-variable host, G201, or OPG-1757",
}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
