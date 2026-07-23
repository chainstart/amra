#!/usr/bin/env python3
"""Exact finite certificates for the R002 Erdős #635 swap-graph attack.

No numeric cutoff is used in the component closure.  At an odd right vertex
b, every incident semiprime swap edge is obtained by trying a distinct prime
divisor r of b and testing whether b/r+1 is 2^a times an odd prime.
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from math import isqrt


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def factorization(value: int) -> dict[int, int]:
    remaining = value
    out: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            out[divisor] = out.get(divisor, 0) + 1
            remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        out[remaining] = out.get(remaining, 0) + 1
    product = 1
    for prime, exponent in out.items():
        assert is_prime(prime)
        product *= prime**exponent
    assert product == value
    return out


def incident_edges(vertex: int) -> list[dict[str, int]]:
    """Exhaust all incident semiprime swap edges at one odd vertex."""
    edges: list[dict[str, int]] = []
    for deleted_prime in factorization(vertex):
        if deleted_prime == 2:
            continue
        quotient_plus_one = vertex // deleted_prime + 1
        scale = quotient_plus_one & -quotient_plus_one
        partner_prime = quotient_plus_one // scale
        if (
            scale < 2
            or partner_prime == deleted_prime
            or not is_prime(partner_prime)
        ):
            continue
        other = vertex + deleted_prime - partner_prime
        label = vertex + deleted_prime
        assert label == scale * deleted_prime * partner_prime
        assert other == label - partner_prime
        assert other > 0 and other % 2 == 1
        edges.append(
            {
                "lo": min(vertex, other),
                "hi": max(vertex, other),
                "label": label,
                "scale": scale,
                "p": min(deleted_prime, partner_prime),
                "q": max(deleted_prime, partner_prime),
            }
        )
    return edges


def closed_component(start: int) -> tuple[set[int], list[dict[str, int]]]:
    vertices = {start}
    queue = deque([start])
    edge_map: dict[tuple[int, int, int], dict[str, int]] = {}
    while queue:
        vertex = queue.popleft()
        for edge in incident_edges(vertex):
            key = (edge["lo"], edge["hi"], edge["label"])
            old = edge_map.setdefault(key, edge)
            assert old == edge
            other = edge["hi"] if edge["lo"] == vertex else edge["lo"]
            if other not in vertices:
                vertices.add(other)
                queue.append(other)
    return vertices, sorted(
        edge_map.values(),
        key=lambda edge: (edge["lo"], edge["hi"], edge["label"]),
    )


def cycle_core(
    vertices: set[int], edges: list[dict[str, int]]
) -> tuple[list[int], list[int]]:
    """Peel leaves in a multigraph and return core vertices/edge indices."""
    active_edges = set(range(len(edges)))
    incident: dict[int, set[int]] = defaultdict(set)
    for index, edge in enumerate(edges):
        incident[edge["lo"]].add(index)
        incident[edge["hi"]].add(index)
    queue = deque(
        vertex for vertex in vertices if len(incident[vertex]) <= 1
    )
    while queue:
        vertex = queue.popleft()
        live = incident[vertex] & active_edges
        if len(live) > 1:
            continue
        for edge_index in list(live):
            active_edges.remove(edge_index)
            edge = edges[edge_index]
            other = edge["hi"] if edge["lo"] == vertex else edge["lo"]
            if len(incident[other] & active_edges) <= 1:
                queue.append(other)
    core_vertices = sorted(
        {
            endpoint
            for edge_index in active_edges
            for endpoint in (
                edges[edge_index]["lo"],
                edges[edge_index]["hi"],
            )
        }
    )
    return core_vertices, sorted(active_edges)


def conflicts(labels: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    for index, first in enumerate(labels):
        for second in labels[index + 1 :]:
            difference = abs(first - second)
            if first % difference == 0:
                assert second % difference == 0
                out.append([first, second, difference])
    return out


def main() -> None:
    vertices, edges = closed_component(29_165)
    expected_vertices = {
        25_619,
        25_709,
        26_253,
        27_131,
        28_943,
        29_149,
        29_165,
        29_181,
        29_211,
        29_359,
        29_391,
        29_419,
        29_469,
    }
    assert vertices == expected_vertices
    assert len(edges) == 13
    cyclomatic_number = len(edges) - len(vertices) + 1
    assert cyclomatic_number == 1

    core_vertices, core_edge_indices = cycle_core(vertices, edges)
    assert core_vertices == [
        29_149,
        29_165,
        29_181,
        29_391,
        29_419,
        29_469,
    ]
    core_labels = sorted(edges[index]["label"] for index in core_edge_indices)
    assert core_labels == [
        29_184,
        29_252,
        29_432,
        29_472,
        29_488,
        29_492,
    ]
    core_conflicts = conflicts(core_labels)
    assert core_conflicts == [
        [29_184, 29_488, 304],
        [29_472, 29_488, 16],
        [29_488, 29_492, 4],
    ]

    # Finite arithmetic guard for the symbolic fixed-valuation lemma:
    # x=A*u and y=A*v with u,v odd have v2(x-y)>v2(x), so x-y cannot
    # divide x.  Here we test a box independently of the component above.
    fixed_valuation_pairs = 0
    for exponent in range(1, 10):
        scale = 1 << exponent
        labels = [scale * odd for odd in range(3, 401, 2)]
        for index, first in enumerate(labels):
            for second in labels[index + 1 :]:
                difference = second - first
                assert difference % (2 * scale) == 0
                assert first % difference != 0
                fixed_valuation_pairs += 1

    print(
        json.dumps(
            {
                "schema": "amra.erdos635.r002-closed-component.v1",
                "status": "PASS",
                "component_start": 29_165,
                "component_vertices": sorted(vertices),
                "component_edges": edges,
                "vertex_count": len(vertices),
                "edge_count": len(edges),
                "cyclomatic_number": cyclomatic_number,
                "component_is_exhaustively_closed": True,
                "closure_reason": (
                    "all distinct prime divisors of every reached odd "
                    "vertex were tested by the exact inversion formula"
                ),
                "unique_cycle_vertices": core_vertices,
                "unique_cycle_labels": core_labels,
                "unique_cycle_label_conflicts": core_conflicts,
                "fixed_valuation_pair_checks": fixed_valuation_pairs,
                "scope": (
                    "The component certificate is finite but exhaustive for "
                    "this component.  It does not prove all components are "
                    "pseudoforests or solve the original extremal problem."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
