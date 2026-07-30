from __future__ import annotations

import json
from pathlib import Path

import pytest

import amra.discovery.opg145_dense_search as dense_search
from amra.discovery.opg_coloring_search import (
    SolverResult,
    decode_graph6,
    proper_edge_coloring_cnf,
    verify_acyclic_edge_coloring,
)


def _graph6(order: int, edges: set[tuple[int, int]]) -> str:
    normalized = {
        (min(left, right), max(left, right)) for left, right in edges
    }
    bits = [
        int((left, right) in normalized)
        for right in range(1, order)
        for left in range(right)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = "".join(
        chr(
            63
            + sum(
                bit << (5 - offset)
                for offset, bit in enumerate(bits[index : index + 6])
            )
        )
        for index in range(0, len(bits), 6)
    )
    return chr(order + 63) + payload


FILTERED_GRAPH6 = _graph6(
    11,
    {
        (vertex, (vertex + 1) % 11)
        for vertex in range(11)
    },
)

ELIGIBLE_EDGES = {
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
    (2, 10),
}
ELIGIBLE_GRAPH6 = _graph6(11, ELIGIBLE_EDGES)
ELIGIBLE_COLORING = (
    0,
    3,
    1,
    5,
    2,
    0,
    2,
    6,
    5,
    0,
    6,
    3,
    0,
    4,
    0,
    6,
)


@pytest.fixture
def frozen_runtime(monkeypatch):
    def provenance():
        toolchain = {}
        for name in ("geng", "minisat", "cadical", "drat-trim"):
            toolchain[name] = {
                "path": f"/frozen/tools/{name}",
                "sha256": name.center(64, "0"),
                "dynamic_linkage": {
                    "ldd_exit": 0,
                    "dependencies": {
                        "libexample.so": {
                            "path": f"/frozen/lib/{name}/libexample.so",
                            "sha256": name.center(64, "1"),
                        }
                    },
                    "missing": [],
                },
            }
        return {
            "implementation": {
                "aggregate_sha256": "a" * 64,
                "files": [
                    {"path": "/frozen/runner.py", "sha256": "b" * 64},
                    {"path": "/frozen/shared.py", "sha256": "c" * 64},
                ],
            },
            "toolchain": toolchain,
        }

    monkeypatch.setattr(dense_search, "_runtime_provenance", provenance)


def _records(monkeypatch, *records: str) -> None:
    def iterate(command):
        yield from records

    monkeypatch.setattr(dense_search, "_iter_catalogue_records", iterate)


def _sat_evaluator(problem, graph, timeout_seconds):
    assert problem == "opg145"
    assert timeout_seconds > 0
    assert graph.encoding == ELIGIBLE_GRAPH6
    assert verify_acyclic_edge_coloring(graph, ELIGIBLE_COLORING)
    return (
        SolverResult("sat", 0.01, frozenset(), "SAT", ""),
        proper_edge_coloring_cnf(graph, 7),
        ELIGIBLE_COLORING,
        0,
        (),
    )


def _config(
    *,
    expected: int = 2,
    per_instance_seconds: float = 10.0,
) -> dense_search.DenseSearchConfig:
    return dense_search.DenseSearchConfig(
        minimum_edges=11,
        maximum_edges=16,
        shard_index=0,
        expected_generated=expected,
        per_instance_seconds=per_instance_seconds,
    )


def test_frozen_denominators_and_exact_default_catalogue_command(
    frozen_runtime,
) -> None:
    assert dense_search.DEFAULT_EXPECTED_BY_SHARD == {
        0: 88_595,
        1: 100_734,
        2: 80_076,
        3: 114_717,
    }
    assert sum(dense_search.DEFAULT_EXPECTED_BY_SHARD.values()) == 384_122
    config = dense_search.DenseSearchConfig(
        25,
        27,
        2,
        80_076,
        300.0,
    )
    identity = dense_search.build_identity(config)
    assert identity["catalogue_command"] == [
        "/frozen/tools/geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "25:27",
        "2/4",
    ]
    assert identity["catalogue_command_canonical"] == [
        "geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "25:27",
        "2/4",
    ]
    assert identity["expected_generated"] == 80_076
    assert identity["expected_denominator_manifest"]["total"] == 384_122
    assert identity["expected_denominator_manifest"][
        "count_command_canonical"
    ] == [
        "geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "-u",
        "11",
        "25:27",
        "i/4",
    ]


def test_default_denominator_cannot_be_overridden(frozen_runtime) -> None:
    config = dense_search.DenseSearchConfig(25, 27, 0, 88_594, 300.0)
    with pytest.raises(ValueError, match="frozen 25:27 denominator"):
        dense_search.build_identity(config)


def test_exact_resume_replays_prefix_then_completes(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    _records(monkeypatch, FILTERED_GRAPH6, ELIGIBLE_GRAPH6)
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        _sat_evaluator,
    )
    output = tmp_path / "shard"
    first = dense_search.run_dense_search(
        _config(), wall_seconds=60.0, output=output, max_cases=1
    )
    assert first["status"] == "paused_budget"
    assert first["next_index"] == 1
    assert first["generated"] == 1
    assert first["filtered_three_sparse"] == 1
    assert first["eligible"] == 0

    second = dense_search.run_dense_search(
        _config(), wall_seconds=60.0, output=output
    )
    assert second["status"] == "complete"
    assert second["generated"] == 2
    assert second["filtered_three_sparse"] == 1
    assert second["eligible"] == second["sat"] == 1
    assert second["unsat"] == second["timeouts"] == second["unknown"] == 0

    events = [
        json.loads(line)
        for line in (output / "events.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert [event["index"] for event in events] == [0, 1]
    assert events[0]["graph6"] == FILTERED_GRAPH6
    assert events[0]["status"] == "filtered_three_sparse"
    assert events[1]["graph6"] == ELIGIBLE_GRAPH6
    assert events[1]["edges"] == [
        list(edge) for edge in decode_graph6(ELIGIBLE_GRAPH6).edges
    ]
    assert events[1]["verified_coloring"] == list(ELIGIBLE_COLORING)


@pytest.mark.parametrize(
    ("solver_status", "run_status", "counter"),
    (
        ("unsat", "stopped_unsat", "unsat"),
        ("timeout", "stopped_timeout", "timeouts"),
        ("unknown", "stopped_unknown", "unknown"),
    ),
)
def test_any_non_sat_solver_result_is_terminal_and_never_complete(
    solver_status: str,
    run_status: str,
    counter: str,
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    _records(monkeypatch, ELIGIBLE_GRAPH6)

    def evaluate(problem, graph, timeout_seconds):
        return (
            SolverResult(solver_status, 0.01, frozenset(), "", ""),
            proper_edge_coloring_cnf(graph, 7),
            None,
            0,
            (),
        )

    monkeypatch.setattr(
        dense_search.coloring_search, "evaluate_coloring_instance", evaluate
    )
    result = dense_search.run_dense_search(
        dense_search.DenseSearchConfig(16, 16, 0, 1, 10.0),
        wall_seconds=60.0,
        output=tmp_path / solver_status,
    )
    assert result["status"] == run_status
    assert result[counter] == 1
    assert result["status"] != "complete"


def test_invalid_sat_witness_fails_before_an_event_or_counter_advance(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    _records(monkeypatch, ELIGIBLE_GRAPH6)

    def invalid_evaluate(problem, graph, timeout_seconds):
        return (
            SolverResult("sat", 0.01, frozenset(), "", ""),
            proper_edge_coloring_cnf(graph, 7),
            (0,) * len(graph.edges),
            0,
            (),
        )

    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        invalid_evaluate,
    )
    output = tmp_path / "invalid"
    with pytest.raises(RuntimeError, match="acyclic verifier"):
        dense_search.run_dense_search(
            dense_search.DenseSearchConfig(16, 16, 0, 1, 10.0),
            wall_seconds=60.0,
            output=output,
        )
    state = json.loads((output / "state.json").read_text(encoding="utf-8"))
    assert state["generated"] == state["next_index"] == 0
    assert not (output / "events.jsonl").exists()


def test_catalogue_exhaustion_with_wrong_denominator_is_not_complete(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    _records(monkeypatch, ELIGIBLE_GRAPH6)
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        _sat_evaluator,
    )
    result = dense_search.run_dense_search(
        _config(expected=2),
        wall_seconds=60.0,
        output=tmp_path / "short",
    )
    assert result["status"] == "denominator_mismatch"
    assert result["observed_generated_at_exhaustion"] == 1
    assert result["status"] != "complete"


def test_resume_rejects_event_tampering_and_config_drift(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    _records(monkeypatch, FILTERED_GRAPH6, ELIGIBLE_GRAPH6)
    output = tmp_path / "tamper"
    dense_search.run_dense_search(
        _config(), wall_seconds=60.0, output=output, max_cases=1
    )

    with pytest.raises(ValueError, match="full frozen search config"):
        dense_search.run_dense_search(
            _config(per_instance_seconds=20.0),
            wall_seconds=60.0,
            output=output,
        )

    event = json.loads((output / "events.jsonl").read_text(encoding="utf-8"))
    event["graph6"] = ELIGIBLE_GRAPH6
    (output / "events.jsonl").write_text(
        json.dumps(event, sort_keys=True) + "\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="graph payload is inconsistent"):
        dense_search.run_dense_search(
            _config(), wall_seconds=60.0, output=output
        )


def test_events_without_checkpoint_are_rejected(
    tmp_path: Path,
    frozen_runtime,
) -> None:
    output = tmp_path / "orphan"
    output.mkdir()
    (output / "events.jsonl").write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="events exist without a checkpoint"):
        dense_search.run_dense_search(
            _config(), wall_seconds=60.0, output=output
        )
