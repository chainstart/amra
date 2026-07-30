from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

import pytest

import amra.discovery.opg145_dense_search as dense_search
import amra.discovery.opg145_edge23_three_degree5_search as three_search
from amra.discovery.opg_coloring_search import (
    SolverResult,
    proper_edge_coloring_cnf,
    verify_acyclic_edge_coloring,
)


TARGET_GRAPH6 = "J?AFBjY^Dw?"
WRONG_DEGREES_GRAPH6 = "J?AFBjYnA]?"
TARGET_COLORING = (
    0,
    2,
    4,
    1,
    2,
    3,
    0,
    1,
    6,
    1,
    3,
    2,
    0,
    3,
    0,
    2,
    1,
    4,
    4,
    2,
    1,
    0,
    3,
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
        for name in ("geng", "pickg", "minisat", "cadical", "drat-trim")
    }


def _provenance(marker: str = "a") -> dict[str, object]:
    return {
        "implementation": {
            "aggregate_sha256": marker * 64,
            "files": [
                {
                    "role": "three_degree5_wrapper",
                    "path": "/frozen/opg145_edge23_three_degree5_search.py",
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
        three_search, "_runtime_provenance", lambda: _provenance()
    )


def _catalogue(monkeypatch, *records: str) -> None:
    def iterate(command):
        assert command == [
            "/frozen/tools/geng",
            "-q",
            "-C",
            "-d3",
            "-D5",
            "11",
            "23:23",
            "0/16",
        ]
        yield from records

    monkeypatch.setattr(
        three_search, "_iter_filtered_catalogue_records", iterate
    )


def _sat_evaluator(problem, graph, timeout_seconds):
    assert problem == "opg145"
    assert timeout_seconds > 0
    assert graph.encoding == TARGET_GRAPH6
    assert tuple(sorted(graph.degrees, reverse=True)) == (
        5,
        5,
        5,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        3,
    )
    assert verify_acyclic_edge_coloring(graph, TARGET_COLORING)
    return (
        SolverResult("sat", 0.01, frozenset(), "SAT", ""),
        proper_edge_coloring_cnf(graph, three_search.COLOR_COUNT),
        TARGET_COLORING,
        0,
        (),
    )


def test_frozen_denominators_and_configuration() -> None:
    assert three_search.EXPECTED_BY_SHARD == (
        6243,
        7862,
        9963,
        8693,
        9037,
        8129,
        7177,
        8263,
        10056,
        10665,
        7520,
        7198,
        8604,
        7257,
        9174,
        6125,
    )
    assert sum(three_search.EXPECTED_BY_SHARD) == 131_966
    assert three_search.DEGREE_SEQUENCE == (5,) * 3 + (4,) * 7 + (3,)
    assert three_search.config_for_shard(8, 60).expected_generated == 10_056
    with pytest.raises(ValueError, match="denominator"):
        three_search.ThreeDegree5SearchConfig(0, 6_242, 60).validate()
    with pytest.raises(ValueError, match="shard index"):
        three_search.config_for_shard(16, 60)


@pytest.mark.parametrize(
    "value",
    ("0/64", "16/16", "-1/16", "00/16", "0/016", "0/16/1", "0"),
)
def test_parse_shard_accepts_only_canonical_i_over_16(value: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        three_search.parse_shard(value)


def test_identity_freezes_exact_two_process_pipeline(frozen_runtime) -> None:
    identity = three_search.build_identity(
        three_search.config_for_shard(8, 60)
    )
    assert identity["campaign"] == three_search.CAMPAIGN
    assert identity["edge_range"] == [23, 23]
    assert identity["generator_degree_range"] == [3, 5]
    assert identity["maximum_degree_vertex_count"] == 3
    assert identity["degree_sequence_descending"] == (
        [5] * 3 + [4] * 7 + [3]
    )
    assert identity["shard"] == [8, 16]
    assert identity["expected_generated"] == 10_056
    assert identity["catalogue_command"] == [
        "/frozen/tools/geng",
        "-q",
        "-C",
        "-d3",
        "-D5",
        "11",
        "23:23",
        "8/16",
    ]
    assert identity["catalogue_filter_command"] == [
        "/frozen/tools/pickg",
        "-q",
        "-M3",
    ]
    manifest = identity["expected_denominator_manifest"]
    assert manifest["total"] == 131_966
    assert manifest["per_shard"]["15"] == 6_125
    assert set(identity["toolchain"]) == {
        "geng",
        "pickg",
        "minisat",
        "cadical",
        "drat-trim",
    }


def test_runtime_provenance_hashes_three_sources_and_pickg(
    monkeypatch,
) -> None:
    base_tools = _toolchain()
    base_tools.pop("pickg")
    monkeypatch.setattr(
        dense_search,
        "_runtime_provenance",
        lambda: {"implementation": {}, "toolchain": base_tools},
    )
    monkeypatch.setattr(
        three_search,
        "_pickg_fingerprint",
        lambda geng: _toolchain()["pickg"],
    )
    provenance = three_search._runtime_provenance()
    assert set(provenance["toolchain"]) == set(_toolchain())
    records = provenance["implementation"]["files"]
    expected = (
        (
            "three_degree5_wrapper",
            Path(three_search.__file__).resolve(),
        ),
        ("dense_base_runner", Path(dense_search.__file__).resolve()),
        (
            "shared_coloring",
            Path(three_search.coloring_search.__file__).resolve(),
        ),
    )
    assert [
        (record["role"], Path(record["path"])) for record in records
    ] == list(expected)
    for record, (_, path) in zip(records, expected):
        assert record["sha256"] == three_search.coloring_search.file_sha256(
            path
        )


def test_pause_resume_and_event_degree_validation(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    _catalogue(monkeypatch, TARGET_GRAPH6, TARGET_GRAPH6, TARGET_GRAPH6)
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        _sat_evaluator,
    )
    config = three_search.config_for_shard(0, 30)
    output = tmp_path / "shard-0"
    first = three_search.run_three_degree5_search(
        config, wall_seconds=60, output=output, max_cases=1
    )
    second = three_search.run_three_degree5_search(
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
    assert all(
        sorted(event["degrees"], reverse=True)
        == [5] * 3 + [4] * 7 + [3]
        for event in events
    )


def test_wrong_degree_record_rejected_before_solver(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    _catalogue(monkeypatch, WRONG_DEGREES_GRAPH6)
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        lambda *args: pytest.fail("solver received an invalid graph"),
    )
    output = tmp_path / "invalid"
    with pytest.raises(RuntimeError, match="degree sequence"):
        three_search.run_three_degree5_search(
            three_search.config_for_shard(0, 30),
            wall_seconds=60,
            output=output,
        )
    state = json.loads((output / "state.json").read_text())
    assert state["generated"] == state["next_index"] == 0


def test_resume_fails_closed_after_implementation_drift(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _catalogue(monkeypatch, TARGET_GRAPH6, TARGET_GRAPH6)
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        _sat_evaluator,
    )
    monkeypatch.setattr(
        three_search, "_runtime_provenance", lambda: _provenance("a")
    )
    output = tmp_path / "drift"
    config = three_search.config_for_shard(0, 30)
    three_search.run_three_degree5_search(
        config, wall_seconds=60, output=output, max_cases=1
    )
    monkeypatch.setattr(
        three_search, "_runtime_provenance", lambda: _provenance("d")
    )
    with pytest.raises(ValueError, match="full frozen search config"):
        three_search.run_three_degree5_search(
            config, wall_seconds=60, output=output, max_cases=1
        )


def test_delegate_restores_all_three_base_globals(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
) -> None:
    original = (
        dense_search.CHECKPOINT_SCHEMA,
        dense_search.EVENT_SCHEMA,
        dense_search.build_identity,
        dense_search._iter_catalogue_records,
        dense_search._validate_catalogue_graph,
    )

    def broken_catalogue(command):
        raise RuntimeError("synthetic pipeline failure")
        yield  # pragma: no cover

    monkeypatch.setattr(
        three_search, "_iter_filtered_catalogue_records", broken_catalogue
    )
    with pytest.raises(RuntimeError, match="synthetic pipeline failure"):
        three_search.run_three_degree5_search(
            three_search.config_for_shard(0, 30),
            wall_seconds=60,
            output=tmp_path / "broken",
        )
    assert (
        dense_search.CHECKPOINT_SCHEMA,
        dense_search.EVENT_SCHEMA,
        dense_search.build_identity,
        dense_search._iter_catalogue_records,
        dense_search._validate_catalogue_graph,
    ) == original


class _FakeProcess:
    def __init__(self, stdout: str, return_code: int):
        self.stdout = io.StringIO(stdout)
        self._return_code = return_code
        self.returncode = None

    def wait(self, timeout=None):
        self.returncode = self._return_code
        return self.returncode

    def poll(self):
        return self.returncode

    def terminate(self):
        self.returncode = self._return_code

    def kill(self):
        self.returncode = self._return_code


@pytest.mark.parametrize(
    ("geng_code", "pickg_code", "message"),
    ((7, 0, "geng=7, pickg=0"), (0, 9, "geng=0, pickg=9")),
)
def test_pipeline_requires_both_process_return_codes(
    monkeypatch,
    geng_code,
    pickg_code,
    message,
) -> None:
    geng = _FakeProcess("", geng_code)
    pickg = _FakeProcess(TARGET_GRAPH6 + "\n", pickg_code)
    launches = []

    def popen(command, **kwargs):
        launches.append((command, kwargs))
        return (geng, pickg)[len(launches) - 1]

    monkeypatch.setattr(three_search.subprocess, "Popen", popen)
    monkeypatch.setattr(
        three_search,
        "_pickg_path_for_geng",
        lambda path: Path("/frozen/tools/nauty-pickg"),
    )
    monkeypatch.setattr(
        three_search.coloring_search, "file_sha256", lambda path: "a" * 64
    )
    monkeypatch.setattr(
        three_search.coloring_search,
        "_shared_library_fingerprint",
        lambda path: {
            "ldd_exit": 0,
            "dependencies": {},
            "missing": [],
        },
    )
    monkeypatch.setattr(
        three_search,
        "_pipeline_environment",
        lambda first, second: {"LC_ALL": "C"},
    )
    command = [
        "/frozen/tools/nauty-geng",
        "-q",
        "-C",
        "-d3",
        "-D5",
        "11",
        "23:23",
        "0/16",
    ]
    with pytest.raises(RuntimeError, match=message):
        list(three_search._iter_filtered_catalogue_records(command))
    assert len(launches) == 2
    assert launches[0][0] == command
    assert launches[1][0] == [
        "/frozen/tools/nauty-pickg",
        "-q",
        "-M3",
    ]
    assert "shell" not in launches[0][1]
    assert "shell" not in launches[1][1]
