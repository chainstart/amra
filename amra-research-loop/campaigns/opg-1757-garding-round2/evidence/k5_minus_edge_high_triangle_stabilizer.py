#!/usr/bin/env python3
"""Independent K5-e high-triangle marked-edge stabilizer calculation."""

from __future__ import annotations

from collections import Counter
from itertools import permutations
import hashlib
import json
from pathlib import Path

import sympy as sp


V = tuple(range(5))
MISSING = (3, 4)
MARKED = (0, 1)
HOST_EDGES = {tuple(sorted((i, j))) for i in V for j in V if i < j} - {MISSING}
DELETE_EDGES = sorted(HOST_EDGES - {MARKED})


def image_edge(edge: tuple[int, int], perm: tuple[int, ...]) -> tuple[int, int]:
    return tuple(sorted((perm[edge[0]], perm[edge[1]])))


STABILIZER = [
    perm for perm in permutations(V)
    if {image_edge(e, perm) for e in HOST_EDGES} == HOST_EDGES
    and image_edge(MARKED, perm) == MARKED
]


def edge_orbits() -> list[list[tuple[int, int]]]:
    unseen = set(DELETE_EDGES)
    out = []
    while unseen:
        edge = min(unseen)
        orbit = {image_edge(edge, perm) for perm in STABILIZER}
        out.append(sorted(orbit))
        unseen -= orbit
    return sorted(out, key=lambda orbit: (len(orbit), orbit))


ORBITS = edge_orbits()
# Name the geometrically distinct 2,4,2 classes, independently of sort order.
OA = {(0, 2), (1, 2)}
OB = {(0, 3), (0, 4), (1, 3), (1, 4)}
OC = {(2, 3), (2, 4)}
assert {frozenset(x) for x in ORBITS} == {frozenset(OA), frozenset(OB), frozenset(OC)}


def is_forest(edges: list[tuple[int, int]]) -> bool:
    parent = list(V)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True


