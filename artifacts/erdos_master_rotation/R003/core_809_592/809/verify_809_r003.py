#!/usr/bin/env python3
"""Finite guards for the new R003 #809 lemmas.

The exhaustive checks only verify explicit templates and algebraic structural
bounds.  They are not used to extrapolate the asymptotic theorem.
"""

from __future__ import annotations

import itertools
import json


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


def one_anchor_witness(e1, e2, a_side, b_side, p, q, anchor):
    """Explicit C7 templates for the one-anchor fan lemma."""
    a1, b1 = split_cross_edge(e1)
    a2, b2 = split_cross_edge(e2)

    if a1 == a2:
        c = next(a for a in a_side if a not in {p, q, a1})
        return [p, q, b1, a1, b2, c, anchor]

    if b1 == b2:
        x = next(b for b in b_side if b not in {b1, anchor})
        return [p, q, x, a1, b1, a2, anchor]

    return [p, q, b1, a1, b2, a2, anchor]


def verify_one_anchor(a_size, b_size, p_cross_neighbors):
    a_side = [("A", i) for i in range(a_size)]
    b_side = [("B", i) for i in range(b_size)]
    p, q = a_side[:2]
    s_set = set(b_side[:p_cross_neighbors])
    anchor = b_side[0]

    edges = {
        edge(a, b)
        for a in a_side
        for b in b_side
        if a != p or b in s_set
    }
    edges.add(edge(p, q))
    family = {
        edge(a, b)
        for a in a_side
        if a not in {p, q}
        for b in b_side
        if b != anchor
    }

    case_counts = {"same_A": 0, "same_B": 0, "disjoint": 0}
    checked = 0
    for e1, e2 in itertools.combinations(family, 2):
        a1, b1 = split_cross_edge(e1)
        a2, b2 = split_cross_edge(e2)
        case = "same_A" if a1 == a2 else "same_B" if b1 == b2 else "disjoint"
        cycle = one_anchor_witness(
            e1, e2, a_side, b_side, p, q, anchor
        )
        assert len(cycle) == 7 and len(set(cycle)) == 7
        ce = cycle_edges(cycle)
        assert ce <= edges
        assert e1 in ce and e2 in ce and edge(p, q) in ce
        case_counts[case] += 1
        checked += 1

    assert len(family) == (a_size - 2) * (b_size - 1)
    return {
        "a_size": a_size,
        "b_size": b_size,
        "p_cross_neighbors": p_cross_neighbors,
        "family_size": len(family),
        "checked_edge_pairs": checked,
        "case_counts": case_counts,
        "passed": True,
    }


def has_length_three_path_avoiding(n, edges, u, v, forbidden):
    allowed = set(range(n)) - set(forbidden)
    if u not in allowed or v not in allowed:
        return False
    for x in allowed - {u, v}:
        if edge(u, x) not in edges:
            continue
        for y in allowed - {u, v, x}:
            if edge(x, y) in edges and edge(y, v) in edges:
                return True
    return False


def verify_neighborhood_obstruction_exhaustive(n):
    """Exhaust all labelled n-vertex graphs and check the dichotomy bounds."""
    all_edges = [edge(i, j) for i in range(n) for j in range(i + 1, n)]
    checked_obstructions = 0
    nonempty_intersection_obstructions = 0

    for mask in range(1 << len(all_edges)):
        edges = {
            all_edges[i]
            for i in range(len(all_edges))
            if mask & (1 << i)
        }
        neighborhoods = {
            u: {v for v in range(n) if edge(u, v) in edges}
            for u in range(n)
        }
        delta = min(map(len, neighborhoods.values()))

        for u, v in itertools.combinations(range(n), 2):
            # In the reduction u and v are the opposite endpoints of two
            # edge-distance-two edges, hence they are nonadjacent.
            if edge(u, v) in edges:
                continue
            remaining = [x for x in range(n) if x not in {u, v}]
            for s_size in range(min(3, len(remaining)) + 1):
                for forbidden_tuple in itertools.combinations(remaining, s_size):
                    forbidden = set(forbidden_tuple)
                    if has_length_three_path_avoiding(
                        n, edges, u, v, forbidden
                    ):
                        continue

                    p_set = neighborhoods[u] - forbidden
                    q_set = neighborhoods[v] - forbidden
                    # A distinct P--Q edge would itself give the forbidden path.
                    assert all(
                        x == y or edge(x, y) not in edges
                        for x in p_set
                        for y in q_set
                    )
                    intersection = p_set & q_set
                    if not intersection:
                        z_size = n - len(p_set | q_set)
                        assert z_size <= n - 2 * delta + 2 * s_size
                    else:
                        nonempty_intersection_obstructions += 1
                        r_size = len(intersection)
                        w_size = len((p_set | q_set) - intersection)
                        assert r_size >= 3 * delta - n - 2 * s_size
                        assert w_size <= 2 * n - 4 * delta + 2 * s_size
                    checked_obstructions += 1

    return {
        "n": n,
        "labelled_graphs": 1 << len(all_edges),
        "checked_no_length3_certificates": checked_obstructions,
        "nonempty_intersection_certificates":
            nonempty_intersection_obstructions,
        "passed": True,
    }


def main():
    one_anchor = [
        verify_one_anchor(a, b, t)
        for a in range(4, 9)
        for b in range(3, 9)
        for t in range(1, b + 1)
    ]
    obstruction = [
        verify_neighborhood_obstruction_exhaustive(n)
        for n in (4, 5, 6)
    ]
    print(
        json.dumps(
            {
                "claims": [
                    "one-anchor exact C7 fan lemma",
                    "length-three neighborhood obstruction bounds"
                ],
                "one_anchor_summary": {
                    "instances": len(one_anchor),
                    "a_size_range": [4, 8],
                    "b_size_range": [3, 8],
                    "p_cross_neighbor_range_for_each_b": "1..b",
                    "checked_edge_pairs": sum(
                        item["checked_edge_pairs"] for item in one_anchor
                    ),
                    "all_passed": all(item["passed"] for item in one_anchor)
                },
                "neighborhood_obstruction_instances": obstruction,
                "passed": True
            },
            indent=2,
            sort_keys=True
        )
    )


if __name__ == "__main__":
    main()
