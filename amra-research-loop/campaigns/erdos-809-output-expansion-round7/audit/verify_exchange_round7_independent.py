#!/usr/bin/env python3
"""Independent exhaustive audit of Erdos-809 output-expansion round 7.

Unlike the author search, this verifier does not use deletion-set bit masks.
It constructs the bad-C7 trace hypergraph and directly enumerates every
deletion set for every unprotected assignment.  Deterministic deleted-graph
replays cross-check the independently proved trace/hitting equivalence.
"""

from collections import Counter
from itertools import combinations


def edge(u, v):
    return tuple(sorted((u, v)))


X = tuple(f"x{i}" for i in range(1, 5))
Y = tuple(f"y{i}" for i in range(1, 5))
A = frozenset(("v",) + X + Y + ("r1", "r2"))
B0 = frozenset(("b", "c", "z"))
V0 = tuple(sorted(A | B0))
V = tuple(sorted(set(V0) | {"w", "u"}))

removed = {edge("x1", "x2"), edge("y1", "y2")}
old_edges = {
    edge(p, q) for p, q in combinations(A, 2)
    if not ((p in X and q in Y) or (p in Y and q in X))
    and edge(p, q) not in removed
}
old_edges.update(edge("b", p) for p in X)
old_edges.update(edge("c", q) for q in Y)
old_edges.add(edge("b", "z"))
old_edges.update(edge("z", p) for p in X)
old_edges = frozenset(old_edges)

all_incident = frozenset(
    {edge(q, p) for q in ("w", "u") for p in V0 if p != "v"}
    | {edge("w", "u")}
)
required = frozenset({edge("w", "x1"), edge("u", "x2")})
forbidden = frozenset({
    edge("w", "c"), edge("u", "c"), edge("w", "z"), edge("u", "z"),
    edge("w", "y1"), edge("u", "y2"),
})
optional = tuple(sorted(all_incident-required-forbidden))

colour_pairs = tuple(
    [(edge("b", f"x{i}"), edge("c", f"y{i}")) for i in range(1, 5)]
    + [(edge("w", "x1"), edge("c", "y1")),
       (edge("u", "x2"), edge("c", "y2"))]
)
repeated_old = frozenset(e for pair in colour_pairs[:4] for e in pair)
v_incident = frozenset(e for e in old_edges if "v" in e)
deletable = tuple(sorted(old_edges-v_incident-repeated_old))

# Independent domain audit.
assert len(V) == 16 and len(old_edges) == 50
assert len(all_incident) == 27
assert required.isdisjoint(forbidden)
assert len(optional) == 19
assert len(v_incident) == 10 and len(repeated_old) == 8
assert v_incident.isdisjoint(repeated_old)
assert len(deletable) == 32
assert set(deletable) | set(v_incident) | set(repeated_old) == set(old_edges)


def adjacency(edges):
    adj = {v: set() for v in V}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


class ProtectedFound(Exception):
    pass


def bad_traces(edges, stop_on_protected=True):
    """All distinct intersections of bad C7s with the deletable-old domain."""
    adj = adjacency(edges)
    traces = set()
    for first, second in colour_pairs:
        start, nxt = first

        def dfs(path, contains_second):
            if len(path) == 7:
                if start not in adj[path[-1]]:
                    return
                closing = edge(path[-1], start)
                if not (contains_second or closing == second):
                    return
                cycle = {
                    edge(path[i], path[(i+1) % 7]) for i in range(7)
                }
                trace = frozenset(cycle & set(deletable))
                traces.add(trace)
                if stop_on_protected and not trace:
                    raise ProtectedFound
                return
            for q in sorted(adj[path[-1]]):
                if q == start or q in path:
                    continue
                dfs(path+(q,), contains_second or edge(path[-1], q) == second)

        try:
            dfs((start, nxt), first == second)
        except ProtectedFound:
            return {frozenset()}
    return traces


def has_bad_c7(edges):
    """Independent early-exit replay after a concrete deletion."""
    adj = adjacency(edges)
    for first, second in colour_pairs:
        start, nxt = first

        def dfs(path, contains_second):
            if len(path) == 7:
                return start in adj[path[-1]] and (
                    contains_second or edge(path[-1], start) == second
                )
            for q in adj[path[-1]]:
                if q == start or q in path:
                    continue
                if dfs(path+(q,), contains_second or edge(path[-1], q) == second):
                    return True
            return False

        if dfs((start, nxt), first == second):
            return True
    return False


def audit_mode(deletion_count):
    choose = 13+deletion_count
    assignments = 0
    protected = 0
    candidates = 0
    unprotected_records = []
    deletion_sets = tuple(combinations(deletable, deletion_count))

    for chosen in combinations(optional, choose):
        assignments += 1
        eplus = frozenset(set(old_edges) | set(required) | set(chosen))
        traces = bad_traces(eplus)
        if frozenset() in traces:
            protected += 1
            continue

        safe_here = 0
        # Exhaust every deletion set in the independently built trace
        # hypergraph.  Direct graph replay is an implementation cross-check;
        # the exact equivalence itself is proved in the audit note.
        replay_indices = {0, len(deletion_sets)-1}
        replay_indices.update(
            i*(len(deletion_sets)-1)//15 for i in range(16)
        )
        for deletion_index, deleted_tuple in enumerate(deletion_sets):
            deleted = frozenset(deleted_tuple)
            hits = all(not trace.isdisjoint(deleted) for trace in traces)
            if deletion_index in replay_indices:
                direct_safe = not has_bad_c7(eplus-deleted)
                assert hits == direct_safe
            safe_here += int(hits)
        candidates += safe_here
        unprotected_records.append((
            tuple(sorted(set(optional)-set(chosen))), traces, safe_here
        ))

    return {
        "assignments": assignments,
        "deletion_sets": len(deletion_sets),
        "protected": protected,
        "candidates": candidates,
        "unprotected": unprotected_records,
    }


mode2 = audit_mode(2)
assert mode2["assignments"] == 3876
assert mode2["deletion_sets"] == 496
assert mode2["protected"] == 3860
assert mode2["candidates"] == 0

mode3 = audit_mode(3)
assert mode3["assignments"] == 969
assert mode3["deletion_sets"] == 4960
assert mode3["protected"] == 968
assert mode3["candidates"] == 0
assert len(mode3["unprotected"]) == 1

omitted, traces, safe_here = mode3["unprotected"][0]
assert omitted == (edge("b", "u"), edge("b", "w"), edge("u", "w"))
assert len(traces) == 93
assert Counter(map(len, traces)) == Counter({1: 21, 3: 72})
singletons = {next(iter(t)) for t in traces if len(t) == 1}
assert len(singletons) == 21
assert all(not trace.isdisjoint(singletons) for trace in traces)
assert safe_here == 0

print("PASS: independent full round-7 exchange audit")
print("mode2: 3876 x 496; protected 3860; candidates 0")
print("mode3: 969 x 4960; protected 968; candidates 0")
print("unique mode3 unprotected: 93 traces, 21 singleton, tau=21")
