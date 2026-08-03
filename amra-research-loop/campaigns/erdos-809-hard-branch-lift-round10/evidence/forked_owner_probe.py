#!/usr/bin/env python3
"""Exact trace enumerator for the minimal forked-owner switch family.

The base state has pairs (b-x_i,c-y_i).  Two alternative one-edge switches
both consume owner c-y1, replacing b-x1 by w-x1 or u-x1.  They are mutually
exclusive, so there is no joint state.  This is the smallest state complex
which is not the two-owner Boolean square used in round 9.
"""

from collections import Counter
from itertools import combinations
import json


def edge(a, b):
    return tuple(sorted((a, b)))


def instance(m, r):
    assert m >= 3 and r >= 0
    X = tuple(f"x{i}" for i in range(1, m + 1))
    Y = tuple(f"y{i}" for i in range(1, m + 1))
    R = tuple(f"r{i}" for i in range(1, r + 1))
    A = ("v",) + X + Y + R
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

    # Both alternatives have the same local interface and the same owner.
    all_new = {edge(q, p) for q in ("w", "u") for p in V0 if p != "v"}
    all_new.add(edge("w", "u"))
    required = {edge("w", "x1"), edge("u", "x1")}
    forbidden = {
        edge("w", "c"), edge("u", "c"), edge("w", "z"), edge("u", "z"),
        edge("w", "y1"), edge("u", "y1"),
    }
    omitted = {edge("b", "u"), edge("b", "w"), edge("u", "w")}
    eplus = frozenset(E0 | required | ((all_new - required - forbidden) - omitted))

    base = tuple((edge("b", f"x{i}"), edge("c", f"y{i}")) for i in range(1, m + 1))
    # A union of state constraints is sufficient because deletion must make
    # every state legal.  The two alternatives are never asserted jointly.
    pairs = base + (
        (edge("w", "x1"), edge("c", "y1")),
        (edge("u", "x1"), edge("c", "y1")),
    )
    repeated_old = {f for pair in base for f in pair}
    deletable = {f for f in E0 if "v" not in f and f not in repeated_old}
    adj = {p: set() for p in V}
    for p, q in eplus:
        adj[p].add(q)
        adj[q].add(p)

    traces = set()
    witnesses = {}
    for first, second in pairs:
        start, current = first

        def extend(path, used_second):
            if len(path) == 7:
                closing = edge(path[-1], start)
                if start in adj[path[-1]] and (used_second or closing == second):
                    cyc = frozenset(edge(path[i], path[(i + 1) % 7]) for i in range(7))
                    trace = frozenset(cyc & deletable)
                    traces.add(trace)
                    witnesses.setdefault(trace, path)
                return
            for nxt in sorted(adj[path[-1]]):
                if nxt != start and nxt not in path:
                    extend(path + (nxt,), used_second or edge(path[-1], nxt) == second)

        extend((start, current), False)

    singleton = {next(iter(t)) for t in traces if len(t) == 1}
    Q, U, W, RR = set(X[2:]), set(Y[:2]), set(Y[2:]), set(R)
    formula = (
        {edge(p, q) for p in RR for q in {X[0]} | set(Y)}
        | {edge(X[0], q) for q in Q}
        | {edge(p, q) for p in U for q in W}
        | {edge(p, q) for p, q in combinations(W, 2)}
    )
    return {
        "m": m,
        "r": r,
        "vertices": len(V),
        "edges": len(eplus),
        "trace_sizes": dict(sorted(Counter(map(len, traces)).items())),
        "singleton_count": len(singleton),
        "singletons": sorted(singleton),
        "formula_count": len(formula),
        "formula_minus_singleton": sorted(formula - singleton),
        "singleton_minus_formula": sorted(singleton - formula),
        "formula_hits_all": all(not t.isdisjoint(formula) for t in traces),
        "singleton_hits_all": all(not t.isdisjoint(singleton) for t in traces),
        "empty_trace": [] in [list(t) for t in traces],
        "sample_unhit_trace": next((sorted(t) for t in traces if t.isdisjoint(singleton)), None),
    }


if __name__ == "__main__":
    rows = [instance(m, r) for m in range(3, 7) for r in range(4)]
    print(json.dumps({"schema": "amra.erdos809.forked-owner.v1", "rows": rows}, indent=2))
