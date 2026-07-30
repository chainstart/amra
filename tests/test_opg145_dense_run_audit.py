from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

import pytest

import amra.discovery.opg145_dense_run_audit as run_audit


GRAPH6 = "J?BDdzs]fg?"
COLORING = [
    0,
    4,
    4,
    1,
    3,
    3,
    4,
    2,
    1,
    6,
    6,
    2,
    3,
    0,
    1,
    5,
    6,
    1,
    0,
    2,
    2,
    1,
    0,
    6,
    3,
]
TEST_COUNTS = {0: 2, 1: 1, 2: 1, 3: 1}


@pytest.fixture(scope="module")
def frozen_toolchain() -> dict[str, object]:
    tool_path = Path("/usr/bin/true").resolve()
    preliminary = run_audit._current_dynamic_linkage(
        tool_path, dict(os.environ)
    )
    preliminary_record: dict[str, object] = {
        "path": str(tool_path),
        "sha256": run_audit._file_sha256(tool_path),
        "dynamic_linkage": preliminary,
    }
    linkage = run_audit._current_dynamic_linkage(
        tool_path, run_audit._frozen_environment(preliminary_record)
    )
    record = {
        "path": str(tool_path),
        "sha256": run_audit._file_sha256(tool_path),
        "dynamic_linkage": linkage,
    }
    return {
        name: copy.deepcopy(record)
        for name in ("geng", "minisat", "cadical", "drat-trim")
    }


@pytest.fixture
def small_denominators(monkeypatch):
    monkeypatch.setattr(run_audit, "EXPECTED_BY_SHARD", dict(TEST_COUNTS))
    monkeypatch.setattr(run_audit, "EXPECTED_TOTAL", sum(TEST_COUNTS.values()))


@pytest.fixture
def replay_catalogue(monkeypatch):
    def iterate(identity, geng):
        assert identity["catalogue_command_canonical"] == [
            "geng",
            "-q",
            "-C",
            "-d2",
            "-D5",
            "11",
            "25:27",
            f"{identity['shard'][0]}/4",
        ]
        yield from [GRAPH6] * TEST_COUNTS[identity["shard"][0]]

    monkeypatch.setattr(run_audit, "_iter_recorded_catalogue", iterate)


def _implementation_record() -> dict[str, object]:
    digest = hashlib.sha256()
    files = []
    for raw_path in run_audit.EXPECTED_IMPLEMENTATION_PATHS:
        path = raw_path.resolve()
        sha = run_audit._file_sha256(path)
        files.append({"path": str(path), "sha256": sha})
        digest.update(str(path).encode("utf-8"))
        digest.update(sha.encode("ascii"))
    return {"aggregate_sha256": digest.hexdigest(), "files": files}


def _identity(
    shard: int, toolchain: dict[str, object]
) -> dict[str, object]:
    geng_path = toolchain["geng"]["path"]
    canonical = [
        "geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "25:27",
        f"{shard}/4",
    ]
    return {
        "campaign": "opg145_n11_dense_edge_layer",
        "problem": "opg145",
        "order": 11,
        "edge_range": [25, 27],
        "shard": [shard, 4],
        "expected_generated": TEST_COUNTS[shard],
        "expected_denominator_manifest": {
            "method": "independent_geng_count_with_u",
            "count_command_canonical": [
                "geng",
                "-q",
                "-C",
                "-d2",
                "-D5",
                "-u",
                "11",
                "25:27",
                "i/4",
            ],
            "edge_range": [25, 27],
            "shard_count": 4,
            "per_shard": {
                str(index): count for index, count in TEST_COUNTS.items()
            },
            "total": sum(TEST_COUNTS.values()),
        },
        "color_count": 7,
        "known_positive_filter": "is_three_sparse",
        "catalogue_command": [geng_path, *canonical[1:]],
        "catalogue_command_canonical": canonical,
        "per_instance_seconds": 60.0,
        "checkpoint_interval_records": 1,
        "event_policy": "one_fsynced_event_per_generated_record",
        "implementation": _implementation_record(),
        "toolchain": copy.deepcopy(toolchain),
    }


