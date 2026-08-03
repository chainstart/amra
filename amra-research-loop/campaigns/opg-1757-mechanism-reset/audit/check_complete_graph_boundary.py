#!/usr/bin/env python3
"""Independent exact K3--K5 corroboration without importing author code."""

from __future__ import annotations

import hashlib
import json
from itertools import combinations
from pathlib import Path


Polynomial = tuple[int, ...]


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    size = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(size)
    )


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    output = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] += a * b
    while len(output) > 1 and output[-1] == 0:
        output.pop()
    return tuple(output)


def subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    size = max(len(left), len(right))
    output = [
        (left[i] if i < len(left) else 0)
        - (right[i] if i < len(right) else 0)
        for i in range(size)
    ]
    while len(output) > 1 and output[-1] == 0:
        output.pop()
    return tuple(output)


def cyclomatic(n: int, edges: list[tuple[int, int]], mask: int) -> int:
    parent = list(range(n))
    components = n

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    edge_count = 0
    for index, (left, right) in enumerate(edges):
        if not (mask >> index) & 1:
            continue
        edge_count += 1
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[left_root] = right_root
            components -= 1
    result = edge_count - n + components
    assert result >= 0
    return result


def rayleigh(n: int, first: int, second: int) -> Polynomial:
    edges = list(combinations(range(n), 2))
    cells: list[list[Polynomial]] = [[[0], [0]], [[0], [0]]]  # type: ignore[list-item]
    for mask in range(1 << len(edges)):
        exponent = cyclomatic(n, edges, mask)
        monomial = tuple([0] * exponent + [1])
        i, j = (mask >> first) & 1, (mask >> second) & 1
        cells[i][j] = add(tuple(cells[i][j]), monomial)
    return subtract(
        multiply(tuple(cells[1][0]), tuple(cells[0][1])),
        multiply(tuple(cells[1][1]), tuple(cells[0][0])),
    )


def divide_by_one_minus_q(value: Polynomial) -> Polynomial:
    # d_0=p_0 and d_i=p_i-p_(i-1) for d=(1-q)p.
    quotient = [value[0]]
    for index in range(1, len(value) - 1):
        quotient.append(value[index] + quotient[-1])
    assert value[-1] == -quotient[-1]
    return tuple(quotient)


def main() -> None:
    complete_graphs: dict[str, list[dict[str, object]]] = {}
    for n in range(3, 6):
        edges = list(combinations(range(n), 2))
        orbits: list[Polynomial] = []
        for first, second in combinations(range(len(edges)), 2):
            value = rayleigh(n, first, second)
            if value not in orbits:
                orbits.append(value)
        rows = []
        for value in orbits:
            quotient = divide_by_one_minus_q(value)
            assert all(coefficient > 0 for coefficient in quotient)
            rows.append(
                {
                    "rayleigh_coefficients_low_to_high": value,
                    "quotient_by_1_minus_q_low_to_high": quotient,
                    "quotient_strictly_positive": True,
                }
            )
        complete_graphs[f"K{n}"] = rows

    payload = {
        "classification": "finite_exact_corroboration_not_a_reduction",
        "complete_graphs": complete_graphs,
        "all_orbits_nonnegative_for_0_le_q_le_1": True,
        "universal_finite_q_negative_dependence_proved": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_name("complete_graph_boundary_check.json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
