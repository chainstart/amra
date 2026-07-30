#!/usr/bin/env python3
"""Independent bit-mask audit of the q=2 multiedge recolouring graph.

This file deliberately does not import either multiedge verifier or the old
Hopcroft--Karp implementation.  It rebuilds the K6 forests, signed layers,
candidate edges, and augmenting-path matchings from bit masks.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import struct
from collections import Counter, defaultdict, deque
from pathlib import Path


VERTEX_COUNT = 6
EDGES = tuple(itertools.combinations(range(VERTEX_COUNT), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
E_INDEX = EDGE_INDEX[(0, 1)]
F_INDEX = EDGE_INDEX[(2, 3)]
E_BIT = 1 << E_INDEX
F_BIT = 1 << F_INDEX
ALL_ACTIVE = (1 << VERTEX_COUNT) - 1


def edge_bit(edge: tuple[int, int]) -> int:
    return 1 << EDGE_INDEX[tuple(sorted(edge))]


def is_forest(mask: int) -> bool:
    parent = list(range(VERTEX_COUNT))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for index, (left, right) in enumerate(EDGES):
        if not mask & (1 << index):
            continue
        left_root = root(left)
        right_root = root(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def active_mask(pair: tuple[int, int]) -> int:
    active = 0
    union = pair[0] | pair[1]
    for index, (left, right) in enumerate(EDGES):
        if union & (1 << index):
            active |= (1 << left) | (1 << right)
    return active


def mask_edges(mask: int) -> list[list[int]]:
    return [
        list(edge)
        for index, edge in enumerate(EDGES)
        if mask & (1 << index)
    ]


def pair_row(pair: tuple[int, int]) -> dict[str, list[list[int]]]:
    return {"red": mask_edges(pair[0]), "blue": mask_edges(pair[1])}


def row_pair(row: dict[str, object]) -> tuple[int, int]:
    def convert(edges: object) -> int:
        mask = 0
        for raw in edges:  # type: ignore[union-attr]
            mask |= edge_bit(tuple(raw))
        return mask

    return convert(row["red"]), convert(row["blue"])


def all_forests_by_size() -> tuple[dict[int, list[int]], set[int]]:
    rows: dict[int, list[int]] = defaultdict(list)
    forest_set: set[int] = set()
    for mask in range(1 << len(EDGES)):
        if is_forest(mask):
            rows[mask.bit_count()].append(mask)
            forest_set.add(mask)
    return dict(rows), forest_set


def enumerate_layer(
    forests_by_size: dict[int, list[int]], k: int
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    positives: list[tuple[int, int]] = []
    negatives: list[tuple[int, int]] = []
    for red_size in range(VERTEX_COUNT):
        blue_size = k + 2 - red_size
        if not 0 <= blue_size < VERTEX_COUNT:
            continue
        reds = forests_by_size.get(red_size, [])
        blues = [
            blue
            for blue in forests_by_size.get(blue_size, [])
            if blue & F_BIT
        ]
        for red in reds:
            red_has_e = bool(red & E_BIT)
            for blue in blues:
                blue_has_e = bool(blue & E_BIT)
                if red_has_e == blue_has_e:
                    continue
                pair = (red, blue)
                if active_mask(pair) != ALL_ACTIVE:
                    continue
                if red_has_e:
                    positives.append(pair)
                else:
                    negatives.append(pair)
    return positives, negatives


def component_labels(mask: int) -> tuple[int, ...]:
    parent = list(range(VERTEX_COUNT))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for index, (left, right) in enumerate(EDGES):
        if mask & (1 << index):
            parent[root(left)] = root(right)
    return tuple(root(vertex) for vertex in range(VERTEX_COUNT))


def forest_path(mask: int, start: int, end: int) -> list[int] | None:
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(VERTEX_COUNT)
    ]
    for index, (left, right) in enumerate(EDGES):
        if mask & (1 << index):
            adjacency[left].append((right, index))
            adjacency[right].append((left, index))
    predecessor: dict[int, tuple[int, int]] = {start: (-1, -1)}
    queue = deque([start])
    while queue and end not in predecessor:
        vertex = queue.popleft()
        for following, edge_index in sorted(adjacency[vertex]):
            if following in predecessor:
                continue
            predecessor[following] = (vertex, edge_index)
            queue.append(following)
    if end not in predecessor:
        return None
    path: list[int] = []
    vertex = end
    while vertex != start:
        previous, edge_index = predecessor[vertex]
        path.append(edge_index)
        vertex = previous
    path.reverse()
    return path


def cycle_open(
    source: tuple[int, int], forest_set: set[int]
) -> tuple[tuple[int, int], int | None]:
    red, blue = source
    path = forest_path(red, 0, 1)
    blue_without_e = blue ^ E_BIT
    if path is None:
        target = red | E_BIT, blue_without_e
        if target[0] not in forest_set or target[1] not in forest_set:
            raise AssertionError("independent direct opening failed")
        return target, None
    labels = component_labels(blue_without_e)
    exchange_index = next(
        index
        for index in path
        if labels[EDGES[index][0]] != labels[EDGES[index][1]]
    )
    exchange_bit = 1 << exchange_index
    target = (
        (red ^ exchange_bit) | E_BIT,
        blue_without_e | exchange_bit,
    )
    if target[0] not in forest_set or target[1] not in forest_set:
        raise AssertionError("independent exchange opening failed")
    return target, exchange_index


def direct_single_targets(
    source: tuple[int, int],
    positive_index: dict[tuple[int, int], int],
) -> set[int]:
    red, blue = source
    blue_without_e = blue ^ E_BIT
    targets: set[int] = set()
    direct = positive_index.get((red | E_BIT, blue_without_e))
    if direct is not None:
        targets.add(direct)
    for index in range(len(EDGES)):
        bit = 1 << index
        if not red & bit:
            continue
        target = positive_index.get(
            ((red ^ bit) | E_BIT, blue_without_e | bit)
        )
        if target is not None:
            targets.add(target)
    return targets


def reserve_targets(
    source: tuple[int, int],
    positive_index: dict[tuple[int, int], int],
    forest_set: set[int],
) -> dict[int, tuple[int, int, int] | None]:
    base, _ = cycle_open(source, forest_set)
    targets: dict[int, tuple[int, int, int] | None] = {
        positive_index[base]: None
    }
    for color, selected in enumerate(base):
        for edge_out in range(len(EDGES)):
            out_bit = 1 << edge_out
            if not selected & out_bit:
                continue
            if edge_out == E_INDEX or (color == 1 and edge_out == F_INDEX):
                continue
            reduced = selected ^ out_bit
            for edge_in in range(len(EDGES)):
                in_bit = 1 << edge_in
                if selected & in_bit or (color == 1 and edge_in == E_INDEX):
                    continue
                replacement = reduced | in_bit
                if replacement not in forest_set:
                    continue
                target = (
                    (replacement, base[1])
                    if color == 0
                    else (base[0], replacement)
                )
                if active_mask(target) != active_mask(source):
                    continue
                target_index = positive_index.get(target)
                if target_index is not None:
                    targets.setdefault(
                        target_index, (color, edge_out, edge_in)
                    )
    return targets


def adjacency_hash(adjacency: list[list[int]]) -> str:
    digest = hashlib.sha256()
    digest.update(b"amra.opg1757.csr-adjacency.v1\0")
    digest.update(struct.pack("<I", len(adjacency)))
    for row in adjacency:
        digest.update(struct.pack("<I", len(row)))
        for target in row:
            digest.update(struct.pack("<I", target))
    return digest.hexdigest()


def matching_hash(source_to_target: list[int]) -> str:
    digest = hashlib.sha256()
    digest.update(b"amra.opg1757.source-matching.v1\0")
    for source, target in enumerate(source_to_target):
        if target >= 0:
            digest.update(struct.pack("<II", source, target))
    return digest.hexdigest()


def find_augmenting_path(
    root: int,
    adjacency: list[list[int]],
    source_to_target: list[int],
    target_to_source: list[int],
) -> list[tuple[int, int]] | None:
    source_predecessor: dict[int, int | None] = {root: None}
    target_predecessor: dict[int, int] = {}
    queue = deque([root])
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
        return None
    path: list[tuple[int, int]] = []
    target = free_target
    while True:
        source = target_predecessor[target]
        path.append((source, target))
        preceding = source_predecessor[source]
        if preceding is None:
            break
        target = preceding
    path.reverse()
    return path


def augment_matching(
    adjacency: list[list[int]],
    target_count: int,
    initial: tuple[list[int], list[int]] | None = None,
    base_adjacency: list[list[int]] | None = None,
) -> tuple[list[int], list[int], dict[str, object]]:
    if initial is None:
        source_to_target = [-1] * len(adjacency)
        target_to_source = [-1] * target_count
        for source, row in enumerate(adjacency):
            for target in row:
                if target_to_source[target] < 0:
                    source_to_target[source] = target
                    target_to_source[target] = source
                    break
    else:
        source_to_target = initial[0].copy()
        target_to_source = initial[1].copy()

    path_lengths: Counter[int] = Counter()
    new_edges_per_path: Counter[int] = Counter()
    path_digest = hashlib.sha256()
    samples: list[list[list[int]]] = []
    while True:
        successful = 0
        roots = [
            source
            for source, target in enumerate(source_to_target)
            if target < 0
        ]
        for root in roots:
            if source_to_target[root] >= 0:
                continue
            path = find_augmenting_path(
                root, adjacency, source_to_target, target_to_source
            )
            if path is None:
                continue
            successful += 1
            path_lengths[len(path)] += 1
            new_count = 0
            for source, target in path:
                if (
                    base_adjacency is not None
                    and target not in base_adjacency[source]
                ):
                    new_count += 1
                path_digest.update(struct.pack("<II", source, target))
                source_to_target[source] = target
                target_to_source[target] = source
            new_edges_per_path[new_count] += 1
            if len(samples) < 12:
                samples.append([[source, target] for source, target in path])
        if successful == 0:
            break

    matched = [target for target in source_to_target if target >= 0]
    if len(set(matched)) != len(matched):
        raise AssertionError("independent augmenter produced a collision")
    if any(
        target not in adjacency[source]
        for source, target in enumerate(source_to_target)
        if target >= 0
    ):
        raise AssertionError("independent matching used a non-edge")
    return (
        source_to_target,
        target_to_source,
        {
            "matching_size": len(matched),
            "augmenting_path_count": sum(path_lengths.values()),
            "augmenting_path_length_histogram": {
                str(length): count
                for length, count in sorted(path_lengths.items())
            },
            "new_edges_per_path_histogram": {
                str(count): paths
                for count, paths in sorted(new_edges_per_path.items())
            },
            "augmenting_paths_sha256": path_digest.hexdigest(),
            "first_augmenting_paths": samples,
        },
    )


def alternating_hall_witness(
    adjacency: list[list[int]],
    source_to_target: list[int],
    target_to_source: list[int],
) -> tuple[set[int], set[int]]:
    sources = {
        source
        for source, target in enumerate(source_to_target)
        if target < 0
    }
    targets: set[int] = set()
    queue = deque(sorted(sources))
    while queue:
        source = queue.popleft()
        for target in adjacency[source]:
            if target in targets:
                continue
            targets.add(target)
            following = target_to_source[target]
            if following < 0:
                raise AssertionError("matching still has an augmenting path")
            if following not in sources:
                sources.add(following)
                queue.append(following)
    neighborhood = {
        target for source in sources for target in adjacency[source]
    }
    if neighborhood != targets:
        raise AssertionError("alternating Hall neighborhood is incomplete")
    return sources, targets


def build_graph(
    k: int,
    forests_by_size: dict[int, list[int]],
    forest_set: set[int],
) -> dict[str, object]:
    positives, negatives = enumerate_layer(forests_by_size, k)
    positive_index = {
        pair: index for index, pair in enumerate(positives)
    }
    base_adjacency: list[list[int]] = []
    expanded_adjacency: list[list[int]] = []
    reserve_maps: list[dict[int, tuple[int, int, int] | None]] = []
    for source in negatives:
        base = direct_single_targets(source, positive_index)
        reserves = reserve_targets(source, positive_index, forest_set)
        base_adjacency.append(sorted(base))
        expanded_adjacency.append(sorted(base | set(reserves)))
        reserve_maps.append(reserves)

    base_source, base_target, base_match = augment_matching(
        base_adjacency, len(positives)
    )
    base_hall_sources, base_hall_targets = alternating_hall_witness(
        base_adjacency, base_source, base_target
    )
    expanded_source, expanded_target, completion = augment_matching(
        expanded_adjacency,
        len(positives),
        initial=(base_source, base_target),
        base_adjacency=base_adjacency,
    )
    if len(negatives) != completion["matching_size"]:
        expanded_hall = alternating_hall_witness(
            expanded_adjacency, expanded_source, expanded_target
        )
        expanded_hall_counts = [
            len(expanded_hall[0]),
            len(expanded_hall[1]),
        ]
    else:
        expanded_hall_counts = [0, 0]
    return {
        "positives": positives,
        "negatives": negatives,
        "positive_index": positive_index,
        "base_adjacency": base_adjacency,
        "expanded_adjacency": expanded_adjacency,
        "reserve_maps": reserve_maps,
        "base_source_matching": base_source,
        "expanded_source_matching": expanded_source,
        "summary": {
            "k": k,
            "negative_count": len(negatives),
            "positive_count": len(positives),
            "direct_or_single_edge_count": sum(map(len, base_adjacency)),
            "direct_or_single_adjacency_sha256": adjacency_hash(
                base_adjacency
            ),
            "direct_or_single_matching_size": base_match["matching_size"],
            "direct_or_single_matching_sha256": matching_hash(base_source),
            "direct_or_single_hall_source_count": len(base_hall_sources),
            "direct_or_single_hall_target_count": len(base_hall_targets),
            "direct_or_single_deficiency": (
                len(negatives) - int(base_match["matching_size"])
            ),
            "expanded_edge_count": sum(map(len, expanded_adjacency)),
            "expanded_adjacency_sha256": adjacency_hash(
                expanded_adjacency
            ),
            "expanded_matching_size": completion["matching_size"],
            "expanded_matching_sha256": matching_hash(expanded_source),
            "expanded_deficiency": (
                len(negatives) - int(completion["matching_size"])
            ),
            "expanded_hall_source_count": expanded_hall_counts[0],
            "expanded_hall_target_count": expanded_hall_counts[1],
            "base_to_expanded_completion": completion,
        },
    }


def audit_saved_k5(
    graph: dict[str, object], saved_path: Path, forest_set: set[int]
) -> dict[str, object]:
    saved_bytes = saved_path.read_bytes()
    saved = json.loads(saved_bytes)
    payload = {
        key: saved[key] for key in ("scope", "layer", "hall_kernel")
    }
    recomputed_payload_hash = hashlib.sha256(
        json.dumps(
            payload, separators=(",", ":"), sort_keys=True
        ).encode()
    ).hexdigest()
    if recomputed_payload_hash != saved["sha256_payload"]:
        raise AssertionError("saved k=5 payload hash is invalid")
    required_claims = {
        "protected_basis_exchange_forest_preservation": "human_proof",
        "two_stage_tagged_reversibility": "human_proof",
        "q2_k5_expanded_untagged_injection": "finite_evidence",
        "all_q_all_k_untagged_injection": "open_gap",
        "full_first_coefficient_positivity": "open_gap",
    }
    if any(
        saved["claim_labels"].get(claim) != status
        for claim, status in required_claims.items()
    ):
        raise AssertionError("saved k=5 claim boundary changed")

    positives = graph["positives"]
    negatives = graph["negatives"]
    positive_index = graph["positive_index"]
    base_adjacency = graph["base_adjacency"]
    reserve_maps = graph["reserve_maps"]
    negative_index = {
        pair: index for index, pair in enumerate(negatives)
    }
    kernel = saved["hall_kernel"]
    saved_sources = {
        row["index"]: row_pair(row)
        for row in kernel["source_rows"]
    }
    saved_targets = {
        row["index"]: row_pair(row)
        for row in kernel["target_rows"]
    }

    for row in kernel["source_rows"]:
        pair = row_pair(row)
        source = negative_index[pair]
        actual_targets = {
            positives[target] for target in base_adjacency[source]
        }
        expected_targets = {
            saved_targets[target]
            for target in row["direct_or_single_neighbor_indices"]
        }
        if actual_targets != expected_targets:
            raise AssertionError("saved kernel adjacency is incomplete")

    collision_sizes: list[list[int]] = []
    for bucket in kernel["collision_buckets"]:
        target_pair = saved_targets[bucket["target_index"]]
        source_pairs = [
            saved_sources[index] for index in bucket["source_indices"]
        ]
        if len(source_pairs) != 2:
            raise AssertionError("collision bucket is not 2-to-1")
        for pair in source_pairs:
            source = negative_index[pair]
            if {
                positives[target] for target in base_adjacency[source]
            } != {target_pair}:
                raise AssertionError("collision bucket has a hidden edge")
        collision_sizes.append([len(source_pairs), 1])

    same_union_rows: list[list[int]] = []
    for block in kernel["same_union_blocks"]:
        block_sources = [
            saved_sources[index] for index in block["source_indices"]
        ]
        union = block_sources[0][0] | block_sources[0][1]
        if any((red | blue) != union for red, blue in block_sources):
            raise AssertionError("saved same-union source block is mixed")
        same_union_targets = [
            pair for pair in positives if pair[0] | pair[1] == union
        ]
        if len(same_union_targets) != block["all_same_union_target_count"]:
            raise AssertionError("same-union target exhaustion changed")
        same_union_rows.append(
            [
                len(block_sources),
                len(same_union_targets),
                max(0, len(block_sources) - len(same_union_targets)),
            ]
        )

    reserve_targets_seen: set[tuple[int, int]] = set()
    for row in kernel["reserve_matching"]:
        source_pair = saved_sources[row["source_index"]]
        source = negative_index[source_pair]
        reserve_row = row["reserve"]
        if reserve_row is None:
            reserve = None
        else:
            reserve = (
                0 if reserve_row["color"] == "red" else 1,
                EDGE_INDEX[tuple(reserve_row["edge_out"])],
                EDGE_INDEX[tuple(reserve_row["edge_in"])],
            )
        target_pair = row_pair(row["target"])
        target = positive_index[target_pair]
        if reserve_maps[source].get(target) != reserve:
            raise AssertionError("saved reserve move is not generated")
        base, opening_tag = cycle_open(source_pair, forest_set)
        expected_opening = row["opening_tag"]
        expected_opening_index = (
            None
            if expected_opening is None
            else EDGE_INDEX[tuple(expected_opening)]
        )
        if opening_tag != expected_opening_index:
            raise AssertionError("saved opening tag changed")
        if reserve is None:
            rebuilt_target = base
        else:
            color, edge_out, edge_in = reserve
            selected = base[color]
            replacement = (
                selected ^ (1 << edge_out)
            ) | (1 << edge_in)
            rebuilt_target = (
                (replacement, base[1])
                if color == 0
                else (base[0], replacement)
            )
        if rebuilt_target != target_pair:
            raise AssertionError("saved reserve target does not replay")
        if reserve is not None:
            color, edge_out, edge_in = reserve
            selected = rebuilt_target[color]
            restored = (
                selected ^ (1 << edge_in)
            ) | (1 << edge_out)
            rebuilt_base = (
                (restored, rebuilt_target[1])
                if color == 0
                else (rebuilt_target[0], restored)
            )
        else:
            rebuilt_base = rebuilt_target
        if rebuilt_base != base:
            raise AssertionError("independent reserve inverse failed")
        if opening_tag is None:
            rebuilt_source = (
                rebuilt_base[0] ^ E_BIT,
                rebuilt_base[1] | E_BIT,
            )
        else:
            opening_bit = 1 << opening_tag
            rebuilt_source = (
                (rebuilt_base[0] ^ E_BIT) | opening_bit,
                (rebuilt_base[1] ^ opening_bit) | E_BIT,
            )
        if rebuilt_source != source_pair:
            raise AssertionError("independent opening inverse failed")
        reserve_targets_seen.add(target_pair)
    if len(reserve_targets_seen) != len(kernel["reserve_matching"]):
        raise AssertionError("saved reserve matching has a collision")

    summary = graph["summary"]
    if (
        summary["negative_count"],
        summary["positive_count"],
        summary["direct_or_single_edge_count"],
        summary["direct_or_single_matching_size"],
        summary["expanded_edge_count"],
        summary["expanded_matching_size"],
    ) != (
        saved["layer"]["negative_count"],
        saved["layer"]["positive_count"],
        saved["layer"]["direct_or_single_edge_count"],
        saved["layer"]["direct_or_single_matching_size"],
        saved["layer"]["expanded_edge_count"],
        saved["layer"]["expanded_matching_size"],
    ):
        raise AssertionError("independent k=5 reconstruction disagrees")
    return {
        "saved_schema": saved["schema"],
        "saved_payload_sha256": saved["sha256_payload"],
        "recomputed_payload_sha256": recomputed_payload_hash,
        "saved_file_sha256": hashlib.sha256(saved_bytes).hexdigest(),
        "audited_claim_labels": required_claims,
        "hash_scope": (
            "sha256_payload authenticates scope, layer, and hall_kernel; "
            "it does not include schema, claim_labels, or the hash field."
        ),
        "independent_layer_summary": summary,
        "collision_component_sizes": collision_sizes,
        "same_union_source_target_deficiency_rows": same_union_rows,
        "reserve_matching_target_count": len(reserve_targets_seen),
        "human_proof_audit": {
            "forest_preservation": "valid",
            "colored_copy_count_preservation": "valid",
            "union_symmetric_difference_subset_of_two_edges": "valid",
            "tagged_inverse": "valid",
            "untagged_all_parameter_injection": "not_proved",
        },
        "precision_notes": [
            (
                "The canonical 12-to-6 witness is not inclusion-minimal; "
                "it is the union of six inclusion-minimal 2-to-1 components."
            ),
            (
                "The stored payload hash is not a hash of the complete JSON "
                "certificate."
            ),
            (
                "Full candidate adjacency and the 43648-entry matching are "
                "reconstructible but not serialized in the old certificate."
            ),
        ],
    }


def certificate(payload: dict[str, object], schema: str, claims: dict) -> dict:
    return {
        "schema": schema,
        "claim_labels": claims,
        **payload,
        "sha256_payload": hashlib.sha256(
            json.dumps(
                payload, separators=(",", ":"), sort_keys=True
            ).encode()
        ).hexdigest(),
    }


def build_audits() -> tuple[dict[str, object], dict[str, object]]:
    forests_by_size, forest_set = all_forests_by_size()
    k5_graph = build_graph(5, forests_by_size, forest_set)
    source_certificate = Path(__file__).with_name(
        "multiedge_recoloring_attack_certificate.json"
    )
    independent_payload = {
        "scope": (
            "Independent bit-mask reconstruction of the complete q=2,k=5 "
            "candidate graph and audit of the saved multiedge certificate."
        ),
        "forest_count": len(forest_set),
        "audit": audit_saved_k5(
            k5_graph, source_certificate, forest_set
        ),
    }
    independent = certificate(
        independent_payload,
        "amra.opg1757.independent_multiedge_audit.v1",
        {
            "k5_definition_and_counts": "independently_reproduced",
            "k5_expanded_perfect_matching": "finite_evidence",
            "protected_basis_exchange": "human_proof_audited",
            "all_q_all_k_injection": "open_gap",
        },
    )
    del k5_graph

    k6_graph = build_graph(6, forests_by_size, forest_set)
    k6_payload = {
        "scope": (
            "Complete q=2,k=6 enumeration on K6 using every valid direct/"
            "single E-exchange and every protected one-basis reserve after "
            "deterministic global cycle opening."
        ),
        "candidate_move_family": {
            "base": "all valid direct and single E<->x exchanges",
            "reserve": (
                "one protected forest basis exchange after deterministic "
                "global cycle opening, with active vertex set preserved"
            ),
        },
        "layer": k6_graph["summary"],
    }
    k6 = certificate(
        k6_payload,
        "amra.opg1757.q2_k6_extension.v1",
        {
            "q2_k6_candidate_graph_completeness": "finite_exhaustion",
            "q2_k6_expanded_untagged_injection": "finite_evidence",
            "protected_basis_exchange": "human_proof",
            "all_q_all_k_injection": "open_gap",
            "full_first_coefficient_positivity": "open_gap",
        },
    )
    return independent, k6


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--independent-output",
        type=Path,
        default=Path(__file__).with_name(
            "independent_multiedge_audit_certificate.json"
        ),
    )
    parser.add_argument(
        "--k6-output",
        type=Path,
        default=Path(__file__).with_name(
            "q2_k6_extension_certificate.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    independent, k6 = build_audits()
    args.independent_output.write_text(
        json.dumps(independent, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.k6_output.write_text(
        json.dumps(k6, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.independent_output)
    print(f"INDEPENDENT|sha256={independent['sha256_payload']}")
    print(args.k6_output)
    print(f"K6|sha256={k6['sha256_payload']}")


if __name__ == "__main__":
    main()
