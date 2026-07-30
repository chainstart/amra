#!/usr/bin/env python3
"""Classify q=1 deficits and certify the complete k=5 finite injection."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

from verify_f_leading_swap_obstruction import (
    Edge,
    Forest,
    all_forests,
    union_multiplicity,
    valid_negative,
    valid_positive,
)
from verify_f_leading_k4_outside_stability import local_repair_rows


Pair = tuple[Forest, Forest]
UnionKey = tuple[tuple[Edge, int], ...]
TERMINAL_EDGES = frozenset(itertools.combinations(range(4), 2))


def edge_rows(edges: Forest) -> list[list[int]]:
    return [list(edge) for edge in sorted(edges)]


def pair_key(pair: Pair) -> tuple[tuple[Edge, ...], tuple[Edge, ...]]:
    return tuple(sorted(pair[0])), tuple(sorted(pair[1]))


def colored_copies(pair: Pair) -> frozenset[tuple[int, Edge]]:
    return frozenset(
        (color, edge)
        for color, forest in enumerate(pair)
        for edge in forest
    )


def component_partition(forest: Forest) -> tuple[tuple[int, ...], ...]:
    parent = list(range(5))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in forest:
        left_root = root(left)
        right_root = root(right)
        parent[left_root] = right_root
    return tuple(
        sorted(
            tuple(vertex for vertex in range(5) if root(vertex) == component)
            for component in {root(vertex) for vertex in range(5)}
        )
    )


def active_outside(pair: Pair) -> bool:
    return any(4 in edge for edge in pair[0] | pair[1])


def endpoint_permutations() -> tuple[dict[int, int], ...]:
    rows: list[dict[int, int]] = []
    for swap_first in (False, True):
        for swap_second in (False, True):
            rows.append(
                {
                    0: 1 if swap_first else 0,
                    1: 0 if swap_first else 1,
                    2: 3 if swap_second else 2,
                    3: 2 if swap_second else 3,
                    4: 4,
                }
            )
    return tuple(rows)


def transform_union(key: UnionKey, permutation: dict[int, int]) -> UnionKey:
    return tuple(
        sorted(
            (
                tuple(sorted((permutation[left], permutation[right]))),
                multiplicity,
            )
            for (left, right), multiplicity in key
        )
    )


def union_rows(key: UnionKey) -> list[list[object]]:
    return [[list(edge), multiplicity] for edge, multiplicity in key]


def normal_form_type(key: UnionKey) -> str:
    multiplicities = dict(key)
    total = sum(multiplicities.values())
    terminal_complete = all(multiplicities.get(edge) == 1 for edge in TERMINAL_EDGES)
    outside = [
        (edge, multiplicity)
        for edge, multiplicity in key
        if 4 in edge
    ]
    missing = TERMINAL_EDGES - set(multiplicities)
    outside_neighbors = {
        left if right == 4 else right
        for (left, right), _ in outside
    }
    if terminal_complete and total == 7:
        return "saturated_k4_plus_pendant"
    if (
        total == 7
        and len(outside) == 2
        and len(missing) == 1
        and missing == {tuple(sorted(outside_neighbors))}
    ):
        return "single_edge_subdivision_k4"
    if total == 7:
        return "three_arm_y_replacement"
    if terminal_complete and any(value == 2 for _, value in outside):
        return "saturated_k4_plus_doubled_pendant"
    if terminal_complete:
        return "saturated_k4_plus_two_pendants"
    if any(value == 2 for _, value in key):
        return "doubled_edge_extension"
    return "simple_eight_edge_extension"


def enumerate_objects() -> tuple[list[Pair], list[Pair]]:
    positives: list[Pair] = []
    negatives: list[Pair] = []
    for red in all_forests(5):
        for blue in all_forests(5):
            pair = (red, blue)
            if not active_outside(pair):
                continue
            if valid_positive(red, blue):
                positives.append(pair)
            elif valid_negative(red, blue):
                negatives.append(pair)
    return sorted(positives, key=pair_key), sorted(negatives, key=pair_key)


def deterministic_distance_two_matching(
    positives: list[Pair], negatives: list[Pair]
) -> tuple[list[int], Counter[int], int]:
    positive_copies = [colored_copies(pair) for pair in positives]
    negative_copies = [colored_copies(pair) for pair in negatives]
    adjacency: list[list[int]] = []
    zero_degree_at_one = 0
    for source in negative_copies:
        distance_one = [
            target
            for target, copies in enumerate(positive_copies)
            if len(source - copies) <= 1
        ]
        if not distance_one:
            zero_degree_at_one += 1
        candidates = [
            target
            for target, copies in enumerate(positive_copies)
            if len(source - copies) <= 2
        ]
        candidates.sort(
            key=lambda target: (
                len(source - positive_copies[target]),
                pair_key(positives[target]),
            )
        )
        adjacency.append(candidates)
    if min(map(len, adjacency)) == 0:
        raise AssertionError("distance-two candidate graph has an isolate")

    sys.setrecursionlimit(10000)
    target_to_source = [-1] * len(positives)
    visit_stamp = [0] * len(positives)
    stamp = 0

    def augment(source: int) -> bool:
        for target in adjacency[source]:
            if visit_stamp[target] == stamp:
                continue
            visit_stamp[target] = stamp
            if target_to_source[target] < 0 or augment(
                target_to_source[target]
            ):
                target_to_source[target] = source
                return True
        return False

    order = sorted(
        range(len(negatives)),
        key=lambda source: (len(adjacency[source]), pair_key(negatives[source])),
    )
    for source in order:
        stamp += 1
        if not augment(source):
            raise AssertionError("distance-two matching failed")

    source_to_target = [-1] * len(negatives)
    for target, source in enumerate(target_to_source):
        if source >= 0:
            source_to_target[source] = target
    if any(target < 0 for target in source_to_target):
        raise AssertionError("matching omitted a negative object")
    if len(set(source_to_target)) != len(source_to_target):
        raise AssertionError("matching is not injective")
    distance_counts = Counter(
        len(negative_copies[source] - positive_copies[target])
        for source, target in enumerate(source_to_target)
    )
    return source_to_target, distance_counts, zero_degree_at_one


def balanced_exchange_allowed(
    source: frozenset[tuple[int, Edge]],
    target: frozenset[tuple[int, Edge]],
) -> bool:
    removed = source - target
    added = target - source
    if len(removed) == 1:
        return removed == {(1, (0, 1))} and added == {(0, (0, 1))}
    return (
        len(removed) == 2
        and Counter(color for color, _ in removed) == {0: 1, 1: 1}
        and Counter(color for color, _ in added) == {0: 1, 1: 1}
    )


def maximum_matching(
    adjacency: list[list[int]],
    positives: list[Pair],
    negatives: list[Pair],
) -> list[int]:
    sys.setrecursionlimit(10000)
    target_to_source = [-1] * len(positives)
    visit_stamp = [0] * len(positives)
    stamp = 0

    def augment(source: int) -> bool:
        for target in adjacency[source]:
            if visit_stamp[target] == stamp:
                continue
            visit_stamp[target] = stamp
            if target_to_source[target] < 0 or augment(
                target_to_source[target]
            ):
                target_to_source[target] = source
                return True
        return False

    order = sorted(
        range(len(negatives)),
        key=lambda source: (len(adjacency[source]), pair_key(negatives[source])),
    )
    for source in order:
        stamp += 1
        augment(source)
    source_to_target = [-1] * len(negatives)
    for target, source in enumerate(target_to_source):
        if source >= 0:
            source_to_target[source] = target
    return source_to_target


def hall_witness(
    adjacency: list[list[int]], source_to_target: list[int]
) -> tuple[set[int], set[int]]:
    """Return the alternating-reachable deficient source set and its neighborhood."""

    target_to_source = {
        target: source
        for source, target in enumerate(source_to_target)
        if target >= 0
    }
    sources = {
        source
        for source, target in enumerate(source_to_target)
        if target < 0
    }
    queue = deque(sources)
    targets: set[int] = set()
    while queue:
        source = queue.popleft()
        for target in adjacency[source]:
            if target == source_to_target[source] or target in targets:
                continue
            targets.add(target)
            following = target_to_source.get(target)
            if following is not None and following not in sources:
                sources.add(following)
                queue.append(following)
    if {
        target
        for source in sources
        for target in adjacency[source]
    } != targets:
        raise AssertionError("alternating Hall witness lost a neighbor")
    return sources, targets


def transform_colored_copy(
    colored: tuple[int, Edge], permutation: dict[int, int]
) -> tuple[int, Edge]:
    color, (left, right) = colored
    return color, tuple(sorted((permutation[left], permutation[right])))


def transform_pair(pair: Pair, permutation: dict[int, int]) -> Pair:
    return tuple(
        frozenset(
            tuple(sorted((permutation[left], permutation[right])))
            for left, right in forest
        )
        for forest in pair
    )


def bridge_exchange_edge(
    source: frozenset[tuple[int, Edge]],
    target: frozenset[tuple[int, Edge]],
) -> Edge | None:
    """Return x when the move swaps the colors of E=01 and x."""

    removed = source - target
    added = target - source
    if len(removed) != 2 or len(added) != 2:
        return None
    red_removed = [edge for color, edge in removed if color == 0]
    blue_removed = [edge for color, edge in removed if color == 1]
    red_added = [edge for color, edge in added if color == 0]
    blue_added = [edge for color, edge in added if color == 1]
    if (
        len(red_removed) == len(blue_removed)
        == len(red_added) == len(blue_added)
        == 1
        and blue_removed[0] == (0, 1)
        and red_added[0] == (0, 1)
        and red_removed[0] == blue_added[0]
    ):
        return red_removed[0]
    return None


def fundamental_exchange_type(edge: Edge) -> str:
    if 4 not in edge:
        return "core_cross"
    if set(edge).intersection({0, 1}):
        return "E_active"
    return "F_active"


def orbit_summary(
    indices: set[int],
    objects: list[Pair],
    permutations: tuple[dict[int, int], ...],
) -> dict[str, object]:
    object_index = {pair: index for index, pair in enumerate(objects)}
    seen: set[int] = set()
    orbit_types: Counter[str] = Counter()
    orbit_sizes: Counter[int] = Counter()
    for index in sorted(indices):
        if index in seen:
            continue
        orbit = {
            object_index[transform_pair(objects[index], permutation)]
            for permutation in permutations
        }
        if not orbit.issubset(indices):
            raise AssertionError("set is not invariant under endpoint swaps")
        seen.update(orbit)
        orbit_types[
            normal_form_type(union_multiplicity(*objects[index]))
        ] += 1
        orbit_sizes[len(orbit)] += 1
    return {
        "object_count": len(indices),
        "orbit_count": sum(orbit_types.values()),
        "orbit_normal_form_counts": dict(sorted(orbit_types.items())),
        "orbit_size_counts": {
            str(size): count for size, count in sorted(orbit_sizes.items())
        },
    }


def shortest_augmenting_extension(
    adjacency: list[list[int]],
    positives: list[Pair],
    negatives: list[Pair],
    initial_matching: list[int],
) -> tuple[list[int], list[list[tuple[int, int]]]]:
    """Extend a matching by deterministic shortest alternating paths."""

    source_to_target = initial_matching.copy()
    target_to_source = {
        target: source
        for source, target in enumerate(source_to_target)
        if target >= 0
    }
    if len(target_to_source) != sum(
        target >= 0 for target in source_to_target
    ):
        raise AssertionError("initial matching is not injective")
    chains: list[list[tuple[int, int]]] = []
    unmatched = sorted(
        (
            source
            for source, target in enumerate(source_to_target)
            if target < 0
        ),
        key=lambda source: (
            len(adjacency[source]),
            pair_key(negatives[source]),
        ),
    )
    for start in unmatched:
        source_queue = deque([start])
        seen_sources = {start}
        seen_targets: set[int] = set()
        target_predecessor: dict[int, int] = {}
        source_predecessor: dict[int, int] = {}
        endpoint: int | None = None
        while source_queue and endpoint is None:
            source = source_queue.popleft()
            for target in adjacency[source]:
                if (
                    target == source_to_target[source]
                    or target in seen_targets
                ):
                    continue
                seen_targets.add(target)
                target_predecessor[target] = source
                following = target_to_source.get(target)
                if following is None:
                    endpoint = target
                    break
                if following not in seen_sources:
                    seen_sources.add(following)
                    source_predecessor[following] = target
                    source_queue.append(following)
        if endpoint is None:
            raise AssertionError("expanded graph has no augmenting path")

        chain: list[tuple[int, int]] = []
        target = endpoint
        while True:
            source = target_predecessor[target]
            chain.append((source, target))
            if source == start:
                break
            target = source_predecessor[source]
        chain.reverse()

        if source_to_target[chain[0][0]] >= 0:
            raise AssertionError("augmenting chain does not start unmatched")
        for position in range(1, len(chain)):
            if (
                source_to_target[chain[position][0]]
                != chain[position - 1][1]
            ):
                raise AssertionError("augmenting chain is not alternating")
        if chain[-1][1] in target_to_source:
            raise AssertionError("augmenting chain does not end unmatched")
        for source, _ in chain:
            old_target = source_to_target[source]
            if old_target >= 0:
                del target_to_source[old_target]
        for source, target in chain:
            source_to_target[source] = target
            target_to_source[target] = source
        chains.append(chain)
    return source_to_target, chains


def canonical_rule_signature(
    source: frozenset[tuple[int, Edge]],
    target: frozenset[tuple[int, Edge]],
) -> tuple[tuple[tuple[int, Edge], ...], tuple[tuple[int, Edge], ...]]:
    removed = source - target
    added = target - source
    return min(
        (
            tuple(
                sorted(
                    transform_colored_copy(colored, permutation)
                    for colored in removed
                )
            ),
            tuple(
                sorted(
                    transform_colored_copy(colored, permutation)
                    for colored in added
                )
            ),
        )
        for permutation in endpoint_permutations()
    )


def colored_rows(
    copies: tuple[tuple[int, Edge], ...]
) -> list[list[object]]:
    return [[color, list(edge)] for color, edge in copies]


def build_audit() -> dict[str, object]:
    positives, negatives = enumerate_objects()
    grouped: defaultdict[UnionKey, list[int]] = defaultdict(lambda: [0, 0])
    for pair in positives:
        grouped[union_multiplicity(*pair)][0] += 1
    for pair in negatives:
        grouped[union_multiplicity(*pair)][1] += 1
    deficits = {
        key: tuple(counts)
        for key, counts in grouped.items()
        if counts[1] > counts[0]
    }
    if len(deficits) != 42:
        raise AssertionError("five-vertex deficit class count changed")
    by_total = Counter(
        sum(multiplicity for _, multiplicity in key)
        for key in deficits
    )
    if by_total != {7: 12, 8: 30}:
        raise AssertionError("q=1 deficit degree split changed")

    permutations = endpoint_permutations()
    seen: set[UnionKey] = set()
    normal_forms: list[list[object]] = []
    for representative in sorted(deficits):
        if representative in seen:
            continue
        orbit = {
            transform_union(representative, permutation)
            for permutation in permutations
        }
        if not orbit.issubset(deficits):
            raise AssertionError("deficit class is not symmetry invariant")
        seen.update(orbit)
        counts = deficits[representative]
        total = sum(multiplicity for _, multiplicity in representative)
        missing = sorted(TERMINAL_EDGES - {edge for edge, _ in representative})
        outside = [
            [list(edge), multiplicity]
            for edge, multiplicity in representative
            if 4 in edge
        ]
        normal_forms.append(
            [
                len(normal_forms),
                total - 2,
                len(orbit),
                counts[0],
                counts[1],
                counts[1] - counts[0],
                normal_form_type(representative),
                union_rows(representative),
                [list(edge) for edge in missing],
                outside,
                sorted(multiplicity for _, multiplicity in representative),
            ]
        )
    normal_forms.sort(key=lambda row: (row[1], row[7]))
    for index, row in enumerate(normal_forms):
        row[0] = index
    if len(normal_forms) != 16:
        raise AssertionError("normal-form orbit count changed")
    if Counter(row[1] for row in normal_forms) != {5: 5, 6: 11}:
        raise AssertionError("normal-form degree split changed")
    if sum(row[2] for row in normal_forms) != 42:
        raise AssertionError("normal forms do not cover all deficit classes")

    k5_positives = [
        pair for pair in positives if len(pair[0]) + len(pair[1]) == 7
    ]
    k5_negatives = [
        pair for pair in negatives if len(pair[0]) + len(pair[1]) == 7
    ]
    if (len(k5_positives), len(k5_negatives)) != (2240, 2140):
        raise AssertionError("q=1,k=5 object totals changed")
    target_indices, distance_counts, zero_degree_at_one = (
        deterministic_distance_two_matching(k5_positives, k5_negatives)
    )
    if distance_counts != {1: 239, 2: 1901}:
        raise AssertionError("finite injection distance profile changed")
    matching_payload = json.dumps(
        target_indices, separators=(",", ":")
    ).encode("utf-8")
    matching_digest = hashlib.sha256(matching_payload).hexdigest()

    positive_copies = [colored_copies(pair) for pair in k5_positives]
    negative_copies = [colored_copies(pair) for pair in k5_negatives]
    balanced_adjacency: list[list[int]] = []
    for source in negative_copies:
        candidates = [
            target
            for target, copies in enumerate(positive_copies)
            if balanced_exchange_allowed(source, copies)
        ]
        candidates.sort(
            key=lambda target: (
                len(source - positive_copies[target]),
                pair_key(k5_positives[target]),
            )
        )
        balanced_adjacency.append(candidates)
    balanced_targets = maximum_matching(
        balanced_adjacency, k5_positives, k5_negatives
    )
    if any(target < 0 for target in balanced_targets):
        raise AssertionError("balanced direct/exchange matching failed")
    if len(set(balanced_targets)) != len(balanced_targets):
        raise AssertionError("balanced matching is not injective")
    balanced_distance_counts = Counter(
        len(negative_copies[source] - positive_copies[target])
        for source, target in enumerate(balanced_targets)
    )
    if balanced_distance_counts != {1: 594, 2: 1546}:
        raise AssertionError("balanced matching distance profile changed")
    rule_counts = Counter(
        canonical_rule_signature(
            negative_copies[source], positive_copies[target]
        )
        for source, target in enumerate(balanced_targets)
    )
    if len(rule_counts) != 22:
        raise AssertionError("balanced rule-orbit count changed")
    rule_rows = [
        [
            count,
            colored_rows(signature[0]),
            colored_rows(signature[1]),
        ]
        for signature, count in sorted(
            rule_counts.items(), key=lambda row: (-row[1], row[0])
        )
    ]
    balanced_digest = hashlib.sha256(
        json.dumps(balanced_targets, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    source_partitions = [
        (
            component_partition(pair[0]),
            component_partition(pair[1]),
        )
        for pair in k5_negatives
    ]
    target_partitions = [
        (
            component_partition(pair[0]),
            component_partition(pair[1]),
        )
        for pair in k5_positives
    ]
    tree_stable_adjacency = [
        [
            target
            for target in candidates
            if (
                len(negative_copies[source] - positive_copies[target]) == 1
                or source_partitions[source] == target_partitions[target]
            )
        ]
        for source, candidates in enumerate(balanced_adjacency)
    ]
    tree_stable_isolates = [
        source
        for source, candidates in enumerate(tree_stable_adjacency)
        if not candidates
    ]
    if len(tree_stable_isolates) != 150:
        raise AssertionError("tree-stable isolate count changed")
    isolate_types = Counter(
        normal_form_type(union_multiplicity(*k5_negatives[source]))
        for source in tree_stable_isolates
    )
    if isolate_types != {
        "three_arm_y_replacement": 146,
        "single_edge_subdivision_k4": 4,
    }:
        raise AssertionError("tree-stable isolate types changed")
    tree_stable_targets = maximum_matching(
        tree_stable_adjacency, k5_positives, k5_negatives
    )
    tree_stable_matched = sum(target >= 0 for target in tree_stable_targets)
    if tree_stable_matched != 1790:
        raise AssertionError("tree-stable maximum matching changed")
    first_isolate = min(tree_stable_isolates)
    failure_pair = k5_negatives[first_isolate]
    failure_row = {
        "negative_index": first_isolate,
        "red": edge_rows(failure_pair[0]),
        "blue": edge_rows(failure_pair[1]),
        "union": union_rows(union_multiplicity(*failure_pair)),
        "normal_form": normal_form_type(union_multiplicity(*failure_pair)),
        "red_partition": [
            list(component) for component in source_partitions[first_isolate][0]
        ],
        "blue_partition": [
            list(component) for component in source_partitions[first_isolate][1]
        ],
        "candidate_count": 0,
    }

    # The 150 same-support isolates admit a much smaller component-transition
    # repair.  Their blue forest is E plus a tree on C={2,3,4}.  The red
    # E-path crosses the cut A={0,1}, C exactly twice; swapping the color of
    # E with either crossing edge x is a valid positive pair.  In the image,
    # x is the unique blue A--C edge, so the inverse is local and canonical.
    bridge_adjacency: list[list[int]] = []
    bridge_action_types: Counter[str] = Counter()
    bridge_target_preimages: Counter[int] = Counter()
    for source in tree_stable_isolates:
        candidates: list[int] = []
        for target in balanced_adjacency[source]:
            exchanged = bridge_exchange_edge(
                negative_copies[source], positive_copies[target]
            )
            if exchanged is None:
                continue
            candidates.append(target)
            bridge_action_types[
                "active_bridge" if 4 in exchanged else "terminal_bridge"
            ] += 1
            bridge_target_preimages[target] += 1
            cut_edges = [
                edge
                for edge in k5_positives[target][1]
                if len(set(edge).intersection({0, 1})) == 1
            ]
            if cut_edges != [exchanged]:
                raise AssertionError("bridge tag is not unique in the image")
            reconstructed = (
                (k5_positives[target][0] - {(0, 1)}) | {exchanged},
                (k5_positives[target][1] - {exchanged}) | {(0, 1)},
            )
            if reconstructed != k5_negatives[source]:
                raise AssertionError("bridge inverse reconstruction failed")
        bridge_adjacency.append(
            sorted(
                candidates,
                key=lambda target: (
                    bridge_exchange_edge(
                        negative_copies[source], positive_copies[target]
                    ),
                    pair_key(k5_positives[target]),
                ),
            )
        )
    if Counter(map(len, bridge_adjacency)) != {2: 150}:
        raise AssertionError("bridge candidate degree profile changed")
    if bridge_action_types != {
        "terminal_bridge": 200,
        "active_bridge": 100,
    }:
        raise AssertionError("bridge action-type count changed")
    if max(bridge_target_preimages.values()) != 1:
        raise AssertionError("bridge relation is not injective")
    bridge_targets = set(bridge_target_preimages)
    if len(bridge_targets) != 300:
        raise AssertionError("bridge target count changed")

    selected_bridge_targets = [
        candidates[0] for candidates in bridge_adjacency
    ]
    if len(set(selected_bridge_targets)) != 150:
        raise AssertionError("deterministic bridge repair is not injective")
    selected_action_types = Counter(
        "active_bridge" if 4 in exchanged else "terminal_bridge"
        for source, target in zip(
            tree_stable_isolates, selected_bridge_targets
        )
        for exchanged in [
            bridge_exchange_edge(
                negative_copies[source], positive_copies[target]
            )
        ]
        if exchanged is not None
    )
    if selected_action_types != {
        "terminal_bridge": 100,
        "active_bridge": 50,
    }:
        raise AssertionError("selected bridge action profile changed")

    isolate_set = set(tree_stable_isolates)
    seen_isolates: set[int] = set()
    isolate_pair_orbit_types: Counter[str] = Counter()
    for source in tree_stable_isolates:
        if source in seen_isolates:
            continue
        orbit = {
            k5_negatives.index(
                transform_pair(k5_negatives[source], permutation)
            )
            for permutation in permutations
        }
        if not orbit.issubset(isolate_set):
            raise AssertionError("bridge source orbit leaves isolate class")
        seen_isolates.update(orbit)
        isolate_pair_orbit_types[
            normal_form_type(
                union_multiplicity(*k5_negatives[source])
            )
        ] += 1
    if isolate_pair_orbit_types != {
        "three_arm_y_replacement": 41,
        "single_edge_subdivision_k4": 1,
    }:
        raise AssertionError("bridge source-pair orbit count changed")

    positive_index = {
        pair: index for index, pair in enumerate(k5_positives)
    }
    saturated_targets: set[int] = set()
    for _, _, positive_red, positive_blue in local_repair_rows():
        for color in (0, 1):
            for terminal in range(4):
                outside = (terminal, 4)
                target = (
                    positive_red | ({outside} if color == 0 else set()),
                    positive_blue | ({outside} if color == 1 else set()),
                )
                saturated_targets.add(positive_index[target])
    if len(saturated_targets) != 32:
        raise AssertionError("saturated q=1 target count changed")
    if bridge_targets.intersection(saturated_targets):
        raise AssertionError("bridge image meets saturated-repair image")

    tree_target_universe = {
        target
        for candidates in tree_stable_adjacency
        for target in candidates
    }
    if len(tree_target_universe) != 2150:
        raise AssertionError("tree-repair target universe changed")
    if not bridge_targets.issubset(tree_target_universe):
        raise AssertionError("bridge image gained a fresh tree-disjoint target")
    bridge_augmented_adjacency = [
        sorted(
            set(candidates).union(
                bridge_adjacency[tree_stable_isolates.index(source)]
                if source in isolate_set
                else ()
            )
        )
        for source, candidates in enumerate(tree_stable_adjacency)
    ]
    bridge_augmented_targets = maximum_matching(
        bridge_augmented_adjacency, k5_positives, k5_negatives
    )
    bridge_augmented_matched = sum(
        target >= 0 for target in bridge_augmented_targets
    )
    if bridge_augmented_matched != 1790:
        raise AssertionError("bridge-augmented matching size changed")
    hall_sources, hall_targets = hall_witness(
        bridge_augmented_adjacency, bridge_augmented_targets
    )
    if (
        len(hall_sources),
        len(hall_targets),
        len(hall_sources) - len(hall_targets),
        len(hall_sources.intersection(isolate_set)),
    ) != (900, 550, 350, 150):
        raise AssertionError("bridge Hall witness changed")

    first_bridge_source = tree_stable_isolates[0]
    first_bridge_target = bridge_adjacency[0][0]
    competing_tree_sources = [
        source
        for source, candidates in enumerate(tree_stable_adjacency)
        if first_bridge_target in candidates
    ]
    if not competing_tree_sources:
        raise AssertionError("missing bridge/tree image collision")
    first_tree_source = competing_tree_sources[0]
    first_bridge_edge = bridge_exchange_edge(
        negative_copies[first_bridge_source],
        positive_copies[first_bridge_target],
    )
    assert first_bridge_edge is not None
    bridge_collision_row = {
        "bridge_source_index": first_bridge_source,
        "bridge_source_red": edge_rows(k5_negatives[first_bridge_source][0]),
        "bridge_source_blue": edge_rows(k5_negatives[first_bridge_source][1]),
        "bridge_edge": list(first_bridge_edge),
        "tree_source_index": first_tree_source,
        "tree_source_red": edge_rows(k5_negatives[first_tree_source][0]),
        "tree_source_blue": edge_rows(k5_negatives[first_tree_source][1]),
        "common_target_index": first_bridge_target,
        "common_target_red": edge_rows(k5_positives[first_bridge_target][0]),
        "common_target_blue": edge_rows(k5_positives[first_bridge_target][1]),
    }
    bridge_repair_row = {
        "source_count": len(tree_stable_isolates),
        "source_pair_orbit_count": sum(isolate_pair_orbit_types.values()),
        "source_pair_orbit_normal_form_counts": dict(
            sorted(isolate_pair_orbit_types.items())
        ),
        "candidate_degree_counts": {"2": len(tree_stable_isolates)},
        "candidate_action_type_counts": dict(
            sorted(bridge_action_types.items())
        ),
        "candidate_target_count": len(bridge_targets),
        "maximum_candidate_target_indegree": max(
            bridge_target_preimages.values()
        ),
        "selected_action_type_counts": dict(
            sorted(selected_action_types.items())
        ),
        "selected_target_count": len(set(selected_bridge_targets)),
        "saturated_repair_target_count": len(saturated_targets),
        "saturated_image_intersection_count": len(
            bridge_targets.intersection(saturated_targets)
        ),
        "tree_replacement_target_universe_count": len(
            tree_target_universe
        ),
        "bridge_targets_inside_tree_universe_count": len(
            bridge_targets.intersection(tree_target_universe)
        ),
        "tree_plus_bridge_maximum_matching_size": (
            bridge_augmented_matched
        ),
        "tree_plus_bridge_hall_witness_source_count": len(
            hall_sources
        ),
        "tree_plus_bridge_hall_witness_target_count": len(
            hall_targets
        ),
        "tree_plus_bridge_hall_deficiency": (
            len(hall_sources) - len(hall_targets)
        ),
        "tree_plus_bridge_hall_witness_isolate_count": len(
            hall_sources.intersection(isolate_set)
        ),
        "first_tree_image_collision": bridge_collision_row,
    }

    # Round 21: extend the bridge/tree matching by the three possible
    # fundamental exchanges E <-> x.  The three types record whether x is
    # a core cross edge, an E-side active edge, or an F-side active edge.
    hall_source_summary = orbit_summary(
        hall_sources, k5_negatives, permutations
    )
    hall_target_summary = orbit_summary(
        hall_targets, k5_positives, permutations
    )
    hall_source_object_types = Counter(
        normal_form_type(union_multiplicity(*k5_negatives[source]))
        for source in hall_sources
    )
    hall_target_object_types = Counter(
        normal_form_type(union_multiplicity(*k5_positives[target]))
        for target in hall_targets
    )
    if hall_source_summary != {
        "object_count": 900,
        "orbit_count": 231,
        "orbit_normal_form_counts": {
            "saturated_k4_plus_pendant": 4,
            "single_edge_subdivision_k4": 7,
            "three_arm_y_replacement": 220,
        },
        "orbit_size_counts": {"2": 12, "4": 219},
    }:
        raise AssertionError("Hall source orbit summary changed")
    if hall_target_summary != {
        "object_count": 550,
        "orbit_count": 139,
        "orbit_normal_form_counts": {
            "saturated_k4_plus_pendant": 2,
            "single_edge_subdivision_k4": 3,
            "three_arm_y_replacement": 134,
        },
        "orbit_size_counts": {"2": 3, "4": 136},
    }:
        raise AssertionError("Hall target orbit summary changed")

    fresh_targets = set(range(len(k5_positives))) - tree_target_universe
    if len(fresh_targets) != 90:
        raise AssertionError("tree-external positive target count changed")
    fresh_summary = orbit_summary(
        fresh_targets, k5_positives, permutations
    )
    if fresh_summary != {
        "object_count": 90,
        "orbit_count": 27,
        "orbit_normal_form_counts": {
            "three_arm_y_replacement": 27
        },
        "orbit_size_counts": {"2": 9, "4": 18},
    }:
        raise AssertionError("fresh target orbit summary changed")
    fresh_balanced_edges = [
        [
            target
            for target in candidates
            if target in fresh_targets
        ]
        for candidates in balanced_adjacency
    ]
    fresh_augmented_adjacency = [
        sorted(set(base).union(fresh))
        for base, fresh in zip(
            bridge_augmented_adjacency, fresh_balanced_edges
        )
    ]
    fresh_augmented_matching = maximum_matching(
        fresh_augmented_adjacency, k5_positives, k5_negatives
    )
    fresh_augmented_size = sum(
        target >= 0 for target in fresh_augmented_matching
    )
    hall_fresh_edges = sum(
        len(fresh_balanced_edges[source]) for source in hall_sources
    )
    hall_fresh_sources = sum(
        bool(fresh_balanced_edges[source]) for source in hall_sources
    )
    hall_fresh_targets = {
        target
        for source in hall_sources
        for target in fresh_balanced_edges[source]
    }
    if (
        sum(map(len, fresh_balanced_edges)),
        sum(bool(row) for row in fresh_balanced_edges),
        hall_fresh_edges,
        hall_fresh_sources,
        len(hall_fresh_targets),
        fresh_augmented_size,
    ) != (1224, 360, 324, 108, 54, 1844):
        raise AssertionError("fresh-target augmentation profile changed")

    fundamental_types = ("core_cross", "E_active", "F_active")
    fundamental_by_type = {
        kind: [[] for _ in k5_negatives]
        for kind in fundamental_types
    }
    for source, candidates in enumerate(balanced_adjacency):
        for target in candidates:
            exchanged = bridge_exchange_edge(
                negative_copies[source], positive_copies[target]
            )
            if exchanged is not None:
                fundamental_by_type[
                    fundamental_exchange_type(exchanged)
                ][source].append(target)
    fundamental_candidate_counts = {
        kind: sum(map(len, fundamental_by_type[kind]))
        for kind in fundamental_types
    }
    if fundamental_candidate_counts != {
        "core_cross": 1560,
        "E_active": 830,
        "F_active": 320,
    }:
        raise AssertionError("fundamental candidate profile changed")

    def expanded_adjacency(kinds: tuple[str, ...]) -> list[list[int]]:
        return [
            sorted(
                set(bridge_augmented_adjacency[source]).union(
                    *(
                        fundamental_by_type[kind][source]
                        for kind in kinds
                    )
                )
            )
            for source in range(len(k5_negatives))
        ]

    def matching_size(adjacency: list[list[int]]) -> int:
        return sum(
            target >= 0
            for target in maximum_matching(
                adjacency, k5_positives, k5_negatives
            )
        )

    fundamental_subset_rows: list[list[object]] = []
    for subset_size in range(4):
        for kinds in itertools.combinations(
            fundamental_types, subset_size
        ):
            adjacency = expanded_adjacency(kinds)
            fundamental_subset_rows.append(
                [
                    list(kinds),
                    sum(map(len, adjacency)),
                    len(
                        {
                            target
                            for candidates in adjacency
                            for target in candidates
                        }
                    ),
                    matching_size(adjacency),
                ]
            )
    expected_fundamental_rows = [
        [[], 7240, 2150, 1790],
        [["core_cross"], 8040, 2222, 2018],
        [["E_active"], 7740, 2192, 1960],
        [["F_active"], 7544, 2150, 1790],
        [["core_cross", "E_active"], 8540, 2240, 2108],
        [["core_cross", "F_active"], 8344, 2222, 2058],
        [["E_active", "F_active"], 8044, 2192, 1968],
        [
            ["core_cross", "E_active", "F_active"],
            8844,
            2240,
            2140,
        ],
    ]
    if fundamental_subset_rows != expected_fundamental_rows:
        raise AssertionError("fundamental subset matching table changed")

    # Certify minimality against every one- or two-orbit extension, not only
    # against the three natural fundamental types.
    extra_rule_groups: defaultdict[
        tuple[
            tuple[tuple[int, Edge], ...],
            tuple[tuple[int, Edge], ...],
        ],
        list[list[int]],
    ] = defaultdict(lambda: [[] for _ in k5_negatives])
    for source, candidates in enumerate(balanced_adjacency):
        base_targets = set(bridge_augmented_adjacency[source])
        for target in candidates:
            if target not in base_targets:
                extra_rule_groups[
                    canonical_rule_signature(
                        negative_copies[source],
                        positive_copies[target],
                    )
                ][source].append(target)
    extra_rules = sorted(extra_rule_groups)
    if len(extra_rules) != 21:
        raise AssertionError("extra balanced rule-orbit count changed")

    def rule_expanded_size(
        selected_rules: tuple[
            tuple[
                tuple[tuple[int, Edge], ...],
                tuple[tuple[int, Edge], ...],
            ],
            ...,
        ],
    ) -> int:
        adjacency = [
            sorted(
                set(bridge_augmented_adjacency[source]).union(
                    *(
                        extra_rule_groups[rule][source]
                        for rule in selected_rules
                    )
                )
            )
            for source in range(len(k5_negatives))
        ]
        return matching_size(adjacency)

    best_single = max(
        (rule_expanded_size((rule,)), rule) for rule in extra_rules
    )
    best_pair = max(
        (
            rule_expanded_size((first, second)),
            first,
            second,
        )
        for first, second in itertools.combinations(extra_rules, 2)
    )
    if best_single[0] != 2018 or best_pair[0] != 2110:
        raise AssertionError("one/two-rule minimality audit changed")

    full_adjacency = expanded_adjacency(fundamental_types)
    final_targets, augmentation_chains = shortest_augmenting_extension(
        full_adjacency,
        k5_positives,
        k5_negatives,
        bridge_augmented_targets,
    )
    if any(target < 0 for target in final_targets):
        raise AssertionError("fundamental extension is not complete")
    if len(set(final_targets)) != len(final_targets):
        raise AssertionError("fundamental extension is not injective")
    if len(augmentation_chains) != 350:
        raise AssertionError("augmenting-chain count changed")
    chain_length_counts = Counter(map(len, augmentation_chains))
    if chain_length_counts != {
        2: 168,
        3: 112,
        4: 47,
        5: 14,
        6: 6,
        7: 2,
        8: 1,
    }:
        raise AssertionError("shortest augmenting-chain profile changed")
    chain_new_rule_counts = Counter(
        sum(
            target not in bridge_augmented_adjacency[source]
            for source, target in chain
        )
        for chain in augmentation_chains
    )
    if chain_new_rule_counts != {1: 150, 2: 188, 3: 11, 4: 1}:
        raise AssertionError("augmenting-chain new-rule profile changed")

    final_rule_counts: Counter[str] = Counter()
    final_image_sets: defaultdict[str, set[int]] = defaultdict(set)
    for source, target in enumerate(final_targets):
        if target in bridge_augmented_adjacency[source]:
            rule = "base_tree_or_bridge"
        else:
            exchanged = bridge_exchange_edge(
                negative_copies[source], positive_copies[target]
            )
            if exchanged is None:
                raise AssertionError("final nonbase edge is not fundamental")
            rule = fundamental_exchange_type(exchanged)
        final_rule_counts[rule] += 1
        final_image_sets[rule].add(target)
    if final_rule_counts != {
        "base_tree_or_bridge": 1590,
        "core_cross": 295,
        "E_active": 203,
        "F_active": 52,
    }:
        raise AssertionError("final routed rule profile changed")
    if sum(map(len, final_image_sets.values())) != len(
        set().union(*final_image_sets.values())
    ):
        raise AssertionError("final rule images are not disjoint")

    chain_endpoints = [
        chain[-1][1] for chain in augmentation_chains
    ]
    endpoint_types = Counter(
        normal_form_type(union_multiplicity(*k5_positives[target]))
        for target in chain_endpoints
    )
    if (
        sum(target in fresh_targets for target in chain_endpoints),
        endpoint_types,
    ) != (
        89,
        {
            "three_arm_y_replacement": 345,
            "single_edge_subdivision_k4": 5,
        },
    ):
        raise AssertionError("augmenting endpoint profile changed")

    # Replay and reverse the ordered path certificate.  This proves finite
    # reversibility independently of the matching search.
    replayed = bridge_augmented_targets.copy()
    for chain in augmentation_chains:
        if replayed[chain[0][0]] >= 0:
            raise AssertionError("replay chain starts at a matched source")
        for position in range(1, len(chain)):
            if replayed[chain[position][0]] != chain[position - 1][1]:
                raise AssertionError("replay chain lost alternation")
        for source, target in chain:
            replayed[source] = target
    if replayed != final_targets:
        raise AssertionError("forward chain replay changed final matching")
    reversed_matching = final_targets.copy()
    for chain in reversed(augmentation_chains):
        for source, target in chain:
            if reversed_matching[source] != target:
                raise AssertionError("reverse chain lost its assigned edge")
        reversed_matching[chain[0][0]] = -1
        for position in range(1, len(chain)):
            reversed_matching[chain[position][0]] = chain[position - 1][1]
    if reversed_matching != bridge_augmented_targets:
        raise AssertionError("reverse chain replay changed base matching")

    chain_rows = [
        [[source, target] for source, target in chain]
        for chain in augmentation_chains
    ]
    routed_matching_digest = hashlib.sha256(
        json.dumps(final_targets, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    chain_digest = hashlib.sha256(
        json.dumps(chain_rows, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    def rule_row(
        signature: tuple[
            tuple[tuple[int, Edge], ...],
            tuple[tuple[int, Edge], ...],
        ]
    ) -> dict[str, object]:
        return {
            "removed": colored_rows(signature[0]),
            "added": colored_rows(signature[1]),
        }

    alternating_routing_row = {
        "hall_source_summary": {
            **hall_source_summary,
            "object_normal_form_counts": dict(
                sorted(hall_source_object_types.items())
            ),
        },
        "hall_target_summary": {
            **hall_target_summary,
            "object_normal_form_counts": dict(
                sorted(hall_target_object_types.items())
            ),
        },
        "fresh_target_summary": fresh_summary,
        "fresh_balanced_edge_count": sum(map(len, fresh_balanced_edges)),
        "fresh_accessible_source_count": sum(
            bool(row) for row in fresh_balanced_edges
        ),
        "hall_to_fresh_edge_count": hall_fresh_edges,
        "hall_source_with_fresh_edge_count": hall_fresh_sources,
        "hall_accessible_fresh_target_count": len(hall_fresh_targets),
        "base_plus_all_fresh_maximum_matching_size": (
            fresh_augmented_size
        ),
        "fundamental_candidate_counts": fundamental_candidate_counts,
        "fundamental_subset_rows": fundamental_subset_rows,
        "extra_balanced_rule_orbit_count": len(extra_rules),
        "best_single_extra_rule_matching_size": best_single[0],
        "best_pair_extra_rule_matching_size": best_pair[0],
        "best_pair_extra_rules": [
            rule_row(best_pair[1]),
            rule_row(best_pair[2]),
        ],
        "minimum_extra_rule_orbit_count_for_full_matching": 3,
        "augmenting_chain_count": len(augmentation_chains),
        "augmenting_chain_length_counts": {
            str(length): count
            for length, count in sorted(chain_length_counts.items())
        },
        "maximum_augmenting_chain_length": max(chain_length_counts),
        "augmenting_chain_new_rule_counts": {
            str(count): frequency
            for count, frequency in sorted(chain_new_rule_counts.items())
        },
        "chain_endpoint_inside_tree_universe_count": sum(
            target in tree_target_universe for target in chain_endpoints
        ),
        "chain_endpoint_outside_tree_universe_count": sum(
            target in fresh_targets for target in chain_endpoints
        ),
        "chain_endpoint_normal_form_counts": dict(
            sorted(endpoint_types.items())
        ),
        "final_rule_counts": dict(sorted(final_rule_counts.items())),
        "final_image_count": len(set(final_targets)),
        "unused_positive_target_count": (
            len(k5_positives) - len(set(final_targets))
        ),
        "pairwise_final_rule_image_intersection_count": 0,
        "target_indices_in_sorted_positive_list": final_targets,
        "sha256_target_indices": routed_matching_digest,
        "augmentation_chains": chain_rows,
        "sha256_augmentation_chains": chain_digest,
    }

    payload = json.dumps(
        [
            normal_forms,
            target_indices,
            balanced_targets,
            rule_rows,
            failure_row,
            bridge_repair_row,
            alternating_routing_row,
        ],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return {
        "schema": "amra.complete_split.f_leading_series_subdivision.v1",
        "deficit_class_count": len(deficits),
        "deficit_classes_by_remaining_degree": {
            "5": by_total[7],
            "6": by_total[8],
        },
        "normal_form_rows": normal_forms,
        "normal_form_summary": (
            "Under independent endpoint swaps of E=01 and F=23, the "
            "12 q=1,k=5 deficit unions form 5 orbits and the 30 q=1,k=6 "
            "deficit unions form 11 orbits. The k=5 orbits comprise two "
            "saturated-K4-plus-pendant types, one single-edge subdivision, "
            "and two three-arm Y-replacement types."
        ),
        "q1_k5_finite_injection": {
            "positive_count": len(k5_positives),
            "negative_count": len(k5_negatives),
            "surplus": len(k5_positives) - len(k5_negatives),
            "maximum_colored_copy_moves": max(distance_counts),
            "distance_counts": {
                str(distance): count
                for distance, count in sorted(distance_counts.items())
            },
            "negative_zero_degree_count_at_distance_1": zero_degree_at_one,
            "target_indices_in_sorted_positive_list": target_indices,
            "sha256_target_indices": matching_digest,
        },
        "q1_k5_balanced_rule_compression": {
            "allowed_moves": (
                "Either move E blue-to-red directly, or remove/add one "
                "edge in each color. No two-to-one color-size transfer "
                "is used."
            ),
            "distance_counts": {
                str(distance): count
                for distance, count in sorted(
                    balanced_distance_counts.items()
                )
            },
            "rule_orbit_count": len(rule_rows),
            "rule_rows": rule_rows,
            "target_indices_in_sorted_positive_list": balanced_targets,
            "sha256_target_indices": balanced_digest,
        },
        "tree_replacement_filter": {
            "definition": (
                "For a two-edge balanced exchange, require both colors "
                "to have the same connected-component partition before "
                "and after. Then each changed component is a tree on the "
                "same local support and is outside-stable by the "
                "terminal-tree replacement lemma."
            ),
            "candidate_edge_count": sum(map(len, tree_stable_adjacency)),
            "isolated_negative_count": len(tree_stable_isolates),
            "isolate_normal_form_counts": dict(sorted(isolate_types.items())),
            "maximum_matching_size": tree_stable_matched,
            "first_failure": failure_row,
        },
        "first_component_bridge_repair": {
            "definition": (
                "For each of the 150 same-support isolates, put "
                "A={0,1} and C={2,3,4}. The blue source is E=01 plus "
                "a tree on C. The red 0--1 path crosses the A--C cut "
                "in exactly two edges x. Swap the colors of E and "
                "either x. In the image x is the unique blue A--C "
                "edge, so moving x back to red and E back to blue is "
                "the inverse."
            ),
            **bridge_repair_row,
        },
        "coupled_first_component_routing": {
            "definition": (
                "Start from the maximum same-support-plus-isolate-bridge "
                "matching. Add the three fundamental color-swap types "
                "E<->x: core-cross, E-active, and F-active. Repeatedly "
                "take a deterministic shortest alternating path from "
                "an unmatched negative source to an unused positive "
                "target. The ordered path list replays to a full "
                "matching and reverses exactly to the base matching."
            ),
            **alternating_routing_row,
        },
        "path_tag_obstruction": (
            "Suppressing a single two-edge path covers only one of the "
            "five k=5 normal forms. Two additional Y-replacement orbits "
            "share one active vertex among two missing terminal edges. "
            "A balanced direct/exchange matching compresses to 22 rule "
            "orbits, but the outside-stable same-component tree filter "
            "has 150 isolated negatives (146 Y and 4 path types) and "
            "maximum matching size only 1790. Thus the independent "
            "same-support tree lemma does not by itself unify path/Y. "
            "The 150 isolates do admit an injective first-component "
            "bridge swap, compressed to terminal-bridge and active-bridge "
            "tags, whose image avoids all 32 q=1 saturated-repair images. "
            "All 300 possible bridge targets already lie in the "
            "2150-target same-support repair universe, and adding these "
            "bridge edges alone leaves the maximum matching at 1790. "
            "Round 21 closes this finite routing obstruction by adding "
            "the three fundamental E<->x edge types and 350 shortest "
            "alternating paths of length at most 8."
        ),
        "next_lemma": (
            "Generalize the finite shortest-chain certificate to "
            "arbitrary q and k. Define the first active block and the "
            "three fundamental E<->x types without using the five-vertex "
            "ordering; prove every alternating chain strictly decreases "
            "a lexicographic block potential or reaches an unused image, "
            "and prove the terminal image recovers the ordered sequence "
            "of first-transition tags. The q=1,k=5 audit shows chain "
            "length at most 8, but does not yet provide a uniform bound."
        ),
        "scope": (
            "The 16 normal forms and the q=1,k=5 injection are exact "
            "finite certificates. They are not a general injection for "
            "arbitrary q or k."
        ),
        "sha256_payload": hashlib.sha256(payload).hexdigest(),
        "status": "proved_finite_coupled_routing_not_general",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rendered = json.dumps(build_audit(), indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
