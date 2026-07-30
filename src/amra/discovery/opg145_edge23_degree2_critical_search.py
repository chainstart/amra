"""Exact OPG-145 search on the unresolved ``n=11,m=23`` degree-two layer.

The frozen catalogue is

``geng -q -C -d2 -D5 11 23:23 i/16``.

Every graph receives a durable event.  Graphs with no degree-two vertex,
with a suppressible degree-two vertex, or with an adjacent-neighbour
degree-two vertex not flanked by two degree-five vertices are classified
without SAT.  The residual graphs are passed to the existing independently
checkable seven-colour acyclic edge-colouring solver.  A shard is complete
only after exact catalogue exhaustion, exact classification denominators,
and zero timeout, unknown, or UNSAT result.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass, field
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
import time
from typing import Iterator, Mapping, Sequence

import amra.discovery.opg_coloring_search as coloring_search
from amra.discovery.opg_coloring_search import CNF, EdgeGraph, SolverResult


CHECKPOINT_SCHEMA = (
    "amra.opg145.n11-m23-d2-d5-degree2-critical-16.checkpoint.v1"
)
EVENT_SCHEMA = "amra.opg145.n11-m23-d2-d5-degree2-critical-16.event.v1"
CAMPAIGN = "opg145_n11_edge23_degree2_critical_16shard_exact"
ORDER = 11
EDGE_COUNT = 23
COLOR_COUNT = 7
SHARD_COUNT = 16
MINIMUM_DEGREE = 2
MAXIMUM_DEGREE = 5

# Independently counted twice with the exact graph6 stream.  The four rows
# form an exact mutually exclusive partition of every frozen shard.
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

for _name, _row, _total in (
    (
        "generated",
        EXPECTED_GENERATED_BY_SHARD,
        EXPECTED_GENERATED_TOTAL,
    ),
    (
        "no-degree-two",
        EXPECTED_NO_DEGREE2_BY_SHARD,
        EXPECTED_NO_DEGREE2_TOTAL,
    ),
    (
        "suppressible",
        EXPECTED_SUPPRESSIBLE_BY_SHARD,
        EXPECTED_SUPPRESSIBLE_TOTAL,
    ),
    (
        "common-missing",
        EXPECTED_COMMON_MISSING_BY_SHARD,
        EXPECTED_COMMON_MISSING_TOTAL,
    ),
    ("residual", EXPECTED_RESIDUAL_BY_SHARD, EXPECTED_RESIDUAL_TOTAL),
):
    if len(_row) != SHARD_COUNT or sum(_row) != _total:
        raise RuntimeError(f"frozen {_name} denominator table is inconsistent")
for _shard in range(SHARD_COUNT):
    if EXPECTED_GENERATED_BY_SHARD[_shard] != sum(
        row[_shard]
        for row in (
            EXPECTED_NO_DEGREE2_BY_SHARD,
            EXPECTED_SUPPRESSIBLE_BY_SHARD,
            EXPECTED_COMMON_MISSING_BY_SHARD,
            EXPECTED_RESIDUAL_BY_SHARD,
        )
    ):
        raise RuntimeError(
            f"frozen class partition is inconsistent at shard {_shard}"
        )

_COUNTER_KEYS = (
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
_SOLVER_STATUSES = frozenset(("sat", "unsat", "timeout", "unknown"))
_TERMINAL_EVENT_STATUSES = frozenset(("unsat", "timeout", "unknown"))
_TERMINAL_RUN_STATUSES = frozenset(
    (
        "complete",
        "stopped_unsat",
        "stopped_timeout",
        "stopped_unknown",
        "denominator_mismatch",
        "classification_denominator_mismatch",
    )
)


@dataclass(frozen=True)
class Degree2CriticalSearchConfig:
    """Immutable mathematical/search configuration for one catalogue shard."""

    shard_index: int
    expected_generated: int
    per_instance_seconds: float
    minimum_edges: int = field(default=EDGE_COUNT, init=False)
    maximum_edges: int = field(default=EDGE_COUNT, init=False)

    def validate(self) -> None:
        if type(self.shard_index) is not int or not (
            0 <= self.shard_index < SHARD_COUNT
        ):
            raise ValueError(f"shard index must lie in 0..{SHARD_COUNT - 1}")
        expected = EXPECTED_GENERATED_BY_SHARD[self.shard_index]
        if (
            type(self.expected_generated) is not int
            or self.expected_generated != expected
        ):
            raise ValueError(
                "the frozen degree-two denominator for shard "
                f"{self.shard_index}/{SHARD_COUNT} is {expected}"
            )
        if (
            not isinstance(self.per_instance_seconds, (int, float))
            or isinstance(self.per_instance_seconds, bool)
            or not math.isfinite(float(self.per_instance_seconds))
            or float(self.per_instance_seconds) <= 0
        ):
            raise ValueError("per_instance_seconds must be finite and positive")

    @property
    def shard(self) -> tuple[int, int]:
        return self.shard_index, SHARD_COUNT

    @property
    def edge_range(self) -> str:
        return f"{EDGE_COUNT}:{EDGE_COUNT}"


def config_for_shard(
    shard_index: int, per_instance_seconds: float
) -> Degree2CriticalSearchConfig:
    if type(shard_index) is not int or not 0 <= shard_index < SHARD_COUNT:
        raise ValueError(f"shard index must lie in 0..{SHARD_COUNT - 1}")
    return Degree2CriticalSearchConfig(
        shard_index=shard_index,
        expected_generated=EXPECTED_GENERATED_BY_SHARD[shard_index],
        per_instance_seconds=per_instance_seconds,
    )


def _json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _runtime_provenance() -> dict[str, object]:
    """Record the runner, shared implementation, binaries, and linked libraries."""

    runner_path = Path(__file__).resolve()
    shared_path = Path(coloring_search.__file__).resolve()
    paths = (
        ("degree2_critical_runner", runner_path),
        ("shared_coloring", shared_path),
    )
    implementation = {
        "aggregate_sha256": coloring_search.implementation_fingerprint(
            *(path for _, path in paths)
        ),
        "files": [
            {
                "role": role,
                "path": str(path),
                "sha256": coloring_search.file_sha256(path),
            }
            for role, path in paths
        ],
    }
    toolchain = coloring_search.toolchain_fingerprint(
        ("geng", "minisat", "cadical", "drat-trim")
    )
    for name, record in toolchain.items():
        if record.get("sha256") == "unavailable":
            raise FileNotFoundError(f"required frozen tool is unavailable: {name}")
        linkage = record.get("dynamic_linkage")
        if not isinstance(linkage, Mapping):
            raise RuntimeError(f"toolchain record for {name} has no linkage map")
        if linkage.get("missing"):
            raise RuntimeError(
                f"toolchain record for {name} has missing libraries: "
                f"{linkage['missing']}"
            )
        dependencies = linkage.get("dependencies")
        if not isinstance(dependencies, Mapping):
            raise RuntimeError(
                f"toolchain record for {name} has no dependency hashes"
            )
        for dependency, dependency_record in dependencies.items():
            if (
                not isinstance(dependency_record, Mapping)
                or not dependency_record.get("path")
                or not dependency_record.get("sha256")
            ):
                raise RuntimeError(
                    f"incomplete dependency fingerprint for {name}: {dependency}"
                )
    return {"implementation": implementation, "toolchain": toolchain}


def build_identity(config: Degree2CriticalSearchConfig) -> dict[str, object]:
    """Build the exact immutable identity checked on every continuation."""

    config.validate()
    provenance = _runtime_provenance()
    toolchain = provenance["toolchain"]
    assert isinstance(toolchain, Mapping)
    geng = toolchain["geng"]
    assert isinstance(geng, Mapping)
    geng_path = str(geng["path"])
    canonical_command = [
        "geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        str(ORDER),
        config.edge_range,
        f"{config.shard_index}/{SHARD_COUNT}",
    ]
    command = [geng_path, *canonical_command[1:]]
    denominator_manifest = {
        "method": (
            "two_independent_exact_graph6_stream_classifications"
        ),
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
        "classification_order": [
            "no_degree2_external_delta3_strata",
            "suppressible_nonadjacent_degree2",
            "common_missing_triangle_degree2",
            "degree2_critical_residual",
        ],
        "classification_contract": {
            "no_degree2_external_delta3_strata": (
                "minimum degree is at least 3; this is only a disjoint "
                "partition routed to external delta>=3 campaigns"
            ),
            "suppressible_nonadjacent_degree2": (
                "minimum degree is 2 and some degree-2 vertex has "
                "nonadjacent neighbours"
            ),
            "common_missing_triangle_degree2": (
                "every degree-2 vertex has adjacent neighbours, but some "
                "such vertex is not flanked by two degree-5 vertices"
            ),
            "degree2_critical_residual": (
                "minimum degree is 2 and every degree-2 vertex has "
                "adjacent degree-5 neighbours"
            ),
        },
        "shard_count": SHARD_COUNT,
        "per_shard": {
            str(index): {
                "generated": EXPECTED_GENERATED_BY_SHARD[index],
                "filtered_no_degree2": (
                    EXPECTED_NO_DEGREE2_BY_SHARD[index]
                ),
                "filtered_suppressible": (
                    EXPECTED_SUPPRESSIBLE_BY_SHARD[index]
                ),
                "filtered_common_missing": (
                    EXPECTED_COMMON_MISSING_BY_SHARD[index]
                ),
                "eligible_residual": EXPECTED_RESIDUAL_BY_SHARD[index],
            }
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
    return {
        "campaign": CAMPAIGN,
        "problem": "opg145",
        "order": ORDER,
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "generator_degree_range": [MINIMUM_DEGREE, MAXIMUM_DEGREE],
        "shard": [config.shard_index, SHARD_COUNT],
        "expected_generated": config.expected_generated,
        "expected_partition_counts": denominator_manifest["per_shard"][
            str(config.shard_index)
        ],
        "expected_denominator_manifest": denominator_manifest,
        "color_count": COLOR_COUNT,
        "classification_policy": (
            "degree2_reduction_with_external_delta3_partition_v1"
        ),
        "positive_basis": {
            "no_degree2_external_delta3_strata": (
                "external_disjoint_campaigns"
            ),
            "suppressible_nonadjacent_degree2": (
                "degree2_suppression_extension_lemma"
            ),
            "common_missing_triangle_degree2": (
                "degree2_common_missing_extension_lemma"
            ),
            "degree2_critical_residual": "solver_required",
        },
        "catalogue_command": command,
        "catalogue_command_canonical": canonical_command,
        "catalogue_environment_contract": {
            "locale": "C",
            "dynamic_library_directories": (
                "recorded_geng_dependency_parents"
            ),
            "removed_variables": ["LD_AUDIT", "LD_PRELOAD"],
        },
        "per_instance_seconds": config.per_instance_seconds,
        "checkpoint_interval_records": 1,
        "event_policy": "one_fsynced_event_per_generated_record",
        "fixed_campaign_contract": {
            "order": ORDER,
            "edge_count": EDGE_COUNT,
            "minimum_degree": MINIMUM_DEGREE,
            "maximum_degree": MAXIMUM_DEGREE,
            "shard_notation": "i/16",
            "classification_order": (
                denominator_manifest["classification_order"]
            ),
            "caller_configurable_catalogue": False,
        },
        **provenance,
    }


def _atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    directory_descriptor = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_descriptor)
    finally:
        os.close(directory_descriptor)


def _append_event(path: Path, event: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
        )
        handle.flush()
        os.fsync(handle.fileno())


@contextmanager
def _exclusive_output_lock(output: Path) -> Iterator[None]:
    output.mkdir(parents=True, exist_ok=True)
    lock_path = output / ".opg145-degree2-critical.lock"
    with lock_path.open("a+", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError(
                f"another OPG-145 degree-2 critical runner owns {output}"
            ) from error
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _catalogue_environment(geng_path: Path) -> dict[str, str]:
    linkage = coloring_search._shared_library_fingerprint(geng_path)
    if linkage.get("missing"):
        raise RuntimeError(
            f"geng has missing dynamic dependencies: {linkage['missing']}"
        )
    dependencies = linkage.get("dependencies")
    if not isinstance(dependencies, Mapping):
        raise RuntimeError("geng has no dynamic dependency map")
    directories: list[str] = []
    for raw_record in dependencies.values():
        if not isinstance(raw_record, Mapping):
            raise RuntimeError("geng has a malformed dependency record")
        raw_path = raw_record.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            raise RuntimeError("geng dependency record has no path")
        directory = str(Path(raw_path).parent)
        if directory not in directories:
            directories.append(directory)
    environment = dict(os.environ)
    environment.pop("LD_AUDIT", None)
    environment.pop("LD_PRELOAD", None)
    environment["LD_LIBRARY_PATH"] = os.pathsep.join(directories)
    environment["LC_ALL"] = "C"
    return environment


def _iter_catalogue_records(command: Sequence[str]) -> Iterator[str]:
    """Stream the exact graph6 shard with strict exit/stderr handling."""

    if (
        len(command) != 8
        or list(command[1:7])
        != ["-q", "-C", "-d2", "-D5", "11", "23:23"]
        or command[7] not in {
            f"{index}/{SHARD_COUNT}" for index in range(SHARD_COUNT)
        }
    ):
        raise RuntimeError("geng command does not match the frozen catalogue")
    geng_path = Path(str(command[0])).resolve()
    if geng_path.is_symlink() or not geng_path.is_file():
        raise RuntimeError("frozen geng path disappeared or became a symlink")

    with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as error_file:
        process = subprocess.Popen(
            [str(item) for item in command],
            stdout=subprocess.PIPE,
            stderr=error_file,
            text=True,
            bufsize=1,
            env=_catalogue_environment(geng_path),
        )
        if process.stdout is None:
            process.terminate()
            raise RuntimeError("failed to open geng output")
        completed_normally = False
        try:
            for raw_line in process.stdout:
                record = raw_line.strip()
                if not record or record.startswith(">"):
                    raise RuntimeError(
                        "geng emitted an unexpected non-graph6 output line"
                    )
                yield record
            return_code = process.wait()
            error_file.seek(0)
            stderr = error_file.read()
            completed_normally = True
            if return_code != 0 or stderr.strip():
                raise RuntimeError(
                    f"geng catalogue failed ({return_code}): {stderr.strip()}"
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


def _validate_catalogue_graph(graph: EdgeGraph, config: Degree2CriticalSearchConfig) -> None:
    if graph.vertex_count != ORDER:
        raise RuntimeError(
            f"catalogue emitted order {graph.vertex_count}, expected {ORDER}"
        )
    if len(graph.edges) != EDGE_COUNT:
        raise RuntimeError(
            f"catalogue emitted {len(graph.edges)} edges, expected {EDGE_COUNT}"
        )
    degrees = graph.degrees
    if min(degrees, default=0) < 2 or max(degrees, default=0) > 5:
        raise RuntimeError("catalogue graph violates the frozen -d2/-D5 bounds")


NO_DEGREE2_CLASS = "no_degree2_external_delta3_strata"
SUPPRESSIBLE_CLASS = "suppressible_nonadjacent_degree2"
COMMON_MISSING_CLASS = "common_missing_triangle_degree2"
RESIDUAL_CLASS = "degree2_critical_residual"
PARTITION_CLASSES = frozenset(
    (
        NO_DEGREE2_CLASS,
        SUPPRESSIBLE_CLASS,
        COMMON_MISSING_CLASS,
        RESIDUAL_CLASS,
    )
)


def _adjacency_sets(graph: EdgeGraph) -> tuple[frozenset[int], ...]:
    rows: list[set[int]] = [set() for _ in range(graph.vertex_count)]
    for left, right in graph.edges:
        rows[left].add(right)
        rows[right].add(left)
    return tuple(frozenset(row) for row in rows)


def degree2_partition_class(graph: EdgeGraph) -> str:
    """Return the exact mutually exclusive degree-two reduction class."""

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
            raise RuntimeError("degree-two adjacency reconstruction failed")
        if neighbours[1] not in adjacency[neighbours[0]]:
            return SUPPRESSIBLE_CLASS
    for vertex in degree2_vertices:
        neighbours = tuple(sorted(adjacency[vertex]))
        if any(degrees[neighbour] != MAXIMUM_DEGREE for neighbour in neighbours):
            return COMMON_MISSING_CLASS
    return RESIDUAL_CLASS


def _degree2_local_profiles(graph: EdgeGraph) -> list[dict[str, object]]:
    degrees = graph.degrees
    adjacency = _adjacency_sets(graph)
    return [
        {
            "vertex": vertex,
            "neighbours": list(sorted(adjacency[vertex])),
            "neighbour_degrees": [
                degrees[neighbour] for neighbour in sorted(adjacency[vertex])
            ],
            "neighbours_adjacent": (
                tuple(sorted(adjacency[vertex]))[1]
                in adjacency[tuple(sorted(adjacency[vertex]))[0]]
            ),
        }
        for vertex, degree in enumerate(degrees)
        if degree == 2
    ]


def _graph_fields(graph: EdgeGraph) -> dict[str, object]:
    return {
        "graph6": graph.encoding,
        "vertices": graph.vertex_count,
        "edge_count": len(graph.edges),
        "edges": [list(edge) for edge in graph.edges],
        "degrees": list(graph.degrees),
    }


def _base_event(
    graph: EdgeGraph,
    index: int,
    identity_sha256: str,
) -> dict[str, object]:
    return {
        "event_schema": EVENT_SCHEMA,
        "identity_sha256": identity_sha256,
        "time_unix": time.time(),
        "problem": "opg145",
        "order": ORDER,
        "index": index,
        **_graph_fields(graph),
    }


def _filtered_event(
    graph: EdgeGraph,
    index: int,
    identity_sha256: str,
    partition_class: str,
) -> dict[str, object]:
    if partition_class not in (
        NO_DEGREE2_CLASS,
        SUPPRESSIBLE_CLASS,
        COMMON_MISSING_CLASS,
    ):
        raise ValueError("filtered event received a residual graph")
    is_external = partition_class == NO_DEGREE2_CLASS
    event = _base_event(graph, index, identity_sha256)
    event.update(
        {
            "partition_class": partition_class,
            "filter_reason": partition_class,
            "positive_basis": (
                "external_disjoint_campaigns"
                if is_external
                else (
                    "degree2_suppression_extension_lemma"
                    if partition_class == SUPPRESSIBLE_CLASS
                    else "degree2_common_missing_extension_lemma"
                )
            ),
            "mathematical_positive_claimed": not is_external,
            "degree2_local_profiles": _degree2_local_profiles(graph),
            "eligible": False,
            "status": (
                "partition_filtered" if is_external else "theorem_filtered"
            ),
            "verified_coloring": None,
        }
    )
    return event


def _solver_event(
    graph: EdgeGraph,
    index: int,
    identity_sha256: str,
    result: SolverResult,
    cnf: CNF,
    coloring: tuple[int, ...] | None,
    cuts: int,
    cut_records: tuple[dict[str, object], ...],
) -> dict[str, object]:
    if result.status not in _SOLVER_STATUSES:
        raise RuntimeError(f"unexpected solver status: {result.status}")
    if cuts != len(cut_records):
        raise RuntimeError("lazy-cycle cut count does not match its records")
    certificate = coloring_search._semantic_certificate(
        "opg145", graph, cnf, cut_records
    )
    if (
        certificate is None
        or certificate.get("records_semantically_valid") is not True
        or certificate.get("independently_replayed") is not True
    ):
        raise RuntimeError("the lazy-cycle CNF failed semantic replay")
    if result.status == "sat":
        if coloring is None:
            raise RuntimeError("SAT result has no coloring witness")
        if any(
            type(color) is not int or not 0 <= color < COLOR_COUNT
            for color in coloring
        ):
            raise RuntimeError("SAT coloring uses an invalid color")
        if not coloring_search.verify_acyclic_edge_coloring(graph, coloring):
            raise RuntimeError("SAT coloring failed the acyclic verifier")
    elif coloring is not None:
        raise RuntimeError("non-SAT solver result unexpectedly has a coloring")

    event = _base_event(graph, index, identity_sha256)
    event.update(
        {
            "partition_class": RESIDUAL_CLASS,
            "filter_reason": None,
            "positive_basis": "solver_verified_witness",
            "mathematical_positive_claimed": result.status == "sat",
            "degree2_local_profiles": _degree2_local_profiles(graph),
            "eligible": True,
            "status": result.status,
            "elapsed_seconds": result.elapsed_seconds,
            "variables": cnf.variable_count,
            "clauses": len(cnf.clauses),
            "cnf_sha256": _text_sha256(cnf.dimacs()),
            "lazy_cycle_cuts": cuts,
            "lazy_cycle_records_sha256": _json_sha256(list(cut_records)),
            # A SAT coloring is itself a compact, directly checkable
            # certificate.  Preserve the much larger cut transcript only for
            # a terminal non-SAT result that needs forensic solver review.
            "lazy_cycle_certificate": (
                certificate if result.status != "sat" else None
            ),
            "verified_coloring": (
                list(coloring) if coloring is not None else None
            ),
            "solver_stdout_sha256": _text_sha256(result.stdout),
            "solver_stderr_sha256": _text_sha256(result.stderr),
        }
    )
    return event


def _empty_counts() -> dict[str, int]:
    return {key: 0 for key in _COUNTER_KEYS}


def _accumulate_event(counts: dict[str, int], event: Mapping[str, object]) -> None:
    counts["generated"] += 1
    status = event["status"]
    partition_class = event.get("partition_class")
    if status == "partition_filtered":
        if partition_class != NO_DEGREE2_CLASS:
            raise ValueError("partition-filtered event has the wrong class")
        counts["filtered_no_degree2"] += 1
        return
    if status == "theorem_filtered":
        if partition_class == SUPPRESSIBLE_CLASS:
            counts["filtered_suppressible"] += 1
        elif partition_class == COMMON_MISSING_CLASS:
            counts["filtered_common_missing"] += 1
        else:
            raise ValueError("theorem-filtered event has the wrong class")
        return
    if partition_class != RESIDUAL_CLASS:
        raise ValueError("solver event is not in the critical residual")
    counts["eligible"] += 1
    if status == "sat":
        counts["sat"] += 1
    elif status == "unsat":
        counts["unsat"] += 1
    elif status == "timeout":
        counts["timeouts"] += 1
    elif status == "unknown":
        counts["unknown"] += 1
    else:
        raise ValueError(f"invalid event status: {status}")


def _validate_solver_certificate(
    event: Mapping[str, object], graph: EdgeGraph
) -> None:
    certificate = event.get("lazy_cycle_certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("solver event has no lazy-cycle certificate")
    raw_records = certificate.get("records")
    if not isinstance(raw_records, list):
        raise ValueError("solver event has no lazy-cycle records")
    records = tuple(raw_records)
    replayed = coloring_search.proper_edge_coloring_cnf(graph, COLOR_COUNT)
    for record in records:
        if not isinstance(record, Mapping):
            raise ValueError("invalid lazy-cycle record")
        clause = record.get("clause")
        if not isinstance(clause, list):
            raise ValueError("lazy-cycle record has no clause")
        replayed.add(*(int(literal) for literal in clause))
    expected = coloring_search._semantic_certificate(
        "opg145", graph, replayed, records  # type: ignore[arg-type]
    )
    if expected != certificate:
        raise ValueError("persisted lazy-cycle certificate failed exact replay")
    if event.get("lazy_cycle_cuts") != len(records):
        raise ValueError("persisted lazy-cycle count is inconsistent")
    if event.get("variables") != replayed.variable_count:
        raise ValueError("persisted CNF variable count is inconsistent")
    if event.get("clauses") != len(replayed.clauses):
        raise ValueError("persisted CNF clause count is inconsistent")
    if event.get("cnf_sha256") != _text_sha256(replayed.dimacs()):
        raise ValueError("persisted CNF digest is inconsistent")
    if event.get("lazy_cycle_records_sha256") != _json_sha256(list(records)):
        raise ValueError("persisted lazy-cycle record digest is inconsistent")


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _validate_sat_solver_metadata(
    event: Mapping[str, object], graph: EdgeGraph
) -> None:
    cuts = event.get("lazy_cycle_cuts")
    variables = event.get("variables")
    clauses = event.get("clauses")
    if (
        type(cuts) is not int
        or cuts < 0
        or type(variables) is not int
        or type(clauses) is not int
    ):
        raise ValueError("SAT event has invalid CNF accounting")
    base = coloring_search.proper_edge_coloring_cnf(graph, COLOR_COUNT)
    if variables != base.variable_count or clauses != len(base.clauses) + cuts:
        raise ValueError("SAT event CNF accounting is inconsistent")
    if event.get("lazy_cycle_certificate") is not None:
        raise ValueError("SAT event unexpectedly stores a bulky cut transcript")
    for key in (
        "cnf_sha256",
        "lazy_cycle_records_sha256",
        "solver_stdout_sha256",
        "solver_stderr_sha256",
    ):
        if not _is_sha256(event.get(key)):
            raise ValueError(f"SAT event has an invalid {key}")


def _validate_event(
    event: Mapping[str, object],
    expected_index: int,
    identity_sha256: str,
    config: Degree2CriticalSearchConfig,
) -> None:
    if event.get("event_schema") != EVENT_SCHEMA:
        raise ValueError(f"event {expected_index} has the wrong schema")
    if event.get("identity_sha256") != identity_sha256:
        raise ValueError(f"event {expected_index} belongs to another campaign")
    if type(event.get("index")) is not int or event["index"] != expected_index:
        raise ValueError(f"event sequence breaks at index {expected_index}")
    if event.get("problem") != "opg145" or event.get("order") != ORDER:
        raise ValueError(f"event {expected_index} has the wrong problem/order")
    encoding = event.get("graph6")
    if not isinstance(encoding, str):
        raise ValueError(f"event {expected_index} has no graph6 record")
    graph = coloring_search.decode_graph6(encoding)
    _validate_catalogue_graph(graph, config)
    expected_fields = _graph_fields(graph)
    if any(event.get(key) != value for key, value in expected_fields.items()):
        raise ValueError(f"event {expected_index} graph payload is inconsistent")
    partition_class = degree2_partition_class(graph)
    if event.get("partition_class") != partition_class:
        raise ValueError(
            f"event {expected_index} has a wrong partition decision"
        )
    if event.get("degree2_local_profiles") != _degree2_local_profiles(graph):
        raise ValueError(
            f"event {expected_index} has wrong degree-two local profiles"
        )
    status = event.get("status")
    if partition_class != RESIDUAL_CLASS:
        is_external = partition_class == NO_DEGREE2_CLASS
        expected_basis = (
            "external_disjoint_campaigns"
            if is_external
            else (
                "degree2_suppression_extension_lemma"
                if partition_class == SUPPRESSIBLE_CLASS
                else "degree2_common_missing_extension_lemma"
            )
        )
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
            raise ValueError(f"event {expected_index} has a wrong filtered result")
        return
    if (
        status not in _SOLVER_STATUSES
        or event.get("filter_reason") is not None
        or event.get("positive_basis") != "solver_verified_witness"
        or event.get("mathematical_positive_claimed") is not (status == "sat")
        or event.get("eligible") is not True
    ):
        raise ValueError(f"event {expected_index} has an invalid solver result")
    elapsed = event.get("elapsed_seconds")
    if (
        not isinstance(elapsed, (int, float))
        or isinstance(elapsed, bool)
        or not math.isfinite(float(elapsed))
        or float(elapsed) < 0
    ):
        raise ValueError(f"event {expected_index} has invalid solver timing")
    witness = event.get("verified_coloring")
    if status == "sat":
        _validate_sat_solver_metadata(event, graph)
        if (
            not isinstance(witness, list)
            or not coloring_search.verify_acyclic_edge_coloring(graph, witness)
            or any(
                type(color) is not int or not 0 <= color < COLOR_COUNT
                for color in witness
            )
        ):
            raise ValueError(f"event {expected_index} has an invalid SAT witness")
    else:
        _validate_solver_certificate(event, graph)
        if witness is not None:
            raise ValueError(
                f"event {expected_index} has a witness for a non-SAT result"
            )


def _load_events(
    path: Path,
    identity_sha256: str,
    config: Degree2CriticalSearchConfig,
) -> tuple[list[dict[str, object]], dict[str, int]]:
    events: list[dict[str, object]] = []
    counts = _empty_counts()
    if not path.exists():
        return events, counts
    with path.open(encoding="utf-8") as handle:
        for index, raw_line in enumerate(handle):
            if not raw_line.endswith("\n") or not raw_line.strip():
                raise ValueError(f"events log is truncated at line {index + 1}")
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"events log has invalid JSON at line {index + 1}"
                ) from error
            if not isinstance(event, dict):
                raise ValueError(f"event {index} is not an object")
            _validate_event(event, index, identity_sha256, config)
            if events and events[-1]["status"] in _TERMINAL_EVENT_STATUSES:
                raise ValueError("events occur after a terminal solver result")
            events.append(
                {
                    "graph6": event["graph6"],
                    "status": event["status"],
                    "partition_class": event["partition_class"],
                }
            )
            _accumulate_event(counts, event)
    return events, counts


def _state_counts(state: Mapping[str, object]) -> dict[str, int]:
    result: dict[str, int] = {}
    for key in _COUNTER_KEYS:
        value = state.get(key)
        if type(value) is not int or value < 0:
            raise ValueError(f"checkpoint counter {key} is invalid")
        result[key] = value
    return result


def _counts_for_prefix(
    events: Sequence[Mapping[str, object]], length: int
) -> dict[str, int]:
    counts = _empty_counts()
    for event in events[:length]:
        _accumulate_event(counts, event)
    return counts


def _terminal_status_for_event(status: object) -> str:
    return {
        "unsat": "stopped_unsat",
        "timeout": "stopped_timeout",
        "unknown": "stopped_unknown",
    }[str(status)]


def _new_state(
    identity: Mapping[str, object], identity_sha256: str
) -> dict[str, object]:
    return {
        "checkpoint_schema": CHECKPOINT_SCHEMA,
        "identity": identity,
        "identity_sha256": identity_sha256,
        "status": "running",
        "next_index": 0,
        **_empty_counts(),
        "launch_history": [],
    }


def _load_or_create_state(
    state_path: Path,
    events_path: Path,
    identity: Mapping[str, object],
    identity_sha256: str,
    config: Degree2CriticalSearchConfig,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    if not state_path.exists():
        if events_path.exists():
            raise ValueError(
                "events exist without a checkpoint; use a fresh output directory"
            )
        state = _new_state(identity, identity_sha256)
        _atomic_json(state_path, state)
        return state, []

    loaded = json.loads(state_path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError("checkpoint is not a JSON object")
    if loaded.get("checkpoint_schema") != CHECKPOINT_SCHEMA:
        raise ValueError("checkpoint schema mismatch; use a fresh output directory")
    if (
        loaded.get("identity") != identity
        or loaded.get("identity_sha256") != identity_sha256
    ):
        raise ValueError("checkpoint does not match the full frozen search config")

    events, event_counts = _load_events(events_path, identity_sha256, config)
    next_index = loaded.get("next_index")
    if type(next_index) is not int or not 0 <= next_index <= len(events):
        raise ValueError("checkpoint is ahead of, or inconsistent with, its events")
    checkpoint_counts = _state_counts(loaded)
    if checkpoint_counts != _counts_for_prefix(events, next_index):
        raise ValueError("checkpoint counters do not match their event prefix")

    state = dict(loaded)
    state.update(event_counts)
    state["next_index"] = len(events)
    if events and events[-1]["status"] in _TERMINAL_EVENT_STATUSES:
        state["status"] = _terminal_status_for_event(events[-1]["status"])
    elif state.get("status") in (
        "stopped_unsat",
        "stopped_timeout",
        "stopped_unknown",
    ):
        raise ValueError("checkpoint claims a terminal result absent from events")
    if next_index != len(events):
        state["recovered_event_tail"] = len(events) - next_index
        _atomic_json(state_path, state)
    return state, events


def _pause(
    state: dict[str, object],
    state_path: Path,
    started: float,
) -> dict[str, object]:
    state["status"] = "paused_budget"
    state["elapsed_seconds_last_session"] = time.monotonic() - started
    _atomic_json(state_path, state)
    return state


def _checkpoint_event(
    state: dict[str, object],
    state_path: Path,
    events_path: Path,
    event: Mapping[str, object],
) -> None:
    _append_event(events_path, event)
    counts = _state_counts(state)
    _accumulate_event(counts, event)
    state.update(counts)
    state["next_index"] = int(event["index"]) + 1
    _atomic_json(state_path, state)


def _validate_terminal_state(
    state: Mapping[str, object],
    events: Sequence[Mapping[str, object]],
    events_path: Path,
    config: Degree2CriticalSearchConfig,
) -> None:
    status = state.get("status")
    counts = _state_counts(state)
    shard = config.shard_index
    expected_counts = {
        "generated": EXPECTED_GENERATED_BY_SHARD[shard],
        "filtered_no_degree2": EXPECTED_NO_DEGREE2_BY_SHARD[shard],
        "filtered_suppressible": EXPECTED_SUPPRESSIBLE_BY_SHARD[shard],
        "filtered_common_missing": (
            EXPECTED_COMMON_MISSING_BY_SHARD[shard]
        ),
        "eligible": EXPECTED_RESIDUAL_BY_SHARD[shard],
        "sat": EXPECTED_RESIDUAL_BY_SHARD[shard],
        "unsat": 0,
        "timeouts": 0,
        "unknown": 0,
    }
    if status == "complete":
        if (
            len(events) != config.expected_generated
            or counts != expected_counts
            or state.get("catalogue_exhausted") is not True
            or not events_path.is_file()
            or state.get("events_sha256")
            != coloring_search.file_sha256(events_path)
        ):
            raise ValueError("completed checkpoint fails closure verification")
        return
    if status == "denominator_mismatch":
        if (
            state.get("observed_generated_at_exhaustion") != len(events)
            or len(events) == config.expected_generated
        ):
            raise ValueError("denominator-mismatch checkpoint is inconsistent")
        return
    if status == "classification_denominator_mismatch":
        if (
            state.get("expected_complete_counts") == counts
            or state.get("observed_complete_counts") != counts
            or len(events) != config.expected_generated
        ):
            raise ValueError(
                "classification-mismatch checkpoint is inconsistent"
            )
        return
    expected_event_status = {
        "stopped_unsat": "unsat",
        "stopped_timeout": "timeout",
        "stopped_unknown": "unknown",
    }.get(str(status))
    if (
        expected_event_status is None
        or not events
        or events[-1].get("status") != expected_event_status
    ):
        raise ValueError("terminal checkpoint is inconsistent with its last event")


def run_degree2_critical_search(
    config: Degree2CriticalSearchConfig,
    *,
    wall_seconds: float,
    output: Path,
    max_cases: int = 0,
) -> dict[str, object]:
    """Search one exact shard and return its durable checkpoint."""

    config.validate()
    if not math.isfinite(wall_seconds) or wall_seconds <= 0:
        raise ValueError("wall_seconds must be finite and positive")
    if max_cases < 0:
        raise ValueError("max_cases cannot be negative")
    identity = build_identity(config)
    identity_sha256 = _json_sha256(identity)
    output = output.resolve()

    with _exclusive_output_lock(output):
        state_path = output / "state.json"
        events_path = output / "events.jsonl"
        state, prior_events = _load_or_create_state(
            state_path,
            events_path,
            identity,
            identity_sha256,
            config,
        )
        if state.get("status") in _TERMINAL_RUN_STATUSES:
            _validate_terminal_state(
                state, prior_events, events_path, config
            )
            return state

        launch_history = state.get("launch_history")
        if not isinstance(launch_history, list):
            raise ValueError("checkpoint launch history is invalid")
        launch_history.append(
            {
                "time_unix": time.time(),
                "wall_seconds": wall_seconds,
                "max_cases": max_cases,
            }
        )
        state["status"] = "running"
        _atomic_json(state_path, state)

        started = time.monotonic()
        deadline = started + wall_seconds
        processed_this_session = 0
        resume_index = len(prior_events)
        observed = 0
        command = identity["catalogue_command"]
        assert isinstance(command, list)
        records = _iter_catalogue_records([str(item) for item in command])
        try:
            for index, record in enumerate(records):
                observed = index + 1
                graph = coloring_search.decode_graph6(record)
                _validate_catalogue_graph(graph, config)
                if index < resume_index:
                    if graph.encoding != prior_events[index]["graph6"]:
                        raise RuntimeError(
                            f"catalogue drift at resumed index {index}"
                        )
                    if time.monotonic() >= deadline:
                        return _pause(state, state_path, started)
                    continue
                if time.monotonic() >= deadline or (
                    max_cases and processed_this_session >= max_cases
                ):
                    return _pause(state, state_path, started)

                partition_class = degree2_partition_class(graph)
                if partition_class != RESIDUAL_CLASS:
                    event = _filtered_event(
                        graph,
                        index,
                        identity_sha256,
                        partition_class,
                    )
                else:
                    result, cnf, witness, cuts, cut_records = (
                        coloring_search.evaluate_coloring_instance(
                            "opg145",
                            graph,
                            config.per_instance_seconds,
                        )
                    )
                    event = _solver_event(
                        graph,
                        index,
                        identity_sha256,
                        result,
                        cnf,
                        witness,
                        cuts,
                        cut_records,
                    )
                _checkpoint_event(state, state_path, events_path, event)
                processed_this_session += 1
                if event["status"] in _TERMINAL_EVENT_STATUSES:
                    state["status"] = _terminal_status_for_event(event["status"])
                    state["terminal_graph"] = _graph_fields(graph)
                    state["elapsed_seconds_last_session"] = (
                        time.monotonic() - started
                    )
                    _atomic_json(state_path, state)
                    return state
        finally:
            close = getattr(records, "close", None)
            if close is not None:
                close()

        if observed < resume_index:
            raise RuntimeError(
                "catalogue ended before the persisted resume position"
            )
        if observed != config.expected_generated:
            state["status"] = "denominator_mismatch"
            state["observed_generated_at_exhaustion"] = observed
            state["elapsed_seconds_last_session"] = time.monotonic() - started
            _atomic_json(state_path, state)
            return state
        counts = _state_counts(state)
        if counts["generated"] != observed:
            raise RuntimeError("event coverage does not equal the exhausted catalogue")
        shard = config.shard_index
        expected_counts = {
            "generated": EXPECTED_GENERATED_BY_SHARD[shard],
            "filtered_no_degree2": EXPECTED_NO_DEGREE2_BY_SHARD[shard],
            "filtered_suppressible": EXPECTED_SUPPRESSIBLE_BY_SHARD[shard],
            "filtered_common_missing": (
                EXPECTED_COMMON_MISSING_BY_SHARD[shard]
            ),
            "eligible": EXPECTED_RESIDUAL_BY_SHARD[shard],
            "sat": EXPECTED_RESIDUAL_BY_SHARD[shard],
            "unsat": 0,
            "timeouts": 0,
            "unknown": 0,
        }
        if (
            counts != expected_counts
        ):
            state["status"] = "classification_denominator_mismatch"
            state["expected_complete_counts"] = expected_counts
            state["observed_complete_counts"] = counts
            state["elapsed_seconds_last_session"] = (
                time.monotonic() - started
            )
            _atomic_json(state_path, state)
            return state
        state["status"] = "complete"
        state["catalogue_exhausted"] = True
        state["events_sha256"] = coloring_search.file_sha256(events_path)
        state["elapsed_seconds_last_session"] = time.monotonic() - started
        _atomic_json(state_path, state)
        return state


def parse_shard(value: str) -> int:
    try:
        left_text, right_text = value.split("/", 1)
        left, right = int(left_text), int(right_text)
    except (AttributeError, TypeError, ValueError) as error:
        raise argparse.ArgumentTypeError("shard must have form i/16") from error
    if (
        right != SHARD_COUNT
        or not 0 <= left < SHARD_COUNT
        or value != f"{left}/{right}"
    ):
        raise argparse.ArgumentTypeError(
            "shard must have canonical form i/16 with 0<=i<16"
        )
    return left


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Exact resumable OPG-145 n=11 degree-2 critical search; only an "
            "exhausted catalogue with zero timeout/UNSAT/unknown is complete."
        )
    )
    parser.add_argument("--shard", type=parse_shard, required=True)
    parser.add_argument("--per-instance-seconds", type=float, default=300.0)
    parser.add_argument("--wall-seconds", type=float, required=True)
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        config = config_for_shard(
            arguments.shard,
            arguments.per_instance_seconds,
        )
        result = run_degree2_critical_search(
            config,
            wall_seconds=arguments.wall_seconds,
            output=arguments.output,
            max_cases=arguments.max_cases,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] in ("complete", "paused_budget") else 2


if __name__ == "__main__":
    raise SystemExit(main())
