#!/usr/bin/env python3
"""Independent finite counterexample search for the elementary #596 branches.

This does not test the two cited structural theorems.  It exhaustively checks
the finite patterns used in the triangle obstruction and in the girth
trichotomy for every labelled simple graph through the requested order.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

Edge = tuple[int, int]


def universe(order: int) -> list[Edge]:
    return list(itertools.combinations(range(order), 2))


def graph_from_mask(edge_universe: list[Edge], mask: int) -> set[Edge]:
    return {
        edge
        for bit, edge in enumerate(edge_universe)
        if mask & (1 << bit)
    }


def neighbours(order: int, edges: set[Edge]) -> list[set[int]]:
    result = [set() for _ in range(order)]
    for left, right in edges:
        result[left].add(right)
        result[right].add(left)
    return result


def has_c4(order: int, edges: set[Edge]) -> bool:
    """A simple graph has C4 iff two vertices have two common neighbours."""
    nbrs = neighbours(order, edges)
    return any(
        len(nbrs[left] & nbrs[right]) >= 2
        for left, right in itertools.combinations(range(order), 2)
    )


def triangles(order: int, edges: set[Edge]) -> list[tuple[Edge, Edge, Edge]]:
    found: list[tuple[Edge, Edge, Edge]] = []
    for a, b, c in itertools.combinations(range(order), 3):
        candidate = ((a, b), (a, c), (b, c))
        if all(edge in edges for edge in candidate):
            found.append(candidate)
    return found


def has_cycle(order: int, edges: set[Edge]) -> bool:
    parent = list(range(order))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left_root, right_root = root(left), root(right)
        if left_root == right_root:
            return True
        parent[left_root] = right_root
    return False


def deterministic_triangle_coloring(
    edges: set[Edge],
    graph_triangles: list[tuple[Edge, Edge, Edge]],
) -> dict[Edge, str]:
    colors: dict[Edge, str] = {}
    for triangle in graph_triangles:
        least, middle, greatest = sorted(triangle)
        if any(edge in colors for edge in triangle):
            raise AssertionError("triangle edge overlap")
        colors[least] = "red"
        colors[middle] = "blue"
        colors[greatest] = "blue"
    for edge in edges:
        colors.setdefault(edge, "red")
    return colors


def run(max_order: int) -> dict[str, object]:
    rows: list[dict[str, int]] = []
    counterexamples: list[dict[str, object]] = []
    for order in range(1, max_order + 1):
        edge_universe = universe(order)
        counts = {
            "order": order,
            "all_labelled_simple_graphs": 1 << len(edge_universe),
            "cyclic_graphs": 0,
            "girth_3_class": 0,
            "girth_4_class": 0,
            "girth_at_least_5_class": 0,
            "c4_free_graphs": 0,
            "c4_free_triangle_bearing_graphs": 0,
        }
        for mask in range(1 << len(edge_universe)):
            edges = graph_from_mask(edge_universe, mask)
            graph_triangles = triangles(order, edges)
            triangle_present = bool(graph_triangles)
            c4_present = has_c4(order, edges)
            cyclic = has_cycle(order, edges)

            if cyclic:
                counts["cyclic_graphs"] += 1
                categories = (
                    triangle_present,
                    (not triangle_present) and c4_present,
                    (not triangle_present) and (not c4_present),
                )
                if sum(categories) != 1:
                    counterexamples.append(
                        {
                            "kind": "trichotomy",
                            "order": order,
                            "mask": mask,
                        }
                    )
                if categories[0]:
                    counts["girth_3_class"] += 1
                elif categories[1]:
                    counts["girth_4_class"] += 1
                else:
                    counts["girth_at_least_5_class"] += 1

            if not c4_present:
                counts["c4_free_graphs"] += 1
                if triangle_present:
                    counts["c4_free_triangle_bearing_graphs"] += 1
                triangle_edges = [
                    edge for triangle in graph_triangles for edge in triangle
                ]
                if len(triangle_edges) != len(set(triangle_edges)):
                    counterexamples.append(
                        {
                            "kind": "triangle_edge_overlap_in_c4_free_graph",
                            "order": order,
                            "mask": mask,
                        }
                    )
                    continue
                coloring = deterministic_triangle_coloring(edges, graph_triangles)
                if any(
                    len({coloring[edge] for edge in triangle}) == 1
                    for triangle in graph_triangles
                ):
                    counterexamples.append(
                        {
                            "kind": "monochromatic_triangle",
                            "order": order,
                            "mask": mask,
                        }
                    )
        rows.append(counts)

    return {
        "schema_version": "amra.erdos596.independent_qa.v1",
        "problem_id": 596,
        "max_order": max_order,
        "method": "exhaustive enumeration of all labelled finite simple graphs",
        "checks": [
            "cyclic-graph girth trichotomy",
            "edge-disjointness of triangles in C4-free graphs",
            "absence of monochromatic triangles under the deterministic coloring",
        ],
        "rows": rows,
        "counterexample_count": len(counterexamples),
        "counterexamples": counterexamples[:20],
        "passed": not counterexamples,
        "scope_note": (
            "This finite search is a regression certificate for the elementary "
            "branches only; it does not replace either cited structural theorem."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=6)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.max_order < 1:
        parser.error("--max-order must be positive")
    result = run(args.max_order)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

