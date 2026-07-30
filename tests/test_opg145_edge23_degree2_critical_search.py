from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

import pytest

import amra.discovery.opg145_edge23_degree2_critical_search as critical
from amra.discovery.opg_coloring_search import (
    SolverResult,
    decode_graph6,
    proper_edge_coloring_cnf,
    verify_acyclic_edge_coloring,
)


SUPPRESSIBLE_GRAPH6 = "J?AFBjw}Fo?"
NO_DEGREE2_GRAPH6 = "J?AFBjw}FW?"
RESIDUAL_GRAPH6 = "J?ABfJiz?}?"
COMMON_MISSING_GRAPH6 = "J?ABfJY}@u?"
RESIDUAL_COLORING = (
    0,
    5,
    4,
    2,
    3,
    2,
    1,
    4,
    5,
    4,
    3,
    1,
    0,
    4,
    3,
    2,
    0,
    1,
    3,
    2,
    5,
    1,
    0,
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
                    "role": "degree2_critical_runner",
                    "path": "/frozen/degree2.py",
                    "sha256": marker * 64,
                },
                {
                    "role": "shared_coloring",
                    "path": "/frozen/coloring.py",
                    "sha256": "b" * 64,
                },
            ],
        },
        "toolchain": _toolchain(),
    }


@pytest.fixture
def frozen_runtime(monkeypatch):
    monkeypatch.setattr(
        critical, "_runtime_provenance", lambda: _provenance()
    )


@pytest.fixture
def small_denominators(monkeypatch):
    rows = {
        "EXPECTED_GENERATED_BY_SHARD": (4,) + (0,) * 15,
        "EXPECTED_NO_DEGREE2_BY_SHARD": (1,) + (0,) * 15,
        "EXPECTED_SUPPRESSIBLE_BY_SHARD": (1,) + (0,) * 15,
        "EXPECTED_COMMON_MISSING_BY_SHARD": (1,) + (0,) * 15,
        "EXPECTED_RESIDUAL_BY_SHARD": (1,) + (0,) * 15,
    }
    for name, value in rows.items():
        monkeypatch.setattr(critical, name, value)
    monkeypatch.setattr(critical, "EXPECTED_GENERATED_TOTAL", 4)
    monkeypatch.setattr(critical, "EXPECTED_NO_DEGREE2_TOTAL", 1)
    monkeypatch.setattr(critical, "EXPECTED_SUPPRESSIBLE_TOTAL", 1)
    monkeypatch.setattr(critical, "EXPECTED_COMMON_MISSING_TOTAL", 1)
    monkeypatch.setattr(critical, "EXPECTED_RESIDUAL_TOTAL", 1)


def _records(monkeypatch, *records: str) -> None:
    def iterate(command):
        assert command == [
            "/frozen/tools/geng",
            "-q",
            "-C",
            "-d2",
            "-D5",
            "11",
            "23:23",
            "0/16",
        ]
        yield from records

    monkeypatch.setattr(critical, "_iter_catalogue_records", iterate)


def _sat_evaluator(problem, graph, timeout_seconds):
    assert problem == "opg145"
    assert timeout_seconds > 0
    assert graph.encoding == RESIDUAL_GRAPH6
    assert verify_acyclic_edge_coloring(graph, RESIDUAL_COLORING)
    return (
        SolverResult("sat", 0.01, frozenset(), "SAT", ""),
        proper_edge_coloring_cnf(graph, critical.COLOR_COUNT),
        RESIDUAL_COLORING,
        0,
        (),
    )


def test_frozen_denominators_and_mutually_exclusive_totals() -> None:
    assert critical.EXPECTED_GENERATED_BY_SHARD == (
        80617,
        99770,
        132255,
        153050,
        129042,
        133346,
        143824,
        102642,
        187137,
        172013,
        121368,
        148261,
        107103,
        100732,
        113832,
        88026,
    )
    assert critical.EXPECTED_RESIDUAL_BY_SHARD == (
        5813,
        5702,
        7242,
        10963,
        6509,
        11889,
        12611,
        7923,
        12280,
        9959,
        10345,
        11126,
        5936,
        7078,
        5354,
        6272,
    )
    assert sum(critical.EXPECTED_GENERATED_BY_SHARD) == 2_013_018
    assert sum(critical.EXPECTED_NO_DEGREE2_BY_SHARD) == 1_094_808
    assert sum(critical.EXPECTED_SUPPRESSIBLE_BY_SHARD) == 646_555
    assert sum(critical.EXPECTED_COMMON_MISSING_BY_SHARD) == 134_653
    assert sum(critical.EXPECTED_RESIDUAL_BY_SHARD) == 137_002
    for index in range(16):
        assert critical.EXPECTED_GENERATED_BY_SHARD[index] == (
            critical.EXPECTED_NO_DEGREE2_BY_SHARD[index]
            + critical.EXPECTED_SUPPRESSIBLE_BY_SHARD[index]
            + critical.EXPECTED_COMMON_MISSING_BY_SHARD[index]
            + critical.EXPECTED_RESIDUAL_BY_SHARD[index]
        )


