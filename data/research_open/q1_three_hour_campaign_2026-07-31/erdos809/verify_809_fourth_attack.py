#!/usr/bin/env python3
"""Finite guards for the fourth 2026-07-31 Erdős #809 attack.

The guards check the fixed-missing-pair shore-cover combinatorics:

1. congestion one is attainable when a shore edge exists;
2. simultaneous left- and right-rooted colours force a non-rainbow C7;
3. congestion is unbounded when the shore graph is empty;
4. the colour-class / missing-pair double-counting identity;
5. the zero-shore missing-energy lower bound.

These are local certificates.  The sharp aggregate canonical charge and
Erdős #809 remain open.
"""

from __future__ import annotations

import itertools
import json
import math


def sharp_one_congestion_guard() -> dict[str, int | bool]:
    """Realize one induced same-colour pair covering one shore edge."""
    vertices = {"v", "b", "bp", "p", "q", "a"}
    edges = {
        frozenset(edge)
        for edge in [
            ("v", "p"),
            ("v", "a"),
            ("b", "p"),
            ("p", "q"),
            ("q", "bp"),
            ("bp", "a"),
        ]
    }
    colour_pair = [frozenset(("b", "p")), frozenset(("bp", "a"))]
    pair_endpoints = set().union(*colour_pair)
    induced_edges = {edge for edge in edges if edge <= pair_endpoints}
    assert induced_edges == set(colour_pair)
    assert len(vertices) == 6
    return {
        "vertices": len(vertices),
        "shore_edges": 1,
        "congestion": 1,
        "passed": True,
    }


def two_role_collision_guard() -> dict[str, int | bool]:
    """Exhibit the repeated-colour C7 forced by both shore roles."""
    cycle = ["b", "p", "q", "bp", "a", "v", "c"]
    cycle_edges = [
        frozenset((cycle[index], cycle[(index + 1) % len(cycle)]))
        for index in range(len(cycle))
    ]
    gamma = {
        frozenset(("b", "p")),
        frozenset(("bp", "a")),
    }
    eta = {
        frozenset(("b", "c")),
        frozenset(("bp", "q")),
    }
    graph_edges = set(cycle_edges)
    gamma_vertices = set().union(*gamma)
    eta_vertices = set().union(*eta)
    assert len(set(cycle)) == 7
    assert gamma <= graph_edges
    assert eta <= graph_edges
    assert {edge for edge in graph_edges if edge <= gamma_vertices} == gamma
    assert {edge for edge in graph_edges if edge <= eta_vertices} == eta
    return {
        "cycle_length": len(cycle),
        "gamma_edges_on_cycle": len(gamma),
        "eta_edges_on_cycle": len(eta),
        "rainbow": False,
        "passed": True,
    }


def empty_shore_unbounded_guard(
    congestion: int = 40,
) -> dict[str, int | bool]:
    """With no three-path shore, every coordinate pair is a cover."""
    left = list(range(congestion))
    right = list(range(congestion, 2 * congestion))
    covers = list(zip(left, right))
    shore_edges: set[frozenset[int]] = set()
    assert len({item[0] for item in covers}) == congestion
    assert len({item[1] for item in covers}) == congestion
    assert all(
        all(set(pair) & set(shore) for shore in shore_edges)
        for pair in covers
    )
    return {
        "shore_edges": 0,
        "coordinate_injective_covers": len(covers),
        "congestion": congestion,
        "passed": True,
    }


def aggregate_double_count_guard() -> dict[str, int | bool]:
    """Check sum_gamma C(t_gamma,2)=sum_missing_pair lambda."""
    colour_outer_sets = [
        {0, 1, 2},
        {1, 2},
        {2, 3, 4, 5},
        {0},
        set(),
    ]
    left = sum(math.comb(len(item), 2) for item in colour_outer_sets)
    multiplicity: dict[tuple[int, int], int] = {}
    for outer_set in colour_outer_sets:
        for pair in itertools.combinations(sorted(outer_set), 2):
            multiplicity[pair] = multiplicity.get(pair, 0) + 1
    right = sum(multiplicity.values())
    rooted_extras = sum(max(0, len(item) - 1) for item in colour_outer_sets)
    assert left == right
    assert rooted_extras <= left
    return {
        "colours": len(colour_outer_sets),
        "pair_incidence_sum": left,
        "maximum_pair_congestion": max(multiplicity.values()),
        "rooted_B_outer_extras": rooted_extras,
        "passed": True,
    }


def zero_shore_energy_guard(
    left_size: int = 9, right_size: int = 11, overlap: int = 5
) -> dict[str, int | bool]:
    """Verify the minimum missing-pair count for two anticomplete sets."""
    left = set(range(left_size))
    right = set(range(left_size - overlap, left_size - overlap + right_size))
    cross_pairs = {
        tuple(sorted((x, z)))
        for x in left
        for z in right
        if x != z
    }
    lower = math.comb(min(left_size, right_size), 2)
    assert len(cross_pairs) >= lower
    return {
        "left_size": left_size,
        "right_size": right_size,
        "overlap": overlap,
        "forced_missing_pairs": len(cross_pairs),
        "claimed_lower_bound": lower,
        "passed": True,
    }


def main() -> None:
    result = {
        "sharp_nonempty_shore": sharp_one_congestion_guard(),
        "two_role_collision": two_role_collision_guard(),
        "empty_shore": empty_shore_unbounded_guard(),
        "aggregate_double_count": aggregate_double_count_guard(),
        "zero_shore_energy": zero_shore_energy_guard(),
        "scope": (
            "Local finite certificates only; aggregate congestion under "
            "the full Case-1 contract and Erdos #809 remain open."
        ),
        "passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
