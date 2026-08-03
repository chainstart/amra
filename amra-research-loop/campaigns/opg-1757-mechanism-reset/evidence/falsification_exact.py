#!/usr/bin/env python3
"""Exact small-host falsification certificates for OPG-1757 mechanisms.

These certificates refute proof mechanisms, not the public negative-
correlation statement.  Only integer and Fraction arithmetic is used.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path


def is_forest(n: int, edges: list[tuple[int, int]], mask: int) -> bool:
    parent = list(range(n))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for index, (left, right) in enumerate(edges):
        if not (mask >> index) & 1:
            continue
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def coefficientwise_k4_certificate() -> dict[str, object]:
    edges = list(combinations(range(4), 2))
    marked_left = edges.index((0, 1))
    marked_right = edges.index((2, 3))
    remaining = [i for i in range(len(edges)) if i not in (marked_left, marked_right)]
    cells = [[defaultdict(int) for _ in range(2)] for _ in range(2)]
    for mask in range(1 << len(edges)):
        if not is_forest(4, edges, mask):
            continue
        exponent = tuple(int((mask >> index) & 1) for index in remaining)
        cells[(mask >> marked_left) & 1][(mask >> marked_right) & 1][exponent] += 1

    coefficient = 0
    target = (1, 1, 1, 1)
    for left_exp, left_count in cells[1][0].items():
        for right_exp, right_count in cells[0][1].items():
            if tuple(a + b for a, b in zip(left_exp, right_exp)) == target:
                coefficient += left_count * right_count
    for both_exp, both_count in cells[1][1].items():
        for neither_exp, neither_count in cells[0][0].items():
            if tuple(a + b for a, b in zip(both_exp, neither_exp)) == target:
                coefficient -= both_count * neither_count
    assert coefficient == -2
    return {
        "graph": "K4",
        "marked_edges": [[0, 1], [2, 3]],
        "remaining_edges": [list(edges[index]) for index in remaining],
        "monomial_exponent": list(target),
        "rayleigh_coefficient": coefficient,
    }


def component_partition(mask: int, edges: list[tuple[int, int]], n: int) -> tuple[tuple[int, ...], ...]:
    parent = list(range(n))

    def find(vertex: int) -> int:
        if parent[vertex] != vertex:
            parent[vertex] = find(parent[vertex])
        return parent[vertex]

    for index, (left, right) in enumerate(edges):
        if (mask >> index) & 1:
            left_root, right_root = find(left), find(right)
            parent[left_root] = right_root
    roots = {find(vertex) for vertex in range(n)}
    return tuple(sorted(tuple(vertex for vertex in range(n) if find(vertex) == root) for root in roots))


def k3_partition_covariance() -> dict[str, object]:
    edges = list(combinations(range(3), 2))
    marked_left = edges.index((0, 1))
    marked_right = edges.index((0, 2))
    groups: dict[tuple[tuple[int, ...], ...], list[int]] = defaultdict(list)
    for mask in range(1 << len(edges)):
        if is_forest(3, edges, mask):
            groups[component_partition(mask, edges, 3)].append(mask)
    total = sum(len(masks) for masks in groups.values())
    mean_left = Fraction()
    mean_right = Fraction()
    mean_product = Fraction()
    for masks in groups.values():
        weight = Fraction(len(masks), total)
        left = Fraction(sum((mask >> marked_left) & 1 for mask in masks), len(masks))
        right = Fraction(sum((mask >> marked_right) & 1 for mask in masks), len(masks))
        mean_left += weight * left
        mean_right += weight * right
        mean_product += weight * left * right
    covariance = mean_product - mean_left * mean_right
    assert covariance == Fraction(1, 147)
    return {
        "graph": "K3",
        "marked_edges": [[0, 1], [0, 2]],
        "conditional_mean_covariance": "1/147",
    }


def deletion_contraction_mixed_coefficient() -> dict[str, object]:
    edges = [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3)]
    e_index, f_index, pivot_index = 0, 4, 6
    absent = [[0, 0], [0, 0]]
    present = [[0, 0], [0, 0]]
    for mask in range(1 << len(edges)):
        if not is_forest(5, edges, mask):
            continue
        table = present if (mask >> pivot_index) & 1 else absent
        table[(mask >> e_index) & 1][(mask >> f_index) & 1] += 1

    def values(table: list[list[int]]) -> tuple[int, int, int, int]:
        return (
            sum(map(sum, table)),
            table[1][0] + table[1][1],
            table[0][1] + table[1][1],
            table[1][1],
        )

    a, ae, af, aef = values(absent)
    b, be, bf, bef = values(present)
    mixed = ae * bf + be * af - a * bef - b * aef
    assert absent == [[16, 14], [14, 10]]
    assert present == [[15, 7], [7, 3]]
    assert mixed == -2
    return {
        "vertices": 5,
        "edges": [list(edge) for edge in edges],
        "marked_edges": [list(edges[e_index]), list(edges[f_index])],
        "pivot_edge": list(edges[pivot_index]),
        "pivot_absent_cells": absent,
        "pivot_present_cells": present,
        "mixed_coefficient_at_unit_other_weights": mixed,
    }


def main() -> None:
    coefficient = coefficientwise_k4_certificate()
    partition = k3_partition_covariance()
    mixed = deletion_contraction_mixed_coefficient()
    result = {
        "scope": "mechanism falsification only; OPG-1757 remains open",
        "certificates": {
            "M001_and_M012": coefficient,
            "M002": {
                "triangle_homogenization": "H=t^2+t(x+y+z)+xy+xz+yz",
                "rayleigh_xy": "z(t+z)",
                "negative_assignment": {"t": -2, "z": 1, "value": -1},
            },
            "M003": {
                "host": "P4",
                "same_component_count": 2,
                "component_size_products": [3, 4],
                "conclusion": "one scalar root-activity moment cannot normalize both fibers",
            },
            "M005": partition,
            "M006": {
                "host": "K4",
                "marked_edges": [[0, 1], [2, 3]],
                "both_forest": [[0, 1], [2, 3]],
                "neither_forest": [[0, 2], [1, 2], [1, 3]],
                "conclusion": "adding either marked edge to the neither forest creates a cycle",
            },
            "M007": mixed,
            "M009": {
                "singleton_equations": "a_v=1 for every vertex v",
                "two_vertex_equation": "a_u+a_v=1",
                "contradiction": "2=1",
            },
            "M010": {
                "host": "K3",
                "marked_edges": [[0, 1], [0, 2]],
                "expected_conditional_covariance": "-2/21",
                "between_size_covariance": "8/147",
                "total_covariance": "-2/49",
                "conclusion": "layer averaging has an omitted positive covariance term",
            },
        },
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output = Path(__file__).with_name("falsification_exact.json")
    output.write_text(encoded, encoding="utf-8")
    print(f"wrote {output}")
    print(f"sha256 {hashlib.sha256(encoded.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
