#!/usr/bin/env python3
"""Blind audit by exhaustive canonical 7-cycle enumeration, not author DFS."""
from collections import Counter
from itertools import combinations, permutations

def edge(a, b):
    return tuple(sorted((a, b)))

X = tuple(f"x{i}" for i in range(1, 5))
Y = tuple(f"y{i}" for i in range(1, 5))
A = ("v",) + X + Y + ("r1", "r2")
V0 = tuple(sorted(set(A) | {"b", "c", "z"}))
V = tuple(sorted(set(V0) | {"w", "u"}))
E0 = {edge(p,q) for p,q in combinations(A,2)
      if not ((p in X and q in Y) or (p in Y and q in X))
      and edge(p,q) not in {edge("x1","x2"),edge("y1","y2")}}
E0 |= {edge("b",p) for p in X} | {edge("c",q) for q in Y}
E0 |= {edge("b","z")} | {edge("z",p) for p in X}
all_new = {edge(q,p) for q in ("w","u") for p in V0 if p != "v"} | {edge("w","u")}
required = {edge("w","x1"),edge("u","x2")}
forbidden = {edge("w","c"),edge("u","c"),edge("w","z"),edge("u","z"),edge("w","y1"),edge("u","y2")}
omitted = {edge("b","u"),edge("b","w"),edge("u","w")}
E = E0 | required | ((all_new-required-forbidden)-omitted)
colour_pairs = ([{edge("b",f"x{i}"),edge("c",f"y{i}")} for i in range(1,5)]
                + [{edge("w","x1"),edge("c","y1")},
                   {edge("u","x2"),edge("c","y2")}])
repeated_old = set().union(*colour_pairs[:4])
deletable = {f for f in E0 if "v" not in f and f not in repeated_old}

# Enumerate every undirected 7-cycle exactly once: choose its vertex set, put
# the lexicographically least vertex first, and quotient reversal by requiring
# second vertex < last vertex.  This is independent of the author's colour-pair
# rooted DFS.
traces = set()
cycle_count = 0
for chosen in combinations(V, 7):
    first = chosen[0]
    for tail in permutations(chosen[1:]):
        if tail[0] > tail[-1]:
            continue
        seq = (first,) + tail
        cycle = frozenset(edge(seq[i],seq[(i+1)%7]) for i in range(7))
        if not cycle <= E:
            continue
        cycle_count += 1
        if any(pair <= cycle for pair in colour_pairs):
            traces.add(frozenset(cycle & deletable))

R,P,Q,U,W = {"r1","r2"},{"x1","x2"},{"x3","x4"},{"y1","y2"},{"y3","y4"}
blocks = (
    {edge(p,q) for p in R for q in P|U|W},
    {edge(p,q) for p in P for q in Q},
    {edge(p,q) for p in U for q in W},
    {edge("y3","y4")},
)
F = set().union(*blocks)
singletons = {next(iter(t)) for t in traces if len(t)==1}
profile = Counter(len(t&F) for t in traces if len(t)==3)
signatures = Counter(tuple(len(t&block) for block in blocks)+(len(t-F),)
                     for t in traces if len(t)==3)
assert cycle_count == 68508
assert Counter(map(len,traces)) == Counter({1:21,3:72})
assert tuple(map(len,blocks)) == (12,4,4,1)
assert singletons == F and len(F)==21
assert profile == Counter({3:60,2:12})
assert signatures == Counter({(2,0,1,0,0):32,(3,0,0,0,0):24,
                              (1,1,0,0,1):8,(2,0,0,0,1):4,
                              (2,0,0,1,0):4})
assert all(t&F for t in traces)
print("independent canonical-cycle trace audit: PASS")
print("cycles=68508 traces=93 singleton=21 triples=72 tau=21")
