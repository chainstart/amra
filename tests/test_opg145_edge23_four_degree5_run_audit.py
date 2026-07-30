from __future__ import annotations

import ast
import copy
import json
from pathlib import Path

import pytest

from amra.discovery import opg145_dense_run_audit as base_audit
from amra.discovery import opg145_edge23_four_degree5_run_audit as audit
from amra.discovery import opg145_edge23_four_degree5_search as search


TARGET_GRAPH6 = "J?AFBjYnBY?"
WRONG_DEGREES_GRAPH6 = "J?AFBjYnA]?"


def test_frozen_denominators_manifest_and_degree_sequence() -> None:
    assert audit.EXPECTED_BY_SHARD == {
        0: 18118,
        1: 25131,
        2: 32971,
        3: 34344,
        4: 29940,
        5: 28464,
        6: 28337,
        7: 25230,
        8: 40657,
        9: 39482,
        10: 26597,
        11: 30604,
        12: 27979,
        13: 24268,
        14: 28875,
        15: 19621,
    }
    assert sum(audit.EXPECTED_BY_SHARD.values()) == 460_618
    assert audit.DEGREE_SEQUENCE == (5,) * 4 + (4,) * 5 + (3,) * 2
    manifest = audit._expected_manifest()
    assert manifest["maximum_degree_vertex_count"] == 4
    assert manifest["per_shard_pipeline_canonical"][1] == [
        "pickg",
        "-q",
        "-M4",
    ]
    assert manifest["total"] == 460_618


def test_exact_regenerated_degree_validation() -> None:
    target = base_audit.decode_graph6_independently(TARGET_GRAPH6)
    audit._validate_exact_catalogue_graph(target)
    wrong = base_audit.decode_graph6_independently(
        WRONG_DEGREES_GRAPH6
    )
    with pytest.raises(
        audit.FourDegree5RunAuditError,
        match="degree sequence",
    ):
        audit._validate_exact_catalogue_graph(wrong)


def test_auditor_never_imports_the_search_implementation() -> None:
    tree = ast.parse(
        Path(audit.__file__).read_text(encoding="utf-8")
    )
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    assert {
        name for name in imported if name.startswith("amra.discovery")
    } == {"amra.discovery.opg145_dense_run_audit"}


def test_real_smoke_identity_is_accepted_independently(
    tmp_path: Path,
) -> None:
    identity = search.build_identity(search.config_for_shard(0, 60))
    state = {
        "checkpoint_schema": audit.CHECKPOINT_SCHEMA,
        "status": "complete",
        "identity": identity,
        "identity_sha256": base_audit._json_sha256(identity),
    }
    with audit._four_degree5_audit_context():
        (
            verified_identity,
            geng,
            implementation_sha,
            toolchain_sha,
        ) = audit._validate_identity(state, 0)
    assert verified_identity == identity
    assert geng["path"] == identity["toolchain"]["geng"]["path"]
    assert base_audit._is_sha256(implementation_sha)
    assert base_audit._is_sha256(toolchain_sha)


def test_identity_tampering_is_rejected() -> None:
    identity = search.build_identity(search.config_for_shard(0, 60))
    state = {
        "checkpoint_schema": audit.CHECKPOINT_SCHEMA,
        "status": "complete",
        "identity": identity,
        "identity_sha256": base_audit._json_sha256(identity),
    }
    tampered = copy.deepcopy(state)
    tampered["identity"]["expected_denominator_manifest"]["per_shard"][
        "0"
    ] -= 1
    tampered["identity_sha256"] = base_audit._json_sha256(
        tampered["identity"]
    )
    with (
        audit._four_degree5_audit_context(),
        pytest.raises(
            audit.FourDegree5RunAuditError,
            match="identity field drift",
        ),
    ):
        audit._validate_identity(tampered, 0)


def test_independent_real_pipeline_replays_first_two_records() -> None:
    identity = search.build_identity(search.config_for_shard(0, 60))
    state = {
        "checkpoint_schema": audit.CHECKPOINT_SCHEMA,
        "status": "complete",
        "identity": identity,
        "identity_sha256": base_audit._json_sha256(identity),
    }
    with audit._four_degree5_audit_context():
        verified_identity, geng, _, _ = audit._validate_identity(state, 0)
        records = audit._iter_exact_pipeline(verified_identity, geng)
        try:
            assert next(records) == "J?AFBjYnBY?"
            assert next(records) == "J?AFBi]}BY?"
        finally:
            records.close()


def test_adapter_restores_independent_base_globals() -> None:
    names = (
        "AUDIT_SCHEMA",
        "CHECKPOINT_SCHEMA",
        "EVENT_SCHEMA",
        "MINIMUM_EDGES",
        "MAXIMUM_EDGES",
        "SHARD_COUNT",
        "EXPECTED_BY_SHARD",
        "EXPECTED_TOTAL",
        "TOOL_NAMES",
        "_validate_identity",
        "_validate_catalogue_graph",
        "_iter_recorded_catalogue",
    )
    originals = {name: getattr(base_audit, name) for name in names}
    with audit._four_degree5_audit_context():
        assert base_audit.AUDIT_SCHEMA == audit.AUDIT_SCHEMA
        assert base_audit.EXPECTED_TOTAL == 460_618
        assert base_audit._iter_recorded_catalogue is (
            audit._iter_exact_pipeline
        )
    assert {
        name: getattr(base_audit, name) for name in names
    } == originals


def test_auditor_provenance_binds_wrapper_and_base_engine() -> None:
    provenance = audit._auditor_provenance()
    assert set(provenance) == {
        "four_degree5_contract_wrapper",
        "independent_base_engine",
        "reuse_boundary",
    }
    for key in (
        "four_degree5_contract_wrapper",
        "independent_base_engine",
    ):
        record = provenance[key]
        assert Path(record["path"]).is_file()
        assert base_audit._is_sha256(record["sha256"])