@pytest.mark.parametrize(
    ("record", "expected"),
    (
        (NO_DEGREE2_GRAPH6, critical.NO_DEGREE2_CLASS),
        (SUPPRESSIBLE_GRAPH6, critical.SUPPRESSIBLE_CLASS),
        (COMMON_MISSING_GRAPH6, critical.COMMON_MISSING_CLASS),
        (RESIDUAL_GRAPH6, critical.RESIDUAL_CLASS),
    ),
)
def test_exact_partition_on_real_catalogue_records(
    record: str, expected: str
) -> None:
    graph = decode_graph6(record)
    assert len(graph.edges) == 23
    assert min(graph.degrees) >= 2
    assert max(graph.degrees) <= 5
    assert critical.degree2_partition_class(graph) == expected
    profiles = critical._degree2_local_profiles(graph)
    if expected == critical.NO_DEGREE2_CLASS:
        assert profiles == []
    elif expected == critical.RESIDUAL_CLASS:
        assert profiles
        assert all(row["neighbours_adjacent"] for row in profiles)
        assert all(
            row["neighbour_degrees"] == [5, 5] for row in profiles
        )


def test_identity_freezes_full_catalogue_and_partition_semantics(
    frozen_runtime,
) -> None:
    identity = critical.build_identity(
        critical.config_for_shard(8, 60)
    )
    assert identity["campaign"] == critical.CAMPAIGN
    assert identity["shard"] == [8, 16]
    assert identity["edge_range"] == [23, 23]
    assert identity["generator_degree_range"] == [2, 5]
    assert identity["expected_generated"] == 187_137
    assert identity["expected_partition_counts"] == {
        "generated": 187_137,
        "filtered_no_degree2": 101_168,
        "filtered_suppressible": 60_258,
        "filtered_common_missing": 13_431,
        "eligible_residual": 12_280,
    }
    assert identity["catalogue_command"] == [
        "/frozen/tools/geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "23:23",
        "8/16",
    ]
    assert identity["positive_basis"][critical.NO_DEGREE2_CLASS] == (
        "external_disjoint_campaigns"
    )
    assert identity["positive_basis"][critical.SUPPRESSIBLE_CLASS] == (
        "degree2_suppression_extension_lemma"
    )
    assert identity["fixed_campaign_contract"][
        "caller_configurable_catalogue"
    ] is False


