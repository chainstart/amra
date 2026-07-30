#!/usr/bin/env python3
"""Compact-CSR finite audit of the q=2,k=7 reserve-expanded graph."""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import struct
from array import array
from collections import Counter, deque
from pathlib import Path

from independent_verify_multiedge_and_k6 import (
    all_forests_by_size,
    direct_single_targets,
    enumerate_layer,
    matching_hash,
    reserve_targets,
)


K = 7


class CompactCSR:
    """Unsigned 32-bit targets with unsigned 64-bit row offsets."""

    def __init__(self) -> None:
        self.offsets = array("Q", [0])
        self.targets = array("I")

    def append(self, row: list[int]) -> None:
        self.targets.extend(row)
        self.offsets.append(len(self.targets))

    def row_bounds(self, source: int) -> tuple[int, int]:
        return self.offsets[source], self.offsets[source + 1]

    def contains(self, source: int, target: int) -> bool:
        left, right = self.row_bounds(source)
        return (
            bisect.bisect_left(self.targets, target, left, right) < right
            and self.targets[
                bisect.bisect_left(self.targets, target, left, right)
            ]
            == target
        )

    @property
    def source_count(self) -> int:
        return len(self.offsets) - 1

    @property
    def edge_count(self) -> int:
        return len(self.targets)

    @property
    def storage_bytes(self) -> int:
        return (
            len(self.offsets) * self.offsets.itemsize
            + len(self.targets) * self.targets.itemsize
        )


def compact_adjacency_hash(adjacency: CompactCSR) -> str:
    digest = hashlib.sha256()
    digest.update(b"amra.opg1757.csr-adjacency.v1\0")
    digest.update(struct.pack("<I", adjacency.source_count))
    for source in range(adjacency.source_count):
        left, right = adjacency.row_bounds(source)
        digest.update(struct.pack("<I", right - left))
        for index in range(left, right):
            digest.update(struct.pack("<I", adjacency.targets[index]))
    return digest.hexdigest()


def degree_profile(
    adjacency: CompactCSR, target_count: int
) -> dict[str, int]:
    left_degrees = [
        adjacency.offsets[source + 1] - adjacency.offsets[source]
        for source in range(adjacency.source_count)
    ]
    right_degrees = array("I", [0]) * target_count
    for target in adjacency.targets:
        right_degrees[target] += 1
    return {
        "minimum_left_degree": min(left_degrees, default=0),
        "maximum_left_degree": max(left_degrees, default=0),
        "minimum_right_degree": min(right_degrees, default=0),
        "maximum_right_degree": max(right_degrees, default=0),
        "zero_right_degree_count": sum(
            degree == 0 for degree in right_degrees
        ),
    }


def find_path(
    root: int,
    adjacency: CompactCSR,
    source_to_target: list[int],
    target_to_source: list[int],
) -> list[tuple[int, int]] | None:
    source_predecessor: dict[int, int | None] = {root: None}
    target_predecessor: dict[int, int] = {}
    queue = deque([root])
    free_target: int | None = None
    while queue and free_target is None:
        source = queue.popleft()
        left, right = adjacency.row_bounds(source)
        for index in range(left, right):
            target = adjacency.targets[index]
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


def augment(
    adjacency: CompactCSR,
    target_count: int,
    initial: tuple[list[int], list[int]] | None = None,
    base: CompactCSR | None = None,
) -> tuple[list[int], list[int], dict[str, object]]:
    if initial is None:
        source_to_target = [-1] * adjacency.source_count
        target_to_source = [-1] * target_count
        for source in range(adjacency.source_count):
            left, right = adjacency.row_bounds(source)
            for index in range(left, right):
                target = adjacency.targets[index]
                if target_to_source[target] < 0:
                    source_to_target[source] = target
                    target_to_source[target] = source
                    break
    else:
        source_to_target = initial[0].copy()
        target_to_source = initial[1].copy()

    length_counts: Counter[int] = Counter()
    new_edge_counts: Counter[int] = Counter()
    path_digest = hashlib.sha256()
    samples: list[list[list[int]]] = []
    while True:
        successes = 0
        roots = [
            source
            for source, target in enumerate(source_to_target)
            if target < 0
        ]
        for root in roots:
            if source_to_target[root] >= 0:
                continue
            path = find_path(
                root, adjacency, source_to_target, target_to_source
            )
            if path is None:
                continue
            successes += 1
            length_counts[len(path)] += 1
            new_count = 0
            for source, target in path:
                if base is not None and not base.contains(source, target):
                    new_count += 1
                path_digest.update(struct.pack("<II", source, target))
                source_to_target[source] = target
                target_to_source[target] = source
            new_edge_counts[new_count] += 1
            if len(samples) < 12:
                samples.append([[source, target] for source, target in path])
        if successes == 0:
            break

    matched = [target for target in source_to_target if target >= 0]
    if len(set(matched)) != len(matched):
        raise AssertionError("compact matcher produced target collision")
    if any(
        not adjacency.contains(source, target)
        for source, target in enumerate(source_to_target)
        if target >= 0
    ):
        raise AssertionError("compact matcher used a non-edge")
    return (
        source_to_target,
        target_to_source,
        {
            "matching_size": len(matched),
            "augmenting_path_count": sum(length_counts.values()),
            "augmenting_path_length_histogram": {
                str(length): count
                for length, count in sorted(length_counts.items())
            },
            "new_edges_per_path_histogram": {
                str(count): paths
                for count, paths in sorted(new_edge_counts.items())
            },
            "augmenting_paths_sha256": path_digest.hexdigest(),
            "first_augmenting_paths": samples,
        },
    )


