from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

import pytest

import amra.discovery.opg145_dense_run_audit as base_audit
import amra.discovery.opg145_edge24_run_audit as edge24_audit


GRAPH24 = "J~KWWKF_]@_"
GRAPH25 = "J?BDdzs]fg?"
COLORING24 = [
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
]
TEST_COUNTS = {index: 1 for index in range(16)}
TEST_COUNTS[0] = 2


@pytest.fixture(scope="module")
def frozen_toolchain() -> dict[str, object]:
    tool_path = Path("/usr/bin/true").resolve()
    preliminary = base_audit._current_dynamic_linkage(
        tool_path, dict(os.environ)
    )
    preliminary_record: dict[str, object] = {
        "path": str(tool_path),
        "sha256": base_audit._file_sha256(tool_path),
        "dynamic_linkage": preliminary,
    }
    linkage = base_audit._current_dynamic_linkage(
        tool_path, base_audit._frozen_environment(preliminary_record)
    )
    record = {
        "path": str(tool_path),
        "sha256": base_audit._file_sha256(tool_path),
        "dynamic_linkage": linkage,
    }
    return {
        name: copy.deepcopy(record)
        for name in ("geng", "minisat", "cadical", "drat-trim")
    }


@pytest.fixture
def small_denominators(monkeypatch):
    monkeypatch.setattr(
        edge24_audit, "EXPECTED_BY_SHARD", dict(TEST_COUNTS)
    )
    monkeypatch.setattr(
        edge24_audit, "EXPECTED_TOTAL", sum(TEST_COUNTS.values())
    )


@pytest.fixture
def replay_catalogue(monkeypatch):
    def iterate(identity, geng):
        shard = identity["shard"][0]
        assert identity["catalogue_command_canonical"] == [
            "geng",
            "-q",
            "-C",
            "-d2",
            "-D5",
            "11",
            "24:24",
            f"{shard}/16",
        ]
        yield from [GRAPH24] * TEST_COUNTS[shard]

    monkeypatch.setattr(base_audit, "_iter_recorded_catalogue", iterate)