@pytest.mark.parametrize(
    "value",
    ("0/64", "16/16", "-1/16", "00/16", "0/016", "0/16/1", "0"),
)
def test_shard_parser_requires_canonical_i_over_16(value: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        critical.parse_shard(value)


def test_pause_resume_records_all_partition_events_and_completes(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
    small_denominators,
) -> None:
    ordered = (
        SUPPRESSIBLE_GRAPH6,
        NO_DEGREE2_GRAPH6,
        RESIDUAL_GRAPH6,
        COMMON_MISSING_GRAPH6,
    )
    _records(monkeypatch, *ordered)
    monkeypatch.setattr(
        critical.coloring_search,
        "evaluate_coloring_instance",
        _sat_evaluator,
    )
    config = critical.config_for_shard(0, 30)
    output = tmp_path / "shard-0"
    first = critical.run_degree2_critical_search(
        config, wall_seconds=60, output=output, max_cases=2
    )
    assert first["status"] == "paused_budget"
    assert first["generated"] == 2
    assert first["filtered_suppressible"] == 1
    assert first["filtered_no_degree2"] == 1
    assert first["eligible"] == 0

    second = critical.run_degree2_critical_search(
        config, wall_seconds=60, output=output
    )
    assert second["status"] == "complete"
    assert {
        key: second[key] for key in critical._COUNTER_KEYS
    } == {
        "generated": 4,
        "filtered_no_degree2": 1,
        "filtered_suppressible": 1,
        "filtered_common_missing": 1,
        "eligible": 1,
        "sat": 1,
        "unsat": 0,
        "timeouts": 0,
        "unknown": 0,
    }
    events = [
        json.loads(line)
        for line in (output / "events.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert [event["index"] for event in events] == [0, 1, 2, 3]
    assert events[0]["status"] == "theorem_filtered"
    assert events[0]["mathematical_positive_claimed"] is True
    assert events[1]["status"] == "partition_filtered"
    assert events[1]["positive_basis"] == "external_disjoint_campaigns"
    assert events[1]["mathematical_positive_claimed"] is False
    assert events[2]["status"] == "sat"
    assert events[2]["verified_coloring"] == list(RESIDUAL_COLORING)
    assert events[3]["status"] == "theorem_filtered"


def test_wrong_partition_tamper_is_rejected_on_resume(
    tmp_path: Path,
    monkeypatch,
    frozen_runtime,
    small_denominators,
) -> None:
    _records(monkeypatch, SUPPRESSIBLE_GRAPH6, NO_DEGREE2_GRAPH6)
    config = critical.config_for_shard(0, 30)
    output = tmp_path / "tamper"
    critical.run_degree2_critical_search(
        config, wall_seconds=60, output=output, max_cases=1
    )
    event_path = output / "events.jsonl"
    event = json.loads(event_path.read_text())
    event["partition_class"] = critical.RESIDUAL_CLASS
    event_path.write_text(json.dumps(event) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="partition decision"):
        critical.run_degree2_critical_search(
            config, wall_seconds=60, output=output, max_cases=1
        )


def test_resume_fails_closed_after_source_identity_drift(
    tmp_path: Path,
    monkeypatch,
    small_denominators,
) -> None:
    _records(monkeypatch, SUPPRESSIBLE_GRAPH6, NO_DEGREE2_GRAPH6)
    monkeypatch.setattr(
        critical, "_runtime_provenance", lambda: _provenance("a")
    )
    output = tmp_path / "drift"
    config = critical.config_for_shard(0, 30)
    critical.run_degree2_critical_search(
        config, wall_seconds=60, output=output, max_cases=1
    )
    monkeypatch.setattr(
        critical, "_runtime_provenance", lambda: _provenance("d")
    )
    with pytest.raises(ValueError, match="full frozen search config"):
        critical.run_degree2_critical_search(
            config, wall_seconds=60, output=output, max_cases=1
        )


def test_runtime_provenance_binds_only_runner_and_coloring(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        critical.coloring_search,
        "toolchain_fingerprint",
        lambda names: _toolchain(),
    )
    provenance = critical._runtime_provenance()
    records = provenance["implementation"]["files"]
    assert [record["role"] for record in records] == [
        "degree2_critical_runner",
        "shared_coloring",
    ]
    assert Path(records[0]["path"]).resolve() == Path(
        critical.__file__
    ).resolve()
    assert Path(records[1]["path"]).resolve() == Path(
        critical.coloring_search.__file__
    ).resolve()


class _FakeProcess:
    def __init__(self, stdout: str, return_code: int):
        self.stdout = io.StringIO(stdout)
        self.returncode = None
        self._return_code = return_code

    def wait(self, timeout=None):
        self.returncode = self._return_code
        return self.returncode

    def poll(self):
        return self.returncode

    def terminate(self):
        self.returncode = self._return_code

    def kill(self):
        self.returncode = self._return_code


def test_catalogue_stream_rejects_nonzero_exit_and_uses_no_shell(
    monkeypatch,
) -> None:
    process = _FakeProcess(SUPPRESSIBLE_GRAPH6 + "\n", 7)
    launches = []

    def popen(command, **kwargs):
        launches.append((command, kwargs))
        return process

    monkeypatch.setattr(critical.subprocess, "Popen", popen)
    monkeypatch.setattr(
        critical, "_catalogue_environment", lambda path: {"LC_ALL": "C"}
    )
    monkeypatch.setattr(
        critical.Path, "resolve", lambda path: path
    )
    monkeypatch.setattr(
        critical.Path, "is_symlink", lambda path: False
    )
    monkeypatch.setattr(
        critical.Path, "is_file", lambda path: True
    )
    command = [
        "/frozen/tools/geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "23:23",
        "0/16",
    ]
    with pytest.raises(RuntimeError, match="failed \\(7\\)"):
        list(critical._iter_catalogue_records(command))
    assert len(launches) == 1
    assert launches[0][0] == command
    assert "shell" not in launches[0][1]


def test_noncanonical_catalogue_command_is_rejected_before_launch() -> None:
    with pytest.raises(RuntimeError, match="frozen catalogue"):
        list(
            critical._iter_catalogue_records(
                [
                    "/frozen/tools/geng",
                    "-q",
                    "-C",
                    "-d3",
                    "-D5",
                    "11",
                    "23:23",
                    "0/16",
                ]
            )
        )
