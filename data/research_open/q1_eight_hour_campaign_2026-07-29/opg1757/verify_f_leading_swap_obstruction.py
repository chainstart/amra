#!/usr/bin/env python3
"""Audit color-swap obstructions for the leading F_k Rayleigh coefficient."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path


Edge = tuple[int, int]
Forest = frozenset[Edge]
Pair = tuple[Forest, Forest]

E: Edge = (0, 1)
F: Edge = (2, 3)
CROSS_EDGES: tuple[Edge, ...] = ((0, 2), (0, 3), (1, 2), (1, 3))


def is_forest(vertex_count: int, edges: Forest) -> bool:
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


def all_forests(vertex_count: int) -> tuple[Forest, ...]:
    edges = tuple(itertools.combinations(range(vertex_count), 2))
    return tuple(
        frozenset(selected)
        for degree in range(vertex_count)
        for selected in itertools.combinations(edges, degree)
        if is_forest(vertex_count, frozenset(selected))
    )


def forest_path(forest: Forest, source: int, target: int) -> tuple[Edge, ...]:
    adjacency: list[list[int]] = [[] for _ in range(4)]
    for left, right in forest:
        adjacency[left].append(right)
        adjacency[right].append(left)
    parent: dict[int, int | None] = {source: None}
    stack = [source]
    while stack:
        vertex = stack.pop()
        if vertex == target:
            break
        for neighbor in adjacency[vertex]:
            if neighbor not in parent:
                parent[neighbor] = vertex
                stack.append(neighbor)
    if target not in parent:
        return ()
    path: list[Edge] = []
    vertex = target
    while parent[vertex] is not None:
        previous = parent[vertex]
        assert previous is not None
        path.append(tuple(sorted((vertex, previous))))
        vertex = previous
    return tuple(path)


def naive_fundamental_swap(red: Forest, blue: Forest) -> Pair | None:
    """Move E blue->red; choose the lexicographically first feasible cycle edge."""

    blue_without_e = blue - {E}
    if is_forest(4, red | {E}):
        return red | {E}, blue_without_e
    for exchanged in sorted(forest_path(red, *E)):
        if exchanged in blue_without_e:
            continue
        following_red = (red - {exchanged}) | {E}
        following_blue = blue_without_e | {exchanged}
        if is_forest(4, following_blue):
            return following_red, following_blue
    return None


def edge_rows(forest: Forest) -> list[list[int]]:
    return [list(edge) for edge in sorted(forest)]


def pair_row(pair: Pair) -> list[list[list[int]]]:
    return [edge_rows(pair[0]), edge_rows(pair[1])]


def union_multiplicity(red: Forest, blue: Forest) -> tuple[tuple[Edge, int], ...]:
    return tuple(
        (edge, int(edge in red) + int(edge in blue))
        for edge in sorted(red | blue)
    )


def valid_negative(red: Forest, blue: Forest) -> bool:
    return E not in red and E in blue and F in blue


def valid_positive(red: Forest, blue: Forest) -> bool:
    return E in red and E not in blue and F in blue


def build_audit() -> dict[str, object]:
    forests = all_forests(4)

    output_preimages: defaultdict[Pair, list[Pair]] = defaultdict(list)
    for red in forests:
        for blue in forests:
            if not valid_negative(red, blue):
                continue
            following = naive_fundamental_swap(red, blue)
            if following is not None:
                output_preimages[following].append((red, blue))

    collisions_by_size = [
        (
            len(preimages[0][0]) + len(preimages[0][1]),
            output,
            preimages,
        )
        for output, preimages in output_preimages.items()
        if len(preimages) > 1
        and len(
            {
                len(red) + len(blue)
                for red, blue in preimages
            }
        )
        == 1
    ]
    minimum_size = min(size for size, _, _ in collisions_by_size)
    if minimum_size != 4:
        raise AssertionError("minimal naive collision size changed")
    minimum_collision = min(
        (
            (output, preimages)
            for size, output, preimages in collisions_by_size
            if size == minimum_size
        ),
        key=lambda row: (pair_row(row[0]), [pair_row(pair) for pair in row[1]]),
    )
    collision_output, collision_preimages = minimum_collision
    collision_preimages = [
        pair
        for pair in collision_preimages
        if len(pair[0]) + len(pair[1]) == minimum_size
    ]
    if len(collision_preimages) < 2:
        raise AssertionError("collision certificate lost its two preimages")
    collision_preimages = sorted(collision_preimages, key=pair_row)[:2]
    if any(
        naive_fundamental_swap(*pair) != collision_output
        for pair in collision_preimages
    ):
        raise AssertionError("naive collision no longer reproduces")

    simple_k4_key = tuple((edge, 1) for edge in ((0, 1), *CROSS_EDGES, (2, 3)))
    fixed_union_objects: list[tuple[str, Pair]] = []
    for red in forests:
        for blue in forests:
            if union_multiplicity(red, blue) != simple_k4_key:
                continue
            if valid_positive(red, blue):
                fixed_union_objects.append(("positive", (red, blue)))
            elif valid_negative(red, blue):
                fixed_union_objects.append(("negative", (red, blue)))
    fixed_positive = [
        pair for side, pair in fixed_union_objects if side == "positive"
    ]
    fixed_negative = [
        pair for side, pair in fixed_union_objects if side == "negative"
    ]
    if (len(fixed_positive), len(fixed_negative)) != (2, 4):
        raise AssertionError("fixed-union K4 obstruction changed")

    matching_rows = (
        (((0, 2), (1, 3)), (0, 2), (1, 3)),
        (((0, 3), (1, 2)), (0, 3), (1, 2)),
    )
    repair_map: list[tuple[Pair, Pair]] = []
    for matching, smaller, larger in matching_rows:
        matching_forest = frozenset(matching)
        same_union_positive = (
            frozenset((E, *matching)),
            frozenset((F, *(set(CROSS_EDGES) - set(matching)))),
        )
        doubled_matching_positive = (
            frozenset((E, *matching)),
            frozenset((F, *matching)),
        )
        negative_missing_smaller = (
            frozenset(set(CROSS_EDGES) - {smaller}),
            frozenset((E, F, smaller)),
        )
        negative_missing_larger = (
            frozenset(set(CROSS_EDGES) - {larger}),
            frozenset((E, F, larger)),
        )
        repair_map.extend(
            (
                (negative_missing_smaller, same_union_positive),
                (negative_missing_larger, doubled_matching_positive),
            )
        )
    if {source for source, _ in repair_map} != set(fixed_negative):
        raise AssertionError("K4 repair does not cover the four deficits")
    repair_outputs = [target for _, target in repair_map]
    if len(set(repair_outputs)) != 4:
        raise AssertionError("K4 repair is not injective")
    for source, target in repair_map:
        if not valid_negative(*source) or not valid_positive(*target):
            raise AssertionError("K4 repair side condition failed")
        if not all(is_forest(4, forest) for forest in (*source, *target)):
            raise AssertionError("K4 repair forest condition failed")
        if sum(map(len, source)) != sum(map(len, target)):
            raise AssertionError("K4 repair changed total edge-copy count")
        if set().union(*source) == set() or set().union(*target) == set():
            raise AssertionError("K4 repair lost all active vertices")
        source_vertices = set(itertools.chain.from_iterable(set().union(*source)))
        target_vertices = set(itertools.chain.from_iterable(set().union(*target)))
        if source_vertices != target_vertices:
            raise AssertionError("K4 repair changed the active vertex set")

    grouped_counts: defaultdict[
        tuple[tuple[Edge, int], ...], list[int]
    ] = defaultdict(lambda: [0, 0])
    for red in forests:
        for blue in forests:
            if len(red) + len(blue) != 6:
                continue
            if valid_positive(red, blue):
                grouped_counts[union_multiplicity(red, blue)][0] += 1
            elif valid_negative(red, blue):
                grouped_counts[union_multiplicity(red, blue)][1] += 1
    nonzero_group_rows = [
        [
            [[list(edge), multiplicity] for edge, multiplicity in key],
            counts[0],
            counts[1],
        ]
        for key, counts in sorted(grouped_counts.items())
        if counts[0] != counts[1]
    ]
    differences = [
        positive - negative
        for _, positive, negative in nonzero_group_rows
    ]
    if sorted(differences) != [-2, 1, 1]:
        raise AssertionError("K4 deficit/surplus balance changed")

    collision_row = {
        "total_edge_copies": minimum_size,
        "remaining_degree_k": minimum_size - 2,
        "preimages": [pair_row(pair) for pair in collision_preimages],
        "common_output": pair_row(collision_output),
    }
    fixed_union_row = {
        "union": [[list(edge), multiplicity] for edge, multiplicity in simple_k4_key],
        "positive_count": len(fixed_positive),
        "negative_count": len(fixed_negative),
        "positive_pairs": [pair_row(pair) for pair in sorted(fixed_positive, key=pair_row)],
        "negative_pairs": [pair_row(pair) for pair in sorted(fixed_negative, key=pair_row)],
    }
    repair_rows = [
        {"negative": pair_row(source), "positive": pair_row(target)}
        for source, target in repair_map
    ]
    payload = json.dumps(
        [collision_row, fixed_union_row, nonzero_group_rows, repair_rows],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return {
        "schema": "amra.complete_split.f_leading_swap_obstruction.v1",
        "common_term_cancellation": (
            "After cancelling pairs with E in both forests, the positive "
            "side has E red-only and F blue, while the negative side has "
            "E blue-only and F blue. Recoloring preserves the active "
            "vertex set selected by the base-4 finite difference."
        ),
        "naive_fundamental_cycle_collision": collision_row,
        "fixed_union_k4_obstruction": fixed_union_row,
        "fixed_union_nonzero_balance_rows_at_total_6": nonzero_group_rows,
        "local_k4_repair_rows": repair_rows,
        "next_lemma": (
            "Prove an outside-stable K4 repair lemma: after contracting "
            "common outside components, a saturated alternating K4 "
            "deficit can be sent either to its same-union positive "
            "coloring or to the doubled complementary matching. If the "
            "local replacement creates an outside monochromatic cycle, "
            "continue along its canonical first edge. Termination and "
            "reverse recovery are the remaining requirements."
        ),
        "scope": (
            "The certificates prove that both the naive swap and every "
            "union-preserving alternating-chain injection fail. The "
            "four-row K4 repair is a valid local bijection only when no "
            "outside edges are present; it is a target lemma, not the "
            "general positivity proof."
        ),
        "sha256_payload": hashlib.sha256(payload).hexdigest(),
        "status": "proved_obstruction_and_local_repair_not_general_injection",
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
