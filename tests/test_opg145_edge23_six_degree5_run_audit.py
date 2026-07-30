from __future__ import annotations

import copy
import hashlib
import io
import json
import os
from pathlib import Path

import pytest

import amra.discovery.opg145_dense_run_audit as base_audit
import amra.discovery.opg145_edge23_six_degree5_run_audit as six_audit


TARGET_GRAPH6 = "J?AFBjw}FW?"
WRONG_DEGREES_GRAPH6 = "J?AFbY[}Bw?"
COLORING = [
    0,
    6,
    2,
    3,
    0,
    4,
    3,
    1,
    5,
    4,
    2,
    0,
    1,
    4,
    3,
    1,
    2,
    0,
    3,
    1,
    0,
    5,
    2,
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
        for name in ("geng", "pickg", "minisat", "cadical", "drat-trim")
    }


@pytest.fixture
def small_denominators(monkeypatch):
    monkeypatch.setattr(
        six_audit, "EXPECTED_BY_SHARD", dict(TEST_COUNTS)
    )
    monkeypatch.setattr(
        six_audit, "EXPECTED_TOTAL", sum(TEST_COUNTS.values())
    )


@pytest.fixture
def replay_catalogue(monkeypatch):
    def iterate(identity, geng):
        shard = identity["shard"][0]
        assert identity["catalogue_command_canonical"] == [
            "geng",
            "-q",
            "-C",
            "-d3",
            "-D5",
            "11",
            "23:23",
            f"{shard}/16",
        ]
        assert identity["catalogue_filter_command_canonical"] == [
            "pickg",
            "-q",
            "-M6",
        ]
        yield from [TARGET_GRAPH6] * TEST_COUNTS[shard]

    monkeypatch.setattr(six_audit, "_iter_exact_pipeline", iterate)


def _implementation_record() -> dict[str, object]:
    digest = hashlib.sha256()
    records = []
    for role, raw_path in six_audit.EXPECTED_IMPLEMENTATION_FILES:
        path = raw_path.resolve()
        sha = base_audit._file_sha256(path)
        records.append({"role": role, "path": str(path), "sha256": sha})
        digest.update(str(path).encode())
        digest.update(sha.encode())
    return {"aggregate_sha256": digest.hexdigest(), "files": records}


def _identity(
    shard: int, toolchain: dict[str, object]
) -> dict[str, object]:
    geng_canonical = [
        "geng",
        "-q",
        "-C",
        "-d3",
        "-D5",
        "11",
        "23:23",
        f"{shard}/16",
    ]
    pickg_canonical = ["pickg", "-q", "-M6"]
    manifest = {
        "method": "independent_exact_pipeline_graph6_line_count",
        "per_shard_pipeline_canonical": [
            [
                "geng",
                "-q",
                "-C",
                "-d3",
                "-D5",
                "11",
                "23:23",
                "i/16",
            ],
            ["pickg", "-q", "-M6"],
        ],
        "pipeline_transport": "stdout_pipe_two_popen_no_shell",
        "per_shard_count_operation": "count_filtered_stdout_graph6_records",
        "edge_range": [23, 23],
        "generator_degree_range": [3, 5],
        "maximum_degree_vertex_count": 6,
        "degree_sequence_descending": [5] * 6 + [4] + [3] * 4,
        "degree_sequence_derivation": (
            "sum(deg)=46; average>4 and D5 force maximum degree 5; "
            "M6 gives six degree-5 vertices; the five remaining degrees "
            "are in 3..4 and sum to 16, hence (4,3,3,3,3)"
        ),
        "shard_count": 16,
        "per_shard": {
            str(index): TEST_COUNTS[index] for index in range(16)
        },
        "total": sum(TEST_COUNTS.values()),
    }
    return {
        "campaign": six_audit.CAMPAIGN,
        "problem": "opg145",
        "order": 11,
        "edge_range": [23, 23],
        "generator_degree_range": [3, 5],
        "maximum_degree_vertex_count": 6,
        "degree_sequence_descending": [5] * 6 + [4] + [3] * 4,
        "shard": [shard, 16],
        "expected_generated": TEST_COUNTS[shard],
        "expected_denominator_manifest": manifest,
        "color_count": 7,
        "known_positive_filter": "is_three_sparse",
        "catalogue_command": [
            toolchain["geng"]["path"],
            *geng_canonical[1:],
        ],
        "catalogue_command_canonical": geng_canonical,
        "catalogue_filter_command": [
            toolchain["pickg"]["path"],
            *pickg_canonical[1:],
        ],
        "catalogue_filter_command_canonical": pickg_canonical,
        "catalogue_pipeline_transport": "stdout_pipe_two_popen_no_shell",
        "pipeline_environment_contract": {
            "locale": "C",
            "dynamic_library_directories": (
                "recorded_geng_and_pickg_dependency_parents"
            ),
            "removed_variables": ["LD_AUDIT", "LD_PRELOAD"],
        },
        "per_instance_seconds": 60.0,
        "checkpoint_interval_records": 1,
        "event_policy": "one_fsynced_event_per_generated_record",
        "fixed_campaign_contract": {
            "order": 11,
            "edge_count": 23,
            "minimum_degree": 3,
            "maximum_degree": 5,
            "maximum_degree_vertex_count": 6,
            "degree_sequence_descending": [5] * 6 + [4] + [3] * 4,
            "shard_notation": "i/16",
            "caller_configurable_catalogue": False,
        },
        "implementation": _implementation_record(),
        "toolchain": copy.deepcopy(toolchain),
    }


