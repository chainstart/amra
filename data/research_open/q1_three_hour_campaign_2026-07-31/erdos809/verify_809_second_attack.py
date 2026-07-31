#!/usr/bin/env python3
"""Finite guards for the second 2026-07-31 Erdős #809 attack.

The checks separate three assertions that must not be conflated:

1. the budgeted-defect inequality is false for an arbitrary admissible
   diameter-three witness A;
2. on the same graph, the witness produced by the maximum-degree branch
   of BCM Lemma 3.1 is aligned with the larger clique and has zero
   good-edge defect;
3. a sufficiently dense core supplies a pairwise C7-compatible family.

The first two checks use the four-bridge two-clique construction.  The
third is only a finite guard for the dense-core lemma proved on paper.
None of the checks proves Erdős #809.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import deque

Edge = tuple[int, int]


def edge(u: int, v: int) -> Edge:
    if u == v:
        raise ValueError((u, v))
    return (u, v) if u < v else (v, u)


def four_bridge_graph(
    p: int, q: int
) -> tuple[int, set[Edge], list[Edge], list[Edge], list[Edge]]:
    """Return G_{p,q}, its bridges, and the two generic-edge lists."""
    if p < q or q < 7 or p - q < 4:
        raise ValueError((p, q))
    n = p + q
    p_side = range(p)
    q_side = range(p, n)
    bridges = [edge(i, p + i) for i in range(4)]
    edges = {
        edge(u, v)
        for side in (p_side, q_side)
        for u, v in itertools.combinations(side, 2)
    }
    edges.update(bridges)
    p_generic = [
        edge(u, v) for u, v in itertools.combinations(range(4, p), 2)
    ]
    q_generic = [
        edge(u, v)
        for u, v in itertools.combinations(range(p + 4, n), 2)
    ]
    return n, edges, bridges, p_generic, q_generic


def distances(n: int, edges: set[Edge], start: int) -> list[int]:
    neigh = [set() for _ in range(n)]
    for u, v in edges:
        neigh[u].add(v)
        neigh[v].add(u)
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for nxt in neigh[current]:
            if dist[nxt] < 0:
                dist[nxt] = dist[current] + 1
                queue.append(nxt)
    return dist


def arranged_colouring(
    p: int,
    q: int,
    bad_p: set[int],
    bad_q: set[int],
) -> tuple[set[Edge], dict[Edge, int], int]:
    """Pair as many bad Q-generic edges with bad P-generic edges as possible."""
    _, edges, _, p_generic, q_generic = four_bridge_graph(p, q)
    bad_p_edges = [
        item for item in p_generic if item[0] in bad_p and item[1] in bad_p
    ]
    bad_q_edges = [
        item for item in q_generic if item[0] in bad_q and item[1] in bad_q
    ]
    h = min(len(bad_p_edges), len(bad_q_edges))

    bad_p_edge_set = set(bad_p_edges)
    bad_q_edge_set = set(bad_q_edges)
    paired_p_order = bad_p_edges + [
        item for item in p_generic if item not in bad_p_edge_set
    ]
    paired_q_order = bad_q_edges + [
        item for item in q_generic if item not in bad_q_edge_set
    ]
    assert len(paired_p_order) >= len(paired_q_order)

    colours: dict[Edge, int] = {}
    next_colour = 0
    for q_item, p_item in zip(paired_q_order, paired_p_order):
        colours[q_item] = next_colour
        colours[p_item] = next_colour
        next_colour += 1
    for item in sorted(edges):
        if item not in colours:
            colours[item] = next_colour
            next_colour += 1
    return edges, colours, h


def colour_statistics(
    edges: set[Edge],
    colours: dict[Edge, int],
    witness: set[int],
) -> tuple[int, int, int]:
    good = {
        item for item in edges if item[0] in witness or item[1] in witness
    }
    good_colours = {colours[item] for item in good}
    return len(good), len(good_colours), len(good) - len(good_colours)


def arbitrary_witness_budget_guard(
    p: int = 120, q: int = 80
) -> dict[str, int | float | bool]:
    """Exhibit a legal A for which even budgeted defect fails quadratically."""
    n, edges, _, _, _ = four_bridge_graph(p, q)
    bad_size = q - 1
    r = bad_size // 2
    t = bad_size - r
    # All bridge endpoints stay in A, so B only uses generic vertices.
    bad_p = set(range(4, 4 + r))
    bad_q = set(range(p + 4, p + 4 + t))
    witness = set(range(n)) - bad_p - bad_q
    edges, colours, hidden_colours = arranged_colouring(
        p, q, bad_p, bad_q
    )

    assert len(witness) == p + 1
    assert all(
        max(distances(n, edges, vertex)[other] for other in witness) <= 3
        for vertex in witness
    )

    edge_count = len(edges)
    c1 = n / 2 + math.sqrt(edge_count - n * n / 4 + n / 2)
    assert len(witness) >= c1

    good_edges, good_colours, defect = colour_statistics(
        edges, colours, witness
    )
    target = edge_count / 2 + n / 2 * math.sqrt(
        edge_count - n * n / 4
    )
    surplus = good_edges - target

    # The missing good colours are precisely the paired colour classes
    # whose P-edge and Q-edge both lie in B.
    total_colours = len(set(colours.values()))
    assert total_colours - good_colours == hidden_colours
    assert hidden_colours == math.comb(r, 2)
    assert defect > surplus
    assert good_colours < target

    return {
        "vertices": n,
        "p": p,
        "q": q,
        "witness_size": len(witness),
        "BCM_C1": c1,
        "hidden_good_colours": hidden_colours,
        "good_edges": good_edges,
        "good_colours": good_colours,
        "good_edge_defect": defect,
        "BCM_finite_target": target,
        "good_edge_surplus": surplus,
        "defect_exceeds_surplus": defect > surplus,
        "passed": True,
    }


def canonical_witness_guard(
    p: int = 120, q: int = 80
) -> dict[str, int | float | bool]:
    """Check the maximum-degree BCM witness on the same construction."""
    n, edges, _, _, _ = four_bridge_graph(p, q)
    empty: set[int] = set()
    edges, colours, _ = arranged_colouring(p, q, empty, empty)

    # p_0 is a bridge endpoint in the larger clique.  Its closed
    # neighbourhood is P union {q_0}.
    p0 = 0
    q0 = p
    witness = set(range(p)) | {q0}
    closed_neighbourhood = {p0}
    for item in edges:
        if p0 in item:
            closed_neighbourhood.add(item[0] if item[1] == p0 else item[1])
    assert witness == closed_neighbourhood

    degrees = [0] * n
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    assert degrees[p0] == max(degrees) == p

    edge_count = len(edges)
    c1 = n / 2 + math.sqrt(edge_count - n * n / 4 + n / 2)
    assert max(degrees) >= c1 - 1
    assert len(witness) >= c1

    good_edges, good_colours, defect = colour_statistics(
        edges, colours, witness
    )
    assert defect == 0
    assert good_edges == math.comb(p, 2) + q + 3
    assert good_colours == good_edges

    return {
        "vertices": n,
        "maximum_degree": max(degrees),
        "witness_size": len(witness),
        "BCM_C1": c1,
        "good_edges": good_edges,
        "good_colours": good_colours,
        "good_edge_defect": defect,
        "maximum_degree_branch_applies": True,
        "passed": True,
    }


def cycles_7(n: int, edges: set[Edge]) -> list[frozenset[Edge]]:
    """Enumerate unoriented C7 edge sets."""
    found: set[frozenset[Edge]] = set()

    def extend(path: tuple[int, ...]) -> None:
        if len(path) == 7:
            if edge(path[-1], path[0]) in edges:
                found.add(
                    frozenset(
                        edge(path[index], path[(index + 1) % 7])
                        for index in range(7)
                    )
                )
            return
        for nxt in range(path[0] + 1, n):
            if nxt in path or edge(path[-1], nxt) not in edges:
                continue
            extend(path + (nxt,))

    # The smallest cycle vertex is the root.  This is enough for a guard,
    # and the edge-set container removes the two orientations.
    for root in range(n):
        extend((root,))
    return list(found)


def dense_core_compatibility_guard(
    vertices: int = 9,
) -> dict[str, int | bool]:
    """Check every order-nine threshold graph up to isomorphism.

    At order nine, 2*delta-m >= 5 means delta >= 7.  Equivalently, the
    complement has maximum degree at most one, so it is a matching.
    Matching size is the only isomorphism parameter.
    """
    if vertices != 9:
        raise ValueError(vertices)
    checked_pairs = 0
    isomorphism_types = 0
    for matching_size in range(vertices // 2 + 1):
        edges = {
            edge(u, v) for u, v in itertools.combinations(range(vertices), 2)
        }
        for index in range(matching_size):
            edges.discard(edge(2 * index, 2 * index + 1))
        degrees = [0] * vertices
        for u, v in edges:
            degrees[u] += 1
            degrees[v] += 1
        assert 2 * min(degrees) - vertices >= 5
        cycles = cycles_7(vertices, edges)
        for left, right in itertools.combinations(sorted(edges), 2):
            assert any(left in cycle and right in cycle for cycle in cycles)
            checked_pairs += 1
        isomorphism_types += 1
    return {
        "vertices": vertices,
        "threshold_isomorphism_types": isomorphism_types,
        "edge_pairs_checked": checked_pairs,
        "passed": True,
    }


def main() -> None:
    result = {
        "arbitrary_witness_no_go": arbitrary_witness_budget_guard(),
        "canonical_BCM_witness": canonical_witness_guard(),
        "dense_core_compatibility": dense_core_compatibility_guard(),
        "scope": (
            "Finite guards verify constructions and a dense-core sanity "
            "check only; the existential budgeted-defect theorem and "
            "Erdos #809 remain open."
        ),
        "passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
