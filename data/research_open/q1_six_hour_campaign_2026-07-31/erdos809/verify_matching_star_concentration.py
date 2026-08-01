#!/usr/bin/env python3
"""Finite guards for weighted matching--star concentration."""

from __future__ import annotations

import random


Edge = tuple[int, int]


def edge(x: int, y: int) -> Edge:
    if x == y:
        raise ValueError("distinct endpoints required")
    return (x, y) if x < y else (y, x)


def greedy_maximal_matching(
    vertex_count: int, weights: dict[Edge, int]
) -> list[Edge]:
    used: set[int] = set()
    matching: list[Edge] = []
    for x, y in sorted(weights, key=lambda e: (-weights[e], e)):
        if x not in used and y not in used:
            matching.append((x, y))
            used.add(x)
            used.add(y)
    return matching


def audit(
    vertex_count: int,
    weights: dict[Edge, int],
    types: dict[tuple[int, int], int],
) -> dict[str, int]:
    if not weights:
        raise ValueError("nonempty weighted graph required")
    if any(weight <= 0 for weight in weights.values()):
        raise ValueError("positive weights required")
    matching = greedy_maximal_matching(vertex_count, weights)
    endpoints = {vertex for e in matching for vertex in e}
    assert matching
    assert all(x in endpoints or y in endpoints for x, y in weights)

    total_weight = sum(weights.values())
    star_weight = {
        vertex: sum(
            weight
            for (x, y), weight in weights.items()
            if vertex in (x, y)
        )
        for vertex in endpoints
    }
    centre = max(star_weight, key=star_weight.get)
    best_star = star_weight[centre]
    assert 2 * len(matching) * best_star >= total_weight

    type_weight = [0, 0]
    for (x, y), weight in weights.items():
        if centre not in (x, y):
            continue
        leaf = y if x == centre else x
        branch = types[(centre, leaf)]
        assert branch in (0, 1)
        type_weight[branch] += weight
    coherent_weight = max(type_weight)
    assert 4 * len(matching) * coherent_weight >= total_weight

    return {
        "vertices": vertex_count,
        "edges": len(weights),
        "matching_size": len(matching),
        "total_weight": total_weight,
        "best_star_weight": best_star,
        "coherent_weight": coherent_weight,
    }


def random_audits(seed: int = 809_36, trials: int = 10_000) -> int:
    rng = random.Random(seed)
    for _ in range(trials):
        vertex_count = rng.randint(2, 35)
        weights: dict[Edge, int] = {}
        types: dict[tuple[int, int], int] = {}
        for x in range(vertex_count):
            for y in range(x + 1, vertex_count):
                if rng.random() < 0.2:
                    weights[(x, y)] = rng.randint(1, 100)
                    branch = rng.randint(0, 1)
                    types[(x, y)] = branch
                    types[(y, x)] = branch
        if not weights:
            x, y = rng.sample(range(vertex_count), 2)
            weights[edge(x, y)] = rng.randint(1, 100)
            branch = rng.randint(0, 1)
            types[(x, y)] = branch
            types[(y, x)] = branch
        audit(vertex_count, weights, types)
    return trials


def main() -> None:
    random_count = random_audits()
    print(
        {
            "schema": "amra.erdos809.matching-star-concentration.v1",
            "random_weighted_graphs": random_count,
            "status": "PASS",
            "scope": "finite weighted-cover guards only; Erdos #809 remains open",
        }
    )


if __name__ == "__main__":
    main()
