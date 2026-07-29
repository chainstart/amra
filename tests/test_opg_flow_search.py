from __future__ import annotations

import json
from pathlib import Path

import pytest

from amra.discovery import opg_flow_search
from amra.discovery.opg_coloring_search import EdgeGraph
from amra.discovery.opg_flow_search import (
    FlowEvaluation,
    FlowEvaluationBudgetExceeded,
    decode_graph6,
    flow_numerator_11_over_2,
    run_flow_search,
    spanning_subgraph_numerator_11_over_2,
)


def test_exact_flow_recurrence_on_cycles_parallel_edges_and_k4() -> None:
    cycle = EdgeGraph(5, ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)), "C5")
    parallel_three = EdgeGraph(2, ((0, 1), (0, 1), (0, 1)), "3K2")
    k4 = EdgeGraph(
        4,
        ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)),
        "K4",
    )
    assert flow_numerator_11_over_2(cycle).numerator == 9
    assert flow_numerator_11_over_2(parallel_three).numerator == 63
    assert flow_numerator_11_over_2(k4).numerator == 315


def test_recurrence_matches_independent_spanning_subgraph_formula() -> None:
    graphs = (
        EdgeGraph(2, ((0, 1), (0, 1)), "2K2"),
        EdgeGraph(3, ((0, 1), (1, 2), (0, 2)), "K3"),
        EdgeGraph(
            4,
            ((0, 1), (1, 2), (2, 3), (0, 3), (0, 2)),
            "square-plus-diagonal",
        ),
    )
    for graph in graphs:
        assert (
            flow_numerator_11_over_2(graph).numerator
            == spanning_subgraph_numerator_11_over_2(graph)
        )


def test_subdivision_does_not_change_the_flow_polynomial_value() -> None:
    triangle = EdgeGraph(3, ((0, 1), (1, 2), (0, 2)), "K3")
    subdivided = EdgeGraph(4, ((0, 3), (1, 3), (1, 2), (0, 2)), "C4")
    assert (
        flow_numerator_11_over_2(triangle).numerator
        == flow_numerator_11_over_2(subdivided).numerator
        == 9
    )


def test_max_states_counts_active_reduction_chain() -> None:
    cycle = EdgeGraph(
        10,
        tuple((vertex, vertex + 1) for vertex in range(9)) + ((0, 9),),
        "C10",
    )
    with pytest.raises(FlowEvaluationBudgetExceeded):
        flow_numerator_11_over_2(cycle, max_states=1)


def test_candidate_checkpoint_is_terminal_on_resume(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    graph = decode_graph6("C~")
    generated = 0

    def graphs(order: int, shard: tuple[int, int] | None = None):
        nonlocal generated
        generated += 1
        yield graph

    monkeypatch.setattr(opg_flow_search, "iter_girth_six_cubic_graphs", graphs)
    monkeypatch.setattr(
        opg_flow_search,
        "flow_numerator_11_over_2",
        lambda *args, **kwargs: FlowEvaluation(0, 3, 1, 0.0),
    )
    first = run_flow_search(14, 14, 10.0, 1.0, 1_000, tmp_path)
    second = run_flow_search(14, 14, 10.0, 1.0, 1_000, tmp_path)
    events = (tmp_path / "events.jsonl").read_text(encoding="utf-8").splitlines()
    assert first["status"] == "candidate_pending_independent_verification"
    assert second["status"] == "candidate_pending_independent_verification"
    assert second["nonpositive"] == 1
    assert generated == 1
    assert len(events) == 1


def test_zero_wall_budget_does_not_start_generator(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    called = False

    def graphs(order: int, shard: tuple[int, int] | None = None):
        nonlocal called
        called = True
        return iter(())

    monkeypatch.setattr(opg_flow_search, "iter_girth_six_cubic_graphs", graphs)
    state = run_flow_search(14, 14, 0.0, 1.0, 1_000, tmp_path)
    assert state["status"] == "paused_budget"
    assert state["generated"] == 0
    assert not called


def test_completed_checkpoint_stays_complete_with_zero_wall_budget(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        opg_flow_search,
        "iter_girth_six_cubic_graphs",
        lambda order, shard=None: iter(()),
    )
    first = run_flow_search(14, 14, 1.0, 1.0, 1_000, tmp_path)
    second = run_flow_search(14, 14, 0.0, 1.0, 1_000, tmp_path)
    assert first["status"] == "complete"
    assert second["status"] == "complete"
    assert second["next_order"] == 15


def test_empty_generator_cannot_start_next_order_after_deadline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    called_orders: list[int] = []
    clock = iter((0.0, 0.0, 0.0, 2.0))

    def graphs(order: int, shard: tuple[int, int] | None = None):
        called_orders.append(order)
        return iter(())

    monkeypatch.setattr(
        opg_flow_search.time,
        "monotonic",
        lambda: next(clock, 2.0),
    )
    monkeypatch.setattr(opg_flow_search, "iter_girth_six_cubic_graphs", graphs)
    state = run_flow_search(14, 16, 1.0, 1.0, 1_000, tmp_path)
    assert state["status"] == "paused_budget"
    assert state["next_order"] == 15
    assert called_orders == [14]


def test_orphan_events_are_rejected(
    tmp_path: Path,
) -> None:
    (tmp_path / "events.jsonl").write_text("{}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="without state.json"):
        run_flow_search(14, 14, 1.0, 1.0, 1_000, tmp_path)


def test_hard_queue_is_retried_and_cleared_with_larger_budget(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    graph = decode_graph6("C~")
    monkeypatch.setattr(
        opg_flow_search,
        "iter_girth_six_cubic_graphs",
        lambda order, shard=None: iter((graph,)),
    )

    def timeout(*args, **kwargs):
        raise FlowEvaluationBudgetExceeded("deliberate timeout")

    monkeypatch.setattr(opg_flow_search, "flow_numerator_11_over_2", timeout)
    first = run_flow_search(14, 14, 10.0, 0.01, 1, tmp_path)
    assert first["status"] == "complete_with_hard_queue"
    assert len(first["hard_queue"]) == 1

    monkeypatch.setattr(
        opg_flow_search,
        "flow_numerator_11_over_2",
        lambda *args, **kwargs: FlowEvaluation(315, 3, 20, 0.0),
    )
    second = run_flow_search(14, 14, 10.0, 1.0, 1_000, tmp_path)
    events = [
        json.loads(row)
        for row in (tmp_path / "events.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert second["status"] == "complete"
    assert second["hard_queue"] == []
    assert second["generated"] == 1
    assert second["three_edge_connected"] == 1
    assert second["positive"] == 1
    assert second["timeouts"] == 1
    assert len(events) == 2
    assert events[-1]["status"] == "positive"
    assert events[-1]["retry"] is True
