from __future__ import annotations

from itertools import combinations

import pytest

from amra.discovery.opg_uniform_forest_parallel_path_closure import (
    ExactInclusionCounts,
    append_base_only_star_of_size_at_most_one,
    append_endpoint_paths,
    append_parallel_two_edge_path,
    parallel_path_bundle_margin_classes,
    parallel_path_local_pair_margins,
)


def _is_forest(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    subset: int,
) -> bool:
    parent = list(range(vertex_count))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for index, (left, right) in enumerate(edges):
        if not subset & (1 << index):
            continue
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def _exact_counts(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    pair: tuple[int, int],
) -> ExactInclusionCounts:
    categories = [0, 0, 0, 0]
    for subset in range(1 << len(edges)):
        if not _is_forest(vertex_count, edges, subset):
            continue
        e_present = bool(subset & (1 << pair[0]))
        f_present = bool(subset & (1 << pair[1]))
        category = int(e_present) + 2 * int(f_present)
        categories[category] += 1
    return ExactInclusionCounts(
        categories[0],
        categories[1],
        categories[2],
        categories[3],
    )


def test_channel_conversion_and_margin_identity() -> None:
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    counts = ExactInclusionCounts(a, b, c, d)
                    channels = counts.forest_channels
                    assert (
                        ExactInclusionCounts.from_forest_channels(channels)
                        == counts
                    )
                    total, edge_e, edge_f, pair = channels
                    assert counts.margin == (
                        edge_e * edge_f - total * pair
                    )


def test_parallel_path_algebra_scales_the_margin_by_nine() -> None:
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    counts = ExactInclusionCounts(a, b, c, d)
                    assert (
                        append_parallel_two_edge_path(
                            counts, "e"
                        ).margin
                        == 9 * counts.margin
                    )
                    assert (
                        append_parallel_two_edge_path(
                            counts, "f"
                        ).margin
                        == 9 * counts.margin
                    )


def test_closed_multi_path_form_matches_repeated_one_step_maps() -> None:
    seeds = (
        ExactInclusionCounts(1, 1, 1, 0),
        ExactInclusionCounts(7, 11, 13, 5),
        ExactInclusionCounts(19, 2, 3, 17),
    )
    for seed in seeds:
        for e_count in range(6):
            for f_count in range(6):
                repeated = seed
                for _ in range(e_count):
                    repeated = append_parallel_two_edge_path(
                        repeated, "e"
                    )
                for _ in range(f_count):
                    repeated = append_parallel_two_edge_path(
                        repeated, "f"
                    )
                closed = append_endpoint_paths(
                    seed, e_count, f_count
                )
                assert closed == repeated
                assert closed.margin == (
                    9 ** (e_count + f_count) * seed.margin
                )


def test_exhaustive_simple_graphs_through_four_vertices() -> None:
    graph_count = 0
    distinguished_pair_count = 0
    for vertex_count in range(3, 5):
        possible_edges = tuple(combinations(range(vertex_count), 2))
        for graph_mask in range(1 << len(possible_edges)):
            edges = tuple(
                edge
                for index, edge in enumerate(possible_edges)
                if graph_mask & (1 << index)
            )
            if len(edges) < 2:
                continue
            graph_count += 1
            for pair in combinations(range(len(edges)), 2):
                distinguished_pair_count += 1
                counts = _exact_counts(vertex_count, edges, pair)
                for label, edge_index in (
                    ("e", pair[0]),
                    ("f", pair[1]),
                ):
                    left, right = edges[edge_index]
                    augmented_edges = (
                        *edges,
                        (vertex_count, left),
                        (vertex_count, right),
                    )
                    direct = _exact_counts(
                        vertex_count + 1,
                        augmented_edges,
                        pair,
                    )
                    assert direct == append_parallel_two_edge_path(
                        counts, label
                    )
    assert graph_count == 61
    assert distinguished_pair_count == 246


