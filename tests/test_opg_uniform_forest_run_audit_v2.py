from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import pytest

import amra.discovery.opg_uniform_forest_run_audit_v2 as audit_v2


_TINY_GENG_SHA256 = "a" * 64
_TINY_DEPENDENCIES = {"libtiny.so": "b" * 64}
_TINY_SHARDS = {
    0: ("A",),
    1: ("B",),
    2: ("C",),
    3: ("D",),
}
_TINY_UNSHARDED = ("A", "B", "C", "D")


def _write_tiny_shards(tmp_path: Path) -> tuple[Path, ...]:
    directories = []
    for shard_index in range(4):
        directory = tmp_path / f"shard-{shard_index}"
        directory.mkdir()
        state = {
            "checkpoint_schema": 1,
            "problem": "opg1757",
            "connected_only": True,
            "order": 9,
            "minimum_edges": 19,
            "maximum_edges": 36,
            "shard": [shard_index, 4],
            "next_index": 1,
            "generated": 1,
            "evaluated": 1,
            "nonviolating": 1,
            "violations": 0,
            "timeouts": 0,
            "hard_queue": [],
            "candidate": None,
            "status": "complete",
            "toolchain": {"geng": {}},
        }
        (directory / "state.json").write_text(
            json.dumps(state),
            encoding="utf-8",
        )
        (directory / "events.jsonl").write_text("", encoding="utf-8")
        directories.append(directory)
    return tuple(directories)


def _patch_tiny_constants(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        audit_v2,
        "CAMPAIGN_EXPECTED_GENERATED",
        (1, 1, 1, 1),
    )
    monkeypatch.setattr(audit_v2, "CAMPAIGN_EXPECTED_TOTAL", 4)
    monkeypatch.setattr(
        audit_v2,
        "CAMPAIGN_GENG_SHA256",
        _TINY_GENG_SHA256,
    )
    monkeypatch.setattr(
        audit_v2,
        "CAMPAIGN_SORTED_CATALOGUE_SHA256",
        audit_v2._sorted_catalogue_sha256(set(_TINY_UNSHARDED)),
    )


def _install_tiny_campaign_mocks(
    monkeypatch: pytest.MonkeyPatch,
    *,
    sharded: dict[int, tuple[str, ...]] | None = None,
    unsharded: tuple[str, ...] | None = None,
    mutate_report: (
        Callable[[dict[str, object], int], None] | None
    ) = None,
) -> dict[str, object]:
    _patch_tiny_constants(monkeypatch)
    tool = audit_v2.base_audit._ValidatedGeng(
        Path("/fake/geng"),
        _TINY_GENG_SHA256,
        (),
        dict(_TINY_DEPENDENCIES),
    )
    monkeypatch.setattr(
        audit_v2.base_audit,
        "_validated_geng_tool",
        lambda state: tool,
    )
    calls: dict[str, object] = {
        "base": [],
        "catalogue": [],
    }
    base_hash = audit_v2._file_sha256(
        Path(audit_v2.base_audit.__file__).resolve()
    )

    def fake_base_audit(
        directory: Path,
        *,
        expected_generated: int,
    ) -> dict[str, object]:
        state = json.loads(
            (directory / "state.json").read_text(encoding="utf-8")
        )
        shard_index = int(state["shard"][0])
        calls["base"].append((shard_index, expected_generated))
        report: dict[str, object] = {
            "schema": audit_v2.base_audit.AUDIT_SCHEMA,
            "shard": [shard_index, 4],
            "generated": 1,
            "events_replayed": 1,
            "nonviolating": 1,
            "violations": 0,
            "timeouts": 0,
            "geng_sha256": _TINY_GENG_SHA256,
            "geng_dependency_sha256": dict(_TINY_DEPENDENCIES),
            "search_implementation_sha256": "c" * 64,
            "auditor_sha256": base_hash,
            "residual_trust_boundary": ["counts are not independently replayed"],
        }
        if mutate_report is not None:
            mutate_report(report, shard_index)
        return report

    monkeypatch.setattr(
        audit_v2.base_audit,
        "audit_uniform_forest_shard",
        fake_base_audit,
    )
    shard_records = _TINY_SHARDS if sharded is None else sharded
    unsharded_records = (
        _TINY_UNSHARDED if unsharded is None else unsharded
    )

    def fake_catalogue(
        tool_record: audit_v2.base_audit._ValidatedGeng,
        shard: tuple[int, int] | None,
    ):
        assert tool_record is tool
        calls["catalogue"].append(shard)
        records = (
            unsharded_records
            if shard is None
            else shard_records[shard[0]]
        )
        yield from records

    monkeypatch.setattr(
        audit_v2,
        "_iter_frozen_catalogue",
        fake_catalogue,
    )
    return calls


def test_tiny_campaign_closes_dependency_and_catalogue_contracts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directories = _write_tiny_shards(tmp_path)
    calls = _install_tiny_campaign_mocks(monkeypatch)

    result = audit_v2.audit_uniform_forest_campaign_v2(
        tuple(reversed(directories))
    )

    assert result["campaign_complete"] is True
    assert result["dependency_closure"] == {
        "all_four_maps_identical": True,
        "geng_sha256": _TINY_GENG_SHA256,
        "geng_dependency_sha256": _TINY_DEPENDENCIES,
    }
    closure = result["catalogue_closure"]
    assert closure["shard_counts"] == [1, 1, 1, 1]
    assert closure["sharded_count"] == 4
    assert closure["unsharded_count"] == 4
    assert closure["exact_set_equal"] is True
    assert closure["exact_multiset_equal"] is True
    assert calls["base"] == [(0, 1), (1, 1), (2, 1), (3, 1)]
    assert calls["catalogue"] == [(0, 4), (1, 4), (2, 4), (3, 4), None]
    hashes = result["source_hashes"]
    assert hashes["wrapper_auditor_sha256"] == audit_v2._file_sha256(
        Path(audit_v2.__file__).resolve()
    )
    assert hashes["base_auditor_sha256"] == audit_v2._file_sha256(
        Path(audit_v2.base_audit.__file__).resolve()
    )


