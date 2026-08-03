#!/usr/bin/env python3
"""Independent-formula finite guard for Q_ONE_ENDPOINT_LEMMA.md."""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import sympy as sp


def nullity(n: int, edges: list[tuple[int, int]], selected: set[int]) -> int:
    parent = list(range(n))
    components = n

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for index in selected:
        left, right = edges[index]
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[left_root] = right_root
            components -= 1
    return len(selected) - n + components


def check_complete_graph(n: int) -> dict[str, int]:
    q = sp.Symbol("q")
    edges = list(combinations(range(n), 2))
    checked_pairs = 0
    positive_defects = 0
    for e_index, f_index in combinations(range(len(edges)), 2):
        remaining = [index for index in range(len(edges)) if index not in (e_index, f_index)]
        cells = [[sp.Integer(0), sp.Integer(0)], [sp.Integer(0), sp.Integer(0)]]
        defect_sum = 0
        for mask in range(1 << len(remaining)):
            base = {remaining[position] for position in range(len(remaining)) if (mask >> position) & 1}
            for left in range(2):
                for right in range(2):
                    selected = set(base)
                    if left:
                        selected.add(e_index)
                    if right:
                        selected.add(f_index)
                    cells[left][right] += q ** nullity(n, edges, selected)
            defect = (
                nullity(n, edges, base | {e_index, f_index})
                + nullity(n, edges, base)
                - nullity(n, edges, base | {e_index})
                - nullity(n, edges, base | {f_index})
            )
            assert defect in (0, 1)
            defect_sum += defect
        rayleigh = cells[1][0] * cells[0][1] - cells[1][1] * cells[0][0]
        cell_at_one = 2 ** len(remaining)
        assert -sp.diff(rayleigh, q).subs(q, 1) == cell_at_one * defect_sum
        checked_pairs += 1
        positive_defects += defect_sum
    return {"checked_pairs": checked_pairs, "summed_positive_defects": positive_defects}


def main() -> None:
    result = {f"K{n}": check_complete_graph(n) for n in range(3, 6)}
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
