"""Independent fail-closed audit of the four OPG-145 n=11 dense shards.

The auditor is deliberately read-only and does not import the search runner or
its graph/coloring helpers.  It replays the frozen ``geng`` catalogue, decodes
graph6 independently, and verifies every persisted seven-color witness with a
separate union-find implementation.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
import time
from typing import BinaryIO, Iterator, Mapping, Sequence


AUDIT_SCHEMA = "amra.opg145.n11-dense.audit.v1"
CHECKPOINT_SCHEMA = "amra.opg145.n11-dense.checkpoint.v1"
EVENT_SCHEMA = "amra.opg145.n11-dense.event.v1"
ORDER = 11
COLOR_COUNT = 7
MINIMUM_EDGES = 25
MAXIMUM_EDGES = 27
SHARD_COUNT = 4
EXPECTED_BY_SHARD: dict[int, int] = {
    0: 88_595,
    1: 100_734,
    2: 80_076,
    3: 114_717,
}
EXPECTED_TOTAL = 384_122
COUNTER_KEYS = (
    "generated",
    "filtered_three_sparse",
    "eligible",
    "sat",
    "unsat",
    "timeouts",
    "unknown",
)
TOOL_NAMES = frozenset(("geng", "minisat", "cadical", "drat-trim"))
DISCOVERY_DIRECTORY = Path(__file__).resolve().parent
EXPECTED_IMPLEMENTATION_PATHS = (
    DISCOVERY_DIRECTORY / "opg145_dense_search.py",
    DISCOVERY_DIRECTORY / "opg_coloring_search.py",
)


class DenseRunAuditError(ValueError):
    """Raised whenever a shard cannot be certified exactly."""


@dataclass(frozen=True)
class AuditGraph:
    vertex_count: int
    edges: tuple[tuple[int, int], ...]
    graph6: str

    @property
    def degrees(self) -> tuple[int, ...]:
        values = [0] * self.vertex_count
        for left, right in self.edges:
            values[left] += 1
            values[right] += 1
        return tuple(values)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _stable_json_object(path: Path) -> dict[str, object]:
    if path.is_symlink() or not path.is_file():
        raise DenseRunAuditError(f"missing or redirected file: {path}")
    with path.open("rb") as handle:
        before = os.fstat(handle.fileno())
        payload = handle.read()
        after = os.fstat(handle.fileno())
    metadata_before = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )
    metadata_after = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    )
    if metadata_before != metadata_after:
        raise DenseRunAuditError(f"file changed while being read: {path}")
    if not payload.endswith(b"\n"):
        raise DenseRunAuditError(f"truncated JSON file: {path}")
    try:
        decoded = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DenseRunAuditError(f"invalid JSON file: {path}") from error
    if not isinstance(decoded, dict):
        raise DenseRunAuditError(f"JSON root is not an object: {path}")
    return decoded


def decode_graph6_independently(record: str) -> AuditGraph:
    """Decode compact graph6 without using the search implementation."""

    value = record.strip()
    if not value or value != record or value.startswith(">>graph6<<"):
        raise DenseRunAuditError("graph6 record is empty, wrapped, or noncanonical")
    if value[0] == "~":
        raise DenseRunAuditError("extended graph6 orders are outside this campaign")
    order = ord(value[0]) - 63
    if not 0 <= order <= 62:
        raise DenseRunAuditError("invalid compact graph6 order")
    required_bits = order * (order - 1) // 2
    required_characters = (required_bits + 5) // 6
    if len(value) != 1 + required_characters:
        raise DenseRunAuditError("graph6 payload has the wrong length")
    bits: list[int] = []
    for character in value[1:]:
        encoded = ord(character) - 63
        if not 0 <= encoded < 64:
            raise DenseRunAuditError("graph6 contains an invalid character")
        bits.extend(
            (encoded >> shift) & 1 for shift in range(5, -1, -1)
        )
    if any(bits[required_bits:]):
        raise DenseRunAuditError("graph6 has nonzero padding")
    possible_edges = (
        (left, right)
        for right in range(1, order)
        for left in range(right)
    )
    edges = tuple(
        edge
        for bit, edge in zip(bits[:required_bits], possible_edges)
        if bit
    )
    return AuditGraph(order, edges, value)


def is_three_sparse_independently(graph: AuditGraph) -> bool:
    degrees = graph.degrees
    return all(
        min(degrees[left], degrees[right]) <= 3
        for left, right in graph.edges
    )


def verify_acyclic_seven_edge_coloring_independently(
    graph: AuditGraph, coloring: object
) -> bool:
    """Verify properness and every two-color forest using union-find."""

    if not isinstance(coloring, list) or len(coloring) != len(graph.edges):
        return False
    if any(
        type(color) is not int or not 0 <= color < COLOR_COUNT
        for color in coloring
    ):
        return False

    incident_colors = [set() for _ in range(graph.vertex_count)]
    for edge_index, (left, right) in enumerate(graph.edges):
        color = coloring[edge_index]
        if (
            color in incident_colors[left]
            or color in incident_colors[right]
        ):
            return False
        incident_colors[left].add(color)
        incident_colors[right].add(color)

    for first in range(COLOR_COUNT):
        for second in range(first + 1, COLOR_COUNT):
            parent = list(range(graph.vertex_count))
            rank = [0] * graph.vertex_count

            def find(vertex: int) -> int:
                while parent[vertex] != vertex:
                    parent[vertex] = parent[parent[vertex]]
                    vertex = parent[vertex]
                return vertex

            for edge_index, (left, right) in enumerate(graph.edges):
                if coloring[edge_index] not in (first, second):
                    continue
                left_root = find(left)
                right_root = find(right)
                if left_root == right_root:
                    return False
                if rank[left_root] < rank[right_root]:
                    left_root, right_root = right_root, left_root
                parent[right_root] = left_root
                if rank[left_root] == rank[right_root]:
                    rank[left_root] += 1
    return True


def _frozen_environment(tool_record: Mapping[str, object]) -> dict[str, str]:
    linkage = tool_record.get("dynamic_linkage")
    if not isinstance(linkage, Mapping):
        raise DenseRunAuditError("tool has no recorded dynamic linkage")
    dependencies = linkage.get("dependencies")
    if not isinstance(dependencies, Mapping):
        raise DenseRunAuditError("tool has no recorded dependency map")
    directories: list[str] = []
    for dependency_record in dependencies.values():
        if not isinstance(dependency_record, Mapping):
            raise DenseRunAuditError("malformed recorded dependency")
        directory = str(Path(str(dependency_record.get("path", ""))).parent)
        if directory not in directories:
            directories.append(directory)
    environment = dict(os.environ)
    for variable in ("LD_PRELOAD", "LD_AUDIT"):
        environment.pop(variable, None)
    environment["LD_LIBRARY_PATH"] = os.pathsep.join(directories)
    environment["LC_ALL"] = "C"
    return environment


def _current_dynamic_linkage(
    path: Path, environment: Mapping[str, str]
) -> dict[str, object]:
    process = subprocess.run(
        ["ldd", str(path)],
        capture_output=True,
        text=True,
        check=False,
        env=dict(environment),
    )
    dependencies: dict[str, dict[str, str]] = {}
    missing: list[str] = []
    for raw_line in process.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "=>" in line:
            soname, target = (
                part.strip() for part in line.split("=>", 1)
            )
            candidate = target.split("(", 1)[0].strip()
            if candidate == "not found":
                missing.append(soname)
                continue
        else:
            candidate = line.split("(", 1)[0].strip()
            soname = Path(candidate).name
        dependency = Path(candidate)
        if dependency.is_absolute() and dependency.is_file():
            dependencies[soname] = {
                "path": str(dependency),
                "sha256": _file_sha256(dependency),
            }
    return {
        "ldd_exit": process.returncode,
        "dependencies": dependencies,
        "missing": sorted(missing),
    }


def _verify_implementation(identity: Mapping[str, object]) -> str:
    implementation = identity.get("implementation")
    if not isinstance(implementation, Mapping):
        raise DenseRunAuditError("identity has no implementation record")
    raw_files = implementation.get("files")
    if not isinstance(raw_files, list) or len(raw_files) != len(
        EXPECTED_IMPLEMENTATION_PATHS
    ):
        raise DenseRunAuditError("implementation file set is incomplete")
    aggregate = hashlib.sha256()
    for raw_record, expected_path in zip(
        raw_files, EXPECTED_IMPLEMENTATION_PATHS
    ):
        if not isinstance(raw_record, Mapping):
            raise DenseRunAuditError("malformed implementation file record")
        expected = expected_path.resolve()
        if raw_record.get("path") != str(expected):
            raise DenseRunAuditError(
                f"implementation directory drift: {raw_record.get('path')}"
            )
        if not expected.is_file():
            raise DenseRunAuditError(f"implementation file disappeared: {expected}")
        actual_sha = _file_sha256(expected)
        if raw_record.get("sha256") != actual_sha:
            raise DenseRunAuditError(
                f"implementation hash changed: {expected}"
            )
        aggregate.update(str(expected).encode("utf-8"))
        aggregate.update(actual_sha.encode("ascii"))
    aggregate_sha = aggregate.hexdigest()
    if implementation.get("aggregate_sha256") != aggregate_sha:
        raise DenseRunAuditError("implementation aggregate hash is inconsistent")
    return aggregate_sha


def _verify_toolchain(
    identity: Mapping[str, object],
) -> tuple[Mapping[str, object], str]:
    toolchain = identity.get("toolchain")
    if not isinstance(toolchain, Mapping) or set(toolchain) != TOOL_NAMES:
        raise DenseRunAuditError("frozen tool set is incomplete or has drifted")
    for name in sorted(TOOL_NAMES):
        raw_record = toolchain.get(name)
        if not isinstance(raw_record, Mapping):
            raise DenseRunAuditError(f"missing tool record: {name}")
        raw_path = raw_record.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            raise DenseRunAuditError(f"tool has no absolute path: {name}")
        path = Path(raw_path)
        if (
            not path.is_absolute()
            or not path.is_file()
            or str(path.resolve()) != raw_path
        ):
            raise DenseRunAuditError(f"tool path drift: {name}: {raw_path}")
        actual_sha = _file_sha256(path)
        if not _is_sha256(raw_record.get("sha256")):
            raise DenseRunAuditError(f"tool has an invalid hash: {name}")
        if raw_record.get("sha256") != actual_sha:
            raise DenseRunAuditError(f"tool hash changed: {name}")
        linkage = raw_record.get("dynamic_linkage")
        if not isinstance(linkage, Mapping):
            raise DenseRunAuditError(f"tool linkage is malformed: {name}")
        if linkage.get("missing") != []:
            raise DenseRunAuditError(f"tool had missing dependencies: {name}")
        dependencies = linkage.get("dependencies")
        if not isinstance(dependencies, Mapping):
            raise DenseRunAuditError(f"dependency map is missing: {name}")
        for soname, dependency_record in dependencies.items():
            if (
                not isinstance(soname, str)
                or not isinstance(dependency_record, Mapping)
            ):
                raise DenseRunAuditError(f"malformed dependency for {name}")
            dependency_path = Path(
                str(dependency_record.get("path", ""))
            )
            if not dependency_path.is_absolute() or not dependency_path.is_file():
                raise DenseRunAuditError(
                    f"dependency path drift: {name}: {soname}"
                )
            if (
                not _is_sha256(dependency_record.get("sha256"))
                or dependency_record.get("sha256")
                != _file_sha256(dependency_path)
            ):
                raise DenseRunAuditError(
                    f"dependency hash changed: {name}: {soname}"
                )
        environment = _frozen_environment(raw_record)
        if _current_dynamic_linkage(path, environment) != linkage:
            raise DenseRunAuditError(f"dynamic linkage drift: {name}")
    geng = toolchain["geng"]
    assert isinstance(geng, Mapping)
    return geng, _json_sha256(toolchain)


def _validate_identity(
    state: Mapping[str, object], expected_shard: int
) -> tuple[Mapping[str, object], Mapping[str, object], str, str]:
    if state.get("checkpoint_schema") != CHECKPOINT_SCHEMA:
        raise DenseRunAuditError("checkpoint schema is not the frozen dense schema")
    if state.get("status") != "complete":
        raise DenseRunAuditError("audit is allowed only after status=complete")
    identity = state.get("identity")
    if not isinstance(identity, Mapping):
        raise DenseRunAuditError("checkpoint has no identity object")
    identity_sha = _json_sha256(identity)
    if (
        state.get("identity_sha256") != identity_sha
        or not _is_sha256(identity_sha)
    ):
        raise DenseRunAuditError("checkpoint identity digest is inconsistent")
    expected_generated = EXPECTED_BY_SHARD[expected_shard]
    exact_fields: dict[str, object] = {
        "campaign": "opg145_n11_dense_edge_layer",
        "problem": "opg145",
        "order": ORDER,
        "edge_range": [MINIMUM_EDGES, MAXIMUM_EDGES],
        "shard": [expected_shard, SHARD_COUNT],
        "expected_generated": expected_generated,
        "color_count": COLOR_COUNT,
        "known_positive_filter": "is_three_sparse",
        "checkpoint_interval_records": 1,
        "event_policy": "one_fsynced_event_per_generated_record",
    }
    for field, expected in exact_fields.items():
        if identity.get(field) != expected:
            raise DenseRunAuditError(f"frozen identity field drift: {field}")
    per_instance = identity.get("per_instance_seconds")
    if (
        not isinstance(per_instance, (int, float))
        or isinstance(per_instance, bool)
        or not math.isfinite(float(per_instance))
        or float(per_instance) <= 0
    ):
        raise DenseRunAuditError("invalid per-instance solver budget")

    expected_manifest = {
        "method": "independent_geng_count_with_u",
        "count_command_canonical": [
            "geng",
            "-q",
            "-C",
            "-d2",
            "-D5",
            "-u",
            "11",
            "25:27",
            "i/4",
        ],
        "edge_range": [MINIMUM_EDGES, MAXIMUM_EDGES],
        "shard_count": SHARD_COUNT,
        "per_shard": {
            str(index): count
            for index, count in EXPECTED_BY_SHARD.items()
        },
        "total": EXPECTED_TOTAL,
    }
    if identity.get("expected_denominator_manifest") != expected_manifest:
        raise DenseRunAuditError("frozen denominator manifest has drifted")

    implementation_sha = _verify_implementation(identity)
    geng, toolchain_sha = _verify_toolchain(identity)
    geng_path = str(geng["path"])
    canonical_command = [
        "geng",
        "-q",
        "-C",
        "-d2",
        "-D5",
        "11",
        "25:27",
        f"{expected_shard}/4",
    ]
    actual_command = [geng_path, *canonical_command[1:]]
    if (
        identity.get("catalogue_command_canonical") != canonical_command
        or identity.get("catalogue_command") != actual_command
    ):
        raise DenseRunAuditError("catalogue command is not the exact frozen command")
    return identity, geng, implementation_sha, toolchain_sha


def _validate_closed_state(
    state: Mapping[str, object], expected_generated: int
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for key in COUNTER_KEYS:
        value = state.get(key)
        if type(value) is not int or value < 0:
            raise DenseRunAuditError(f"invalid checkpoint counter: {key}")
        counts[key] = value
    if (
        state.get("catalogue_exhausted") is not True
        or state.get("next_index") != expected_generated
        or counts["generated"] != expected_generated
        or counts["generated"]
        != counts["filtered_three_sparse"] + counts["eligible"]
        or counts["eligible"] != counts["sat"]
        or counts["unsat"] != 0
        or counts["timeouts"] != 0
        or counts["unknown"] != 0
    ):
        raise DenseRunAuditError("checkpoint accounting is not exactly closed")
    if not _is_sha256(state.get("events_sha256")):
        raise DenseRunAuditError("complete checkpoint has no valid events hash")
    return counts


def _iter_recorded_catalogue(
    identity: Mapping[str, object],
    geng: Mapping[str, object],
) -> Iterator[str]:
    command = identity["catalogue_command"]
    if not isinstance(command, list):
        raise DenseRunAuditError("catalogue command is malformed")
    with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as error_file:
        process = subprocess.Popen(
            [str(item) for item in command],
            stdout=subprocess.PIPE,
            stderr=error_file,
            text=True,
            bufsize=1,
            env=_frozen_environment(geng),
        )
        if process.stdout is None:
            process.terminate()
            raise DenseRunAuditError("could not open frozen geng output")
        completed_normally = False
        try:
            for raw_line in process.stdout:
                record = raw_line.strip()
                if not record or record.startswith(">"):
                    raise DenseRunAuditError(
                        "frozen geng emitted a non-graph6 line"
                    )
                yield record
            return_code = process.wait()
            error_file.seek(0)
            stderr = error_file.read()
            completed_normally = True
            if return_code != 0 or stderr.strip():
                raise DenseRunAuditError(
                    f"frozen geng failed ({return_code}): {stderr.strip()}"
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


def _validate_catalogue_graph(graph: AuditGraph) -> None:
    degrees = graph.degrees
    if (
        graph.vertex_count != ORDER
        or not MINIMUM_EDGES <= len(graph.edges) <= MAXIMUM_EDGES
        or min(degrees, default=0) < 2
        or max(degrees, default=0) > 5
    ):
        raise DenseRunAuditError("regenerated graph violates frozen constraints")


def _validate_graph_payload(
    event: Mapping[str, object], graph: AuditGraph, index: int
) -> None:
    expected_edges = [list(edge) for edge in graph.edges]
    if (
        event.get("graph6") != graph.graph6
        or event.get("vertices") != graph.vertex_count
        or event.get("edge_count") != len(graph.edges)
        or event.get("edges") != expected_edges
        or event.get("degrees") != list(graph.degrees)
    ):
        raise DenseRunAuditError(
            f"event {index} does not bind the complete graph payload"
        )


def _parse_event(raw_line: bytes, index: int) -> Mapping[str, object]:
    if not raw_line.endswith(b"\n") or not raw_line.strip():
        raise DenseRunAuditError(f"event {index} is truncated")
    try:
        event = json.loads(raw_line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DenseRunAuditError(f"event {index} is invalid JSON") from error
    if not isinstance(event, Mapping):
        raise DenseRunAuditError(f"event {index} is not an object")
    return event


def _validate_event(
    event: Mapping[str, object],
    regenerated_record: str,
    index: int,
    identity_sha: str,
) -> str:
    if (
        event.get("event_schema") != EVENT_SCHEMA
        or event.get("identity_sha256") != identity_sha
        or event.get("problem") != "opg145"
        or event.get("order") != ORDER
        or type(event.get("index")) is not int
        or event.get("index") != index
    ):
        raise DenseRunAuditError(f"event identity/index drift at {index}")
    event_record = event.get("graph6")
    if not isinstance(event_record, str):
        raise DenseRunAuditError(f"event {index} has no graph6")
    event_graph = decode_graph6_independently(event_record)
    regenerated_graph = decode_graph6_independently(regenerated_record)
    _validate_catalogue_graph(regenerated_graph)
    if (
        event_graph.graph6 != regenerated_graph.graph6
        or event_graph.edges != regenerated_graph.edges
    ):
        raise DenseRunAuditError(f"catalogue/event graph6 mismatch at {index}")
    _validate_graph_payload(event, event_graph, index)
    event_time = event.get("time_unix")
    if (
        not isinstance(event_time, (int, float))
        or isinstance(event_time, bool)
        or not math.isfinite(float(event_time))
    ):
        raise DenseRunAuditError(f"event {index} has invalid timing metadata")

    three_sparse = is_three_sparse_independently(event_graph)
    if event.get("three_sparse") is not three_sparse:
        raise DenseRunAuditError(f"wrong three-sparse decision at event {index}")
    status = event.get("status")
    if three_sparse:
        if (
            status != "filtered_three_sparse"
            or event.get("eligible") is not False
            or event.get("verified_coloring") is not None
        ):
            raise DenseRunAuditError(f"wrong filtered event semantics at {index}")
        return "filtered_three_sparse"
    elapsed = event.get("elapsed_seconds")
    cuts = event.get("lazy_cycle_cuts")
    variables = event.get("variables")
    clauses = event.get("clauses")
    base_clause_count = (
        len(event_graph.edges) * (1 + COLOR_COUNT * (COLOR_COUNT - 1) // 2)
        + sum(
            degree * (degree - 1) // 2 * COLOR_COUNT
            for degree in event_graph.degrees
        )
        + 1
    )
    if (
        status != "sat"
        or event.get("eligible") is not True
        or not isinstance(elapsed, (int, float))
        or isinstance(elapsed, bool)
        or not math.isfinite(float(elapsed))
        or float(elapsed) < 0
        or type(cuts) is not int
        or cuts < 0
        or variables != len(event_graph.edges) * COLOR_COUNT
        or clauses != base_clause_count + cuts
        or event.get("lazy_cycle_certificate") is not None
        or not _is_sha256(event.get("cnf_sha256"))
        or not _is_sha256(event.get("lazy_cycle_records_sha256"))
        or not _is_sha256(event.get("solver_stdout_sha256"))
        or not _is_sha256(event.get("solver_stderr_sha256"))
        or not verify_acyclic_seven_edge_coloring_independently(
            event_graph, event.get("verified_coloring")
        )
    ):
        raise DenseRunAuditError(
            f"event {index} is non-SAT or has an invalid witness"
        )
    return "sat"


def _open_verified_events(
    path: Path, expected_sha: str
) -> tuple[BinaryIO, tuple[int, int, int, int]]:
    if path.is_symlink() or not path.is_file():
        raise DenseRunAuditError(f"missing or redirected events file: {path}")
    handle = path.open("rb")
    before = os.fstat(handle.fileno())
    digest = hashlib.sha256()
    for block in iter(lambda: handle.read(1 << 20), b""):
        digest.update(block)
    if digest.hexdigest() != expected_sha:
        handle.close()
        raise DenseRunAuditError("events hash differs from the complete checkpoint")
    handle.seek(0)
    return handle, (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )


def audit_dense_shard(
    directory: Path, *, expected_shard: int
) -> dict[str, object]:
    """Certify one complete shard without mutating its directory."""

    if expected_shard not in EXPECTED_BY_SHARD:
        raise DenseRunAuditError("invalid expected shard")
    if (
        directory.is_symlink()
        or not directory.is_dir()
        or directory.name != f"shard-{expected_shard}"
    ):
        raise DenseRunAuditError("shard directory layout has drifted")
    state_path = directory / "state.json"
    events_path = directory / "events.jsonl"
    if (directory / "state.json.tmp").exists():
        raise DenseRunAuditError("unfinished checkpoint temporary file remains")
    state = _stable_json_object(state_path)
    identity, geng, implementation_sha, toolchain_sha = _validate_identity(
        state, expected_shard
    )
    expected_generated = EXPECTED_BY_SHARD[expected_shard]
    state_counts = _validate_closed_state(state, expected_generated)
    identity_sha = str(state["identity_sha256"])

    events, initial_metadata = _open_verified_events(
        events_path, str(state["events_sha256"])
    )
    event_digest = hashlib.sha256()
    observed_counts = {key: 0 for key in COUNTER_KEYS}
    observed_catalogue = 0
    records = _iter_recorded_catalogue(identity, geng)
    try:
        for index, regenerated_record in enumerate(records):
            if index >= expected_generated:
                raise DenseRunAuditError(
                    "regenerated catalogue exceeds its frozen denominator"
                )
            raw_line = events.readline()
            if not raw_line:
                raise DenseRunAuditError(f"missing event at index {index}")
            event_digest.update(raw_line)
            event = _parse_event(raw_line, index)
            status = _validate_event(
                event, regenerated_record, index, identity_sha
            )
            observed_catalogue += 1
            observed_counts["generated"] += 1
            if status == "filtered_three_sparse":
                observed_counts["filtered_three_sparse"] += 1
            else:
                observed_counts["eligible"] += 1
                observed_counts["sat"] += 1
        trailing = events.read()
        event_digest.update(trailing)
        if trailing:
            raise DenseRunAuditError("events remain after catalogue exhaustion")
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
        raise DenseRunAuditError("events changed during audit")
    if event_digest.hexdigest() != state["events_sha256"]:
        raise DenseRunAuditError("events changed between hash and replay")
    if observed_catalogue != expected_generated:
        raise DenseRunAuditError(
            "regenerated catalogue does not equal the frozen denominator"
        )
    if observed_counts != state_counts:
        raise DenseRunAuditError("state counters do not equal audited events")

    return {
        "audit_schema": AUDIT_SCHEMA,
        "status": "verified_complete",
        "directory": str(directory.resolve()),
        "shard": [expected_shard, SHARD_COUNT],
        "expected_generated": expected_generated,
        "audited_counts": observed_counts,
        "events_sha256": state["events_sha256"],
        "identity_sha256": identity_sha,
        "implementation_sha256": implementation_sha,
        "toolchain_sha256": toolchain_sha,
        "auditor_sha256": _file_sha256(Path(__file__).resolve()),
    }


def audit_dense_campaign(root: Path) -> dict[str, object]:
    """Certify the exact four-shard directory and aggregate denominator."""

    if root.is_symlink() or not root.is_dir():
        raise DenseRunAuditError("campaign root is missing or redirected")
    expected_names = {f"shard-{index}" for index in range(SHARD_COUNT)}
    actual_names = {entry.name for entry in root.iterdir()}
    if actual_names != expected_names:
        raise DenseRunAuditError("campaign shard directory set has drifted")
    reports = [
        audit_dense_shard(
            root / f"shard-{index}", expected_shard=index
        )
        for index in range(SHARD_COUNT)
    ]
    if (
        sum(int(report["expected_generated"]) for report in reports)
        != EXPECTED_TOTAL
    ):
        raise DenseRunAuditError("aggregate denominator does not close")
    if len({report["implementation_sha256"] for report in reports}) != 1:
        raise DenseRunAuditError("shards used different implementations")
    if len({report["toolchain_sha256"] for report in reports}) != 1:
        raise DenseRunAuditError("shards used different toolchains")
    return {
        "audit_schema": AUDIT_SCHEMA,
        "status": "verified_complete",
        "campaign_root": str(root.resolve()),
        "shard_count": SHARD_COUNT,
        "expected_total": EXPECTED_TOTAL,
        "audited_total": sum(
            int(report["audited_counts"]["generated"])  # type: ignore[index]
            for report in reports
        ),
        "auditor_sha256": _file_sha256(Path(__file__).resolve()),
        "shards": reports,
        "audited_at_unix": time.time(),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only independent auditor for a completed four-shard "
            "OPG-145 n=11, 25:27-edge dense campaign."
        )
    )
    parser.add_argument("campaign_root", type=Path)
    arguments = parser.parse_args(argv)
    try:
        report = audit_dense_campaign(arguments.campaign_root)
    except (DenseRunAuditError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
