#!/usr/bin/env python3
"""Bounded discovery probe for the parameterized round-8 architecture.

This is route-selection evidence only.  Any universal claim selected from
these data must subsequently be proved by explicit cycle templates.
"""

from collections import Counter
from itertools import combinations
import json


def edge(a, b):
    return tuple(sorted((a, b)))


def instance(m, r, omitted_override=None):
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
    all_new = (
        {edge(q, p) for q in ("w", "u") for p in V0 if p != "v"}
        | {edge("w", "u")}
    )
    required = {edge("w", "x1"), edge("u", "x2")}
    forbidden = {
        edge("w", "c"), edge("u", "c"), edge("w", "z"), edge("u", "z"),
        edge("w", "y1"), edge("u", "y2"),
    }
    optional = all_new - required - forbidden
    omitted = ({edge("b", "u"), edge("b", "w"), edge("u", "w")}
               if omitted_override is None else set(omitted_override))
    eplus = frozenset(E0 | required | (optional - omitted))
    pairs = tuple(
        [(edge("b", f"x{i}"), edge("c", f"y{i}")) for i in range(1, m + 1)]
        + [(edge("w", "x1"), edge("c", "y1")),
           (edge("u", "x2"), edge("c", "y2"))]
    )
    repeated_old = {f for pair in pairs[:m] for f in pair}
    deletable = {f for f in E0 if "v" not in f and f not in repeated_old}
    adj = {p: set() for p in V}
    for p, q in eplus:
        adj[p].add(q)
        adj[q].add(p)
    traces = set()
    protected_witness = None
    for first, second in pairs:
        start, current = first

        def extend(path, used_second):
            nonlocal protected_witness
            if len(path) == 7:
                closing = edge(path[-1], start)
                if start in adj[path[-1]] and (used_second or closing == second):
                    cycle = {edge(path[i], path[(i + 1) % 7]) for i in range(7)}
                    trace = frozenset(cycle & deletable)
                    traces.add(trace)
                    if not trace and protected_witness is None:
                        protected_witness = list(path)
                return
            for nxt in sorted(adj[path[-1]]):
                if nxt != start and nxt not in path:
                    extend(path + (nxt,), used_second or edge(path[-1], nxt) == second)

        extend((start, current), False)
    singleton = {next(iter(t)) for t in traces if len(t) == 1}
    P, Q = set(X[:2]), set(X[2:])
    U, W = set(Y[:2]), set(Y[2:])
    RR = set(R)
    formula = (
        {edge(p, q) for p in RR for q in P | U | W}
        | {edge(p, q) for p in P for q in Q}
        | {edge(p, q) for p in U for q in W}
        | {edge(p, q) for p, q in combinations(W, 2)}
    )
    return {
        "m": m, "r": r, "vertices": len(V), "edges": len(eplus),
        "trace_sizes": dict(sorted(Counter(map(len, traces)).items())),
        "singleton_count": len(singleton), "formula_count": len(formula),
        "formula_minus_singleton": sorted(formula - singleton),
        "singleton_minus_formula": sorted(singleton - formula),
        "formula_hits_all": all(not t.isdisjoint(formula) for t in traces),
        "singleton_hits_all": all(not t.isdisjoint(singleton) for t in traces),
        "protected_witness": protected_witness,
    }


if __name__ == "__main__":
    results = [instance(m, r) for m in range(3, 6) for r in range(0, 4)]
    print(json.dumps({
        "schema": "amra.erdos809.round9.parameter-probe.v1",
        "classification": "bounded discovery evidence only",
        "results": results,
    }, indent=2, sort_keys=True))
