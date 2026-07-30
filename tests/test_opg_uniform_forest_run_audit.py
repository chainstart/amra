from __future__ import annotations

import json
from pathlib import Path

import pytest

import amra.discovery.opg_uniform_forest_run_audit as audit_module
from amra.discovery.opg_uniform_forest_run_audit import (
    UniformForestRunAuditError,
    _ValidatedGeng,
    audit_uniform_forest_shard,
)


_RECORD_0 = "H??Ff~~"
_RECORD_1 = "H??Fvz~"
_EVENT_0 = {
    "edges": 19,
    "elapsed_seconds": 0.1439949809864629,
    "graph6": _RECORD_0,
    "index": 0,
    "states": 45199,
    "status": "nonviolating",
    "strongest_pair": {
        "edge_e": [0, 6],
        "edge_f": [4, 7],
        "edge_indexes": [0, 8],
        "forest_count": 52032,
        "forest_count_e": 17256,
        "forest_count_ef": 6584,
        "forest_count_f": 19904,
        "left_product": 342578688,
        "margin": 884736,
        "right_product": 343463424,
    },
    "time": 1785296664.9447355,
    "vertices": 9,
}
_EVENT_1 = {
    "edges": 19,
    "elapsed_seconds": 0.15834675001678988,
    "graph6": _RECORD_1,
    "index": 1,
    "states": 54659,
    "status": "nonviolating",
    "strongest_pair": {
        "edge_e": [0, 6],
        "edge_f": [5, 7],
        "edge_indexes": [0, 10],
        "forest_count": 59136,
        "forest_count_e": 20160,
        "forest_count_ef": 7744,
        "forest_count_f": 22784,
        "left_product": 457949184,
        "margin": 1376256,
        "right_product": 459325440,
    },
    "time": 1785296665.09094,
    "vertices": 9,
}


def _best_from_event(event: dict[str, object]) -> dict[str, object]:
    pair = dict(event["strongest_pair"])  # type: ignore[arg-type]
    return {
        "index": event["index"],
        "graph6": event["graph6"],
        **pair,
    }


def _write_complete_shard(
    directory: Path,
    *,
    events: list[dict[str, object]],
    generated: int | None = None,
    best_pair: dict[str, object] | None = None,
) -> None:
    count = len(events) if generated is None else generated
    state = {
        "checkpoint_schema": 1,
        "problem": "opg1757",
        "connected_only": True,
        "order": 9,
        "minimum_edges": 19,
        "maximum_edges": 36,
        "shard": [0, 4],
        "implementation_sha256": audit_module._implementation_fingerprint(),
        "toolchain": {"geng": {}},
        "next_index": count,
        "generated": count,
        "evaluated": count,
        "nonviolating": count,
        "violations": 0,
        "timeouts": 0,
        "hard_queue": [],
        "best_pair": (
            _best_from_event(events[0])
            if best_pair is None and events
            else best_pair
        ),
        "status": "complete",
    }
    directory.mkdir()
    (directory / "state.json").write_text(
        json.dumps(state),
        encoding="utf-8",
    )
    (directory / "events.jsonl").write_text(
        "".join(json.dumps(event) + "\n" for event in events),
        encoding="utf-8",
    )


def _patch_catalogue(
    monkeypatch: pytest.MonkeyPatch,
    records: tuple[str, ...],
) -> None:
    monkeypatch.setattr(
        audit_module,
        "_validated_geng_tool",
        lambda state: _ValidatedGeng(
            Path("/test/geng"),
            "a" * 64,
            (),
            {"libtest.so": "b" * 64},
        ),
    )
    monkeypatch.setattr(
        audit_module,
        "_iter_geng_catalogue",
        lambda tool, **kwargs: iter(records),
    )


def test_audit_closes_catalogue_events_arithmetic_and_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "shard"
    _write_complete_shard(output, events=[_EVENT_0])
    _patch_catalogue(monkeypatch, (_RECORD_0,))

    result = audit_uniform_forest_shard(output, expected_generated=1)

    assert result["generated"] == 1
    assert result["events_replayed"] == 1
    assert result["catalogue_unique"] is True
    assert result["catalogue_event_binding"] == "exact_index_and_graph6"
    assert result["minimum_reported_margin"] == 884736
    assert result["status"] == (
        "execution_evidence_verified_with_counting_trust_boundary"
    )
    assert len(result["residual_trust_boundary"]) == 3


def test_missing_event_with_compensated_state_counts_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    replacement = json.loads(json.dumps(_EVENT_1))
    replacement["index"] = 2
    output = tmp_path / "shard"
    _write_complete_shard(
        output,
        events=[_EVENT_1, replacement],
        generated=2,
        best_pair=_best_from_event(_EVENT_1),
    )
    _patch_catalogue(monkeypatch, (_RECORD_0, _RECORD_1))

    with pytest.raises(
        UniformForestRunAuditError,
        match="catalogue/event binding failed at index 0",
    ):
        audit_uniform_forest_shard(output, expected_generated=2)


