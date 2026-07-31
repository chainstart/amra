#!/usr/bin/env python3
"""Finite guards for the fifth 2026-07-31 Erdős #809 attack."""

from __future__ import annotations

import itertools
import json


def edge(left: str, right: str) -> frozenset[str]:
    return frozenset((left, right))


def zero_shore_rectangle_guard(h: int = 12) -> dict[str, int | bool]:
    """Build h induced colour pairs and check their h-by-h missing block."""
    x_side = [f"x{index}" for index in range(h)]
    y_side = [f"y{index}" for index in range(h)]
    vertices = {"v", "b", "bp", *x_side, *y_side}
    graph_edges = {
        edge("v", item) for item in x_side + y_side
    } | {
        edge("b", item) for item in x_side
    } | {
        edge("bp", item) for item in y_side
    }

    for index in range(h):
        colour_pair = {
            edge("b", x_side[index]),
            edge("bp", y_side[index]),
        }
        endpoints = set().union(*colour_pair)
        induced_edges = {
            item for item in graph_edges if item <= endpoints
        }
        assert induced_edges == colour_pair

    missing_rectangle = {
        edge(left, right) for left in x_side for right in y_side
    }
    assert not (missing_rectangle & graph_edges)
    assert len(missing_rectangle) == h * h
    return {
        "vertices": len(vertices),
        "colours": h,
        "missing_rectangle": len(missing_rectangle),
        "claimed_lower_bound": h * h,
        "passed": True,
    }


def branch_one_bound_guard(
    n: int = 80, delta: int = 34, h: int = 10
) -> dict[str, int | bool]:
    """Check the exact Branch-I chain 2h <= |W| <= 2n-4delta."""
    w_upper = 2 * n - 4 * delta
    assert 2 * h <= w_upper
    return {
        "n": n,
        "delta": delta,
        "colours": h,
        "coordinate_vertices": 2 * h,
        "W_upper_bound": w_upper,
        "lambda_upper_bound": n - 2 * delta,
        "passed": True,
    }


def connector_transversal_guard() -> dict[str, int | bool]:
    """Three disjoint P-L-Q connectors survive any two deletions."""
    triples = [
        frozenset((f"p{index}", f"l{index}", f"q{index}"))
        for index in range(3)
    ]
    internal_vertices = set().union(*triples)

    for deletion_size in range(3):
        for deleted in itertools.combinations(
            sorted(internal_vertices), deletion_size
        ):
            deleted_set = set(deleted)
            assert any(not (set(item) & deleted_set) for item in triples)

    transversal_number = next(
        size
        for size in range(len(internal_vertices) + 1)
        if any(
            all(set(chosen) & set(item) for item in triples)
            for chosen in itertools.combinations(
                sorted(internal_vertices), size
            )
        )
    )
    assert transversal_number == 3
    return {
        "connector_triples": len(triples),
        "middle_vertices": 3,
        "transversal_number": transversal_number,
        "passed": True,
    }


def main() -> None:
    result = {
        "zero_shore_rectangle": zero_shore_rectangle_guard(),
        "branch_one_bound": branch_one_bound_guard(),
        "connector_transversal": connector_transversal_guard(),
        "scope": (
            "Finite local guards only; the fixed-s aggregate zero-shore "
            "bypass and Erdos #809 remain open."
        ),
        "passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
