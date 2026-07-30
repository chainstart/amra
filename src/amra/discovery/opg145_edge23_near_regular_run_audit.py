"""Independent audit of the OPG-145 ``m=23, degree 4:5`` campaign.

The search implementation is never imported.  This wrapper freezes the exact
sixteen-shard identity and degree sequence ``(5,5,4^9)``, while the independent
base audit engine regenerates graph6 records, checks every event/filter/witness,
and revalidates source, tool, linkage, dependency, and file hashes.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import math
from pathlib import Path
import threading
from typing import Iterator, Mapping, Sequence

import amra.discovery.opg145_dense_run_audit as base_audit


AUDIT_SCHEMA = "amra.opg145.n11-m23-d4-d5-16.audit.v1"
CHECKPOINT_SCHEMA = "amra.opg145.n11-m23-d4-d5-16.checkpoint.v1"
EVENT_SCHEMA = "amra.opg145.n11-m23-d4-d5-16.event.v1"
CAMPAIGN = "opg145_n11_edge23_near_regular_16shard_exact"
ORDER = 11
EDGE_COUNT = 23
MINIMUM_DEGREE = 4
MAXIMUM_DEGREE = 5
DEGREE_SEQUENCE = (5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4)
COLOR_COUNT = 7
SHARD_COUNT = 16
EXPECTED_BY_SHARD: dict[int, int] = {
    0: 880,
    1: 449,
    2: 664,
    3: 517,
    4: 425,
    5: 602,
    6: 906,
    7: 629,
    8: 451,
    9: 437,
    10: 492,
    11: 507,
    12: 611,
    13: 536,
    14: 463,
    15: 417,
}
EXPECTED_TOTAL = 8_986

DISCOVERY_DIRECTORY = Path(__file__).resolve().parent
EXPECTED_IMPLEMENTATION_FILES = (
    (
        "near_regular_wrapper",
        DISCOVERY_DIRECTORY / "opg145_edge23_near_regular_search.py",
    ),
    (
        "dense_base_runner",
        DISCOVERY_DIRECTORY / "opg145_dense_search.py",
    ),
    (
        "shared_coloring",
        DISCOVERY_DIRECTORY / "opg_coloring_search.py",
    ),
)
EXPECTED_IDENTITY_KEYS = frozenset(
    (
        "campaign",
        "problem",
        "order",
        "edge_range",
        "degree_range",
        "degree_sequence_descending",
        "shard",
        "expected_generated",
        "expected_denominator_manifest",
        "color_count",
        "known_positive_filter",
        "catalogue_command",
        "catalogue_command_canonical",
        "per_instance_seconds",
        "checkpoint_interval_records",
        "event_policy",
        "fixed_campaign_contract",
        "implementation",
        "toolchain",
    )
)

if set(EXPECTED_BY_SHARD) != set(range(SHARD_COUNT)):
    raise RuntimeError(
        "the frozen near-regular denominator table is incomplete"
    )
if sum(EXPECTED_BY_SHARD.values()) != EXPECTED_TOTAL:
    raise RuntimeError(
        "the frozen near-regular denominator total is inconsistent"
    )

NearRegularRunAuditError = base_audit.DenseRunAuditError
_ADAPTER_LOCK = threading.Lock()


def _expected_manifest() -> dict[str, object]:
    return {
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
            str(ORDER),
            f"{EDGE_COUNT}:{EDGE_COUNT}",
            "i/16",
        ],
        "per_shard_count_operation": "count_stdout_graph6_records",
        "total_count_command_canonical": [
            "geng",
            "-C",
            "-d4",
            "-D5",
            "-u",
            str(ORDER),
            f"{EDGE_COUNT}:{EDGE_COUNT}",
        ],
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "degree_range": [MINIMUM_DEGREE, MAXIMUM_DEGREE],
        "degree_sequence_descending": list(DEGREE_SEQUENCE),
        "shard_count": SHARD_COUNT,
        "per_shard": {
            str(index): EXPECTED_BY_SHARD[index]
            for index in range(SHARD_COUNT)
        },
        "total": EXPECTED_TOTAL,
    }


def _validate_near_regular_catalogue_graph(
    graph: base_audit.AuditGraph,
) -> None:
    if (
        graph.vertex_count != ORDER
        or len(graph.edges) != EDGE_COUNT
        or tuple(sorted(graph.degrees, reverse=True)) != DEGREE_SEQUENCE
    ):
        raise NearRegularRunAuditError(
            "regenerated graph violates n=11, m=23, degree sequence "
            "(5,5,4^9)"
        )


def _verify_implementation(identity: Mapping[str, object]) -> str:
    implementation = identity.get("implementation")
    if not isinstance(implementation, Mapping) or set(implementation) != {
        "aggregate_sha256",
        "files",
    }:
        raise NearRegularRunAuditError(
            "identity has a malformed implementation record"
        )
    raw_files = implementation.get("files")
    if not isinstance(raw_files, list) or len(raw_files) != len(
        EXPECTED_IMPLEMENTATION_FILES
    ):
        raise NearRegularRunAuditError(
            "near-regular implementation file set is incomplete"
        )

    aggregate = hashlib.sha256()
    for raw_record, (expected_role, raw_expected_path) in zip(
        raw_files, EXPECTED_IMPLEMENTATION_FILES
    ):
        if (
            not isinstance(raw_record, Mapping)
            or set(raw_record) != {"role", "path", "sha256"}
        ):
            raise NearRegularRunAuditError(
                "malformed near-regular implementation file record"
            )
        expected_path = raw_expected_path.resolve()
        if raw_record.get("role") != expected_role:
            raise NearRegularRunAuditError(
                f"implementation role/order drift: {expected_role}"
            )
        if raw_record.get("path") != str(expected_path):
            raise NearRegularRunAuditError(
                f"implementation directory drift: {raw_record.get('path')}"
            )
        if expected_path.is_symlink() or not expected_path.is_file():
            raise NearRegularRunAuditError(
                f"implementation file disappeared or redirected: {expected_path}"
            )
        actual_sha = base_audit._file_sha256(expected_path)
        if (
            not base_audit._is_sha256(raw_record.get("sha256"))
            or raw_record.get("sha256") != actual_sha
        ):
            raise NearRegularRunAuditError(
                f"implementation hash changed: {expected_path}"
            )
        aggregate.update(str(expected_path).encode("utf-8"))
        aggregate.update(actual_sha.encode("ascii"))
    aggregate_sha = aggregate.hexdigest()
    if implementation.get("aggregate_sha256") != aggregate_sha:
        raise NearRegularRunAuditError(
            "implementation aggregate hash is inconsistent"
        )
    return aggregate_sha


def _validate_identity(
    state: Mapping[str, object], expected_shard: int
) -> tuple[Mapping[str, object], Mapping[str, object], str, str]:
    if state.get("checkpoint_schema") != CHECKPOINT_SCHEMA:
        raise NearRegularRunAuditError(
            "checkpoint schema is not the frozen near-regular schema"
        )
    if state.get("status") != "complete":
        raise NearRegularRunAuditError(
            "audit is allowed only after status=complete"
        )
    if expected_shard not in EXPECTED_BY_SHARD:
        raise NearRegularRunAuditError("invalid expected near-regular shard")
    identity = state.get("identity")
    if not isinstance(identity, Mapping):
        raise NearRegularRunAuditError("checkpoint has no identity object")
    if set(identity) != EXPECTED_IDENTITY_KEYS:
        raise NearRegularRunAuditError(
            "near-regular identity field set has drifted"
        )
    identity_sha = base_audit._json_sha256(identity)
    if (
        state.get("identity_sha256") != identity_sha
        or not base_audit._is_sha256(identity_sha)
    ):
        raise NearRegularRunAuditError(
            "checkpoint identity digest is inconsistent"
        )

    exact_fields: dict[str, object] = {
        "campaign": CAMPAIGN,
        "problem": "opg145",
        "order": ORDER,
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "degree_range": [MINIMUM_DEGREE, MAXIMUM_DEGREE],
        "degree_sequence_descending": list(DEGREE_SEQUENCE),
        "shard": [expected_shard, SHARD_COUNT],
        "expected_generated": EXPECTED_BY_SHARD[expected_shard],
        "expected_denominator_manifest": _expected_manifest(),
        "color_count": COLOR_COUNT,
        "known_positive_filter": "is_three_sparse",
        "checkpoint_interval_records": 1,
        "event_policy": "one_fsynced_event_per_generated_record",
        "fixed_campaign_contract": {
            "order": ORDER,
            "edge_count": EDGE_COUNT,
            "minimum_degree": MINIMUM_DEGREE,
            "maximum_degree": MAXIMUM_DEGREE,
            "degree_sequence_descending": list(DEGREE_SEQUENCE),
            "shard_notation": "i/16",
            "caller_configurable_catalogue": False,
        },
    }
    for field, expected in exact_fields.items():
        if identity.get(field) != expected:
            raise NearRegularRunAuditError(
                f"frozen near-regular identity field drift: {field}"
            )
    per_instance = identity.get("per_instance_seconds")
    if (
        not isinstance(per_instance, (int, float))
        or isinstance(per_instance, bool)
        or not math.isfinite(float(per_instance))
        or float(per_instance) <= 0
    ):
        raise NearRegularRunAuditError("invalid per-instance solver budget")

    implementation_sha = _verify_implementation(identity)
    geng, toolchain_sha = base_audit._verify_toolchain(identity)
    canonical_command = [
        "geng",
        "-q",
        "-C",
        "-d4",
        "-D5",
        str(ORDER),
        f"{EDGE_COUNT}:{EDGE_COUNT}",
        f"{expected_shard}/{SHARD_COUNT}",
    ]
    actual_command = [str(geng["path"]), *canonical_command[1:]]
    if (
        identity.get("catalogue_command_canonical") != canonical_command
        or identity.get("catalogue_command") != actual_command
    ):
        raise NearRegularRunAuditError(
            "catalogue command is not the exact frozen near-regular command"
        )
    return identity, geng, implementation_sha, toolchain_sha


@contextmanager
def _near_regular_audit_context() -> Iterator[None]:
    with _ADAPTER_LOCK:
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
            "_validate_catalogue_graph",
        )
        originals = {name: getattr(base_audit, name) for name in names}
        replacements = {
            "AUDIT_SCHEMA": AUDIT_SCHEMA,
            "CHECKPOINT_SCHEMA": CHECKPOINT_SCHEMA,
            "EVENT_SCHEMA": EVENT_SCHEMA,
            "MINIMUM_EDGES": EDGE_COUNT,
            "MAXIMUM_EDGES": EDGE_COUNT,
            "SHARD_COUNT": SHARD_COUNT,
            "EXPECTED_BY_SHARD": dict(EXPECTED_BY_SHARD),
            "EXPECTED_TOTAL": EXPECTED_TOTAL,
            "_validate_identity": _validate_identity,
            "_validate_catalogue_graph": (
                _validate_near_regular_catalogue_graph
            ),
        }
        for name, value in replacements.items():
            setattr(base_audit, name, value)
        try:
            yield
        finally:
            for name, value in originals.items():
                setattr(base_audit, name, value)


def _auditor_provenance() -> dict[str, object]:
    wrapper_path = Path(__file__).resolve()
    base_path = Path(base_audit.__file__).resolve()
    return {
        "near_regular_contract_wrapper": {
            "path": str(wrapper_path),
            "sha256": base_audit._file_sha256(wrapper_path),
        },
        "independent_base_engine": {
            "path": str(base_path),
            "sha256": base_audit._file_sha256(base_path),
        },
        "reuse_boundary": (
            "the wrapper freezes the near-regular identity, degree sequence, "
            "and layout; the base engine independently decodes graph6, checks "
            "filters and witnesses, verifies all hashes, and replays events"
        ),
    }


def _decorate_report(report: Mapping[str, object]) -> dict[str, object]:
    provenance = _auditor_provenance()
    base_record = provenance["independent_base_engine"]
    assert isinstance(base_record, Mapping)
    if report.get("auditor_sha256") != base_record["sha256"]:
        raise NearRegularRunAuditError(
            "base audit report did not bind the executing base auditor"
        )
    decorated = dict(report)
    decorated.pop("auditor_sha256", None)
    decorated["auditor_provenance"] = provenance
    return decorated


def audit_near_regular_shard(
    directory: Path, *, expected_shard: int
) -> dict[str, object]:
    if expected_shard not in EXPECTED_BY_SHARD:
        raise NearRegularRunAuditError("invalid expected near-regular shard")
    with _near_regular_audit_context():
        report = base_audit.audit_dense_shard(
            directory, expected_shard=expected_shard
        )
    return _decorate_report(report)


def audit_near_regular_campaign(root: Path) -> dict[str, object]:
    with _near_regular_audit_context():
        report = base_audit.audit_dense_campaign(root)
    decorated = _decorate_report(report)
    raw_shards = decorated.get("shards")
    if not isinstance(raw_shards, list) or len(raw_shards) != SHARD_COUNT:
        raise NearRegularRunAuditError(
            "base audit returned an incomplete shard set"
        )
    shard_reports: list[dict[str, object]] = []
    for shard in raw_shards:
        if not isinstance(shard, Mapping):
            raise NearRegularRunAuditError(
                "base audit returned a malformed shard report"
            )
        shard_reports.append(_decorate_report(shard))
    decorated["shards"] = shard_reports
    if (
        decorated.get("audit_schema") != AUDIT_SCHEMA
        or decorated.get("shard_count") != SHARD_COUNT
        or decorated.get("expected_total") != EXPECTED_TOTAL
        or decorated.get("audited_total") != EXPECTED_TOTAL
    ):
        raise NearRegularRunAuditError(
            "decorated campaign report does not exactly close near-regular"
        )
    return decorated


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only independent audit of the exact OPG-145 n=11,m=23,"
            "degree 4:5 sixteen-shard campaign."
        )
    )
    parser.add_argument("campaign_root", type=Path)
    arguments = parser.parse_args(argv)
    try:
        report = audit_near_regular_campaign(arguments.campaign_root)
    except (NearRegularRunAuditError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