def test_duplicate_catalogue_record_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    second = json.loads(json.dumps(_EVENT_0))
    second["index"] = 1
    output = tmp_path / "shard"
    _write_complete_shard(
        output,
        events=[_EVENT_0, second],
        best_pair=_best_from_event(_EVENT_0),
    )
    _patch_catalogue(monkeypatch, (_RECORD_0, _RECORD_0))

    with pytest.raises(
        UniformForestRunAuditError,
        match="duplicate graph6 catalogue record",
    ):
        audit_uniform_forest_shard(output, expected_generated=2)


def test_tampered_integer_identity_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event = json.loads(json.dumps(_EVENT_0))
    event["strongest_pair"]["margin"] += 1
    output = tmp_path / "shard"
    _write_complete_shard(output, events=[event])
    _patch_catalogue(monkeypatch, (_RECORD_0,))

    with pytest.raises(
        UniformForestRunAuditError,
        match="margin is inconsistent",
    ):
        audit_uniform_forest_shard(output, expected_generated=1)


def test_impossible_pair_count_fails_basic_bounds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event = json.loads(json.dumps(_EVENT_0))
    pair = event["strongest_pair"]
    pair["forest_count_ef"] = pair["forest_count_e"] + 1
    pair["left_product"] = (
        pair["forest_count"] * pair["forest_count_ef"]
    )
    pair["margin"] = pair["right_product"] - pair["left_product"]
    output = tmp_path / "shard"
    _write_complete_shard(output, events=[event])
    _patch_catalogue(monkeypatch, (_RECORD_0,))

    with pytest.raises(
        UniformForestRunAuditError,
        match="pair count exceeds a marginal count",
    ):
        audit_uniform_forest_shard(output, expected_generated=1)


def test_state_counters_and_implementation_hash_are_mandatory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "shard"
    _write_complete_shard(output, events=[_EVENT_0])
    _patch_catalogue(monkeypatch, (_RECORD_0,))
    state_path = output / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["evaluated"] = 0
    state_path.write_text(json.dumps(state), encoding="utf-8")
    with pytest.raises(UniformForestRunAuditError, match="do not close"):
        audit_uniform_forest_shard(output, expected_generated=1)

    state["evaluated"] = 1
    state["implementation_sha256"] = "0" * 64
    state_path.write_text(json.dumps(state), encoding="utf-8")
    with pytest.raises(
        UniformForestRunAuditError,
        match="implementation no longer matches",
    ):
        audit_uniform_forest_shard(output, expected_generated=1)


def test_tampered_global_best_pair_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "shard"
    wrong_best = _best_from_event(_EVENT_0)
    wrong_best["margin"] += 1
    _write_complete_shard(
        output,
        events=[_EVENT_0],
        best_pair=wrong_best,
    )
    _patch_catalogue(monkeypatch, (_RECORD_0,))

    with pytest.raises(
        UniformForestRunAuditError,
        match="best_pair does not match",
    ):
        audit_uniform_forest_shard(output, expected_generated=1)


def test_recorded_geng_binary_hash_is_enforced(tmp_path: Path) -> None:
    executable = tmp_path / "geng"
    executable.write_bytes(b"not-the-recorded-binary")
    state = {
        "toolchain": {
            "geng": {
                "path": str(executable),
                "sha256": "0" * 64,
                "dynamic_linkage": {
                    "ldd_exit": 0,
                    "missing": [],
                    "dependencies": {},
                },
            }
        }
    }

    with pytest.raises(UniformForestRunAuditError, match="SHA-256 changed"):
        audit_module._validated_geng_tool(state)


def test_recorded_geng_dependency_hash_is_enforced(tmp_path: Path) -> None:
    executable = tmp_path / "geng"
    dependency = tmp_path / "libnauty.so"
    executable.write_bytes(b"recorded-geng")
    dependency.write_bytes(b"changed-library")
    state = {
        "toolchain": {
            "geng": {
                "path": str(executable),
                "sha256": audit_module._file_sha256(executable),
                "dynamic_linkage": {
                    "ldd_exit": 0,
                    "missing": [],
                    "dependencies": {
                        "libnauty.so": {
                            "path": str(dependency),
                            "sha256": "0" * 64,
                        }
                    },
                },
            }
        }
    }

    with pytest.raises(
        UniformForestRunAuditError,
        match="dependency libnauty.so SHA-256 changed",
    ):
        audit_module._validated_geng_tool(state)
