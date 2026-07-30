"""Independent semantic audit for completed OPG colouring search shards.

The search code verifies each SAT assignment before writing it.  This module
deliberately repeats the mathematical check with a separate union-find
implementation and then closes the checkpoint/event accounting.  It does not
invoke, or trust, a SAT solver.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Iterator, Mapping, Sequence

import amra.discovery.opg_coloring_search as coloring_search
from amra.discovery.opg_coloring_search import EdgeGraph


class ColoringRunAuditError(ValueError):
    """Raised when a persisted shard fails an independent audit."""


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _search_implementation_fingerprint() -> str:
    path = Path(coloring_search.__file__).resolve()
    digest = hashlib.sha256()
    digest.update(str(path).encode("utf-8"))
    digest.update(_file_sha256(path).encode("ascii"))
    return digest.hexdigest()


def _decode_graph6_independently(record: str) -> EdgeGraph:
    value = record.strip()
    if value.startswith(">>graph6<<"):
        value = value[10:]
    if not value or value[0] == "~":
        raise ColoringRunAuditError("unsupported or empty compact graph6 record")
    order = ord(value[0]) - 63
    if not 0 <= order <= 62:
        raise ColoringRunAuditError("invalid compact graph6 order")
    required_bits = order * (order - 1) // 2
    required_characters = (required_bits + 5) // 6
    if len(value) != required_characters + 1:
        raise ColoringRunAuditError("graph6 payload length is invalid")
    bits: list[int] = []
    for character in value[1:]:
        encoded = ord(character) - 63
        if not 0 <= encoded < 64:
            raise ColoringRunAuditError("graph6 contains an invalid character")
        bits.extend(
            (encoded >> shift) & 1 for shift in range(5, -1, -1)
        )
    if any(bits[required_bits:]):
        raise ColoringRunAuditError("graph6 padding bits are nonzero")
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
    return EdgeGraph(order, edges, value)


def _is_eligible_delta_five_non_three_sparse(graph: EdgeGraph) -> bool:
    degrees = [0] * graph.vertex_count
    for left, right in graph.edges:
        degrees[left] += 1
        degrees[right] += 1
    return max(degrees, default=0) == 5 and any(
        degrees[left] >= 4 and degrees[right] >= 4
        for left, right in graph.edges
    )


def _geng_tool_record(state: Mapping[str, object]) -> Mapping[str, object]:
    toolchain = state.get("toolchain")
    if not isinstance(toolchain, Mapping):
        raise ColoringRunAuditError("state has no toolchain mapping")
    record = toolchain.get("geng")
    if not isinstance(record, Mapping):
        raise ColoringRunAuditError("state has no geng tool record")
    path = Path(str(record.get("path", "")))
    if not path.is_file():
        raise ColoringRunAuditError("recorded geng executable is unavailable")
    if _file_sha256(path) != record.get("sha256"):
        raise ColoringRunAuditError("recorded geng executable hash changed")
    return record


def _iter_geng_catalogue(
    tool: Mapping[str, object],
    *,
    order: int,
    shard: tuple[int, int],
) -> Iterator[str]:
    path = Path(str(tool["path"]))
    environment = os.environ.copy()
    library_directories: list[str] = []
    linkage = tool.get("dynamic_linkage")
    if isinstance(linkage, Mapping):
        dependencies = linkage.get("dependencies")
        if isinstance(dependencies, Mapping):
            for raw in dependencies.values():
                if not isinstance(raw, Mapping) or "path" not in raw:
                    continue
                directory = str(Path(str(raw["path"])).parent)
                if directory not in library_directories:
                    library_directories.append(directory)
    previous = environment.get("LD_LIBRARY_PATH")
    if previous:
        library_directories.append(previous)
    if library_directories:
        environment["LD_LIBRARY_PATH"] = os.pathsep.join(
            library_directories
        )
    command = [
        str(path),
        "-q",
        "-C",
        "-d2",
        "-D5",
        str(order),
        f"{shard[0]}/{shard[1]}",
    ]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=environment,
    )
    assert process.stdout is not None
    assert process.stderr is not None
    completed_normally = False
    try:
        for line in process.stdout:
            record = line.strip()
            if not record:
                raise ColoringRunAuditError(
                    "geng emitted an empty catalogue record"
                )
            yield record
        stderr = process.stderr.read()
        return_code = process.wait()
        completed_normally = True
        if return_code != 0 or stderr.strip():
            raise ColoringRunAuditError(
                f"geng catalogue replay failed ({return_code}): {stderr.strip()}"
            )
    finally:
        process.stdout.close()
        process.stderr.close()
        if not completed_normally and process.poll() is None:
            process.terminate()
            process.wait(timeout=5)


def independently_verify_acyclic_coloring(
    graph: EdgeGraph,
    coloring: Sequence[int],
    *,
    color_count: int = 7,
) -> bool:
    """Check properness and absence of bichromatic cycles from first principles."""

    if len(coloring) != len(graph.edges) or color_count <= 0:
        return False
    if any(type(color) is not int or not 0 <= color < color_count for color in coloring):
        return False

    incident_colors = [set() for _ in range(graph.vertex_count)]
    for edge_index, (left, right) in enumerate(graph.edges):
        color = coloring[edge_index]
        if color in incident_colors[left] or color in incident_colors[right]:
            return False
        incident_colors[left].add(color)
        incident_colors[right].add(color)

    used_colors = sorted(set(coloring))
    for first_position, first_color in enumerate(used_colors):
        for second_color in used_colors[first_position + 1 :]:
            parent = list(range(graph.vertex_count))
            rank = [0] * graph.vertex_count

            def find(vertex: int) -> int:
                while parent[vertex] != vertex:
                    parent[vertex] = parent[parent[vertex]]
                    vertex = parent[vertex]
                return vertex

            for edge_index, (left, right) in enumerate(graph.edges):
                if coloring[edge_index] not in (first_color, second_color):
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


def audit_coloring_shard(
    directory: Path,
    *,
    expected_generated: int,
    color_count: int = 7,
) -> dict[str, object]:
    """Regenerate one n=10 catalogue shard and replay every SAT witness."""

    state_path = directory / "state.json"
    events_path = directory / "events.jsonl"
    if not state_path.is_file() or not events_path.is_file():
        raise ColoringRunAuditError(f"missing state/events in {directory}")

    state = json.loads(state_path.read_text(encoding="utf-8"))
    shard_value = state.get("shard")
    if (
        state.get("problem") != "opg145"
        or state.get("lane") != "default"
        or int(state.get("minimum_order", -1)) != 10
        or int(state.get("maximum_order", -1)) != 10
        or int(state.get("next_order", -1)) != 11
        or int(state.get("next_index", -1)) != 0
        or not isinstance(shard_value, list)
        or len(shard_value) != 2
        or int(shard_value[1]) != 4
        or not 0 <= int(shard_value[0]) < 4
    ):
        raise ColoringRunAuditError(
            "audit accepts only complete n=10 opg145 i/4 campaign shards"
        )
    shard = int(shard_value[0]), int(shard_value[1])
    if state.get("status") != "complete":
        raise ColoringRunAuditError(
            f"shard is not complete: {state.get('status')!r}"
        )
    if color_count != 7:
        raise ColoringRunAuditError("the n=10 campaign contract uses seven colors")
    if int(state.get("timeouts", -1)) != 0 or int(state.get("unsat", -1)) != 0:
        raise ColoringRunAuditError("completed null shard has timeout or UNSAT")
    if state.get("hard_queue") != []:
        raise ColoringRunAuditError("completed shard has a nonempty hard queue")
    if state.get("implementation_sha256") != _search_implementation_fingerprint():
        raise ColoringRunAuditError(
            "search implementation no longer matches the checkpoint"
        )
    if expected_generated <= 0:
        raise ColoringRunAuditError("expected_generated must be positive")
    if int(state.get("generated", -1)) != expected_generated:
        raise ColoringRunAuditError(
            f"generated {state.get('generated')}, expected {expected_generated}"
        )

    event_digest = hashlib.sha256()
    catalogue_digest = hashlib.sha256()
    event_count = 0
    generated = 0
    eligible = 0
    filtered = 0
    maximum_elapsed = 0.0
    maximum_lazy_cuts = 0
    tool = _geng_tool_record(state)
    with events_path.open("rb") as events:
        for index, record in enumerate(
            _iter_geng_catalogue(tool, order=10, shard=shard)
        ):
            generated += 1
            catalogue_digest.update(record.encode("ascii") + b"\n")
            graph = _decode_graph6_independently(record)
            if graph.vertex_count != 10:
                raise ColoringRunAuditError(
                    f"catalogue record {index} has the wrong order"
                )
            if not _is_eligible_delta_five_non_three_sparse(graph):
                filtered += 1
                continue
            eligible += 1
            raw_line = events.readline()
            if not raw_line:
                raise ColoringRunAuditError(
                    f"missing eligible event for catalogue index {index}"
                )
            event_count += 1
            event_digest.update(raw_line)
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError as error:
                raise ColoringRunAuditError(
                    f"invalid JSON at event line {event_count}"
                ) from error
            if (
                event.get("problem") != "opg145"
                or event.get("status") != "sat"
                or int(event.get("order", -1)) != 10
                or int(event.get("index", -1)) != index
                or event.get("encoding") != record
                or int(event.get("vertices", -1)) != 10
                or int(event.get("edges", -1)) != len(graph.edges)
            ):
                raise ColoringRunAuditError(
                    f"catalogue/event binding failed at index {index}"
                )
            raw_coloring = event.get("verified_coloring")
            if not isinstance(raw_coloring, list) or not independently_verify_acyclic_coloring(
                graph, raw_coloring, color_count=color_count
            ):
                raise ColoringRunAuditError(
                    f"invalid acyclic coloring at catalogue index {index}"
                )
            maximum_elapsed = max(
                maximum_elapsed, float(event.get("elapsed_seconds", 0.0))
            )
            maximum_lazy_cuts = max(
                maximum_lazy_cuts, int(event.get("lazy_cycle_cuts", 0))
            )
        if events.readline():
            raise ColoringRunAuditError(
                "events remain after the regenerated catalogue was exhausted"
            )

    sat = int(state["sat"])
    if generated != expected_generated:
        raise ColoringRunAuditError(
            f"regenerated {generated}, expected {expected_generated}"
        )
    if (
        event_count != eligible
        or event_count != sat
        or eligible != int(state["eligible"])
        or filtered != int(state["filtered_known_positive"])
    ):
        raise ColoringRunAuditError(
            "regenerated eligibility, events, and checkpoint counts disagree"
        )
    if generated != eligible + filtered:
        raise ColoringRunAuditError(
            "generated count does not equal eligible plus theorem-filtered"
        )

    return {
        "directory": str(directory),
        "shard": list(shard),
        "order_contract": [10, 10],
        "catalogue_event_binding": "exact_index_and_graph6",
        "eligibility_recomputed": "maximum_degree_5_and_not_3_sparse",
        "search_implementation_sha256": state.get(
            "implementation_sha256"
        ),
        "auditor_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "generated": generated,
        "filtered_known_positive": filtered,
        "eligible": eligible,
        "sat_witnesses_replayed": event_count,
        "maximum_elapsed_seconds": maximum_elapsed,
        "maximum_lazy_cycle_cuts": maximum_lazy_cuts,
        "geng_sha256": tool.get("sha256"),
        "catalogue_sha256": catalogue_digest.hexdigest(),
        "events_sha256": event_digest.hexdigest(),
        "status": "independently_verified",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Independently replay completed OPG-145 shard witnesses."
    )
    parser.add_argument("directories", nargs="+", type=Path)
    parser.add_argument(
        "--expected-generated",
        nargs="+",
        type=int,
        required=True,
        help="one exact geng count per directory",
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(argv)
    expected = arguments.expected_generated
    if len(expected) != len(arguments.directories):
        parser.error("--expected-generated must have one value per directory")
    reports = [
        audit_coloring_shard(
            directory,
            expected_generated=expected[index],
        )
        for index, directory in enumerate(arguments.directories)
    ]
    shard_indexes = [int(report["shard"][0]) for report in reports]  # type: ignore[index]
    if len(reports) == 4 and sorted(shard_indexes) != [0, 1, 2, 3]:
        parser.error("four-shard audit must contain each i/4 shard exactly once")
    payload = {
        "shards": reports,
        "totals": {
            "generated": sum(int(report["generated"]) for report in reports),
            "filtered_known_positive": sum(
                int(report["filtered_known_positive"]) for report in reports
            ),
            "eligible": sum(int(report["eligible"]) for report in reports),
            "sat_witnesses_replayed": sum(
                int(report["sat_witnesses_replayed"]) for report in reports
            ),
        },
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
