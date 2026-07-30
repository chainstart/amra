from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

import amra.discovery.opg145_dense_search as dense_search
import amra.discovery.opg145_edge23_near_regular_search as near_search
from amra.discovery.opg_coloring_search import (
    SolverResult,
    proper_edge_coloring_cnf,
    verify_acyclic_edge_coloring,
)


NEAR_GRAPH6 = "J?AFbY[}Bw?"
NON_NEAR_GRAPH6 = "J~KWWKF_]@?"
NEAR_COLORING = (
    0,
    1,
    0,
    6,
    3,
    1,
    0,
    2,
    6,
    3,
    2,
    1,
    4,
    2,
    3,
    4,
    1,
    0,
    2,
    1,
    0,
    4,
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
                    "role": "near_regular_wrapper",
                    "path": "/frozen/opg145_edge23_near_regular_search.py",
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
        near_search, "_runtime_provenance", lambda: _provenance()
    )


def _catalogue(monkeypatch, *records: str) -> None:
    def iterate(command):
        assert command[-5:] == [
            "-d4",
            "-D5",
            "11",
            "23:23",
            "0/16",
        ]
        yield from records

    monkeypatch.setattr(dense_search, "_iter_catalogue_records", iterate)


def _sat_evaluator(problem, graph, timeout_seconds):
    assert problem == "opg145"
    assert timeout_seconds > 0
    assert graph.encoding == NEAR_GRAPH6
    assert tuple(sorted(graph.degrees, reverse=True)) == (
        5,
        5,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
    )
    assert verify_acyclic_edge_coloring(graph, NEAR_COLORING)
    return (
        SolverResult("sat", 0.01, frozenset(), "SAT", ""),
        proper_edge_coloring_cnf(graph, near_search.COLOR_COUNT),
        NEAR_COLORING,
        0,
        (),
    )


def test_frozen_counts_and_config_rejection() -> None:
    assert near_search.EXPECTED_BY_SHARD == (
        880,
        449,
        664,
        517,
        425,
        602,
        906,
        629,
        451,
        437,
        492,
        507,
        611,
        536,
        463,
        417,
    )
    assert sum(near_search.EXPECTED_BY_SHARD) == 8_986
    assert near_search.config_for_shard(15, 60).expected_generated == 417
    with pytest.raises(ValueError, match="denominator"):
        near_search.NearRegularSearchConfig(0, 879, 60).validate()
    with pytest.raises(ValueError, match="shard index"):
        near_search.config_for_shard(16, 60)


