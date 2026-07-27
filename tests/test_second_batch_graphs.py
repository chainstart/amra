from __future__ import annotations

import itertools
import json
import random
import time
from pathlib import Path

import pytest
import yaml

import amra.discovery.second_batch_graphs as graph_search
from amra.discovery.second_batch_graphs import (
    SECOND_BATCH_GRAPH_SPECS,
    UNREGISTERED_SECOND_BATCH_GRAPH_IDS,
    Graph,
    _decode_graph6,
    _iter_targeted_graphs,
    run_second_batch_graph_search,
)


def _budget(*, max_cases: int = 1, max_vertices: int = 3) -> dict:
    return {
        "time_seconds": 10,
        "max_cases": max_cases,
        "parameters": {"max_vertices": max_vertices},
    }


def test_graph6_decoder_uses_nauty_edge_order() -> None:
    graph = _decode_graph6("Bw")
    assert graph.n == 3
    assert set(graph.edges) == {(0, 1), (0, 2), (1, 2)}


def test_registry_is_frozen_and_matches_source_bank() -> None:
    assert isinstance(SECOND_BATCH_GRAPH_SPECS, tuple)
    assert len(SECOND_BATCH_GRAPH_SPECS) == 32
    bank_path = Path(__file__).parents[1] / "data/banks/unsolvedmath_open_non_erdos.yaml"
    bank = {
        row["problem_id"]: row
        for row in yaml.safe_load(bank_path.read_text(encoding="utf-8"))
    }
    for spec in SECOND_BATCH_GRAPH_SPECS:
        source = bank[spec["problem_id"]]
        assert source["metadata"]["source_id"] == spec["source_id"]
        assert source["title"] == spec["title"]
        assert spec["model_contract"]["premise"]
        assert spec["model_contract"]["conclusion"]
        assert spec["deep_bounds"]["max_vertices"] <= spec["supported_max_vertices"]
        assert spec["claim_scope"] in {
            "full_claim",
            "explicit_subclaim",
            "restricted_family",
            "witness_search",
        }
        assert spec["scope_limitation"]
        assert "same-executor replay" in spec["model_contract"]["acceptance"]
        assert "not independent verification" in spec["model_contract"]["acceptance"]

    restricted = {
        spec["source_id"]
        for spec in SECOND_BATCH_GRAPH_SPECS
        if spec["claim_scope"] == "restricted_family"
    }
    assert restricted == {
        "OPG-127",
        "OPG-412",
        "OPG-37182",
        "OPG-60001",
    }
    registered_source_ids = {
        spec["source_id"] for spec in SECOND_BATCH_GRAPH_SPECS
    }
    assert {
        "OPG-412",
        "OPG-729",
        "OPG-1757",
        "OPG-638",
        "OPG-60039",
    } <= registered_source_ids
    assert not {
        "OPG-130",
        "OPG-2226",
        "OPG-2242",
        "OPG-824",
        "OPG-46432",
    } & registered_source_ids
    for source_id in {"OPG-1757", "OPG-638", "OPG-60039"}:
        spec = next(
            spec
            for spec in SECOND_BATCH_GRAPH_SPECS
            if spec["source_id"] == source_id
        )
        assert spec["claim_scope"] == "full_claim"
        assert spec["source_statement"]
        assert spec["model_contract"]["source_statement"]
    weak_pentagon = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-434"
    )
    assert weak_pentagon["claim_scope"] == "explicit_subclaim"
    assert "properness is not imposed" in weak_pentagon["model_contract"]["conclusion"]
    clique_coloring = next(
        spec
        for spec in SECOND_BATCH_GRAPH_SPECS
        if spec["source_id"] == "OPG-56230"
    )
    assert "at least one edge" in clique_coloring["model_contract"]["premise"]
    edge_reconstruction = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-804"
    )
    assert edge_reconstruction["supports_deep"] is True
    assert edge_reconstruction["deep_strategies"] == ["deep-exact"]
    assert edge_reconstruction["deep_launches"] == 1
    assert (
        edge_reconstruction["deep_search_role"]
        == "complete_nonisomorphic_graph_enumeration"
    )
    uniform_forest = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-1757"
    )
    assert "distinct" not in uniform_forest["source_statement"].lower()
    assert "distinct" in uniform_forest["model_contract"]["premise"].lower()
    assert "distinct" in uniform_forest["scope_limitation"].lower()
    assert (
        uniform_forest["deep_search_role"]
        == "dense_nine_vertex_frontier_sampling"
    )
    assert (
        uniform_forest["frontier_provenance"][
            "known_verified_edge_ceiling_at_nine"
        ]
        == 18
    )
    jones = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-638"
    )
    assert jones["deep_launches"] == 1
    assert jones["deep_bounds"]["max_vertices"] == 9
    assert (
        jones["deep_search_role"]
        == "complete_nonisomorphic_planar_enumeration"
    )
    assert (
        jones["frontier_provenance"][
            "deep_planar_graph_count_through_order_nine"
        ]
        == 87_834
    )
    sidorenko = next(
        spec
        for spec in SECOND_BATCH_GRAPH_SPECS
        if spec["source_id"] == "OPG-60039"
    )
    assert (
        sidorenko["deep_search_role"]
        == "known_family_filtered_bipartite_source_sampling"
    )
    odd_cycle = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-412"
    )
    assert odd_cycle["deep_bounds"]["k_values"] == [2, 3, 4, 5]
    assert odd_cycle["deep_bounds"]["max_vertices"] == 40
    assert odd_cycle["deep_launches"] == 1
    assert (
        odd_cycle["frontier_provenance"][
            "deep_structural_corpus_size_at_order_40"
        ]
        == 2_584
    )
    assert odd_cycle["frontier_provenance"]["excluded_settled_k_values"] == [1]
    seagull = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-729"
    )
    assert seagull["deep_bounds"]["max_vertices"] == 16
    assert seagull["deep_launches"] == 1
    assert seagull["frontier_provenance"]["known_positive_order_ceiling"] == 12
    assert (
        seagull["frontier_provenance"]["deep_canonical_corpus_size"]
        == 25_706
    )


