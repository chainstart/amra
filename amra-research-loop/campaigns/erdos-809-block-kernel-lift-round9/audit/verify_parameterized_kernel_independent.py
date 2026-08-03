#!/usr/bin/env python3
"""Independent reconstruction of the parameterized natural-switch kernel.

This implementation was written from the frozen round-7 labelled model and
the round-9 closure contract.  It does not import the author's round-9
verifier or certificates.
"""

from collections import Counter
from itertools import combinations


def edge(a, b):
    assert a != b
    return tuple(sorted((a, b)))


def build(m, r):
    assert m >= 3 and r >= 0
    X = tuple(f"x{i}" for i in range(1, m + 1))
    Y = tuple(f"y{i}" for i in range(1, m + 1))
    R = tuple(f"r{i}" for i in range(1, r + 1))
    A = ("v",) + X + Y + R

    # Frozen old graph: two overlapping A-cliques, with the two special
    # internal edges removed, plus the b/c/z typed interface.
    old = {
        edge(p, q)
        for p, q in combinations(A, 2)
        if not ((p in X and q in Y) or (p in Y and q in X))
        and edge(p, q) not in {edge("x1", "x2"), edge("y1", "y2")}
    }
    old.update(edge("b", x) for x in X)
    old.update(edge("c", y) for y in Y)
    old.add(edge("b", "z"))
    old.update(edge("z", x) for x in X)

    repeated_old = {edge("b", x) for x in X} | {edge("c", y) for y in Y}
    v_incident = {e for e in old if "v" in e}
    deletable = frozenset(old - repeated_old - v_incident)

    # Unique colour-legal natural-switch branch: all typed w/u incidences
    # except cw,cu,wz,uz,wy1,uy2 and the three protected-cycle edges
    # bw,bu,uw.
    new = set()
    new.update(edge("w", x) for x in X)
    new.update(edge("w", y) for y in Y if y != "y1")
    new.update(edge("w", q) for q in R)
    new.update(edge("u", x) for x in X)
    new.update(edge("u", y) for y in Y if y != "y2")
    new.update(edge("u", q) for q in R)

    edges = frozenset(old | new)
    vertices = tuple(sorted(set(A) | {"b", "c", "z", "w", "u"}))
    colour_pairs = tuple(
        [(edge("b", X[i]), edge("c", Y[i])) for i in range(m)]
        + [(edge("w", "x1"), edge("c", "y1")),
           (edge("u", "x2"), edge("c", "y2"))]
    )
    return vertices, edges, deletable, colour_pairs, X, Y, R


def traces_for(m, r):
    vertices, edges, deletable, colour_pairs, X, Y, R = build(m, r)
    adjacency = {q: set() for q in vertices}
    for p, q in edges:
        adjacency[p].add(q)
        adjacency[q].add(p)

    traces = set()
    for first, second in colour_pairs:
        start, nxt = first
        assert first in edges and second in edges

        def extend(path, found_second):
            if len(path) == 7:
                if start not in adjacency[path[-1]]:
                    return
                closing = edge(path[-1], start)
                if not (found_second or closing == second):
                    return
                cycle = {
                    edge(path[i], path[(i + 1) % 7]) for i in range(7)
                }
                traces.add(frozenset(cycle & deletable))
                return
            for q in sorted(adjacency[path[-1]]):
                if q == start or q in path:
                    continue
                extend(path + (q,), found_second or edge(path[-1], q) == second)

        extend((start, nxt), False)

    P, Q = set(X[:2]), set(X[2:])
    U, W = set(Y[:2]), set(Y[2:])
    F = set()
    for rr in R:
        F.update(edge(rr, q) for q in P | U | W)
    F.update(edge(p, q) for p in P for q in Q)
    F.update(edge(u, w) for u in U for w in W)
    F.update(edge(p, q) for p, q in combinations(W, 2))
    return traces, frozenset(F), deletable


def protected_templates():
    # Each tuple is a seven-cycle created if the named omitted edge is
    # restored.  Every old edge on it is frozen (v-incident or repeated), so
    # its deletion trace is empty.
    return {
        edge("b", "w"): ("b", "x1", "u", "y1", "c", "y2", "w"),
        edge("b", "u"): ("b", "x1", "v", "y1", "c", "y3", "u"),
        edge("u", "w"): ("w", "x1", "v", "y1", "c", "y3", "u"),
    }


def check_templates():
    vertices, base, deletable, colour_pairs, *_ = build(3, 0)
    pair_sets = [set(pair) for pair in colour_pairs]
    for restored, cycle_vertices in protected_templates().items():
        augmented = set(base) | {restored}
        cycle = {
            edge(cycle_vertices[i], cycle_vertices[(i + 1) % 7])
            for i in range(7)
        }
        assert cycle <= augmented
        assert any(pair <= cycle for pair in pair_sets)
        assert cycle.isdisjoint(deletable)


def main():
    check_templates()
    records = []
    for m in range(3, 7):
        for r in range(4):
            traces, F, deletable = traces_for(m, r)
            singleton = {next(iter(t)) for t in traces if len(t) == 1}
            expected_count = r * (m + 2) + (m - 2) * (m + 5) // 2
            assert frozenset() not in traces
            assert Counter(map(len, traces)).keys() <= {1, 3}
            assert singleton == set(F)
            assert len(F) == expected_count
            assert F <= deletable
            assert all(not trace.isdisjoint(F) for trace in traces)
            records.append((m, r, len(traces), len(F), Counter(map(len, traces))))

    # Locked round-8 specialization.
    traces, F, _ = traces_for(4, 2)
    assert len(traces) == 93
    assert Counter(map(len, traces)) == Counter({1: 21, 3: 72})
    assert len(F) == 21

    print("PASS independent parameterized-kernel reconstruction")
    print("protected_templates=3 support_representatives=16")
    print("locked=(m=4,r=2): traces=93 singleton=21 triple=72 tau=21")
    for m, r, count, forced, sizes in records:
        print(f"m={m} r={r} traces={count} forced={forced} sizes={dict(sizes)}")


if __name__ == "__main__":
    main()