def _implementation_record() -> dict[str, object]:
    digest = hashlib.sha256()
    records = []
    for role, raw_path in edge24_audit.EXPECTED_IMPLEMENTATION_FILES:
        path = raw_path.resolve()
        sha = base_audit._file_sha256(path)
        records.append(
            {"role": role, "path": str(path), "sha256": sha}
        )
        digest.update(str(path).encode("utf-8"))
        digest.update(sha.encode("ascii"))
    return {"aggregate_sha256": digest.hexdigest(), "files": records}


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
        "24:24",
        f"{shard}/16",
    ]
    return {
        "campaign": edge24_audit.CAMPAIGN,
        "problem": "opg145",
        "order": 11,
        "edge_range": [24, 24],
        "shard": [shard, 16],
        "expected_generated": TEST_COUNTS[shard],
        "expected_denominator_manifest": {
            "method": (
                "independent_per_shard_graph6_line_count_with_nonquiet_u_"
                "total_crosscheck"
            ),
            "per_shard_catalogue_command_canonical": [
                "geng",
                "-q",
                "-C",
                "-d2",
                "-D5",
                "11",
                "24:24",
                "i/16",
            ],
            "per_shard_count_operation": "count_stdout_graph6_records",
            "total_count_command_canonical": [
                "geng",
                "-C",
                "-d2",
                "-D5",
                "-u",
                "11",
                "24:24",
            ],
            "edge_range": [24, 24],
            "shard_count": 16,
            "per_shard": {
                str(index): TEST_COUNTS[index] for index in range(16)
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
        "fixed_campaign_contract": {
            "order": 11,
            "edge_count": 24,
            "shard_notation": "i/16",
            "caller_configurable_catalogue": False,
        },
        "implementation": _implementation_record(),
        "toolchain": copy.deepcopy(toolchain),
    }


def _sat_event(index: int, identity_sha: str) -> dict[str, object]:
    graph = base_audit.decode_graph6_independently(GRAPH24)
    cuts = 5
    base_clauses = (
        len(graph.edges) * 22
        + sum(
            degree * (degree - 1) // 2 * 7
            for degree in graph.degrees
        )
        + 1
    )
    return {
        "event_schema": edge24_audit.EVENT_SCHEMA,
        "identity_sha256": identity_sha,
        "time_unix": 1_785_301_142.0 + index,
        "problem": "opg145",
        "order": 11,
        "index": index,
        "graph6": GRAPH24,
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
        "verified_coloring": list(COLORING24),
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
    identity_sha = base_audit._json_sha256(identity)
    for index, event in enumerate(events):
        event["index"] = index
        event["identity_sha256"] = identity_sha
    payload = "".join(
        json.dumps(event, sort_keys=True) + "\n" for event in events
    ).encode("utf-8")
    (directory / "events.jsonl").write_bytes(payload)
    generated = len(events)
    filtered = sum(
        event["status"] == "filtered_three_sparse" for event in events
    )
    sat = sum(event["status"] == "sat" for event in events)
    state: dict[str, object] = {
        "checkpoint_schema": edge24_audit.CHECKPOINT_SCHEMA,
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
        "events_sha256": hashlib.sha256(payload).hexdigest(),
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
    identity_sha = base_audit._json_sha256(identity)
    events = [
        _sat_event(index, identity_sha)
        for index in range(TEST_COUNTS[shard])
    ]
    directory = root / f"shard-{shard}"
    _write_run(directory, identity, events)
    return directory, identity, events


def test_exact_constants_and_independent_witness_primitives() -> None:
    assert edge24_audit.EXPECTED_TOTAL == 1_003_287
    assert sum(edge24_audit.EXPECTED_BY_SHARD.values()) == 1_003_287
    assert edge24_audit.EXPECTED_BY_SHARD[15] == 73_206
    graph = base_audit.decode_graph6_independently(GRAPH24)
    assert graph.vertex_count == 11
    assert len(graph.edges) == 24
    assert not base_audit.is_three_sparse_independently(graph)
    assert base_audit.verify_acyclic_seven_edge_coloring_independently(
        graph, COLORING24
    )


def test_complete_shard_replays_and_reports_both_auditor_hashes(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, _, _ = _make_shard(tmp_path, 0, frozen_toolchain)
    report = edge24_audit.audit_edge24_shard(
        directory, expected_shard=0
    )
    assert report["audit_schema"] == edge24_audit.AUDIT_SCHEMA
    assert report["status"] == "verified_complete"
    assert report["shard"] == [0, 16]
    assert report["expected_generated"] == 2
    assert report["audited_counts"]["sat"] == 2
    provenance = report["auditor_provenance"]
    wrapper = provenance["edge24_contract_wrapper"]
    engine = provenance["independent_base_engine"]
    assert wrapper == {
        "path": str(Path(edge24_audit.__file__).resolve()),
        "sha256": base_audit._file_sha256(
            Path(edge24_audit.__file__).resolve()
        ),
    }
    assert engine == {
        "path": str(Path(base_audit.__file__).resolve()),
        "sha256": base_audit._file_sha256(
            Path(base_audit.__file__).resolve()
        ),
    }
    assert "auditor_sha256" not in report


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        (
            lambda identity: identity.update({"campaign": "forged"}),
            "field drift: campaign",
        ),
        (
            lambda identity: identity["expected_denominator_manifest"].update(
                {"total": 17_000}
            ),
            "field drift: expected_denominator_manifest",
        ),
        (
            lambda identity: identity["fixed_campaign_contract"].update(
                {"shard_notation": "i/4"}
            ),
            "field drift: fixed_campaign_contract",
        ),
        (
            lambda identity: identity["catalogue_command_canonical"].__setitem__(
                -1, "0/4"
            ),
            "exact frozen edge-24 command",
        ),
        (
            lambda identity: identity.update({"unexpected": True}),
            "field set has drifted",
        ),
    ),
)
def test_identity_manifest_and_command_attacks_fail_closed(
    mutation,
    message: str,
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    mutation(identity)
    _write_run(directory, identity, events)
    with pytest.raises(edge24_audit.Edge24RunAuditError, match=message):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=0
        )


@pytest.mark.parametrize(
    ("attack", "message"),
    (
        ("role", "role/order drift"),
        ("path", "directory drift"),
        ("hash", "hash changed"),
        ("extra", "file set is incomplete"),
    ),
)
def test_three_source_role_path_hash_and_cardinality_attacks_fail_closed(
    attack: str,
    message: str,
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    records = identity["implementation"]["files"]
    if attack == "role":
        records[0]["role"], records[1]["role"] = (
            records[1]["role"],
            records[0]["role"],
        )
    elif attack == "path":
        original = Path(records[0]["path"])
        copied = tmp_path / "same-bytes-wrapper.py"
        copied.write_bytes(original.read_bytes())
        records[0]["path"] = str(copied)
        aggregate = hashlib.sha256()
        for record in records:
            aggregate.update(record["path"].encode("utf-8"))
            aggregate.update(record["sha256"].encode("ascii"))
        identity["implementation"]["aggregate_sha256"] = aggregate.hexdigest()
    elif attack == "hash":
        records[2]["sha256"] = "0" * 64
    else:
        records.append(copy.deepcopy(records[-1]))
    _write_run(directory, identity, events)
    with pytest.raises(edge24_audit.Edge24RunAuditError, match=message):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=0
        )


@pytest.mark.parametrize("target", ("tool", "dependency"))
def test_tool_and_dependency_hash_attacks_fail_closed(
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
        message = "tool hash changed"
    else:
        dependencies = identity["toolchain"]["geng"][
            "dynamic_linkage"
        ]["dependencies"]
        next(iter(dependencies.values()))["sha256"] = "0" * 64
        message = "dependency hash changed"
    _write_run(directory, identity, events)
    with pytest.raises(edge24_audit.Edge24RunAuditError, match=message):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=0
        )


@pytest.mark.parametrize(
    ("attack", "message"),
    (
        ("event_schema", "identity/index drift"),
        ("witness", "invalid witness"),
        ("filter", "three-sparse"),
        ("payload", "graph payload"),
    ),
)
def test_event_filter_witness_and_payload_attacks_fail_closed(
    attack: str,
    message: str,
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    if attack == "event_schema":
        events[0]["event_schema"] = "amra.opg145.n11-dense.event.v1"
    elif attack == "witness":
        events[0]["verified_coloring"] = [0] * 24
    elif attack == "filter":
        events[0].update(
            {
                "three_sparse": True,
                "eligible": False,
                "status": "filtered_three_sparse",
                "verified_coloring": None,
            }
        )
    else:
        events[0]["degrees"][0] += 1
    _write_run(directory, identity, events)
    with pytest.raises(edge24_audit.Edge24RunAuditError, match=message):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=0
        )


def test_running_status_and_counter_stuffing_fail_before_replay(
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
        base_audit,
        "_iter_recorded_catalogue",
        lambda identity, geng: pytest.fail("replay must not start"),
    )
    with pytest.raises(edge24_audit.Edge24RunAuditError, match="only after"):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=0
        )

    _write_run(
        directory,
        identity,
        events,
        state_overrides={"status": "complete", "sat": 3},
    )
    with pytest.raises(edge24_audit.Edge24RunAuditError, match="accounting"):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=0
        )


def test_missing_event_and_wrong_regenerated_edge_layer_fail_closed(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
    monkeypatch,
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
    with pytest.raises(edge24_audit.Edge24RunAuditError, match="missing event"):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=0
        )

    _write_run(directory, identity, events)
    monkeypatch.setattr(
        base_audit,
        "_iter_recorded_catalogue",
        lambda identity, geng: iter((GRAPH25, GRAPH24)),
    )
    with pytest.raises(
        edge24_audit.Edge24RunAuditError,
        match="violates frozen constraints",
    ):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=0
        )