@pytest.mark.parametrize(
    "problem_id",
    sorted(spec["problem_id"] for spec in SECOND_BATCH_GRAPH_SPECS),
)
def test_every_registered_exact_strategy_smoke(problem_id: str) -> None:
    result = run_second_batch_graph_search(
        problem_id,
        strategy_id="exact-small",
        budget=_budget(),
        seed=20260727,
    )

    assert result["outcome"] in {"candidate", "no_candidate", "inconclusive"}
    assert result["checked_cases"] <= 1
    assert result["stop_reason"]
    assert result["checkpoint"]["next_case"] >= 0
    assert result["model_contract"]["counterexample"]
    assert result["tool_versions"]["python"]


def test_targeted_search_is_seed_deterministic_and_never_claims_exhaustion() -> None:
    first = run_second_batch_graph_search(
        "OPG-335",
        strategy_id="targeted",
        budget=_budget(max_cases=5, max_vertices=5),
        seed=17,
    )
    second = run_second_batch_graph_search(
        "OPG-335",
        strategy_id="targeted",
        budget=_budget(max_cases=5, max_vertices=5),
        seed=17,
    )

    assert first == second
    assert first["outcome"] in {"candidate", "inconclusive"}
    if first["outcome"] == "inconclusive":
        assert first["stop_reason"] in {
            "max_cases_exhausted",
            "targeted_sample_exhausted",
        }
    assert first["metrics"]["generated_cases"] == first["checked_cases"]


def test_targeted_mixture_changes_with_launch_seed() -> None:
    spec = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-335"
    )
    first = [
        (graph.n, graph.mask)
        for graph in _iter_targeted_graphs(spec, 7, seed=17, count=20)
    ]
    second = [
        (graph.n, graph.mask)
        for graph in _iter_targeted_graphs(spec, 7, seed=18, count=20)
    ]
    assert first != second


def test_odd_cycle_deep_crosses_multiple_k_frontiers_and_resumes() -> None:
    spec = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-412"
    )
    graphs = list(
        _iter_targeted_graphs(spec, 40, seed=17, count=16)
    )
    for graph in graphs:
        eligible = [
            k
            for k in (2, 3, 4, 5)
            if graph.n >= 6 * k and graph_search._girth(graph) >= 4 * k
        ]
        assert eligible
        assert graph_search._is_planar(graph)
        assert not graph_search._is_bipartite(graph)
        assert graph_search._semantic_premise_check(
            spec, graph, spec["deep_bounds"]
        )
    resumed = list(
        _iter_targeted_graphs(spec, 40, seed=17, count=5, start=11)
    )
    assert resumed == graphs[11:16]

    result = run_second_batch_graph_search(
        spec["problem_id"],
        strategy_id="deep-diversified",
        budget={
            "time_seconds": 10,
            "max_cases": 16,
            "parameters": {"max_vertices": 40},
        },
        seed=17,
    )
    assert result["checked_cases"] == 16
    assert result["metrics"]["premise_cases"] == 16
    assert result["metrics"]["frontier_premise_cases"] == 16
    assert result["metrics"]["known_frontier_exceeded"] is True


