from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path

import pytest

from amra.discovery import opg145_dense_run_audit as base_audit
from amra.discovery import opg145_edge23_degree2_critical_run_audit as audit


GRAPH6_BY_CLASS = {
    audit.NO_DEGREE2_CLASS: "J?AFBjw}FW?",
    audit.SUPPRESSIBLE_CLASS: "J?AFBjw}Fo?",
    audit.COMMON_MISSING_CLASS: "J?ABfJY}@u?",
    audit.RESIDUAL_CLASS: "J?ABfJiz?}?",
}
RESIDUAL_COLORING = [
    0,
    5,
    4,
    2,
    3,
    2,
    1,
    4,
    5,
    4,
    3,
    1,
    0,
    4,
    3,
    2,
    0,
    1,
    3,
    2,
    5,
    1,
    0,
]
SHA256_ZERO = "0" * 64


def _graph(partition_class: str) -> audit.AuditGraph:
    return base_audit.decode_graph6_independently(
        GRAPH6_BY_CLASS[partition_class]
    )


def _base_event(
    graph: audit.AuditGraph,
    partition_class: str,
    *,
    index: int = 0,
    identity_sha: str = SHA256_ZERO,
) -> dict[str, object]:
    return {
        "event_schema": audit.EVENT_SCHEMA,
        "identity_sha256": identity_sha,
        "time_unix": 1.0,
        "problem": "opg145",
        "order": audit.ORDER,
        "index": index,
        "graph6": graph.graph6,
        "vertices": graph.vertex_count,
        "edge_count": len(graph.edges),
        "edges": [list(edge) for edge in graph.edges],
        "degrees": list(graph.degrees),
        "partition_class": partition_class,
        "degree2_local_profiles": audit._degree2_local_profiles(graph),
    }


def _filtered_event(
    partition_class: str,
    *,
    index: int = 0,
    identity_sha: str = SHA256_ZERO,
) -> dict[str, object]:
    graph = _graph(partition_class)
    event = _base_event(
        graph,
        partition_class,
        index=index,
        identity_sha=identity_sha,
    )
    is_external = partition_class == audit.NO_DEGREE2_CLASS
    basis = {
        audit.NO_DEGREE2_CLASS: "external_disjoint_campaigns",
        audit.SUPPRESSIBLE_CLASS: (
            "degree2_suppression_extension_lemma"
        ),
        audit.COMMON_MISSING_CLASS: (
            "degree2_common_missing_extension_lemma"
        ),
    }[partition_class]
    event.update(
        {
            "filter_reason": partition_class,
            "positive_basis": basis,
            "mathematical_positive_claimed": not is_external,
            "eligible": False,
            "status": (
                "partition_filtered" if is_external else "theorem_filtered"
            ),
            "verified_coloring": None,
        }
    )
    return event