def test_sixteen_shard_root_closes_and_rejects_any_layout_drift(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    root = tmp_path / "campaign"
    for shard in range(16):
        _make_shard(root, shard, frozen_toolchain)
    report = edge24_audit.audit_edge24_campaign(root)
    assert report["status"] == "verified_complete"
    assert report["shard_count"] == 16
    assert report["expected_total"] == sum(TEST_COUNTS.values())
    assert report["audited_total"] == sum(TEST_COUNTS.values())
    assert len(report["shards"]) == 16
    assert all(
        "edge24_contract_wrapper" in shard["auditor_provenance"]
        for shard in report["shards"]
    )

    (root / "worker-0.log").write_text("unexpected", encoding="utf-8")
    with pytest.raises(edge24_audit.Edge24RunAuditError, match="drifted"):
        edge24_audit.audit_edge24_campaign(root)


def test_shard_label_and_temporary_checkpoint_are_rejected(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, _, _ = _make_shard(tmp_path, 0, frozen_toolchain)
    with pytest.raises(edge24_audit.Edge24RunAuditError, match="layout"):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=1
        )
    (directory / "state.json.tmp").write_text("{}\n", encoding="utf-8")
    with pytest.raises(edge24_audit.Edge24RunAuditError, match="temporary"):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=0
        )


def test_adapter_restores_every_base_contract_after_failure(
    tmp_path: Path,
    frozen_toolchain,
    small_denominators,
    monkeypatch,
) -> None:
    directory, _, _ = _make_shard(tmp_path, 0, frozen_toolchain)
    names = (
        "AUDIT_SCHEMA",
        "CHECKPOINT_SCHEMA",
        "EVENT_SCHEMA",
        "MINIMUM_EDGES",
        "MAXIMUM_EDGES",
        "SHARD_COUNT",
        "EXPECTED_BY_SHARD",
        "EXPECTED_TOTAL",
        "_validate_identity",
    )
    originals = {name: getattr(base_audit, name) for name in names}

    def broken_replay(identity, geng):
        raise RuntimeError("synthetic replay failure")
        yield  # pragma: no cover

    monkeypatch.setattr(
        base_audit, "_iter_recorded_catalogue", broken_replay
    )
    with pytest.raises(RuntimeError, match="synthetic replay failure"):
        edge24_audit.audit_edge24_shard(
            directory, expected_shard=0
        )
    assert {
        name: getattr(base_audit, name) for name in names
    } == originals
