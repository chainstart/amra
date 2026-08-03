#!/usr/bin/env python3
"""Bounded necessary-condition search for the M809-11 sharp bad pattern.

The B-graph scan is a relaxation: it enforces the exact B-side zero-shore
reserve definition but not the full BCM edge count, L4(2), or colouring.
Failure in this relaxation is a valid no-realization certificate in the
scanned domain; success would still require a full-graph lift.
"""

from __future__ import annotations

import hashlib
import json
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path


TARGET = (
    frozenset({"q1"}),
    frozenset({"q1", "q2"}),
    frozenset({"q2"}),
)


def target_base_assignment_models() -> list[tuple[str, str, str]]:
    models = []
    for bases in (tuple(choice) for choice in __import__("itertools").product(("q1", "q2"), repeat=3)):
        if any(bases[index] not in TARGET[index] for index in range(3)):
            continue
        if any(bases[i] == bases[j] and TARGET[i] != TARGET[j] for i, j in combinations(range(3), 2)):
            continue
        models.append(bases)
    return models


def minimum_opposite_rectangle(colour_count: int) -> dict[str, object]:
    feasible = []
    for x_size in range(1, colour_count + 1):
        for y_size in range(1, colour_count + 1):
            assignments = 0
            for xs in permutations(range(x_size), colour_count):
                for ys in permutations(range(y_size), colour_count):
                    assignments += 1
                    owned_pairs = {(x, y) for x, y in zip(xs, ys)}
                    assert len(owned_pairs) == colour_count
            if assignments:
                feasible.append((x_size * y_size, x_size, y_size, assignments))
    minimum = min(feasible)
    return {
        "colour_count": colour_count,
        "minimum_X_size": minimum[1],
        "minimum_Y_size": minimum[2],
        "minimum_missing_A_rectangle_atoms": minimum[0],
        "distinct_owned_diagonal_atoms": colour_count,
        "assignments_at_minimum": minimum[3],
        "one_by_one_rectangle_feasible": minimum[0] <= 1,
    }


def b_reserve(n: int, edges: frozenset[tuple[int, int]], pair: tuple[int, int]) -> frozenset[tuple[int, int]] | None:
    b, c = pair
    neighbours_b = {v for v in range(n) if tuple(sorted((b, v))) in edges and v != b}
    neighbours_c = {v for v in range(n) if tuple(sorted((c, v))) in edges and v != c}
    # Exact simple three-edge B-shore obstruction.
    for p in neighbours_b:
        for q in neighbours_c:
            if p != q and tuple(sorted((p, q))) in edges:
                return None
    missing = {
        pair0
        for pair0 in combinations(range(n), 2)
        if pair0 not in edges
    }
    reserve = {edge for edge in missing if b in edge or c in edge}
    reserve.update(
        tuple(sorted((p, q)))
        for p in neighbours_b
        for q in neighbours_c
        if p != q
    )
    assert pair in reserve
    assert reserve <= missing
    return frozenset(reserve)


def scan_b_graphs(n_max: int = 6) -> dict[str, object]:
    graphs = 0
    zero_pairs = 0
    first_tight = None
    first_target = None
    for n in range(2, n_max + 1):
        all_pairs = tuple(combinations(range(n), 2))
        for mask in range(1 << len(all_pairs)):
            graphs += 1
            edges = frozenset(edge for index, edge in enumerate(all_pairs) if mask & (1 << index))
            reserves = []
            for pair in all_pairs:
                if pair in edges:
                    continue
                reserve = b_reserve(n, edges, pair)
                if reserve is not None:
                    zero_pairs += 1
                    reserves.append((pair, reserve))
            for triple in combinations_with_replacement(range(len(reserves)), 3):
                neighbourhoods = tuple(reserves[index][1] for index in triple)
                union = frozenset().union(*neighbourhoods)
                if len(union) != 2:
                    continue
                if any(len(neighbourhoods[i] | neighbourhoods[j]) < 2 for i, j in combinations(range(3), 2)):
                    continue
                row = {
                    "n_B": n,
                    "B_edges": sorted(edges),
                    "base_pairs": [reserves[index][0] for index in triple],
                    "reserve_neighbourhoods": [sorted(reserves[index][1]) for index in triple],
                }
                if first_tight is None:
                    first_tight = row
                relabel = {token: name for token, name in zip(sorted(union), ("q1", "q2"))}
                relabelled = tuple(frozenset(relabel[token] for token in neighbourhood) for neighbourhood in neighbourhoods)
                if sorted(map(sorted, relabelled)) == sorted(map(sorted, TARGET)):
                    first_target = row
                    break
            if first_target is not None:
                break
        if first_target is not None:
            break
    return {
        "n_B_max": n_max,
        "B_graphs_checked": graphs,
        "zero_shore_B_pairs_checked": zero_pairs,
        "first_three_colour_tight_full_reserve_circuit": first_tight,
        "first_exact_path_target": first_target,
    }


def main() -> None:
    base_models = target_base_assignment_models()
    payload = {
        "classification": "bounded_real_graph_necessary_condition_probe",
        "exact_full_reserve_translation": {
            "constraints": [
                "each colour base pair belongs to its own reserve neighbourhood",
                "colours with the same base pair have identical full reserve neighbourhoods",
            ],
            "models_for_path_neighbourhoods": base_models,
            "path_pattern_realisable": bool(base_models),
        },
        "opposite_star_inner_endpoint_translation": minimum_opposite_rectangle(3),
        "relaxed_B_graph_scan": scan_b_graphs(),
        "full_hard_BCM_realisation_claimed": False,
        "public_problem_changed": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_suffix(".json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
