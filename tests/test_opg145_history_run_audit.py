from __future__ import annotations

import hashlib
from itertools import combinations
import json
from pathlib import Path

import pytest

import amra.discovery.opg145_history_run_audit as audit_module
from amra.discovery.opg145_history_run_audit import (
    EXPECTED_ARCHIVED_IMPLEMENTATION_SHA256,
    OPG145HistoryAuditError,
    audit_opg145_history,
)


def _encode_graph6(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> str:
    edge_set = {
        (min(left, right), max(left, right))
        for left, right in edges
    }
    bits = [
        int((left, right) in edge_set)
        for right in range(1, order)
        for left in range(right)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = "".join(
        chr(
            63
            + sum(
                bits[offset + bit] << (5 - bit)
                for bit in range(6)
            )
        )
        for offset in range(0, len(bits), 6)
    )
    return chr(order + 63) + payload


def _cycle(order: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            (
                (min(vertex, (vertex + 1) % order),
                 max(vertex, (vertex + 1) % order))
                for vertex in range(order)
            ),
            key=lambda edge: (edge[1], edge[0]),
        )
    )


def _eligible_order_seven_graph() -> tuple[
    tuple[tuple[int, int], ...],
    list[int],
]:
    raw_edges = [
        edge
        for edge in combinations(range(6), 2)
        if edge != (0, 1)
    ]
    raw_edges.extend(((0, 6), (1, 6)))
    edges = tuple(
        sorted(raw_edges, key=lambda edge: (edge[1], edge[0]))
    )
    coloring = [
        0,
        4,
        5,
        6,
        3,
        6,
        1,
        5,
        2,
        4,
        3,
        2,
        1,
        0,
        3,
        0,
    ]
    return edges, coloring


def _patch_small_contract(
    monkeypatch: pytest.MonkeyPatch,
    catalogues: dict[int, tuple[str, ...]],
) -> None:
    monkeypatch.setattr(
        audit_module,
        "EXPECTED_GENERATED_BY_ORDER",
        {7: 1, 8: 1, 9: 1},
    )
    monkeypatch.setattr(
        audit_module,
        "EXPECTED_ELIGIBLE_BY_ORDER",
        {7: 1, 8: 0, 9: 0},
    )
    monkeypatch.setattr(
        audit_module,
        "EXPECTED_CATALOGUE_SHA256_BY_ORDER",
        {
            order: hashlib.sha256(
                "".join(
                    record + "\n" for record in catalogues[order]
                ).encode("ascii")
            ).hexdigest()
            for order in catalogues
        },
    )
    monkeypatch.setattr(
        audit_module,
        "_recorded_geng",
        lambda state: (
            Path("/test/nauty-geng"),
            "test-geng-sha256",
            {},
        ),
    )
    monkeypatch.setattr(
        audit_module,
        "_runtime_linkage_snapshot",
        lambda path, environment: {
            "captured_during_audit": True,
            "legacy_checkpoint_bound": False,
            "ldd_exit": 0,
            "dependencies": {},
            "missing": [],
        },
    )
    monkeypatch.setattr(
        audit_module,
        "_iter_geng_catalogue",
        lambda path, order, environment: iter(catalogues[order]),
    )


def _write_small_history(
    directory: Path,
    *,
    coloring: list[int] | None = None,
    include_event: bool = True,
    append_event: bool = False,
    generated: int = 3,
) -> dict[int, tuple[str, ...]]:
    eligible_edges, valid_coloring = _eligible_order_seven_graph()
    catalogues = {
        7: (_encode_graph6(7, eligible_edges),),
        8: (_encode_graph6(8, _cycle(8)),),
        9: (_encode_graph6(9, _cycle(9)),),
    }
    state = {
        "checkpoint_schema": 2,
        "problem": "opg145",
        "lane": "default",
        "status": "complete",
        "shard": None,
        "minimum_order": 7,
        "maximum_order": 9,
        "next_order": 10,
        "next_index": 0,
        "implementation_sha256": (
            EXPECTED_ARCHIVED_IMPLEMENTATION_SHA256
        ),
        "toolchain": {
            "geng": {
                "path": "/test/nauty-geng",
                "sha256": "test-geng-sha256",
            }
        },
        "generated": generated,
        "eligible": 1,
        "filtered_known_positive": 2,
        "sat": 1,
        "unsat": 0,
        "timeouts": 0,
        "hard_queue": [],
    }
    event = {
        "problem": "opg145",
        "status": "sat",
        "order": 7,
        "index": 0,
        "encoding": catalogues[7][0],
        "vertices": 7,
        "edges": len(eligible_edges),
        "elapsed_seconds": 0.25,
        "lazy_cycle_cuts": 2,
        "verified_coloring": (
            valid_coloring if coloring is None else coloring
        ),
    }
    directory.mkdir()
    (directory / "state.json").write_text(
        json.dumps(state), encoding="utf-8"
    )
    event_rows = [event] if include_event else []
    if append_event:
        event_rows.append(event)
    (directory / "events.jsonl").write_text(
        "".join(json.dumps(row) + "\n" for row in event_rows),
        encoding="utf-8",
    )
    return catalogues


def test_history_audit_closes_each_order_and_records_residual_boundary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "history"
    catalogues = _write_small_history(directory)
    _patch_small_contract(monkeypatch, catalogues)

    result = audit_opg145_history(directory)

    assert result["status"] == (
        "independently_verified_with_legacy_provenance_boundary"
    )
    assert result["totals"]["generated"] == 3
    assert result["totals"]["sat_witnesses_replayed"] == 1
    assert result["per_order"]["7"]["eligible"] == 1
    assert result["per_order"]["8"]["filtered_known_positive"] == 1
    assert result["per_order"]["9"]["generated"] == 1
    provenance = result["legacy_provenance"]
    assert provenance[
        "archived_search_implementation_sha256"
    ] == EXPECTED_ARCHIVED_IMPLEMENTATION_SHA256
    assert provenance[
        "dynamic_linkage_recorded_by_legacy_checkpoint"
    ] is False
    assert provenance["geng_binary_hash_reverified"] is True
    assert len(str(result["auditor_sha256"])) == 64


def test_history_audit_rejects_missing_event_attack(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "history"
    catalogues = _write_small_history(
        directory,
        include_event=False,
    )
    _patch_small_contract(monkeypatch, catalogues)

    with pytest.raises(
        OPG145HistoryAuditError,
        match="missing eligible event",
    ):
        audit_opg145_history(directory)


def test_history_audit_rejects_padded_counter_attack(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "history"
    catalogues = _write_small_history(directory, generated=4)
    _patch_small_contract(monkeypatch, catalogues)

    with pytest.raises(
        OPG145HistoryAuditError,
        match="field 'generated'.*expected 3",
    ):
        audit_opg145_history(directory)


def test_history_audit_rejects_extra_event_attack(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "history"
    catalogues = _write_small_history(
        directory,
        append_event=True,
    )
    _patch_small_contract(monkeypatch, catalogues)

    with pytest.raises(
        OPG145HistoryAuditError,
        match="events remain",
    ):
        audit_opg145_history(directory)


def test_history_audit_rejects_same_count_catalogue_substitution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "history"
    catalogues = _write_small_history(directory)
    _patch_small_contract(monkeypatch, catalogues)
    replacement_edges = _cycle(8) + ((0, 4),)
    catalogues[8] = (_encode_graph6(8, replacement_edges),)

    with pytest.raises(
        OPG145HistoryAuditError,
        match="order 8 catalogue hash",
    ):
        audit_opg145_history(directory)


def test_history_audit_rejects_boolean_counter_type_confusion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "history"
    catalogues = _write_small_history(directory)
    _patch_small_contract(monkeypatch, catalogues)
    state_path = directory / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["next_index"] = False
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(
        OPG145HistoryAuditError,
        match="field 'next_index'.*expected 0",
    ):
        audit_opg145_history(directory)


def test_history_audit_rejects_tampered_witness_attack(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "history"
    tampered = [
        0,
        5,
        6,
        0,
        4,
        5,
        3,
        1,
        2,
        4,
        2,
        3,
        1,
        0,
        3,
        1,
    ]
    catalogues = _write_small_history(
        directory,
        coloring=tampered,
    )
    _patch_small_contract(monkeypatch, catalogues)
    graph = audit_module._decode_graph6_independently(
        catalogues[7][0]
    )
    incident_colors = [set() for _ in range(graph.order)]
    for edge_index, (left, right) in enumerate(graph.edges):
        color = tampered[edge_index]
        assert color not in incident_colors[left]
        assert color not in incident_colors[right]
        incident_colors[left].add(color)
        incident_colors[right].add(color)
    assert not audit_module.independently_verify_acyclic_seven_coloring(
        graph, tampered
    )

    with pytest.raises(
        OPG145HistoryAuditError,
        match="invalid acyclic seven-colour witness",
    ):
        audit_opg145_history(directory)
