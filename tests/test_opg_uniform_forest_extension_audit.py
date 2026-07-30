from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy
import pytest

from amra.discovery import opg_uniform_forest_extension_audit as audit


REPOSITORY = Path(audit.__file__).resolve().parents[3]
ARTIFACT_DIRECTORY = (
    REPOSITORY
    / "artifacts/opg_breakthrough/certified"
    / "opg1757-n12-best-beam-six-hour"
)
BEAM = ARTIFACT_DIRECTORY / "beam-best.json"


def _brute_force_statistics(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, tuple[int, ...], tuple[tuple[int, ...], ...]]:
    total = 0
    singles = [0] * len(edges)
    pairs = [[0] * len(edges) for _ in edges]
    for selected_mask in range(1 << len(edges)):
        parent = list(range(vertex_count))

        def find(vertex: int) -> int:
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        selected = []
        acyclic = True
        for edge_index, (left, right) in enumerate(edges):
            if not selected_mask & (1 << edge_index):
                continue
            left_root = find(left)
            right_root = find(right)
            if left_root == right_root:
                acyclic = False
                break
            parent[right_root] = left_root
            selected.append(edge_index)
        if not acyclic:
            continue
        total += 1
        for edge_index in selected:
            singles[edge_index] += 1
        for first_position, first in enumerate(selected):
            for second in selected[first_position + 1 :]:
                pairs[first][second] += 1
                pairs[second][first] += 1
    return (
        total,
        tuple(singles),
        tuple(tuple(row) for row in pairs),
    )


def _tiny_replay() -> audit._AllPairReplay:
    base_edges = ((0, 1), (0, 2), (1, 2), (2, 3))
    seed = audit._Graph(
        4,
        base_edges,
        audit._encode_compact_graph6(4, base_edges),
    )
    neighbours = (0, 1, 3)
    extension_edges = base_edges + tuple(
        (vertex, 4) for vertex in neighbours
    )
    extension = audit._Extension(
        0,
        neighbours,
        audit._Graph(
            5,
            extension_edges,
            audit._encode_compact_graph6(5, extension_edges),
        ),
    )
    base = audit._BasePartitionReplay(seed)
    return audit._replay_selected_all_pairs(seed, (extension,), base)[0]


def test_independent_partition_star_replay_matches_brute_force() -> None:
    replay = _tiny_replay()
    expected = _brute_force_statistics(
        replay.extension.graph.vertex_count,
        replay.extension.graph.edges,
    )

    assert replay.forest_count == expected[0]
    assert replay.edge_forest_counts == expected[1]
    assert replay.pair_forest_counts == expected[2]


def test_all_pair_semantic_tampering_fails_closed() -> None:
    replay = _tiny_replay()
    payload = {
        **audit._expected_all_pair_semantics(replay),
        "states": 123,
        "elapsed_seconds": 0.25,
    }
    payload["violation_pair_count"] = (
        int(payload["violation_pair_count"]) + 1
    )

    with pytest.raises(
        audit.ExtensionAuditError,
        match="violation_pair_count",
    ):
        audit._validate_analysis_artifact(payload, replay, "tiny.json")


def test_graph6_decoder_rejects_nonzero_padding() -> None:
    valid = audit._encode_compact_graph6(3, ((0, 1),))
    final_value = ord(valid[-1]) - 63
    assert final_value & 0b111 == 0
    tampered = valid[:-1] + chr(final_value + 1 + 63)

    with pytest.raises(
        audit.ExtensionAuditError,
        match="nonzero padding",
    ):
        audit._decode_compact_graph6(tampered)


def test_duplicate_json_keys_fail_closed(tmp_path: Path) -> None:
    artifact = tmp_path / "duplicate.json"
    artifact.write_text('{"status":"complete","status":"running"}', encoding="utf-8")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()

    with pytest.raises(audit.ExtensionAuditError, match="duplicate JSON key"):
        audit._read_frozen_json(artifact, digest)


def test_beam_byte_mutation_fails_before_partition_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mutated = tmp_path / "beam-best.json"
    mutated.write_bytes(BEAM.read_bytes() + b" ")

    class ForbiddenReplay:
        def __init__(self, seed) -> None:
            raise AssertionError("partition replay must not start")

    monkeypatch.setattr(audit, "_BasePartitionReplay", ForbiddenReplay)
    with pytest.raises(
        audit.ExtensionAuditError,
        match="artifact SHA-256 mismatch",
    ):
        audit.audit_n12_labelled_extension_campaign(
            mutated,
            analysis_directory=ARTIFACT_DIRECTORY,
        )


def test_source_hash_drift_fails_before_artifact_replay(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    changed = dict(audit.EXPECTED_SOURCE_SHA256)
    path, _digest = changed["artifact_producer"]
    changed["artifact_producer"] = (path, "0" * 64)
    monkeypatch.setattr(audit, "EXPECTED_SOURCE_SHA256", changed)

    with pytest.raises(
        audit.ExtensionAuditError,
        match="source SHA-256 mismatch",
    ):
        audit.audit_n12_labelled_extension_campaign(BEAM)


def test_sparse_dot_rejects_unknown_partition() -> None:
    replay = _tiny_replay()
    seed_edges = ((0, 1), (1, 2))
    seed = audit._Graph(
        3,
        seed_edges,
        audit._encode_compact_graph6(3, seed_edges),
    )
    base = audit._BasePartitionReplay(seed)
    unknown = {(1, 2): 1}
    weights = numpy.ones(len(base.partitions), dtype=numpy.int64)

    with pytest.raises(audit.ExtensionAuditError, match="absent from total DP"):
        base.sparse_dot(unknown, weights)
    assert replay.forest_count > 0


def test_live_frozen_campaign_replays_every_persisted_count() -> None:
    result = audit.audit_n12_labelled_extension_campaign(BEAM)

    assert result["campaign_complete"] is True
    labelled = result["labelled_extension_replay"]
    assert labelled["evaluated"] == 1012
    assert labelled["strict_inherited_pair_count"] == 1012
    assert labelled["equality_inherited_pair_count"] == 0
    assert labelled["violation_inherited_pair_count"] == 0
    assert len(labelled["exact_four_count_table_sha256"]) == 64
    all_pairs = result["representative_all_pair_replay"]
    assert all_pairs["artifacts_verified"] == 7
    assert all_pairs["pair_count"] == 3861
    assert all_pairs["strict_pair_count"] == 3861
    assert all_pairs["equality_pair_count"] == 0
    assert all_pairs["violation_pair_count"] == 0
    assert all_pairs["persisted_top_strict_records_verified"] == 140
