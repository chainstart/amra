from __future__ import annotations

import json
from pathlib import Path

import pytest

import amra.discovery.opg_coloring_run_audit as audit_module
from amra.discovery.opg_coloring_run_audit import (
    ColoringRunAuditError,
    audit_coloring_shard,
    independently_verify_acyclic_coloring,
)
from amra.discovery.opg_coloring_search import EdgeGraph


def test_independent_acyclic_checker_rejects_bichromatic_cycle() -> None:
    cycle = EdgeGraph(
        4,
        ((0, 1), (1, 2), (2, 3), (0, 3)),
        "manual-cycle",
    )
    assert independently_verify_acyclic_coloring(cycle, (0, 1, 2, 3))
    assert not independently_verify_acyclic_coloring(cycle, (0, 1, 0, 1))
    assert not independently_verify_acyclic_coloring(cycle, (0, 0, 1, 2))


def _write_complete_shard(directory: Path) -> None:
    state = {
        "checkpoint_schema": 2,
        "problem": "opg145",
        "lane": "default",
        "status": "complete",
        "shard": [0, 4],
        "minimum_order": 10,
        "maximum_order": 10,
        "next_order": 11,
        "next_index": 0,
        "implementation_sha256": (
            audit_module._search_implementation_fingerprint()
        ),
        "toolchain": {"geng": {}},
        "generated": 2,
        "filtered_known_positive": 1,
        "eligible": 1,
        "sat": 1,
        "unsat": 0,
        "timeouts": 0,
        "hard_queue": [],
    }
    event = {
        "problem": "opg145",
        "status": "sat",
        "order": 10,
        "index": 0,
        "encoding": "I~sGGC@_G",
        "vertices": 10,
        "edges": 15,
        "elapsed_seconds": 0.25,
        "lazy_cycle_cuts": 2,
        "verified_coloring": [
            0,
            3,
            1,
            4,
            2,
            0,
            1,
            5,
            3,
            0,
            1,
            0,
            6,
            6,
            0,
        ],
    }
    directory.mkdir()
    (directory / "state.json").write_text(
        json.dumps(state), encoding="utf-8"
    )
    (directory / "events.jsonl").write_text(
        json.dumps(event) + "\n", encoding="utf-8"
    )


def test_audit_closes_catalogue_binding_and_replays_witness(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "shard"
    _write_complete_shard(output)
    monkeypatch.setattr(
        audit_module,
        "_geng_tool_record",
        lambda state: {"sha256": "test-geng"},
    )
    monkeypatch.setattr(
        audit_module,
        "_iter_geng_catalogue",
        lambda tool, order, shard: iter(("I~sGGC@_G", "IhCGGC@_G")),
    )
    result = audit_coloring_shard(output, expected_generated=2)
    assert result["sat_witnesses_replayed"] == 1
    assert result["filtered_known_positive"] == 1
    assert result["catalogue_event_binding"] == "exact_index_and_graph6"
    assert result["status"] == "independently_verified"
    assert len(str(result["events_sha256"])) == 64
    assert len(str(result["auditor_sha256"])) == 64


def test_audit_rejects_incomplete_or_wrong_generator_count(
    tmp_path: Path,
) -> None:
    output = tmp_path / "shard"
    _write_complete_shard(output)
    with pytest.raises(ColoringRunAuditError, match="expected 3"):
        audit_coloring_shard(output, expected_generated=3)

    state_path = output / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "running"
    state_path.write_text(json.dumps(state), encoding="utf-8")
    with pytest.raises(ColoringRunAuditError, match="not complete"):
        audit_coloring_shard(output, expected_generated=2)


def test_audit_rejects_event_not_bound_to_eligible_catalogue_record(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "shard"
    _write_complete_shard(output)
    events_path = output / "events.jsonl"
    event = json.loads(events_path.read_text(encoding="utf-8"))
    event["index"] = 1
    events_path.write_text(json.dumps(event) + "\n", encoding="utf-8")
    monkeypatch.setattr(
        audit_module,
        "_geng_tool_record",
        lambda state: {"sha256": "test-geng"},
    )
    monkeypatch.setattr(
        audit_module,
        "_iter_geng_catalogue",
        lambda tool, order, shard: iter(("I~sGGC@_G", "IhCGGC@_G")),
    )
    with pytest.raises(ColoringRunAuditError, match="binding failed"):
        audit_coloring_shard(output, expected_generated=2)
