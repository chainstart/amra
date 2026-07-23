#!/usr/bin/env python3
"""Finite checks for the #809 low-cross endpoint audit.

This is a guard against transcription errors, not a replacement for the
symbolic proofs in STABILITY_COUNTEREXAMPLE.md.
"""

from __future__ import annotations

import itertools
import json
from math import comb


def edge(u, v):
    return frozenset((u, v))


def cycle_edges(cycle):
    return {
        edge(cycle[i], cycle[(i + 1) % len(cycle)])
        for i in range(len(cycle))
    }


def split_cross_edge(e):
    u, v = tuple(e)
    if u[0] == "A":
        return u, v
    return v, u


def star_swap_graph(m):
    """Return the balanced star-swap construction G_{m,t}."""
    assert m >= 12
    a_side = [("A", i) for i in range(m)]
    b_side = [("B", i) for i in range(m)]
    p = a_side[0]
    t = m // 4
    s_set = set(b_side[:t])
    t_set = set(a_side[1 : m - t + 2])
    assert len(t_set) == m - t + 1

    edges = {
        edge(a, b)
        for a in a_side
        for b in b_side
        if a != p or b in s_set
    }
    edges.update(edge(p, a) for a in t_set)
    return a_side, b_side, p, s_set, t_set, edges


def fan_witness(e1, e2, a_side, b_side, p, q, s_set):
    """The three explicit seven-cycle templates in the fan lemma."""
    a1, b1 = split_cross_edge(e1)
    a2, b2 = split_cross_edge(e2)

    if a1 == a2:
        c = next(a for a in a_side if a not in {p, q, a1})
        s = next(b for b in s_set if b not in {b1, b2})
        return [p, q, b1, a1, b2, c, s]

    if b1 == b2:
        s = next(b for b in s_set if b != b1)
        x = next(b for b in b_side if b not in {b1, s})
        return [p, q, x, a1, b1, a2, s]

    s = next(b for b in s_set if b not in {b1, b2})
    return [p, q, b1, a1, b2, a2, s]


def verify_star_swap(m):
    a_side, b_side, p, s_set, t_set, edges = star_swap_graph(m)
    q = min(t_set)
    family = {
        edge(a, b)
        for a in a_side
        if a not in {p, q}
        for b in b_side
    }

    checked_pairs = 0
    for e1, e2 in itertools.combinations(family, 2):
        cycle = fan_witness(e1, e2, a_side, b_side, p, q, s_set)
        assert len(cycle) == 7 and len(set(cycle)) == 7
        ce = cycle_edges(cycle)
        assert ce <= edges
        assert e1 in ce and e2 in ce and edge(p, q) in ce
        checked_pairs += 1

    degrees = {
        v: sum(v in e for e in edges)
        for v in a_side + b_side
    }
    t = len(s_set)
    removed_cross_edges = m - t
    added_internal_edges = m - t + 1
    independent_b_two_clique_lower_bound = (
        comb(m // 2, 2) + comb(m - m // 2, 2)
    )
    local_common_neighborhood_family = (m - 2) * t

    assert len(edges) == m * m + 1
    assert min(degrees.values()) == m - 1
    assert degrees[p] == m + 1
    assert removed_cross_edges + added_internal_edges == 2 * (m - t) + 1
    assert all(p in e for e in edges if all(v[0] == "A" for v in e))
    assert sum(edge(p, b) in edges for b in b_side) == t
    assert len(family) == (m - 2) * m
    assert local_common_neighborhood_family < m * m / 2
    assert len(family) > m * m / 2
    assert independent_b_two_clique_lower_bound == (m - 1) ** 2 // 4

    return {
        "m": m,
        "n": 2 * m,
        "t": t,
        "edge_count": len(edges),
        "minimum_degree": min(degrees.values()),
        "distance_from_displayed_Kmm": 2 * (m - t) + 1,
        "lower_bound_distance_from_every_two_clique_graph":
            independent_b_two_clique_lower_bound,
        "low_cross_degree_of_p": t,
        "robust_common_neighborhood_family_size":
            local_common_neighborhood_family,
        "fan_family_size": len(family),
        "checked_fan_edge_pairs": checked_pairs,
        "passed": True,
    }


def verify_sparse_robust_bound(m):
    """A regular circulant satisfying the robust lemma with only O(m) output."""
    assert m % 2 == 0 and m >= 12
    d = m // 2 + 4
    a_side = [("A", i) for i in range(m)]
    b_side = [("B", i) for i in range(m)]
    p = a_side[0]
    q = a_side[m // 2]
    offsets = set(range(d))
    edges = {
        edge(a_side[i], b_side[(i + j) % m])
        for i in range(m)
        for j in offsets
    }
    edges.add(edge(p, q))

    n_p = {b for b in b_side if edge(p, b) in edges}
    n_q = {b for b in b_side if edge(q, b) in edges}
    b_zero = n_p & n_q
    family = {
        edge(a, b)
        for a in a_side
        if a not in {p, q}
        for b in b_zero
        if edge(a, b) in edges
    }

    cross_degrees_a = [
        sum(edge(a, b) in edges for b in b_side)
        for a in a_side
    ]
    cross_degrees_b = [
        sum(edge(a, b) in edges for a in a_side)
        for b in b_side
    ]
    assert set(cross_degrees_a) == {d}
    assert set(cross_degrees_b) == {d}
    assert d > m / 2 + 3
    assert len(b_zero) == 2 * d - m == 8
    assert len(family) == 8 * (d - 2)

    return {
        "m": m,
        "cross_degree": d,
        "common_pq_neighborhood_size": len(b_zero),
        "robust_lemma_family_size": len(family),
        "family_size_over_m": len(family) / m,
        "passed": True,
    }


def main():
    star_instances = [verify_star_swap(m) for m in (12, 16, 20, 24)]
    circulant_instances = [
        verify_sparse_robust_bound(m) for m in (12, 16, 20, 24, 32, 40)
    ]
    print(
        json.dumps(
            {
                "claim": (
                    "The natural low-cross-endpoint => near-two-clique "
                    "dichotomy is false; a separate fan mechanism exists."
                ),
                "star_swap_instances": star_instances,
                "circulant_robust_bound_instances": circulant_instances,
                "passed": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
