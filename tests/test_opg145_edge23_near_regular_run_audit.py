from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

import pytest

import amra.discovery.opg145_dense_run_audit as base_audit
import amra.discovery.opg145_edge23_near_regular_run_audit as near_audit


NEAR_GRAPH6 = "J?AFbY[}Bw?"
NON_NEAR_GRAPH6 = "J~KWWKF_]@?"
COLORING = [
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
        near_audit, "EXPECTED_BY_SHARD", dict(TEST_COUNTS)
    )
    monkeypatch.setattr(
        near_audit, "EXPECTED_TOTAL", sum(TEST_COUNTS.values())
    )


@pytest.fixture
def replay_catalogue(monkeypatch):
    def iterate(identity, geng):
        shard = identity["shard"][0]
        assert identity["catalogue_command_canonical"] == [
            "geng",
            "-q",
            "-C",
            "-d4",
            "-D5",
            "11",
            "23:23",
            f"{shard}/16",
        ]
        yield from [NEAR_GRAPH6] * TEST_COUNTS[shard]

    monkeypatch.setattr(base_audit, "_iter_recorded_catalogue", iterate)


def _implementation_record() -> dict[str, object]:
    digest = hashlib.sha256()
    records = []
    for role, raw_path in near_audit.EXPECTED_IMPLEMENTATION_FILES:
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
    canonical = [
        "geng",
        "-q",
        "-C",
        "-d4",
        "-D5",
        "11",
        "23:23",
        f"{shard}/16",
    ]
    manifest = {
        "method": (
            "independent_per_shard_graph6_line_count_with_nonquiet_u_"
            "total_crosscheck"
        ),
        "per_shard_catalogue_command_canonical": [
            "geng",
            "-q",
            "-C",
            "-d4",
            "-D5",
            "11",
            "23:23",
            "i/16",
        ],
        "per_shard_count_operation": "count_stdout_graph6_records",
        "total_count_command_canonical": [
            "geng",
            "-C",
            "-d4",
            "-D5",
            "-u",
            "11",
            "23:23",
        ],
        "edge_range": [23, 23],
        "degree_range": [4, 5],
        "degree_sequence_descending": [5, 5] + [4] * 9,
        "shard_count": 16,
        "per_shard": {
            str(index): TEST_COUNTS[index] for index in range(16)
        },
        "total": sum(TEST_COUNTS.values()),
    }
    return {
        "campaign": near_audit.CAMPAIGN,
        "problem": "opg145",
        "order": 11,
        "edge_range": [23, 23],
        "degree_range": [4, 5],
        "degree_sequence_descending": [5, 5] + [4] * 9,
        "shard": [shard, 16],
        "expected_generated": TEST_COUNTS[shard],
        "expected_denominator_manifest": manifest,
        "color_count": 7,
        "known_positive_filter": "is_three_sparse",
        "catalogue_command": [
            toolchain["geng"]["path"],
            *canonical[1:],
        ],
        "catalogue_command_canonical": canonical,
        "per_instance_seconds": 60.0,
        "checkpoint_interval_records": 1,
        "event_policy": "one_fsynced_event_per_generated_record",
        "fixed_campaign_contract": {
            "order": 11,
            "edge_count": 23,
            "minimum_degree": 4,
            "maximum_degree": 5,
            "degree_sequence_descending": [5, 5] + [4] * 9,
            "shard_notation": "i/16",
            "caller_configurable_catalogue": False,
        },
        "implementation": _implementation_record(),
        "toolchain": copy.deepcopy(toolchain),
    }


