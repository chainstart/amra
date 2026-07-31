#!/usr/bin/env python3
"""Finite guards for the corrected A-oriented Erdős #809 taxonomy.

The unbounded proposition is proved in ROOT_809_A_ORIENTED_AUDIT.md.
This script checks its vertex bookkeeping on random finite graphs and checks
that the local codegree-two boundary is attained. It is not evidence for the
open total linkage-defect estimate.
"""

from __future__ import annotations

import json
import random
from collections import deque


Adjacency = list[set[int]]


def add_edge(adjacency: Adjacency, left: int, right: int) -> None:
    adjacency[left].add(right)
    adjacency[right].add(left)


def shortest_path(
    adjacency: Adjacency,
    start: int,
    finish: int,
) -> list[int] | None:
    parent = {start: -1}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        if vertex == finish:
            path = []
            while vertex != -1:
                path.append(vertex)
                vertex = parent[vertex]
            return list(reversed(path))
        for neighbour in sorted(adjacency[vertex]):
            if neighbour not in parent:
                parent[neighbour] = vertex
                queue.append(neighbour)
    return None


def simple_paths_of_length(
    adjacency: Adjacency,
    start: int,
    finish: int,
    length: int,
) -> list[tuple[int, ...]]:
    paths: list[tuple[int, ...]] = []

    def visit(path: list[int]) -> None:
        if len(path) == length + 1:
            if path[-1] == finish:
                paths.append(tuple(path))
            return
        for neighbour in adjacency[path[-1]]:
            if neighbour not in path:
                visit(path + [neighbour])

    visit([start])
    return paths


def is_cycle(adjacency: Adjacency, vertices: list[int]) -> bool:
    return (
        len(vertices) == 7
        and len(set(vertices)) == 7
        and all(
            vertices[(index + 1) % 7] in adjacency[vertex]
            for index, vertex in enumerate(vertices)
        )
    )


def audit_oriented_pair(
    adjacency: Adjacency,
    first_edge: tuple[int, int],
    second_edge: tuple[int, int],
) -> tuple[int, int, int]:
    """Audit all four choices of the two designated A-endpoints.

    Returns the number of distance-two and distance-three orientations checked.
    Orientations at other distances are outside the corrected proposition.
    """

    checked_two = 0
    checked_three_clean = 0
    checked_three_transversal = 0
    for x in first_edge:
        y = first_edge[0] if x == first_edge[1] else first_edge[1]
        for z in second_edge:
            w = second_edge[0] if z == second_edge[1] else second_edge[1]
            path = shortest_path(adjacency, x, z)
            if path is None:
                continue
            distance = len(path) - 1
            if distance == 2:
                checked_two += 1
                forbidden = set(path)
                for outer_path in simple_paths_of_length(
                    adjacency, y, w, 3
                ):
                    if set(outer_path).isdisjoint(forbidden):
                        cycle = [
                            y,
                            x,
                            path[1],
                            z,
                            w,
                            outer_path[2],
                            outer_path[1],
                        ]
                        assert is_cycle(adjacency, cycle)
            elif distance == 3:
                length_three_paths = simple_paths_of_length(
                    adjacency, x, z, 3
                )
                clean_paths = [
                    candidate
                    for candidate in length_three_paths
                    if set(candidate[1:-1]).isdisjoint({y, w})
                ]
                if not clean_paths:
                    checked_three_transversal += 1
                    assert all(
                        set(candidate[1:-1]) & {y, w}
                        for candidate in length_three_paths
                    )
                    continue
                checked_three_clean += 1
                clean = clean_paths[0]
                internal = set(clean[1:-1])
                for common in adjacency[y] & adjacency[w]:
                    if common not in internal:
                        cycle = [
                            y,
                            x,
                            clean[1],
                            clean[2],
                            z,
                            w,
                            common,
                        ]
                        assert is_cycle(adjacency, cycle)
    return checked_two, checked_three_clean, checked_three_transversal


def random_guard() -> dict[str, int]:
    generator = random.Random(809_731)
    graphs = 0
    edge_pairs = 0
    distance_two = 0
    distance_three_clean = 0
    distance_three_transversal = 0
    for order in range(7, 11):
        for probability in (0.2, 0.35, 0.5, 0.65, 0.8):
            for _ in range(20):
                adjacency: Adjacency = [set() for _ in range(order)]
                for left in range(order):
                    for right in range(left + 1, order):
                        if generator.random() < probability:
                            add_edge(adjacency, left, right)
                edges = [
                    (left, right)
                    for left in range(order)
                    for right in adjacency[left]
                    if left < right
                ]
                graphs += 1
                for first_index, first_edge in enumerate(edges):
                    for second_edge in edges[first_index + 1 :]:
                        if set(first_edge) & set(second_edge):
                            continue
                        if any(
                            right in adjacency[left]
                            for left in first_edge
                            for right in second_edge
                        ):
                            continue
                        edge_pairs += 1
                        two, three_clean, three_transversal = audit_oriented_pair(
                            adjacency, first_edge, second_edge
                        )
                        distance_two += two
                        distance_three_clean += three_clean
                        distance_three_transversal += three_transversal
    return {
        "random_graphs": graphs,
        "disjoint_edge_pairs": edge_pairs,
        "distance_two_orientations": distance_two,
        "distance_three_clean_orientations": distance_three_clean,
        "distance_three_transversal_orientations": (
            distance_three_transversal
        ),
    }


def sharp_local_guard() -> dict[str, object]:
    # x,y,z,w,a,b = 0,1,2,3,4,5.
    adjacency: Adjacency = [set() for _ in range(6)]
    for edge in (
        (0, 1),
        (2, 3),
        (0, 4),
        (4, 5),
        (5, 2),
        (1, 4),
        (1, 5),
        (3, 4),
        (3, 5),
    ):
        add_edge(adjacency, *edge)
    clean_paths = [
        path
        for path in simple_paths_of_length(adjacency, 0, 2, 3)
        if set(path[1:-1]).isdisjoint({1, 3})
    ]
    assert (0, 4, 5, 2) in clean_paths
    common = adjacency[1] & adjacency[3]
    assert common == {4, 5}
    return {
        "a_endpoint_distance": 3,
        "outer_codegree": len(common),
        "bound_attained": True,
    }


def main() -> None:
    result = {
        "status": "PASS",
        "sharp_local_example": sharp_local_guard(),
        "random_guard": random_guard(),
        "scope": (
            "Finite vertex-bookkeeping guard only; the written proof is "
            "unbounded and the total linkage-defect estimate remains open."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