def _sat_event(
    *,
    index: int = 0,
    identity_sha: str = SHA256_ZERO,
) -> dict[str, object]:
    graph = _graph(audit.RESIDUAL_CLASS)
    event = _base_event(
        graph,
        audit.RESIDUAL_CLASS,
        index=index,
        identity_sha=identity_sha,
    )
    base_clause_count = (
        len(graph.edges)
        * (1 + audit.COLOR_COUNT * (audit.COLOR_COUNT - 1) // 2)
        + sum(
            degree * (degree - 1) // 2 * audit.COLOR_COUNT
            for degree in graph.degrees
        )
        + 1
    )
    event.update(
        {
            "filter_reason": None,
            "positive_basis": "solver_verified_witness",
            "mathematical_positive_claimed": True,
            "eligible": True,
            "status": "sat",
            "elapsed_seconds": 0.01,
            "variables": len(graph.edges) * audit.COLOR_COUNT,
            "clauses": base_clause_count,
            "cnf_sha256": SHA256_ZERO,
            "lazy_cycle_cuts": 0,
            "lazy_cycle_records_sha256": SHA256_ZERO,
            "lazy_cycle_certificate": None,
            "verified_coloring": list(RESIDUAL_COLORING),
            "solver_stdout_sha256": SHA256_ZERO,
            "solver_stderr_sha256": SHA256_ZERO,
        }
    )
    return event


def _identity(shard: int = 0) -> dict[str, object]:
    geng_path = "/frozen/geng"
    canonical = [
        "geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "23:23",
        f"{shard}/16",
    ]
    return {
        "campaign": audit.CAMPAIGN,
        "problem": "opg145",
        "order": audit.ORDER,
        "edge_range": [audit.EDGE_COUNT, audit.EDGE_COUNT],
        "generator_degree_range": [
            audit.MINIMUM_DEGREE,
            audit.MAXIMUM_DEGREE,
        ],
        "shard": [shard, audit.SHARD_COUNT],
        "expected_generated": audit.EXPECTED_GENERATED_BY_SHARD[shard],
        "expected_partition_counts": audit._partition_row(shard),
        "expected_denominator_manifest": audit._expected_manifest(),
        "color_count": audit.COLOR_COUNT,
        "classification_policy": (
            "degree2_reduction_with_external_delta3_partition_v1"
        ),
        "positive_basis": {
            audit.NO_DEGREE2_CLASS: "external_disjoint_campaigns",
            audit.SUPPRESSIBLE_CLASS: (
                "degree2_suppression_extension_lemma"
            ),
            audit.COMMON_MISSING_CLASS: (
                "degree2_common_missing_extension_lemma"
            ),
            audit.RESIDUAL_CLASS: "solver_required",
        },
        "catalogue_command": [geng_path, *canonical[1:]],
        "catalogue_command_canonical": canonical,
        "catalogue_environment_contract": {
            "locale": "C",
            "dynamic_library_directories": (
                "recorded_geng_dependency_parents"
            ),
            "removed_variables": ["LD_AUDIT", "LD_PRELOAD"],
        },
        "per_instance_seconds": 60.0,
        "checkpoint_interval_records": 1,
        "event_policy": "one_fsynced_event_per_generated_record",
        "fixed_campaign_contract": {
            "order": audit.ORDER,
            "edge_count": audit.EDGE_COUNT,
            "minimum_degree": audit.MINIMUM_DEGREE,
            "maximum_degree": audit.MAXIMUM_DEGREE,
            "shard_notation": "i/16",
            "classification_order": list(audit.CLASSIFICATION_ORDER),
            "caller_configurable_catalogue": False,
        },
        "implementation": {},
        "toolchain": {},
    }


def test_frozen_partition_tables_and_manifest_close_exactly() -> None:
    assert audit.EXPECTED_GENERATED_BY_SHARD == (
        80617,
        99770,
        132255,
        153050,
        129042,
        133346,
        143824,
        102642,
        187137,
        172013,
        121368,
        148261,
        107103,
        100732,
        113832,
        88026,
    )
    assert audit.EXPECTED_RESIDUAL_BY_SHARD == (
        5813,
        5702,
        7242,
        10963,
        6509,
        11889,
        12611,
        7923,
        12280,
        9959,
        10345,
        11126,
        5936,
        7078,
        5354,
        6272,
    )
    assert sum(audit.EXPECTED_GENERATED_BY_SHARD) == 2_013_018
    assert sum(audit.EXPECTED_RESIDUAL_BY_SHARD) == 137_002
    for shard in range(audit.SHARD_COUNT):
        assert audit.EXPECTED_GENERATED_BY_SHARD[shard] == (
            audit.EXPECTED_NO_DEGREE2_BY_SHARD[shard]
            + audit.EXPECTED_SUPPRESSIBLE_BY_SHARD[shard]
            + audit.EXPECTED_COMMON_MISSING_BY_SHARD[shard]
            + audit.EXPECTED_RESIDUAL_BY_SHARD[shard]
        )
    manifest = audit._expected_manifest()
    assert manifest["classification_order"] == list(
        audit.CLASSIFICATION_ORDER
    )
    assert manifest["per_shard"]["0"] == {
        "generated": 80617,
        "filtered_no_degree2": 42771,
        "filtered_suppressible": 26328,
        "filtered_common_missing": 5705,
        "eligible_residual": 5813,
    }
    assert manifest["totals"]["eligible_residual"] == 137_002


@pytest.mark.parametrize(
    "partition_class", audit.CLASSIFICATION_ORDER
)
def test_real_graph6_examples_are_independently_classified(
    partition_class: str,
) -> None:
    graph = _graph(partition_class)
    assert audit.classify_degree2_critical_graph(graph) == partition_class


def test_local_profiles_certify_the_two_degree2_lemmas_and_residual() -> None:
    suppressible = audit._degree2_local_profiles(
        _graph(audit.SUPPRESSIBLE_CLASS)
    )
    assert suppressible == [
        {
            "vertex": 5,
            "neighbours": [0, 7],
            "neighbour_degrees": [5, 4],
            "neighbours_adjacent": False,
        }
    ]
    common_missing = audit._degree2_local_profiles(
        _graph(audit.COMMON_MISSING_CLASS)
    )
    assert common_missing[0]["neighbours_adjacent"] is True
    assert sum(common_missing[0]["neighbour_degrees"]) == 9
    residual = audit._degree2_local_profiles(
        _graph(audit.RESIDUAL_CLASS)
    )
    assert residual[0]["neighbours_adjacent"] is True
    assert residual[0]["neighbour_degrees"] == [5, 5]


def test_catalogue_validator_rejects_a_non_frozen_graph() -> None:
    graph = _graph(audit.RESIDUAL_CLASS)
    malformed = audit.AuditGraph(
        graph.vertex_count,
        graph.edges[:-1],
        graph.graph6,
    )
    with pytest.raises(
        audit.Degree2CriticalRunAuditError,
        match="catalogue constraints",
    ):
        audit._validate_catalogue_graph(malformed)


def test_no_degree2_is_external_partition_not_theorem_positive() -> None:
    graph = _graph(audit.NO_DEGREE2_CLASS)
    event = _filtered_event(audit.NO_DEGREE2_CLASS)
    assert (
        audit._validate_event(
            event,
            graph,
            audit.NO_DEGREE2_CLASS,
            0,
            SHA256_ZERO,
        )
        == "filtered_no_degree2"
    )

    tampered = dict(event)
    tampered["status"] = "theorem_filtered"
    tampered["mathematical_positive_claimed"] = True
    with pytest.raises(
        audit.Degree2CriticalRunAuditError,
        match="filtered semantics",
    ):
        audit._validate_event(
            tampered,
            graph,
            audit.NO_DEGREE2_CLASS,
            0,
            SHA256_ZERO,
        )


@pytest.mark.parametrize(
    ("partition_class", "outcome"),
    (
        (audit.SUPPRESSIBLE_CLASS, "filtered_suppressible"),
        (audit.COMMON_MISSING_CLASS, "filtered_common_missing"),
    ),
)
def test_only_the_two_lemma_classes_are_theorem_filtered(
    partition_class: str, outcome: str
) -> None:
    graph = _graph(partition_class)
    event = _filtered_event(partition_class)
    assert (
        audit._validate_event(
            event,
            graph,
            partition_class,
            0,
            SHA256_ZERO,
        )
        == outcome
    )
    tampered = dict(event)
    tampered["positive_basis"] = "external_disjoint_campaigns"
    with pytest.raises(
        audit.Degree2CriticalRunAuditError,
        match="filtered semantics",
    ):
        audit._validate_event(
            tampered,
            graph,
            partition_class,
            0,
            SHA256_ZERO,
        )


def test_residual_event_requires_an_independently_validated_witness() -> None:
    graph = _graph(audit.RESIDUAL_CLASS)
    event = _sat_event()
    assert (
        audit._validate_event(
            event,
            graph,
            audit.RESIDUAL_CLASS,
            0,
            SHA256_ZERO,
        )
        == "sat"
    )
    tampered = copy.deepcopy(event)
    tampered["verified_coloring"][0] = audit.COLOR_COUNT
    with pytest.raises(
        audit.Degree2CriticalRunAuditError,
        match="invalid acyclic",
    ):
        audit._validate_event(
            tampered,
            graph,
            audit.RESIDUAL_CLASS,
            0,
            SHA256_ZERO,
        )


def test_closed_state_uses_full_generated_and_residual_eligible_counts() -> None:
    state = {
        "catalogue_exhausted": True,
        "next_index": 80617,
        "events_sha256": SHA256_ZERO,
        "generated": 80617,
        "filtered_no_degree2": 42771,
        "filtered_suppressible": 26328,
        "filtered_common_missing": 5705,
        "eligible": 5813,
        "sat": 5813,
        "unsat": 0,
        "timeouts": 0,
        "unknown": 0,
    }
    assert audit._validate_closed_state(state, 0) == {
        key: state[key] for key in audit.COUNTER_KEYS
    }
    tampered = dict(state)
    tampered["eligible"] -= 1
    with pytest.raises(
        audit.Degree2CriticalRunAuditError,
        match="not exactly closed",
    ):
        audit._validate_closed_state(tampered, 0)


def test_identity_contract_is_strict_without_importing_runner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identity = _identity()
    state = {
        "checkpoint_schema": audit.CHECKPOINT_SCHEMA,
        "status": "complete",
        "identity": identity,
        "identity_sha256": base_audit._json_sha256(identity),
    }
    monkeypatch.setattr(
        audit, "_verify_implementation", lambda unused: "1" * 64
    )
    monkeypatch.setattr(
        base_audit,
        "_verify_toolchain",
        lambda unused: ({"path": "/frozen/geng"}, "2" * 64),
    )
    verified, geng, implementation_sha, toolchain_sha = (
        audit._validate_identity(state, 0)
    )
    assert verified == identity
    assert geng == {"path": "/frozen/geng"}
    assert implementation_sha == "1" * 64
    assert toolchain_sha == "2" * 64

    tampered = copy.deepcopy(state)
    tampered["identity"]["positive_basis"][
        audit.NO_DEGREE2_CLASS
    ] = "theorem_positive"
    tampered["identity_sha256"] = base_audit._json_sha256(
        tampered["identity"]
    )
    with pytest.raises(
        audit.Degree2CriticalRunAuditError,
        match="identity field drift",
    ):
        audit._validate_identity(tampered, 0)


def test_auditor_source_never_imports_the_search_runner() -> None:
    tree = ast.parse(Path(audit.__file__).read_text(encoding="utf-8"))
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    assert {
        name for name in imported if name.startswith("amra.discovery")
    } == {"amra.discovery.opg145_dense_run_audit"}


def test_real_geng_pipeline_is_decoded_without_runner_import() -> None:
    geng_path = Path(
        "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/bin/nauty-geng"
    )
    cliquer = Path(
        "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/lib/"
        "libcliquer.so.1"
    )
    nauty = Path(
        "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/lib/"
        "x86_64-linux-gnu/libnautyW1-2.8.8.so"
    )
    if not all(path.is_file() for path in (geng_path, cliquer, nauty)):
        pytest.skip("the frozen nauty installation is unavailable")
    command = [
        str(geng_path),
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "23:23",
        "0/16",
    ]
    identity = {"catalogue_command": command}
    geng = {
        "path": str(geng_path),
        "dynamic_linkage": {
            "dependencies": {
                "libcliquer.so.1": {"path": str(cliquer)},
                "libnautyW1-2.8.8.so": {"path": str(nauty)},
            }
        },
    }
    records = audit._iter_regenerated_catalogue(
        identity, geng, expected_shard=0
    )
    try:
        prefix = [next(records) for _ in range(3)]
    finally:
        records.close()
    assert [graph.graph6 for graph, _ in prefix] == [
        "J?AFBjw}Fo?",
        "J?AFBjw}Fg?",
        "J?AFBjw}FW?",
    ]
    assert prefix[0][1] == audit.SUPPRESSIBLE_CLASS
    assert prefix[2][1] == audit.NO_DEGREE2_CLASS


def test_four_event_shard_replay_checks_hashes_and_accounting(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    shard = tmp_path / "shard-0"
    shard.mkdir()
    identity_sha = "a" * 64
    events = [
        _filtered_event(
            audit.NO_DEGREE2_CLASS, index=0, identity_sha=identity_sha
        ),
        _filtered_event(
            audit.SUPPRESSIBLE_CLASS, index=1, identity_sha=identity_sha
        ),
        _filtered_event(
            audit.COMMON_MISSING_CLASS, index=2, identity_sha=identity_sha
        ),
        _sat_event(index=3, identity_sha=identity_sha),
    ]
    event_bytes = b"".join(
        (
            json.dumps(
                event,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")
        for event in events
    )
    events_sha = hashlib.sha256(event_bytes).hexdigest()
    (shard / "events.jsonl").write_bytes(event_bytes)
    state = {
        "checkpoint_schema": audit.CHECKPOINT_SCHEMA,
        "status": "complete",
        "identity": {},
        "identity_sha256": identity_sha,
        "catalogue_exhausted": True,
        "next_index": 4,
        "events_sha256": events_sha,
        "generated": 4,
        "filtered_no_degree2": 1,
        "filtered_suppressible": 1,
        "filtered_common_missing": 1,
        "eligible": 1,
        "sat": 1,
        "unsat": 0,
        "timeouts": 0,
        "unknown": 0,
    }
    (shard / "state.json").write_text(
        json.dumps(state, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    def replace_first(
        values: tuple[int, ...], first: int
    ) -> tuple[int, ...]:
        return (first, *values[1:])

    monkeypatch.setattr(
        audit,
        "EXPECTED_GENERATED_BY_SHARD",
        replace_first(audit.EXPECTED_GENERATED_BY_SHARD, 4),
    )
    monkeypatch.setattr(
        audit,
        "EXPECTED_NO_DEGREE2_BY_SHARD",
        replace_first(audit.EXPECTED_NO_DEGREE2_BY_SHARD, 1),
    )
    monkeypatch.setattr(
        audit,
        "EXPECTED_SUPPRESSIBLE_BY_SHARD",
        replace_first(audit.EXPECTED_SUPPRESSIBLE_BY_SHARD, 1),
    )
    monkeypatch.setattr(
        audit,
        "EXPECTED_COMMON_MISSING_BY_SHARD",
        replace_first(audit.EXPECTED_COMMON_MISSING_BY_SHARD, 1),
    )
    monkeypatch.setattr(
        audit,
        "EXPECTED_RESIDUAL_BY_SHARD",
        replace_first(audit.EXPECTED_RESIDUAL_BY_SHARD, 1),
    )
    monkeypatch.setattr(
        audit,
        "_validate_identity",
        lambda unused_state, unused_shard: (
            {},
            {},
            "1" * 64,
            "2" * 64,
        ),
    )

    def regenerated(
        unused_identity: object,
        unused_geng: object,
        *,
        expected_shard: int,
    ):
        assert expected_shard == 0
        for partition_class in audit.CLASSIFICATION_ORDER:
            yield _graph(partition_class), partition_class

    monkeypatch.setattr(
        audit, "_iter_regenerated_catalogue", regenerated
    )
    report = audit.audit_degree2_critical_shard(
        shard, expected_shard=0
    )
    assert report["status"] == "verified_complete"
    assert report["expected_generated"] == 4
    assert report["expected_residual"] == 1
    assert report["audited_counts"] == {
        "generated": 4,
        "filtered_no_degree2": 1,
        "filtered_suppressible": 1,
        "filtered_common_missing": 1,
        "eligible": 1,
        "sat": 1,
        "unsat": 0,
        "timeouts": 0,
        "unknown": 0,
    }


def test_auditor_provenance_binds_both_independent_layers() -> None:
    provenance = audit._auditor_provenance()
    assert provenance["runner_imported"] is False
    for key in (
        "degree2_critical_independent_auditor",
        "independent_primitive_library",
    ):
        record = provenance[key]
        assert Path(record["path"]).is_file()
        assert base_audit._is_sha256(record["sha256"])