def _sat_event(index: int, identity_sha: str) -> dict[str, object]:
    graph = base_audit.decode_graph6_independently(NEAR_GRAPH6)
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
        "event_schema": near_audit.EVENT_SCHEMA,
        "identity_sha256": identity_sha,
        "time_unix": 1_785_301_142.0 + index,
        "problem": "opg145",
        "order": 11,
        "index": index,
        "graph6": NEAR_GRAPH6,
        "vertices": 11,
        "edge_count": 23,
        "edges": [list(edge) for edge in graph.edges],
        "degrees": list(graph.degrees),
        "three_sparse": False,
        "eligible": True,
        "status": "sat",
        "elapsed_seconds": 0.01,
        "variables": 23 * 7,
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
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    identity_sha = base_audit._json_sha256(identity)
    for index, event in enumerate(events):
        event["index"] = index
        event["identity_sha256"] = identity_sha
    payload = "".join(
        json.dumps(event, sort_keys=True) + "\n" for event in events
    ).encode()
    (directory / "events.jsonl").write_bytes(payload)
    generated = len(events)
    filtered = sum(
        event["status"] == "filtered_three_sparse" for event in events
    )
    state: dict[str, object] = {
        "checkpoint_schema": near_audit.CHECKPOINT_SCHEMA,
        "identity": identity,
        "identity_sha256": identity_sha,
        "status": "complete",
        "next_index": generated,
        "generated": generated,
        "filtered_three_sparse": filtered,
        "eligible": generated - filtered,
        "sat": sum(event["status"] == "sat" for event in events),
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


def _make_shard(
    root: Path,
    shard: int,
    toolchain: dict[str, object],
) -> tuple[Path, dict[str, object], list[dict[str, object]]]:
    identity = _identity(shard, toolchain)
    identity_sha = base_audit._json_sha256(identity)
    events = [
        _sat_event(index, identity_sha)
        for index in range(TEST_COUNTS[shard])
    ]
    directory = root / f"shard-{shard}"
    _write_run(directory, identity, events)
    return directory, identity, events


def test_independent_degree_and_witness_checks() -> None:
    graph = base_audit.decode_graph6_independently(NEAR_GRAPH6)
    assert tuple(sorted(graph.degrees, reverse=True)) == (5, 5) + (4,) * 9
    near_audit._validate_near_regular_catalogue_graph(graph)
    assert base_audit.verify_acyclic_seven_edge_coloring_independently(
        graph, COLORING
    )
    with pytest.raises(
        near_audit.NearRegularRunAuditError, match="degree sequence"
    ):
        near_audit._validate_near_regular_catalogue_graph(
            base_audit.decode_graph6_independently(NON_NEAR_GRAPH6)
        )


def test_complete_shard_reports_both_auditor_hashes(
    tmp_path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, _, _ = _make_shard(tmp_path, 0, frozen_toolchain)
    report = near_audit.audit_near_regular_shard(
        directory, expected_shard=0
    )
    assert report["status"] == "verified_complete"
    assert report["shard"] == [0, 16]
    assert report["audited_counts"]["sat"] == 2
    provenance = report["auditor_provenance"]
    assert provenance["near_regular_contract_wrapper"]["sha256"] == (
        base_audit._file_sha256(Path(near_audit.__file__).resolve())
    )
    assert provenance["independent_base_engine"]["sha256"] == (
        base_audit._file_sha256(Path(base_audit.__file__).resolve())
    )


@pytest.mark.parametrize(
    ("attack", "message"),
    (
        ("campaign", "field drift: campaign"),
        ("manifest", "field drift: expected_denominator_manifest"),
        ("degrees", "field drift: degree_sequence_descending"),
        ("command", "exact frozen near-regular command"),
        ("extra", "field set has drifted"),
    ),
)
def test_identity_attacks_fail_closed(
    attack,
    message,
    tmp_path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    if attack == "campaign":
        identity["campaign"] = "forged"
    elif attack == "manifest":
        identity["expected_denominator_manifest"]["total"] += 1
    elif attack == "degrees":
        identity["degree_sequence_descending"][-1] = 3
    elif attack == "command":
        identity["catalogue_command_canonical"][3] = "-d2"
    else:
        identity["unexpected"] = True
    _write_run(directory, identity, events)
    with pytest.raises(near_audit.NearRegularRunAuditError, match=message):
        near_audit.audit_near_regular_shard(
            directory, expected_shard=0
        )


@pytest.mark.parametrize(
    ("attack", "message"),
    (
        ("role", "role/order drift"),
        ("path", "directory drift"),
        ("hash", "hash changed"),
        ("tool", "tool hash changed"),
        ("dependency", "dependency hash changed"),
    ),
)
def test_source_tool_and_dependency_attacks_fail_closed(
    attack,
    message,
    tmp_path,
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
        copied = tmp_path / "copied.py"
        copied.write_bytes(Path(records[0]["path"]).read_bytes())
        records[0]["path"] = str(copied)
        aggregate = hashlib.sha256()
        for record in records:
            aggregate.update(record["path"].encode())
            aggregate.update(record["sha256"].encode())
        identity["implementation"]["aggregate_sha256"] = aggregate.hexdigest()
    elif attack == "hash":
        records[2]["sha256"] = "0" * 64
    elif attack == "tool":
        identity["toolchain"]["minisat"]["sha256"] = "0" * 64
    else:
        dependencies = identity["toolchain"]["geng"][
            "dynamic_linkage"
        ]["dependencies"]
        next(iter(dependencies.values()))["sha256"] = "0" * 64
    _write_run(directory, identity, events)
    with pytest.raises(near_audit.NearRegularRunAuditError, match=message):
        near_audit.audit_near_regular_shard(
            directory, expected_shard=0
        )


@pytest.mark.parametrize(
    ("attack", "message"),
    (
        ("schema", "identity/index drift"),
        ("witness", "invalid witness"),
        ("filter", "three-sparse"),
        ("payload", "graph payload"),
    ),
)
def test_event_and_witness_attacks_fail_closed(
    attack,
    message,
    tmp_path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    if attack == "schema":
        events[0]["event_schema"] = "forged"
    elif attack == "witness":
        events[0]["verified_coloring"] = [0] * 23
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
        events[0]["degrees"][0] = 3
    _write_run(directory, identity, events)
    with pytest.raises(near_audit.NearRegularRunAuditError, match=message):
        near_audit.audit_near_regular_shard(
            directory, expected_shard=0
        )


def test_non_near_regenerated_record_and_counter_stuffing_fail(
    tmp_path,
    frozen_toolchain,
    small_denominators,
    monkeypatch,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    monkeypatch.setattr(
        base_audit,
        "_iter_recorded_catalogue",
        lambda identity, geng: iter((NON_NEAR_GRAPH6, NEAR_GRAPH6)),
    )
    with pytest.raises(
        near_audit.NearRegularRunAuditError, match="degree sequence"
    ):
        near_audit.audit_near_regular_shard(
            directory, expected_shard=0
        )
    _write_run(directory, identity, events, state_overrides={"sat": 3})
    with pytest.raises(
        near_audit.NearRegularRunAuditError, match="accounting"
    ):
        near_audit.audit_near_regular_shard(
            directory, expected_shard=0
        )


def test_sixteen_shard_root_and_adapter_restoration(
    tmp_path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    root = tmp_path / "campaign"
    for shard in range(16):
        _make_shard(root, shard, frozen_toolchain)
    report = near_audit.audit_near_regular_campaign(root)
    assert report["audited_total"] == sum(TEST_COUNTS.values())
    assert len(report["shards"]) == 16
    (root / "unexpected").mkdir()
    with pytest.raises(near_audit.NearRegularRunAuditError, match="drifted"):
        near_audit.audit_near_regular_campaign(root)
