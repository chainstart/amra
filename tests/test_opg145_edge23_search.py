from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

import amra.discovery.opg145_dense_search as dense_search
import amra.discovery.opg145_edge23_search as edge23_search
from amra.discovery.opg_coloring_search import (
    SolverResult,
    proper_edge_coloring_cnf,
    verify_acyclic_edge_coloring,
)


EDGE23_GRAPH6 = "J~KWWKF_]@?"
EDGE23_COLORING = (
    0,
    5,
    2,
    4,
    3,
    1,
    0,
    2,
    6,
    3,
    1,
    0,
    2,
    5,
    1,
    4,
    3,
    2,
    1,
    0,
    3,
    1,
    2,
)


def _toolchain() -> dict[str, object]:
    return {
        name: {
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
        for name in ("geng", "minisat", "cadical", "drat-trim")
    }


def _provenance(marker: str = "a") -> dict[str, object]:
    return {
        "implementation": {
            "aggregate_sha256": marker * 64,
            "files": [
                {
                    "role": "edge23_wrapper",
                    "path": "/frozen/opg145_edge23_search.py",
                    "sha256": marker * 64,
                },
                {
                    "role": "dense_base_runner",
                    "path": "/frozen/opg145_dense_search.py",
                    "sha256": "b" * 64,
                },
                {
                    "role": "shared_coloring",
                    "path": "/frozen/opg_coloring_search.py",
                    "sha256": "c" * 64,
                },
            ],
        },
        "toolchain": _toolchain(),
    }


@pytest.fixture
def frozen_runtime(monkeypatch):
    monkeypatch.setattr(
        edge23_search, "_runtime_provenance", lambda: _provenance()
    )


def _catalogue(monkeypatch, count: int = 3) -> None:
    def iterate(command):
        assert command[-3:] == ["11", "23:23", "0/64"]
        for _ in range(count):
            yield EDGE23_GRAPH6

    monkeypatch.setattr(dense_search, "_iter_catalogue_records", iterate)


def _sat_evaluator(problem, graph, timeout_seconds):
    assert problem == "opg145"
    assert timeout_seconds > 0
    assert graph.encoding == EDGE23_GRAPH6
    assert len(graph.edges) == edge23_search.EDGE_COUNT
    assert verify_acyclic_edge_coloring(graph, EDGE23_COLORING)
    return (
        SolverResult("sat", 0.01, frozenset(), "SAT", ""),
        proper_edge_coloring_cnf(graph, edge23_search.COLOR_COUNT),
        EDGE23_COLORING,
        0,
        (),
    )


def test_frozen_denominators_total_and_config_rejection() -> None:
    assert len(edge23_search.EXPECTED_BY_SHARD) == 64
    assert edge23_search.EXPECTED_BY_SHARD[:4] == (
        32_085,
        8_525,
        35_867,
        44_942,
    )
    assert edge23_search.EXPECTED_BY_SHARD[-4:] == (
        42_672,
        21_026,
        47_432,
        23_993,
    )
    assert sum(edge23_search.EXPECTED_BY_SHARD) == 2_013_018
    assert (
        edge23_search.config_for_shard(63, 60.0).expected_generated
        == 23_993
    )

    with pytest.raises(ValueError, match="denominator"):
        edge23_search.Edge23SearchConfig(0, 32_084, 60.0).validate()
    with pytest.raises(ValueError, match="shard index"):
        edge23_search.config_for_shard(64, 60.0)


@pytest.mark.parametrize(
    "value",
    ("0/16", "64/64", "-1/64", "00/64", "0/064", "0/64/1", "0"),
)
def test_parse_shard_rejects_every_noncanonical_or_out_of_range_value(
    value: str,
) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        edge23_search.parse_shard(value)


def test_identity_fixes_m23_i64_and_accurate_denominator_provenance(
    frozen_runtime,
) -> None:
    config = edge23_search.config_for_shard(57, 300.0)
    identity = edge23_search.build_identity(config)
    assert identity["campaign"] == edge23_search.CAMPAIGN
    assert identity["edge_range"] == [23, 23]
    assert identity["shard"] == [57, 64]
    assert identity["expected_generated"] == 64_935
    assert identity["catalogue_command"] == [
        "/frozen/tools/geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "23:23",
        "57/64",
    ]
    manifest = identity["expected_denominator_manifest"]
    assert manifest["method"] == (
        "independent_per_shard_graph6_line_count_with_nonquiet_u_"
        "total_crosscheck"
    )
    assert manifest["per_shard_catalogue_command_canonical"][-1] == "i/64"
    assert manifest["per_shard_count_operation"] == (
        "count_stdout_graph6_records"
    )
    assert manifest["total_count_command_canonical"] == [
        "geng",
        "-C",
        "-d2",
        "-D5",
        "-u",
        "11",
        "23:23",
    ]
    assert manifest["per_shard"]["57"] == 64_935
    assert manifest["total"] == 2_013_018
    assert [
        record["role"] for record in identity["implementation"]["files"]
    ] == [
        "edge23_wrapper",
        "dense_base_runner",
        "shared_coloring",
    ]


def test_runtime_provenance_hashes_the_actual_three_source_files(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        dense_search,
        "_runtime_provenance",
        lambda: {"implementation": {}, "toolchain": _toolchain()},
    )
    provenance = edge23_search._runtime_provenance()
    records = provenance["implementation"]["files"]
    expected = (
        ("edge23_wrapper", Path(edge23_search.__file__).resolve()),
        ("dense_base_runner", Path(dense_search.__file__).resolve()),
        (
            "shared_coloring",
            Path(edge23_search.coloring_search.__file__).resolve(),
        ),
    )
    assert [
        (record["role"], Path(record["path"])) for record in records
    ] == list(expected)
    for record, (_, path) in zip(records, expected):
        assert record["sha256"] == edge23_search.coloring_search.file_sha256(
            path
        )


def test_smoke_pause_and_exact_prefix_resume(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    _catalogue(monkeypatch)
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        _sat_evaluator,
    )
    output = tmp_path / "shard-0"
    config = edge23_search.config_for_shard(0, 30.0)

    first = edge23_search.run_edge23_search(
        config,
        wall_seconds=60.0,
        output=output,
        max_cases=1,
    )
    assert first["status"] == "paused_budget"
    assert first["next_index"] == first["generated"] == first["sat"] == 1
    assert first["identity"]["campaign"] == edge23_search.CAMPAIGN
    assert first["identity"]["shard"] == [0, 64]
    assert first["identity"]["edge_range"] == [23, 23]

    second = edge23_search.run_edge23_search(
        config,
        wall_seconds=60.0,
        output=output,
        max_cases=1,
    )
    assert second["status"] == "paused_budget"
    assert second["next_index"] == second["generated"] == second["sat"] == 2
    events = [
        json.loads(line)
        for line in (output / "events.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert [event["index"] for event in events] == [0, 1]
    assert all(
        event["event_schema"] == edge23_search.EVENT_SCHEMA
        for event in events
    )
    assert all(event["edge_count"] == 23 for event in events)


def test_resume_fails_closed_after_any_bound_source_hash_drift(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _catalogue(monkeypatch)
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        _sat_evaluator,
    )
    monkeypatch.setattr(
        edge23_search, "_runtime_provenance", lambda: _provenance("a")
    )
    output = tmp_path / "source-drift"
    config = edge23_search.config_for_shard(0, 30.0)
    edge23_search.run_edge23_search(
        config,
        wall_seconds=60.0,
        output=output,
        max_cases=1,
    )

    monkeypatch.setattr(
        edge23_search, "_runtime_provenance", lambda: _provenance("d")
    )
    with pytest.raises(ValueError, match="full frozen search config"):
        edge23_search.run_edge23_search(
            config,
            wall_seconds=60.0,
            output=output,
            max_cases=1,
        )


def test_delegate_always_restores_base_runner_contracts(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    original = (
        dense_search.CHECKPOINT_SCHEMA,
        dense_search.EVENT_SCHEMA,
        dense_search.build_identity,
    )

    def broken_catalogue(command):
        raise RuntimeError("synthetic catalogue failure")
        yield  # pragma: no cover

    monkeypatch.setattr(
        dense_search, "_iter_catalogue_records", broken_catalogue
    )
    with pytest.raises(RuntimeError, match="synthetic catalogue failure"):
        edge23_search.run_edge23_search(
            edge23_search.config_for_shard(0, 30.0),
            wall_seconds=60.0,
            output=tmp_path / "broken",
        )
    assert (
        dense_search.CHECKPOINT_SCHEMA,
        dense_search.EVENT_SCHEMA,
        dense_search.build_identity,
    ) == original
