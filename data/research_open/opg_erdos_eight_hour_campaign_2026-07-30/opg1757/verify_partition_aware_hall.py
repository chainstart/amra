#!/usr/bin/env python3
"""Audit partition-aware forest replacement and the first q=2 Hall core."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


Partition = tuple[int, ...]


def set_partitions(size: int) -> tuple[Partition, ...]:
    """Return restricted-growth encodings of all partitions of [size]."""

    if size == 0:
        return ((),)
    rows: list[Partition] = []

    def extend(prefix: tuple[int, ...], maximum: int) -> None:
        if len(prefix) == size:
            rows.append(prefix)
            return
        for label in range(maximum + 2):
            extend(prefix + (label,), max(maximum, label))

    extend((0,), 0)
    return tuple(rows)


def canonicalize(labels: tuple[object, ...]) -> Partition:
    relabel: dict[object, int] = {}
    return tuple(
        relabel.setdefault(label, len(relabel))
        for label in labels
    )


def refines(fine: Partition, coarse: Partition) -> bool:
    """Whether every fine block lies inside one coarse block."""

    return all(
        fine[left] != fine[right] or coarse[left] == coarse[right]
        for left in range(len(fine))
        for right in range(left)
    )


def common_refinement(left: Partition, right: Partition) -> Partition:
    return canonicalize(tuple(zip(left, right)))


def blocks(partition: Partition) -> list[list[int]]:
    return [
        [
            vertex
            for vertex, block in enumerate(partition)
            if block == label
        ]
        for label in range(max(partition, default=-1) + 1)
    ]


def incidence_components(
    local: Partition, external: Partition
) -> tuple[bool, tuple[int, ...], tuple[int, ...]]:
    """Acyclicity and component labels in the bipartite incidence multigraph."""

    local_count = max(local, default=-1) + 1
    external_count = max(external, default=-1) + 1
    parent = list(range(local_count + external_count))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    acyclic = True
    for vertex in range(len(local)):
        left = root(local[vertex])
        right = root(local_count + external[vertex])
        if left == right:
            acyclic = False
            break
        parent[left] = right
    return (
        acyclic,
        tuple(root(label) for label in range(local_count)),
        tuple(
            root(local_count + label)
            for label in range(external_count)
        ),
    )


def incidence_forest(local: Partition, external: Partition) -> bool:
    return incidence_components(local, external)[0]


def safe_coarsening_by_quotient(
    source: Partition,
    target: Partition,
    external: Partition,
) -> bool:
    """Exact quotient test when target is a coarsening of source."""

    if not refines(source, target):
        raise ValueError("target is not a coarsening of source")
    source_safe, source_components, _ = incidence_components(
        source, external
    )
    if not source_safe:
        raise ValueError("source and external partitions are incompatible")
    source_block_count = max(source, default=-1) + 1
    component_labels = canonicalize(source_components)
    component_count = max(component_labels, default=-1) + 1
    target_block_count = max(target, default=-1) + 1

    # Contract every tree component of I(source, external).  Each source
    # block then gives one edge from its old tree component to the target
    # block into which it is identified.  The quotient is acyclic exactly
    # when this second component-incidence multigraph is acyclic.  Checking
    # each target block separately is not enough: two simultaneous merges
    # can join the same pair of old components twice and create a cycle.
    parent = list(range(component_count + target_block_count))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for source_block in range(source_block_count):
        representative = next(
            vertex
            for vertex in range(len(source))
            if source[vertex] == source_block
        )
        left = root(component_labels[source_block])
        right = root(component_count + target[representative])
        if left == right:
            return False
        parent[left] = right
    return True


def safe_by_split_then_merge(
    source: Partition,
    target: Partition,
    external: Partition,
) -> bool:
    """Normalize an arbitrary replacement to a safe split then a quotient."""

    if not incidence_forest(source, external):
        raise ValueError("source and external partitions are incompatible")
    split = common_refinement(source, target)
    if not refines(split, target):
        raise AssertionError("common refinement did not refine target")
    return safe_coarsening_by_quotient(split, target, external)


def relation(source: Partition, target: Partition) -> str:
    target_refines = refines(target, source)
    source_refines = refines(source, target)
    if target_refines and source_refines:
        return "equal"
    if target_refines:
        return "target_splits_source"
    if source_refines:
        return "target_merges_source"
    return "mixed_split_merge"


def first_merge_witness(
    source: Partition, target: Partition
) -> list[int] | None:
    for left in range(len(source)):
        for right in range(left):
            if (
                target[left] == target[right]
                and source[left] != source[right]
            ):
                return [right, left]
    return None


def partition_audit(max_boundary: int = 6) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for size in range(1, max_boundary + 1):
        partitions = set_partitions(size)
        compatible = [
            [
                incidence_forest(local, external)
                for external in partitions
            ]
            for local in partitions
        ]
        admissible_by_external = [
            sum(compatible[local][external] for local in range(len(partitions)))
            for external in range(len(partitions))
        ]
        context_safe_transitions = sum(
            count * count for count in admissible_by_external
        )
        nonuniversal_context_transitions = 0
        split_merge_checks = 0
        for source_index, source in enumerate(partitions):
            for target_index, target in enumerate(partitions):
                observed_universal = all(
                    not compatible[source_index][external_index]
                    or compatible[target_index][external_index]
                    for external_index in range(len(partitions))
                )
                predicted_universal = refines(target, source)
                if observed_universal != predicted_universal:
                    raise AssertionError(
                        "universal refinement criterion failed: "
                        f"size={size}, source={source}, target={target}"
                    )
                if predicted_universal:
                    continue
                nonuniversal_context_transitions += sum(
                    compatible[source_index][external_index]
                    and compatible[target_index][external_index]
                    for external_index in range(len(partitions))
                )
        for external_index, external in enumerate(partitions):
            for source_index, source in enumerate(partitions):
                if not compatible[source_index][external_index]:
                    continue
                for target_index, target in enumerate(partitions):
                    predicted = compatible[target_index][external_index]
                    normalized = safe_by_split_then_merge(
                        source, target, external
                    )
                    if predicted != normalized:
                        raise AssertionError(
                            "split-then-merge criterion failed: "
                            f"size={size}, source={source}, "
                            f"target={target}, external={external}"
                        )
                    split_merge_checks += 1
        rows.append(
            {
                "boundary_size": size,
                "partition_count": len(partitions),
                "compatible_local_external_pairs": sum(
                    map(sum, compatible)
                ),
                "universally_safe_ordered_partition_replacements": sum(
                    refines(target, source)
                    for source in partitions
                    for target in partitions
                ),
                "context_safe_ordered_replacements": (
                    context_safe_transitions
                ),
                "context_safe_but_not_universal_triples": (
                    nonuniversal_context_transitions
                ),
                "split_then_merge_checks": split_merge_checks,
            }
        )
    return rows


def forest_partition(
    vertex_count: int, edges: frozenset[tuple[int, int]]
) -> Partition:
    parent = list(range(vertex_count))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        parent[root(left)] = root(right)
    return canonicalize(tuple(root(vertex) for vertex in range(vertex_count)))


def q2_k3_hall_partition_audit() -> dict[str, object]:
    """Rebuild the old minimal Hall core, then add partition-context data."""

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
    forests_by_size: dict[int, list[frozenset[tuple[int, int]]]] = {}
    for forest in forests:
        forests_by_size.setdefault(len(forest), []).append(forest)
    old_partitions = {
        forest: old.component_partition(old.Q2_VERTEX_COUNT, forest)
        for forest in forests
    }
    positives, negatives = old.enumerate_q2_layer(forests_by_size, 3)
    three, four, _, _, _ = old.build_q2_adjacencies(
        positives,
        negatives,
        old_partitions,
        include_full=False,
        include_handoff=False,
    )
    source_matching, target_matching, matching_size = old.hopcroft_karp(
        three, len(positives)
    )
    hall_sources, hall_targets = old.hall_witness(
        three, source_matching, target_matching
    )
    escapes = [
        (source, target)
        for source in sorted(hall_sources)
        for target in four[source]
        if target not in set(three[source])
        and target not in hall_targets
    ]
    external_partitions = set_partitions(old.Q2_VERTEX_COUNT)

    def pair_is_safe(
        pair: tuple[
            frozenset[tuple[int, int]],
            frozenset[tuple[int, int]],
        ],
        red_external: Partition,
        blue_external: Partition,
    ) -> bool:
        return (
            incidence_forest(
                forest_partition(old.Q2_VERTEX_COUNT, pair[0]),
                red_external,
            )
            and incidence_forest(
                forest_partition(old.Q2_VERTEX_COUNT, pair[1]),
                blue_external,
            )
        )

    def small_matching_size(adjacency: list[list[int]]) -> int:
        target_to_source: dict[int, int] = {}

        def augment(source: int, seen: set[int]) -> bool:
            for target in adjacency[source]:
                if target in seen:
                    continue
                seen.add(target)
                following = target_to_source.get(target)
                if following is None or augment(following, seen):
                    target_to_source[target] = source
                    return True
            return False

        size = 0
        for source in range(len(adjacency)):
            size += int(augment(source, set()))
        return size

    transition_rows: list[dict[str, object]] = []
    colored_context_counts: Counter[
        tuple[str, str, int, int]
    ] = Counter()
    for source_index, target_index in escapes:
        source = negatives[source_index]
        target = positives[target_index]
        source_red = forest_partition(old.Q2_VERTEX_COUNT, source[0])
        source_blue = forest_partition(old.Q2_VERTEX_COUNT, source[1])
        target_red = forest_partition(old.Q2_VERTEX_COUNT, target[0])
        target_blue = forest_partition(old.Q2_VERTEX_COUNT, target[1])
        red_source_contexts = sum(
            incidence_forest(source_red, external)
            for external in external_partitions
        )
        blue_source_contexts = sum(
            incidence_forest(source_blue, external)
            for external in external_partitions
        )
        red_joint_contexts = sum(
            incidence_forest(source_red, external)
            and incidence_forest(target_red, external)
            for external in external_partitions
        )
        blue_joint_contexts = sum(
            incidence_forest(source_blue, external)
            and incidence_forest(target_blue, external)
            for external in external_partitions
        )
        red_relation = relation(source_red, target_red)
        blue_relation = relation(source_blue, target_blue)
        colored_context_counts[
            (
                red_relation,
                blue_relation,
                red_joint_contexts,
                blue_joint_contexts,
            )
        ] += 1
        transition_rows.append(
            {
                "source_index": source_index,
                "target_index": target_index,
                "source_red_partition": blocks(source_red),
                "target_red_partition": blocks(target_red),
                "red_relation": red_relation,
                "source_blue_partition": blocks(source_blue),
                "target_blue_partition": blocks(target_blue),
                "blue_relation": blue_relation,
                "red_source_external_partition_count": red_source_contexts,
                "red_joint_safe_external_partition_count": red_joint_contexts,
                "blue_source_external_partition_count": blue_source_contexts,
                "blue_joint_safe_external_partition_count": (
                    blue_joint_contexts
                ),
                "colored_source_context_count": (
                    red_source_contexts * blue_source_contexts
                ),
                "colored_joint_safe_context_count": (
                    red_joint_contexts * blue_joint_contexts
                ),
                "red_universal_merge_witness": first_merge_witness(
                    source_red, target_red
                ),
                "blue_universal_merge_witness": first_merge_witness(
                    source_blue, target_blue
                ),
            }
        )
    kernel_context_counts: Counter[str] = Counter()
    max_three_deficiency = 0
    max_four_deficiency = 0
    first_four_rule_context_witness: dict[str, object] | None = None
    for red_external in external_partitions:
        for blue_external in external_partitions:
            active_sources = [
                source
                for source in sorted(hall_sources)
                if pair_is_safe(
                    negatives[source], red_external, blue_external
                )
            ]
            if active_sources:
                kernel_context_counts["nonempty_source_subset"] += 1
            three_rows: list[list[int]] = []
            four_rows: list[list[int]] = []
            for source in active_sources:
                three_rows.append(
                    [
                        target
                        for target in three[source]
                        if pair_is_safe(
                            positives[target],
                            red_external,
                            blue_external,
                        )
                    ]
                )
                four_rows.append(
                    [
                        target
                        for target in four[source]
                        if pair_is_safe(
                            positives[target],
                            red_external,
                            blue_external,
                        )
                    ]
                )
            three_deficiency = len(active_sources) - small_matching_size(
                three_rows
            )
            four_deficiency = len(active_sources) - small_matching_size(
                four_rows
            )
            max_three_deficiency = max(
                max_three_deficiency, three_deficiency
            )
            max_four_deficiency = max(
                max_four_deficiency, four_deficiency
            )
            if three_deficiency:
                kernel_context_counts["three_rule_deficient"] += 1
                if not four_deficiency:
                    kernel_context_counts[
                        "four_rule_closes_three_deficit"
                    ] += 1
            if four_deficiency:
                kernel_context_counts["four_rule_deficient"] += 1
                if first_four_rule_context_witness is None:
                    hall_candidates: list[
                        tuple[int, int, tuple[int, ...], tuple[int, ...]]
                    ] = []
                    for mask in range(1, 1 << len(active_sources)):
                        local_sources = tuple(
                            index
                            for index in range(len(active_sources))
                            if mask & (1 << index)
                        )
                        neighbors = tuple(
                            sorted(
                                {
                                    target
                                    for index in local_sources
                                    for target in four_rows[index]
                                }
                            )
                        )
                        deficiency = len(local_sources) - len(neighbors)
                        if deficiency > 0:
                            hall_candidates.append(
                                (
                                    -deficiency,
                                    len(local_sources),
                                    local_sources,
                                    neighbors,
                                )
                            )
                    if not hall_candidates:
                        raise AssertionError(
                            "matching deficit had no Hall subset"
                        )
                    _, _, local_sources, neighbors = min(hall_candidates)
                    witness_sources = tuple(
                        active_sources[index] for index in local_sources
                    )
                    compatible_positive_indices = [
                        index
                        for index, pair in enumerate(positives)
                        if pair_is_safe(
                            pair, red_external, blue_external
                        )
                    ]
                    compatible_negative_indices = [
                        index
                        for index, pair in enumerate(negatives)
                        if pair_is_safe(
                            pair, red_external, blue_external
                        )
                    ]
                    first_four_rule_context_witness = {
                        "red_external_partition": blocks(red_external),
                        "blue_external_partition": blocks(blue_external),
                        "source_indices": list(witness_sources),
                        "source_rows": [
                            {
                                "index": source,
                                **old.pair_row(negatives[source]),
                                "unrestricted_four_rule_neighbor_indices": (
                                    four[source]
                                ),
                            }
                            for source in witness_sources
                        ],
                        "available_neighbor_indices": list(neighbors),
                        "all_compatible_positive_count": len(
                            compatible_positive_indices
                        ),
                        "all_compatible_negative_count": len(
                            compatible_negative_indices
                        ),
                        "source_count": len(witness_sources),
                        "neighbor_count": len(neighbors),
                        "deficiency": (
                            len(witness_sources) - len(neighbors)
                        ),
                    }
    return {
        "scope": (
            "Exact finite reconstruction of the q=2,k=3 Hall core in the "
            "old three-rule graph; external contexts are all 203 set "
            "partitions of the six current vertices, independently by color."
        ),
        "negative_count": len(negatives),
        "positive_count": len(positives),
        "three_rule_matching_size": matching_size,
        "hall_source_count": len(hall_sources),
        "hall_target_count": len(hall_targets),
        "hall_deficiency": len(hall_sources) - len(hall_targets),
        "active_active_escape_count": len(escapes),
        "escape_partition_profile_rows": [
            {
                "multiplicity": multiplicity,
                "red_relation": key[0],
                "blue_relation": key[1],
                "red_joint_safe_external_partition_count": key[2],
                "blue_joint_safe_external_partition_count": key[3],
            }
            for key, multiplicity in sorted(
                colored_context_counts.items()
            )
        ],
        "escape_rows": transition_rows,
        "partition_restricted_hall_kernel": {
            "colored_external_partition_context_count": (
                len(external_partitions) ** 2
            ),
            "contexts_with_nonempty_hall_source_subset": (
                kernel_context_counts["nonempty_source_subset"]
            ),
            "three_rule_deficient_context_count": (
                kernel_context_counts["three_rule_deficient"]
            ),
            "four_rule_closes_three_deficit_context_count": (
                kernel_context_counts["four_rule_closes_three_deficit"]
            ),
            "four_rule_deficient_context_count": (
                kernel_context_counts["four_rule_deficient"]
            ),
            "maximum_three_rule_deficiency": max_three_deficiency,
            "maximum_four_rule_deficiency": max_four_deficiency,
            "first_four_rule_context_hall_witness": (
                first_four_rule_context_witness
            ),
            "scope": (
                "Finite matching on every context-restricted subset of the "
                "old 8-source Hall kernel, using all of each source's "
                "three/four-rule neighbors. A displayed deficit is therefore "
                "a Hall witness against the full context-restricted graph; "
                "absence of a deficit in this kernel does not certify the "
                "full graph."
            ),
        },
        "conclusion": (
            "Every active-active escape in this minimal finite Hall core "
            "is unsafe in some future context, but remains safe in a "
            "nonempty explicitly enumerable set of partition contexts. "
            "Thus an inductive rule must carry the external partition "
            "state; the unconditioned fourth orbit cannot be the induction."
        ),
    }


def build_audit() -> dict[str, object]:
    partition_rows = partition_audit()
    hall_row = q2_k3_hall_partition_audit()
    payload = {
        "partition_state_rows": partition_rows,
        "q2_k3_hall_partition_audit": hall_row,
    }
    digest = hashlib.sha256(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()
    return {
        "schema": "amra.opg1757.partition_aware_hall.v1",
        "claim_labels": {
            "partition_repair_theorem": "human_proof",
            "safe_coarsening_quotient_criterion": "human_proof",
            "split_then_merge_normal_form": "human_proof",
            "partition_state_hall_lifting": "human_proof",
            "forced_edge_obstruction": "human_proof",
            "partition_state_rows": "finite_evidence",
            "q2_k3_hall_partition_audit": "finite_evidence",
            "outside_fixed_local_injection_for_all_contexts": "refuted",
            "full_first_coefficient_positivity": "open_gap",
        },
        **payload,
        "sha256_payload": digest,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name(
            "partition_aware_hall_certificate.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rendered = json.dumps(build_audit(), indent=2, sort_keys=True)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
