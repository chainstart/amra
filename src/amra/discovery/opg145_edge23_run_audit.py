"""Fail-closed audit of the sixty-four-shard OPG-145 edge-23 campaign.

The edge-23 search implementation is never imported.  This module freezes the
campaign-specific identity and directory contracts, then delegates only the
independent graph6 decoder, filter, union-find witness verifier, stable-file
reader, toolchain verifier, and streaming replay engine from
``opg145_dense_run_audit``.

Both audit layers are hashed separately in every successful report.  The base
auditor is adapted only within a process-local lock and is restored on every
exit path.
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


AUDIT_SCHEMA = "amra.opg145.n11-m23-64.audit.v1"
CHECKPOINT_SCHEMA = "amra.opg145.n11-m23-64.checkpoint.v1"
EVENT_SCHEMA = "amra.opg145.n11-m23-64.event.v1"
CAMPAIGN = "opg145_n11_edge23_64shard_exact"
ORDER = 11
EDGE_COUNT = 23
COLOR_COUNT = 7
SHARD_COUNT = 64
EXPECTED_BY_SHARD: dict[int, int] = {
    0: 32_085,
    1: 8_525,
    2: 35_867,
    3: 44_942,
    4: 13_020,
    5: 23_340,
    6: 50_283,
    7: 26_335,
    8: 77_167,
    9: 34_214,
    10: 25_411,
    11: 37_726,
    12: 25_073,
    13: 18_068,
    14: 18_968,
    15: 31_749,
    16: 15_742,
    17: 41_995,
    18: 45_605,
    19: 25_974,
    20: 28_661,
    21: 21_980,
    22: 22_810,
    23: 34_814,
    24: 29_448,
    25: 39_980,
    26: 18_854,
    27: 23_378,
    28: 21_811,
    29: 34_757,
    30: 23_526,
    31: 8_138,
    32: 19_325,
    33: 36_026,
    34: 30_022,
    35: 50_594,
    36: 54_005,
    37: 29_882,
    38: 24_863,
    39: 18_123,
    40: 36_881,
    41: 32_884,
    42: 46_283,
    43: 61_056,
    44: 17_547,
    45: 26_881,
    46: 23_906,
    47: 24_146,
    48: 13_465,
    49: 13_224,
    50: 20_761,
    51: 31_540,
    52: 33_356,
    53: 58_144,
    54: 45_868,
    55: 23_370,
    56: 43_641,
    57: 64_935,
    58: 30_820,
    59: 26_101,
    60: 42_672,
    61: 21_026,
    62: 47_432,
    63: 23_993,
}
EXPECTED_TOTAL = 2_013_018

DISCOVERY_DIRECTORY = Path(__file__).resolve().parent
EXPECTED_IMPLEMENTATION_FILES = (
    (
        "edge23_wrapper",
        DISCOVERY_DIRECTORY / "opg145_edge23_search.py",
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
    raise RuntimeError("the frozen edge-23 denominator table is incomplete")
if sum(EXPECTED_BY_SHARD.values()) != EXPECTED_TOTAL:
    raise RuntimeError("the frozen edge-23 denominator total is inconsistent")

Edge23RunAuditError = base_audit.DenseRunAuditError
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
            "-d2",
            "-D5",
            str(ORDER),
            f"{EDGE_COUNT}:{EDGE_COUNT}",
            "i/64",
        ],
        "per_shard_count_operation": "count_stdout_graph6_records",
        "total_count_command_canonical": [
            "geng",
            "-C",
            "-d2",
            "-D5",
            "-u",
            str(ORDER),
            f"{EDGE_COUNT}:{EDGE_COUNT}",
        ],
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "shard_count": SHARD_COUNT,
        "per_shard": {
            str(index): EXPECTED_BY_SHARD[index]
            for index in range(SHARD_COUNT)
        },
        "total": EXPECTED_TOTAL,
    }


def _verify_implementation(identity: Mapping[str, object]) -> str:
    """Verify the exact ordered role/path/hash triple used by the search."""

    implementation = identity.get("implementation")
    if not isinstance(implementation, Mapping) or set(implementation) != {
        "aggregate_sha256",
        "files",
    }:
        raise Edge23RunAuditError(
            "identity has a malformed implementation record"
        )
    raw_files = implementation.get("files")
    if not isinstance(raw_files, list) or len(raw_files) != len(
        EXPECTED_IMPLEMENTATION_FILES
    ):
        raise Edge23RunAuditError(
            "edge-23 implementation file set is incomplete"
        )

    aggregate = hashlib.sha256()
    for raw_record, (expected_role, raw_expected_path) in zip(
        raw_files, EXPECTED_IMPLEMENTATION_FILES
    ):
        if (
            not isinstance(raw_record, Mapping)
            or set(raw_record) != {"role", "path", "sha256"}
        ):
            raise Edge23RunAuditError(
                "malformed edge-23 implementation file record"
            )
        expected_path = raw_expected_path.resolve()
        if raw_record.get("role") != expected_role:
            raise Edge23RunAuditError(
                f"implementation role/order drift: {expected_role}"
            )
        if raw_record.get("path") != str(expected_path):
            raise Edge23RunAuditError(
                f"implementation directory drift: {raw_record.get('path')}"
            )
        if expected_path.is_symlink() or not expected_path.is_file():
            raise Edge23RunAuditError(
                f"implementation file disappeared or redirected: {expected_path}"
            )
        actual_sha = base_audit._file_sha256(expected_path)
        if (
            not base_audit._is_sha256(raw_record.get("sha256"))
            or raw_record.get("sha256") != actual_sha
        ):
            raise Edge23RunAuditError(
                f"implementation hash changed: {expected_path}"
            )
        aggregate.update(str(expected_path).encode("utf-8"))
        aggregate.update(actual_sha.encode("ascii"))

    aggregate_sha = aggregate.hexdigest()
    if implementation.get("aggregate_sha256") != aggregate_sha:
        raise Edge23RunAuditError(
            "implementation aggregate hash is inconsistent"
        )
    return aggregate_sha


def _validate_identity(
    state: Mapping[str, object], expected_shard: int
) -> tuple[Mapping[str, object], Mapping[str, object], str, str]:
    """Validate every variable and fixed field before catalogue replay."""

    if state.get("checkpoint_schema") != CHECKPOINT_SCHEMA:
        raise Edge23RunAuditError(
            "checkpoint schema is not the frozen edge-23 schema"
        )
    if state.get("status") != "complete":
        raise Edge23RunAuditError(
            "audit is allowed only after status=complete"
        )
    if expected_shard not in EXPECTED_BY_SHARD:
        raise Edge23RunAuditError("invalid expected edge-23 shard")
    identity = state.get("identity")
    if not isinstance(identity, Mapping):
        raise Edge23RunAuditError("checkpoint has no identity object")
    if set(identity) != EXPECTED_IDENTITY_KEYS:
        raise Edge23RunAuditError("edge-23 identity field set has drifted")
    identity_sha = base_audit._json_sha256(identity)
    if (
        state.get("identity_sha256") != identity_sha
        or not base_audit._is_sha256(identity_sha)
    ):
        raise Edge23RunAuditError(
            "checkpoint identity digest is inconsistent"
        )

    exact_fields: dict[str, object] = {
        "campaign": CAMPAIGN,
        "problem": "opg145",
        "order": ORDER,
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
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
            "shard_notation": "i/64",
            "caller_configurable_catalogue": False,
        },
    }
    for field, expected in exact_fields.items():
        if identity.get(field) != expected:
            raise Edge23RunAuditError(
                f"frozen edge-23 identity field drift: {field}"
            )

    per_instance = identity.get("per_instance_seconds")
    if (
        not isinstance(per_instance, (int, float))
        or isinstance(per_instance, bool)
        or not math.isfinite(float(per_instance))
        or float(per_instance) <= 0
    ):
        raise Edge23RunAuditError("invalid per-instance solver budget")

    implementation_sha = _verify_implementation(identity)
    geng, toolchain_sha = base_audit._verify_toolchain(identity)
    geng_path = str(geng["path"])
    canonical_command = [
        "geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        str(ORDER),
        f"{EDGE_COUNT}:{EDGE_COUNT}",
        f"{expected_shard}/{SHARD_COUNT}",
    ]
    actual_command = [geng_path, *canonical_command[1:]]
    if (
        identity.get("catalogue_command_canonical") != canonical_command
        or identity.get("catalogue_command") != actual_command
    ):
        raise Edge23RunAuditError(
            "catalogue command is not the exact frozen edge-23 command"
        )
    return identity, geng, implementation_sha, toolchain_sha


@contextmanager
def _edge23_audit_context() -> Iterator[None]:
    """Temporarily parameterize only the independent base audit engine."""

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
        "edge23_contract_wrapper": {
            "path": str(wrapper_path),
            "sha256": base_audit._file_sha256(wrapper_path),
        },
        "independent_base_engine": {
            "path": str(base_path),
            "sha256": base_audit._file_sha256(base_path),
        },
        "reuse_boundary": (
            "the wrapper freezes the edge-23 identity/layout; the base engine "
            "independently decodes graph6, checks filters and witnesses, "
            "verifies tool/dependency hashes, and replays every event"
        ),
    }


def _decorate_report(report: Mapping[str, object]) -> dict[str, object]:
    """Replace the base report's single hash with an explicit two-layer chain."""

    provenance = _auditor_provenance()
    base_record = provenance["independent_base_engine"]
    assert isinstance(base_record, Mapping)
    if report.get("auditor_sha256") != base_record["sha256"]:
        raise Edge23RunAuditError(
            "base audit report did not bind the executing base auditor"
        )
    decorated = dict(report)
    decorated.pop("auditor_sha256", None)
    decorated["auditor_provenance"] = provenance
    return decorated


