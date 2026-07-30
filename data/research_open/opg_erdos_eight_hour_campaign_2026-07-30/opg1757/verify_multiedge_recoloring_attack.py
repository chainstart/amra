#!/usr/bin/env python3
"""Audit a two-stage recolouring repair of the q=2, k=5 Hall kernel."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Iterable

from verify_global_cycle_opening import (
    E,
    F,
    Edge,
    Forest,
    Pair,
    cycle_opening_map,
    inverse_from_tag,
    is_forest,
    pair_row,
)


K = 5
VERTEX_COUNT = 6


def active_vertices(pair: Pair) -> frozenset[int]:
    return frozenset(
        vertex
        for forest in pair
        for edge in forest
        for vertex in edge
    )


def apply_protected_basis_exchange(
    vertex_count: int,
    pair: Pair,
    color: int,
    edge_out: Edge,
    edge_in: Edge,
) -> Pair:
    """Replace one edge in one colour, checking all proof hypotheses."""

    if color not in (0, 1):
        raise ValueError("color must be 0 (red) or 1 (blue)")
    forests = [pair[0], pair[1]]
    selected = forests[color]
    if edge_out not in selected or edge_in in selected:
        raise ValueError("basis exchange has invalid edge membership")
    if color == 0 and edge_out == E:
        raise ValueError("the red marked edge E is protected")
    if color == 1 and (edge_out == F or edge_in == E):
        raise ValueError("the blue marked edges E,F are protected")
    replacement = (selected - {edge_out}) | {edge_in}
    if not is_forest(vertex_count, replacement):
        raise ValueError("replacement does not preserve the forest")
    forests[color] = replacement
    return forests[0], forests[1]


def inverse_protected_basis_exchange(
    vertex_count: int,
    target: Pair,
    color: int,
    edge_out: Edge,
    edge_in: Edge,
) -> Pair:
    """Undo apply_protected_basis_exchange using its ordered edge tag."""

    forests = [target[0], target[1]]
    selected = forests[color]
    if edge_in not in selected or edge_out in selected:
        raise ValueError("target is incompatible with exchange tag")
    restored = (selected - {edge_in}) | {edge_out}
    if not is_forest(vertex_count, restored):
        raise ValueError("tag does not restore a forest")
    forests[color] = restored
    return forests[0], forests[1]


def tagged_two_stage_move(
    vertex_count: int,
    source: Pair,
    reserve: tuple[int, Edge, Edge] | None,
) -> tuple[Pair, tuple[Edge | None, tuple[int, Edge, Edge] | None]]:
    """Cycle-open, then optionally make one protected forest basis exchange."""

    base, opening_tag = cycle_opening_map(vertex_count, source)
    target = (
        base
        if reserve is None
        else apply_protected_basis_exchange(
            vertex_count, base, reserve[0], reserve[1], reserve[2]
        )
    )
    return target, (opening_tag, reserve)


def inverse_tagged_two_stage_move(
    vertex_count: int,
    target: Pair,
    tag: tuple[Edge | None, tuple[int, Edge, Edge] | None],
) -> Pair:
    opening_tag, reserve = tag
    base = (
        target
        if reserve is None
        else inverse_protected_basis_exchange(
            vertex_count,
            target,
            reserve[0],
            reserve[1],
            reserve[2],
        )
    )
    source = inverse_from_tag(base, opening_tag)
    replayed, replayed_tag = tagged_two_stage_move(
        vertex_count, source, reserve
    )
    if replayed != target or replayed_tag != tag:
        raise ValueError("tag does not replay the deterministic opening")
    return source


def load_old_enumerator():
    research_open = Path(__file__).resolve().parents[2]
    old_directory = (
        research_open
        / "q1_eight_hour_campaign_2026-07-29"
        / "opg1757"
    )
    sys.path.insert(0, str(old_directory))
    import verify_f_leading_first_active_potential as old  # type: ignore
    from verify_f_leading_swap_obstruction import (  # type: ignore
        all_forests,
    )

    return old, all_forests


def enumerate_k5():
    old, all_forests = load_old_enumerator()
    forests = all_forests(VERTEX_COUNT)
    forests_by_size: dict[int, list[Forest]] = defaultdict(list)
    for forest in forests:
        forests_by_size[len(forest)].append(forest)
    positives, negatives = old.enumerate_q2_layer(forests_by_size, K)
    return old, positives, negatives


def direct_or_single_targets(
    source: Pair, positive_index: dict[Pair, int]
) -> list[int]:
    red, blue = source
    blue_without_e = blue - {E}
    targets: set[int] = set()
    direct = positive_index.get((red | {E}, blue_without_e))
    if direct is not None:
        targets.add(direct)
    for edge in sorted(red):
        target = positive_index.get(
            ((red - {edge}) | {E}, blue_without_e | {edge})
        )
        if target is not None:
            targets.add(target)
    return sorted(targets)


def reserve_target_map(
    source: Pair,
    positive_index: dict[Pair, int],
    all_edges: Iterable[Edge],
) -> dict[int, tuple[int, Edge, Edge] | None]:
    """All one-basis-exchange reserves after deterministic cycle opening."""

    base, _ = cycle_opening_map(VERTEX_COUNT, source)
    targets: dict[int, tuple[int, Edge, Edge] | None] = {
        positive_index[base]: None
    }
    for color, forest in enumerate(base):
        for edge_out in sorted(forest):
            if edge_out == E or (color == 1 and edge_out == F):
                continue
            for edge_in in all_edges:
                if edge_in in forest:
                    continue
                try:
                    target = apply_protected_basis_exchange(
                        VERTEX_COUNT,
                        base,
                        color,
                        edge_out,
                        edge_in,
                    )
                except ValueError:
                    continue
                if active_vertices(target) != active_vertices(source):
                    continue
                target_index = positive_index.get(target)
                if target_index is not None:
                    targets.setdefault(
                        target_index, (color, edge_out, edge_in)
                    )
    return targets


def alternating_completion(
    adjacency: list[list[int]],
    source_to_target: list[int],
    target_to_source: list[int],
    base_sets: list[set[int]],
) -> list[list[dict[str, object]]]:
    """Complete a matching by deterministic alternating BFS paths."""

    paths: list[list[dict[str, object]]] = []
    unmatched = [
        source
        for source, target in enumerate(source_to_target)
        if target < 0
    ]
    for root in unmatched:
        queue = deque([root])
        source_predecessor: dict[int, int | None] = {root: None}
        target_predecessor: dict[int, int] = {}
        free_target: int | None = None
        while queue and free_target is None:
            source = queue.popleft()
            for target in adjacency[source]:
                if target in target_predecessor:
                    continue
                target_predecessor[target] = source
                following = target_to_source[target]
                if following < 0:
                    free_target = target
                    break
                if following not in source_predecessor:
                    source_predecessor[following] = target
                    queue.append(following)
        if free_target is None:
            raise AssertionError("expanded graph has no augmenting path")

        path: list[dict[str, object]] = []
        target = free_target
        while True:
            source = target_predecessor[target]
            path.append(
                {
                    "source_index": source,
                    "target_index": target,
                    "is_new_reserve_edge": target not in base_sets[source],
                }
            )
            preceding_target = source_predecessor[source]
            if preceding_target is None:
                break
            target = preceding_target
        path.reverse()
        for step in path:
            source = int(step["source_index"])
            target = int(step["target_index"])
            source_to_target[source] = target
            target_to_source[target] = source
        paths.append(path)
    return paths


def edge_json(edge: Edge | None) -> list[int] | None:
    return None if edge is None else list(edge)


def reserve_json(
    reserve: tuple[int, Edge, Edge] | None,
) -> dict[str, object] | None:
    if reserve is None:
        return None
    return {
        "color": "red" if reserve[0] == 0 else "blue",
        "edge_out": list(reserve[1]),
        "edge_in": list(reserve[2]),
    }


def object_row(index: int, pair: Pair) -> dict[str, object]:
    return {"index": index, **pair_row(pair)}


def build_audit() -> dict[str, object]:
    old, positives, negatives = enumerate_k5()
    positive_index = {
        pair: index for index, pair in enumerate(positives)
    }
    all_edges = tuple(itertools.combinations(range(VERTEX_COUNT), 2))

    base_adjacency: list[list[int]] = []
    expanded_adjacency: list[list[int]] = []
    reserve_maps: list[dict[int, tuple[int, Edge, Edge] | None]] = []
    for source in negatives:
        base_targets = direct_or_single_targets(source, positive_index)
        reserves = reserve_target_map(source, positive_index, all_edges)
        expanded = sorted(set(base_targets) | set(reserves))
        base_adjacency.append(base_targets)
        expanded_adjacency.append(expanded)
        reserve_maps.append(reserves)

    (
        source_to_target,
        target_to_source,
        base_matching_size,
    ) = old.hopcroft_karp(base_adjacency, len(positives))
    hall_sources, hall_targets = old.hall_witness(
        base_adjacency, source_to_target, target_to_source
    )
    if (len(hall_sources), len(hall_targets)) != (12, 6):
        raise AssertionError("the saved minimal Hall kernel changed")

    source_indices = sorted(hall_sources)
    target_indices = sorted(hall_targets)
    deterministic_buckets: dict[int, list[int]] = defaultdict(list)
    for source_index in source_indices:
        target, _ = cycle_opening_map(
            VERTEX_COUNT, negatives[source_index]
        )
        deterministic_buckets[positive_index[target]].append(source_index)

    union_to_sources: dict[
        frozenset[Edge], list[int]
    ] = defaultdict(list)
    for source_index in source_indices:
        union_to_sources[
            negatives[source_index][0] | negatives[source_index][1]
        ].append(source_index)
    same_union_blocks: list[dict[str, object]] = []
    for union, block_sources in sorted(
        union_to_sources.items(), key=lambda row: tuple(sorted(row[0]))
    ):
        union_targets = [
            index
            for index, pair in enumerate(positives)
            if pair[0] | pair[1] == union
        ]
        same_union_blocks.append(
            {
                "union_edges": [list(edge) for edge in sorted(union)],
                "source_indices": sorted(block_sources),
                "source_count": len(block_sources),
                "all_same_union_target_indices": union_targets,
                "all_same_union_target_count": len(union_targets),
                "hall_deficiency_with_arbitrary_recoloring": max(
                    0, len(block_sources) - len(union_targets)
                ),
            }
        )

    kernel_rows: list[dict[str, object]] = []
    kernel_reserve_adjacency: list[list[int]] = []
    for source_index in source_indices:
        target, opening_tag = cycle_opening_map(
            VERTEX_COUNT, negatives[source_index]
        )
        kernel_rows.append(
            {
                **object_row(source_index, negatives[source_index]),
                "direct_or_single_neighbor_indices": (
                    base_adjacency[source_index]
                ),
                "deterministic_target_index": positive_index[target],
                "opening_tag": edge_json(opening_tag),
                "reserve_neighbor_count": len(
                    reserve_maps[source_index]
                ),
            }
        )
        kernel_reserve_adjacency.append(
            sorted(reserve_maps[source_index])
        )
    (
        kernel_source_matching,
        _,
        kernel_matching_size,
    ) = old.hopcroft_karp(
        kernel_reserve_adjacency, len(positives)
    )
    kernel_matching_rows: list[dict[str, object]] = []
    for local_source, source_index in enumerate(source_indices):
        target_index = kernel_source_matching[local_source]
        reserve = reserve_maps[source_index][target_index]
        target, tag = tagged_two_stage_move(
            VERTEX_COUNT, negatives[source_index], reserve
        )
        if positive_index[target] != target_index:
            raise AssertionError("kernel move did not produce its target")
        if (
            inverse_tagged_two_stage_move(VERTEX_COUNT, target, tag)
            != negatives[source_index]
        ):
            raise AssertionError("kernel tagged inverse failed")
        kernel_matching_rows.append(
            {
                "source_index": source_index,
                "target": object_row(target_index, target),
                "opening_tag": edge_json(tag[0]),
                "reserve": reserve_json(reserve),
            }
        )

    base_sets = list(map(set, base_adjacency))
    augmenting_paths = alternating_completion(
        expanded_adjacency,
        source_to_target,
        target_to_source,
        base_sets,
    )
    expanded_matching_size = sum(
        target >= 0 for target in source_to_target
    )
    matched_targets = [
        target for target in source_to_target if target >= 0
    ]
    if len(set(matched_targets)) != len(matched_targets):
        raise AssertionError("alternating completion is not injective")
    if any(
        target not in expanded_adjacency[source]
        for source, target in enumerate(source_to_target)
        if target >= 0
    ):
        raise AssertionError("matching used an edge outside the graph")
    if expanded_matching_size != len(negatives):
        raise AssertionError("expanded q=2,k=5 matching is not complete")
    enriched_paths: list[list[dict[str, object]]] = []
    for path in augmenting_paths:
        enriched_path: list[dict[str, object]] = []
        for step in path:
            source_index = int(step["source_index"])
            target_index = int(step["target_index"])
            reserve = reserve_maps[source_index].get(target_index)
            if step["is_new_reserve_edge"] and reserve is None:
                raise AssertionError("new augmenting edge lacks reserve data")
            enriched_path.append(
                {
                    **step,
                    "reserve": reserve_json(reserve),
                }
            )
        enriched_paths.append(enriched_path)

    payload = {
        "scope": (
            "Exact q=2,k=5 enumeration on K6.  The expanded graph is the "
            "union of every valid direct/single E-exchange edge and every "
            "target obtained by one protected forest basis exchange after "
            "the deterministic global cycle-opening map."
        ),
        "layer": {
            "k": K,
            "negative_count": len(negatives),
            "positive_count": len(positives),
            "direct_or_single_edge_count": sum(map(len, base_adjacency)),
            "direct_or_single_matching_size": base_matching_size,
            "direct_or_single_deficiency": (
                len(negatives) - base_matching_size
            ),
            "expanded_edge_count": sum(map(len, expanded_adjacency)),
            "expanded_matching_size": expanded_matching_size,
            "expanded_deficiency": (
                len(negatives) - expanded_matching_size
            ),
            "augmenting_path_count": len(enriched_paths),
            "augmenting_path_lengths": [
                len(path) for path in enriched_paths
            ],
            "augmenting_paths": enriched_paths,
        },
        "hall_kernel": {
            "source_count": len(source_indices),
            "target_count": len(target_indices),
            "deficiency": len(source_indices) - len(target_indices),
            "source_rows": kernel_rows,
            "target_rows": [
                object_row(index, positives[index])
                for index in target_indices
            ],
            "collision_buckets": [
                {
                    "target_index": target,
                    "source_indices": sorted(sources),
                }
                for target, sources in sorted(
                    deterministic_buckets.items()
                )
            ],
            "same_union_blocks": same_union_blocks,
            "reserve_graph_matching_size": kernel_matching_size,
            "reserve_matching": kernel_matching_rows,
        },
    }
    return {
        "schema": "amra.opg1757.multiedge_recoloring_attack.v1",
        "claim_labels": {
            "protected_basis_exchange_forest_preservation": "human_proof",
            "two_stage_tagged_reversibility": "human_proof",
            "weighted_fibre_compensation_lemma": "human_proof",
            "opg_unit_weights_satisfy_compensation_hypothesis": "open_gap",
            "strict_union_preserving_repair_of_eight_source_block": "refuted",
            "six_inclusion_minimal_two_to_one_hall_components": (
                "finite_evidence"
            ),
            "q2_k5_expanded_untagged_injection": "finite_evidence",
            "all_q_all_k_untagged_injection": "open_gap",
            "bounded_congestion_weight_compensation": "open_gap",
            "full_first_coefficient_positivity": "open_gap",
        },
        **payload,
        "sha256_payload": hashlib.sha256(
            json.dumps(
                payload, separators=(",", ":"), sort_keys=True
            ).encode()
        ).hexdigest(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name(
            "multiedge_recoloring_attack_certificate.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audit = build_audit()
    args.output.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(f"CERTIFICATE|sha256={audit['sha256_payload']}")


if __name__ == "__main__":
    main()