def _sat_event(index: int, identity_sha: str) -> dict[str, object]:
    graph = base_audit.decode_graph6_independently(TARGET_GRAPH6)
    cuts = 4
    base_clauses = (
        len(graph.edges) * 22
        + sum(
            degree * (degree - 1) // 2 * 7
            for degree in graph.degrees
        )
        + 1
    )
    return {
        "event_schema": six_audit.EVENT_SCHEMA,
        "identity_sha256": identity_sha,
        "time_unix": 1_785_301_142.0 + index,
        "problem": "opg145",
        "order": 11,
        "index": index,
        "graph6": TARGET_GRAPH6,
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
        "checkpoint_schema": six_audit.CHECKPOINT_SCHEMA,
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


def test_independent_degree_and_witness_verification() -> None:
    graph = base_audit.decode_graph6_independently(TARGET_GRAPH6)
    assert tuple(sorted(graph.degrees, reverse=True)) == (
        (5,) * 6 + (4,) + (3,) * 4
    )
    six_audit._validate_exact_catalogue_graph(graph)
    assert base_audit.verify_acyclic_seven_edge_coloring_independently(
        graph, COLORING
    )
    with pytest.raises(
        six_audit.SixDegree5RunAuditError, match="degree sequence"
    ):
        six_audit._validate_exact_catalogue_graph(
            base_audit.decode_graph6_independently(
                WRONG_DEGREES_GRAPH6
            )
        )


def test_complete_shard_reports_both_auditor_hashes(
    tmp_path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    directory, _, _ = _make_shard(tmp_path, 0, frozen_toolchain)
    report = six_audit.audit_six_degree5_shard(
        directory, expected_shard=0
    )
    assert report["status"] == "verified_complete"
    assert report["shard"] == [0, 16]
    assert report["audited_counts"]["sat"] == 2
    provenance = report["auditor_provenance"]
    assert provenance["six_degree5_contract_wrapper"]["sha256"] == (
        base_audit._file_sha256(Path(six_audit.__file__).resolve())
    )
    assert provenance["independent_base_engine"]["sha256"] == (
        base_audit._file_sha256(Path(base_audit.__file__).resolve())
    )


@pytest.mark.parametrize(
    ("attack", "message"),
    (
        ("campaign", "field drift: campaign"),
        ("manifest", "field drift: expected_denominator_manifest"),
        ("degree_sequence", "field drift: degree_sequence_descending"),
        ("geng_command", "exact frozen geng"),
        ("pickg_command", "exact frozen geng"),
        ("extra", "field set has drifted"),
    ),
)
def test_identity_and_pipeline_attacks_fail_closed(
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
    elif attack == "degree_sequence":
        identity["degree_sequence_descending"][-1] = 2
    elif attack == "geng_command":
        identity["catalogue_command_canonical"][3] = "-d2"
    elif attack == "pickg_command":
        identity["catalogue_filter_command_canonical"][-1] = "-M5"
    else:
        identity["unexpected"] = True
    _write_run(directory, identity, events)
    with pytest.raises(six_audit.SixDegree5RunAuditError, match=message):
        six_audit.audit_six_degree5_shard(
            directory, expected_shard=0
        )


@pytest.mark.parametrize(
    ("attack", "message"),
    (
        ("role", "role/order drift"),
        ("path", "directory drift"),
        ("hash", "hash changed"),
        ("pickg_tool", "tool hash changed: pickg"),
        ("pickg_dependency", "dependency hash changed: pickg"),
    ),
)
def test_source_pickg_and_dependency_attacks_fail_closed(
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
    elif attack == "pickg_tool":
        identity["toolchain"]["pickg"]["sha256"] = "0" * 64
    else:
        dependencies = identity["toolchain"]["pickg"][
            "dynamic_linkage"
        ]["dependencies"]
        next(iter(dependencies.values()))["sha256"] = "0" * 64
    _write_run(directory, identity, events)
    with pytest.raises(six_audit.SixDegree5RunAuditError, match=message):
        six_audit.audit_six_degree5_shard(
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
    with pytest.raises(six_audit.SixDegree5RunAuditError, match=message):
        six_audit.audit_six_degree5_shard(
            directory, expected_shard=0
        )


def test_wrong_regenerated_record_and_counter_stuffing_fail(
    tmp_path,
    frozen_toolchain,
    small_denominators,
    monkeypatch,
) -> None:
    directory, identity, events = _make_shard(
        tmp_path, 0, frozen_toolchain
    )
    monkeypatch.setattr(
        six_audit,
        "_iter_exact_pipeline",
        lambda identity, geng: iter(
            (WRONG_DEGREES_GRAPH6, TARGET_GRAPH6)
        ),
    )
    with pytest.raises(
        six_audit.SixDegree5RunAuditError, match="degree sequence"
    ):
        six_audit.audit_six_degree5_shard(
            directory, expected_shard=0
        )
    _write_run(directory, identity, events, state_overrides={"sat": 3})
    with pytest.raises(
        six_audit.SixDegree5RunAuditError, match="accounting"
    ):
        six_audit.audit_six_degree5_shard(
            directory, expected_shard=0
        )


def test_exact_sixteen_shard_root_and_adapter_restoration(
    tmp_path,
    frozen_toolchain,
    small_denominators,
    replay_catalogue,
) -> None:
    original = (
        base_audit.AUDIT_SCHEMA,
        base_audit.CHECKPOINT_SCHEMA,
        base_audit.EVENT_SCHEMA,
        base_audit.TOOL_NAMES,
        base_audit._validate_identity,
        base_audit._iter_recorded_catalogue,
    )
    root = tmp_path / "campaign"
    for shard in range(16):
        _make_shard(root, shard, frozen_toolchain)
    report = six_audit.audit_six_degree5_campaign(root)
    assert report["audited_total"] == sum(TEST_COUNTS.values())
    assert len(report["shards"]) == 16
    assert (
        base_audit.AUDIT_SCHEMA,
        base_audit.CHECKPOINT_SCHEMA,
        base_audit.EVENT_SCHEMA,
        base_audit.TOOL_NAMES,
        base_audit._validate_identity,
        base_audit._iter_recorded_catalogue,
    ) == original
    (root / "unexpected").mkdir()
    with pytest.raises(six_audit.SixDegree5RunAuditError, match="drifted"):
        six_audit.audit_six_degree5_campaign(root)


class _FakeProcess:
    def __init__(self, stdout: str, code: int):
        self.stdout = io.StringIO(stdout)
        self._code = code
        self.returncode = None

    def wait(self, timeout=None):
        self.returncode = self._code
        return self.returncode

    def poll(self):
        return self.returncode

    def terminate(self):
        self.returncode = self._code

    def kill(self):
        self.returncode = self._code


@pytest.mark.parametrize(
    ("geng_code", "pickg_code", "message"),
    ((4, 0, "geng=4, pickg=0"), (0, 5, "geng=0, pickg=5")),
)
def test_independent_pipeline_requires_both_return_codes(
    monkeypatch,
    geng_code,
    pickg_code,
    message,
) -> None:
    record = {
        "path": "/frozen/tool",
        "sha256": "a" * 64,
        "dynamic_linkage": {
            "ldd_exit": 0,
            "dependencies": {},
            "missing": [],
        },
    }
    identity = {
        "catalogue_command": ["/frozen/geng"],
        "catalogue_filter_command": ["/frozen/pickg", "-q", "-M6"],
        "toolchain": {"pickg": copy.deepcopy(record)},
    }
    geng_record = copy.deepcopy(record)
    geng = _FakeProcess("", geng_code)
    pickg = _FakeProcess(TARGET_GRAPH6 + "\n", pickg_code)
    processes = (geng, pickg)
    launches = []

    def popen(command, **kwargs):
        launches.append((command, kwargs))
        return processes[len(launches) - 1]

    monkeypatch.setattr(six_audit.subprocess, "Popen", popen)
    monkeypatch.setattr(
        six_audit.base_audit,
        "_current_dynamic_linkage",
        lambda path, environment: record["dynamic_linkage"],
    )
    with pytest.raises(six_audit.SixDegree5RunAuditError, match=message):
        list(six_audit._iter_exact_pipeline(identity, geng_record))
    assert len(launches) == 2
    assert "shell" not in launches[0][1]
    assert "shell" not in launches[1][1]
