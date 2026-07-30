from __future__ import annotations

import json
from pathlib import Path

import pytest

from amra.discovery import opg_uniform_forest_analysis
from amra.discovery.opg_coloring_search import EdgeGraph
from amra.discovery.opg_uniform_forest_analysis import (
    analyze_biconnected_sample,
    analyze_strict_pairs,
    biconnected_edge_blocks,
    iter_biconnected_simple_graphs,
    main,
)
from amra.discovery.opg_uniform_forest_search import (
    exact_forest_statistics,
    strongest_edge_pair,
)


def test_equality_pairs_no_longer_hide_strict_pairs() -> None:
    triangle_with_bridge = EdgeGraph(
        4,
        ((0, 1), (0, 2), (1, 2), (2, 3)),
        "Cw",
    )
    production_best = strongest_edge_pair(
        exact_forest_statistics(
            triangle_with_bridge.vertex_count,
            triangle_with_bridge.edges,
        )
    )
    analysis = analyze_strict_pairs(triangle_with_bridge, top_k=3)

    assert production_best.margin == 0
    assert analysis["edge_block_count"] == 2
    assert analysis["pair_count"] == 6
    assert analysis["equality_pair_count"] == 3
    assert analysis["structural_equality_pair_count"] == 3
    assert analysis["within_block_equality_pair_count"] == 0
    assert analysis["strict_pair_count"] == 3
    assert len(analysis["top_strict_pairs"]) == 3
    assert all(
        pair["left_product"] < pair["right_product"]
        for pair in analysis["top_strict_pairs"]
    )
    assert all(
        3 not in pair["edge_indexes"]
        for pair in analysis["top_strict_pairs"]
    )


def test_strict_pairs_are_sorted_by_exact_ratio() -> None:
    complete_four = EdgeGraph(
        4,
        (
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (2, 3),
        ),
        "C~",
    )
    analysis = analyze_strict_pairs(complete_four, top_k=3)

    assert analysis["edge_block_count"] == 1
    assert analysis["equality_pair_count"] == 0
    assert analysis["strict_pair_count"] == 15
    assert [pair["margin"] for pair in analysis["top_strict_pairs"]] == [
        6,
        6,
        6,
    ]
    assert {
        tuple(pair["edge_indexes"])
        for pair in analysis["top_strict_pairs"]
    } == {(0, 5), (1, 4), (2, 3)}


def test_biconnected_edge_blocks_separate_two_cycles_at_a_cut_vertex() -> None:
    figure_eight = EdgeGraph(
        5,
        (
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 3),
            (2, 4),
            (3, 4),
        ),
        "figure-eight",
    )
    labels = biconnected_edge_blocks(figure_eight)
    assert len(set(labels)) == 2
    assert len(set(labels[:3])) == 1
    assert len(set(labels[3:])) == 1
    assert labels[0] != labels[3]


def test_biconnected_generator_uses_geng_capital_c(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands: list[tuple[tuple[str, ...], ...]] = []
    monkeypatch.setattr(
        opg_uniform_forest_analysis, "locate_tool", lambda name: Path("/geng")
    )

    def pipeline(value):
        commands.append(tuple(tuple(command) for command in value))
        return iter(("Bw",))

    monkeypatch.setattr(opg_uniform_forest_analysis, "_pipeline", pipeline)
    graphs = list(iter_biconnected_simple_graphs(9, 19, 19, (1, 4)))
    assert len(graphs) == 1
    assert commands == [
        (("/geng", "-q", "-C", "9", "19:19", "1/4"),)
    ]


def test_single_graph_cli_outputs_requested_top_k(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["--graph6", "C~", "--top-k", "2"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["mode"] == "single_graph"
    assert payload["graph6"] == "C~"
    assert len(payload["top_strict_pairs"]) == 2


def test_sample_global_top_uses_exact_cross_graph_integer_ranking(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    first_graph = EdgeGraph(3, ((0, 1), (1, 2)), "first")
    second_graph = EdgeGraph(3, ((0, 1), (1, 2)), "second")
    scale = 10**30

    monkeypatch.setattr(
        opg_uniform_forest_analysis,
        "iter_biconnected_simple_graphs",
        lambda *args, **kwargs: iter((first_graph, second_graph)),
    )

    def analyze(graph: EdgeGraph, **kwargs):
        if graph.encoding == "first":
            left, right = scale - 1, scale
        else:
            left, right = scale - 2, scale - 1
        return {
            "graph6": graph.encoding,
            "vertices": graph.vertex_count,
            "edges": len(graph.edges),
            "edge_block_count": 1,
            "pair_count": 1,
            "strict_pair_count": 1,
            "equality_pair_count": 0,
            "structural_equality_pair_count": 0,
            "within_block_equality_pair_count": 0,
            "violation_pair_count": 0,
            "states": 1,
            "elapsed_seconds": 0.0,
            "top_strict_pairs": [
                {
                    "edge_indexes": [0, 1],
                    "edge_e": [0, 1],
                    "edge_f": [1, 2],
                    "block_ids": [0, 0],
                    "forest_count": 1,
                    "forest_count_e": 1,
                    "forest_count_f": 1,
                    "forest_count_ef": 1,
                    "left_product": left,
                    "right_product": right,
                    "margin": right - left,
                    "left_over_right": "float-display-is-not-used",
                    "relative_gap": "float-display-is-not-used",
                }
            ],
        }

    monkeypatch.setattr(
        opg_uniform_forest_analysis, "analyze_strict_pairs", analyze
    )
    result = analyze_biconnected_sample(
        9,
        19,
        19,
        max_cases=2,
        top_k=2,
        timeout_seconds=1.0,
        max_states=100,
    )

    assert [
        (item["index"], item["graph6"])
        for item in result["global_top_strict_pairs"]
    ] == [(0, "first"), (1, "second")]
    assert result["global_top_strict_pairs"][0]["graph_pair_rank"] == 1
