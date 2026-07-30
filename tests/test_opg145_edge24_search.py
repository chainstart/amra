from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

import amra.discovery.opg145_dense_search as dense_search
import amra.discovery.opg145_edge24_search as edge24_search
from amra.discovery.opg_coloring_search import (
    SolverResult,
    proper_edge_coloring_cnf,
    verify_acyclic_edge_coloring,
)


EDGE24_GRAPH6 = "J~KWWKF_]@_"
EDGE24_COLORING = (
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
    5,
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
                    "role": "edge24_wrapper",
                    "path": "/frozen/opg145_edge24_search.py",
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
        edge24_search, "_runtime_provenance", lambda: _provenance()
    )


def _catalogue(monkeypatch, count: int = 3) -> None:
    def iterate(command):
        assert command[-3:] == ["11", "24:24", "0/16"]
        for _ in range(count):
            yield EDGE24_GRAPH6

    monkeypatch.setattr(dense_search, "_iter_catalogue_records", iterate)


def _sat_evaluator(problem, graph, timeout_seconds):
    assert problem == "opg145"
    assert timeout_seconds > 0
    assert graph.encoding == EDGE24_GRAPH6
    assert len(graph.edges) == edge24_search.EDGE_COUNT
    assert verify_acyclic_edge_coloring(graph, EDGE24_COLORING)
    return (
        SolverResult("sat", 0.01, frozenset(), "SAT", ""),
        proper_edge_coloring_cnf(graph, edge24_search.COLOR_COUNT),
        EDGE24_COLORING,
        0,
        (),
    )


def test_frozen_denominators_total_and_config_rejection() -> None:
    assert edge24_search.EXPECTED_BY_SHARD == (
        70_390,
        71_213,
        53_565,
        53_326,
        52_989,
        88_044,
        56_783,
        57_109,
        39_326,
        64_277,
        67_455,
        41_413,
        77_943,
        47_552,
        88_696,
        73_206,
    )
    assert sum(edge24_search.EXPECTED_BY_SHARD) == 1_003_287
    assert edge24_search.config_for_shard(15, 60.0).expected_generated == 73_206

    with pytest.raises(ValueError, match="denominator"):
        edge24_search.Edge24SearchConfig(0, 70_389, 60.0).validate()
    with pytest.raises(ValueError, match="shard index"):
        edge24_search.config_for_shard(16, 60.0)


@pytest.mark.parametrize(
    "value",
    ("0/4", "16/16", "-1/16", "00/16", "0/016", "0/16/1", "0"),
)
def test_parse_shard_rejects_every_noncanonical_or_out_of_range_value(
    value: str,
) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        edge24_search.parse_shard(value)


def test_identity_fixes_m24_i16_denominator_and_three_source_provenance(
    frozen_runtime,
) -> None:
    config = edge24_search.config_for_shard(9, 300.0)
    identity = edge24_search.build_identity(config)
    assert identity["campaign"] == edge24_search.CAMPAIGN
    assert identity["edge_range"] == [24, 24]
    assert identity["shard"] == [9, 16]
    assert identity["expected_generated"] == 64_277
    assert identity["catalogue_command"] == [
        "/frozen/tools/geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "24:24",
        "9/16",
    ]
    manifest = identity["expected_denominator_manifest"]
    assert manifest["per_shard_catalogue_command_canonical"] == [
        "geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "24:24",
        "i/16",
    ]
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
        "24:24",
    ]
    assert manifest["per_shard"]["9"] == 64_277
    assert manifest["total"] == 1_003_287
    assert [
        record["role"] for record in identity["implementation"]["files"]
    ] == [
        "edge24_wrapper",
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
    provenance = edge24_search._runtime_provenance()
    records = provenance["implementation"]["files"]
    expected = (
        (
            "edge24_wrapper",
            Path(edge24_search.__file__).resolve(),
        ),
        (
            "dense_base_runner",
            Path(dense_search.__file__).resolve(),
        ),
        (
            "shared_coloring",
            Path(edge24_search.coloring_search.__file__).resolve(),
        ),
    )
    assert [
        (record["role"], Path(record["path"])) for record in records
    ] == list(expected)
    for record, (_, path) in zip(records, expected):
        assert record["sha256"] == edge24_search.coloring_search.file_sha256(
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
    config = edge24_search.config_for_shard(0, 30.0)

    first = edge24_search.run_edge24_search(
        config,
        wall_seconds=60.0,
        output=output,
        max_cases=1,
    )
    assert first["status"] == "paused_budget"
    assert first["next_index"] == first["generated"] == first["sat"] == 1
    assert first["identity"]["campaign"] == edge24_search.CAMPAIGN
    assert first["identity"]["shard"] == [0, 16]
    assert first["identity"]["edge_range"] == [24, 24]

    second = edge24_search.run_edge24_search(
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
    assert all(event["event_schema"] == edge24_search.EVENT_SCHEMA for event in events)
    assert all(event["edge_count"] == 24 for event in events)


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
        edge24_search, "_runtime_provenance", lambda: _provenance("a")
    )
    output = tmp_path / "source-drift"
    config = edge24_search.config_for_shard(0, 30.0)
    edge24_search.run_edge24_search(
        config,
        wall_seconds=60.0,
        output=output,
        max_cases=1,
    )

    monkeypatch.setattr(
        edge24_search, "_runtime_provenance", lambda: _provenance("d")
    )
    with pytest.raises(ValueError, match="full frozen search config"):
        edge24_search.run_edge24_search(
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
        edge24_search.run_edge24_search(
            edge24_search.config_for_shard(0, 30.0),
            wall_seconds=60.0,
            output=tmp_path / "broken",
        )
    assert (
        dense_search.CHECKPOINT_SCHEMA,
        dense_search.EVENT_SCHEMA,
        dense_search.build_identity,
    ) == original
