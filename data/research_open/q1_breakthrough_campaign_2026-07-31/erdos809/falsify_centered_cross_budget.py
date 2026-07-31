#!/usr/bin/env python3
"""Deterministic small-template falsifier for the centered #809 budget.

It enumerates every equal three-vertex blow-up of a four-type looped
graph, retains the exact density/maximum-witness/L4(2) contract, and
computes the exact chromatic defect of the C7-compatibility graph on
A--B edges.  Passing is finite evidence only.
"""

from __future__ import annotations

import itertools
import json
import math


def blowup(mask: int, types: int = 4, size: int = 3) -> list[int]:
    n = types * size
    adjacency = [0] * n
    bit = 0
    for left in range(types):
        for right in range(left, types):
            present = (mask >> bit) & 1
            bit += 1
            if not present:
                continue
            for u in range(left * size, (left + 1) * size):
                for v in range(right * size, (right + 1) * size):
                    if u < v:
                        adjacency[u] |= 1 << v
                        adjacency[v] |= 1 << u
    return adjacency


def has_length_four(adjacency: list[int], a: int, b: int, banned: int) -> bool:
    n = len(adjacency)
    for x in range(n):
        if x in (a, b) or (banned >> x) & 1 or not (adjacency[a] >> x) & 1:
            continue
        for y in range(n):
            if y in (a, b, x) or (banned >> y) & 1 or not (adjacency[x] >> y) & 1:
                continue
            available = adjacency[y] & adjacency[b] & ~banned
            available &= ~((1 << a) | (1 << b) | (1 << x) | (1 << y))
            if available:
                return True
    return False


def has_l4_2(adjacency: list[int]) -> bool:
    n = len(adjacency)
    for a in range(n):
        for b in range(a + 1, n):
            others = [v for v in range(n) if v not in (a, b)]
            deletion_sets = [()] + [(v,) for v in others]
            deletion_sets += list(itertools.combinations(others, 2))
            for deleted in deletion_sets:
                banned = sum(1 << v for v in deleted)
                if not has_length_four(adjacency, a, b, banned):
                    return False
    return True


def share_c7(adjacency: list[int], first: tuple[int, int], second: tuple[int, int]) -> bool:
    n = len(adjacency)
    required = {tuple(sorted(first)), tuple(sorted(second))}
    for start in range(n):
        path = [start]

        def extend(used: int) -> bool:
            if len(path) == 7:
                if not (adjacency[path[-1]] >> start) & 1:
                    return False
                cycle_edges = {
                    tuple(sorted((path[i], path[(i + 1) % 7])))
                    for i in range(7)
                }
                return required <= cycle_edges
            candidates = adjacency[path[-1]] & ~used
            while candidates:
                bit = candidates & -candidates
                candidates -= bit
                vertex = bit.bit_length() - 1
                path.append(vertex)
                if extend(used | bit):
                    return True
                path.pop()
            return False

        if extend(1 << start):
            return True
    return False


def chromatic_number(adjacency: list[int]) -> int:
    n = len(adjacency)
    colors = [-1] * n
    best = n

    def search(colored: int, used: int) -> None:
        nonlocal best
        if used >= best:
            return
        if colored == n:
            best = used
            return
        remaining = [v for v in range(n) if colors[v] < 0]
        vertex = max(
            remaining,
            key=lambda v: (
                len({colors[w] for w in range(n) if colors[w] >= 0 and (adjacency[v] >> w) & 1}),
                adjacency[v].bit_count(),
            ),
        )
        forbidden = {
            colors[w]
            for w in range(n)
            if colors[w] >= 0 and (adjacency[vertex] >> w) & 1
        }
        for color in range(used):
            if color not in forbidden:
                colors[vertex] = color
                search(colored + 1, used)
                colors[vertex] = -1
        colors[vertex] = used
        search(colored + 1, used + 1)
        colors[vertex] = -1

    search(0, 0)
    return best


def run() -> dict[str, object]:
    types, size = 4, 3
    n = types * size
    template_count = 1 << (types * (types + 1) // 2)
    qualifying = 0
    maximum_margin = -10**9
    for mask in range(template_count):
        graph = blowup(mask, types, size)
        edge_count = sum(row.bit_count() for row in graph) // 2
        if edge_count <= n * n / 4:
            continue
        degrees = [row.bit_count() for row in graph]
        center = max(range(n), key=degrees.__getitem__)
        A = graph[center] | (1 << center)
        B = ((1 << n) - 1) ^ A
        threshold = n / 2 + math.sqrt(edge_count - n * n / 4 + n / 2)
        if degrees[center] + 1 < threshold or not has_l4_2(graph):
            continue
        cross = [
            (a, b)
            for a in range(n)
            if (A >> a) & 1
            for b in range(n)
            if (B >> b) & 1 and (graph[a] >> b) & 1
        ]
        compatibility = [0] * len(cross)
        for i in range(len(cross)):
            for j in range(i + 1, len(cross)):
                if share_c7(graph, cross[i], cross[j]):
                    compatibility[i] |= 1 << j
                    compatibility[j] |= 1 << i
        colors = chromatic_number(compatibility)
        defect = len(cross) - colors
        missing_B = sum(
            1
            for b in range(n)
            if (B >> b) & 1
            for c in range(b + 1, n)
            if (B >> c) & 1 and not (graph[b] >> c) & 1
        )
        margin = defect - missing_B
        maximum_margin = max(maximum_margin, margin)
        assert margin <= 0, (mask, defect, missing_B)
        qualifying += 1
    assert qualifying == 93
    return {
        "schema": "amra.erdos809.centered-cross-falsifier.v1",
        "templates": template_count,
        "qualifying_full_contract_blowups": qualifying,
        "maximum_defect_minus_M_B": maximum_margin,
        "status": "PASS",
        "boundary": "finite n=12 template evidence only",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
