from __future__ import annotations

import pytest

from amra.discovery.first_batch_graphs import (
    GRAPH_SEARCH_SPECS,
    _chromatic_number,
    _edge_coloring_exists,
    _edge_mask,
    _hamiltonian_cycles,
    _oriented_counterexample,
    _tree_endomorphisms,
    _triangle_edge_masks,
    _triangle_packing_number,
    _triangle_transversal_number,
    run_graph_search,
)


def test_exact_graph_primitives_have_positive_and_negative_examples() -> None:
    triangle = _edge_mask(3, [(0, 1), (1, 2), (0, 2)])
    path = _edge_mask(3, [(0, 1), (1, 2)])

    assert _chromatic_number(3, triangle) == 3
    assert _chromatic_number(3, path) == 2
    assert len(_hamiltonian_cycles(3, triangle)) == 1
    assert _hamiltonian_cycles(3, path) == []
    assert _edge_coloring_exists(3, triangle, 3, star=False)
    assert not _edge_coloring_exists(3, triangle, 2, star=False)


def test_triangle_optimization_and_tree_dp_are_exact_on_tiny_objects() -> None:
    triangle = _edge_mask(3, [(0, 1), (1, 2), (0, 2)])
    triangle_masks = _triangle_edge_masks(3, triangle)

    assert _triangle_packing_number(triangle_masks) == 1
    assert _triangle_transversal_number(triangle_masks) == 1
    assert _triangle_edge_masks(3, _edge_mask(3, [(0, 1), (1, 2)])) == []

    path_edges = [(0, 1), (1, 2), (2, 3)]
    star_edges = [(0, 1), (0, 2), (0, 3)]
    assert _tree_endomorphisms(4, path_edges) <= _tree_endomorphisms(4, star_edges)


def test_second_neighbourhood_model_accepts_a_directed_triangle() -> None:
    # For n=3, base-3 states 1,2,1 encode 0->1, 2->0, 1->2.
    directed_cycle_code = 1 + 2 * 3 + 1 * 9
    assert _oriented_counterexample(3, directed_cycle_code) is None


def test_checkpoint_can_resume_a_chunked_search() -> None:
    first = run_graph_search("OPG-646", {"max_vertices": 4, "max_cases": 10})
    assert first["status"] == "bounded_search_paused"
    assert first["checkpoint"]["next_case"] == 10

    second = run_graph_search(
        "OPG-646",
        {"max_vertices": 4, "max_cases": 10},
        checkpoint=first["checkpoint"],
    )
    assert second["checkpoint"]["next_case"] == 20
    assert second["checked_cases"] == 10


@pytest.mark.parametrize("problem_id", sorted(GRAPH_SEARCH_SPECS))
def test_all_twelve_searchers_smoke(problem_id: str) -> None:
    spec = GRAPH_SEARCH_SPECS[problem_id]
    bounds = dict(spec["default_bounds"])
    bounds["max_cases"] = 12
    if "max_vertices" in bounds:
        bounds["max_vertices"] = min(bounds["max_vertices"], 4)

    result = run_graph_search(problem_id, bounds)

    assert result["executor_id"].startswith("first_batch.")
    assert result["status"] in {
        "bounded_search_candidate",
        "bounded_search_no_counterexample",
        "bounded_search_paused",
    }
    assert result["outcome"] in {
        "candidate_counterexample",
        "no_candidate_in_bounded_range",
        "paused",
    }
    assert result["deterministic"] is True
    assert result["replayable"] is True
    assert result["model_contract"]["counterexample_condition"]
    assert result["checked_cases"] <= 12


def test_unknown_problem_and_unknown_bound_are_rejected() -> None:
    with pytest.raises(KeyError):
        run_graph_search("missing")
    with pytest.raises(ValueError):
        run_graph_search("OPG-646", {"not_a_bound": 1})
