#!/usr/bin/env python3
"""Randomized mechanical check of the robust near-bipartite C7 lemma.

The mathematical proof is in 809_BIPARTITE_MODEL_LEMMA.md.  This script only
guards the explicit cycle templates and their avoidance conditions.
"""

from __future__ import annotations

import itertools
import json
import random


def edge(u: str, v: str) -> frozenset[str]:
    return frozenset((u, v))


def cycle_edges(cycle: tuple[str, ...]) -> set[frozenset[str]]:
    return {
        edge(cycle[i], cycle[(i + 1) % len(cycle)])
        for i in range(len(cycle))
    }


def robust_witness(
    first: tuple[str, str],
    second: tuple[str, str],
    a_vertices: tuple[str, ...],
    b_vertices: tuple[str, ...],
    graph_edges: set[frozenset[str]],
) -> tuple[str, ...]:
    a1, b1 = first
    a2, b2 = second
    p, q = "a0", "a1"

    def adjacent(u: str, v: str) -> bool:
        return edge(u, v) in graph_edges

    if a1 == a2:
        c = next(
            a
            for a in a_vertices
            if a not in {p, q, a1} and adjacent(a, b2)
        )
        x = next(
            b
            for b in b_vertices
            if b not in {b1, b2} and adjacent(c, b) and adjacent(p, b)
        )
        return (p, q, b1, a1, b2, c, x)

    if b1 == b2:
        x = next(
            b
            for b in b_vertices
            if b != b1 and adjacent(q, b) and adjacent(a1, b)
        )
        y = next(
            b
            for b in b_vertices
            if b not in {b1, x} and adjacent(p, b) and adjacent(a2, b)
        )
        return (p, q, x, a1, b1, a2, y)

    x = next(
        b
        for b in b_vertices
        if b not in {b1, b2} and adjacent(a1, b) and adjacent(a2, b)
    )
    return (p, q, b1, a1, x, a2, b2)


def generate_instance(rng: random.Random, a_size: int, b_size: int) -> dict[str, object]:
    a_vertices = tuple(f"a{i}" for i in range(a_size))
    b_vertices = tuple(f"b{i}" for i in range(b_size))
    p, q = "a0", "a1"

    # Dense random bipartite graph, retried until it satisfies the transparent
    # finite hypotheses used by the proof.
    for _ in range(10_000):
        graph_edges = {
            edge(a, b)
            for a in a_vertices
            for b in b_vertices
            if rng.random() < 0.86
        }
        graph_edges.add(edge(p, q))
        degrees_a = {
            a: sum(edge(a, b) in graph_edges for b in b_vertices)
            for a in a_vertices
        }
        degrees_b = {
            b: sum(edge(a, b) in graph_edges for a in a_vertices)
            for b in b_vertices
        }
        if min(degrees_a.values()) >= b_size // 2 + 4 and min(degrees_b.values()) >= 4:
            break
    else:
        raise RuntimeError("failed to sample an admissible dense instance")

    b0 = tuple(
        b
        for b in b_vertices
        if edge(p, b) in graph_edges and edge(q, b) in graph_edges
    )
    family = tuple(
        (a, b)
        for a in a_vertices
        if a not in {p, q}
        for b in b0
        if edge(a, b) in graph_edges
    )

    checked = 0
    for first, second in itertools.combinations(family, 2):
        cycle = robust_witness(
            first, second, a_vertices, b_vertices, graph_edges
        )
        assert len(cycle) == len(set(cycle)) == 7
        used = cycle_edges(cycle)
        assert used <= graph_edges
        assert edge(*first) in used
        assert edge(*second) in used
        checked += 1

    return {
        "a_size": a_size,
        "b_size": b_size,
        "minimum_A_to_B_degree": min(degrees_a.values()),
        "minimum_B_to_A_degree": min(degrees_b.values()),
        "common_pq_neighborhood_size": len(b0),
        "family_size": len(family),
        "checked_edge_pairs": checked,
        "passed": True,
    }


def main() -> None:
    rng = random.Random(809_2026)
    instances = [
        generate_instance(rng, a_size, b_size)
        for a_size in (12, 14, 16)
        for b_size in (12, 14, 16)
        for _ in range(3)
    ]
    print(
        json.dumps(
            {
                "claim": "robust near-bipartite C7 cycle templates",
                "instances": instances,
                "passed": all(item["passed"] for item in instances),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