def test_seagull_deep_uses_triangle_free_complements_beyond_order_twelve() -> None:
    spec = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-729"
    )
    groups = graph_search._seagull_canonical_groups(16)
    assert [len(group) for group in groups] == [16_988, 5_072, 2_854, 792]
    graphs = list(
        _iter_targeted_graphs(spec, 16, seed=17, count=12)
    )
    assert {graph.n for graph in graphs} == {13, 14, 15, 16}
    for graph in graphs:
        assert not graph_search._has_independent_triple(graph)
        complement = graph_search._complement_graph(graph)
        assert not any(
            complement.adjacency[left] & complement.adjacency[right]
            for left, right in complement.edges
        )

    result = run_second_batch_graph_search(
        spec["problem_id"],
        strategy_id="deep-diversified",
        budget={
            "time_seconds": 10,
            "max_cases": 1,
            "parameters": {"max_vertices": 16},
        },
        seed=17,
    )
    assert result["checked_cases"] == 1
    assert result["metrics"]["premise_cases"] == 1
    assert result["metrics"]["frontier_premise_cases"] == 1
    assert result["metrics"]["known_frontier_exceeded"] is True


def test_shallow_minor_fast_path_only_accepts_valid_branch_models() -> None:
    cycle_five = graph_search._cycle_graph(5)
    path_five = Graph(
        5,
        graph_search._mask_from_edges(
            5, [(0, 1), (1, 2), (2, 3), (3, 4)]
        ),
    )
    complete_four = graph_search._complete_graph(4)
    assert graph_search._has_shallow_complete_minor(cycle_five, 3)
    assert graph_search._has_complete_minor(cycle_five, 3)
    assert not graph_search._has_shallow_complete_minor(path_five, 3)
    assert not graph_search._has_complete_minor(path_five, 3)
    assert graph_search._has_shallow_complete_minor(complete_four, 4)
    assert not graph_search._has_complete_minor(complete_four, 5)


@pytest.mark.parametrize("source_id", ["OPG-1757", "OPG-638"])
def test_new_single_graph_targeted_corpora_change_with_seed(
    source_id: str,
) -> None:
    spec = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == source_id
    )
    first = [
        (graph.n, len(graph.edges))
        for graph in _iter_targeted_graphs(
            spec, spec["deep_bounds"]["max_vertices"], seed=17, count=20
        )
    ]
    second = [
        (graph.n, len(graph.edges))
        for graph in _iter_targeted_graphs(
            spec, spec["deep_bounds"]["max_vertices"], seed=18, count=20
        )
    ]
    assert first != second


def test_uniform_forest_deep_starts_beyond_the_old_edge_frontier() -> None:
    spec = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-1757"
    )
    graphs = list(
        _iter_targeted_graphs(spec, 9, seed=3, count=20)
    )
    graphs.extend(
        _iter_targeted_graphs(
            spec, 9, seed=3, count=20, start=100_000
        )
    )
    assert all(graph.n == 9 for graph in graphs)
    assert all(19 <= len(graph.edges) <= 22 for graph in graphs)

    started = time.monotonic()
    result = run_second_batch_graph_search(
        spec["problem_id"],
        strategy_id="deep-diversified",
        budget={
            "time_seconds": 1,
            "max_cases": 1,
            "parameters": {"max_vertices": 9},
        },
        seed=3,
    )
    assert time.monotonic() - started < 2
    assert result["stop_reason"] == "predicate_time_budget_exhausted"
    assert result["checked_cases"] == 0
    assert result["checkpoint"]["next_case"] == 0
    assert result["metrics"]["max_graph_order_seen"] == 9
    assert result["metrics"]["max_graph_edge_count_seen"] > 18
    assert result["metrics"]["known_frontier_exceeded"] is True


def test_uniform_forest_deep_advances_within_production_budget() -> None:
    spec = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-1757"
    )
    seed = next(
        candidate
        for candidate in range(100)
        if len(
            next(iter(_iter_targeted_graphs(spec, 9, candidate, 1))).edges
        )
        == 19
    )
    started = time.monotonic()
    result = run_second_batch_graph_search(
        spec["problem_id"],
        strategy_id="deep-diversified",
        budget={
            "time_seconds": 300,
            "max_cases": 1,
            "parameters": {"max_vertices": 9},
        },
        seed=seed,
    )
    assert time.monotonic() - started < 10
    assert result["checked_cases"] == 1
    assert result["checkpoint"]["next_case"] == 1


