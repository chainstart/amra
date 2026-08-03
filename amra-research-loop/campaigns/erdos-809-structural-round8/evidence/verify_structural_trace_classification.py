#!/usr/bin/env python3
"""Independent exact reconstruction of the round-8 finite trace theorem.

This deliberately restates the locked graph instead of importing round 7.
It is a finite certificate, not an arbitrary-graph result.
"""

from collections import Counter
from itertools import combinations
import json


def edge(a, b):
    return tuple(sorted((a, b)))


X = tuple(f"x{i}" for i in range(1, 5))
Y = tuple(f"y{i}" for i in range(1, 5))
A = ("v",) + X + Y + ("r1", "r2")
V0 = tuple(sorted(set(A) | {"b", "c", "z"}))
V = tuple(sorted(set(V0) | {"w", "u"}))

E0 = {
    edge(p, q)
    for p, q in combinations(A, 2)
    if not ((p in X and q in Y) or (p in Y and q in X))
    and edge(p, q) not in {edge("x1", "x2"), edge("y1", "y2")}
}
E0 |= {edge("b", p) for p in X}
E0 |= {edge("c", q) for q in Y}
E0 |= {edge("b", "z")} | {edge("z", p) for p in X}

all_new = (
    {edge(q, p) for q in ("w", "u") for p in V0 if p != "v"}
    | {edge("w", "u")}
)
required = {edge("w", "x1"), edge("u", "x2")}
forbidden = {
    edge("w", "c"), edge("u", "c"), edge("w", "z"), edge("u", "z"),
    edge("w", "y1"), edge("u", "y2"),
}
optional = tuple(sorted(all_new - required - forbidden))
omitted = {edge("b", "u"), edge("b", "w"), edge("u", "w")}
eplus = frozenset(E0 | required | (set(optional) - omitted))

colour_pairs = tuple(
    [(edge("b", f"x{i}"), edge("c", f"y{i}")) for i in range(1, 5)]
    + [(edge("w", "x1"), edge("c", "y1")),
       (edge("u", "x2"), edge("c", "y2"))]
)
repeated_old = {f for pair in colour_pairs[:4] for f in pair}
deletable = {
    f for f in E0 if "v" not in f and f not in repeated_old
}

adj = {p: set() for p in V}
for p, q in eplus:
    adj[p].add(q)
    adj[q].add(p)

traces = set()
for first, second in colour_pairs:
    start, current = first

    def extend(path, used_second):
        if len(path) == 7:
            closing = edge(path[-1], start)
            if start in adj[path[-1]] and (used_second or closing == second):
                cycle = {edge(path[i], path[(i + 1) % 7]) for i in range(7)}
                traces.add(frozenset(cycle & deletable))
            return
        for nxt in sorted(adj[path[-1]]):
            if nxt != start and nxt not in path:
                extend(path + (nxt,), used_second or edge(path[-1], nxt) == second)

    extend((start, current), first == second)

R = {"r1", "r2"}
P = {"x1", "x2"}
Q = {"x3", "x4"}
U = {"y1", "y2"}
W = {"y3", "y4"}
block_r = {edge(p, q) for p in R for q in P | U | W}
block_x = {edge(p, q) for p in P for q in Q}
block_y = {edge(p, q) for p in U for q in W}
block_w = {edge("y3", "y4")}
forced_formula = block_r | block_x | block_y | block_w
singleton_edges = {next(iter(t)) for t in traces if len(t) == 1}

intersection_profile = Counter(len(t & forced_formula) for t in traces if len(t) == 3)
block_signature_profile = Counter(
    (
        len(t & block_r), len(t & block_x), len(t & block_y), len(t & block_w),
        len(t - forced_formula),
    )
    for t in traces if len(t) == 3
)
outside_edges = set().union(*(t - forced_formula for t in traces if len(t) == 3))
assert len(optional) == 19 and len(eplus) == 68 and len(deletable) == 32
assert frozenset() not in traces
assert Counter(map(len, traces)) == Counter({1: 21, 3: 72})
assert singleton_edges == forced_formula
assert len(block_r) == 12 and len(block_x) == 4
assert len(block_y) == 4 and len(block_w) == 1
assert sum(intersection_profile.values()) == 72
assert min(intersection_profile) >= 1
assert len(outside_edges) > 1

# Exact transversal theorem: all singleton traces force F, while F hits every trace.
assert all(not t.isdisjoint(forced_formula) for t in traces)

print(json.dumps({
    "schema": "amra.erdos809.structural-round8.trace-blocks.v1",
    "model": "locked n=16 natural-switch assignment omitting bu,bw,uw",
    "trace_count": len(traces),
    "trace_size_distribution": dict(sorted(Counter(map(len, traces)).items())),
    "forced_edge_block_sizes": {
        "R_to_P_union_U_union_W": len(block_r),
        "P_to_Q": len(block_x),
        "U_to_W": len(block_y),
        "K2_on_W": len(block_w),
    },
    "forced_edge_count": len(forced_formula),
    "triple_trace_forced_intersection_profile": dict(sorted(intersection_profile.items())),
    "triple_trace_block_signature_profile": {
        ",".join(map(str, signature)): multiplicity
        for signature, multiplicity in sorted(block_signature_profile.items())
    },
    "every_triple_trace_hits_forced_blocks": True,
    "distinct_outside_edges_in_triples": len(outside_edges),
    "exact_transversal_number": len(forced_formula),
    "finite_result_only": True,
    "public_problem_changed": False,
}, indent=2, sort_keys=True))