def marked_connected(edges: list[tuple[int, int]]) -> bool:
    adjacent = {v: [] for v in V}
    for u, v in edges:
        adjacent[u].append(v)
        adjacent[v].append(u)
    seen = {MARKED[0]}
    stack = [MARKED[0]]
    while stack:
        u = stack.pop()
        for v in adjacent[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return MARKED[1] in seen


def monomial_type(complement: list[tuple[int, int]]) -> tuple[int, int, int]:
    return (
        sum(e in OA for e in complement),
        sum(e in OB for e in complement),
        sum(e in OC for e in complement),
    )


forest_counts: Counter[tuple[int, int, int]] = Counter()
connected_counts: Counter[tuple[int, int, int]] = Counter()
for mask in range(1 << len(DELETE_EDGES)):
    selected = [DELETE_EDGES[i] for i in range(len(DELETE_EDGES)) if mask & (1 << i)]
    if not is_forest(selected):
        continue
    complement = [edge for edge in DELETE_EDGES if edge not in selected]
    kind = monomial_type(complement)
    forest_counts[kind] += 1
    if marked_connected(selected):
        connected_counts[kind] += 1

a, b, c = sp.symbols("a b c", real=True)
P = sp.expand(sum(coef * a**i * b**j * c**k for (i, j, k), coef in forest_counts.items()))
XI = sp.expand(sum(coef * a**i * b**j * c**k for (i, j, k), coef in connected_counts.items()))
assert sp.rem(P, b) == 0 and sp.rem(XI, b) == 0
F, G = sp.cancel(P / b), sp.cancel(XI / b)

L = sp.expand(b * (c + 1) + 2 * c)
H = sp.expand(L**2 + 8 * c)
resultant_a = sp.factor(sp.resultant(P, XI, a))
assert sp.expand(resultant_a - b**8 * L**6 * H) == 0

# Exact anchor path c in [-1/10,1] at a=b=1.
t = sp.symbols("t", real=True)
anchor_P = sp.factor(P.subs({a: 1, b: 1, c: t}))
anchor_XI = sp.factor(XI.subs({a: 1, b: 1, c: t}))
anchor_point = {a: 1, b: 1, c: sp.Rational(-1, 10)}
assert sp.expand(anchor_P - 2 * (27 * t**2 + 32 * t + 8)) == 0
assert sp.diff(anchor_P, t).subs(t, sp.Rational(-1, 10)) > 0
assert P.subs(anchor_point) > 0 and XI.subs(anchor_point) > 0
assert H.subs({b: 1, c: sp.Rational(-1, 10)}) < 0

# Complete b=1 component channel.  F=15*u*v over Q(sqrt(10)); on the
# distinguished component both factors retain their positive anchor signs.
rt = sp.sqrt(10)
u = a * c + (1 - rt / 5) * (a + c) + sp.Rational(1, 3) - rt / 15
v = a * c + (1 + rt / 5) * (a + c) + sp.Rational(1, 3) + rt / 15
assert sp.simplify(F.subs(b, 1) - 15 * u * v) == 0
U, W = sp.symbols("U W", real=True)
g_in_walls = (
    U**2 + 22 * U * W + (8 + 8 * rt / 3) * U
    + W**2 + (8 - 8 * rt / 3) * W + sp.Rational(4, 9)
) / 4
sum_ac = 5 * (W - U) / (2 * rt) - sp.Rational(1, 3)
prod_ac = (U + W) / 2 - sum_ac - sp.Rational(1, 3)
G_symmetric = (
    6 * prod_ac**2 + 12 * prod_ac * sum_ac
    + 4 * (sum_ac**2 - 2 * prod_ac) + 16 * prod_ac
    + 4 * sum_ac + 1
)
assert sp.simplify(G_symmetric - g_in_walls) == 0
wall_quadratic_discriminant = sp.factor((8 - 8 * rt / 3) ** 2 - sp.Rational(16, 9))
assert wall_quadratic_discriminant < 0

# A competing (non-anchor on b=1) zero-locus component.  This guards against
# treating an arbitrary negative point as a distinguished-component witness.
zero_line_F = sp.factor(F.subs({a: -b / 2, c: 0}))
zero_line_G = sp.factor(G.subs({a: -b / 2, c: 0}))
assert zero_line_F == b**5 / 4 and zero_line_G == 0
negative_point = {a: sp.Rational(-1, 2), b: 1, c: sp.Rational(-1, 100)}
assert F.subs(negative_point) > 0 and G.subs(negative_point) < 0
assert u.subs(negative_point) < 0 and v.subs(negative_point) < 0

result = {
    "schema": "amra.opg1757.k5-minus-edge.high-triangle-stabilizer.v1",
    "scope": "complete three-variable stabilizer specialization only; not the eight-independent-variable or global G201 statement",
    "host": "K5 minus edge 34",
    "marked_edge": list(MARKED),
    "stabilizer_order": len(STABILIZER),
    "orbits": {
        "a": sorted(map(list, OA)),
        "b": sorted(map(list, OB)),
        "c": sorted(map(list, OC)),
        "sizes": [len(OA), len(OB), len(OC)],
    },
    "enumeration": {
        "forests": sum(forest_counts.values()),
        "marked_connected_forests": sum(connected_counts.values()),
        "P": str(P),
        "xi": str(XI),
        "F_equals_P_over_b": str(F),
        "G_equals_xi_over_b": str(G),
        "at_1_1_1": {"P": int(P.subs({a: 1, b: 1, c: 1})), "xi": int(XI.subs({a: 1, b: 1, c: 1}))},
    },
    "zero_locus": {
        "resultant_eliminate_a": str(resultant_a),
        "L": str(L),
        "H": str(H),
        "shifted_coordinates": "y=b+1,z=c+1 give L=z(y+1)-2 and H=L^2+8(z-1)",
    },
    "anchor_countercheck": {
        "path": "a=b=1, c decreases from 1 to -1/10",
        "P_on_path": str(anchor_P),
        "endpoint": {"a": "1", "b": "1", "c": "-1/10", "z": "9/10"},
        "endpoint_P": str(P.subs(anchor_point)),
        "endpoint_xi": str(XI.subs(anchor_point)),
        "endpoint_H": str(H.subs({b: 1, c: sp.Rational(-1, 10)})),
        "conclusion": "the anchor component forces neither z>=1 nor H>=0; this endpoint is not a xi counterexample",
    },
    "b_equals_1_component_proof": {
        "F_factorization": "F=15*u*v with the two walls recorded in the note",
        "G_in_wall_coordinates": str(g_in_walls),
        "univariate_discriminant": str(wall_quadratic_discriminant),
        "conclusion": "G>0 whenever u>0 and v>0, hence throughout the b=1 distinguished component",
    },
    "competing_zero_locus_component": {
        "line": "a=-b/2,c=0,b>0",
        "F_on_line": str(zero_line_F),
        "G_on_line": str(zero_line_G),
        "nearby_negative_point": {"a": "-1/2", "b": "1", "c": "-1/100"},
        "nearby_F": str(F.subs(negative_point)),
        "nearby_G": str(G.subs(negative_point)),
        "b_equals_1_wall_signs": "u<0,v<0, so this is not the distinguished u>0,v>0 component",
    },
    "global_status": "open on the full three-variable stabilizer component; no counterexample and no domination proof",
}

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
print("sha256", hashlib.sha256(out.read_bytes()).hexdigest())
