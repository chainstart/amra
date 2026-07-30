"""Independent audit of the OPG-145 ``(5^3,4^7,3)`` campaign.

The search implementation is never imported.  This contract wrapper freezes
the sixteen-shard identity, verifies ``geng`` and ``pickg`` and all recorded
dynamic dependencies, independently reruns the exact no-shell two-process
pipeline, and delegates graph6 decoding, filter replay, event checking, and
seven-colour witness verification to the independent dense audit engine.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
import threading
from typing import Iterator, Mapping, Sequence

import amra.discovery.opg145_dense_run_audit as base_audit


AUDIT_SCHEMA = "amra.opg145.n11-m23-d3-d5-M3-16.audit.v1"
CHECKPOINT_SCHEMA = "amra.opg145.n11-m23-d3-d5-M3-16.checkpoint.v1"
EVENT_SCHEMA = "amra.opg145.n11-m23-d3-d5-M3-16.event.v1"
CAMPAIGN = "opg145_n11_edge23_three_degree5_16shard_exact"
ORDER = 11
EDGE_COUNT = 23
MINIMUM_DEGREE = 3
MAXIMUM_DEGREE = 5
MAXIMUM_DEGREE_VERTEX_COUNT = 3
DEGREE_SEQUENCE = (5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 3)
COLOR_COUNT = 7
SHARD_COUNT = 16
EXPECTED_BY_SHARD: dict[int, int] = {
    0: 6_243,
    1: 7_862,
    2: 9_963,
    3: 8_693,
    4: 9_037,
    5: 8_129,
    6: 7_177,
    7: 8_263,
    8: 10_056,
    9: 10_665,
    10: 7_520,
    11: 7_198,
    12: 8_604,
    13: 7_257,
    14: 9_174,
    15: 6_125,
}
EXPECTED_TOTAL = 131_966
TOOL_NAMES = frozenset(
    ("geng", "pickg", "minisat", "cadical", "drat-trim")
)

DISCOVERY_DIRECTORY = Path(__file__).resolve().parent
EXPECTED_IMPLEMENTATION_FILES = (
    (
        "three_degree5_wrapper",
        DISCOVERY_DIRECTORY / "opg145_edge23_three_degree5_search.py",
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
        "generator_degree_range",
        "maximum_degree_vertex_count",
        "degree_sequence_descending",
        "shard",
        "expected_generated",
        "expected_denominator_manifest",
        "color_count",
        "known_positive_filter",
        "catalogue_command",
        "catalogue_command_canonical",
        "catalogue_filter_command",
        "catalogue_filter_command_canonical",
        "catalogue_pipeline_transport",
        "pipeline_environment_contract",
        "per_instance_seconds",
        "checkpoint_interval_records",
        "event_policy",
        "fixed_campaign_contract",
        "implementation",
        "toolchain",
    )
)

if set(EXPECTED_BY_SHARD) != set(range(SHARD_COUNT)):
    raise RuntimeError("the frozen three-degree-5 denominator table is incomplete")
if sum(EXPECTED_BY_SHARD.values()) != EXPECTED_TOTAL:
    raise RuntimeError("the frozen three-degree-5 denominator total is inconsistent")

ThreeDegree5RunAuditError = base_audit.DenseRunAuditError
_ADAPTER_LOCK = threading.Lock()


def _expected_manifest() -> dict[str, object]:
    return {
        "method": "independent_exact_pipeline_graph6_line_count",
        "per_shard_pipeline_canonical": [
            [
                "geng",
                "-q",
                "-C",
                "-d3",
                "-D5",
                str(ORDER),
                f"{EDGE_COUNT}:{EDGE_COUNT}",
                "i/16",
            ],
            ["pickg", "-q", f"-M{MAXIMUM_DEGREE_VERTEX_COUNT}"],
        ],
        "pipeline_transport": "stdout_pipe_two_popen_no_shell",
        "per_shard_count_operation": "count_filtered_stdout_graph6_records",
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "generator_degree_range": [MINIMUM_DEGREE, MAXIMUM_DEGREE],
        "maximum_degree_vertex_count": MAXIMUM_DEGREE_VERTEX_COUNT,
        "degree_sequence_descending": list(DEGREE_SEQUENCE),
        "degree_sequence_derivation": (
            "sum(deg)=46; maximum at most 4 would give sum at most 44, "
            "so D5 forces maximum 5; M3 gives three degree-5 vertices; "
            "the eight remaining degrees are in 3..4 and sum to 31, "
            "hence (4,4,4,4,4,4,4,3)"
        ),
        "shard_count": SHARD_COUNT,
        "per_shard": {
            str(index): EXPECTED_BY_SHARD[index]
            for index in range(SHARD_COUNT)
        },
        "total": EXPECTED_TOTAL,
    }


def _validate_exact_catalogue_graph(graph: base_audit.AuditGraph) -> None:
    if (
        graph.vertex_count != ORDER
        or len(graph.edges) != EDGE_COUNT
        or tuple(sorted(graph.degrees, reverse=True)) != DEGREE_SEQUENCE
    ):
        raise ThreeDegree5RunAuditError(
            "regenerated graph violates n=11, m=23, degree sequence "
            "(5^3,4^7,3)"
        )


def _verify_implementation(identity: Mapping[str, object]) -> str:
    implementation = identity.get("implementation")
    if not isinstance(implementation, Mapping) or set(implementation) != {
        "aggregate_sha256",
        "files",
    }:
        raise ThreeDegree5RunAuditError(
            "identity has a malformed implementation record"
        )
    raw_files = implementation.get("files")
    if not isinstance(raw_files, list) or len(raw_files) != len(
        EXPECTED_IMPLEMENTATION_FILES
    ):
        raise ThreeDegree5RunAuditError(
            "three-degree-5 implementation file set is incomplete"
        )
    aggregate = hashlib.sha256()
    for raw_record, (expected_role, raw_path) in zip(
        raw_files, EXPECTED_IMPLEMENTATION_FILES
    ):
        if (
            not isinstance(raw_record, Mapping)
            or set(raw_record) != {"role", "path", "sha256"}
        ):
            raise ThreeDegree5RunAuditError(
                "malformed implementation file record"
            )
        expected_path = raw_path.resolve()
        if raw_record.get("role") != expected_role:
            raise ThreeDegree5RunAuditError(
                f"implementation role/order drift: {expected_role}"
            )
        if raw_record.get("path") != str(expected_path):
            raise ThreeDegree5RunAuditError(
                f"implementation directory drift: {raw_record.get('path')}"
            )
        if expected_path.is_symlink() or not expected_path.is_file():
            raise ThreeDegree5RunAuditError(
                f"implementation file disappeared or redirected: {expected_path}"
            )
        actual_sha = base_audit._file_sha256(expected_path)
        if (
            not base_audit._is_sha256(raw_record.get("sha256"))
            or raw_record.get("sha256") != actual_sha
        ):
            raise ThreeDegree5RunAuditError(
                f"implementation hash changed: {expected_path}"
            )
        aggregate.update(str(expected_path).encode("utf-8"))
        aggregate.update(actual_sha.encode("ascii"))
    aggregate_sha = aggregate.hexdigest()
    if implementation.get("aggregate_sha256") != aggregate_sha:
        raise ThreeDegree5RunAuditError(
            "implementation aggregate hash is inconsistent"
        )
    return aggregate_sha


def _validate_identity(
    state: Mapping[str, object], expected_shard: int
) -> tuple[Mapping[str, object], Mapping[str, object], str, str]:
    if state.get("checkpoint_schema") != CHECKPOINT_SCHEMA:
        raise ThreeDegree5RunAuditError(
            "checkpoint schema is not the frozen three-degree-5 schema"
        )
    if state.get("status") != "complete":
        raise ThreeDegree5RunAuditError(
            "audit is allowed only after status=complete"
        )
    if expected_shard not in EXPECTED_BY_SHARD:
        raise ThreeDegree5RunAuditError(
            "invalid expected three-degree-5 shard"
        )
    identity = state.get("identity")
    if not isinstance(identity, Mapping):
        raise ThreeDegree5RunAuditError("checkpoint has no identity object")
    if set(identity) != EXPECTED_IDENTITY_KEYS:
        raise ThreeDegree5RunAuditError(
            "three-degree-5 identity field set has drifted"
        )
    identity_sha = base_audit._json_sha256(identity)
    if (
        state.get("identity_sha256") != identity_sha
        or not base_audit._is_sha256(identity_sha)
    ):
        raise ThreeDegree5RunAuditError(
            "checkpoint identity digest is inconsistent"
        )

    exact_fields: dict[str, object] = {
        "campaign": CAMPAIGN,
        "problem": "opg145",
        "order": ORDER,
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "generator_degree_range": [MINIMUM_DEGREE, MAXIMUM_DEGREE],
        "maximum_degree_vertex_count": MAXIMUM_DEGREE_VERTEX_COUNT,
        "degree_sequence_descending": list(DEGREE_SEQUENCE),
        "shard": [expected_shard, SHARD_COUNT],
        "expected_generated": EXPECTED_BY_SHARD[expected_shard],
        "expected_denominator_manifest": _expected_manifest(),
        "color_count": COLOR_COUNT,
        "known_positive_filter": "is_three_sparse",
        "catalogue_pipeline_transport": "stdout_pipe_two_popen_no_shell",
        "pipeline_environment_contract": {
            "locale": "C",
            "dynamic_library_directories": (
                "recorded_geng_and_pickg_dependency_parents"
            ),
            "removed_variables": ["LD_AUDIT", "LD_PRELOAD"],
        },
        "checkpoint_interval_records": 1,
        "event_policy": "one_fsynced_event_per_generated_record",
        "fixed_campaign_contract": {
            "order": ORDER,
            "edge_count": EDGE_COUNT,
            "minimum_degree": MINIMUM_DEGREE,
            "maximum_degree": MAXIMUM_DEGREE,
            "maximum_degree_vertex_count": MAXIMUM_DEGREE_VERTEX_COUNT,
            "degree_sequence_descending": list(DEGREE_SEQUENCE),
            "shard_notation": "i/16",
            "caller_configurable_catalogue": False,
        },
    }
    for field, expected in exact_fields.items():
        if identity.get(field) != expected:
            raise ThreeDegree5RunAuditError(
                f"frozen three-degree-5 identity field drift: {field}"
            )
    per_instance = identity.get("per_instance_seconds")
    if (
        not isinstance(per_instance, (int, float))
        or isinstance(per_instance, bool)
        or not math.isfinite(float(per_instance))
        or float(per_instance) <= 0
    ):
        raise ThreeDegree5RunAuditError("invalid per-instance solver budget")

    implementation_sha = _verify_implementation(identity)
    geng, toolchain_sha = base_audit._verify_toolchain(identity)
    toolchain = identity["toolchain"]
    assert isinstance(toolchain, Mapping)
    pickg = toolchain.get("pickg")
    if not isinstance(pickg, Mapping):
        raise ThreeDegree5RunAuditError("verified toolchain has no pickg")
    geng_canonical = [
        "geng",
        "-q",
        "-C",
        "-d3",
        "-D5",
        str(ORDER),
        f"{EDGE_COUNT}:{EDGE_COUNT}",
        f"{expected_shard}/{SHARD_COUNT}",
    ]
    pickg_canonical = [
        "pickg",
        "-q",
        f"-M{MAXIMUM_DEGREE_VERTEX_COUNT}",
    ]
    if (
        identity.get("catalogue_command_canonical") != geng_canonical
        or identity.get("catalogue_command")
        != [str(geng["path"]), *geng_canonical[1:]]
        or identity.get("catalogue_filter_command_canonical")
        != pickg_canonical
        or identity.get("catalogue_filter_command")
        != [str(pickg["path"]), *pickg_canonical[1:]]
    ):
        raise ThreeDegree5RunAuditError(
            "catalogue pipeline is not the exact frozen geng|pickg pipeline"
        )
    return identity, geng, implementation_sha, toolchain_sha


def _pipeline_environment(
    geng: Mapping[str, object],
    pickg: Mapping[str, object],
) -> dict[str, str]:
    directories: list[str] = []
    for record in (geng, pickg):
        linkage = record.get("dynamic_linkage")
        if not isinstance(linkage, Mapping):
            raise ThreeDegree5RunAuditError(
                "catalogue tool has no linkage map"
            )
        dependencies = linkage.get("dependencies")
        if not isinstance(dependencies, Mapping):
            raise ThreeDegree5RunAuditError(
                "catalogue tool has no dependency map"
            )
        for dependency in dependencies.values():
            if not isinstance(dependency, Mapping):
                raise ThreeDegree5RunAuditError(
                    "catalogue tool has malformed dependency"
                )
            raw_path = dependency.get("path")
            if not isinstance(raw_path, str) or not raw_path:
                raise ThreeDegree5RunAuditError(
                    "catalogue dependency has no path"
                )
            directory = str(Path(raw_path).parent)
            if directory not in directories:
                directories.append(directory)
    environment = dict(os.environ)
    environment.pop("LD_AUDIT", None)
    environment.pop("LD_PRELOAD", None)
    environment["LD_LIBRARY_PATH"] = os.pathsep.join(directories)
    environment["LC_ALL"] = "C"
    return environment


def _terminate(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _iter_exact_pipeline(
    identity: Mapping[str, object],
    geng: Mapping[str, object],
) -> Iterator[str]:
    toolchain = identity.get("toolchain")
    if not isinstance(toolchain, Mapping):
        raise ThreeDegree5RunAuditError("identity has no verified toolchain")
    pickg = toolchain.get("pickg")
    if not isinstance(pickg, Mapping):
        raise ThreeDegree5RunAuditError("identity has no verified pickg")
    raw_geng_command = identity.get("catalogue_command")
    raw_pickg_command = identity.get("catalogue_filter_command")
    if not isinstance(raw_geng_command, list) or not isinstance(
        raw_pickg_command, list
    ):
        raise ThreeDegree5RunAuditError(
            "catalogue pipeline command is malformed"
        )
    geng_command = [str(item) for item in raw_geng_command]
    pickg_command = [str(item) for item in raw_pickg_command]
    environment = _pipeline_environment(geng, pickg)
    for name, record in (("geng", geng), ("pickg", pickg)):
        raw_path = record.get("path")
        linkage = record.get("dynamic_linkage")
        if (
            not isinstance(raw_path, str)
            or not isinstance(linkage, Mapping)
            or base_audit._current_dynamic_linkage(
                Path(raw_path), environment
            )
            != linkage
        ):
            raise ThreeDegree5RunAuditError(
                f"pipeline dynamic linkage drift: {name}"
            )

    with (
        tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as geng_error,
        tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as pickg_error,
    ):
        geng_process = subprocess.Popen(
            geng_command,
            stdout=subprocess.PIPE,
            stderr=geng_error,
            text=True,
            bufsize=1,
            env=environment,
        )
        if geng_process.stdout is None:
            _terminate(geng_process)
            raise ThreeDegree5RunAuditError(
                "could not open frozen geng pipeline output"
            )
        try:
            pickg_process = subprocess.Popen(
                pickg_command,
                stdin=geng_process.stdout,
                stdout=subprocess.PIPE,
                stderr=pickg_error,
                text=True,
                bufsize=1,
                env=environment,
            )
        except BaseException:
            geng_process.stdout.close()
            _terminate(geng_process)
            raise
        geng_process.stdout.close()
        if pickg_process.stdout is None:
            _terminate(pickg_process)
            _terminate(geng_process)
            raise ThreeDegree5RunAuditError(
                "could not open frozen pickg pipeline output"
            )
        completed_normally = False
        try:
            for raw_line in pickg_process.stdout:
                record = raw_line.strip()
                if not record or record.startswith(">"):
                    raise ThreeDegree5RunAuditError(
                        "frozen geng|pickg emitted a non-graph6 line"
                    )
                yield record
            pickg_code = pickg_process.wait()
            geng_code = geng_process.wait()
            geng_error.seek(0)
            pickg_error.seek(0)
            geng_stderr = geng_error.read().strip()
            pickg_stderr = pickg_error.read().strip()
            completed_normally = True
            if (
                geng_code != 0
                or pickg_code != 0
                or geng_stderr
                or pickg_stderr
            ):
                raise ThreeDegree5RunAuditError(
                    "frozen geng|pickg catalogue failed "
                    f"(geng={geng_code}, pickg={pickg_code}): "
                    f"geng stderr={geng_stderr!r}; "
                    f"pickg stderr={pickg_stderr!r}"
                )
        finally:
            pickg_process.stdout.close()
            if not completed_normally:
                _terminate(pickg_process)
                _terminate(geng_process)


@contextmanager
def _three_degree5_audit_context() -> Iterator[None]:
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
            "TOOL_NAMES",
            "_validate_identity",
            "_validate_catalogue_graph",
            "_iter_recorded_catalogue",
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
            "TOOL_NAMES": TOOL_NAMES,
            "_validate_identity": _validate_identity,
            "_validate_catalogue_graph": _validate_exact_catalogue_graph,
            "_iter_recorded_catalogue": _iter_exact_pipeline,
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
        "three_degree5_contract_wrapper": {
            "path": str(wrapper_path),
            "sha256": base_audit._file_sha256(wrapper_path),
        },
        "independent_base_engine": {
            "path": str(base_path),
            "sha256": base_audit._file_sha256(base_path),
        },
        "reuse_boundary": (
            "the wrapper freezes and reruns the exact geng|pickg pipeline, "
            "degree sequence, tool set, and layout; the base engine "
            "independently decodes graph6, checks filters and witnesses, "
            "verifies hashes, and replays every event"
        ),
    }


def _decorate_report(report: Mapping[str, object]) -> dict[str, object]:
    provenance = _auditor_provenance()
    base_record = provenance["independent_base_engine"]
    assert isinstance(base_record, Mapping)
    if report.get("auditor_sha256") != base_record["sha256"]:
        raise ThreeDegree5RunAuditError(
            "base audit report did not bind the executing base auditor"
        )
    decorated = dict(report)
    decorated.pop("auditor_sha256", None)
    decorated["auditor_provenance"] = provenance
    return decorated


def audit_three_degree5_shard(
    directory: Path, *, expected_shard: int
) -> dict[str, object]:
    if expected_shard not in EXPECTED_BY_SHARD:
        raise ThreeDegree5RunAuditError(
            "invalid expected three-degree-5 shard"
        )
    with _three_degree5_audit_context():
        report = base_audit.audit_dense_shard(
            directory, expected_shard=expected_shard
        )
    return _decorate_report(report)


def audit_three_degree5_campaign(root: Path) -> dict[str, object]:
    with _three_degree5_audit_context():
        report = base_audit.audit_dense_campaign(root)
    decorated = _decorate_report(report)
    raw_shards = decorated.get("shards")
    if not isinstance(raw_shards, list) or len(raw_shards) != SHARD_COUNT:
        raise ThreeDegree5RunAuditError(
            "base audit returned an incomplete shard set"
        )
    decorated["shards"] = [
        _decorate_report(shard)
        for shard in raw_shards
        if isinstance(shard, Mapping)
    ]
    if len(decorated["shards"]) != SHARD_COUNT:
        raise ThreeDegree5RunAuditError(
            "base audit returned a malformed shard report"
        )
    if (
        decorated.get("audit_schema") != AUDIT_SCHEMA
        or decorated.get("shard_count") != SHARD_COUNT
        or decorated.get("expected_total") != EXPECTED_TOTAL
        or decorated.get("audited_total") != EXPECTED_TOTAL
    ):
        raise ThreeDegree5RunAuditError(
            "decorated campaign report does not exactly close "
            "the three-degree-5 catalogue"
        )
    return decorated


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only independent audit of the exact OPG-145 "
            "n=11,m=23,(5^3,4^7,3) sixteen-shard campaign."
        )
    )
    parser.add_argument("campaign_root", type=Path)
    arguments = parser.parse_args(argv)
    try:
        report = audit_three_degree5_campaign(arguments.campaign_root)
    except (ThreeDegree5RunAuditError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