def hall_witness(
    adjacency: CompactCSR,
    source_to_target: list[int],
    target_to_source: list[int],
) -> tuple[int, int]:
    sources = {
        source
        for source, target in enumerate(source_to_target)
        if target < 0
    }
    targets: set[int] = set()
    queue = deque(sorted(sources))
    while queue:
        source = queue.popleft()
        left, right = adjacency.row_bounds(source)
        for index in range(left, right):
            target = adjacency.targets[index]
            if target in targets:
                continue
            targets.add(target)
            following = target_to_source[target]
            if following < 0:
                raise AssertionError("compact matching is not maximum")
            if following not in sources:
                sources.add(following)
                queue.append(following)
    neighborhood: set[int] = set()
    for source in sources:
        left, right = adjacency.row_bounds(source)
        neighborhood.update(adjacency.targets[left:right])
    if neighborhood != targets:
        raise AssertionError("compact Hall neighborhood is incomplete")
    return len(sources), len(targets)


def build_audit() -> dict[str, object]:
    forests_by_size, forest_set = all_forests_by_size()
    positives, negatives = enumerate_layer(forests_by_size, K)
    positive_index = {
        pair: index for index, pair in enumerate(positives)
    }
    base = CompactCSR()
    expanded = CompactCSR()
    for source in negatives:
        base_targets = direct_single_targets(source, positive_index)
        reserves = reserve_targets(source, positive_index, forest_set)
        base.append(sorted(base_targets))
        expanded.append(sorted(base_targets | set(reserves)))

    base_source, base_target, base_match = augment(
        base, len(positives)
    )
    hall_sources, hall_targets = hall_witness(
        base, base_source, base_target
    )
    expanded_source, expanded_target, completion = augment(
        expanded,
        len(positives),
        initial=(base_source, base_target),
        base=base,
    )
    if completion["matching_size"] != len(negatives):
        expanded_hall = hall_witness(
            expanded, expanded_source, expanded_target
        )
    else:
        expanded_hall = (0, 0)

    payload = {
        "scope": (
            "Complete q=2,k=7 K6 candidate graph stored in compact CSR. "
            "Edges are every valid direct/single E exchange plus every "
            "protected one-basis reserve after deterministic opening."
        ),
        "layer": {
            "k": K,
            "negative_count": len(negatives),
            "positive_count": len(positives),
            "direct_or_single_edge_count": base.edge_count,
            "direct_or_single_adjacency_sha256": (
                compact_adjacency_hash(base)
            ),
            "direct_or_single_matching_size": (
                base_match["matching_size"]
            ),
            "direct_or_single_matching_sha256": matching_hash(
                base_source
            ),
            "direct_or_single_degree_profile": degree_profile(
                base, len(positives)
            ),
            "direct_or_single_deficiency": (
                len(negatives) - int(base_match["matching_size"])
            ),
            "direct_or_single_hall_source_count": hall_sources,
            "direct_or_single_hall_target_count": hall_targets,
            "expanded_edge_count": expanded.edge_count,
            "expanded_adjacency_sha256": (
                compact_adjacency_hash(expanded)
            ),
            "expanded_matching_size": completion["matching_size"],
            "expanded_matching_sha256": matching_hash(expanded_source),
            "expanded_degree_profile": degree_profile(
                expanded, len(positives)
            ),
            "expanded_deficiency": (
                len(negatives) - int(completion["matching_size"])
            ),
            "expanded_hall_source_count": expanded_hall[0],
            "expanded_hall_target_count": expanded_hall[1],
            "base_to_expanded_completion": completion,
        },
        "resource_accounting": {
            "representation": (
                "uint64 row offsets plus uint32 target indices"
            ),
            "base_csr_bytes": base.storage_bytes,
            "expanded_csr_bytes": expanded.storage_bytes,
            "combined_csr_bytes": (
                base.storage_bytes + expanded.storage_bytes
            ),
            "python_list_adjacency_not_materialized": True,
        },
    }
    return {
        "schema": "amra.opg1757.q2_k7_extension.v1",
        "claim_labels": {
            "q2_k7_candidate_graph_completeness": "finite_exhaustion",
            "q2_k7_expanded_untagged_injection": "finite_evidence",
            "protected_basis_exchange": "human_proof",
            "q2_uniform_hall_theorem": "open_gap",
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
            "q2_k7_extension_certificate.json"
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
