#!/usr/bin/env python3
"""Exact finite-host probes for the q-to-zero random-cluster survivor.

For v_e=q*x_e and after division by q^|V|, a subgraph A has weight
q^(|A|-|V|+k(A)), so forests are precisely the q^0 sector.
The complete-graph calculations below are corroboration, not a reduction.
"""

from __future__ import annotations

import hashlib
import json
from itertools import combinations
from pathlib import Path

import sympy as sp


def cyclomatic_number(n: int, edges: list[tuple[int, int]], mask: int) -> int:
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
    value = edge_count - n + components
    assert value >= 0
    return value


def unweighted_rayleigh(n: int, first: int, second: int, q: sp.Symbol) -> sp.Expr:
    edges = list(combinations(range(n), 2))
    cells = [[sp.Integer(0), sp.Integer(0)], [sp.Integer(0), sp.Integer(0)]]
    for mask in range(1 << len(edges)):
        weight = q ** cyclomatic_number(n, edges, mask)
        cells[(mask >> first) & 1][(mask >> second) & 1] += weight
    return sp.factor(cells[1][0] * cells[0][1] - cells[1][1] * cells[0][0])


def main() -> None:
    q = sp.Symbol("q")
    output: dict[str, object] = {
        "scope": "finite unweighted corroboration and exact boundary identity only",
        "scaled_weight_identity": "q^(-|V|) q^k(A) product(q*x_e) = q^(|A|-|V|+k(A)) product(x_e)",
        "q_zero_sector": "|A|-|V|+k(A)=0 iff A is a forest",
        "complete_graphs": {},
    }
    for n in range(3, 6):
        edges = list(combinations(range(n), 2))
        orbit_values: list[sp.Expr] = []
        for first, second in combinations(range(len(edges)), 2):
            value = unweighted_rayleigh(n, first, second, q)
            if value not in orbit_values:
                orbit_values.append(value)
        output["complete_graphs"][f"K{n}"] = [str(value) for value in orbit_values]
        for value in orbit_values:
            quotient = sp.cancel(value / (1 - q))
            polynomial = sp.Poly(quotient, q)
            assert all(coefficient > 0 for coefficient in polynomial.all_coeffs())

    encoded = json.dumps(output, indent=2, sort_keys=True) + "\n"
    path = Path(__file__).with_suffix(".json")
    path.write_text(encoded, encoding="utf-8")
    print(f"wrote {path}")
    print(f"sha256 {hashlib.sha256(encoded.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
