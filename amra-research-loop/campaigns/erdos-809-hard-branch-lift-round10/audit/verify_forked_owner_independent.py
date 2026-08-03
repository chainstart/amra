#!/usr/bin/env python3
"""Independent reconstruction of the shared-owner fork kernel.

Written from the labelled state definition, without importing the author's
fork probe or verifier.
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

    # Both mutually exclusive candidates have the same local adjacency and
    # share owner cy1.  They see X, Y-{y1}, and R, but not b,c,z,v or each
    # other.  State legality is the union of the base-pair constraints and
    # each singleton state's one switched pair; no joint colour face is used.
    new = set()
    for s in ("w", "u"):
        new.update(edge(s, x) for x in X)
        new.update(edge(s, y) for y in Y if y != "y1")
        new.update(edge(s, q) for q in R)

    edges = frozenset(old | new)
    vertices = tuple(sorted(set(A) | {"b", "c", "z", "w", "u"}))
    pairs = tuple(
        [(edge("b", X[i]), edge("c", Y[i])) for i in range(m)]
        + [(edge("w", "x1"), edge("c", "y1")),
           (edge("u", "x1"), edge("c", "y1"))]
    )
    return vertices, edges, deletable, pairs, X, Y, R


def traces_for(m, r):
    vertices, edges, deletable, pairs, X, Y, R = build(m, r)
    adj = {p: set() for p in vertices}
    for p, q in edges:
        adj[p].add(q)
        adj[q].add(p)
    traces = set()

    for first, second in pairs:
        start, nxt = first
        assert first in edges and second in edges

        def extend(path, found_second):
            if len(path) == 7:
                if start not in adj[path[-1]]:
                    return
                closing = edge(path[-1], start)
                if not (found_second or closing == second):
                    return
                cycle = {
                    edge(path[i], path[(i + 1) % 7]) for i in range(7)
                }
                traces.add(frozenset(cycle & deletable))
                return
            for q in sorted(adj[path[-1]]):
                if q == start or q in path:
                    continue
                extend(path + (q,), found_second or edge(path[-1], q) == second)

        extend((start, nxt), False)

    Q = set(X[2:])
    U, W = set(Y[:2]), set(Y[2:])
    F = set()
    for rr in R:
        F.update(edge(rr, q) for q in {"x1"} | set(Y))
    F.update(edge("x1", q) for q in Q)
    F.update(edge(u, w) for u in U for w in W)
    F.update(edge(p, q) for p, q in combinations(W, 2))
    return traces, frozenset(F), deletable


def main():
    records = []
    for m in range(3, 7):
        for r in range(4):
            traces, F, deletable = traces_for(m, r)
            singleton = {next(iter(t)) for t in traces if len(t) == 1}
            expected = r * (m + 1) + (m - 2) * (m + 3) // 2
            assert frozenset() not in traces
            assert set(map(len, traces)) <= {1, 3}
            assert singleton == set(F)
            assert len(F) == expected
            assert F <= deletable
            assert all(not trace.isdisjoint(F) for trace in traces)
            records.append((m, r, len(traces), len(F), Counter(map(len, traces))))

    # Compare exact kernel loss with the independent-owner formula.
    for m in range(3, 7):
        for r in range(4):
            fork_tau = r * (m + 1) + (m - 2) * (m + 3) // 2
            independent_tau = r * (m + 2) + (m - 2) * (m + 5) // 2
            assert independent_tau - fork_tau == r + m - 2

    print("PASS independent shared-owner fork kernel")
    print("support_representatives=16 trace_sizes={1,3} exact_tau=passed")
    for m, r, count, forced, sizes in records:
        print(f"m={m} r={r} traces={count} forced={forced} sizes={dict(sizes)}")


if __name__ == "__main__":
    main()
