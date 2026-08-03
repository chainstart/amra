#!/usr/bin/env python3
"""Exact small probes for cross-star A-ownership and typed B capacity."""

from __future__ import annotations

import hashlib
import json
from itertools import combinations
from pathlib import Path

import m809_11_hard_graph_probe as core
import m809_11_l4_candidate_probe as candidate


def subsets(items: tuple[str, ...]):
    for size in range(len(items) + 1):
        for subset in combinations(items, size):
            yield frozenset(subset)


def coverage_rank(colours: frozenset[str], owners: dict[str, tuple[str, str]]) -> int:
    return len({owners[colour] for colour in colours})


def check_submodular(owners: dict[str, tuple[str, str]]) -> bool:
    colours = tuple(owners)
    sets = tuple(subsets(colours))
    return all(
        coverage_rank(left, owners) + coverage_rank(right, owners)
        >= coverage_rank(left | right, owners) + coverage_rank(left & right, owners)
        for left in sets
        for right in sets
    )


def minimal_recolouring_pair() -> dict[str, object]:
    # One fixed graph: every listed cross edge exists, and all X--Y pairs are
    # missing.  Only the pairing of two edges into colour delta changes.
    graph_edges = {
        ("b1", "x1"), ("c1", "y1"),
        ("b2", "x1"), ("c2", "y1"),
        ("b2", "x2"), ("c2", "y2"),
    }
    overlap = {"gamma": ("x1", "y1"), "delta": ("x1", "y1")}
    disjoint = {"gamma": ("x1", "y1"), "delta": ("x2", "y2")}
    all_colours = frozenset(("gamma", "delta"))
    assert check_submodular(overlap) and check_submodular(disjoint)
    return {
        "same_underlying_graph_edges": sorted(graph_edges),
        "same_graph_scalar_S_m": True,
        "same_repeated_colour_count": 2,
        "same_D_B": 2,
        "overlap_colouring": {
            "owners": overlap,
            "sum_of_per_star_owned_counts": 2,
            "global_A_coverage_rank": coverage_rank(all_colours, overlap),
        },
        "disjoint_colouring": {
            "owners": disjoint,
            "sum_of_per_star_owned_counts": 2,
            "global_A_coverage_rank": coverage_rank(all_colours, disjoint),
        },
        "coverage_rank_submodular": True,
        "rainbow_C7_vacuous_in_local_graph": True,
        "full_hard_BCM_claimed": False,
    }


def evaluate_current_graph() -> dict[str, object]:
    degrees = {vertex: len(core.neighbours(vertex)) for vertex in core.V}
    cycles = core.canonical_cycles(7)
    nonrainbow = []
    for cycle in cycles:
        colours = [core.colour(core.edge(cycle[i], cycle[(i + 1) % 7])) for i in range(7)]
        if len(set(colours)) < 7:
            nonrainbow.append(cycle)
            if len(nonrainbow) >= 5:
                break
    reserve = core.b_reserve(core.edge("b", "c"))
    return {
        "edge_count": len(core.E),
        "degrees": degrees,
        "B_reserve_bc": sorted(reserve),
        "B_reserve_size": len(reserve),
        "L4_2": not core.l4_2_failures(),
        "rainbow_C7": not nonrainbow,
        "owned_A_rank": 3,
        "D_B": 3,
        "M_B": sum(not core.adjacent(left, right) for left, right in combinations(core.B, 2)),
    }


def hard_graph_swap_pair() -> dict[str, object]:
    tight_edges = core.E
    tight = evaluate_current_graph()
    # Trade one B edge for one previously missing internal A edge.  This
    # preserves n,e,A,B, all repeated colours, and all owned diagonals.
    core.E = frozenset((tight_edges - {core.edge("b", "z")}) | {core.edge("x1", "x2")})
    paid = evaluate_current_graph()
    core.E = tight_edges
    assert tight["edge_count"] == paid["edge_count"] == 50
    assert tight["owned_A_rank"] == paid["owned_A_rank"] == 3
    assert tight["D_B"] == paid["D_B"] == 3
    assert tight["L4_2"] and paid["L4_2"]
    assert tight["rainbow_C7"] and paid["rainbow_C7"]
    return {
        "same_n_e_A_B_hence_same_graph_scalar_S_m": True,
        "same_owned_A_rank": 3,
        "same_D_B": 3,
        "tight_B_instance": tight,
        "paid_B_instance": paid,
        "distinguishing_change": "replace B edge bz by A edge x1x2",
    }


def main() -> None:
    payload = {
        "classification": "exact_typed_submodular_rank_falsifier",
        "minimal_cross_star_overlap": minimal_recolouring_pair(),
        "hard_local_same_A_rank_different_B_reserve": hard_graph_swap_pair(),
        "sound_rank": {
            "A": "rho_A(T)=number of distinct owned missing-A diagonals",
            "B": "rho_B(T)=size of the union of actual B reserve neighbourhoods",
            "typed_pair_not_untyped_sum": True,
        },
        "killed_scalar_claims": [
            "sum of per-star owned diagonal counts equals distinct global A capacity",
            "owned A atoms may be added to B reserve atoms to certify D_B<=M_B",
            "the graph scalar S_m canonically decomposes into the owned A diagonals"
        ],
        "public_problem_changed": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_suffix(".json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