def test_planar_targeted_corpus_is_canonically_diverse() -> None:
    spec = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-638"
    )
    graphs = list(
        _iter_targeted_graphs(spec, 8, seed=17, count=500)
    )
    canonical = [
        graph_search._canonical_graph6(graph)
        for graph in graphs
    ]
    assert len(graphs) == 500
    assert len(set(canonical[:100])) == 100
    assert len(set(canonical)) == 500
    assert {
        graph_search._planar_target_family(graph)
        for graph in graphs
    } == {
        "triangulation",
        "quadrangulation",
        "clique_sum_or_gadget",
        "feedback_pressure",
        "general_planar",
    }
    other = [
        graph_search._canonical_graph6(graph)
        for graph in _iter_targeted_graphs(
            spec, 8, seed=18, count=100
        )
    ]
    assert canonical[:100] != other


def test_planar_deep_exhausts_one_resumable_nine_vertex_corpus() -> None:
    spec = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == "OPG-638"
    )
    corpus = graph_search._planar_targeted_corpus(9, 17)
    assert len(corpus) == 87_834
    assert sum(graph.n == 9 for graph in corpus) == 79_853
    segment = list(
        _iter_targeted_graphs(spec, 9, seed=17, count=10, start=50_000)
    )
    resumed = list(
        _iter_targeted_graphs(spec, 9, seed=17, count=5, start=50_005)
    )
    assert resumed == segment[5:]
    assert any(graph.n == 9 for graph in segment)


def test_sidorenko_targeted_pair_corpus_changes_with_seed() -> None:
    first = [
        (
            graph_search._canonical_graph6(source),
            target.n,
            len(target.edges),
        )
        for source, target in graph_search._iter_sidorenko_targeted_pairs(
            12, 6, seed=17, count=20
        )
    ]
    second = [
        (
            graph_search._canonical_graph6(source),
            target.n,
            len(target.edges),
        )
        for source, target in graph_search._iter_sidorenko_targeted_pairs(
            12, 6, seed=18, count=20
        )
    ]
    assert first != second


def test_sidorenko_deep_prioritizes_nontrivial_connected_bipartite_sources() -> None:
    pairs = list(
        graph_search._iter_sidorenko_targeted_pairs(
            12, 6, seed=17, count=100
        )
    )
    sources = [source for source, _target in pairs]
    for source in sources:
        sides = graph_search._bipartition_sizes(source)
        assert source.n >= 10
        assert graph_search._connected(source)
        assert graph_search._is_bipartite(source)
        assert sides is not None and sides[0] >= 5
        assert len(source.edges) - source.n + 1 >= 3
        assert len(set(row.bit_count() for row in source.adjacency)) >= 3
        assert graph_search._sidorenko_filtered_family(source) is None
    assert sum(source.n in {10, 11} for source in sources) >= 80
    canonical = {
        graph_search._canonical_graph6(source)
        for source in sources
    }
    assert len(canonical) >= 95


def test_sidorenko_filters_universal_to_opposite_known_family() -> None:
    edges = [(0, right) for right in range(5, 10)]
    edges.extend(
        (
            (1, 5),
            (1, 6),
            (2, 6),
            (2, 7),
            (3, 7),
            (3, 8),
            (4, 8),
            (4, 9),
        )
    )
    source = Graph(10, graph_search._mask_from_edges(10, edges))
    assert graph_search._sidorenko_has_universal_to_opposite(source)
    assert (
        graph_search._sidorenko_filtered_family(source)
        == "universal_to_opposite"
    )
    assert not graph_search._sidorenko_known_frontier_exceeded(source)


def _brute_homomorphism_count(source: Graph, target: Graph) -> int:
    return sum(
        all(
            target.adjacency[images[left]] & (1 << images[right])
            for left, right in source.edges
        )
        for images in itertools.product(range(target.n), repeat=source.n)
    )


def test_bipartite_homomorphism_count_matches_bruteforce() -> None:
    rng = random.Random(20260727)
    cases = [
        (Graph(0, 0), Graph(0, 0)),
        (Graph(3, 0), graph_search._complete_graph(3)),
        (graph_search._cycle_graph(4), graph_search._cycle_graph(3)),
        (graph_search._cycle_graph(3), graph_search._complete_graph(4)),
    ]
    for _ in range(50):
        source_order = rng.randrange(5)
        target_order = rng.randrange(5)
        source = Graph(
            source_order,
            rng.randrange(1 << len(graph_search._edge_pairs(source_order))),
        )
        target = Graph(
            target_order,
            rng.randrange(1 << len(graph_search._edge_pairs(target_order))),
        )
        cases.append((source, target))
    for source, target in cases:
        assert graph_search._homomorphism_count(
            source, target
        ) == _brute_homomorphism_count(source, target)


