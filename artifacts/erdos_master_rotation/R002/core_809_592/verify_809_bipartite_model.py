#!/usr/bin/env python3
"""Exact certificate for the K_{a,b}+pq stability model in Erdős #809.

The graph has bipartition A,B and one extra edge pq inside A.  The proof
certificate constructs a C7 through every pair of cross-edges whose A-end is
outside {p,q}.  Exhaustive checks below verify the construction, including
all three possible intersection types of the two prescribed edges.
"""

from __future__ import annotations

import itertools
import json


def edge(u: str, v: str) -> frozenset[str]:
    return frozenset((u, v))


def cycle_edges(cycle: tuple[str, ...]) -> set[frozenset[str]]:
    return {
        edge(cycle[i], cycle[(i + 1) % len(cycle)])
        for i in range(len(cycle))
    }


def witness(
    first: tuple[str, str],
    second: tuple[str, str],
    a_vertices: tuple[str, ...],
    b_vertices: tuple[str, ...],
) -> tuple[str, ...]:
    """Return the explicit seven-cycle from the three-case proof."""
    a1, b1 = first
    a2, b2 = second
    p, q = "a0", "a1"

    if a1 == a2:
        c = next(a for a in a_vertices if a not in {p, q, a1})
        b3 = next(b for b in b_vertices if b not in {b1, b2})
        return (p, q, b3, c, b1, a1, b2)

    if b1 == b2:
        x, y = next(
            (x, y)
            for x, y in itertools.permutations(b_vertices, 2)
            if x != b1 and y != b1
        )
        return (p, q, x, a1, b1, a2, y)

    b3 = next(b for b in b_vertices if b not in {b1, b2})
    return (p, q, b3, a1, b1, a2, b2)


def verify(a_size: int, b_size: int) -> dict[str, object]:
    if a_size < 4 or b_size < 3:
        raise ValueError("the certificate requires |A|>=4 and |B|>=3")

    a_vertices = tuple(f"a{i}" for i in range(a_size))
    b_vertices = tuple(f"b{i}" for i in range(b_size))
    p, q = "a0", "a1"
    graph_edges = {
        edge(a, b) for a in a_vertices for b in b_vertices
    } | {edge(p, q)}
    family = tuple(
        (a, b)
        for a in a_vertices
        if a not in {p, q}
        for b in b_vertices
    )

    case_counts = {"same_A": 0, "same_B": 0, "disjoint": 0}
    checked = 0
    for first, second in itertools.combinations(family, 2):
        if first[0] == second[0]:
            case_counts["same_A"] += 1
        elif first[1] == second[1]:
            case_counts["same_B"] += 1
        else:
            case_counts["disjoint"] += 1

        cycle = witness(first, second, a_vertices, b_vertices)
        assert len(cycle) == 7
        assert len(set(cycle)) == 7
        used = cycle_edges(cycle)
        assert used <= graph_edges
        assert edge(*first) in used
        assert edge(*second) in used
        checked += 1

    return {
        "a_size": a_size,
        "b_size": b_size,
        "family_size": len(family),
        "expected_family_size": (a_size - 2) * b_size,
        "checked_edge_pairs": checked,
        "case_counts": case_counts,
        "passed": True,
    }


def main() -> None:
    payload = {
        "claim": (
            "In K_{a,b}+pq, all cross-edges whose A-end is outside "
            "{p,q} are pairwise contained in a C7."
        ),
        "instances": [verify(a, b) for a in range(4, 10) for b in range(3, 10)],
    }
    payload["passed"] = all(item["passed"] for item in payload["instances"])
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