def _sat_event(index: int, identity_sha: str) -> dict[str, object]:
    graph = run_audit.decode_graph6_independently(GRAPH6)
    cuts = 17
    base_clauses = (
        len(graph.edges) * 22
        + sum(
            degree * (degree - 1) // 2 * 7
            for degree in graph.degrees
        )
        + 1
    )
    return {
        "event_schema": run_audit.EVENT_SCHEMA,
        "identity_sha256": identity_sha,
        "time_unix": 1_785_301_142.0 + index,
        "problem": "opg145",
        "order": 11,
        "index": index,
        "graph6": GRAPH6,
        "vertices": 11,
        "edge_count": len(graph.edges),
        "edges": [list(edge) for edge in graph.edges],
        "degrees": list(graph.degrees),
        "three_sparse": False,
        "eligible": True,
        "status": "sat",
        "elapsed_seconds": 0.01,
        "variables": len(graph.edges) * 7,
        "clauses": base_clauses + cuts,
        "cnf_sha256": "a" * 64,
        "lazy_cycle_cuts": cuts,
        "lazy_cycle_records_sha256": "b" * 64,
        "lazy_cycle_certificate": None,
        "verified_coloring": list(COLORING),
        "solver_stdout_sha256": "c" * 64,
        "solver_stderr_sha256": "d" * 64,
    }


def _write_run(
    directory: Path,
    identity: dict[str, object],
    events: list[dict[str, object]],
    *,
    state_overrides: dict[str, object] | None = None,
) -> dict[str, object]:
    directory.mkdir(parents=True, exist_ok=True)
    identity_sha = run_audit._json_sha256(identity)
    for index, event in enumerate(events):
        event["index"] = index
        event["identity_sha256"] = identity_sha
    events_payload = "".join(
        json.dumps(event, sort_keys=True) + "\n" for event in events
    ).encode("utf-8")
    (directory / "events.jsonl").write_bytes(events_payload)
    generated = len(events)
    filtered = sum(
        event["status"] == "filtered_three_sparse" for event in events
    )
    sat = sum(event["status"] == "sat" for event in events)
    state: dict[str, object] = {
        "checkpoint_schema": run_audit.CHECKPOINT_SCHEMA,
        "identity": identity,
        "identity_sha256": identity_sha,
        "status": "complete",
        "next_index": generated,
        "generated": generated,
        "filtered_three_sparse": filtered,
        "eligible": generated - filtered,
        "sat": sat,
        "unsat": 0,
        "timeouts": 0,
        "unknown": 0,
        "catalogue_exhausted": True,
        "events_sha256": hashlib.sha256(events_payload).hexdigest(),
    }
    if state_overrides:
        state.update(state_overrides)
    (directory / "state.json").write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return state


def _make_shard(
    root: Path,
    shard: int,
    frozen_toolchain: dict[str, object],
) -> tuple[Path, dict[str, object], list[dict[str, object]]]:
    identity = _identity(shard, frozen_toolchain)
    identity_sha = run_audit._json_sha256(identity)
    events = [
        _sat_event(index, identity_sha)
        for index in range(TEST_COUNTS[shard])
    ]
    directory = root / f"shard-{shard}"
    _write_run(directory, identity, events)
    return directory, identity, events


def test_independent_decoder_and_union_find_witness_checker() -> None:
    graph = run_audit.decode_graph6_independently(GRAPH6)
    assert graph.vertex_count == 11
    assert len(graph.edges) == 25
    assert not run_audit.is_three_sparse_independently(graph)
    assert run_audit.verify_acyclic_seven_edge_coloring_independently(
        graph, COLORING
    )
    improper = list(COLORING)
    improper[1] = improper[0]
    assert not run_audit.verify_acyclic_seven_edge_coloring_independently(
        graph, improper
    )


