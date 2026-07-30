from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

import pytest

import amra.discovery.opg145_dense_search as dense_search
import amra.discovery.opg145_edge23_four_degree5_search as four_search
from amra.discovery.opg_coloring_search import (
    SolverResult,
    proper_edge_coloring_cnf,
    verify_acyclic_edge_coloring,
)


TARGET_GRAPH6 = "J?AFBjYnBY?"
WRONG_DEGREES_GRAPH6 = "J?AFBjYnA]?"
TARGET_COLORING = (
    0,
    5,
    3,
    4,
    5,
    1,
    2,
    4,
    6,
    1,
    3,
    2,
    0,
    2,
    3,
    1,
    0,
    6,
    4,
    2,
    1,
    3,
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
        for name in (
            "geng",
            "pickg",
            "minisat",
            "cadical",
            "drat-trim",
        )
    }


def _provenance(marker: str = "a") -> dict[str, object]:
    return {
        "implementation": {
            "aggregate_sha256": marker * 64,
            "files": [
                {
                    "role": "four_degree5_wrapper",
                    "path": "/frozen/four.py",
                    "sha256": marker * 64,
                },
                {
                    "role": "dense_base_runner",
                    "path": "/frozen/dense.py",
                    "sha256": "b" * 64,
                },
                {
                    "role": "shared_coloring",
                    "path": "/frozen/coloring.py",
                    "sha256": "c" * 64,
                },
            ],
        },
        "toolchain": _toolchain(),
    }


@pytest.fixture
def frozen_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        four_search, "_runtime_provenance", lambda: _provenance()
    )


def _catalogue(
    monkeypatch: pytest.MonkeyPatch,
    *records: str,
) -> None:
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
        four_search, "_iter_filtered_catalogue_records", iterate
    )


def _sat_evaluator(problem, graph, timeout_seconds):
    assert problem == "opg145"
    assert timeout_seconds > 0
    assert graph.encoding == TARGET_GRAPH6
    assert tuple(sorted(graph.degrees, reverse=True)) == (
        (5,) * 4 + (4,) * 5 + (3,) * 2
    )
    assert verify_acyclic_edge_coloring(graph, TARGET_COLORING)
    return (
        SolverResult("sat", 0.01, frozenset(), "SAT", ""),
        proper_edge_coloring_cnf(graph, four_search.COLOR_COUNT),
        TARGET_COLORING,
        0,
        (),
    )


def test_frozen_denominators_and_configuration() -> None:
    assert four_search.EXPECTED_BY_SHARD == (
        18118,
        25131,
        32971,
        34344,
        29940,
        28464,
        28337,
        25230,
        40657,
        39482,
        26597,
        30604,
        27979,
        24268,
        28875,
        19621,
    )
    assert sum(four_search.EXPECTED_BY_SHARD) == 460_618
    assert four_search.DEGREE_SEQUENCE == (
        (5,) * 4 + (4,) * 5 + (3,) * 2
    )
    assert (
        four_search.config_for_shard(8, 60).expected_generated
        == 40_657
    )
    with pytest.raises(ValueError, match="denominator"):
        four_search.FourDegree5SearchConfig(0, 18_117, 60).validate()


@pytest.mark.parametrize(
    "value",
    ("0/64", "16/16", "-1/16", "00/16", "0/016", "0/16/1", "0"),
)
def test_parse_shard_accepts_only_canonical_i_over_16(value: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        four_search.parse_shard(value)


def test_identity_freezes_exact_pipeline(frozen_runtime: None) -> None:
    identity = four_search.build_identity(
        four_search.config_for_shard(8, 60)
    )
    assert identity["campaign"] == four_search.CAMPAIGN
    assert identity["maximum_degree_vertex_count"] == 4
    assert identity["degree_sequence_descending"] == (
        [5] * 4 + [4] * 5 + [3] * 2
    )
    assert identity["expected_generated"] == 40_657
    assert identity["catalogue_command_canonical"] == [
        "geng",
        "-q",
        "-C",
        "-d3",
        "-D5",
        "11",
        "23:23",
        "8/16",
    ]
    assert identity["catalogue_filter_command_canonical"] == [
        "pickg",
        "-q",
        "-M4",
    ]
    assert identity["expected_denominator_manifest"]["total"] == 460_618


def test_wrapper_imports_no_other_structured_wrapper() -> None:
    source = Path(four_search.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    amra_imports = {
        name for name in imported if name.startswith("amra.discovery")
    }
    assert amra_imports == {
        "amra.discovery.opg145_dense_search",
        "amra.discovery.opg_coloring_search",
    }


def test_exact_degree_validation() -> None:
    config = four_search.config_for_shard(0, 60)
    target = four_search.coloring_search.decode_graph6(TARGET_GRAPH6)
    four_search._validate_four_degree5_graph(target, config)
    wrong = four_search.coloring_search.decode_graph6(
        WRONG_DEGREES_GRAPH6
    )
    with pytest.raises(RuntimeError, match="degree sequence"):
        four_search._validate_four_degree5_graph(wrong, config)


def test_realistic_pause_resume_and_witness_events(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    frozen_runtime: None,
) -> None:
    _catalogue(
        monkeypatch,
        TARGET_GRAPH6,
        TARGET_GRAPH6,
        TARGET_GRAPH6,
    )
    monkeypatch.setattr(
        dense_search.coloring_search,
        "evaluate_coloring_instance",
        _sat_evaluator,
    )
    config = four_search.config_for_shard(0, 30)
    output = tmp_path / "shard-0"
    first = four_search.run_four_degree5_search(
        config,
        wall_seconds=60,
        output=output,
        max_cases=1,
    )
    second = four_search.run_four_degree5_search(
        config,
        wall_seconds=60,
        output=output,
        max_cases=1,
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
        == [5] * 4 + [4] * 5 + [3] * 2
        for event in events
    )


def test_delegate_restores_all_base_globals(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    frozen_runtime: None,
) -> None:
    original = (
        dense_search.CHECKPOINT_SCHEMA,
        dense_search.EVENT_SCHEMA,
        dense_search.build_identity,
        dense_search._iter_catalogue_records,
        dense_search._validate_catalogue_graph,
    )

    def broken(command):
        raise RuntimeError("synthetic pipeline failure")
        yield

    monkeypatch.setattr(
        four_search, "_iter_filtered_catalogue_records", broken
    )
    with pytest.raises(RuntimeError, match="synthetic pipeline"):
        four_search.run_four_degree5_search(
            four_search.config_for_shard(0, 30),
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
