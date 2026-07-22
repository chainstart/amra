#!/usr/bin/env python3
"""Solver-free certificate for the #635 two-layer canonical Hall obstruction."""

from __future__ import annotations

import json
from itertools import combinations


N = 867
S = (80, 150, 170, 240, 272, 450, 510, 578, 720, 816)
EXPECTED_CANONICAL = {75, 85, 225, 255, 289, 675, 765, 867}
FULL_MATCHING = {
    80: 75,
    150: 125,
    170: 85,
    240: 235,
    272: 255,
    450: 225,
    510: 425,
    578: 289,
    720: 675,
    816: 765,
}


def valuation_oddpart(value: int) -> tuple[int, int]:
    valuation = 0
    while value % 2 == 0:
        valuation += 1
        value //= 2
    return valuation, value


def conflict(left: int, right: int) -> bool:
    difference = abs(left - right)
    return difference >= 2 and max(left, right) % difference == 0


def canonical(value: int) -> tuple[int, int]:
    valuation, oddpart = valuation_oddpart(value)
    scale = 1 << valuation
    return (scale - 1) * oddpart, (scale + 1) * oddpart


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def main() -> None:
    assert all(not conflict(x, y) for x, y in combinations(S, 2))
    assert {valuation_oddpart(x)[0] for x in S} == {1, 4}
    endpoints = {endpoint for x in S for endpoint in canonical(x)}
    assert endpoints == EXPECTED_CANONICAL
    assert all(endpoint <= N for x in S for endpoint in canonical(x))
    assert len(endpoints) == 8 < len(S) == 10
    adjacency = {endpoint: set() for endpoint in endpoints}
    for x in S:
        left, right = canonical(x)
        adjacency[left].add(right)
        adjacency[right].add(left)
    reached = set()
    stack = [next(iter(endpoints))]
    while stack:
        vertex = stack.pop()
        if vertex in reached:
            continue
        reached.add(vertex)
        stack.extend(adjacency[vertex] - reached)
    assert reached == endpoints
    cycle_rank = len(S) - len(endpoints) + 1
    assert cycle_rank == 3
    assert len(set(FULL_MATCHING.values())) == len(S)
    assert all(
        target <= N and target % 2 == 1 and conflict(source, target)
        for source, target in FULL_MATCHING.items()
    )
    square_checks = 0
    for a in range(1, 8):
        for c in range(a + 1, 9):
            A, C = 1 << a, 1 << c
            for scale in range(1, 100, 2):
                oddparts = ((C - 1) * scale, (C + 1) * scale,
                            (A - 1) * scale, (A + 1) * scale)
                # A unit odd part would give distance 1, outside t=2.
                if 1 in oddparts:
                    continue
                square_checks += 1
                assert any(value > 1 and not is_prime(value) for value in oddparts)
    canonical_edges = [(*canonical(x), x) for x in S]
    print(json.dumps({
        "status": "PASS",
        "N": N,
        "independent_even_set": S,
        "valuation_layers": [1, 4],
        "canonical_edges_L_U_center": canonical_edges,
        "canonical_neighbour_count": len(endpoints),
        "set_size": len(S),
        "whole_set_canonical_Hall_deficiency": len(S) - len(endpoints),
        "canonical_graph_connected": True,
        "canonical_graph_cycle_rank": cycle_rank,
        "all_upper_canonical_neighbours_are_in_range": True,
        "full_odd_neighbour_matching": FULL_MATCHING,
        "proper_divisor_targets_used": sorted(
            target for source, target in FULL_MATCHING.items()
            if target not in canonical(source)
        ),
        "basic_two_layer_square_regression_checks": square_checks,
    }, indent=2))


if __name__ == "__main__":
    main()
