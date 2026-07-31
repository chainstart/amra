#!/usr/bin/env python3
"""Finite guards for the sixth 2026-07-31 Erdos #809 attack.

The main guard is a three-hub, two-clique family satisfying the finite
Case-1 structural contract. It has quadratic zero-shore excess and
linear overlap on one fixed missing A-pair, while retaining an aligned
clique core.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter


Vertex = tuple[str, int]
Edge = frozenset[Vertex]


def edge(left: Vertex, right: Vertex) -> Edge:
    return frozenset((left, right))


def build_three_hub_graph(
    p: int = 18, q: int = 13, t: int = 8
) -> dict[str, object]:
    """Construct C1, C2 and three X/Y-complete connector hubs."""
    sizes = {
        "U": t - 3,
        "X": p + 3 - t,
        "W": q - t,
        "Y": t,
        "H": 3,
    }
    assert min(sizes.values()) >= 3
    groups = {
        name: [(name, index) for index in range(size)]
        for name, size in sizes.items()
    }
    vertices = sum(groups.values(), [])
    graph_edges: set[Edge] = set()
    for clique in (
        groups["U"] + groups["X"],
        groups["W"] + groups["Y"],
    ):
        graph_edges.update(
            edge(left, right)
            for left, right in itertools.combinations(clique, 2)
        )
    for hub in groups["H"]:
        graph_edges.update(
            edge(hub, item) for item in groups["X"] + groups["Y"]
        )
    adjacency = {
        item: {
            other
            for other in vertices
            if other != item and edge(item, other) in graph_edges
        }
        for item in vertices
    }
    return {
        "p": p,
        "q": q,
        "t": t,
        "groups": groups,
        "vertices": vertices,
        "edges": graph_edges,
        "adjacency": adjacency,
    }


def exact_four_internal_sets(
    first: Vertex,
    second: Vertex,
    adjacency: dict[Vertex, set[Vertex]],
) -> set[frozenset[Vertex]]:
    """Internal vertex sets of all simple exact-four paths."""
    paths: set[frozenset[Vertex]] = set()
    for one in adjacency[first] - {second}:
        for two in adjacency[one] - {first, second}:
            if two == one:
                continue
            for three in (adjacency[two] & adjacency[second]) - {
                first,
                one,
            }:
                if three in {second, two}:
                    continue
                paths.add(frozenset((one, two, three)))
    return paths


def l4_two_guard(graph: dict[str, object]) -> dict[str, int | bool]:
    """Check L4(2) through the path-hypergraph transversal condition."""
    vertices = graph["vertices"]
    adjacency = graph["adjacency"]
    assert isinstance(vertices, list)
    assert isinstance(adjacency, dict)
    checked_pairs = 0
    checked_deletions = 0
    minimum_path_sets: int | None = None
    for first, second in itertools.combinations(vertices, 2):
        path_sets = exact_four_internal_sets(first, second, adjacency)
        assert path_sets
        minimum_path_sets = (
            len(path_sets)
            if minimum_path_sets is None
            else min(minimum_path_sets, len(path_sets))
        )
        eligible = [item for item in vertices if item not in {first, second}]
        for deletion_size in range(3):
            for deleted_tuple in itertools.combinations(
                eligible, deletion_size
            ):
                deleted = set(deleted_tuple)
                assert any(
                    not (set(path) & deleted) for path in path_sets
                )
                checked_deletions += 1
        checked_pairs += 1
    return {
        "vertex_pairs": checked_pairs,
        "deletion_checks": checked_deletions,
        "minimum_exact_four_internal_sets": minimum_path_sets or 0,
        "passed": True,
    }


def has_length_three(
    first: Vertex,
    second: Vertex,
    adjacency: dict[Vertex, set[Vertex]],
) -> bool:
    for one in adjacency[first] - {second}:
        for two in (adjacency[one] & adjacency[second]) - {first}:
            if two != one:
                return True
    return False


def linked_two_three(
    first_edge: Edge,
    second_edge: Edge,
    adjacency: dict[Vertex, set[Vertex]],
) -> bool:
    """Exact induced-edge C7 / disjoint (2,3)-linkage test."""
    first = tuple(first_edge)
    second = tuple(second_edge)
    for pairing in (
        ((first[0], second[0]), (first[1], second[1])),
        ((first[0], second[1]), (first[1], second[0])),
    ):
        for short_index in range(2):
            short = pairing[short_index]
            long = pairing[1 - short_index]
            for middle in (
                adjacency[short[0]] & adjacency[short[1]]
            ) - set(first + second):
                short_vertices = {short[0], middle, short[1]}
                for one in adjacency[long[0]] - short_vertices - {
                    long[1]
                }:
                    for two in (
                        adjacency[one] & adjacency[long[1]]
                    ) - short_vertices - {long[0], one}:
                        if two != one:
                            return True
    return False


def contract_obstruction_guard() -> dict[str, int | float | bool]:
    """Audit the finite full-contract, high-overlap aligned-core model."""
    graph = build_three_hub_graph()
    groups = graph["groups"]
    vertices = graph["vertices"]
    graph_edges = graph["edges"]
    adjacency = graph["adjacency"]
    assert isinstance(groups, dict)
    assert isinstance(vertices, list)
    assert isinstance(graph_edges, set)
    assert isinstance(adjacency, dict)

    n = len(vertices)
    e_count = len(graph_edges)
    degrees = {item: len(adjacency[item]) for item in vertices}
    delta = min(degrees.values())
    maximum_degree = max(degrees.values())
    center = groups["H"][0]
    a_side = {center, *groups["X"], *groups["Y"]}
    b_side = set(vertices) - a_side
    assert a_side == {center, *adjacency[center]}
    assert maximum_degree == len(a_side) - 1
    threshold = n / 2 + math.sqrt(
        e_count - n * n / 4 + n / 2
    )
    assert len(a_side) >= threshold
    assert e_count > n * n / 4

    repeated_pairs: list[tuple[Edge, Edge]] = []
    for index, w_vertex in enumerate(groups["W"]):
        u_vertex = groups["U"][index]
        for coordinate in range(len(groups["Y"])):
            repeated_pairs.append(
                (
                    edge(u_vertex, groups["X"][coordinate]),
                    edge(w_vertex, groups["Y"][coordinate]),
                )
            )

    for first_edge, second_edge in repeated_pairs:
        endpoints = set(first_edge) | set(second_edge)
        induced_edges = {
            item for item in graph_edges if item <= endpoints
        }
        assert induced_edges == {first_edge, second_edge}
        assert not linked_two_three(first_edge, second_edge, adjacency)

    lambda_count: Counter[Edge] = Counter()
    rectangles: dict[Edge, tuple[set[Vertex], set[Vertex]]] = {}
    for index, w_vertex in enumerate(groups["W"]):
        u_vertex = groups["U"][index]
        missing_pair = edge(u_vertex, w_vertex)
        assert missing_pair not in graph_edges
        assert not has_length_three(u_vertex, w_vertex, adjacency)
        lambda_count[missing_pair] = len(groups["Y"])
        rectangles[missing_pair] = (
            set(groups["X"][: len(groups["Y"])]),
            set(groups["Y"]),
        )

    fixed_a_pair = edge(groups["X"][0], groups["Y"][0])
    fixed_overlap = sum(
        int(
            any(
                fixed_a_pair == edge(left, right)
                for left in left_set
                for right in right_set
            )
        )
        for left_set, right_set in rectangles.values()
    )
    assert fixed_overlap == len(groups["W"])

    e_zero = sum(value - 1 for value in lambda_count.values())
    defect = len(repeated_pairs)
    missing_a = sum(
        edge(left, right) not in graph_edges
        for left, right in itertools.combinations(a_side, 2)
    )
    missing_b = sum(
        edge(left, right) not in graph_edges
        for left, right in itertools.combinations(b_side, 2)
    )
    crossing_edges = sum(
        edge(left, right) in graph_edges
        for left in a_side
        for right in b_side
    )
    phi = e_count / 2 + n / 2 * math.sqrt(
        e_count - n * n / 4
    )
    size_slack = e_count - math.comb(len(b_side), 2) - phi
    assert defect <= missing_b + size_slack + 1e-9

    clique_core = set(groups["U"] + groups["X"])
    assert len(clique_core) == graph["p"]
    assert all(
        edge(left, right) in graph_edges
        for left, right in itertools.combinations(clique_core, 2)
    )

    return {
        "n": n,
        "edges": e_count,
        "density_threshold_floor": math.floor(n * n / 4),
        "minimum_degree": delta,
        "maximum_degree": maximum_degree,
        "maximum_witness_size": len(a_side),
        "BCM_size_threshold": threshold,
        "repeated_good_defect": defect,
        "zero_shore_excess_E0": e_zero,
        "fixed_missing_A_pair_overlap": fixed_overlap,
        "missing_A_edges": missing_a,
        "missing_B_edges": missing_b,
        "crossing_edges": crossing_edges,
        "size_slack_Sm": size_slack,
        "aligned_clique_core": len(clique_core),
        "repeated_pairs_C7_incompatible": True,
        "passed": True,
    }


def overlap_high_low_guard() -> dict[str, int | bool]:
    """Check the rectangle overlap and weighted high/low identities."""
    rectangles = [
        ({"a0", "a1", "a2"}, {"b0", "b1", "b2"}),
        ({"a0", "a3"}, {"b0", "b3"}),
        ({"a0", "a4", "a5", "a6"}, {"b0", "b4", "b5", "b6"}),
    ]
    weights = [len(left) for left, _ in rectangles]
    overlap: Counter[tuple[str, str]] = Counter()
    for left, right in rectangles:
        assert len(left) == len(right)
        for first in left:
            for second in right:
                overlap[(first, second)] += 1
    assert sum(overlap.values()) == sum(
        value * value for value in weights
    )

    threshold = 3
    excess = sum(value - 1 for value in weights)
    low_bound = (threshold - 1) * sum(
        value <= threshold for value in weights
    )
    high_square = sum(
        value * value for value in weights if value > threshold
    )
    high_bound = high_square // threshold
    assert excess <= low_bound + high_bound
    return {
        "rectangles": len(rectangles),
        "maximum_fixed_pair_overlap": max(overlap.values()),
        "rectangle_area_sum": sum(overlap.values()),
        "weight_square_sum": sum(value * value for value in weights),
        "zero_excess": excess,
        "high_low_bound": low_bound + high_bound,
        "passed": True,
    }


def main() -> None:
    graph = build_three_hub_graph()
    result = {
        "overlap_high_low": overlap_high_low_guard(),
        "contract_obstruction": contract_obstruction_guard(),
        "L4_2": l4_two_guard(graph),
        "scope": (
            "The model refutes uniform overlap and E0=o(n^2), but has "
            "an aligned clique core; the aggregate dichotomy remains open."
        ),
        "passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