def test_parallel_path_all_six_local_pair_margins_by_direct_enumeration() -> None:
    graph_count = 0
    distinguished_pair_count = 0
    checked_margin_count = 0
    for vertex_count in range(3, 5):
        possible_edges = tuple(combinations(range(vertex_count), 2))
        for graph_mask in range(1 << len(possible_edges)):
            edges = tuple(
                edge
                for index, edge in enumerate(possible_edges)
                if graph_mask & (1 << index)
            )
            if len(edges) < 2:
                continue
            graph_count += 1
            for pair in combinations(range(len(edges)), 2):
                distinguished_pair_count += 1
                counts = _exact_counts(vertex_count, edges, pair)
                left, right = edges[pair[0]]
                augmented_edges = (
                    *edges,
                    (vertex_count, left),
                    (vertex_count, right),
                )
                label_indices = {
                    "e": pair[0],
                    "f": pair[1],
                    "g": len(edges),
                    "h": len(edges) + 1,
                }
                expected = parallel_path_local_pair_margins(counts)
                assert len(expected) == 6
                for labels, expected_margin in expected.items():
                    direct = _exact_counts(
                        vertex_count + 1,
                        augmented_edges,
                        (
                            label_indices[labels[0]],
                            label_indices[labels[1]],
                        ),
                    )
                    assert direct.margin == expected_margin
                    checked_margin_count += 1
                if counts.margin >= 0:
                    assert all(value >= 0 for value in expected.values())
    assert graph_count == 61
    assert distinguished_pair_count == 246
    assert checked_margin_count == 1_476


def test_parallel_path_bundle_closes_every_local_pair_class() -> None:
    distinguished_pair_count = 0
    checked_margin_count = 0
    for vertex_count in range(3, 5):
        possible_edges = tuple(combinations(range(vertex_count), 2))
        for graph_mask in range(1 << len(possible_edges)):
            edges = tuple(
                edge
                for index, edge in enumerate(possible_edges)
                if graph_mask & (1 << index)
            )
            if len(edges) < 2:
                continue
            for pair in combinations(range(len(edges)), 2):
                distinguished_pair_count += 1
                counts = _exact_counts(vertex_count, edges, pair)
                left, right = edges[pair[0]]
                for path_count in (1, 2):
                    augmented_edges = list(edges)
                    path_edge_pairs: list[tuple[int, int]] = []
                    for offset in range(path_count):
                        new_vertex = vertex_count + offset
                        first = len(augmented_edges)
                        augmented_edges.extend(
                            (
                                (new_vertex, left),
                                (new_vertex, right),
                            )
                        )
                        path_edge_pairs.append((first, first + 1))
                    frozen_edges = tuple(augmented_edges)
                    classes = parallel_path_bundle_margin_classes(
                        counts,
                        path_count,
                    )

                    def direct_margin(
                        first_edge: int,
                        second_edge: int,
                    ) -> int:
                        nonlocal checked_margin_count
                        checked_margin_count += 1
                        return _exact_counts(
                            vertex_count + path_count,
                            frozen_edges,
                            (first_edge, second_edge),
                        ).margin

                    assert direct_margin(pair[0], pair[1]) == classes["e_f"]
                    for first, second in path_edge_pairs:
                        assert (
                            direct_margin(pair[0], first)
                            == classes["e_path_edge"]
                        )
                        assert (
                            direct_margin(pair[0], second)
                            == classes["e_path_edge"]
                        )
                        assert (
                            direct_margin(pair[1], first)
                            == classes["f_path_edge"]
                        )
                        assert (
                            direct_margin(pair[1], second)
                            == classes["f_path_edge"]
                        )
                        assert (
                            direct_margin(first, second)
                            == classes["same_path_edges"]
                        )
                    if path_count >= 2:
                        for first in path_edge_pairs[0]:
                            for second in path_edge_pairs[1]:
                                assert direct_margin(first, second) == (
                                    classes["different_path_edges"]
                                )
                    if counts.margin >= 0:
                        assert all(
                            value >= 0 for value in classes.values()
                        )
    assert distinguished_pair_count == 246
    assert checked_margin_count == 5_166


def test_isolated_vertex_and_leaf_star_factors() -> None:
    counts = ExactInclusionCounts(17, 13, 11, 7)
    assert append_base_only_star_of_size_at_most_one(
        counts, 0
    ) == counts
    leaf = append_base_only_star_of_size_at_most_one(counts, 1)
    assert leaf == ExactInclusionCounts(34, 26, 22, 14)
    assert leaf.margin == 4 * counts.margin


def test_invalid_inputs_fail_closed() -> None:
    with pytest.raises(ValueError):
        ExactInclusionCounts(-1, 0, 0, 0)
    with pytest.raises(ValueError):
        ExactInclusionCounts.from_forest_channels((1, 2, 3))
    with pytest.raises(ValueError):
        append_parallel_two_edge_path(
            ExactInclusionCounts(1, 1, 1, 0), "g"
        )
    with pytest.raises(ValueError):
        append_endpoint_paths(
            ExactInclusionCounts(1, 1, 1, 0), -1, 0
        )
    with pytest.raises(ValueError):
        append_base_only_star_of_size_at_most_one(
            ExactInclusionCounts(1, 1, 1, 0), 2
        )
    with pytest.raises(ValueError):
        parallel_path_bundle_margin_classes(
            ExactInclusionCounts(1, 1, 1, 0), 0
        )