def test_sidorenko_twelve_vertex_exact_count_finishes_quickly() -> None:
    source, _ = next(
        iter(
            graph_search._iter_sidorenko_targeted_pairs(
                12, 6, seed=17, count=1, start=19
            )
        )
    )
    target = graph_search._complete_graph(6)
    started = time.monotonic()
    with graph_search._predicate_budget(started + 5):
        count = graph_search._homomorphism_count(source, target)
    assert count >= 0
    assert time.monotonic() - started < 5


def test_sidorenko_deep_records_separate_h_and_g_frontiers() -> None:
    result = run_second_batch_graph_search(
        "OPG-60039",
        strategy_id="deep-diversified",
        budget={
            "time_seconds": 1,
            "max_cases": 1,
            "parameters": {"max_vertices": 6},
        },
        seed=17,
    )
    assert result["metrics"]["max_h_order_seen"] >= 10
    assert result["metrics"]["max_g_order_seen"] <= 6
    assert result["metrics"]["known_frontier_exceeded"] is True
    assert result["metrics"]["filtered_family_source_cases"] == 0
    assert result["metrics"]["general_source_cases"] == 1


def test_targeted_cubic_search_records_premise_efficiency() -> None:
    result = run_second_batch_graph_search(
        "OPG-543",
        strategy_id="targeted",
        budget=_budget(max_cases=6, max_vertices=10),
        seed=29,
    )
    assert result["metrics"]["generated_cases"] == result["checked_cases"]
    assert result["metrics"]["premise_cases"] > 0


@pytest.mark.parametrize("source_id", ["OPG-37182", "OPG-385", "OPG-434"])
def test_specialized_cubic_families_vary_up_to_isomorphism_by_seed(
    source_id: str,
) -> None:
    spec = next(
        spec for spec in SECOND_BATCH_GRAPH_SPECS if spec["source_id"] == source_id
    )
    first_orders = [
        graph.n
        for graph in _iter_targeted_graphs(
            spec, spec["deep_bounds"]["max_vertices"], seed=1, count=5
        )
    ]
    second_orders = [
        graph.n
        for graph in _iter_targeted_graphs(
            spec, spec["deep_bounds"]["max_vertices"], seed=2, count=5
        )
    ]
    assert first_orders != second_orders


def test_predicate_timeout_does_not_advance_checkpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def slow_coloring(_graph: Graph) -> bool:
        while True:
            graph_search._check_predicate_deadline()

    monkeypatch.setattr(graph_search, "_weak_pentagon_coloring", slow_coloring)
    started = time.monotonic()
    result = run_second_batch_graph_search(
        "OPG-434",
        strategy_id="targeted",
        budget={
            "time_seconds": 1,
            "max_cases": 20,
            "parameters": {"max_vertices": 12},
        },
        seed=20260727,
    )
    elapsed = time.monotonic() - started

    assert result["outcome"] == "inconclusive"
    assert result["stop_reason"] == "predicate_time_budget_exhausted"
    assert result["checked_cases"] == 0
    assert result["checkpoint"]["next_case"] == 0
    assert result["metrics"]["generated_cases"] == 1
    assert elapsed < 2


def test_sidorenko_timeout_does_not_advance_pair_checkpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def slow_violation(_source: Graph, _target: Graph) -> None:
        while True:
            graph_search._check_predicate_deadline()

    monkeypatch.setattr(graph_search, "_sidorenko_violation", slow_violation)
    started = time.monotonic()
    result = run_second_batch_graph_search(
        "OPG-60039",
        strategy_id="deep-diversified",
        budget={
            "time_seconds": 1,
            "max_cases": 20,
            "parameters": {"max_vertices": 6},
        },
        seed=20260727,
    )
    assert time.monotonic() - started < 2
    assert result["outcome"] == "inconclusive"
    assert result["stop_reason"] == "predicate_time_budget_exhausted"
    assert result["checked_cases"] == 0
    assert result["checkpoint"]["next_case"] == 0