@pytest.mark.parametrize(
    "value",
    ("0/64", "16/16", "-1/16", "00/16", "0/016", "0/16/1", "0"),
)
def test_parse_shard_is_canonical_and_fixed(value: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        near_search.parse_shard(value)


def test_identity_fixes_exact_near_regular_catalogue(frozen_runtime) -> None:
    identity = near_search.build_identity(
        near_search.config_for_shard(6, 60)
    )
    assert identity["campaign"] == near_search.CAMPAIGN
    assert identity["edge_range"] == [23, 23]
    assert identity["degree_range"] == [4, 5]
    assert identity["degree_sequence_descending"] == [5, 5] + [4] * 9
    assert identity["shard"] == [6, 16]
    assert identity["expected_generated"] == 906
    assert identity["catalogue_command"] == [
        "/frozen/tools/geng",
        "-q",
        "-C",
        "-d4",
        "-D5",
        "11",
        "23:23",
        "6/16",
    ]
    manifest = identity["expected_denominator_manifest"]
    assert manifest["per_shard_catalogue_command_canonical"][-1] == "i/16"
    assert manifest["total_count_command_canonical"] == [
        "geng",
        "-C",
        "-d4",
        "-D5",
        "-u",
        "11",
        "23:23",
    ]
    assert manifest["degree_sequence_descending"] == [5, 5] + [4] * 9
    assert manifest["total"] == 8_986
    assert [
        record["role"] for record in identity["implementation"]["files"]
    ] == [
        "near_regular_wrapper",
        "dense_base_runner",
        "shared_coloring",
    ]


def test_runtime_provenance_hashes_exact_three_sources(monkeypatch) -> None:
    monkeypatch.setattr(
        dense_search,
        "_runtime_provenance",
        lambda: {"implementation": {}, "toolchain": _toolchain()},
    )
    provenance = near_search._runtime_provenance()
    records = provenance["implementation"]["files"]
    expected = (
        ("near_regular_wrapper", Path(near_search.__file__).resolve()),
        ("dense_base_runner", Path(dense_search.__file__).resolve()),
        (
            "shared_coloring",
            Path(near_search.coloring_search.__file__).resolve(),
        ),
    )
    assert [
        (record["role"], Path(record["path"])) for record in records
    ] == list(expected)
    for record, (_, path) in zip(records, expected):
        assert record["sha256"] == near_search.coloring_search.file_sha256(
            path
        )


def test_pause_resume_with_exact_degree_validation(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    _catalogue(monkeypatch, NEAR_GRAPH6, NEAR_GRAPH6, NEAR_GRAPH6)
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        _sat_evaluator,
    )
    config = near_search.config_for_shard(0, 30)
    output = tmp_path / "shard-0"
    first = near_search.run_near_regular_search(
        config, wall_seconds=60, output=output, max_cases=1
    )
    second = near_search.run_near_regular_search(
        config, wall_seconds=60, output=output, max_cases=1
    )
    assert first["status"] == second["status"] == "paused_budget"
    assert first["generated"] == first["sat"] == 1
    assert second["generated"] == second["sat"] == 2
    events = [
        json.loads(line)
        for line in (output / "events.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert [event["index"] for event in events] == [0, 1]
    assert all(event["edge_count"] == 23 for event in events)
    assert all(sorted(event["degrees"], reverse=True) == [5, 5] + [4] * 9 for event in events)


def test_non_near_regular_record_is_rejected_before_evaluation(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    _catalogue(monkeypatch, NON_NEAR_GRAPH6)
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        lambda *args: pytest.fail("solver must not receive an invalid graph"),
    )
    output = tmp_path / "invalid"
    with pytest.raises(RuntimeError, match="degree sequence"):
        near_search.run_near_regular_search(
            near_search.config_for_shard(0, 30),
            wall_seconds=60,
            output=output,
        )
    state = json.loads((output / "state.json").read_text(encoding="utf-8"))
    assert state["generated"] == state["next_index"] == 0


def test_resume_fails_closed_after_source_hash_drift(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _catalogue(monkeypatch, NEAR_GRAPH6, NEAR_GRAPH6)
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        _sat_evaluator,
    )
    monkeypatch.setattr(
        near_search, "_runtime_provenance", lambda: _provenance("a")
    )
    output = tmp_path / "drift"
    config = near_search.config_for_shard(0, 30)
    near_search.run_near_regular_search(
        config, wall_seconds=60, output=output, max_cases=1
    )
    monkeypatch.setattr(
        near_search, "_runtime_provenance", lambda: _provenance("d")
    )
    with pytest.raises(ValueError, match="full frozen search config"):
        near_search.run_near_regular_search(
            config, wall_seconds=60, output=output, max_cases=1
        )


def test_delegate_restores_base_schemas_identity_and_validator(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    original = (
        dense_search.CHECKPOINT_SCHEMA,
        dense_search.EVENT_SCHEMA,
        dense_search.build_identity,
        dense_search._validate_catalogue_graph,
    )

    def broken_catalogue(command):
        raise RuntimeError("synthetic catalogue failure")
        yield  # pragma: no cover

    monkeypatch.setattr(
        dense_search, "_iter_catalogue_records", broken_catalogue
    )
    with pytest.raises(RuntimeError, match="synthetic catalogue failure"):
        near_search.run_near_regular_search(
            near_search.config_for_shard(0, 30),
            wall_seconds=60,
            output=tmp_path / "broken",
        )
    assert (
        dense_search.CHECKPOINT_SCHEMA,
        dense_search.EVENT_SCHEMA,
        dense_search.build_identity,
        dense_search._validate_catalogue_graph,
    ) == original
