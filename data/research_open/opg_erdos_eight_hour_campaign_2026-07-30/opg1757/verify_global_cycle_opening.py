#!/usr/bin/env python3
"""Verify a deterministic global cycle-opening exchange for OPG-1757."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Iterable


Edge = tuple[int, int]
Forest = frozenset[Edge]
Pair = tuple[Forest, Forest]
E: Edge = (0, 1)
F: Edge = (2, 3)


def canonical_edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def component_labels(vertex_count: int, forest: Forest) -> tuple[int, ...]:
    parent = list(range(vertex_count))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in forest:
        left_root = root(left)
        right_root = root(right)
        if left_root == right_root:
            raise ValueError("component_labels requires a forest")
        parent[left_root] = right_root
    return tuple(root(vertex) for vertex in range(vertex_count))


def forest_path(
    vertex_count: int, forest: Forest, start: int, end: int
) -> tuple[Edge, ...] | None:
    adjacency: list[list[int]] = [[] for _ in range(vertex_count)]
    for left, right in forest:
        adjacency[left].append(right)
        adjacency[right].append(left)
    predecessor: dict[int, int] = {start: -1}
    queue = deque([start])
    while queue and end not in predecessor:
        vertex = queue.popleft()
        for following in sorted(adjacency[vertex]):
            if following in predecessor:
                continue
            predecessor[following] = vertex
            queue.append(following)
    if end not in predecessor:
        return None
    vertices = [end]
    while vertices[-1] != start:
        vertices.append(predecessor[vertices[-1]])
    vertices.reverse()
    return tuple(
        canonical_edge(left, right)
        for left, right in zip(vertices, vertices[1:])
    )


def is_forest(vertex_count: int, edges: Iterable[Edge]) -> bool:
    parent = list(range(vertex_count))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left_root = root(left)
        right_root = root(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def cycle_opening_map(
    vertex_count: int, source: Pair
) -> tuple[Pair, Edge | None]:
    """Move E from blue to red; return the image and reversible edge tag."""

    red, blue = source
    if E in red or E not in blue:
        raise ValueError("source is not in the reduced negative class")
    red_path = forest_path(vertex_count, red, E[0], E[1])
    blue_without_e = blue - {E}
    if red_path is None:
        target = (red | {E}, blue_without_e)
        if not is_forest(vertex_count, target[0]):
            raise AssertionError("direct red move created a cycle")
        if (
            len(target[0]) + len(target[1]) != len(red) + len(blue)
            or target[0] | target[1] != red | blue
        ):
            raise AssertionError("direct move changed weight or support")
        return target, None

    blue_components = component_labels(vertex_count, blue_without_e)
    exchange_edge = next(
        (
            edge
            for edge in red_path
            if blue_components[edge[0]] != blue_components[edge[1]]
        ),
        None,
    )
    if exchange_edge is None:
        raise AssertionError(
            "red E-path stayed inside components of B-E"
        )
    target = (
        (red - {exchange_edge}) | {E},
        blue_without_e | {exchange_edge},
    )
    if not is_forest(vertex_count, target[0]):
        raise AssertionError("cycle opening did not repair red")
    if not is_forest(vertex_count, target[1]):
        raise AssertionError("exchange edge closed a blue cycle")
    if exchange_edge in blue:
        raise AssertionError("exchange edge was already blue")
    if (
        len(target[0]) + len(target[1]) != len(red) + len(blue)
        or target[0] | target[1] != red | blue
    ):
        raise AssertionError("exchange changed weight or support")
    return target, exchange_edge


def inverse_from_tag(target: Pair, tag: Edge | None) -> Pair:
    red, blue = target
    if E not in red or E in blue:
        raise ValueError("target is not in the reduced positive class")
    if tag is None:
        return red - {E}, blue | {E}
    if tag not in blue or tag in red:
        raise ValueError("invalid exchange tag")
    return (red - {E}) | {tag}, (blue - {tag}) | {E}


def edge_rows(forest: Forest) -> list[list[int]]:
    return [list(edge) for edge in sorted(forest)]


def pair_row(pair: Pair) -> dict[str, list[list[int]]]:
    return {"red": edge_rows(pair[0]), "blue": edge_rows(pair[1])}


def all_forests(vertex_count: int) -> tuple[Forest, ...]:
    edges = tuple(itertools.combinations(range(vertex_count), 2))
    rows: list[Forest] = []
    for mask in range(1 << len(edges)):
        selected = frozenset(
            edge
            for index, edge in enumerate(edges)
            if mask & (1 << index)
        )
        if is_forest(vertex_count, selected):
            rows.append(selected)
    return tuple(rows)


def small_complete_graph_audit() -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for vertex_count in range(2, 6):
        forests = all_forests(vertex_count)
        red_forests = [forest for forest in forests if E not in forest]
        blue_forests = [forest for forest in forests if E in forest]
        images: defaultdict[Pair, int] = defaultdict(int)
        tagged_images: set[tuple[Pair, Edge | None]] = set()
        direct_count = 0
        for red in red_forests:
            for blue in blue_forests:
                source = (red, blue)
                target, tag = cycle_opening_map(vertex_count, source)
                if inverse_from_tag(target, tag) != source:
                    raise AssertionError("small-graph tagged inverse failed")
                if (target, tag) in tagged_images:
                    raise AssertionError("small-graph tagged collision")
                tagged_images.add((target, tag))
                images[target] += 1
                direct_count += int(tag is None)
        rows.append(
            {
                "vertex_count": vertex_count,
                "forest_count": len(forests),
                "source_pair_count": len(red_forests) * len(blue_forests),
                "direct_move_count": direct_count,
                "cycle_opening_exchange_count": (
                    len(tagged_images) - direct_count
                ),
                "tagged_image_count": len(tagged_images),
                "untagged_image_count": len(images),
                "maximum_untagged_preimage": max(images.values()),
            }
        )
    return rows


def q2_finite_audit() -> dict[str, object]:
    research_open = Path(__file__).resolve().parents[2]
    old_directory = (
        research_open
        / "q1_eight_hour_campaign_2026-07-29"
        / "opg1757"
    )
    sys.path.insert(0, str(old_directory))
    import verify_f_leading_first_active_potential as old  # type: ignore
    from verify_f_leading_swap_obstruction import all_forests  # type: ignore

    forests = all_forests(old.Q2_VERTEX_COUNT)
    forests_by_size: dict[int, list[Forest]] = defaultdict(list)
    for forest in forests:
        forests_by_size[len(forest)].append(forest)

    layer_rows: list[dict[str, object]] = []
    first_collision: dict[str, object] | None = None
    first_direct_or_single_exchange_hall_witness: dict[str, object] | None = None
    maximum_preimage = 0
    for k in range(1, 8):
        positives, negatives = old.enumerate_q2_layer(forests_by_size, k)
        positive_set = set(positives)
        positive_index = {
            pair: index for index, pair in enumerate(positives)
        }
        image_sources: defaultdict[Pair, list[tuple[int, Edge | None]]] = (
            defaultdict(list)
        )
        direct_or_single_exchange_rows: list[list[int]] = []
        direct_count = 0
        tagged_images: set[tuple[Pair, Edge | None]] = set()
        for source_index, source in enumerate(negatives):
            target, tag = cycle_opening_map(
                old.Q2_VERTEX_COUNT, source
            )
            if target not in positive_set:
                raise AssertionError(
                    f"cycle-opening image left positive layer k={k}"
                )
            if inverse_from_tag(target, tag) != source:
                raise AssertionError("tagged inverse failed")
            tagged = (target, tag)
            if tagged in tagged_images:
                raise AssertionError("tagged map collided")
            tagged_images.add(tagged)
            image_sources[target].append((source_index, tag))
            direct_count += int(tag is None)
            red, blue = source
            candidates = {positive_index[target]}
            blue_without_e = blue - {E}
            direct = (red | {E}, blue_without_e)
            if direct in positive_index:
                candidates.add(positive_index[direct])
            for exchange_edge in red:
                exchanged = (
                    (red - {exchange_edge}) | {E},
                    blue_without_e | {exchange_edge},
                )
                target_index = positive_index.get(exchanged)
                if target_index is None:
                    continue
                if not is_forest(
                    old.Q2_VERTEX_COUNT, exchanged[0]
                ) or not is_forest(old.Q2_VERTEX_COUNT, exchanged[1]):
                    raise AssertionError(
                        "positive index admitted a cyclic exchange"
                    )
                candidates.add(target_index)
            direct_or_single_exchange_rows.append(sorted(candidates))
        (
            union_source_matching,
            union_target_matching,
            union_matching_size,
        ) = old.hopcroft_karp(
            direct_or_single_exchange_rows, len(positives)
        )
        union_deficiency = len(negatives) - union_matching_size
        if (
            union_deficiency
            and first_direct_or_single_exchange_hall_witness is None
        ):
            hall_sources, hall_targets = old.hall_witness(
                direct_or_single_exchange_rows,
                union_source_matching,
                union_target_matching,
            )
            first_direct_or_single_exchange_hall_witness = {
                "k": k,
                "source_count": len(hall_sources),
                "target_count": len(hall_targets),
                "deficiency": len(hall_sources) - len(hall_targets),
                "source_indices": sorted(hall_sources),
                "target_indices": sorted(hall_targets),
                "first_source": {
                    "index": min(hall_sources),
                    **pair_row(negatives[min(hall_sources)]),
                    "neighbor_indices": direct_or_single_exchange_rows[
                        min(hall_sources)
                    ],
                },
            }
        multiplicities = Counter(
            len(sources) for sources in image_sources.values()
        )
        layer_maximum = max(multiplicities, default=0)
        maximum_preimage = max(maximum_preimage, layer_maximum)
        if first_collision is None:
            collision_targets = [
                (target, sources)
                for target, sources in image_sources.items()
                if len(sources) > 1
            ]
            if collision_targets:
                target, sources = min(
                    collision_targets,
                    key=lambda row: (
                        len(row[1]),
                        old.pair_key(row[0]),
                    ),
                )
                first_collision = {
                    "k": k,
                    "target": pair_row(target),
                    "source_indices_and_tags": [
                        [
                            source_index,
                            None if tag is None else list(tag),
                        ]
                        for source_index, tag in sources
                    ],
                    "source_rows": [
                        {
                            "index": source_index,
                            "tag": None if tag is None else list(tag),
                            **pair_row(negatives[source_index]),
                        }
                        for source_index, tag in sources
                    ],
                }
        layer_rows.append(
            {
                "k": k,
                "negative_count": len(negatives),
                "positive_count": len(positives),
                "direct_move_count": direct_count,
                "cycle_opening_exchange_count": (
                    len(negatives) - direct_count
                ),
                "tagged_image_count": len(tagged_images),
                "untagged_distinct_image_count": len(image_sources),
                "untagged_collision_excess": (
                    len(negatives) - len(image_sources)
                ),
                "maximum_untagged_preimage": layer_maximum,
                "direct_or_single_exchange_edge_count": sum(
                    map(len, direct_or_single_exchange_rows)
                ),
                "direct_or_single_exchange_matching_size": (
                    union_matching_size
                ),
                "direct_or_single_exchange_matching_deficiency": (
                    union_deficiency
                ),
                "untagged_preimage_multiplicity_counts": {
                    str(multiplicity): count
                    for multiplicity, count in sorted(
                        multiplicities.items()
                    )
                },
            }
        )
    return {
        "scope": (
            "Exact finite audit of the deterministic global cycle-opening "
            "map on every q=2 layer k=1,...,7 from the prior campaign. "
            "The larger matching graph contains every valid direct move "
            "and every valid single E<->x exchange; it does not contain "
            "multi-edge recolorings."
        ),
        "layer_rows": layer_rows,
        "maximum_untagged_preimage_k1_to_k7": maximum_preimage,
        "first_untagged_collision": first_collision,
        "first_direct_or_single_exchange_hall_witness": (
            first_direct_or_single_exchange_hall_witness
        ),
    }


def build_audit() -> dict[str, object]:
    finite = q2_finite_audit()
    payload = {
        "small_complete_graph_rows": small_complete_graph_audit(),
        "q2_finite_audit": finite,
    }
    return {
        "schema": "amra.opg1757.global_cycle_opening.v1",
        "claim_labels": {
            "one_step_cycle_opening_exchange": "human_proof",
            "tagged_reversibility": "human_proof",
            "untagged_preimage_bound": "human_proof",
            "q2_layers_k1_to_k7": "finite_evidence",
            "untagged_injection": "refuted",
            "direct_or_single_exchange_injection_q2_k5": (
                "refuted_by_finite_hall_witness"
            ),
            "full_first_coefficient_positivity": "open_gap",
        },
        **payload,
        "sha256_payload": hashlib.sha256(
            json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
        ).hexdigest(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name(
            "global_cycle_opening_certificate.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.write_text(
        json.dumps(build_audit(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)


if __name__ == "__main__":
    main()