def test_predicate_timeout_does_not_leak_deadline_to_next_check(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def slow_violation(_source: Graph, _target: Graph) -> None:
        while True:
            graph_search._check_predicate_deadline()

    monkeypatch.setattr(graph_search, "_sidorenko_violation", slow_violation)
    result = run_second_batch_graph_search(
        "OPG-60039",
        strategy_id="deep-diversified",
        budget={
            "time_seconds": 1,
            "max_cases": 1,
            "parameters": {"max_vertices": 6},
        },
        seed=20260727,
    )
    assert result["stop_reason"] == "predicate_time_budget_exhausted"
    assert graph_search._PREDICATE_DEADLINE.get() is None


def test_sidorenko_candidate_serializes_and_replays_both_graphs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []

    def forced_violation(source: Graph, target: Graph) -> dict:
        calls.append((source.n, source.mask, target.n, target.mask))
        return {
            "homomorphism_count": 0,
            "left_integer_product": 0,
            "right_integer_product": 1,
        }

    monkeypatch.setattr(
        graph_search, "_sidorenko_violation", forced_violation
    )
    result = run_second_batch_graph_search(
        "OPG-60039",
        strategy_id="deep-diversified",
        budget=_budget(max_cases=1, max_vertices=4),
        seed=17,
    )
    assert result["outcome"] == "candidate"
    assert len(calls) == 2
    assert calls[0] == calls[1]
    assert result["candidate"]["bipartite_graph_h"]["vertex_count"] > 0
    assert result["candidate"]["target_graph_g"]["vertex_count"] > 0
    assert result["candidate"]["direct_verification"]["accepted"] is True
    assert result["metrics"]["pair_cases"] == 1
    assert result["metrics"]["premise_pair_cases"] == 1


def test_checkpoint_resumes_after_the_previous_graph() -> None:
    first = run_second_batch_graph_search(
        "OPG-335",
        strategy_id="exact-small",
        budget=_budget(max_cases=2),
        seed=1,
    )
    second = run_second_batch_graph_search(
        "OPG-335",
        strategy_id="exact-small",
        budget=_budget(max_cases=2),
        seed=1,
        checkpoint=first["checkpoint"],
    )
    assert second["checkpoint"]["next_case"] >= first["checkpoint"]["next_case"]


def test_sidorenko_checkpoint_resumes_after_previous_pair() -> None:
    first = run_second_batch_graph_search(
        "OPG-60039",
        strategy_id="screen-exact",
        budget=_budget(max_cases=2, max_vertices=3),
        seed=1,
    )
    resumed = run_second_batch_graph_search(
        "OPG-60039",
        strategy_id="screen-exact",
        budget=_budget(max_cases=2, max_vertices=3),
        seed=1,
        checkpoint=first["checkpoint"],
    )
    assert first["checkpoint"]["next_case"] == 2
    assert resumed["checkpoint"]["next_case"] == 4


@pytest.mark.parametrize(
    ("problem_id", "predicate_name"),
    [
        ("OPG-1757", "_counterexample"),
        ("OPG-60039", "_sidorenko_violation"),
    ],
)
def test_targeted_large_checkpoint_uses_global_index_random_access(
    problem_id: str,
    predicate_name: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if predicate_name == "_counterexample":
        monkeypatch.setattr(
            graph_search,
            predicate_name,
            lambda _spec, _graph, _parameters: None,
        )
    else:
        monkeypatch.setattr(
            graph_search,
            predicate_name,
            lambda _source, _target: None,
        )
    started = time.monotonic()
    result = run_second_batch_graph_search(
        problem_id,
        strategy_id="deep-diversified",
        budget={
            "time_seconds": 1,
            "max_cases": 1,
            "parameters": {
                "max_vertices": 9 if problem_id == "OPG-1757" else 6
            },
        },
        seed=17,
        checkpoint={"next_case": 100_000},
    )
    assert time.monotonic() - started < 1
    assert result["checked_cases"] == 1
    assert result["checkpoint"]["next_case"] == 100_001


def test_planar_large_checkpoint_does_not_replay_a_prefix() -> None:
    started = time.monotonic()
    result = run_second_batch_graph_search(
        "OPG-638",
        strategy_id="deep-diversified",
        budget={
            "time_seconds": 1,
            "max_cases": 1,
            "parameters": {"max_vertices": 8},
        },
        seed=17,
        checkpoint={"next_case": 100_000},
    )
    assert time.monotonic() - started < 5
    assert result["checked_cases"] == 0
    assert result["checkpoint"]["next_case"] == 100_000
    assert result["stop_reason"] == "targeted_sample_exhausted"


def test_sidorenko_exact_pairs_stream_before_large_orders_finish() -> None:
    started = time.monotonic()
    first = next(
        iter(graph_search._iter_sidorenko_exact_pairs(9, 9))
    )
    assert time.monotonic() - started < 1
    assert first[0] == Graph(0, 0)


def test_sidorenko_exact_large_prefix_skip_is_deadline_aware() -> None:
    started = time.monotonic()
    result = run_second_batch_graph_search(
        "OPG-60039",
        strategy_id="screen-exact",
        budget={
            "time_seconds": 1,
            "max_cases": 1,
            "parameters": {
                "max_vertices": 8,
                "max_h_vertices": 9,
                "max_g_vertices": 9,
            },
        },
        seed=17,
        checkpoint={"next_case": 1_000_000},
    )
    assert time.monotonic() - started < 2
    assert result["stop_reason"] == "time_budget_exhausted_during_prefix_skip"
    assert result["checked_cases"] == 0
    assert result["checkpoint"]["next_case"] == 1_000_000


def test_edge_reconstruction_replays_prefix_for_cross_chunk_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    first_graph = Graph(4, 0b111111)
    second_graph = Graph(4, 0b011111)
    monkeypatch.setattr(
        graph_search,
        "_iter_nauty_graphs",
        lambda _maximum: iter((first_graph, second_graph)),
    )
    monkeypatch.setattr(graph_search, "_edge_deck", lambda _graph: (7, 11, 13, 17))
    monkeypatch.setattr(graph_search, "_canonical_mask", lambda graph: graph.mask)

    first = run_second_batch_graph_search(
        "OPG-804",
        strategy_id="exact-small",
        budget=_budget(max_cases=1, max_vertices=4),
        seed=1,
    )
    resumed = run_second_batch_graph_search(
        "OPG-804",
        strategy_id="deep-exact",
        budget=_budget(max_cases=1, max_vertices=4),
        seed=1,
        checkpoint=first["checkpoint"],
    )

    assert first["outcome"] == "inconclusive"
    assert resumed["outcome"] == "candidate"
    assert resumed["metrics"]["replayed_cases"] == 0
    assert resumed["checked_cases"] == 1
    json.dumps(first["checkpoint"])

    legacy_checkpoint = dict(first["checkpoint"])
    legacy_checkpoint.pop("edge_reconstruction_state")
    legacy_resumed = run_second_batch_graph_search(
        "OPG-804",
        strategy_id="exact-small",
        budget=_budget(max_cases=1, max_vertices=4),
        seed=1,
        checkpoint=legacy_checkpoint,
    )
    assert legacy_resumed["outcome"] == "candidate"
    assert legacy_resumed["metrics"]["replayed_cases"] == 1


def test_edge_reconstruction_repeated_short_resumes_pass_legacy_stall() -> None:
    checkpoint: dict = {"next_case": 126}
    observed_next_cases = []
    for _ in range(2):
        result = run_second_batch_graph_search(
            "OPG-804",
            strategy_id="screen-exact",
            budget={
                "time_seconds": 1,
                "max_cases": 100_000,
                "parameters": {"max_vertices": 7},
            },
            seed=1,
            checkpoint=checkpoint,
        )
        checkpoint = result["checkpoint"]
        observed_next_cases.append(checkpoint["next_case"])
    assert observed_next_cases[0] >= 126
    assert observed_next_cases[1] > observed_next_cases[0]
    assert (
        checkpoint["edge_reconstruction_state"]["replay_next_case"]
        == checkpoint["next_case"]
    )


def test_integration_strategy_aliases_and_progress_contract() -> None:
    updates = []
    exact = run_second_batch_graph_search(
        "OPG-335",
        strategy_id="screen-exact",
        budget=_budget(max_cases=2),
        seed=1,
        progress=lambda cursor, checked: updates.append((cursor, checked)),
    )
    deep = run_second_batch_graph_search(
        "OPG-335",
        strategy_id="deep-diversified",
        budget=_budget(max_cases=2),
        seed=7,
    )
    assert exact["strategy_id"] == "screen-exact"
    assert exact["checkpoint"]["next_case"] == 2
    assert deep["strategy_id"] == "deep-diversified"
    assert deep["outcome"] in {"candidate", "inconclusive"}
    assert updates == []


def test_strong_colorability_ignores_delta_zero_boundary() -> None:
    result = run_second_batch_graph_search(
        "OPG-171",
        strategy_id="screen-exact",
        budget=_budget(max_cases=1, max_vertices=1),
        seed=1,
    )
    assert result["outcome"] == "no_candidate"
    assert result["candidate"] is None


def test_restricted_graph_order_is_reported_as_inconclusive() -> None:
    result = run_second_batch_graph_search(
        "OPG-127",
        strategy_id="screen-exact",
        budget=_budget(max_cases=1, max_vertices=10),
        seed=1,
    )
    assert result["outcome"] == "inconclusive"
    assert result["stop_reason"] == "unsupported_exact_bound"
    assert result["checked_cases"] == 0


def test_jorgensen_targeted_family_hits_the_premise() -> None:
    result = run_second_batch_graph_search(
        "OPG-154",
        strategy_id="deep-diversified",
        budget={
            "time_seconds": 3,
            "max_cases": 1,
            "parameters": {"max_vertices": 13},
        },
        seed=1,
    )
    assert result["outcome"] == "inconclusive"
    assert result["metrics"]["premise_cases"] == 1
    assert result["checkpoint"]["next_case"] == 1


def test_oddness_model_rejects_disconnected_petersen_union() -> None:
    petersen = graph_search._petersen_graph()
    edges = list(petersen.edges) + [
        (left + 10, right + 10) for left, right in petersen.edges
    ]
    disconnected_union = Graph(20, graph_search._mask_from_edges(20, edges))
    spec = next(
        spec
        for spec in SECOND_BATCH_GRAPH_SPECS
        if spec["source_id"] == "OPG-37182"
    )
    assert not graph_search._semantic_premise_check(
        spec, disconnected_union, spec["deep_bounds"]
    )


def test_uniform_forest_integer_check_on_triangle() -> None:
    triangle = Graph(3, graph_search._mask_from_edges(3, [(0, 1), (1, 2), (0, 2)]))
    assert graph_search._uniform_forest_violation(triangle) is None
    result = run_second_batch_graph_search(
        "OPG-1757",
        strategy_id="screen-exact",
        budget=_budget(max_cases=1_000, max_vertices=4),
        seed=1,
    )
    assert result["outcome"] == "no_candidate"


def test_planar_cycle_packing_parameters_on_k4_and_two_cycles() -> None:
    complete_four = Graph(4, (1 << len(graph_search._edge_pairs(4))) - 1)
    assert graph_search._is_planar(complete_four)
    assert graph_search._planar_cycle_parameters(complete_four) == (1, 2)

    two_triangles = Graph(
        6,
        graph_search._mask_from_edges(
            6,
            [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)],
        ),
    )
    assert graph_search._planar_cycle_parameters(two_triangles) == (2, 2)
    result = run_second_batch_graph_search(
        "OPG-638",
        strategy_id="screen-exact",
        budget=_budget(max_cases=1_000, max_vertices=4),
        seed=1,
    )
    assert result["outcome"] == "no_candidate"


def test_sidorenko_integer_boundaries_include_isolates_and_zero_edges() -> None:
    empty_source = Graph(0, 0)
    one_vertex_target = Graph(1, 0)
    assert graph_search._homomorphism_count(empty_source, one_vertex_target) == 1
    assert (
        graph_search._sidorenko_violation(
            empty_source, one_vertex_target
        )
        is None
    )

    two_isolates = Graph(2, 0)
    single_edge = Graph(2, graph_search._mask_from_edges(2, [(0, 1)]))
    assert graph_search._homomorphism_count(two_isolates, single_edge) == 4
    assert graph_search._sidorenko_violation(two_isolates, single_edge) is None
    assert graph_search._sidorenko_violation(single_edge, Graph(0, 0)) is None

    result = run_second_batch_graph_search(
        "OPG-60039",
        strategy_id="screen-exact",
        budget=_budget(max_cases=1_000, max_vertices=4),
        seed=1,
    )
    assert result["outcome"] == "no_candidate"
    assert result["checked_cases"] == 252


def test_all_registered_models_have_no_candidate_through_four_vertices() -> None:
    for spec in SECOND_BATCH_GRAPH_SPECS:
        result = run_second_batch_graph_search(
            spec["problem_id"],
            strategy_id="screen-exact",
            budget=_budget(max_cases=1_000, max_vertices=4),
            seed=1,
        )
        assert result["outcome"] == "no_candidate", spec["source_id"]
        assert result["candidate"] is None


def test_prescribed_cycle_double_cover_has_no_k33_false_positive() -> None:
    result = run_second_batch_graph_search(
        "OPG-60029",
        strategy_id="screen-exact",
        budget=_budget(max_cases=1_000, max_vertices=6),
        seed=1,
    )
    assert result["outcome"] == "no_candidate"


def test_unimplemented_models_are_explicitly_unregistered() -> None:
    assert len(UNREGISTERED_SECOND_BATCH_GRAPH_IDS) == 32
    with pytest.raises(KeyError):
        run_second_batch_graph_search(
            UNREGISTERED_SECOND_BATCH_GRAPH_IDS[0],
            strategy_id="exact-small",
            budget=_budget(),
            seed=1,
        )


def test_unknown_strategy_is_rejected() -> None:
    with pytest.raises(ValueError):
        run_second_batch_graph_search(
            "OPG-335",
            strategy_id="not-a-strategy",
            budget=_budget(),
            seed=1,
        )
