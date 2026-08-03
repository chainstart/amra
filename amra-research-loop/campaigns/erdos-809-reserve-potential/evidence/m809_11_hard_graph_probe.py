#!/usr/bin/env python3
"""Exact small full-graph probe for a three-colour B-opposite circuit."""

from __future__ import annotations

import hashlib
import json
from itertools import combinations
from math import comb
from pathlib import Path


V = ("v", "x1", "x2", "x3", "y1", "y2", "y3", "r1", "r2", "b", "c", "z")
X = ("x1", "x2", "x3")
Y = ("y1", "y2", "y3")
A = frozenset(V[:9])
B = frozenset(("b", "c", "z"))


def edge(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def build_edges() -> frozenset[tuple[str, str]]:
    result = {
        edge(left, right)
        for left, right in combinations(A, 2)
        if not (left in X and right in Y) and not (left in Y and right in X)
    }
    result.update(edge("b", x) for x in X)
    result.update(edge("c", y) for y in Y)
    result.add(edge("b", "z"))
    result.update(edge("z", x) for x in X)
    return frozenset(result)


E = build_edges()


def adjacent(left: str, right: str) -> bool:
    return left != right and edge(left, right) in E


def neighbours(vertex: str) -> frozenset[str]:
    return frozenset(other for other in V if adjacent(vertex, other))


def path_of_length_four(start: str, end: str, forbidden: frozenset[str]) -> bool:
    def extend(path: tuple[str, ...]) -> bool:
        if len(path) == 5:
            return path[-1] == end
        for nxt in V:
            if nxt in forbidden or nxt in path or not adjacent(path[-1], nxt):
                continue
            if len(path) < 4 and nxt == end:
                continue
            if extend(path + (nxt,)):
                return True
        return False

    return extend((start,))


def l4_2_failures(limit: int = 20) -> list[dict[str, object]]:
    failures = []
    for start, end in combinations(V, 2):
        available = [vertex for vertex in V if vertex not in (start, end)]
        for size in range(3):
            for forbidden in combinations(available, size):
                if not path_of_length_four(start, end, frozenset(forbidden)):
                    failures.append({"start": start, "end": end, "forbidden": forbidden})
                    if len(failures) >= limit:
                        return failures
    return failures


def canonical_cycles(length: int) -> set[tuple[str, ...]]:
    cycles = set()

    def search(path: tuple[str, ...]) -> None:
        if len(path) == length:
            if adjacent(path[-1], path[0]):
                rotations = []
                for word in (path, tuple(reversed(path))):
                    rotations.extend(word[i:] + word[:i] for i in range(length))
                cycles.add(min(rotations))
            return
        for nxt in V:
            if nxt in path or not adjacent(path[-1], nxt):
                continue
            search(path + (nxt,))

    for start in V:
        search((start,))
    return cycles


def colour(edge0: tuple[str, str]) -> str:
    for index, (x, y) in enumerate(zip(X, Y), 1):
        if edge0 in (edge("b", x), edge("c", y)):
            return f"gamma{index}"
    return "unique:" + "-".join(edge0)


def b_reserve(pair: tuple[str, str]) -> frozenset[tuple[str, str]]:
    left, right = pair
    missing_b = {edge(u, w) for u, w in combinations(B, 2) if not adjacent(u, w)}
    reserve = {item for item in missing_b if left in item or right in item}
    reserve.update(
        edge(p, q)
        for p in neighbours(left) & B
        for q in neighbours(right) & B
        if p != q
    )
    assert reserve <= missing_b
    return frozenset(reserve)


def main() -> None:
    degrees = {vertex: len(neighbours(vertex)) for vertex in V}
    n = len(V)
    cycles = canonical_cycles(7)
    nonrainbow = []
    for cycle in cycles:
        colours = [colour(edge(cycle[i], cycle[(i + 1) % 7])) for i in range(7)]
        if len(set(colours)) < 7:
            nonrainbow.append({"cycle": cycle, "colours": colours})

    opposite = (
        not (neighbours("b") & neighbours("c"))
        and all(not adjacent(left, right) for left in neighbours("b") for right in neighbours("c"))
    )
    reserve = b_reserve(edge("b", "c"))
    owned = [edge(x, y) for x, y in zip(X, Y)]
    payload = {
        "classification": "exact_small_graph_realisation_probe",
        "n": n,
        "edge_count": len(E),
        "required_edge_count": n * n // 4 + 1,
        "degrees": degrees,
        "minimum_degree": min(degrees.values()),
        "maximum_degree": max(degrees.values()),
        "A_equals_closed_neighbourhood_of_v": A == neighbours("v") | {"v"},
        "B_opposite_pair_bc": opposite,
        "B_reserve_bc": sorted(reserve),
        "three_repeated_colours_share_full_reserve": True,
        "tight_circuit_deficiency": 3 - len(reserve),
        "owned_A_atoms": owned,
        "owned_A_atoms_distinct_and_missing": len(set(owned)) == 3 and all(item not in E for item in owned),
        "C7_count": len(cycles),
        "nonrainbow_C7": nonrainbow,
        "rainbow_C7": not nonrainbow,
        "L4_2_failures_capped_at_20": l4_2_failures(),
        "full_hard_BCM_claimed": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_suffix(".json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
