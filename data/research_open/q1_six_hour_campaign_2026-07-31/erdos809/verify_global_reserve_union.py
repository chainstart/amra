#!/usr/bin/env python3
"""Finite falsification guard for the global reserve-union reduction.

The generated objects model the B-side facts used by the proof:
colour endpoint sets are independent, every repeated active pair is
zero-shore, and a zero-shore reserve contains its missing stars and
neighbourhood rectangle.  They need not extend to full BCM witnesses.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import comb
from random import Random


Edge = tuple[int, int]


def edge(x: int, y: int) -> Edge:
    if x == y:
        raise ValueError("loops are excluded")
    return (x, y) if x < y else (y, x)


def all_pairs(vertices: tuple[int, ...]) -> set[Edge]:
    return {edge(x, y) for x, y in combinations(vertices, 2)}


def neighbours(vertex: int, graph_edges: set[Edge], order: int) -> set[int]:
    return {
        other
        for other in range(order)
        if other != vertex and edge(vertex, other) in graph_edges
    }


def zero_shore(base_pair: Edge, graph_edges: set[Edge], order: int) -> bool:
    left, right = base_pair
    for x in neighbours(left, graph_edges, order):
        for y in neighbours(right, graph_edges, order):
            if x != y and edge(x, y) in graph_edges:
                return False
    return True


def reserve(
    base_pair: Edge,
    graph_edges: set[Edge],
    order: int,
    is_zero: bool,
) -> set[Edge]:
    missing = all_pairs(tuple(range(order))) - graph_edges
    if not is_zero:
        return {base_pair}
    left, right = base_pair
    answer = {
        candidate
        for candidate in missing
        if left in candidate or right in candidate
    }
    answer.update(
        edge(x, y)
        for x in neighbours(left, graph_edges, order)
        for y in neighbours(right, graph_edges, order)
        if x != y
    )
    assert answer <= missing
    return answer


def audit_instance(
    order: int, graph_edges: set[Edge], colours: tuple[tuple[int, ...], ...]
) -> bool:
    missing = all_pairs(tuple(range(order))) - graph_edges
    active_occurrences = [
        base_pair
        for vertices in colours
        for base_pair in all_pairs(vertices)
    ]
    multiplicity = Counter(active_occurrences)
    active = set(multiplicity)
    assert active <= missing

    zero = {
        base_pair
        for base_pair in active
        if zero_shore(base_pair, graph_edges, order)
    }
    if any(count > 1 and base_pair not in zero for base_pair, count in multiplicity.items()):
        raise ValueError("instance violates nonempty-shore uniqueness")
    repeated_zero = {
        base_pair for base_pair in zero if multiplicity[base_pair] > 1
    }

    reserves = {
        base_pair: reserve(
            base_pair, graph_edges, order, base_pair in zero
        )
        for base_pair in active
    }
    global_union = set().union(*reserves.values()) if reserves else set()
    defect = sum(max(len(vertices) - 1, 0) for vertices in colours)
    pair_occurrences = len(active_occurrences)
    repeated_zero_mass = sum(
        count - 1 for base_pair, count in multiplicity.items() if base_pair in zero
    )
    assert repeated_zero_mass == pair_occurrences - len(active)

    b_degrees = {
        vertex: len(neighbours(vertex, graph_edges, order))
        for vertex in range(order)
    }
    colour_incidence = {
        vertex: sum(vertex in vertices for vertices in colours)
        for vertex in range(order)
    }
    # Realize the only maximum-degree inequality used by Theorem 2.1:
    # d_A(x)+d_B(x) <= m-1.
    m = 1 + max(
        colour_incidence[vertex] + b_degrees[vertex]
        for vertex in range(order)
    )
    imbalance = m - order
    for mask in range(1 << order):
        cover = {vertex for vertex in range(order) if mask & (1 << vertex)}
        if not all(
            left in cover or right in cover for left, right in repeated_zero
        ):
            continue
        internal_missing = sum(
            left in cover and right in cover for left, right in missing
        )
        n_zero_outside = sum(
            bool(vertices) and set(vertices) <= cover for vertices in colours
        )
        outside_surplus = sum(
            comb(len(set(vertices) - cover) - 1, 2)
            for vertices in colours
            if len(set(vertices) - cover) >= 3
        )
        right_side = (
            internal_missing
            + imbalance * len(cover)
            - n_zero_outside
            - outside_surplus
        )
        assert defect - len(missing) <= right_side

    if len(global_union) >= defect:
        return False

    assert defect >= 2
    surplus = 1 + sum(
        comb(len(vertices) - 1, 2)
        for vertices in colours
        if vertices
    )
    assert repeated_zero_mass >= surplus

    zero_endpoints = {
        vertex for base_pair in zero for vertex in base_pair
    }
    incident = {
        base_pair
        for base_pair in missing
        if any(vertex in zero_endpoints for vertex in base_pair)
    }
    outside_credit = sum(
        comb(len(set(vertices) - zero_endpoints), 2)
        for vertices in colours
    )
    assert len(global_union) >= len(incident) + outside_credit
    burden = defect - outside_credit
    assert len(incident) <= burden - 1
    missing_degrees = {
        vertex: sum(vertex in base_pair for base_pair in missing)
        for vertex in range(order)
    }
    assert sum(missing_degrees[v] for v in zero_endpoints) < 2 * burden

    q_d = 0
    while comb(q_d + 1, 2) <= defect - 1:
        q_d += 1
    low_cover = {
        vertex
        for vertex in zero_endpoints
        if len(neighbours(vertex, graph_edges, order)) <= q_d
    }
    assert all(left in low_cover or right in low_cover for left, right in zero)
    low_incident = {
        base_pair
        for base_pair in missing
        if any(vertex in low_cover for vertex in base_pair)
    }
    low_outside_credit = sum(
        comb(len(set(vertices) - low_cover), 2)
        for vertices in colours
    )
    assert len(global_union) >= len(low_incident) + low_outside_credit
    return True


def independent_subsets(order: int, graph_edges: set[Edge]) -> list[tuple[int, ...]]:
    answer = []
    vertices = tuple(range(order))
    for size in range(1, min(order, 4) + 1):
        for candidate in combinations(vertices, size):
            if all_pairs(candidate).isdisjoint(graph_edges):
                answer.append(candidate)
    return answer


def random_audit(seed: int = 809_2, accepted_target: int = 4000) -> tuple[int, int]:
    rng = Random(seed)
    accepted = 0
    obstructed = 0
    attempts = 0
    while accepted < accepted_target and attempts < 200_000:
        attempts += 1
        order = rng.randint(3, 7)
        graph_edges = {
            edge(x, y)
            for x, y in combinations(range(order), 2)
            if rng.random() < 0.35
        }
        choices = independent_subsets(order, graph_edges)
        if not choices:
            continue
        colours = tuple(rng.choice(choices) for _ in range(rng.randint(1, 9)))
        active_occurrences = [
            base_pair
            for vertices in colours
            for base_pair in all_pairs(vertices)
        ]
        multiplicity = Counter(active_occurrences)
        if any(
            count > 1 and not zero_shore(base_pair, graph_edges, order)
            for base_pair, count in multiplicity.items()
        ):
            continue
        obstructed += int(audit_instance(order, graph_edges, colours))
        accepted += 1
    if accepted != accepted_target or obstructed == 0:
        raise AssertionError("random audit did not reach both target classes")
    return accepted, obstructed


def run() -> dict[str, object]:
    # Empty B-side graphs stress repeated zero-shore endpoint sets.
    deterministic = 0
    deterministic_obstructions = 0
    for order in range(3, 8):
        choices = independent_subsets(order, set())
        for multiplicity in range(1, 10):
            colours = tuple(choices[-1] for _ in range(multiplicity))
            deterministic_obstructions += int(
                audit_instance(order, set(), colours)
            )
            deterministic += 1
    accepted, obstructed = random_audit()
    return {
        "schema": "amra.erdos809.global-reserve-union.v1",
        "deterministic_instances": deterministic,
        "deterministic_obstructions": deterministic_obstructions,
        "random_accepted_instances": accepted,
        "random_obstructions": obstructed,
        "status": "PASS",
        "boundary": "B-side finite guards only; no full BCM extension claimed",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
