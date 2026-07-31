#!/usr/bin/env python3
"""Finite guards for the first 2026-07-31 Erdős #809 attack.

The script verifies finite instances of:

1. the four-bridge two-clique family satisfies L4(2);
2. its displayed paired colouring makes every C7 rainbow;
3. its good-edge defect has the claimed exact finite value;
4. A-endpoints need not be globally closest;
5. a contaminated A-geodesic can have arbitrarily large outer codegree.

These are guards for explicit constructions and formulas.  They do not
prove an asymptotic lower bound or Erdős #809.
"""

from __future__ import annotations

import itertools
import json
from collections import deque
from math import comb

Edge = tuple[int, int]


def edge(u: int, v: int) -> Edge:
    if u == v:
        raise ValueError((u, v))
    return (u, v) if u < v else (v, u)


def neighborhoods(n: int, edges: set[Edge]) -> list[set[int]]:
    out = [set() for _ in range(n)]
    for u, v in edges:
        out[u].add(v)
        out[v].add(u)
    return out


def distance(n: int, edges: set[Edge], start: int, end: int) -> int:
    neigh = neighborhoods(n, edges)
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if current == end:
            return dist[current]
        for nxt in neigh[current]:
            if dist[nxt] < 0:
                dist[nxt] = dist[current] + 1
                queue.append(nxt)
    return -1


def has_exact_path(
    n: int,
    edges: set[Edge],
    start: int,
    end: int,
    length: int,
    forbidden: set[int],
) -> bool:
    if start in forbidden or end in forbidden:
        return False

    def visit(path: tuple[int, ...]) -> bool:
        if len(path) == length + 1:
            return path[-1] == end
        for nxt in range(n):
            if nxt in forbidden or nxt in path:
                continue
            if edge(path[-1], nxt) not in edges:
                continue
            if nxt == end and len(path) != length:
                continue
            if visit(path + (nxt,)):
                return True
        return False

    return visit((start,))


def exact_paths(
    n: int,
    edges: set[Edge],
    start: int,
    end: int,
    length: int,
) -> list[tuple[int, ...]]:
    found: list[tuple[int, ...]] = []

    def visit(path: tuple[int, ...]) -> None:
        if len(path) == length + 1:
            if path[-1] == end:
                found.append(path)
            return
        for nxt in range(n):
            if nxt in path or edge(path[-1], nxt) not in edges:
                continue
            if nxt == end and len(path) != length:
                continue
            visit(path + (nxt,))

    visit((start,))
    return found


def cycles_7(n: int, edges: set[Edge]) -> list[tuple[int, ...]]:
    """Enumerate each unoriented seven-cycle once."""
    found: list[tuple[int, ...]] = []
    for vertices in itertools.combinations(range(n), 7):
        root = vertices[0]
        for tail in itertools.permutations(vertices[1:]):
            if tail[0] > tail[-1]:
                continue
            cycle = (root,) + tail
            if all(
                edge(cycle[i], cycle[(i + 1) % 7]) in edges
                for i in range(7)
            ):
                found.append(cycle)
    return found


def four_bridge_graph(
    p: int, q: int
) -> tuple[int, set[Edge], list[Edge], list[Edge]]:
    if p < q or q < 6:
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
    return n, edges, p_generic, q_generic


def l4_guard(p: int = 8, q: int = 7) -> dict[str, int | bool]:
    n, edges, _, _ = four_bridge_graph(p, q)
    deletion_sets = [set()]
    deletion_sets.extend({v} for v in range(n))
    deletion_sets.extend(
        set(pair) for pair in itertools.combinations(range(n), 2)
    )
    endpoint_pairs = 0
    for deleted in deletion_sets:
        remaining = set(range(n)) - deleted
        for u, v in itertools.combinations(remaining, 2):
            assert has_exact_path(n, edges, u, v, 4, deleted)
            endpoint_pairs += 1
    return {
        "vertices": n,
        "deletion_sets": len(deletion_sets),
        "endpoint_pairs_checked": endpoint_pairs,
        "passed": True,
    }