def test_incomplete_state_fails_before_tool_or_base_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directories = _write_tiny_shards(tmp_path)
    _patch_tiny_constants(monkeypatch)
    state_path = directories[2] / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "running"
    state_path.write_text(json.dumps(state), encoding="utf-8")
    calls = {"tool": 0, "base": 0, "catalogue": 0}

    def forbidden_tool(state):
        calls["tool"] += 1
        raise AssertionError("tool validation must not run")

    def forbidden_base(directory, *, expected_generated):
        calls["base"] += 1
        raise AssertionError("base replay must not run")

    def forbidden_catalogue(tool, shard):
        calls["catalogue"] += 1
        raise AssertionError("catalogue replay must not run")
        yield

    monkeypatch.setattr(
        audit_v2.base_audit,
        "_validated_geng_tool",
        forbidden_tool,
    )
    monkeypatch.setattr(
        audit_v2.base_audit,
        "audit_uniform_forest_shard",
        forbidden_base,
    )
    monkeypatch.setattr(
        audit_v2,
        "_iter_frozen_catalogue",
        forbidden_catalogue,
    )

    with pytest.raises(
        audit_v2.UniformForestRunAuditV2Error,
        match="shard 2 is not complete",
    ):
        audit_v2.audit_uniform_forest_campaign_v2(directories)

    assert calls == {"tool": 0, "base": 0, "catalogue": 0}


def test_dependency_map_mismatch_fails_before_base_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directories = _write_tiny_shards(tmp_path)
    _patch_tiny_constants(monkeypatch)
    base_calls = 0

    def fake_tool(state):
        shard_index = int(state["shard"][0])
        dependencies = {
            "libtiny.so": (
                "d" * 64 if shard_index == 3 else "b" * 64
            )
        }
        return audit_v2.base_audit._ValidatedGeng(
            Path("/fake/geng"),
            _TINY_GENG_SHA256,
            (),
            dependencies,
        )

    def forbidden_base(directory, *, expected_generated):
        nonlocal base_calls
        base_calls += 1
        raise AssertionError("base replay must not run")

    monkeypatch.setattr(
        audit_v2.base_audit,
        "_validated_geng_tool",
        fake_tool,
    )
    monkeypatch.setattr(
        audit_v2.base_audit,
        "audit_uniform_forest_shard",
        forbidden_base,
    )

    with pytest.raises(
        audit_v2.UniformForestRunAuditV2Error,
        match="dependency SHA-256 maps differ",
    ):
        audit_v2.audit_uniform_forest_campaign_v2(directories)

    assert base_calls == 0


def test_duplicate_across_shards_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directories = _write_tiny_shards(tmp_path)
    _install_tiny_campaign_mocks(
        monkeypatch,
        sharded={0: ("A",), 1: ("A",), 2: ("C",), 3: ("D",)},
    )

    with pytest.raises(
        audit_v2.UniformForestRunAuditV2Error,
        match="duplicate graph6 record across",
    ):
        audit_v2.audit_uniform_forest_campaign_v2(directories)


def test_duplicate_in_unsharded_catalogue_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directories = _write_tiny_shards(tmp_path)
    _install_tiny_campaign_mocks(
        monkeypatch,
        unsharded=("A", "B", "C", "C", "D"),
    )

    with pytest.raises(
        audit_v2.UniformForestRunAuditV2Error,
        match="duplicate graph6 record in frozen unsharded",
    ):
        audit_v2.audit_uniform_forest_campaign_v2(directories)


def test_equal_counts_but_different_catalogue_sets_fail_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directories = _write_tiny_shards(tmp_path)
    _install_tiny_campaign_mocks(
        monkeypatch,
        unsharded=("A", "B", "C", "E"),
    )

    with pytest.raises(
        audit_v2.UniformForestRunAuditV2Error,
        match="catalogue sets differ",
    ):
        audit_v2.audit_uniform_forest_campaign_v2(directories)


def test_matching_sets_with_wrong_frozen_digest_fail_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directories = _write_tiny_shards(tmp_path)
    _install_tiny_campaign_mocks(monkeypatch)
    monkeypatch.setattr(
        audit_v2,
        "CAMPAIGN_SORTED_CATALOGUE_SHA256",
        "0" * 64,
    )

    with pytest.raises(
        audit_v2.UniformForestRunAuditV2Error,
        match="digest does not match",
    ):
        audit_v2.audit_uniform_forest_campaign_v2(directories)


def test_v1_report_dependency_tamper_fails_before_catalogue_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directories = _write_tiny_shards(tmp_path)

    def mutate_report(report: dict[str, object], shard_index: int) -> None:
        if shard_index == 1:
            report["geng_dependency_sha256"] = {
                "libtiny.so": "e" * 64
            }

    calls = _install_tiny_campaign_mocks(
        monkeypatch,
        mutate_report=mutate_report,
    )

    with pytest.raises(
        audit_v2.UniformForestRunAuditV2Error,
        match="report dependency map differs",
    ):
        audit_v2.audit_uniform_forest_campaign_v2(directories)

    assert calls["catalogue"] == []