def test_complete_shard_replays_every_event_and_passes(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, _, _ = _make_shard(tmp_path, 0, frozen_toolchain)
    report = run_audit.audit_dense_shard(directory, expected_shard=0)
    assert report["status"] == "verified_complete"
    assert report["expected_generated"] == 2
    assert report["audited_counts"] == {
        "generated": 2,
        "filtered_three_sparse": 0,
        "eligible": 2,
        "sat": 2,
        "unsat": 0,
        "timeouts": 0,
        "unknown": 0,
    }


def test_audit_rejects_running_checkpoint_without_starting_replay(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    monkeypatch,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    _write_run(
        directory,
        identity,
        events,
        state_overrides={"status": "running"},
    )
    monkeypatch.setattr(
        run_audit,
        "_iter_recorded_catalogue",
        lambda identity, geng: pytest.fail("catalogue replay must not start"),
    )
    with pytest.raises(run_audit.DenseRunAuditError, match="only after"):
        run_audit.audit_dense_shard(directory, expected_shard=0)


def test_missing_event_and_stuffed_counters_fail_closed(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    _write_run(
        directory,
        identity,
        events[:1],
        state_overrides={
            "next_index": 2,
            "generated": 2,
            "eligible": 2,
            "sat": 2,
        },
    )
    with pytest.raises(run_audit.DenseRunAuditError, match="missing event"):
        run_audit.audit_dense_shard(directory, expected_shard=0)


def test_counter_tampering_fails_before_replay(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    _write_run(
        directory,
        identity,
        events,
        state_overrides={"sat": 3},
    )
    with pytest.raises(run_audit.DenseRunAuditError, match="accounting"):
        run_audit.audit_dense_shard(directory, expected_shard=0)


def test_tampered_sat_witness_fails_even_with_updated_events_hash(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    events[0]["verified_coloring"] = [0] * 25
    _write_run(directory, identity, events)
    with pytest.raises(run_audit.DenseRunAuditError, match="invalid witness"):
        run_audit.audit_dense_shard(directory, expected_shard=0)


def test_wrong_filter_decision_fails_with_consistent_forged_counters(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    events[0].update(
        {
            "three_sparse": True,
            "eligible": False,
            "status": "filtered_three_sparse",
            "verified_coloring": None,
        }
    )
    _write_run(directory, identity, events)
    with pytest.raises(run_audit.DenseRunAuditError, match="three-sparse"):
        run_audit.audit_dense_shard(directory, expected_shard=0)


def test_full_edge_payload_and_event_hash_are_both_bound(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    events[0]["edges"][0] = [0, 1]
    _write_run(directory, identity, events)
    with pytest.raises(run_audit.DenseRunAuditError, match="graph payload"):
        run_audit.audit_dense_shard(directory, expected_shard=0)

    directory, identity, events = _make_shard(
        tmp_path / "second", 0, frozen_toolchain
    )
    events_path = directory / "events.jsonl"
    events_path.write_bytes(events_path.read_bytes() + b" ")
    with pytest.raises(run_audit.DenseRunAuditError, match="events hash"):
        run_audit.audit_dense_shard(directory, expected_shard=0)


@pytest.mark.parametrize("target", ("tool", "dependency"))
def test_tool_and_every_recorded_dependency_hash_are_rechecked(
    target: str,
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    if target == "tool":
        identity["toolchain"]["minisat"]["sha256"] = "0" * 64
        expected_message = "tool hash changed"
    else:
        dependencies = identity["toolchain"]["geng"][
            "dynamic_linkage"
        ]["dependencies"]
        first_dependency = next(iter(dependencies.values()))
        first_dependency["sha256"] = "0" * 64
        expected_message = "dependency hash changed"
    _write_run(directory, identity, events)
    with pytest.raises(run_audit.DenseRunAuditError, match=expected_message):
        run_audit.audit_dense_shard(directory, expected_shard=0)


def test_implementation_directory_drift_fails_even_for_same_bytes(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    original = run_audit.EXPECTED_IMPLEMENTATION_PATHS[0].resolve()
    drifted = tmp_path / "copied-runner.py"
    drifted.write_bytes(original.read_bytes())
    record = identity["implementation"]["files"][0]
    record["path"] = str(drifted)
    aggregate = hashlib.sha256()
    for file_record in identity["implementation"]["files"]:
        aggregate.update(file_record["path"].encode("utf-8"))
        aggregate.update(file_record["sha256"].encode("ascii"))
    identity["implementation"]["aggregate_sha256"] = aggregate.hexdigest()
    _write_run(directory, identity, events)
    with pytest.raises(
        run_audit.DenseRunAuditError, match="directory drift"
    ):
        run_audit.audit_dense_shard(directory, expected_shard=0)


def test_four_shard_campaign_closes_and_rejects_layout_drift(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    root = tmp_path / "campaign"
    for shard in range(4):
        _make_shard(root, shard, frozen_toolchain)
    report = run_audit.audit_dense_campaign(root)
    assert report["status"] == "verified_complete"
    assert report["audited_total"] == sum(TEST_COUNTS.values())
    assert len(report["shards"]) == 4

    (root / "unexpected-directory").mkdir()
    with pytest.raises(run_audit.DenseRunAuditError, match="drifted"):
        run_audit.audit_dense_campaign(root)
