"""Fail-closed execution audit for the OPG-1757 n=9 campaign.

The production search records one event for every graph emitted by a sharded
``geng -c 9 19:36`` catalogue.  This auditor does not import the production
counter or graph6 decoder.  It validates the recorded executable and shared
libraries, regenerates the exact catalogue, independently decodes graph6,
binds every catalogue record to one event, and checks the persisted integer
arithmetic and elementary counting bounds.

The event protocol stores counts only for the edge pair selected by the
production search.  It does not store the full vector/matrix of single-edge
and pair counts.  Consequently this module cannot independently recompute the
forest counts or prove that the reported pair is strongest.  The report makes
that residual trust boundary explicit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Iterator, Mapping, Sequence


AUDIT_SCHEMA = "amra.opg1757.run_audit.v1"
CAMPAIGN_ORDER = 9
CAMPAIGN_MINIMUM_EDGES = 19
CAMPAIGN_MAXIMUM_EDGES = 36
CAMPAIGN_SHARD_COUNT = 4
CAMPAIGN_MAX_STATES = 2_000_000

_EVENT_KEYS = frozenset(
    {
        "time",
        "index",
        "graph6",
        "vertices",
        "edges",
        "status",
        "states",
        "elapsed_seconds",
        "strongest_pair",
    }
)
_PAIR_KEYS = frozenset(
    {
        "edge_indexes",
        "edge_e",
        "edge_f",
        "forest_count",
        "forest_count_e",
        "forest_count_f",
        "forest_count_ef",
        "left_product",
        "right_product",
        "margin",
    }
)
_BEST_PAIR_KEYS = _PAIR_KEYS | {"index", "graph6"}


class UniformForestRunAuditError(ValueError):
    """Raised when a persisted OPG-1757 shard fails closed."""


@dataclass(frozen=True)
class _DecodedGraph:
    vertex_count: int
    edges: tuple[tuple[int, int], ...]
    encoding: str


@dataclass(frozen=True)
class _ValidatedGeng:
    path: Path
    sha256: str
    library_directories: tuple[str, ...]
    dependency_hashes: Mapping[str, str]


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _implementation_fingerprint() -> str:
    """Reproduce the production two-file fingerprint without importing it."""

    directory = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    for name in ("opg_uniform_forest_search.py", "opg_coloring_search.py"):
        path = (directory / name).resolve()
        if not path.is_file():
            raise UniformForestRunAuditError(
                f"search implementation file is unavailable: {path}"
            )
        digest.update(str(path).encode("utf-8"))
        digest.update(_file_sha256(path).encode("ascii"))
    return digest.hexdigest()


def _require_mapping(value: object, field: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise UniformForestRunAuditError(f"{field} must be a mapping")
    return value


def _require_int(value: object, field: str, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise UniformForestRunAuditError(f"{field} must be an integer")
    if minimum is not None and value < minimum:
        raise UniformForestRunAuditError(
            f"{field} must be at least {minimum}, got {value}"
        )
    return value


def _require_finite_number(
    value: object,
    field: str,
    *,
    minimum: float | None = None,
) -> float:
    if type(value) not in (int, float):
        raise UniformForestRunAuditError(f"{field} must be a number")
    result = float(value)
    if not math.isfinite(result):
        raise UniformForestRunAuditError(f"{field} must be finite")
    if minimum is not None and result < minimum:
        raise UniformForestRunAuditError(
            f"{field} must be at least {minimum}, got {result}"
        )
    return result


def _decode_graph6_independently(record: str) -> _DecodedGraph:
    value = record.strip()
    if value.startswith(">>graph6<<"):
        value = value[10:]
    if not value or value[0] == "~":
        raise UniformForestRunAuditError(
            "unsupported or empty compact graph6 record"
        )
    order = ord(value[0]) - 63
    if not 0 <= order <= 62:
        raise UniformForestRunAuditError("invalid compact graph6 order")
    required_bits = order * (order - 1) // 2
    required_characters = (required_bits + 5) // 6
    if len(value) != required_characters + 1:
        raise UniformForestRunAuditError("graph6 payload length is invalid")
    bits: list[int] = []
    for character in value[1:]:
        encoded = ord(character) - 63
        if not 0 <= encoded < 64:
            raise UniformForestRunAuditError(
                "graph6 contains an invalid character"
            )
        bits.extend(
            (encoded >> shift) & 1 for shift in range(5, -1, -1)
        )
    if any(bits[required_bits:]):
        raise UniformForestRunAuditError("graph6 padding bits are nonzero")
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
    return _DecodedGraph(order, edges, value)


def _is_connected(graph: _DecodedGraph) -> bool:
    if graph.vertex_count == 0:
        return False
    adjacency = [[] for _ in range(graph.vertex_count)]
    for left, right in graph.edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return len(seen) == graph.vertex_count


def _validate_file_record(
    raw_record: object,
    field: str,
) -> tuple[Path, str]:
    record = _require_mapping(raw_record, field)
    path = Path(str(record.get("path", "")))
    expected = record.get("sha256")
    if not path.is_file():
        raise UniformForestRunAuditError(f"{field} file is unavailable")
    if not isinstance(expected, str) or len(expected) != 64:
        raise UniformForestRunAuditError(f"{field} has no valid SHA-256")
    actual = _file_sha256(path)
    if actual != expected:
        raise UniformForestRunAuditError(
            f"{field} SHA-256 changed: {actual} != {expected}"
        )
    return path, actual


def _validated_geng_tool(state: Mapping[str, object]) -> _ValidatedGeng:
    toolchain = _require_mapping(state.get("toolchain"), "state.toolchain")
    if set(toolchain) != {"geng"}:
        raise UniformForestRunAuditError(
            "state.toolchain must contain exactly the recorded geng tool"
        )
    record = _require_mapping(toolchain.get("geng"), "state.toolchain.geng")
    path, executable_hash = _validate_file_record(
        record,
        "state.toolchain.geng",
    )
    linkage = _require_mapping(
        record.get("dynamic_linkage"),
        "state.toolchain.geng.dynamic_linkage",
    )
    if _require_int(
        linkage.get("ldd_exit"),
        "state.toolchain.geng.dynamic_linkage.ldd_exit",
    ) != 0:
        raise UniformForestRunAuditError("recorded geng ldd invocation failed")
    missing = linkage.get("missing")
    if not isinstance(missing, list) or missing:
        raise UniformForestRunAuditError(
            "recorded geng dynamic linkage has missing dependencies"
        )
    dependencies = _require_mapping(
        linkage.get("dependencies"),
        "state.toolchain.geng.dynamic_linkage.dependencies",
    )
    if not dependencies:
        raise UniformForestRunAuditError(
            "recorded geng dynamic dependency set is empty"
        )
    directories: list[str] = []
    dependency_hashes: dict[str, str] = {}
    for name in sorted(dependencies):
        dependency_path, dependency_hash = _validate_file_record(
            dependencies[name],
            f"state.toolchain.geng dependency {name}",
        )
        directory = str(dependency_path.parent)
        if directory not in directories:
            directories.append(directory)
        dependency_hashes[str(name)] = dependency_hash
    return _ValidatedGeng(
        path=path,
        sha256=executable_hash,
        library_directories=tuple(directories),
        dependency_hashes=dependency_hashes,
    )


def _iter_geng_catalogue(
    tool: _ValidatedGeng,
    *,
    order: int,
    minimum_edges: int,
    maximum_edges: int,
    shard: tuple[int, int],
) -> Iterator[str]:
    environment = os.environ.copy()
    directories = list(tool.library_directories)
    previous = environment.get("LD_LIBRARY_PATH")
    if previous:
        directories.append(previous)
    if directories:
        environment["LD_LIBRARY_PATH"] = os.pathsep.join(directories)
    command = [
        str(tool.path),
        "-q",
        "-c",
        str(order),
        f"{minimum_edges}:{maximum_edges}",
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
            record = line.rstrip("\n")
            if not record:
                raise UniformForestRunAuditError(
                    "geng emitted an empty catalogue record"
                )
            yield record
        stderr = process.stderr.read()
        return_code = process.wait()
        completed_normally = True
        if return_code != 0 or stderr.strip():
            raise UniformForestRunAuditError(
                f"geng catalogue replay failed ({return_code}): "
                f"{stderr.strip()}"
            )
    finally:
        process.stdout.close()
        process.stderr.close()
        if not completed_normally and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


def _validate_pair_record(
    raw_pair: object,
    graph: _DecodedGraph,
    *,
    catalogue_index: int,
) -> dict[str, object]:
    pair = _require_mapping(
        raw_pair,
        f"event[{catalogue_index}].strongest_pair",
    )
    if set(pair) != _PAIR_KEYS:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] strongest_pair schema is invalid"
        )
    raw_indexes = pair.get("edge_indexes")
    if not isinstance(raw_indexes, list) or len(raw_indexes) != 2:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] edge_indexes must contain two entries"
        )
    first = _require_int(
        raw_indexes[0],
        f"event[{catalogue_index}].edge_indexes[0]",
        minimum=0,
    )
    second = _require_int(
        raw_indexes[1],
        f"event[{catalogue_index}].edge_indexes[1]",
        minimum=0,
    )
    if not first < second < len(graph.edges):
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] edge indexes are not a valid "
            "ordered distinct pair"
        )
    if pair.get("edge_e") != list(graph.edges[first]):
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] edge_e does not match graph6"
        )
    if pair.get("edge_f") != list(graph.edges[second]):
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] edge_f does not match graph6"
        )

    forest_count = _require_int(
        pair.get("forest_count"),
        f"event[{catalogue_index}].forest_count",
        minimum=1,
    )
    count_e = _require_int(
        pair.get("forest_count_e"),
        f"event[{catalogue_index}].forest_count_e",
        minimum=1,
    )
    count_f = _require_int(
        pair.get("forest_count_f"),
        f"event[{catalogue_index}].forest_count_f",
        minimum=1,
    )
    count_ef = _require_int(
        pair.get("forest_count_ef"),
        f"event[{catalogue_index}].forest_count_ef",
        minimum=1,
    )
    left = _require_int(
        pair.get("left_product"),
        f"event[{catalogue_index}].left_product",
        minimum=1,
    )
    right = _require_int(
        pair.get("right_product"),
        f"event[{catalogue_index}].right_product",
        minimum=1,
    )
    margin = _require_int(
        pair.get("margin"),
        f"event[{catalogue_index}].margin",
    )

    edge_count = len(graph.edges)
    order = graph.vertex_count
    total_upper = sum(
        math.comb(edge_count, size)
        for size in range(0, min(order - 1, edge_count) + 1)
    )
    edge_upper = sum(
        math.comb(edge_count - 1, size)
        for size in range(0, min(order - 2, edge_count - 1) + 1)
    )
    pair_upper = sum(
        math.comb(edge_count - 2, size)
        for size in range(0, min(order - 3, edge_count - 2) + 1)
    )
    total_lower = 1 + edge_count + math.comb(edge_count, 2)
    if not total_lower <= forest_count <= total_upper:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] forest_count violates basic bounds"
        )
    if not edge_count <= count_e <= edge_upper:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] forest_count_e violates basic bounds"
        )
    if not edge_count <= count_f <= edge_upper:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] forest_count_f violates basic bounds"
        )
    if not 1 <= count_ef <= pair_upper:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] forest_count_ef violates basic bounds"
        )
    if count_ef > min(count_e, count_f):
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] pair count exceeds a marginal count"
        )
    if count_e > forest_count or count_f > forest_count:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] marginal count exceeds total forests"
        )
    if count_e + count_f - count_ef > forest_count:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] inclusion-exclusion bound fails"
        )
    if left != forest_count * count_ef:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] left_product is inconsistent"
        )
    if right != count_e * count_f:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] right_product is inconsistent"
        )
    if margin != right - left:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] margin is inconsistent"
        )
    if left > right:
        raise UniformForestRunAuditError(
            f"event[{catalogue_index}] contains a negative-association "
            "violation"
        )
    return {key: pair[key] for key in sorted(_PAIR_KEYS)}


def _candidate_is_better(
    candidate: Mapping[str, object],
    incumbent: Mapping[str, object] | None,
) -> bool:
    if incumbent is None:
        return True
    return (
        int(candidate["left_product"]) * int(incumbent["right_product"])
        > int(incumbent["left_product"]) * int(candidate["right_product"])
    )


def audit_uniform_forest_shard(
    directory: Path,
    *,
    expected_generated: int,
) -> dict[str, object]:
    """Regenerate and audit one completed OPG-1757 n=9 i/4 shard."""

    state_path = directory / "state.json"
    events_path = directory / "events.jsonl"
    candidate_path = directory / "candidate.json"
    if not state_path.is_file() or not events_path.is_file():
        raise UniformForestRunAuditError(
            f"missing state/events in {directory}"
        )
    if candidate_path.exists():
        raise UniformForestRunAuditError(
            "completed null-result shard unexpectedly has candidate.json"
        )

    state_bytes = state_path.read_bytes()
    state = json.loads(state_bytes)
    if not isinstance(state, dict):
        raise UniformForestRunAuditError("state.json must contain an object")
    shard_value = state.get("shard")
    if (
        state.get("checkpoint_schema") != 1
        or state.get("problem") != "opg1757"
        or state.get("connected_only") is not True
        or state.get("order") != CAMPAIGN_ORDER
        or state.get("minimum_edges") != CAMPAIGN_MINIMUM_EDGES
        or state.get("maximum_edges") != CAMPAIGN_MAXIMUM_EDGES
        or not isinstance(shard_value, list)
        or len(shard_value) != 2
        or type(shard_value[0]) is not int
        or type(shard_value[1]) is not int
        or shard_value[1] != CAMPAIGN_SHARD_COUNT
        or not 0 <= shard_value[0] < CAMPAIGN_SHARD_COUNT
    ):
        raise UniformForestRunAuditError(
            "audit accepts only OPG-1757 n=9 m=19..36 i/4 shards"
        )
    shard = shard_value[0], shard_value[1]
    if state.get("status") != "complete":
        raise UniformForestRunAuditError(
            f"shard is not complete: {state.get('status')!r}"
        )
    if state.get("candidate") is not None:
        raise UniformForestRunAuditError(
            "completed null-result state unexpectedly contains a candidate"
        )
    if state.get("hard_queue") != []:
        raise UniformForestRunAuditError(
            "completed shard has a nonempty hard queue"
        )
    if expected_generated <= 0:
        raise UniformForestRunAuditError(
            "expected_generated must be positive"
        )

    generated_state = _require_int(
        state.get("generated"),
        "state.generated",
        minimum=0,
    )
    evaluated_state = _require_int(
        state.get("evaluated"),
        "state.evaluated",
        minimum=0,
    )
    nonviolating_state = _require_int(
        state.get("nonviolating"),
        "state.nonviolating",
        minimum=0,
    )
    violations_state = _require_int(
        state.get("violations"),
        "state.violations",
        minimum=0,
    )
    timeouts_state = _require_int(
        state.get("timeouts"),
        "state.timeouts",
        minimum=0,
    )
    next_index = _require_int(
        state.get("next_index"),
        "state.next_index",
        minimum=0,
    )
    if generated_state != expected_generated:
        raise UniformForestRunAuditError(
            f"state generated {generated_state}, expected "
            f"{expected_generated}"
        )
    if not (
        generated_state
        == evaluated_state
        == nonviolating_state
        == next_index
    ):
        raise UniformForestRunAuditError(
            "state generated/evaluated/nonviolating/next_index do not close"
        )
    if violations_state != 0 or timeouts_state != 0:
        raise UniformForestRunAuditError(
            "completed null-result shard has a timeout or violation"
        )

    implementation_hash = _implementation_fingerprint()
    if state.get("implementation_sha256") != implementation_hash:
        raise UniformForestRunAuditError(
            "search implementation no longer matches the checkpoint"
        )
    tool = _validated_geng_tool(state)

    catalogue_digest = hashlib.sha256()
    event_digest = hashlib.sha256()
    seen_graph6: set[str] = set()
    generated = 0
    event_count = 0
    maximum_states = 0
    maximum_elapsed = 0.0
    minimum_margin: int | None = None
    best_pair: dict[str, object] | None = None

    with events_path.open("rb") as events:
        for index, record in enumerate(
            _iter_geng_catalogue(
                tool,
                order=CAMPAIGN_ORDER,
                minimum_edges=CAMPAIGN_MINIMUM_EDGES,
                maximum_edges=CAMPAIGN_MAXIMUM_EDGES,
                shard=shard,
            )
        ):
            generated += 1
            catalogue_digest.update(record.encode("ascii") + b"\n")
            if record in seen_graph6:
                raise UniformForestRunAuditError(
                    f"duplicate graph6 catalogue record at index {index}"
                )
            seen_graph6.add(record)
            graph = _decode_graph6_independently(record)
            if graph.vertex_count != CAMPAIGN_ORDER:
                raise UniformForestRunAuditError(
                    f"catalogue record {index} has the wrong order"
                )
            if not (
                CAMPAIGN_MINIMUM_EDGES
                <= len(graph.edges)
                <= CAMPAIGN_MAXIMUM_EDGES
            ):
                raise UniformForestRunAuditError(
                    f"catalogue record {index} is outside the edge range"
                )
            if not _is_connected(graph):
                raise UniformForestRunAuditError(
                    f"catalogue record {index} is disconnected"
                )

            raw_line = events.readline()
            if not raw_line:
                raise UniformForestRunAuditError(
                    f"missing event for catalogue index {index}"
                )
            event_count += 1
            event_digest.update(raw_line)
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError as error:
                raise UniformForestRunAuditError(
                    f"invalid JSON at event line {event_count}"
                ) from error
            if not isinstance(event, dict) or set(event) != _EVENT_KEYS:
                raise UniformForestRunAuditError(
                    f"event schema is invalid at catalogue index {index}"
                )
            if (
                event.get("index") != index
                or event.get("graph6") != record
                or event.get("vertices") != CAMPAIGN_ORDER
                or event.get("edges") != len(graph.edges)
            ):
                raise UniformForestRunAuditError(
                    f"catalogue/event binding failed at index {index}"
                )
            if event.get("status") != "nonviolating":
                raise UniformForestRunAuditError(
                    f"event {index} is not a completed nonviolating result"
                )
            _require_finite_number(
                event.get("time"),
                f"event[{index}].time",
                minimum=0.0,
            )
            elapsed = _require_finite_number(
                event.get("elapsed_seconds"),
                f"event[{index}].elapsed_seconds",
                minimum=0.0,
            )
            states = _require_int(
                event.get("states"),
                f"event[{index}].states",
                minimum=1,
            )
            if states > CAMPAIGN_MAX_STATES:
                raise UniformForestRunAuditError(
                    f"event[{index}] exceeds the campaign state budget"
                )
            pair = _validate_pair_record(
                event.get("strongest_pair"),
                graph,
                catalogue_index=index,
            )
            candidate = {"index": index, "graph6": record, **pair}
            if _candidate_is_better(candidate, best_pair):
                best_pair = candidate
            maximum_states = max(maximum_states, states)
            maximum_elapsed = max(maximum_elapsed, elapsed)
            margin = int(pair["margin"])
            minimum_margin = (
                margin
                if minimum_margin is None
                else min(minimum_margin, margin)
            )
        if events.readline():
            raise UniformForestRunAuditError(
                "events remain after the regenerated catalogue was exhausted"
            )

    if generated != expected_generated:
        raise UniformForestRunAuditError(
            f"regenerated {generated}, expected {expected_generated}"
        )
    if event_count != generated:
        raise UniformForestRunAuditError(
            "event count does not equal regenerated catalogue size"
        )
    raw_best = state.get("best_pair")
    if (
        not isinstance(raw_best, dict)
        or set(raw_best) != _BEST_PAIR_KEYS
        or raw_best != best_pair
    ):
        raise UniformForestRunAuditError(
            "state.best_pair does not match the exact event-stream maximum"
        )

    return {
        "schema": AUDIT_SCHEMA,
        "directory": str(directory),
        "problem": "opg1757",
        "shard": list(shard),
        "order": CAMPAIGN_ORDER,
        "edge_range": [
            CAMPAIGN_MINIMUM_EDGES,
            CAMPAIGN_MAXIMUM_EDGES,
        ],
        "generator_command_contract": [
            str(tool.path),
            "-q",
            "-c",
            str(CAMPAIGN_ORDER),
            (
                f"{CAMPAIGN_MINIMUM_EDGES}:"
                f"{CAMPAIGN_MAXIMUM_EDGES}"
            ),
            f"{shard[0]}/{shard[1]}",
        ],
        "generated": generated,
        "events_replayed": event_count,
        "nonviolating": event_count,
        "violations": 0,
        "timeouts": 0,
        "catalogue_event_binding": "exact_index_and_graph6",
        "catalogue_unique": True,
        "integer_checks": [
            "exact left_product, right_product, and margin identities",
            "forest/marginal/pair subset-count bounds",
            "marginal containment and inclusion-exclusion bounds",
            "reported pair is nonviolating",
        ],
        "best_reported_pair": best_pair,
        "minimum_reported_margin": minimum_margin,
        "maximum_states": maximum_states,
        "maximum_elapsed_seconds": maximum_elapsed,
        "state_sha256": hashlib.sha256(state_bytes).hexdigest(),
        "events_sha256": event_digest.hexdigest(),
        "catalogue_sha256": catalogue_digest.hexdigest(),
        "geng_sha256": tool.sha256,
        "geng_dependency_sha256": dict(tool.dependency_hashes),
        "search_implementation_sha256": implementation_hash,
        "auditor_sha256": _file_sha256(Path(__file__).resolve()),
        "residual_trust_boundary": [
            (
                "Events persist counts only for the production-selected edge "
                "pair; the full per-edge and per-pair count tables are absent."
            ),
            (
                "The persisted forest counts are checked for exact internal "
                "arithmetic and elementary combinatorial bounds, but are not "
                "independently recomputed."
            ),
            (
                "That the reported pair is strongest, and hence that no "
                "unreported pair violates negative association, remains "
                "dependent on the recorded search implementation hash."
            ),
        ],
        "status": "execution_evidence_verified_with_counting_trust_boundary",
    }


def _atomic_write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Regenerate and audit completed OPG-1757 n=9 m=19..36 "
            "catalogue shards."
        )
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
    if len(arguments.expected_generated) != len(arguments.directories):
        parser.error(
            "--expected-generated must have one value per directory"
        )
    reports = [
        audit_uniform_forest_shard(
            directory,
            expected_generated=arguments.expected_generated[index],
        )
        for index, directory in enumerate(arguments.directories)
    ]
    shard_indexes = [
        int(report["shard"][0])  # type: ignore[index]
        for report in reports
    ]
    if len(set(shard_indexes)) != len(shard_indexes):
        parser.error("each shard may be audited at most once")
    if len(reports) == CAMPAIGN_SHARD_COUNT and sorted(shard_indexes) != list(
        range(CAMPAIGN_SHARD_COUNT)
    ):
        parser.error("four-shard audit must contain every i/4 shard once")
    for field in (
        "geng_sha256",
        "search_implementation_sha256",
        "auditor_sha256",
    ):
        if len({str(report[field]) for report in reports}) != 1:
            parser.error(f"audited shards disagree on {field}")
    payload = {
        "schema": AUDIT_SCHEMA,
        "campaign_complete": len(reports) == CAMPAIGN_SHARD_COUNT,
        "shards": reports,
        "totals": {
            "generated": sum(int(report["generated"]) for report in reports),
            "events_replayed": sum(
                int(report["events_replayed"]) for report in reports
            ),
            "nonviolating": sum(
                int(report["nonviolating"]) for report in reports
            ),
            "violations": 0,
            "timeouts": 0,
        },
        "residual_trust_boundary": reports[0][
            "residual_trust_boundary"
        ],
    }
    if len(reports) == CAMPAIGN_SHARD_COUNT:
        payload["catalogue_shards"] = [[index, 4] for index in range(4)]
    if arguments.output is not None:
        _atomic_write_json(arguments.output, payload)
    print(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