def audit_edge23_shard(
    directory: Path, *, expected_shard: int
) -> dict[str, object]:
    """Read-only audit of one complete, correctly named edge-23 shard."""

    if expected_shard not in EXPECTED_BY_SHARD:
        raise Edge23RunAuditError("invalid expected edge-23 shard")
    with _edge23_audit_context():
        report = base_audit.audit_dense_shard(
            directory, expected_shard=expected_shard
        )
    return _decorate_report(report)


def audit_edge23_campaign(root: Path) -> dict[str, object]:
    """Audit a root containing exactly ``shard-0`` through ``shard-63``."""

    with _edge23_audit_context():
        report = base_audit.audit_dense_campaign(root)
    decorated = _decorate_report(report)
    raw_shards = decorated.get("shards")
    if not isinstance(raw_shards, list) or len(raw_shards) != SHARD_COUNT:
        raise Edge23RunAuditError("base audit returned an incomplete shard set")
    shard_reports: list[dict[str, object]] = []
    for shard in raw_shards:
        if not isinstance(shard, Mapping):
            raise Edge23RunAuditError(
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
        raise Edge23RunAuditError(
            "decorated campaign report does not exactly close edge-23"
        )
    return decorated


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only independent audit of the exact sixty-four-shard "
            "OPG-145 n=11,m=23 campaign."
        )
    )
    parser.add_argument("campaign_root", type=Path)
    arguments = parser.parse_args(argv)
    try:
        report = audit_edge23_campaign(arguments.campaign_root)
    except (Edge23RunAuditError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
