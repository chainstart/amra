from __future__ import annotations

import json
from pathlib import Path

import pytest

from amra.discovery import opg_uniform_forest_search
from amra.discovery.opg_coloring_search import EdgeGraph
from amra.discovery.opg_uniform_forest_search import (
    ForestEvaluationBudgetExceeded,
    GraphicMatroidForestCounter,
    brute_force_forest_statistics,
    exact_forest_statistics,
    iter_connected_simple_graphs,
    run_uniform_forest_search,
    strongest_edge_pair,
)


def _graph(
    vertex_count: int, edges: tuple[tuple[int, int], ...], encoding: str
) -> EdgeGraph:
    return EdgeGraph(vertex_count, edges, encoding)


def test_exact_known_forest_counts_and_negative_association_margins() -> None:
    path = ((0, 1), (1, 2))
    triangle = ((0, 1), (0, 2), (1, 2))
    complete_four = (
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    )

    path_counts = exact_forest_statistics(3, path)
    assert path_counts.forest_count == 4
    assert path_counts.edge_forest_counts == (2, 2)
    assert path_counts.pair_forest_counts[0][1] == 1
    assert strongest_edge_pair(path_counts).margin == 0

    triangle_counts = exact_forest_statistics(3, triangle)
    assert triangle_counts.forest_count == 7
    assert triangle_counts.edge_forest_counts == (3, 3, 3)
    assert triangle_counts.pair_forest_counts[0][1] == 1
    assert strongest_edge_pair(triangle_counts).margin == 2

    k4_counts = exact_forest_statistics(4, complete_four)
    assert k4_counts.forest_count == 38
    assert k4_counts.edge_forest_counts == (14,) * 6
    assert k4_counts.pair_forest_counts[0][1] == 4
    assert k4_counts.pair_forest_counts[0][5] == 5
    assert strongest_edge_pair(k4_counts).margin == 6


def test_loops_and_parallel_edges_have_graphic_matroid_semantics() -> None:
    loop_and_parallel = ((0, 0), (0, 1), (1, 0))
    exact = exact_forest_statistics(2, loop_and_parallel)
    brute = brute_force_forest_statistics(2, loop_and_parallel)

    assert exact.forest_count == 3
    assert exact.edge_forest_counts == (0, 1, 1)
    assert exact.pair_forest_counts[1][2] == 0
    assert (
        exact.forest_count,
        exact.edge_forest_counts,
        exact.pair_forest_counts,
    ) == (
        brute.forest_count,
        brute.edge_forest_counts,
        brute.pair_forest_counts,
    )

    three_parallel = GraphicMatroidForestCounter(
        2, ((0, 1), (0, 1), (0, 1))
    )
    assert three_parallel.count_after_contracting() == 4
    assert three_parallel.count_after_contracting((0,)) == 1
    assert three_parallel.count_after_contracting((0, 1)) == 0


def test_deletion_contraction_matches_independent_bruteforce_on_all_graphs_n5() -> None:
    for vertex_count in range(6):
        possible_edges = tuple(
            (left, right)
            for right in range(1, vertex_count)
            for left in range(right)
        )
        for mask in range(1 << len(possible_edges)):
            edges = tuple(
                edge
                for index, edge in enumerate(possible_edges)
                if mask & (1 << index)
            )
            exact = exact_forest_statistics(vertex_count, edges)
            brute = brute_force_forest_statistics(vertex_count, edges)
            assert exact.forest_count == brute.forest_count
            assert exact.edge_forest_counts == brute.edge_forest_counts
            assert exact.pair_forest_counts == brute.pair_forest_counts


def test_connected_component_factorization_preserves_pair_margin() -> None:
    triangle_plus_edge = (
        (0, 1),
        (0, 2),
        (1, 2),
        (3, 4),
    )
    counts = exact_forest_statistics(5, triangle_plus_edge)
    assert counts.forest_count == 14

    same_component_left = (
        counts.forest_count * counts.pair_forest_counts[0][1]
    )
    same_component_right = (
        counts.edge_forest_counts[0] * counts.edge_forest_counts[1]
    )
    assert (
        counts.edge_forest_counts[0],
        counts.edge_forest_counts[1],
        counts.pair_forest_counts[0][1],
        same_component_right - same_component_left,
    ) == (6, 6, 2, 8)

    cross_component_left = (
        counts.forest_count * counts.pair_forest_counts[0][3]
    )
    cross_component_right = (
        counts.edge_forest_counts[0] * counts.edge_forest_counts[3]
    )
    assert (
        counts.edge_forest_counts[0],
        counts.edge_forest_counts[3],
        counts.pair_forest_counts[0][3],
        cross_component_right - cross_component_left,
    ) == (6, 7, 3, 0)


def test_state_budget_is_enforced() -> None:
    with pytest.raises(ForestEvaluationBudgetExceeded):
        exact_forest_statistics(
            4,
            (
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 2),
                (1, 3),
                (2, 3),
            ),
            max_states=1,
        )


def test_connected_generator_uses_edge_range_and_shard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands: list[tuple[tuple[str, ...], ...]] = []

    monkeypatch.setattr(
        opg_uniform_forest_search, "locate_tool", lambda name: Path("/geng")
    )

    def pipeline(value):
        commands.append(tuple(tuple(command) for command in value))
        return iter(("Bw",))

    monkeypatch.setattr(opg_uniform_forest_search, "_pipeline", pipeline)
    graphs = list(iter_connected_simple_graphs(9, 19, 36, (2, 4)))
    assert len(graphs) == 1
    assert commands == [
        (("/geng", "-q", "-c", "9", "19:36", "2/4"),)
    ]


def test_search_checkpoint_resumes_without_rechecking_completed_graph(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    triangle = _graph(3, ((0, 1), (0, 2), (1, 2)), "Bw")
    path = _graph(3, ((0, 1), (1, 2)), "Bg")
    generated = 0

    def graphs(*args, **kwargs):
        nonlocal generated
        generated += 1
        yield triangle
        yield path

    monkeypatch.setattr(
        opg_uniform_forest_search, "iter_connected_simple_graphs", graphs
    )
    first = run_uniform_forest_search(
        3,
        2,
        3,
        10.0,
        2.0,
        100_000,
        tmp_path,
        max_cases=1,
        checkpoint_every=1,
    )
    second = run_uniform_forest_search(
        3,
        2,
        3,
        10.0,
        2.0,
        100_000,
        tmp_path,
        checkpoint_every=1,
    )
    events = (tmp_path / "events.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()

    assert first["status"] == "paused_case_budget"
    assert first["next_index"] == 1
    assert second["status"] == "complete"
    assert second["generated"] == 2
    assert second["evaluated"] == 2
    assert generated == 2
    assert len(events) == 2
    assert [json.loads(event)["index"] for event in events] == [0, 1]


def test_zero_wall_budget_does_not_start_generator(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    called = False

    def graphs(*args, **kwargs):
        nonlocal called
        called = True
        return iter(())

    monkeypatch.setattr(
        opg_uniform_forest_search, "iter_connected_simple_graphs", graphs
    )
    state = run_uniform_forest_search(
        3, 2, 3, 0.0, 2.0, 100_000, tmp_path
    )
    assert state["status"] == "paused_wall_budget"
    assert state["generated"] == 0
    assert called is False
