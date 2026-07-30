"""Independent fail-closed audit of the OPG-145 degree-two critical backup.

The audited catalogue is exactly

``geng -q -C -d2 -D5 11 23:23 i/16``.

Every graph is decoded and classified again without importing the search
runner.  The first class is only an external partition: graphs with no
degree-two vertex belong to the five disjoint ``delta >= 3`` campaigns and
are *not* claimed positive here.  The next two classes are covered by the
degree-two suppression and common-missing-colour extension lemmas.  Only the
residual class is allowed to carry a SAT coloring witness.

The module deliberately reuses only generic, runner-independent primitives
from :mod:`opg145_dense_run_audit`: compact graph6 decoding, stable file
reads, tool/dependency verification, and the union-find coloring verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
import time
from typing import BinaryIO, Iterator, Mapping, Sequence

import amra.discovery.opg145_dense_run_audit as base_audit


AUDIT_SCHEMA = (
    "amra.opg145.n11-m23-d2-d5-degree2-critical-16.audit.v1"
)
CHECKPOINT_SCHEMA = (
    "amra.opg145.n11-m23-d2-d5-degree2-critical-16.checkpoint.v1"
)
EVENT_SCHEMA = (
    "amra.opg145.n11-m23-d2-d5-degree2-critical-16.event.v1"
)
CAMPAIGN = "opg145_n11_edge23_degree2_critical_16shard_exact"
ORDER = 11
EDGE_COUNT = 23
COLOR_COUNT = 7
SHARD_COUNT = 16
MINIMUM_DEGREE = 2
MAXIMUM_DEGREE = 5

EXPECTED_GENERATED_BY_SHARD: tuple[int, ...] = (
    80_617,
    99_770,
    132_255,
    153_050,
    129_042,
    133_346,
    143_824,
    102_642,
    187_137,
    172_013,
    121_368,
    148_261,
    107_103,
    100_732,
    113_832,
    88_026,
)
EXPECTED_NO_DEGREE2_BY_SHARD: tuple[int, ...] = (
    42_771,
    55_312,
    75_989,
    80_125,
    74_106,
    69_577,
    71_813,
    59_380,
    101_168,
    94_270,
    63_662,
    74_137,
    61_272,
    55_012,
    68_262,
    47_952,
)
EXPECTED_SUPPRESSIBLE_BY_SHARD: tuple[int, ...] = (
    26_328,
    32_848,
    41_770,
    51_564,
    40_556,
    40_955,
    48_418,
    26_679,
    60_258,
    59_555,
    39_040,
    50_719,
    33_828,
    31_289,
    34_989,
    27_759,
)
EXPECTED_COMMON_MISSING_BY_SHARD: tuple[int, ...] = (
    5_705,
    5_908,
    7_254,
    10_398,
    7_871,
    10_925,
    10_982,
    8_660,
    13_431,
    8_229,
    8_321,
    12_279,
    6_067,
    7_353,
    5_227,
    6_043,
)
EXPECTED_RESIDUAL_BY_SHARD: tuple[int, ...] = (
    5_813,
    5_702,
    7_242,
    10_963,
    6_509,
    11_889,
    12_611,
    7_923,
    12_280,
    9_959,
    10_345,
    11_126,
    5_936,
    7_078,
    5_354,
    6_272,
)

EXPECTED_GENERATED_TOTAL = 2_013_018
EXPECTED_NO_DEGREE2_TOTAL = 1_094_808
EXPECTED_SUPPRESSIBLE_TOTAL = 646_555
EXPECTED_COMMON_MISSING_TOTAL = 134_653
EXPECTED_RESIDUAL_TOTAL = 137_002

NO_DEGREE2_CLASS = "no_degree2_external_delta3_strata"
SUPPRESSIBLE_CLASS = "suppressible_nonadjacent_degree2"
COMMON_MISSING_CLASS = "common_missing_triangle_degree2"
RESIDUAL_CLASS = "degree2_critical_residual"
CLASSIFICATION_ORDER = (
    NO_DEGREE2_CLASS,
    SUPPRESSIBLE_CLASS,
    COMMON_MISSING_CLASS,
    RESIDUAL_CLASS,
)
PARTITION_CLASSES = frozenset(CLASSIFICATION_ORDER)

COUNTER_KEYS = (
    "generated",
    "filtered_no_degree2",
    "filtered_suppressible",
    "filtered_common_missing",
    "eligible",
    "sat",
    "unsat",
    "timeouts",
    "unknown",
)

EXPECTED_BY_SHARD = {
    index: count
    for index, count in enumerate(EXPECTED_GENERATED_BY_SHARD)
}
EXPECTED_TOTAL = EXPECTED_GENERATED_TOTAL

DISCOVERY_DIRECTORY = Path(__file__).resolve().parent
EXPECTED_IMPLEMENTATION_FILES = (
    (
        "degree2_critical_runner",
        DISCOVERY_DIRECTORY / "opg145_edge23_degree2_critical_search.py",
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
        "shard",
        "expected_generated",
        "expected_partition_counts",
        "expected_denominator_manifest",
        "color_count",
        "classification_policy",
        "positive_basis",
        "catalogue_command",
        "catalogue_command_canonical",
        "catalogue_environment_contract",
        "per_instance_seconds",
        "checkpoint_interval_records",
        "event_policy",
        "fixed_campaign_contract",
        "implementation",
        "toolchain",
    )
)

Degree2CriticalRunAuditError = base_audit.DenseRunAuditError
AuditGraph = base_audit.AuditGraph


def _partition_row(shard: int) -> dict[str, int]:
    return {
        "generated": EXPECTED_GENERATED_BY_SHARD[shard],
        "filtered_no_degree2": EXPECTED_NO_DEGREE2_BY_SHARD[shard],
        "filtered_suppressible": EXPECTED_SUPPRESSIBLE_BY_SHARD[shard],
        "filtered_common_missing": EXPECTED_COMMON_MISSING_BY_SHARD[shard],
        "eligible_residual": EXPECTED_RESIDUAL_BY_SHARD[shard],
    }


def _expected_manifest() -> dict[str, object]:
    """Return the exact independently reproduced denominator contract."""

    return {
        "method": "two_independent_exact_graph6_stream_classifications",
        "count_command_canonical": [
            "geng",
            "-q",
            "-C",
            "-d2",
            "-D5",
            str(ORDER),
            f"{EDGE_COUNT}:{EDGE_COUNT}",
            "i/16",
        ],
        "classification_order": list(CLASSIFICATION_ORDER),
        "classification_contract": {
            NO_DEGREE2_CLASS: (
                "minimum degree is at least 3; this is only a disjoint "
                "partition routed to external delta>=3 campaigns"
            ),
            SUPPRESSIBLE_CLASS: (
                "minimum degree is 2 and some degree-2 vertex has "
                "nonadjacent neighbours"
            ),
            COMMON_MISSING_CLASS: (
                "every degree-2 vertex has adjacent neighbours, but some "
                "such vertex is not flanked by two degree-5 vertices"
            ),
            RESIDUAL_CLASS: (
                "minimum degree is 2 and every degree-2 vertex has "
                "adjacent degree-5 neighbours"
            ),
        },
        "shard_count": SHARD_COUNT,
        "per_shard": {
            str(index): _partition_row(index)
            for index in range(SHARD_COUNT)
        },
        "totals": {
            "generated": EXPECTED_GENERATED_TOTAL,
            "filtered_no_degree2": EXPECTED_NO_DEGREE2_TOTAL,
            "filtered_suppressible": EXPECTED_SUPPRESSIBLE_TOTAL,
            "filtered_common_missing": EXPECTED_COMMON_MISSING_TOTAL,
            "eligible_residual": EXPECTED_RESIDUAL_TOTAL,
        },
    }


def _validate_frozen_tables() -> None:
    rows_and_totals = (
        (EXPECTED_GENERATED_BY_SHARD, EXPECTED_GENERATED_TOTAL),
        (EXPECTED_NO_DEGREE2_BY_SHARD, EXPECTED_NO_DEGREE2_TOTAL),
        (EXPECTED_SUPPRESSIBLE_BY_SHARD, EXPECTED_SUPPRESSIBLE_TOTAL),
        (EXPECTED_COMMON_MISSING_BY_SHARD, EXPECTED_COMMON_MISSING_TOTAL),
        (EXPECTED_RESIDUAL_BY_SHARD, EXPECTED_RESIDUAL_TOTAL),
    )
    for row, total in rows_and_totals:
        if len(row) != SHARD_COUNT or sum(row) != total:
            raise RuntimeError("a frozen degree-two denominator row is inconsistent")
    for shard in range(SHARD_COUNT):
        if EXPECTED_GENERATED_BY_SHARD[shard] != (
            EXPECTED_NO_DEGREE2_BY_SHARD[shard]
            + EXPECTED_SUPPRESSIBLE_BY_SHARD[shard]
            + EXPECTED_COMMON_MISSING_BY_SHARD[shard]
            + EXPECTED_RESIDUAL_BY_SHARD[shard]
        ):
            raise RuntimeError(
                f"the frozen partition does not close at shard {shard}"
            )


_validate_frozen_tables()


def _adjacency_sets(graph: AuditGraph) -> tuple[frozenset[int], ...]:
    rows: list[set[int]] = [set() for _ in range(graph.vertex_count)]
    seen: set[tuple[int, int]] = set()
    for edge in graph.edges:
        if (
            not isinstance(edge, tuple)
            or len(edge) != 2
            or type(edge[0]) is not int
            or type(edge[1]) is not int
        ):
            raise Degree2CriticalRunAuditError("graph has a malformed edge")
        left, right = edge
        if (
            not 0 <= left < right < graph.vertex_count
            or edge in seen
        ):
            raise Degree2CriticalRunAuditError(
                "graph is not a canonical finite simple graph"
            )
        seen.add(edge)
        rows[left].add(right)
        rows[right].add(left)
    return tuple(frozenset(row) for row in rows)


def _is_biconnected(
    adjacency: tuple[frozenset[int], ...],
) -> bool:
    """Check connectivity after deleting each single vertex."""

    order = len(adjacency)
    if order < 3:
        return False
    for removed in range(-1, order):
        start = next(
            (
                vertex
                for vertex in range(order)
                if vertex != removed
            ),
            None,
        )
        if start is None:
            return False
        reached = {start}
        pending = [start]
        while pending:
            vertex = pending.pop()
            for neighbour in adjacency[vertex]:
                if neighbour == removed or neighbour in reached:
                    continue
                reached.add(neighbour)
                pending.append(neighbour)
        expected = order if removed == -1 else order - 1
        if len(reached) != expected:
            return False
    return True


def _validate_catalogue_graph(graph: AuditGraph) -> None:
    """Verify all graph constraints independently of ``geng``."""

    adjacency = _adjacency_sets(graph)
    degrees = tuple(len(row) for row in adjacency)
    if (
        graph.vertex_count != ORDER
        or len(graph.edges) != EDGE_COUNT
        or min(degrees, default=0) < MINIMUM_DEGREE
        or max(degrees, default=0) > MAXIMUM_DEGREE
        or tuple(graph.degrees) != degrees
        or not _is_biconnected(adjacency)
    ):
        raise Degree2CriticalRunAuditError(
            "regenerated graph violates the frozen catalogue constraints"
        )


def classify_degree2_critical_graph(graph: AuditGraph) -> str:
    """Classify a valid catalogue graph by the exact priority contract."""

    _validate_catalogue_graph(graph)
    degrees = graph.degrees
    adjacency = _adjacency_sets(graph)
    degree2_vertices = tuple(
        vertex for vertex, degree in enumerate(degrees) if degree == 2
    )
    if not degree2_vertices:
        return NO_DEGREE2_CLASS

    for vertex in degree2_vertices:
        neighbours = tuple(sorted(adjacency[vertex]))
        if len(neighbours) != 2:
            raise Degree2CriticalRunAuditError(
                "degree-two adjacency reconstruction failed"
            )
        if neighbours[1] not in adjacency[neighbours[0]]:
            return SUPPRESSIBLE_CLASS

    for vertex in degree2_vertices:
        neighbours = tuple(sorted(adjacency[vertex]))
        if sum(degrees[neighbour] for neighbour in neighbours) <= 9:
            return COMMON_MISSING_CLASS

    # Both neighbours have degree at most five, so a sum greater than nine
    # forces the residual local profile (5,5).
    if any(
        degrees[neighbour] != MAXIMUM_DEGREE
        for vertex in degree2_vertices
        for neighbour in adjacency[vertex]
    ):
        raise Degree2CriticalRunAuditError(
            "degree-two residual implication failed"
        )
    return RESIDUAL_CLASS


def _degree2_local_profiles(graph: AuditGraph) -> list[dict[str, object]]:
    """Reconstruct the complete persisted local-profile witness."""

    degrees = graph.degrees
    adjacency = _adjacency_sets(graph)
    profiles: list[dict[str, object]] = []
    for vertex, degree in enumerate(degrees):
        if degree != 2:
            continue
        neighbours = tuple(sorted(adjacency[vertex]))
        if len(neighbours) != 2:
            raise Degree2CriticalRunAuditError(
                "degree-two profile reconstruction failed"
            )
        profiles.append(
            {
                "vertex": vertex,
                "neighbours": list(neighbours),
                "neighbour_degrees": [
                    degrees[neighbour] for neighbour in neighbours
                ],
                "neighbours_adjacent": (
                    neighbours[1] in adjacency[neighbours[0]]
                ),
            }
        )
    return profiles


def _verify_implementation(identity: Mapping[str, object]) -> str:
    """Bind the audit to the exact runner and shared coloring source."""

    implementation = identity.get("implementation")
    if not isinstance(implementation, Mapping) or set(implementation) != {
        "aggregate_sha256",
        "files",
    }:
        raise Degree2CriticalRunAuditError(
            "identity has a malformed implementation record"
        )
    raw_files = implementation.get("files")
    if not isinstance(raw_files, list) or len(raw_files) != len(
        EXPECTED_IMPLEMENTATION_FILES
    ):
        raise Degree2CriticalRunAuditError(
            "degree-two critical implementation file set is incomplete"
        )

    aggregate = hashlib.sha256()
    for raw_record, (expected_role, raw_expected_path) in zip(
        raw_files, EXPECTED_IMPLEMENTATION_FILES
    ):
        if (
            not isinstance(raw_record, Mapping)
            or set(raw_record) != {"role", "path", "sha256"}
        ):
            raise Degree2CriticalRunAuditError(
                "malformed degree-two critical implementation file record"
            )
        expected_path = raw_expected_path.resolve()
        if raw_record.get("role") != expected_role:
            raise Degree2CriticalRunAuditError(
                f"implementation role/order drift: {expected_role}"
            )
        if raw_record.get("path") != str(expected_path):
            raise Degree2CriticalRunAuditError(
                f"implementation directory drift: {raw_record.get('path')}"
            )
        if expected_path.is_symlink() or not expected_path.is_file():
            raise Degree2CriticalRunAuditError(
                f"implementation file disappeared or redirected: {expected_path}"
            )
        actual_sha = base_audit._file_sha256(expected_path)
        if (
            not base_audit._is_sha256(raw_record.get("sha256"))
            or raw_record.get("sha256") != actual_sha
        ):
            raise Degree2CriticalRunAuditError(
                f"implementation hash changed: {expected_path}"
            )
        aggregate.update(str(expected_path).encode("utf-8"))
        aggregate.update(actual_sha.encode("ascii"))

    aggregate_sha = aggregate.hexdigest()
    if implementation.get("aggregate_sha256") != aggregate_sha:
        raise Degree2CriticalRunAuditError(
            "implementation aggregate hash is inconsistent"
        )
    return aggregate_sha


def _validate_identity(
    state: Mapping[str, object], expected_shard: int
) -> tuple[Mapping[str, object], Mapping[str, object], str, str]:
    """Validate every frozen identity field before catalogue replay."""

    if state.get("checkpoint_schema") != CHECKPOINT_SCHEMA:
        raise Degree2CriticalRunAuditError(
            "checkpoint schema is not the frozen degree-two critical schema"
        )
    if state.get("status") != "complete":
        raise Degree2CriticalRunAuditError(
            "audit is allowed only after status=complete"
        )
    if not 0 <= expected_shard < SHARD_COUNT:
        raise Degree2CriticalRunAuditError("invalid expected shard")

    identity = state.get("identity")
    if not isinstance(identity, Mapping):
        raise Degree2CriticalRunAuditError("checkpoint has no identity object")
    if set(identity) != EXPECTED_IDENTITY_KEYS:
        raise Degree2CriticalRunAuditError(
            "degree-two critical identity field set has drifted"
        )
    identity_sha = base_audit._json_sha256(identity)
    if (
        state.get("identity_sha256") != identity_sha
        or not base_audit._is_sha256(identity_sha)
    ):
        raise Degree2CriticalRunAuditError(
            "checkpoint identity digest is inconsistent"
        )

    exact_fields: dict[str, object] = {
        "campaign": CAMPAIGN,
        "problem": "opg145",
        "order": ORDER,
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "generator_degree_range": [MINIMUM_DEGREE, MAXIMUM_DEGREE],
        "shard": [expected_shard, SHARD_COUNT],
        "expected_generated": EXPECTED_GENERATED_BY_SHARD[expected_shard],
        "expected_partition_counts": _partition_row(expected_shard),
        "expected_denominator_manifest": _expected_manifest(),
        "color_count": COLOR_COUNT,
        "classification_policy": (
            "degree2_reduction_with_external_delta3_partition_v1"
        ),
        "positive_basis": {
            NO_DEGREE2_CLASS: "external_disjoint_campaigns",
            SUPPRESSIBLE_CLASS: "degree2_suppression_extension_lemma",
            COMMON_MISSING_CLASS: (
                "degree2_common_missing_extension_lemma"
            ),
            RESIDUAL_CLASS: "solver_required",
        },
        "catalogue_environment_contract": {
            "locale": "C",
            "dynamic_library_directories": (
                "recorded_geng_dependency_parents"
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
            "shard_notation": "i/16",
            "classification_order": list(CLASSIFICATION_ORDER),
            "caller_configurable_catalogue": False,
        },
    }
    for field, expected in exact_fields.items():
        if identity.get(field) != expected:
            raise Degree2CriticalRunAuditError(
                f"frozen degree-two critical identity field drift: {field}"
            )

    per_instance = identity.get("per_instance_seconds")
    if (
        not isinstance(per_instance, (int, float))
        or isinstance(per_instance, bool)
        or not math.isfinite(float(per_instance))
        or float(per_instance) <= 0
    ):
        raise Degree2CriticalRunAuditError("invalid per-instance solver budget")

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
        raise Degree2CriticalRunAuditError(
            "catalogue command is not the exact frozen degree-two command"
        )
    return identity, geng, implementation_sha, toolchain_sha


def _validate_closed_state(
    state: Mapping[str, object], expected_shard: int
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for key in COUNTER_KEYS:
        value = state.get(key)
        if type(value) is not int or value < 0:
            raise Degree2CriticalRunAuditError(
                f"invalid checkpoint counter: {key}"
            )
        counts[key] = value

    expected_generated = EXPECTED_GENERATED_BY_SHARD[expected_shard]
    expected_residual = EXPECTED_RESIDUAL_BY_SHARD[expected_shard]
    if (
        state.get("catalogue_exhausted") is not True
        or state.get("next_index") != expected_generated
        or counts["generated"] != expected_generated
        or counts["filtered_no_degree2"]
        != EXPECTED_NO_DEGREE2_BY_SHARD[expected_shard]
        or counts["filtered_suppressible"]
        != EXPECTED_SUPPRESSIBLE_BY_SHARD[expected_shard]
        or counts["filtered_common_missing"]
        != EXPECTED_COMMON_MISSING_BY_SHARD[expected_shard]
        or counts["eligible"] != expected_residual
        or counts["sat"] != expected_residual
        or counts["generated"]
        != (
            counts["filtered_no_degree2"]
            + counts["filtered_suppressible"]
            + counts["filtered_common_missing"]
            + counts["eligible"]
        )
        or counts["unsat"] != 0
        or counts["timeouts"] != 0
        or counts["unknown"] != 0
    ):
        raise Degree2CriticalRunAuditError(
            "checkpoint accounting is not exactly closed"
        )
    if not base_audit._is_sha256(state.get("events_sha256")):
        raise Degree2CriticalRunAuditError(
            "complete checkpoint has no valid events hash"
        )
    return counts


def _iter_regenerated_catalogue(
    identity: Mapping[str, object],
    geng: Mapping[str, object],
    *,
    expected_shard: int,
) -> Iterator[tuple[AuditGraph, str]]:
    """Regenerate, decode, validate, and classify an exact full shard."""

    command = identity.get("catalogue_command")
    if not isinstance(command, list) or any(
        not isinstance(item, str) for item in command
    ):
        raise Degree2CriticalRunAuditError("catalogue command is malformed")
    expected_command = [
        str(geng["path"]),
        "-q",
        "-C",
        "-d2",
        "-D5",
        str(ORDER),
        f"{EDGE_COUNT}:{EDGE_COUNT}",
        f"{expected_shard}/{SHARD_COUNT}",
    ]
    if command != expected_command:
        raise Degree2CriticalRunAuditError(
            "catalogue command drifted after identity validation"
        )

    observed = {
        NO_DEGREE2_CLASS: 0,
        SUPPRESSIBLE_CLASS: 0,
        COMMON_MISSING_CLASS: 0,
        RESIDUAL_CLASS: 0,
    }
    generated = 0
    with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as error_file:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=error_file,
            text=True,
            bufsize=1,
            env=base_audit._frozen_environment(geng),
        )
        if process.stdout is None:
            process.terminate()
            raise Degree2CriticalRunAuditError(
                "could not open frozen geng output"
            )
        completed_normally = False
        try:
            for raw_line in process.stdout:
                record = raw_line.strip()
                if (
                    not record
                    or record != raw_line.rstrip("\n")
                    or record.startswith(">")
                ):
                    raise Degree2CriticalRunAuditError(
                        "frozen geng emitted a noncanonical graph6 line"
                    )
                graph = base_audit.decode_graph6_independently(record)
                partition_class = classify_degree2_critical_graph(graph)
                observed[partition_class] += 1
                generated += 1
                yield graph, partition_class

            return_code = process.wait()
            error_file.seek(0)
            stderr = error_file.read()
            completed_normally = True
            if return_code != 0 or stderr.strip():
                raise Degree2CriticalRunAuditError(
                    f"frozen geng failed ({return_code}): {stderr.strip()}"
                )
            expected = {
                NO_DEGREE2_CLASS: (
                    EXPECTED_NO_DEGREE2_BY_SHARD[expected_shard]
                ),
                SUPPRESSIBLE_CLASS: (
                    EXPECTED_SUPPRESSIBLE_BY_SHARD[expected_shard]
                ),
                COMMON_MISSING_CLASS: (
                    EXPECTED_COMMON_MISSING_BY_SHARD[expected_shard]
                ),
                RESIDUAL_CLASS: EXPECTED_RESIDUAL_BY_SHARD[expected_shard],
            }
            if (
                generated != EXPECTED_GENERATED_BY_SHARD[expected_shard]
                or observed != expected
            ):
                raise Degree2CriticalRunAuditError(
                    "regenerated structural partition differs from the "
                    "frozen independent denominators"
                )
        finally:
            process.stdout.close()
            if not completed_normally and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)


def _validate_graph_payload(
    event: Mapping[str, object], graph: AuditGraph, index: int
) -> None:
    if (
        event.get("graph6") != graph.graph6
        or event.get("vertices") != graph.vertex_count
        or event.get("edge_count") != len(graph.edges)
        or event.get("edges") != [list(edge) for edge in graph.edges]
        or event.get("degrees") != list(graph.degrees)
    ):
        raise Degree2CriticalRunAuditError(
            f"event {index} does not bind the complete graph payload"
        )


def _validate_sat_metadata(
    event: Mapping[str, object], graph: AuditGraph, index: int
) -> None:
    elapsed = event.get("elapsed_seconds")
    cuts = event.get("lazy_cycle_cuts")
    variables = event.get("variables")
    clauses = event.get("clauses")
    base_clause_count = (
        len(graph.edges) * (1 + COLOR_COUNT * (COLOR_COUNT - 1) // 2)
        + sum(
            degree * (degree - 1) // 2 * COLOR_COUNT
            for degree in graph.degrees
        )
        + 1
    )
    if (
        not isinstance(elapsed, (int, float))
        or isinstance(elapsed, bool)
        or not math.isfinite(float(elapsed))
        or float(elapsed) < 0
        or type(cuts) is not int
        or cuts < 0
        or variables != len(graph.edges) * COLOR_COUNT
        or clauses != base_clause_count + cuts
        or event.get("lazy_cycle_certificate") is not None
        or any(
            not base_audit._is_sha256(event.get(field))
            for field in (
                "cnf_sha256",
                "lazy_cycle_records_sha256",
                "solver_stdout_sha256",
                "solver_stderr_sha256",
            )
        )
    ):
        raise Degree2CriticalRunAuditError(
            f"event {index} has invalid SAT/CNF metadata"
        )


def _validate_event(
    event: Mapping[str, object],
    regenerated_graph: AuditGraph,
    partition_class: str,
    index: int,
    identity_sha: str,
) -> str:
    """Validate an event against an independently regenerated graph."""

    if (
        event.get("event_schema") != EVENT_SCHEMA
        or event.get("identity_sha256") != identity_sha
        or event.get("problem") != "opg145"
        or event.get("order") != ORDER
        or type(event.get("index")) is not int
        or event.get("index") != index
    ):
        raise Degree2CriticalRunAuditError(
            f"event identity/index drift at {index}"
        )

    event_record = event.get("graph6")
    if not isinstance(event_record, str):
        raise Degree2CriticalRunAuditError(f"event {index} has no graph6")
    event_graph = base_audit.decode_graph6_independently(event_record)
    _validate_catalogue_graph(event_graph)
    if (
        event_graph.graph6 != regenerated_graph.graph6
        or event_graph.edges != regenerated_graph.edges
    ):
        raise Degree2CriticalRunAuditError(
            f"catalogue/event graph6 mismatch at {index}"
        )
    _validate_graph_payload(event, event_graph, index)

    event_time = event.get("time_unix")
    if (
        not isinstance(event_time, (int, float))
        or isinstance(event_time, bool)
        or not math.isfinite(float(event_time))
    ):
        raise Degree2CriticalRunAuditError(
            f"event {index} has invalid timing metadata"
        )

    independently_classified = classify_degree2_critical_graph(event_graph)
    if (
        independently_classified != partition_class
        or event.get("partition_class") != partition_class
        or event.get("degree2_local_profiles")
        != _degree2_local_profiles(event_graph)
    ):
        raise Degree2CriticalRunAuditError(
            f"event {index} has a wrong degree-two partition witness"
        )

    status = event.get("status")
    if partition_class != RESIDUAL_CLASS:
        is_external = partition_class == NO_DEGREE2_CLASS
        expected_basis = {
            NO_DEGREE2_CLASS: "external_disjoint_campaigns",
            SUPPRESSIBLE_CLASS: "degree2_suppression_extension_lemma",
            COMMON_MISSING_CLASS: (
                "degree2_common_missing_extension_lemma"
            ),
        }[partition_class]
        if (
            status
            != ("partition_filtered" if is_external else "theorem_filtered")
            or event.get("filter_reason") != partition_class
            or event.get("positive_basis") != expected_basis
            or event.get("mathematical_positive_claimed") is not (
                not is_external
            )
            or event.get("eligible") is not False
            or event.get("verified_coloring") is not None
        ):
            raise Degree2CriticalRunAuditError(
                f"event {index} has invalid filtered semantics"
            )
        return {
            NO_DEGREE2_CLASS: "filtered_no_degree2",
            SUPPRESSIBLE_CLASS: "filtered_suppressible",
            COMMON_MISSING_CLASS: "filtered_common_missing",
        }[partition_class]

    if (
        status != "sat"
        or event.get("filter_reason") is not None
        or event.get("positive_basis") != "solver_verified_witness"
        or event.get("mathematical_positive_claimed") is not True
        or event.get("eligible") is not True
    ):
        raise Degree2CriticalRunAuditError(
            f"event {index} is not a valid residual SAT result"
        )
    _validate_sat_metadata(event, event_graph, index)
    if not base_audit.verify_acyclic_seven_edge_coloring_independently(
        event_graph, event.get("verified_coloring")
    ):
        raise Degree2CriticalRunAuditError(
            f"event {index} has an invalid acyclic seven-edge-coloring"
        )
    return "sat"


def _open_verified_events(
    path: Path, expected_sha: str
) -> tuple[BinaryIO, tuple[int, int, int, int]]:
    if path.is_symlink() or not path.is_file():
        raise Degree2CriticalRunAuditError(
            f"missing or redirected events file: {path}"
        )
    handle = path.open("rb")
    before = os.fstat(handle.fileno())
    digest = hashlib.sha256()
    for block in iter(lambda: handle.read(1 << 20), b""):
        digest.update(block)
    if digest.hexdigest() != expected_sha:
        handle.close()
        raise Degree2CriticalRunAuditError(
            "events hash differs from the complete checkpoint"
        )
    handle.seek(0)
    return handle, (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )


def _parse_event(raw_line: bytes, index: int) -> Mapping[str, object]:
    if not raw_line.endswith(b"\n") or not raw_line.strip():
        raise Degree2CriticalRunAuditError(f"event {index} is truncated")
    try:
        event = json.loads(raw_line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Degree2CriticalRunAuditError(
            f"event {index} is invalid JSON"
        ) from error
    if not isinstance(event, Mapping):
        raise Degree2CriticalRunAuditError(
            f"event {index} is not an object"
        )
    return event


def _auditor_provenance() -> dict[str, object]:
    auditor_path = Path(__file__).resolve()
    primitive_path = Path(base_audit.__file__).resolve()
    return {
        "degree2_critical_independent_auditor": {
            "path": str(auditor_path),
            "sha256": base_audit._file_sha256(auditor_path),
        },
        "independent_primitive_library": {
            "path": str(primitive_path),
            "sha256": base_audit._file_sha256(primitive_path),
        },
        "runner_imported": False,
        "reuse_boundary": (
            "only graph6 decoding, stable reads, toolchain verification, "
            "and union-find coloring verification are reused; structural "
            "classification, event semantics, counters, and catalogue "
            "partition closure are implemented in this auditor"
        ),
    }


def audit_degree2_critical_shard(
    directory: Path, *, expected_shard: int
) -> dict[str, object]:
    """Read-only audit of one completed exact shard."""

    if not 0 <= expected_shard < SHARD_COUNT:
        raise Degree2CriticalRunAuditError("invalid expected shard")
    if (
        directory.is_symlink()
        or not directory.is_dir()
        or directory.name != f"shard-{expected_shard}"
    ):
        raise Degree2CriticalRunAuditError(
            "shard directory layout has drifted"
        )
    state_path = directory / "state.json"
    events_path = directory / "events.jsonl"
    if (directory / "state.json.tmp").exists():
        raise Degree2CriticalRunAuditError(
            "unfinished checkpoint temporary file remains"
        )

    state = base_audit._stable_json_object(state_path)
    identity, geng, implementation_sha, toolchain_sha = _validate_identity(
        state, expected_shard
    )
    state_counts = _validate_closed_state(state, expected_shard)
    identity_sha = str(state["identity_sha256"])

    events, initial_metadata = _open_verified_events(
        events_path, str(state["events_sha256"])
    )
    event_digest = hashlib.sha256()
    observed_counts = {key: 0 for key in COUNTER_KEYS}
    observed_catalogue = 0
    records = _iter_regenerated_catalogue(
        identity, geng, expected_shard=expected_shard
    )
    try:
        for index, (regenerated_graph, partition_class) in enumerate(records):
            if index >= EXPECTED_GENERATED_BY_SHARD[expected_shard]:
                raise Degree2CriticalRunAuditError(
                    "regenerated catalogue exceeds its frozen denominator"
                )
            raw_line = events.readline()
            if not raw_line:
                raise Degree2CriticalRunAuditError(
                    f"missing event at index {index}"
                )
            event_digest.update(raw_line)
            event = _parse_event(raw_line, index)
            outcome = _validate_event(
                event,
                regenerated_graph,
                partition_class,
                index,
                identity_sha,
            )
            observed_catalogue += 1
            observed_counts["generated"] += 1
            if outcome == "sat":
                observed_counts["eligible"] += 1
                observed_counts["sat"] += 1
            else:
                observed_counts[outcome] += 1

        trailing = events.read()
        event_digest.update(trailing)
        if trailing:
            raise Degree2CriticalRunAuditError(
                "events remain after catalogue exhaustion"
            )
    finally:
        close = getattr(records, "close", None)
        if close is not None:
            close()
        final_stat = os.fstat(events.fileno())
        events.close()

    final_metadata = (
        final_stat.st_dev,
        final_stat.st_ino,
        final_stat.st_size,
        final_stat.st_mtime_ns,
    )
    if final_metadata != initial_metadata:
        raise Degree2CriticalRunAuditError("events changed during audit")
    if event_digest.hexdigest() != state["events_sha256"]:
        raise Degree2CriticalRunAuditError(
            "events changed between hash and replay"
        )
    if observed_catalogue != EXPECTED_GENERATED_BY_SHARD[expected_shard]:
        raise Degree2CriticalRunAuditError(
            "regenerated catalogue does not equal the frozen denominator"
        )
    if observed_counts != state_counts:
        raise Degree2CriticalRunAuditError(
            "state counters do not equal independently audited events"
        )

    return {
        "audit_schema": AUDIT_SCHEMA,
        "status": "verified_complete",
        "directory": str(directory.resolve()),
        "shard": [expected_shard, SHARD_COUNT],
        "expected_generated": EXPECTED_GENERATED_BY_SHARD[expected_shard],
        "expected_residual": EXPECTED_RESIDUAL_BY_SHARD[expected_shard],
        "audited_counts": observed_counts,
        "events_sha256": state["events_sha256"],
        "identity_sha256": identity_sha,
        "implementation_sha256": implementation_sha,
        "toolchain_sha256": toolchain_sha,
        "auditor_provenance": _auditor_provenance(),
    }


def audit_degree2_critical_campaign(root: Path) -> dict[str, object]:
    """Audit exactly ``shard-0`` through ``shard-15`` and close all totals."""

    if root.is_symlink() or not root.is_dir():
        raise Degree2CriticalRunAuditError(
            "campaign root is missing or redirected"
        )
    expected_names = {
        f"shard-{index}" for index in range(SHARD_COUNT)
    }
    actual_names = {entry.name for entry in root.iterdir()}
    if actual_names != expected_names:
        raise Degree2CriticalRunAuditError(
            "campaign shard directory set has drifted"
        )

    reports = [
        audit_degree2_critical_shard(
            root / f"shard-{index}", expected_shard=index
        )
        for index in range(SHARD_COUNT)
    ]
    aggregate = {
        key: sum(
            int(report["audited_counts"][key])  # type: ignore[index]
            for report in reports
        )
        for key in COUNTER_KEYS
    }
    expected_aggregate = {
        "generated": EXPECTED_GENERATED_TOTAL,
        "filtered_no_degree2": EXPECTED_NO_DEGREE2_TOTAL,
        "filtered_suppressible": EXPECTED_SUPPRESSIBLE_TOTAL,
        "filtered_common_missing": EXPECTED_COMMON_MISSING_TOTAL,
        "eligible": EXPECTED_RESIDUAL_TOTAL,
        "sat": EXPECTED_RESIDUAL_TOTAL,
        "unsat": 0,
        "timeouts": 0,
        "unknown": 0,
    }
    if aggregate != expected_aggregate:
        raise Degree2CriticalRunAuditError(
            "campaign aggregate partition does not close"
        )
    if len({report["implementation_sha256"] for report in reports}) != 1:
        raise Degree2CriticalRunAuditError(
            "shards used different implementations"
        )
    if len({report["toolchain_sha256"] for report in reports}) != 1:
        raise Degree2CriticalRunAuditError(
            "shards used different toolchains"
        )

    return {
        "audit_schema": AUDIT_SCHEMA,
        "status": "verified_complete",
        "campaign_root": str(root.resolve()),
        "shard_count": SHARD_COUNT,
        "expected_total": EXPECTED_GENERATED_TOTAL,
        "expected_residual_total": EXPECTED_RESIDUAL_TOTAL,
        "audited_counts": aggregate,
        "auditor_provenance": _auditor_provenance(),
        "shards": reports,
        "audited_at_unix": time.time(),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only independent audit of the sixteen-shard OPG-145 "
            "n=11,m=23 degree-two critical backup campaign."
        )
    )
    parser.add_argument("campaign_root", type=Path)
    arguments = parser.parse_args(argv)
    try:
        report = audit_degree2_critical_campaign(arguments.campaign_root)
    except (Degree2CriticalRunAuditError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
