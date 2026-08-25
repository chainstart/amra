#!/usr/bin/env python3
"""Verify explicit five-colouring certificates for Dirac's 6-critical joins."""

from __future__ import annotations

import argparse
import json

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]


def canon(u: Vertex, v: Vertex) -> Edge:
    return (u, v) if u < v else (v, u)


def graph(q: int) -> tuple[list[Vertex], set[Edge]]:
    vertices = [(side, i) for side in (0, 1) for i in range(q)]
    edges: set[Edge] = set()
    for side in (0, 1):
        for i in range(q):
            edges.add(canon((side, i), (side, (i + 1) % q)))
    for i in range(q):
        for j in range(q):
            edges.add(canon((0, i), (1, j)))
    return vertices, edges


def colour_path_after_removed_cycle_edge(
    q: int, side: int, start: int, palette: tuple[int, int]
) -> dict[Vertex, int]:
    # Removed edge is between start-1 and start; walk the remaining q-vertex path.
    return {
        (side, (start + step) % q): palette[step % 2]
        for step in range(q)
    }


def colour_cycle_with_unique_anchor(
    q: int, side: int, anchor: int, palette: tuple[int, int], unique: int
) -> dict[Vertex, int]:
    colours = {(side, anchor): unique}
    for step in range(1, q):
        colours[(side, (anchor + step) % q)] = palette[(step - 1) % 2]
    return colours


def witness(q: int, edge: Edge) -> dict[Vertex, int]:
    (s1, i), (s2, j) = edge
    if s1 == s2:
        side = s1
        # Orient the deleted cycle edge as previous--start.
        if (i + 1) % q == j:
            start = j
        elif (j + 1) % q == i:
            start = i
        else:
            raise AssertionError("not a cycle edge")
        colours = colour_path_after_removed_cycle_edge(q, side, start, (0, 1))
        other = 1 - side
        colours.update(colour_cycle_with_unique_anchor(q, other, 0, (2, 3), 4))
        return colours
    colours = colour_cycle_with_unique_anchor(q, 0, i, (0, 1), 4)
    colours.update(colour_cycle_with_unique_anchor(q, 1, j, (2, 3), 4))
    return colours


def verify(m: int) -> dict[str, int | bool]:
    q = 2 * m + 1
    vertices, edges = graph(q)
    all_valid = True
    endpoints_same = True
    for removed in edges:
        colours = witness(q, removed)
        all_valid &= set(colours) == set(vertices) and max(colours.values()) <= 4
        endpoints_same &= colours[removed[0]] == colours[removed[1]]
        for edge in edges - {removed}:
            if colours[edge[0]] == colours[edge[1]]:
                all_valid = False
                break
    return {
        "m": m,
        "vertices": len(vertices),
        "edges": len(edges),
        "expected_edges": 4 * m * m + 8 * m + 3,
        "all_edge_deletion_five_colourings_valid": all_valid,
        "deleted_edge_endpoints_share_colour": endpoints_same,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=20)
    args = parser.parse_args()
    rows = [verify(m) for m in range(1, args.max_m + 1)]
    print(
        json.dumps(
            {
                "schema_version": "amra.erdos917.dirac-witness-replay.v1",
                "rows": rows,
                "all_passed": all(
                    row["edges"] == row["expected_edges"]
                    and row["all_edge_deletion_five_colourings_valid"]
                    and row["deleted_edge_endpoints_share_colour"]
                    for row in rows
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
