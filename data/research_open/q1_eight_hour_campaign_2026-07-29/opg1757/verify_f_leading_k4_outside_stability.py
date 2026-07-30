#!/usr/bin/env python3
"""Audit the outside-stable saturated-K4 repair for leading F_k."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

from verify_f_leading_swap_obstruction import (
    CROSS_EDGES,
    E,
    F,
    Edge,
    Forest,
    all_forests,
    is_forest,
    union_multiplicity,
    valid_negative,
    valid_positive,
)


TERMINALS = frozenset(range(4))


def component_signature(vertex_count: int, edges: Forest) -> tuple[tuple[int, ...], ...]:
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
            raise AssertionError("component signature received a cycle")
        parent[left_root] = right_root
    components: dict[int, list[int]] = {}
    for vertex in range(vertex_count):
        components.setdefault(root(vertex), []).append(vertex)
    return tuple(sorted(tuple(component) for component in components.values()))


def terminal_excess(vertex_count: int, edges: Forest) -> int:
    return sum(
        max(len(TERMINALS.intersection(component)) - 1, 0)
        for component in component_signature(vertex_count, edges)
    )


def outside_edges(outside_count: int) -> tuple[Edge, ...]:
    vertex_count = 4 + outside_count
    return tuple(
        edge
        for edge in itertools.combinations(range(vertex_count), 2)
        if edge[1] >= 4
    )


def outside_forests(outside_count: int, terminal_tree: Forest) -> tuple[Forest, ...]:
    vertex_count = 4 + outside_count
    candidates = outside_edges(outside_count)
    rows: list[Forest] = []
    for edge_count in range(len(candidates) + 1):
        for selected in itertools.combinations(candidates, edge_count):
            outside = frozenset(selected)
            if is_forest(vertex_count, terminal_tree | outside):
                rows.append(outside)
    return tuple(rows)


def active_mask(outside_count: int, edges: Forest) -> int:
    mask = 0
    for left, right in edges:
        for vertex in (left, right):
            if vertex >= 4:
                mask |= 1 << (vertex - 4)
    return mask


def local_repair_rows() -> tuple[tuple[Forest, Forest, Forest, Forest], ...]:
    rows: list[tuple[Forest, Forest, Forest, Forest]] = []
    for matching in (((0, 2), (1, 3)), ((0, 3), (1, 2))):
        smaller, larger = matching
        matching_forest = frozenset(matching)
        complement = frozenset(set(CROSS_EDGES) - set(matching))
        same_positive_red = frozenset((E, *matching))
        same_positive_blue = frozenset((F, *complement))
        doubled_positive_red = frozenset((E, *matching))
        doubled_positive_blue = frozenset((F, *matching))
        negative_smaller_red = frozenset(set(CROSS_EDGES) - {smaller})
        negative_smaller_blue = frozenset((E, F, smaller))
        negative_larger_red = frozenset(set(CROSS_EDGES) - {larger})
        negative_larger_blue = frozenset((E, F, larger))
        rows.extend(
            (
                (
                    negative_smaller_red,
                    negative_smaller_blue,
                    same_positive_red,
                    same_positive_blue,
                ),
                (
                    negative_larger_red,
                    negative_larger_blue,
                    doubled_positive_red,
                    doubled_positive_blue,
                ),
            )
        )
    return tuple(rows)


def edge_rows(edges: Forest) -> list[list[int]]:
    return [list(edge) for edge in sorted(edges)]


def pair_rows(red: Forest, blue: Forest) -> list[list[list[int]]]:
    return [edge_rows(red), edge_rows(blue)]


def build_audit() -> dict[str, object]:
    repair_rows = local_repair_rows()
    for row in repair_rows:
        if not all(is_forest(4, tree) and len(tree) == 3 for tree in row):
            raise AssertionError("local repair row is not four terminal trees")

    state_rows: list[list[object]] = []
    for outside_count in range(4):
        vertex_count = 4 + outside_count
        full_mask = (1 << outside_count) - 1
        reference_tree = repair_rows[0][0]
        reference_outside = outside_forests(outside_count, reference_tree)
        mask_counts = Counter(
            active_mask(outside_count, outside)
            for outside in reference_outside
        )
        active_pair_count = sum(
            left_count * right_count
            for left_mask, left_count in mask_counts.items()
            for right_mask, right_count in mask_counts.items()
            if left_mask | right_mask == full_mask
        )
        signatures = {
            component_signature(vertex_count, outside)
            for outside in reference_outside
        }

        invalid_replacements = 0
        positive_excess = 0
        for (
            negative_red,
            negative_blue,
            positive_red,
            positive_blue,
        ) in repair_rows:
            red_rows = outside_forests(outside_count, negative_red)
            blue_rows = outside_forests(outside_count, negative_blue)
            if len(red_rows) != len(reference_outside):
                raise AssertionError("terminal-tree extension count changed")
            if len(blue_rows) != len(reference_outside):
                raise AssertionError("terminal-tree extension count changed")
            for outside in red_rows:
                excess = terminal_excess(vertex_count, outside)
                positive_excess += int(excess > 0)
                if excess != 0:
                    raise AssertionError("source forest allows terminal excess")
                if not is_forest(vertex_count, positive_red | outside):
                    invalid_replacements += 1
            for outside in blue_rows:
                excess = terminal_excess(vertex_count, outside)
                positive_excess += int(excess > 0)
                if excess != 0:
                    raise AssertionError("source forest allows terminal excess")
                if not is_forest(vertex_count, positive_blue | outside):
                    invalid_replacements += 1
        if invalid_replacements or positive_excess:
            raise AssertionError("outside-stable replacement failed")

        state_rows.append(
            [
                outside_count,
                len(outside_edges(outside_count)),
                len(reference_outside),
                len(signatures),
                active_pair_count,
                invalid_replacements,
                positive_excess,
                [
                    [mask, count]
                    for mask, count in sorted(mask_counts.items())
                ],
            ]
        )

    inverse_rows: list[list[object]] = []
    targets: set[tuple[Forest, Forest]] = set()
    for (
        negative_red,
        negative_blue,
        positive_red,
        positive_blue,
    ) in repair_rows:
        target = (positive_red, positive_blue)
        if target in targets:
            raise AssertionError("local target does not identify its inverse")
        targets.add(target)
        inverse_rows.append(
            [
                edge_rows(positive_red),
                edge_rows(positive_blue),
                edge_rows(negative_red),
                edge_rows(negative_blue),
            ]
        )

    five_vertex_forests = all_forests(5)
    grouped: dict[
        tuple[tuple[Edge, int], ...], list[list[tuple[Forest, Forest]]]
    ] = {}
    for red in five_vertex_forests:
        for blue in five_vertex_forests:
            if not valid_positive(red, blue) and not valid_negative(red, blue):
                continue
            if 4 not in set(itertools.chain.from_iterable(red | blue)):
                continue
            key = union_multiplicity(red, blue)
            groups = grouped.setdefault(key, [[], []])
            groups[0 if valid_positive(red, blue) else 1].append((red, blue))
    deficits = [
        (key, groups)
        for key, groups in grouped.items()
        if len(groups[1]) > len(groups[0])
    ]
    if not deficits:
        raise AssertionError("expected five-vertex global routing deficits")
    minimum_total = min(
        sum(multiplicity for _, multiplicity in key)
        for key, _ in deficits
    )
    if minimum_total != 7:
        raise AssertionError("minimal active outside deficit size changed")
    terminal_edges = set(itertools.combinations(range(4), 2))
    nonsaturated = [
        (key, groups)
        for key, groups in deficits
        if not all(dict(key).get(edge) == 1 for edge in terminal_edges)
    ]
    minimum_nonsaturated_total = min(
        sum(multiplicity for _, multiplicity in key)
        for key, _ in nonsaturated
    )
    if minimum_nonsaturated_total != 7:
        raise AssertionError("minimal nonsaturated deficit size changed")
    selected_key, selected_groups = min(
        (
            (key, groups)
            for key, groups in nonsaturated
            if sum(multiplicity for _, multiplicity in key)
            == minimum_nonsaturated_total
        ),
        key=lambda row: row[0],
    )
    selected_edges = {edge for edge, multiplicity in selected_key if multiplicity}
    outside_neighbors = {
        left if right == 4 else right
        for left, right in selected_edges
        if 4 in (left, right)
    }
    missing_terminal_edges = terminal_edges - selected_edges
    if len(outside_neighbors) != 2 or missing_terminal_edges != {
        tuple(sorted(outside_neighbors))
    }:
        raise AssertionError("minimal deficit is no longer a subdivided K4")
    if any(multiplicity != 1 for _, multiplicity in selected_key):
        raise AssertionError("minimal subdivided-K4 union gained multiplicity")
    subdivided_row = {
        "q": 1,
        "total_edge_copies": minimum_nonsaturated_total,
        "remaining_degree_k": minimum_nonsaturated_total - 2,
        "union": [
            [list(edge), multiplicity]
            for edge, multiplicity in selected_key
        ],
        "suppressed_edge": list(tuple(sorted(outside_neighbors))),
        "positive_count": len(selected_groups[0]),
        "negative_count": len(selected_groups[1]),
        "positive_pairs": [
            pair_rows(red, blue)
            for red, blue in sorted(selected_groups[0], key=lambda pair: pair_rows(*pair))
        ],
        "negative_pairs": [
            pair_rows(red, blue)
            for red, blue in sorted(selected_groups[1], key=lambda pair: pair_rows(*pair))
        ],
    }
    if (
        subdivided_row["positive_count"],
        subdivided_row["negative_count"],
    ) != (10, 12):
        raise AssertionError("subdivided-K4 deficit counts changed")

    payload = json.dumps(
        [state_rows, inverse_rows, subdivided_row],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return {
        "schema": "amra.complete_split.f_leading_k4_outside_stability.v1",
        "terminal_tree_replacement_lemma": (
            "Let S be the four terminals, T and T' trees on S, and H "
            "contain no terminal-terminal edge. If T union H is a "
            "forest, every component of H meets S in at most one vertex: "
            "otherwise its terminal path plus the T path is a cycle. "
            "Consequently T' union H is also a forest."
        ),
        "chain_potential": (
            "mu(H)=sum_components max(|component intersect S|-1,0). "
            "Source acyclicity forces mu=0. Hence the proposed external "
            "alternating chain terminates before its first step; no "
            "outside monochromatic cycle can be created by replacing "
            "one terminal tree with another."
        ),
        "state_rows_q0_to_q3": state_rows,
        "inverse_rows": inverse_rows,
        "inverse_rule": (
            "The four positive terminal restrictions are distinct. A "
            "simple-K4 target identifies its matching from the red tree "
            "and inverts to the source missing the smaller matching edge; "
            "a doubled-matching target inverts to the source missing the "
            "larger edge. All outside edges are left fixed."
        ),
        "minimal_uncovered_subdivided_k4": subdivided_row,
        "five_vertex_active_fixed_union_deficit_count": len(deficits),
        "next_lemma": (
            "Series-subdivision K4 repair: when one terminal edge of the "
            "saturated K4 is replaced by a monochromatic/mixed two-edge "
            "path through the first active outside vertex, suppress that "
            "vertex with a reversible path-color tag, apply the K4 "
            "repair, and expand it back. The displayed q=1,k=5 union has "
            "12 negative versus 10 positive colorings and is the first "
            "uncovered state."
        ),
        "scope": (
            "This proves the outside-stable repair for the saturated "
            "simple-K4 deficit class, for arbitrarily many outside "
            "vertices. It is not yet an injection for all negative "
            "forest pairs; other terminal multiplicity patterns still "
            "need a disjoint global routing rule."
        ),
        "sha256_payload": hashlib.sha256(payload).hexdigest(),
        "status": "proved_outside_stable_local_lemma_not_global_positivity",
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