def colouring_guard(p: int = 8, q: int = 7) -> dict[str, int | bool]:
    n, edges, p_generic, q_generic = four_bridge_graph(p, q)
    assert len(p_generic) >= len(q_generic)

    colours: dict[Edge, int] = {}
    next_colour = 0
    paired: list[tuple[Edge, Edge]] = []
    for q_edge, p_edge in zip(q_generic, p_generic):
        colours[q_edge] = next_colour
        colours[p_edge] = next_colour
        paired.append((p_edge, q_edge))
        next_colour += 1
    for item in sorted(edges):
        if item not in colours:
            colours[item] = next_colour
            next_colour += 1

    cycles = cycles_7(n, edges)
    pair_sets = [{left, right} for left, right in paired]
    for cycle in cycles:
        used = {
            edge(cycle[index], cycle[(index + 1) % 7])
            for index in range(7)
        }
        assert len({colours[item] for item in used}) == 7
        assert not any(pair <= used for pair in pair_sets)

    defect = len(edges) - len(set(colours.values()))
    assert defect == len(q_generic) == comb(q - 4, 2)
    assert len(set(colours.values())) == comb(p, 2) + 4 * q - 6
    return {
        "vertices": n,
        "edges": len(edges),
        "cycles_checked": len(cycles),
        "paired_colours": len(paired),
        "defect": defect,
        "colours": len(set(colours.values())),
        "passed": True,
    }


def orientation_guard() -> dict[str, int | bool]:
    # Vertex order: x,y,z,w,a,b.
    x, y, z, w, a, b = range(6)
    edges = {
        edge(x, y),
        edge(z, w),
        edge(x, a),
        edge(a, b),
        edge(b, z),
        edge(y, a),
        edge(y, b),
        edge(w, a),
        edge(w, b),
    }
    neigh = neighborhoods(6, edges)
    assert distance(6, edges, x, z) == 3
    assert distance(6, edges, y, w) == 2
    assert neigh[y] & neigh[w] == {a, b}
    assert len(cycles_7(6, edges)) == 0
    return {
        "vertices": 6,
        "A_endpoint_distance": 3,
        "outer_endpoint_distance": 2,
        "outer_codegree": 2,
        "passed": True,
    }


def contaminated_geodesic_guard(common_neighbors: int = 7) -> dict[str, int | bool]:
    # Vertex order: x,y,z,w,a,c_1,...,c_r.
    if common_neighbors < 1:
        raise ValueError(common_neighbors)
    x, y, z, w, a = range(5)
    n = 5 + common_neighbors
    edges = {
        edge(x, y),
        edge(z, w),
        edge(y, a),
        edge(a, z),
    }
    for common in range(5, n):
        edges.add(edge(y, common))
        edges.add(edge(w, common))
    neigh = neighborhoods(n, edges)
    assert distance(n, edges, x, z) == 3
    assert len(neigh[y] & neigh[w]) == common_neighbors
    assert len(neigh[x]) == 1
    three_paths = exact_paths(n, edges, x, z, 3)
    assert three_paths
    assert all(y in path or w in path for path in three_paths)
    # Since x has degree one, no cycle can contain the specified edge xy.
    assert all(
        edge(x, y)
        not in {
            edge(cycle[index], cycle[(index + 1) % 7])
            for index in range(7)
        }
        for cycle in cycles_7(n, edges)
    )
    return {
        "vertices": n,
        "A_endpoint_distance": 3,
        "outer_codegree": common_neighbors,
        "A_three_paths": len(three_paths),
        "outer_pair_hits_all_A_three_paths": True,
        "specified_edge_in_C7": False,
        "passed": True,
    }


def main() -> None:
    result = {
        "four_bridge_L4": l4_guard(),
        "four_bridge_colouring": colouring_guard(),
        "orientation_sharpness": orientation_guard(),
        "contaminated_A_geodesic": contaminated_geodesic_guard(),
        "scope": (
            "Finite guards verify explicit constructions only; the "
            "budgeted defect inequality and Erdős #809 remain open."
        ),
        "passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
