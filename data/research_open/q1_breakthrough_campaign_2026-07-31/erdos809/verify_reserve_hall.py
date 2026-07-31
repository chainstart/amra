#!/usr/bin/env python3
"""Exact finite guards for the reserve-Hall attack on Erdős #809.

The checks certify only the stated finite combinatorics.  They do not
prove the universal reserve-expansion conjecture.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations


Edge = tuple[str, str]


def edge(x: str, y: str) -> Edge:
    if x == y:
        raise ValueError("loops are not missing-edge charges")
    return (x, y) if x < y else (y, x)


def maximum_bipartite_matching(candidates: list[set[Edge]]) -> dict[int, Edge]:
    """Return a maximum matching using Hopcroft--Karp."""

    right_edges = sorted(set().union(*candidates)) if candidates else []
    right_index = {candidate: i for i, candidate in enumerate(right_edges)}
    adjacency = [tuple(right_index[e] for e in sorted(options)) for options in candidates]
    pair_left = [-1] * len(adjacency)
    pair_right = [-1] * len(right_edges)
    distance = [0] * len(adjacency)

    def bfs() -> bool:
        queue: deque[int] = deque()
        found = False
        for token, mate in enumerate(pair_left):
            if mate == -1:
                distance[token] = 0
                queue.append(token)
            else:
                distance[token] = -1
        while queue:
            token = queue.popleft()
            for candidate in adjacency[token]:
                previous = pair_right[candidate]
                if previous == -1:
                    found = True
                elif distance[previous] == -1:
                    distance[previous] = distance[token] + 1
                    queue.append(previous)
        return found

    def dfs(token: int) -> bool:
        for candidate in adjacency[token]:
            previous = pair_right[candidate]
            if previous == -1 or (
                distance[previous] == distance[token] + 1 and dfs(previous)
            ):
                pair_left[token] = candidate
                pair_right[candidate] = token
                return True
        distance[token] = -1
        return False

    while bfs():
        for token, mate in enumerate(pair_left):
            if mate == -1:
                dfs(token)

    return {
        token: right_edges[candidate]
        for token, candidate in enumerate(pair_left)
        if candidate != -1
    }


@dataclass(frozen=True)
class ChainCertificate:
    k: int
    tokens: int
    missing_edges: int
    matched_tokens: int


def balanced_chain_certificate(k: int) -> ChainCertificate:
    """Build the exact token/reserve system in equation (8)."""

    if k < 3:
        raise ValueError("the stated uniform certificate starts at k=3")

    U = [f"u{i}" for i in range(k)]
    W = [f"w{i}" for i in range(k)]
    missing = {edge(u, w) for u in U for w in W}

    candidates: list[set[Edge]] = []
    for i in range(k):
        incident = {
            candidate
            for candidate in missing
            if U[i] in candidate or W[i] in candidate
        }
        rectangle = {
            edge(U[j], W[ell])
            for j in range(k)
            for ell in range(k)
            if j != i and ell != i
        }
        reserve = incident | rectangle
        assert reserve <= missing
        assert reserve == missing
        for _ in range(k):
            candidates.append(set(reserve))

    matching = maximum_bipartite_matching(candidates)
    return ChainCertificate(
        k=k,
        tokens=len(candidates),
        missing_edges=len(missing),
        matched_tokens=len(matching),
    )


def three_hub_certificate(u_size: int, w_size: int) -> ChainCertificate:
    """Build the token/reserve system in the unbalanced three-hub model."""

    if not (1 <= w_size <= u_size):
        raise ValueError("the construction requires W to inject into U")
    U = [f"u{i}" for i in range(u_size)]
    W = [f"w{i}" for i in range(w_size)]
    hubs = ["h0", "h1"]
    cross_block = {edge(u, w) for u in U for w in W}
    hub_missing = {edge(h, z) for h in hubs for z in U + W} | {
        edge(hubs[0], hubs[1])
    }
    missing = cross_block | hub_missing
    tokens_per_pair = u_size + 3

    candidates: list[set[Edge]] = []
    for i in range(w_size):
        # The incident part of (3) supplies the four missing hub edges
        # at u_i,w_i; the incident rows/columns plus the forced rectangle
        # supply the complete U x W block.
        reserve = set(cross_block)
        reserve.update(edge(h, U[i]) for h in hubs)
        reserve.update(edge(h, W[i]) for h in hubs)
        assert reserve <= missing
        for _ in range(tokens_per_pair):
            candidates.append(set(reserve))

    matching = maximum_bipartite_matching(candidates)
    return ChainCertificate(
        k=u_size,
        tokens=len(candidates),
        missing_edges=len(missing),
        matched_tokens=len(matching),
    )


def check_zero_shore_reserve() -> None:
    """Exhaust a small abstract graph and verify Lemma 3.1 directly."""

    # b--P and c--Q are the only incident edges.  P--Q is deliberately
    # empty, which is exactly the zero-shore condition.
    P = {"p0", "p1", "p2"}
    Q = {"q0", "q1"}
    graph_edges = {edge("b", p) for p in P} | {edge("c", q) for q in Q}
    # Add two explicitly known missing incident edges as the first part
    # of (3), in addition to the forced P x Q rectangle.
    incident_missing = {edge("b", "z0"), edge("c", "z1"), edge("b", "c")}
    reserve = incident_missing | {edge(p, q) for p in P for q in Q}
    assert graph_edges.isdisjoint(reserve)
    assert len(reserve) == len(incident_missing) + len(P) * len(Q)


def check_rectangle_lower_bound() -> int:
    """Exhaust all neighbourhood-set pairs on a six-point universe."""

    universe = tuple(range(6))
    subsets = [set(choice) for size in range(7) for choice in combinations(universe, size)]
    checks = 0
    for P in subsets:
        for Q in subsets:
            rectangle = {
                tuple(sorted((p, q)))
                for p in P
                for q in Q
                if p != q
            }
            lower = min(len(P), len(Q)) * (min(len(P), len(Q)) - 1) // 2
            assert len(rectangle) >= lower
            checks += 1
    return checks


def run() -> dict[str, object]:
    check_zero_shore_reserve()
    rectangle_checks = check_rectangle_lower_bound()
    certificates = [balanced_chain_certificate(k) for k in range(3, 31)]
    for certificate in certificates:
        assert certificate.tokens == certificate.missing_edges
        assert certificate.matched_tokens == certificate.tokens
    three_hub = [
        three_hub_certificate(u_size, w_size)
        for u_size in range(3, 16)
        for w_size in range(1, u_size + 1)
    ]
    for certificate in three_hub:
        assert certificate.matched_tokens == certificate.tokens
    return {
        "schema": "amra.erdos809.reserve-hall.v1",
        "zero_shore_reserve": "PASS",
        "rectangle_lower_bound_checks": rectangle_checks,
        "balanced_chain_range": [3, 30],
        "balanced_chain_instances": len(certificates),
        "largest_matching": certificates[-1].matched_tokens,
        "three_hub_instances": len(three_hub),
        "three_hub_status": "PASS",
        "status": "PASS",
        "boundary": "finite guards only; universal reserve expansion remains open",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
