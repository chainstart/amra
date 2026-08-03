#!/usr/bin/env python3
"""Exact K5-e marked-cross-edge stabilizer and natural-slice probe."""

from collections import Counter
from itertools import combinations, permutations
from math import gcd
import json
from pathlib import Path

import sympy as sp


V = tuple(range(5))
MISSING = (3, 4)
MARKED = (0, 3)
HOST = {e for e in combinations(V, 2)} - {MISSING}
DELETE = sorted(HOST - {MARKED})


def image(edge, perm):
    return tuple(sorted((perm[edge[0]], perm[edge[1]])))


STABILIZER = [
    p for p in permutations(V)
    if {image(e, p) for e in HOST} == HOST and image(MARKED, p) == MARKED
]


def edge_orbits():
    unseen, out = set(DELETE), []
    while unseen:
        seed = min(unseen)
        orbit = {image(seed, p) for p in STABILIZER}
        out.append(tuple(sorted(orbit)))
        unseen -= orbit
    return tuple(sorted(out, key=lambda o: (min(o), len(o))))


ORBITS = edge_orbits()
EXPECTED = (
    ((0, 1), (0, 2)),
    ((0, 4),),
    ((1, 2),),
    ((1, 3), (2, 3)),
    ((1, 4), (2, 4)),
)
assert set(map(frozenset, ORBITS)) == set(map(frozenset, EXPECTED))
ORBITS = EXPECTED
symbols = sp.symbols("a b c d e", real=True)
edge_class = {edge: i for i, orbit in enumerate(ORBITS) for edge in orbit}


def forest_and_connected(chosen):
    parent = list(V)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in chosen:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False, False
        parent[ru] = rv
    return True, find(MARKED[0]) == find(MARKED[1])


all_counts, conn_counts = Counter(), Counter()
for mask in range(1 << len(DELETE)):
    chosen = [DELETE[i] for i in range(len(DELETE)) if mask & (1 << i)]
    ok, connected = forest_and_connected(chosen)
    if not ok:
        continue
    complement = [edge for edge in DELETE if edge not in chosen]
    exponent = tuple(sum(edge_class[e] == i for e in complement) for i in range(5))
    all_counts[exponent] += 1
    if connected:
        conn_counts[exponent] += 1


def polynomial(counts):
    return sp.expand(sum(
        coefficient * sp.prod(symbols[i] ** exponent[i] for i in range(5))
        for exponent, coefficient in counts.items()
    ))


P, XI = polynomial(all_counts), polynomial(conn_counts)
anchor = {s: 1 for s in symbols}
assert P.subs(anchor) == sum(all_counts.values())
assert XI.subs(anchor) == sum(conn_counts.values())


def exact_segment_certificate(poly, free, point):
    """Return exact P-positive straight-anchor segment data, if root-free."""
    t = sp.symbols("t", real=True)
    sub = {s: 1 for s in symbols}
    for s, target in zip(free, point):
        sub[s] = 1 + t * (target - 1)
    path = sp.Poly(sp.expand(poly.subs(sub)), t, domain=sp.QQ)
    roots = path.count_roots(0, 1)
    return path, roots == 0 and path.eval(0) > 0 and path.eval(1) > 0


slices = []
counterexample = None
grid = [sp.Rational(k, 4) for k in range(-12, 13)]
for i, j in combinations(range(5), 2):
    free = (symbols[i], symbols[j])
    fixed = {s: 1 for k, s in enumerate(symbols) if k not in (i, j)}
    p2, x2 = sp.factor(P.subs(fixed)), sp.factor(XI.subs(fixed))
    resultant = sp.factor(sp.resultant(p2, x2, free[1]))
    record = {
        "free": [str(s) for s in free],
        "P": str(p2),
        "xi": str(x2),
        "resultant_eliminate_second": str(resultant),
        "P_total_degree": sp.Poly(p2, *free).total_degree(),
        "xi_total_degree": sp.Poly(x2, *free).total_degree(),
    }
    negative = None
    for u in grid:
        for v in grid:
            values = {free[0]: u, free[1]: v}
            if p2.subs(values) <= 0 or x2.subs(values) >= 0:
                continue
            path, certified = exact_segment_certificate(P, free, (u, v))
            if certified:
                negative = {
                    "point": [str(u), str(v)],
                    "P": str(p2.subs(values)),
                    "xi": str(x2.subs(values)),
                    "anchor_segment_P": str(path.as_expr()),
                    "open_segment_roots": 0,
                }
                counterexample = counterexample or {**negative, "free": [str(s) for s in free]}
                break
        if negative:
            break
    record["certified_anchor_segment_negative"] = negative
    slices.append(record)


result = {
    "schema": "amra.opg1757.k5-cross-orbit-probe.v1",
    "host": "K5 minus edge 34",
    "marked_edge": list(MARKED),
    "stabilizer_order": len(STABILIZER),
    "stabilizer": [list(p) for p in STABILIZER],
    "orbits": {str(s): [list(e) for e in orbit] for s, orbit in zip(symbols, ORBITS)},
    "orbit_sizes": [len(o) for o in ORBITS],
    "fixed_dimension": len(ORBITS),
    "transverse_dimension": len(DELETE) - len(ORBITS),
    "enumeration": {
        "deletion_edges": [list(e) for e in DELETE],
        "forests": sum(all_counts.values()),
        "endpoint_connected_forests": sum(conn_counts.values()),
        "P": str(P),
        "xi": str(XI),
        "P_factor": str(sp.factor(P)),
        "xi_factor": str(sp.factor(XI)),
        "gcd": str(sp.factor(sp.gcd(P, XI))),
        "anchor": {"P": int(P.subs(anchor)), "xi": int(XI.subs(anchor))},
    },
    "natural_two_variable_slices": slices,
    "first_certified_counterexample": counterexample,
    "scope": "five-variable stabilizer specialization and its two-variable unit slices only; not the eight-independent-variable host or OPG-1757",
}

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
