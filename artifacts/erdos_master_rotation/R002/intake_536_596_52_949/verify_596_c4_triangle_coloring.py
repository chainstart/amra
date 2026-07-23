#!/usr/bin/env python3
"""Exhaustively check the elementary necessity lemma used for #596.

For every labelled graph on at most six vertices, the program checks that if
the graph is C4-free then:

1. no edge lies in two different triangles; and
2. the explicit two-colouring which makes each triangle bichromatic contains
   no monochromatic triangle.

The general proof is elementary and appears in 596_REPORT.md.  Exhaustion is
only a regression certificate for the implementation of the finite pattern.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


Edge = tuple[int, int]


def all_edges(order: int) -> list[Edge]:
    return list(itertools.combinations(range(order), 2))


def edge_set(order: int, mask: int) -> set[Edge]:
    edges = all_edges(order)
    return {edge for index, edge in enumerate(edges) if mask & (1 << index)}


def is_c4_free(order: int, edges: set[Edge]) -> bool:
    neighbours = {vertex: set() for vertex in range(order)}
    for left, right in edges:
        neighbours[left].add(right)
        neighbours[right].add(left)
    return all(
        len(neighbours[left] & neighbours[right]) <= 1
        for left, right in itertools.combinations(range(order), 2)
    )


def triangles(order: int, edges: set[Edge]) -> list[tuple[Edge, Edge, Edge]]:
    result: list[tuple[Edge, Edge, Edge]] = []
    for a, b, c in itertools.combinations(range(order), 3):
        candidate = ((a, b), (a, c), (b, c))
        if all(edge in edges for edge in candidate):
            result.append(candidate)
    return result


def explicit_coloring(
    edges: set[Edge], graph_triangles: list[tuple[Edge, Edge, Edge]]
) -> dict[Edge, int]:
    coloring: dict[Edge, int] = {}
    for triangle in graph_triangles:
        ordered = sorted(triangle)
        coloring[ordered[0]] = 0
        coloring[ordered[1]] = 1
        coloring[ordered[2]] = 1
    for edge in edges:
        coloring.setdefault(edge, 0)
    return coloring


def verify(max_order: int) -> dict[str, object]:
    rows: list[dict[str, int]] = []
    passed = True
    for order in range(1, max_order + 1):
        edge_count = len(all_edges(order))
        c4_free_count = 0
        triangle_bearing_count = 0
        for mask in range(1 << edge_count):
            edges = edge_set(order, mask)
            if not is_c4_free(order, edges):
                continue
            c4_free_count += 1
            graph_triangles = triangles(order, edges)
            triangle_bearing_count += bool(graph_triangles)

            used_edges = [edge for triangle in graph_triangles for edge in triangle]
            edge_disjoint = len(used_edges) == len(set(used_edges))
            coloring = explicit_coloring(edges, graph_triangles)
            no_monochromatic_triangle = all(
                len({coloring[edge] for edge in triangle}) > 1
                for triangle in graph_triangles
            )
            passed &= edge_disjoint and no_monochromatic_triangle
        rows.append(
            {
                "order": order,
                "labelled_graph_count": 1 << edge_count,
                "c4_free_graph_count": c4_free_count,
                "c4_free_graphs_with_triangle": triangle_bearing_count,
            }
        )
    return {
        "schema_version": "amra.erdos596.c4_triangle_coloring.v1",
        "problem_id": "596",
        "max_order": max_order,
        "rows": rows,
        "passed": passed,
        "scope_note": (
            "Finite exhaustive confirmation only.  The general edge-disjointness "
            "and two-colouring arguments are proved directly in the report."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=6)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = verify(args.max_order)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
