#!/usr/bin/env python3
"""Audit first-active-block potentials and the q=2 fourth-rule obstruction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

from verify_f_leading_series_subdivision import (
    colored_copies,
    edge_rows,
    enumerate_objects,
)
from verify_f_leading_swap_obstruction import (
    E,
    F,
    Edge,
    Forest,
    Pair,
    all_forests,
    is_forest,
)


Q1_AUDIT_PATH = Path(__file__).with_name(
    "f_leading_series_subdivision_audit.json"
)
Q2_VERTEX_COUNT = 6
Q2_OUTSIDE = frozenset({4, 5})
Q2_EDGES = tuple(itertools.combinations(range(Q2_VERTEX_COUNT), 2))
ACTIVE_HANDOFF_SIGNATURE = ((2, 4), (2, 5))
CORE_TO_ACTIVE_PAIR_SIGNATURE = ((0, 2), (4, 5))


def pair_key(pair: Pair) -> tuple[tuple[Edge, ...], tuple[Edge, ...]]:
    return tuple(sorted(pair[0])), tuple(sorted(pair[1]))


def pair_row(pair: Pair) -> dict[str, list[list[int]]]:
    return {"red": edge_rows(pair[0]), "blue": edge_rows(pair[1])}


def component_partition(
    vertex_count: int, forest: Forest
) -> tuple[tuple[int, ...], ...]:
    parent = list(range(vertex_count))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in forest:
        parent[root(left)] = root(right)
    return tuple(
        sorted(
            tuple(
                vertex
                for vertex in range(vertex_count)
                if root(vertex) == component
            )
            for component in {root(vertex) for vertex in range(vertex_count)}
        )
    )


def exact_q2_active(pair: Pair) -> bool:
    active = {
        vertex
        for forest in pair
        for edge in forest
        for vertex in edge
    }
    return Q2_OUTSIDE.issubset(active)


def fundamental_type(edge: Edge) -> str:
    left, right = edge
    if right < 4:
        return "core_cross"
    if left >= 4:
        return "active_active"
    if left in (0, 1):
        return "E_active"
    return "F_active"


def q2_permutations() -> tuple[dict[int, int], ...]:
    rows: list[dict[int, int]] = []
    for swap_e in (False, True):
        for swap_f in (False, True):
            for swap_active in (False, True):
                rows.append(
                    {
                        0: 1 if swap_e else 0,
                        1: 0 if swap_e else 1,
                        2: 3 if swap_f else 2,
                        3: 2 if swap_f else 3,
                        4: 5 if swap_active else 4,
                        5: 4 if swap_active else 5,
                    }
                )
    return tuple(rows)


def transform_edge(edge: Edge, permutation: dict[int, int]) -> Edge:
    return tuple(
        sorted((permutation[edge[0]], permutation[edge[1]]))
    )


def exchange_signature(edge_out: Edge, edge_in: Edge) -> tuple[Edge, Edge]:
    return min(
        (
            transform_edge(edge_out, permutation),
            transform_edge(edge_in, permutation),
        )
        for permutation in q2_permutations()
    )


def active_handoff_allowed(edge_out: Edge, edge_in: Edge) -> bool:
    """Recognize the orbit (2,4)->(2,5) without canonicalizing every move."""

    if fundamental_type(edge_out) != "F_active":
        return False
    core = edge_out[0]
    first_active = edge_out[1]
    return edge_in == (
        core,
        5 if first_active == 4 else 4,
    )


def core_to_active_pair_allowed(
    edge_out: Edge, edge_in: Edge
) -> bool:
    return (
        edge_out in {(0, 2), (0, 3), (1, 2), (1, 3)}
        and edge_in == (4, 5)
    )


def enumerate_q2_layer(
    forests_by_size: dict[int, list[Forest]], k: int
) -> tuple[list[Pair], list[Pair]]:
    positives: list[Pair] = []
    negatives: list[Pair] = []
    for red_size in range(Q2_VERTEX_COUNT):
        blue_size = k + 2 - red_size
        if not 0 <= blue_size < Q2_VERTEX_COUNT:
            continue
        for red in forests_by_size[red_size]:
            for blue in forests_by_size[blue_size]:
                pair = (red, blue)
                if not exact_q2_active(pair):
                    continue
                if E in red and E not in blue and F in blue:
                    positives.append(pair)
                elif E not in red and E in blue and F in blue:
                    negatives.append(pair)
    return (
        sorted(positives, key=pair_key),
        sorted(negatives, key=pair_key),
    )


def build_q2_adjacencies(
    positives: list[Pair],
    negatives: list[Pair],
    partitions: dict[Forest, tuple[tuple[int, ...], ...]],
    include_full: bool,
    include_handoff: bool,
) -> tuple[
    list[list[int]],
    list[list[int]],
    list[list[int]] | None,
    list[list[int]],
    list[list[int]],
]:
    positive_index = {
        pair: index for index, pair in enumerate(positives)
    }
    three_rows: list[list[int]] = []
    four_rows: list[list[int]] = []
    full_rows: list[list[int]] | None = [] if include_full else None
    handoff_rows: list[list[int]] = []
    core_pair_rows: list[list[int]] = []
    for red, blue in negatives:
        base_targets: set[int] = set()
        three_targets: set[int] = set()
        active_active_targets: set[int] = set()
        full_targets: set[int] = set()
        handoff_targets: set[int] = set()
        core_pair_targets: set[int] = set()

        direct = positive_index.get((red | {E}, blue - {E}))
        if direct is not None:
            base_targets.add(direct)
            full_targets.add(direct)
        red_partition = partitions[red]
        blue_partition = partitions[blue]
        for edge_out in red:
            following_red = (red - {edge_out}) | {E}
            if following_red not in partitions:
                continue
            for edge_in in Q2_EDGES:
                following_blue = (blue - {E}) | {edge_in}
                target = positive_index.get(
                    (following_red, following_blue)
                )
                if target is None:
                    continue
                full_targets.add(target)
                if (
                    partitions[following_red] == red_partition
                    and partitions[following_blue] == blue_partition
                ):
                    base_targets.add(target)
                if edge_in == edge_out:
                    if fundamental_type(edge_out) == "active_active":
                        active_active_targets.add(target)
                    else:
                        three_targets.add(target)
                elif (
                    include_handoff
                    and active_handoff_allowed(edge_out, edge_in)
                ):
                    handoff_targets.add(target)
                elif core_to_active_pair_allowed(edge_out, edge_in):
                    core_pair_targets.add(target)
        three = base_targets | three_targets
        four = three | active_active_targets
        three_rows.append(sorted(three))
        four_rows.append(sorted(four))
        handoff_rows.append(sorted(four | handoff_targets))
        core_pair_rows.append(sorted(four | core_pair_targets))
        if full_rows is not None:
            full_rows.append(sorted(full_targets))
    return (
        three_rows,
        four_rows,
        full_rows,
        handoff_rows,
        core_pair_rows,
    )


def hopcroft_karp(
    adjacency: list[list[int]], target_count: int
) -> tuple[list[int], list[int], int]:
    source_count = len(adjacency)
    source_to_target = [-1] * source_count
    target_to_source = [-1] * target_count
    distance = [0] * source_count
    infinity = source_count + 1
    sys.setrecursionlimit(max(10000, source_count * 2))

    def breadth_first() -> bool:
        queue: deque[int] = deque()
        found = False
        for source in range(source_count):
            if source_to_target[source] < 0:
                distance[source] = 0
                queue.append(source)
            else:
                distance[source] = infinity
        while queue:
            source = queue.popleft()
            for target in adjacency[source]:
                following = target_to_source[target]
                if following < 0:
                    found = True
                elif distance[following] == infinity:
                    distance[following] = distance[source] + 1
                    queue.append(following)
        return found

    def depth_first(source: int) -> bool:
        for target in adjacency[source]:
            following = target_to_source[target]
            if (
                following < 0
                or (
                    distance[following] == distance[source] + 1
                    and depth_first(following)
                )
            ):
                source_to_target[source] = target
                target_to_source[target] = source
                return True
        distance[source] = infinity
        return False

    size = 0
    while breadth_first():
        for source in range(source_count):
            if source_to_target[source] < 0 and depth_first(source):
                size += 1
    return source_to_target, target_to_source, size


def hall_witness(
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
    queue = deque(sources)
    while queue:
        source = queue.popleft()
        for target in adjacency[source]:
            if target == source_to_target[source] or target in targets:
                continue
            targets.add(target)
            following = target_to_source[target]
            if following >= 0 and following not in sources:
                sources.add(following)
                queue.append(following)
    if {
        target
        for source in sources
        for target in adjacency[source]
    } != targets:
        raise AssertionError("Hall witness lost a neighbor")
    return sources, targets


def shortest_extension_lengths(
    adjacency: list[list[int]],
    initial: list[int],
) -> list[int]:
    source_to_target = initial.copy()
    target_to_source = {
        target: source
        for source, target in enumerate(source_to_target)
        if target >= 0
    }
    lengths: list[int] = []
    for start in (
        source
        for source, target in enumerate(initial)
        if target < 0
    ):
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
            raise AssertionError("fourth rule has no augmenting path")
        chain: list[tuple[int, int]] = []
        target = endpoint
        while True:
            source = target_predecessor[target]
            chain.append((source, target))
            if source == start:
                break
            target = source_predecessor[source]
        chain.reverse()
        for source, _ in chain:
            old = source_to_target[source]
            if old >= 0:
                del target_to_source[old]
        for source, target in chain:
            source_to_target[source] = target
            target_to_source[target] = source
        lengths.append(len(chain))
    return lengths


def q1_static_cycle() -> dict[str, object]:
    saved = json.loads(Q1_AUDIT_PATH.read_text(encoding="utf-8"))
    chains = saved["coupled_first_component_routing"][
        "augmentation_chains"
    ]
    first, second, common_target = 1054, 1174, 903
    occurrences: list[list[int]] = []
    for chain_index, chain in enumerate(chains):
        for position, (left, right) in enumerate(zip(chain, chain[1:])):
            if (left[0], right[0]) in (
                (first, second),
                (second, first),
            ):
                occurrences.append(
                    [
                        chain_index,
                        position,
                        left[0],
                        right[0],
                        left[1],
                    ]
                )
    if occurrences != [
        [317, 2, first, second, common_target],
        [349, 2, second, first, common_target],
    ]:
        raise AssertionError("q=1 source-potential cycle changed")

    positives, negatives = enumerate_objects()
    positives = [
        pair for pair in positives if sum(map(len, pair)) == 7
    ]
    negatives = [
        pair for pair in negatives if sum(map(len, pair)) == 7
    ]
    source_rows = [negatives[first], negatives[second]]
    target = positives[common_target]
    partitions = [
        [
            [
                list(component)
                for component in component_partition(5, forest)
            ]
            for forest in pair
        ]
        for pair in source_rows
    ]
    if partitions[0] != partitions[1]:
        raise AssertionError("cycle source component states changed")
    source_copies = [colored_copies(pair) for pair in source_rows]
    target_copies = colored_copies(target)
    move_rows = []
    for copies in source_copies:
        removed = sorted(copies - target_copies)
        added = sorted(target_copies - copies)
        move_rows.append(
            {
                "removed": [
                    [color, list(edge)] for color, edge in removed
                ],
                "added": [
                    [color, list(edge)] for color, edge in added
                ],
            }
        )
    return {
        "q": 1,
        "k": 5,
        "source_indices": [first, second],
        "common_target_index": common_target,
        "source_rows": [pair_row(pair) for pair in source_rows],
        "common_target": pair_row(target),
        "common_first_active_vertex": 4,
        "common_component_partitions": partitions[0],
        "common_blue_merge_edge": [1, 4],
        "move_rows_to_common_target": move_rows,
        "directed_cycle_occurrences": occurrences,
        "conclusion": (
            "The deterministic shortest-chain conflict relation contains "
            "both 1054->1174 and 1174->1054. Hence no potential depending "
            "only on the current negative source can strictly decrease "
            "at every conflict step. A phase/matching-state coordinate "
            "is necessary, even before q=2."
        ),
    }


def build_audit() -> dict[str, object]:
    forests = all_forests(Q2_VERTEX_COUNT)
    forests_by_size: defaultdict[int, list[Forest]] = defaultdict(list)
    for forest in forests:
        forests_by_size[len(forest)].append(forest)
    partitions = {
        forest: component_partition(Q2_VERTEX_COUNT, forest)
        for forest in forests
    }

    layer_rows: list[list[object]] = []
    q2_k3_hall_row: dict[str, object] | None = None
    q2_k7_core_pair_row: dict[str, object] | None = None
    expected_rows = [
        [1, 2, 2, 2, 3, 2, 2, 2],
        [2, 115, 115, 203, 228, 115, 115, 115],
        [3, 1585, 1589, 3479, 3755, 1583, 1585, 1585],
        [4, 10730, 11024, 27072, 28764, 10692, 10730, 10730],
        [5, 43648, 45620, 130976, 137028, 43488, 43648, 43648],
        [6, 112200, 117384, 470296, 482120, 111960, 112196, 112200],
        [7, 172800, 177984, 1233264, 1242672, 172536, 172768, 172800],
    ]
    for k in range(1, 8):
        positives, negatives = enumerate_q2_layer(forests_by_size, k)
        include_full = k >= 6
        three, four, full, handoff, core_pair = build_q2_adjacencies(
            positives,
            negatives,
            partitions,
            include_full,
            include_handoff=k >= 6,
        )
        three_source, three_target, three_size = hopcroft_karp(
            three, len(positives)
        )
        four_source, four_target, four_size = hopcroft_karp(
            four, len(positives)
        )
        if full is not None:
            _, _, full_size = hopcroft_karp(full, len(positives))
        else:
            full_size = four_size
        row = [
            k,
            len(negatives),
            len(positives),
            sum(map(len, three)),
            sum(map(len, four)),
            three_size,
            four_size,
            full_size,
        ]
        layer_rows.append(row)

        if k == 3:
            hall_sources, hall_targets = hall_witness(
                three, three_source, three_target
            )
            active_active_escapes = [
                [source, target]
                for source in sorted(hall_sources)
                for target in four[source]
                if target not in set(three[source])
                and target not in hall_targets
            ]
            if (
                len(hall_sources),
                len(hall_targets),
                len(hall_sources) - len(hall_targets),
                len(active_active_escapes),
            ) != (8, 6, 2, 8):
                raise AssertionError("minimal fourth-rule Hall witness changed")
            extension_lengths = shortest_extension_lengths(
                four, three_source
            )
            if Counter(extension_lengths) != {3: 2}:
                raise AssertionError("q=2,k=3 fourth-rule chains changed")
            first_source = active_active_escapes[0][0]
            q2_k3_hall_row = {
                "source_count": len(hall_sources),
                "target_count": len(hall_targets),
                "deficiency": len(hall_sources) - len(hall_targets),
                "source_indices": sorted(hall_sources),
                "target_indices": sorted(hall_targets),
                "unmatched_source_indices": [
                    source
                    for source, target in enumerate(three_source)
                    if target < 0
                ],
                "active_active_escape_rows": active_active_escapes,
                "first_source": {
                    "index": first_source,
                    **pair_row(negatives[first_source]),
                },
                "first_escape_target": {
                    "index": active_active_escapes[0][1],
                    **pair_row(
                        positives[active_active_escapes[0][1]]
                    ),
                },
                "fourth_rule": (
                    "When x joins the first two active vertices, swap "
                    "the colors of E and x: "
                    "(R,B)->(R-x+E,B-E+x)."
                ),
                "shortest_augmentation_length_counts": {"3": 2},
            }

        if k in (6, 7):
            _, _, handoff_size = hopcroft_karp(
                handoff, len(positives)
            )
            handoff_added = sum(
                len(set(handoff_row) - set(four_row))
                for handoff_row, four_row in zip(handoff, four)
            )
            expected = {
                6: (37040, 112200),
                7: (30528, 172768),
            }[k]
            if (handoff_added, handoff_size) != expected:
                raise AssertionError("active-handoff extension changed")
            row.extend([handoff_added, handoff_size])
        else:
            row.extend([0, four_size])
        _, _, core_pair_size = hopcroft_karp(
            core_pair, len(positives)
        )
        core_pair_added = sum(
            len(set(core_pair_row) - set(four_row))
            for core_pair_row, four_row in zip(core_pair, four)
        )
        expected_core_pair = {
            1: (0, 2),
            2: (4, 115),
            3: (328, 1585),
            4: (4016, 10730),
            5: (20744, 43648),
            6: (52544, 112196),
            7: (55296, 172800),
        }[k]
        if (core_pair_added, core_pair_size) != expected_core_pair:
            raise AssertionError(
                "core-to-active-pair extension changed: "
                f"k={k}, got={(core_pair_added, core_pair_size)}, "
                f"expected={expected_core_pair}"
            )
        row.extend([core_pair_added, core_pair_size])

        if k == 7:
            hall_sources, hall_targets = hall_witness(
                four, four_source, four_target
            )
            if (
                len(hall_sources),
                len(hall_targets),
                len(hall_sources) - len(hall_targets),
            ) != (2272, 2240, 32):
                raise AssertionError("q=2,k=7 four-rule Hall row changed")
            escape_signatures: set[tuple[Edge, Edge]] = set()
            escape_edge_count = 0
            for source in hall_sources:
                four_targets = set(four[source])
                for target in full[source]:
                    if target in four_targets or target in hall_targets:
                        continue
                    red, blue = negatives[source]
                    target_red, target_blue = positives[target]
                    edge_out = next(iter(red - target_red))
                    edge_in = next(iter(target_blue - blue))
                    escape_signatures.add(
                        exchange_signature(edge_out, edge_in)
                    )
                    escape_edge_count += 1
            if (len(escape_signatures), escape_edge_count) != (20, 25296):
                raise AssertionError("k=7 Hall escape signature count changed")
            added_rows = [
                list(set(core_pair_row) - set(four_row))
                for core_pair_row, four_row in zip(core_pair, four)
            ]
            target_indegrees = Counter(
                target for targets in added_rows for target in targets
            )
            source_outdegrees = Counter(
                source
                for source, targets in enumerate(added_rows)
                for _ in targets
            )
            if (
                len(target_indegrees),
                max(target_indegrees.values()),
                max(source_outdegrees.values()),
            ) != (26496, 4, 2):
                raise AssertionError("core-pair collision profile changed")
            extension_lengths = shortest_extension_lengths(
                core_pair, four_source
            )
            if Counter(extension_lengths) != {
                4: 3,
                5: 17,
                6: 7,
                7: 1,
                8: 1,
                9: 2,
                10: 1,
            }:
                raise AssertionError("core-pair chain profile changed")

            source_index = 1
            target_index = 7890
            source_pair = negatives[source_index]
            target_pair = positives[target_index]
            if target_index not in added_rows[source_index]:
                raise AssertionError("outside-stability example moved")
            extension = frozenset({(0, 6), (1, 6)})
            if not is_forest(7, source_pair[0] | extension):
                raise AssertionError("outside-stability source gained a cycle")
            if is_forest(7, target_pair[0] | extension):
                raise AssertionError("outside-stability target lost its cycle")
            q2_k7_core_pair_row = {
                "rule_signature": [
                    list(CORE_TO_ACTIVE_PAIR_SIGNATURE[0]),
                    list(CORE_TO_ACTIVE_PAIR_SIGNATURE[1]),
                ],
                "definition": (
                    "Remove a red core-cross edge x, add E to red; "
                    "remove E from blue and add the active-active edge 45."
                ),
                "four_rule_hall_source_count": len(hall_sources),
                "four_rule_hall_target_count": len(hall_targets),
                "four_rule_hall_deficiency": (
                    len(hall_sources) - len(hall_targets)
                ),
                "four_rule_hall_escape_signature_orbit_count": len(
                    escape_signatures
                ),
                "four_rule_hall_escape_edge_count": escape_edge_count,
                "added_edge_count": core_pair_added,
                "added_target_count": len(target_indegrees),
                "maximum_added_target_indegree": max(
                    target_indegrees.values()
                ),
                "maximum_added_source_outdegree": max(
                    source_outdegrees.values()
                ),
                "matching_size": core_pair_size,
                "minimum_additional_signature_orbit_count": 1,
                "shortest_augmentation_length_counts": {
                    str(length): count
                    for length, count in sorted(
                        Counter(extension_lengths).items()
                    )
                },
                "maximum_augmentation_length": max(extension_lengths),
                "local_inverse_boundary": (
                    "The image contains the unique q=2 active-active edge "
                    "45, so the added blue edge is visible, but the removed "
                    "core-cross edge is not: target indegree reaches 4. "
                    "A recoverable x-tag or the global matching is required."
                ),
                "outside_stability_counterexample": {
                    "q": 3,
                    "source_index_q2_k7": source_index,
                    "target_index_q2_k7": target_index,
                    "source": pair_row(source_pair),
                    "target": pair_row(target_pair),
                    "unchanged_red_extension": edge_rows(extension),
                    "source_red_extension_is_forest": True,
                    "target_red_extension_is_forest": False,
                    "created_cycle": [[0, 1], [0, 6], [1, 6]],
                },
            }
    if layer_rows != [
        row
        + (
            [37040, 112200]
            if row[0] == 6
            else [30528, 172768]
            if row[0] == 7
            else [0, row[6]]
        )
        + [
            {
                1: 0,
                2: 4,
                3: 328,
                4: 4016,
                5: 20744,
                6: 52544,
                7: 55296,
            }[row[0]],
            {
                1: 2,
                2: 115,
                3: 1585,
                4: 10730,
                5: 43648,
                6: 112196,
                7: 172800,
            }[row[0]],
        ]
        for row in expected_rows
    ]:
        raise AssertionError("q=2 layer table changed")
    if q2_k3_hall_row is None:
        raise AssertionError("missing q=2,k=3 Hall row")
    if q2_k7_core_pair_row is None:
        raise AssertionError("missing q=2,k=7 core-pair row")

    q1_cycle = q1_static_cycle()
    payload = json.dumps(
        [q1_cycle, layer_rows, q2_k3_hall_row, q2_k7_core_pair_row],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return {
        "schema": "amra.complete_split.f_leading_first_active_potential.v1",
        "q1_static_source_potential_obstruction": q1_cycle,
        "q2_layer_columns": [
            "k",
            "negative_count",
            "positive_count",
            "base_plus_three_edge_count",
            "base_plus_four_edge_count",
            "base_plus_three_matching_size",
            "base_plus_four_matching_size",
            "full_balanced_matching_size",
            "active_handoff_added_edge_count",
            "base_plus_four_plus_handoff_matching_size",
            "core_to_active_pair_added_edge_count",
            "base_plus_four_plus_core_pair_matching_size",
        ],
        "q2_layer_rows_k1_to_k7": layer_rows,
        "minimal_fourth_rule_hall_witness": q2_k3_hall_row,
        "q2_k7_single_signature_completion": q2_k7_core_pair_row,
        "fourth_rule_scope": (
            "Within the nested base-plus-fundamental rule family, the "
            "active-active exchange is unnecessary for q=2,k<=2, first "
            "necessary at q=2,k=3, and closes the matching through k=5. "
            "The four-rule graph leaves deficits 4 and 32 at k=6 and k=7. "
            "Thus it is the required fourth orbit for this first failure, "
            "but not a uniform q=2 solution."
        ),
        "active_handoff_scope": (
            "The natural fifth orbit (2,4)->(2,5), handing an F-active "
            "edge from the first active vertex to the second, adds 37040 "
            "edges and closes k=6. At k=7 it adds 30528 edges but does not "
            "increase the matching size 172768. A fixed local handoff is "
            "therefore not the missing uniform potential."
        ),
        "two_signature_small_completion": (
            "For q=2,k<=7 in the tested nested family, two complementary "
            "non-fundamental signatures suffice beyond the four-rule graph: "
            "(2,4)->(2,5) closes k=6 but not k=7, while "
            "(0,2)->(4,5) closes k=7 but not k=6. This is a finite "
            "two-layer completion, not an outside-stable general rule."
        ),
        "revised_potential_requirement": (
            "A source-only lexicographic potential cannot strictly decrease "
            "along the current deterministic Round-21 routing because its "
            "q=1 conflict graph contains directed cycles. This does not "
            "exclude a different routing, a whole-chain potential, a "
            "nonstrict potential with tie-breaking, or a global Hall proof. "
            "A dynamic phase coordinate such as alternating BFS layer plus "
            "a first-active-block tag is one supported repair direction. "
            "Within the tested nested rule family, q=2 also needs an "
            "active-active fourth tag and higher-k rerouting."
        ),
        "next_lemma": (
            "Test a phase-aware first-active-block routing state "
            "(matching phase, BFS distance to a free image, active-block "
            "index, transition tag). Prove BFS distance strictly falls "
            "within a phase and unmatched-source count falls between "
            "phases, or replace it by a whole-chain/global Hall argument. "
            "Then classify the four-rule graph residuals at q=2,k=6 and "
            "k=7; the tested handoff closes k=6 but not k=7."
        ),
        "sha256_payload": hashlib.sha256(payload).hexdigest(),
        "status": "static_potential_refuted_fourth_rule_finite_audited",
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
