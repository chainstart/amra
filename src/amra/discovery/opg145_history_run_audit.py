"""Independent audit of the archived OPG-145 orders 7--9 search.

This module intentionally does not import the historical search runner or the
newer n=10 auditor.  It regenerates the nauty catalogues with the exact binary
recorded by the legacy checkpoint, independently decodes graph6, recomputes the
theorem filter, binds every eligible catalogue row to one persisted event, and
checks each seven-colour witness with a union-find implementation.

The legacy checkpoint records the search implementation and geng binary hashes,
but not source snapshots or dynamic-library hashes.  The report preserves that
provenance boundary instead of pretending that the archived implementation is
identical to the current source tree.
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
from typing import Iterator, Mapping, Sequence


EXPECTED_ARCHIVED_IMPLEMENTATION_SHA256 = (
    "470e43d729c1db9bf518d7f6efc307ec38dd475ee4968c40ee8c53121a4371ce"
)
EXPECTED_GENERATED_BY_ORDER = {7: 356, 8: 3511, 9: 44920}
EXPECTED_ELIGIBLE_BY_ORDER = {7: 195, 8: 2615, 9: 39203}
EXPECTED_CATALOGUE_SHA256_BY_ORDER = {
    7: "eefb48e8d6f62ebb3a22dfc3633d67d103f955797445e5a01b36b853f3dc7bee",
    8: "53ac4992212f8032ce52949c17175fbf53b77ae3e34c0218b3de0be9820fb566",
    9: "a20ced5769d777af734c2983b3812c365f4836935e51280e5b0205556b078f34",
}
COLOR_COUNT = 7


class OPG145HistoryAuditError(ValueError):
    """Raised when the archived run fails a fail-closed audit check."""


class _DuplicateJSONKey(ValueError):
    """Internal signal used to reject ambiguous JSON objects."""


@dataclass(frozen=True)
class _SimpleGraph:
    order: int
    edges: tuple[tuple[int, int], ...]
    encoding: str

    @property
    def degrees(self) -> tuple[int, ...]:
        result = [0] * self.order
        for left, right in self.edges:
            result[left] += 1
            result[right] += 1
        return tuple(result)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _legacy_style_implementation_fingerprint(path: Path) -> str:
    """Reproduce the path-plus-file-hash convention used by the old runner."""

    resolved = path.resolve()
    digest = hashlib.sha256()
    digest.update(str(resolved).encode("utf-8"))
    digest.update(_file_sha256(resolved).encode("ascii"))
    return digest.hexdigest()


def _unique_json_object(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateJSONKey(key)
        result[key] = value
    return result


def _load_unique_json(raw: bytes, *, context: str) -> object:
    try:
        return json.loads(raw, object_pairs_hook=_unique_json_object)
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        _DuplicateJSONKey,
    ) as error:
        raise OPG145HistoryAuditError(
            f"{context} is not unambiguous valid JSON"
        ) from error


def _decode_graph6_independently(record: str) -> _SimpleGraph:
    value = record.strip()
    if value.startswith(">>graph6<<"):
        value = value[10:]
    if not value or value[0] == "~":
        raise OPG145HistoryAuditError(
            "unsupported or empty compact graph6 record"
        )
    order = ord(value[0]) - 63
    if not 0 <= order <= 62:
        raise OPG145HistoryAuditError("invalid compact graph6 order")
    bit_count = order * (order - 1) // 2
    character_count = (bit_count + 5) // 6
    if len(value) != character_count + 1:
        raise OPG145HistoryAuditError("graph6 payload length is invalid")

    bits: list[int] = []
    for character in value[1:]:
        encoded = ord(character) - 63
        if not 0 <= encoded < 64:
            raise OPG145HistoryAuditError(
                "graph6 contains an invalid character"
            )
        bits.extend(
            (encoded >> shift) & 1 for shift in range(5, -1, -1)
        )
    if any(bits[bit_count:]):
        raise OPG145HistoryAuditError("graph6 padding bits are nonzero")

    possible_edges = (
        (left, right)
        for right in range(1, order)
        for left in range(right)
    )
    edges = tuple(
        edge
        for bit, edge in zip(bits[:bit_count], possible_edges)
        if bit
    )
    return _SimpleGraph(order, edges, value)


def _is_biconnected(graph: _SimpleGraph) -> bool:
    """Check vertex biconnectivity without relying on a graph package."""

    if graph.order < 3:
        return False
    adjacency = [[] for _ in range(graph.order)]
    for left, right in graph.edges:
        adjacency[left].append(right)
        adjacency[right].append(left)

    for removed in range(graph.order):
        start = next(
            (vertex for vertex in range(graph.order) if vertex != removed),
            None,
        )
        if start is None:
            return False
        seen = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other != removed and other not in seen:
                    seen.add(other)
                    stack.append(other)
        if len(seen) != graph.order - 1:
            return False
    return True


def _validate_catalogue_class(graph: _SimpleGraph, order: int) -> None:
    if graph.order != order:
        raise OPG145HistoryAuditError(
            f"catalogue record has order {graph.order}, expected {order}"
        )
    degrees = graph.degrees
    if min(degrees, default=0) < 2:
        raise OPG145HistoryAuditError(
            f"order {order} catalogue record violates -d2"
        )
    if max(degrees, default=0) > 5:
        raise OPG145HistoryAuditError(
            f"order {order} catalogue record violates -D5"
        )
    if not _is_biconnected(graph):
        raise OPG145HistoryAuditError(
            f"order {order} catalogue record violates -C"
        )


def _is_eligible_delta_five_non_three_sparse(
    graph: _SimpleGraph,
) -> bool:
    degrees = graph.degrees
    return max(degrees, default=0) == 5 and any(
        degrees[left] >= 4 and degrees[right] >= 4
        for left, right in graph.edges
    )


def independently_verify_acyclic_seven_coloring(
    graph: _SimpleGraph,
    coloring: Sequence[int],
) -> bool:
    """Verify properness and that each two-colour subgraph is a forest."""

    if len(coloring) != len(graph.edges):
        return False
    if any(
        type(color) is not int or not 0 <= color < COLOR_COUNT
        for color in coloring
    ):
        return False

    incident_colors = [set() for _ in range(graph.order)]
    for edge_index, (left, right) in enumerate(graph.edges):
        color = coloring[edge_index]
        if (
            color in incident_colors[left]
            or color in incident_colors[right]
        ):
            return False
        incident_colors[left].add(color)
        incident_colors[right].add(color)

    used_colors = sorted(set(coloring))
    for first_index, first_color in enumerate(used_colors):
        for second_color in used_colors[first_index + 1 :]:
            parent = list(range(graph.order))
            rank = [0] * graph.order

            def find(vertex: int) -> int:
                while parent[vertex] != vertex:
                    parent[vertex] = parent[parent[vertex]]
                    vertex = parent[vertex]
                return vertex

            for edge_index, (left, right) in enumerate(graph.edges):
                if coloring[edge_index] not in (
                    first_color,
                    second_color,
                ):
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


def _nauty_environment(geng_path: Path) -> dict[str, str]:
    environment = dict(os.environ)
    prefix = geng_path.parent.parent
    candidates = (
        prefix / "lib",
        prefix / "lib" / "x86_64-linux-gnu",
    )
    library_directories = [
        str(candidate) for candidate in candidates if candidate.is_dir()
    ]
    previous = environment.get("LD_LIBRARY_PATH")
    if previous:
        library_directories.append(previous)
    if library_directories:
        environment["LD_LIBRARY_PATH"] = os.pathsep.join(
            library_directories
        )
    return environment


def _runtime_linkage_snapshot(
    geng_path: Path,
    environment: Mapping[str, str],
) -> dict[str, object]:
    process = subprocess.run(
        ["ldd", str(geng_path)],
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
        "captured_during_audit": True,
        "legacy_checkpoint_bound": False,
        "ldd_exit": process.returncode,
        "dependencies": dependencies,
        "missing": sorted(missing),
    }


def _recorded_geng(
    state: Mapping[str, object],
) -> tuple[Path, str, dict[str, str]]:
    toolchain = state.get("toolchain")
    if not isinstance(toolchain, Mapping):
        raise OPG145HistoryAuditError(
            "legacy state has no toolchain mapping"
        )
    record = toolchain.get("geng")
    if not isinstance(record, Mapping):
        raise OPG145HistoryAuditError(
            "legacy state has no geng tool record"
        )
    path = Path(str(record.get("path", "")))
    recorded_sha256 = str(record.get("sha256", ""))
    if not path.is_file():
        raise OPG145HistoryAuditError(
            "recorded geng executable is unavailable"
        )
    observed_sha256 = _file_sha256(path)
    if observed_sha256 != recorded_sha256:
        raise OPG145HistoryAuditError(
            "recorded geng executable hash changed"
        )
    if "dynamic_linkage" in record:
        raise OPG145HistoryAuditError(
            "legacy geng record unexpectedly changed schema"
        )
    environment = _nauty_environment(path)
    return path, recorded_sha256, environment


def _iter_geng_catalogue(
    geng_path: Path,
    *,
    order: int,
    environment: Mapping[str, str],
) -> Iterator[str]:
    command = [
        str(geng_path),
        "-q",
        "-C",
        "-d2",
        "-D5",
        str(order),
    ]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=dict(environment),
    )
    assert process.stdout is not None
    assert process.stderr is not None
    completed_normally = False
    try:
        for line in process.stdout:
            record = line.strip()
            if not record:
                raise OPG145HistoryAuditError(
                    "geng emitted an empty catalogue record"
                )
            yield record
        stderr = process.stderr.read()
        return_code = process.wait()
        completed_normally = True
        if return_code != 0 or stderr.strip():
            raise OPG145HistoryAuditError(
                "geng catalogue replay failed "
                f"({return_code}): {stderr.strip()}"
            )
    finally:
        process.stdout.close()
        process.stderr.close()
        if not completed_normally and process.poll() is None:
            process.terminate()
            process.wait(timeout=5)


def _strict_state_contract(state: Mapping[str, object]) -> None:
    expected = {
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
        "generated": sum(EXPECTED_GENERATED_BY_ORDER.values()),
        "eligible": sum(EXPECTED_ELIGIBLE_BY_ORDER.values()),
        "filtered_known_positive": sum(
            EXPECTED_GENERATED_BY_ORDER[order]
            - EXPECTED_ELIGIBLE_BY_ORDER[order]
            for order in EXPECTED_GENERATED_BY_ORDER
        ),
        "sat": sum(EXPECTED_ELIGIBLE_BY_ORDER.values()),
        "unsat": 0,
        "timeouts": 0,
        "hard_queue": [],
    }
    for key, value in expected.items():
        observed = state.get(key)
        if type(observed) is not type(value) or observed != value:
            raise OPG145HistoryAuditError(
                f"legacy state field {key!r} is "
                f"{observed!r}, expected {value!r}"
            )
    if "candidate" in state and state["candidate"] is not None:
        raise OPG145HistoryAuditError(
            "legacy state unexpectedly contains a candidate"
        )


def _read_event(
    events,
    *,
    order: int,
    index: int,
) -> tuple[bytes, Mapping[str, object]]:
    raw_line = events.readline()
    if not raw_line:
        raise OPG145HistoryAuditError(
            f"missing eligible event for order {order} index {index}"
        )
    event = _load_unique_json(
        raw_line,
        context=f"event for order {order} index {index}",
    )
    if not isinstance(event, Mapping):
        raise OPG145HistoryAuditError(
            f"event for order {order} index {index} is not an object"
        )
    return raw_line, event


def audit_opg145_history(directory: Path) -> dict[str, object]:
    """Audit the exact archived unsharded OPG-145 orders 7--9 run."""

    state_path = directory / "state.json"
    events_path = directory / "events.jsonl"
    if not state_path.is_file() or not events_path.is_file():
        raise OPG145HistoryAuditError(
            f"missing state/events in {directory}"
        )

    state_raw = state_path.read_bytes()
    state = _load_unique_json(state_raw, context="legacy state")
    if not isinstance(state, Mapping):
        raise OPG145HistoryAuditError(
            "legacy state root is not an object"
        )
    _strict_state_contract(state)

    geng_path, geng_sha256, environment = _recorded_geng(state)
    linkage = _runtime_linkage_snapshot(geng_path, environment)
    if linkage["ldd_exit"] != 0 or linkage["missing"]:
        raise OPG145HistoryAuditError(
            "runtime geng linkage is unresolved"
        )

    aggregate_catalogue_digest = hashlib.sha256()
    aggregate_event_digest = hashlib.sha256()
    per_order: dict[str, dict[str, object]] = {}
    total_generated = 0
    total_eligible = 0
    total_filtered = 0
    total_events = 0

    with events_path.open("rb") as events:
        for order in sorted(EXPECTED_GENERATED_BY_ORDER):
            catalogue_digest = hashlib.sha256()
            event_digest = hashlib.sha256()
            generated = 0
            eligible = 0
            filtered = 0
            event_count = 0
            maximum_elapsed = 0.0
            maximum_lazy_cuts = 0

            for index, record in enumerate(
                _iter_geng_catalogue(
                    geng_path,
                    order=order,
                    environment=environment,
                )
            ):
                generated += 1
                encoded_line = record.encode("ascii") + b"\n"
                catalogue_digest.update(encoded_line)
                aggregate_catalogue_digest.update(encoded_line)
                graph = _decode_graph6_independently(record)
                _validate_catalogue_class(graph, order)
                if not _is_eligible_delta_five_non_three_sparse(graph):
                    filtered += 1
                    continue

                eligible += 1
                raw_line, event = _read_event(
                    events,
                    order=order,
                    index=index,
                )
                event_count += 1
                event_digest.update(raw_line)
                aggregate_event_digest.update(raw_line)
                if (
                    event.get("problem") != "opg145"
                    or event.get("status") != "sat"
                    or type(event.get("order")) is not int
                    or event.get("order") != order
                    or type(event.get("index")) is not int
                    or event.get("index") != index
                    or event.get("encoding") != record
                    or type(event.get("vertices")) is not int
                    or event.get("vertices") != order
                    or type(event.get("edges")) is not int
                    or event.get("edges") != len(graph.edges)
                    or (
                        "retry" in event
                        and event["retry"] is not False
                    )
                ):
                    raise OPG145HistoryAuditError(
                        "catalogue/event binding failed for "
                        f"order {order} index {index}"
                    )
                coloring = event.get("verified_coloring")
                if not isinstance(coloring, list) or not (
                    independently_verify_acyclic_seven_coloring(
                        graph, coloring
                    )
                ):
                    raise OPG145HistoryAuditError(
                        "invalid acyclic seven-colour witness for "
                        f"order {order} index {index}"
                    )
                elapsed = event.get("elapsed_seconds", 0.0)
                lazy_cuts = event.get("lazy_cycle_cuts", 0)
                if (
                    type(elapsed) not in (int, float)
                    or not math.isfinite(float(elapsed))
                    or float(elapsed) < 0.0
                    or type(lazy_cuts) is not int
                    or lazy_cuts < 0
                ):
                    raise OPG145HistoryAuditError(
                        "invalid event telemetry for "
                        f"order {order} index {index}"
                    )
                maximum_elapsed = max(
                    maximum_elapsed, float(elapsed)
                )
                maximum_lazy_cuts = max(
                    maximum_lazy_cuts, lazy_cuts
                )

            expected_generated = EXPECTED_GENERATED_BY_ORDER[order]
            expected_eligible = EXPECTED_ELIGIBLE_BY_ORDER[order]
            expected_filtered = expected_generated - expected_eligible
            if generated != expected_generated:
                raise OPG145HistoryAuditError(
                    f"order {order} generated {generated}, "
                    f"expected {expected_generated}"
                )
            if eligible != expected_eligible:
                raise OPG145HistoryAuditError(
                    f"order {order} eligible {eligible}, "
                    f"expected {expected_eligible}"
                )
            if filtered != expected_filtered:
                raise OPG145HistoryAuditError(
                    f"order {order} filtered {filtered}, "
                    f"expected {expected_filtered}"
                )
            if event_count != eligible:
                raise OPG145HistoryAuditError(
                    f"order {order} replayed {event_count} events "
                    f"for {eligible} eligible records"
                )
            catalogue_sha256 = catalogue_digest.hexdigest()
            expected_catalogue_sha256 = (
                EXPECTED_CATALOGUE_SHA256_BY_ORDER[order]
            )
            if catalogue_sha256 != expected_catalogue_sha256:
                raise OPG145HistoryAuditError(
                    f"order {order} catalogue hash {catalogue_sha256}, "
                    f"expected {expected_catalogue_sha256}"
                )

            per_order[str(order)] = {
                "generated": generated,
                "eligible": eligible,
                "filtered_known_positive": filtered,
                "sat_witnesses_replayed": event_count,
                "catalogue_sha256": catalogue_sha256,
                "events_sha256": event_digest.hexdigest(),
                "maximum_elapsed_seconds": maximum_elapsed,
                "maximum_lazy_cycle_cuts": maximum_lazy_cuts,
                "status": "independently_verified",
            }
            total_generated += generated
            total_eligible += eligible
            total_filtered += filtered
            total_events += event_count

        if events.readline():
            raise OPG145HistoryAuditError(
                "events remain after all regenerated catalogues "
                "were exhausted"
            )

    if (
        total_generated != state["generated"]
        or total_eligible != state["eligible"]
        or total_filtered != state["filtered_known_positive"]
        or total_events != state["sat"]
        or total_generated != total_eligible + total_filtered
    ):
        raise OPG145HistoryAuditError(
            "replayed totals disagree with legacy checkpoint counters"
        )

    current_search_path = Path(__file__).with_name(
        "opg_coloring_search.py"
    )
    current_search_fingerprint = (
        _legacy_style_implementation_fingerprint(current_search_path)
        if current_search_path.is_file()
        else None
    )
    archived_fingerprint = str(state["implementation_sha256"])
    return {
        "schema_version": "amra.opg145.history-run-audit.v1",
        "status": "independently_verified_with_legacy_provenance_boundary",
        "directory": str(directory),
        "order_contract": [7, 9],
        "generator_command": [
            str(geng_path),
            "-q",
            "-C",
            "-d2",
            "-D5",
            "{order}",
        ],
        "catalogue_event_binding": "exact_order_index_and_graph6",
        "catalogue_class_recomputed": (
            "biconnected_simple_minimum_degree_at_least_2_"
            "maximum_degree_at_most_5"
        ),
        "eligibility_recomputed": (
            "maximum_degree_5_and_not_3_sparse"
        ),
        "witness_checker": (
            "independent_properness_and_two_colour_union_find"
        ),
        "files": {
            "state_sha256": hashlib.sha256(state_raw).hexdigest(),
            "events_sha256": _file_sha256(events_path),
        },
        "per_order": per_order,
        "totals": {
            "generated": total_generated,
            "eligible": total_eligible,
            "filtered_known_positive": total_filtered,
            "sat_witnesses_replayed": total_events,
            "catalogue_sha256": (
                aggregate_catalogue_digest.hexdigest()
            ),
            "bound_events_sha256": (
                aggregate_event_digest.hexdigest()
            ),
        },
        "legacy_provenance": {
            "archived_search_implementation_sha256": (
                archived_fingerprint
            ),
            "current_search_implementation_sha256": (
                current_search_fingerprint
            ),
            "archived_matches_current_search": (
                current_search_fingerprint == archived_fingerprint
            ),
            "archived_source_snapshot_available": False,
            "geng_path": str(geng_path),
            "recorded_geng_sha256": geng_sha256,
            "geng_binary_hash_reverified": True,
            "dynamic_linkage_recorded_by_legacy_checkpoint": False,
            "runtime_dynamic_linkage": linkage,
            "residual_boundary": (
                "The legacy checkpoint binds the geng executable but "
                "does not bind its dynamic libraries or preserve the "
                "archived search source.  The historical implementation "
                "hash is recorded without requiring equality to the "
                "current source; confidence instead comes from exact "
                "catalogue regeneration, event binding, and independent "
                "semantic witness replay."
            ),
        },
        "auditor_sha256": _file_sha256(Path(__file__)),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Independently audit the archived OPG-145 orders 7--9 run."
        )
    )
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(argv)
    payload = audit_opg145_history(arguments.directory)
    rendered = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    )
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = arguments.output.with_name(
            f".{arguments.output.name}.tmp-{os.getpid()}"
        )
        with temporary.open("w", encoding="utf-8") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, arguments.output)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
