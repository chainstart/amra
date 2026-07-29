from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from amra.discovery.opg_coloring_search import (
    EdgeGraph,
    _atomic_json,
    _pipeline,
    decode_graph6,
    implementation_fingerprint,
    graph_payload,
    locate_tool,
    toolchain_fingerprint,
)


FLOW_CHECKPOINT_SCHEMA = 2


class FlowEvaluationBudgetExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class FlowEvaluation:
    numerator: int
    cycle_rank: int
    states: int
    elapsed_seconds: float


def _normalize(edges: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    normalized = [(min(left, right), max(left, right)) for left, right in edges]
    vertices = sorted({vertex for edge in normalized for vertex in edge})
    labels = {vertex: index for index, vertex in enumerate(vertices)}
    return tuple(
        sorted((labels[left], labels[right]) for left, right in normalized)
    )


def _vertex_count(edges: Sequence[tuple[int, int]]) -> int:
    return 0 if not edges else max(max(edge) for edge in edges) + 1


def _components(
    edges: Sequence[tuple[int, int]],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    n = _vertex_count(edges)
    adjacency = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        if left == right:
            continue
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    labels = [-1] * n
    component_count = 0
    for start in range(n):
        if labels[start] >= 0:
            continue
        labels[start] = component_count
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other, _ in adjacency[vertex]:
                if labels[other] < 0:
                    labels[other] = component_count
                    stack.append(other)
        component_count += 1
    grouped: list[list[tuple[int, int]]] = [[] for _ in range(component_count)]
    for edge in edges:
        grouped[labels[edge[0]]].append(edge)
    return tuple(_normalize(group) for group in grouped if group)


def _bridge_indexes(edges: Sequence[tuple[int, int]]) -> frozenset[int]:
    n = _vertex_count(edges)
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        if left == right:
            continue
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    discovery = [-1] * n
    low = [0] * n
    clock = 0
    bridges: set[int] = set()

    def visit(vertex: int, parent_edge: int) -> None:
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        for other, edge in adjacency[vertex]:
            if edge == parent_edge:
                continue
            if discovery[other] < 0:
                visit(other, edge)
                low[vertex] = min(low[vertex], low[other])
                if low[other] > discovery[vertex]:
                    bridges.add(edge)
            else:
                low[vertex] = min(low[vertex], discovery[other])

    for vertex in range(n):
        if discovery[vertex] < 0:
            visit(vertex, -1)
    return frozenset(bridges)


def _suppress_degree_two(
    edges: Sequence[tuple[int, int]],
) -> tuple[tuple[int, int], ...] | None:
    n = _vertex_count(edges)
    incident: list[list[int]] = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        if left == right:
            continue
        incident[left].append(edge)
        incident[right].append(edge)
    for vertex, row in enumerate(incident):
        if len(row) != 2:
            continue
        first, second = row
        first_other = (
            edges[first][1] if edges[first][0] == vertex else edges[first][0]
        )
        second_other = (
            edges[second][1] if edges[second][0] == vertex else edges[second][0]
        )
        remaining = [
            edge
            for index, edge in enumerate(edges)
            if index not in {first, second}
        ]
        remaining.append((first_other, second_other))
        return _normalize(remaining)
    return None


def _delete(
    edges: Sequence[tuple[int, int]], edge: int
) -> tuple[tuple[int, int], ...]:
    return _normalize(item for index, item in enumerate(edges) if index != edge)


def _contract(
    edges: Sequence[tuple[int, int]], edge: int
) -> tuple[tuple[int, int], ...]:
    left, right = edges[edge]
    if left == right:
        raise ValueError("loops are deleted, not contracted")
    contracted = []
    for index, (first, second) in enumerate(edges):
        if index == edge:
            continue
        first = left if first == right else first
        second = left if second == right else second
        contracted.append((first, second))
    return _normalize(contracted)


def flow_numerator_11_over_2(
    graph: EdgeGraph,
    *,
    timeout_seconds: float = 30.0,
    max_states: int = 2_000_000,
) -> FlowEvaluation:
    """Return N(G)=2^r F(G,11/2), using exact integer recurrence."""

    initial = _normalize(graph.edges)
    n = graph.vertex_count
    component_count = _component_count(graph.vertex_count, graph.edges)
    cycle_rank = len(graph.edges) - n + component_count
    memo: dict[tuple[tuple[int, int], ...], int] = {}
    expanded_states = 0
    started = time.monotonic()

    def visit(edges: tuple[tuple[int, int], ...]) -> int:
        nonlocal expanded_states
        cached = memo.get(edges)
        if cached is not None:
            return cached
        expanded_states += 1
        if expanded_states > max_states or time.monotonic() - started > timeout_seconds:
            raise FlowEvaluationBudgetExceeded(
                f"flow recurrence exceeded {max_states} states or {timeout_seconds}s"
            )
        if not edges:
            memo[edges] = 1
            return 1
        parts = _components(edges)
        if len(parts) > 1:
            value = 1
            for part in parts:
                value *= visit(part)
            memo[edges] = value
            return value
        for edge, (left, right) in enumerate(edges):
            if left == right:
                value = 9 * visit(_delete(edges, edge))
                memo[edges] = value
                return value
        if _bridge_indexes(edges):
            memo[edges] = 0
            return 0
        suppressed = _suppress_degree_two(edges)
        if suppressed is not None:
            value = visit(suppressed)
            memo[edges] = value
            return value
        degrees = [0] * _vertex_count(edges)
        multiplicities: dict[tuple[int, int], int] = {}
        for left, right in edges:
            degrees[left] += 1
            degrees[right] += 1
            multiplicities[(left, right)] = multiplicities.get((left, right), 0) + 1
        branch = max(
            range(len(edges)),
            key=lambda index: (
                multiplicities[edges[index]],
                degrees[edges[index][0]] + degrees[edges[index][1]],
            ),
        )
        value = visit(_contract(edges, branch)) - 2 * visit(_delete(edges, branch))
        memo[edges] = value
        return value

    numerator = visit(initial)
    return FlowEvaluation(
        numerator,
        cycle_rank,
        len(memo),
        time.monotonic() - started,
    )


def spanning_subgraph_numerator_11_over_2(graph: EdgeGraph) -> int:
    """Independent 2^m oracle, intended only for small regression graphs."""

    m = len(graph.edges)
    component_count = _component_count(graph.vertex_count, graph.edges)
    rank = m - graph.vertex_count + component_count
    value = 0
    for mask in range(1 << m):
        selected = [
            edge for index, edge in enumerate(graph.edges) if mask & (1 << index)
        ]
        dimension = (
            len(selected)
            - graph.vertex_count
            + _component_count(graph.vertex_count, selected)
        )
        sign = -1 if (m - len(selected)) % 2 else 1
        value += sign * 11**dimension * 2 ** (rank - dimension)
    return value


def _component_count(n: int, edges: Iterable[tuple[int, int]]) -> int:
    parent = list(range(n))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root
    return len({find(vertex) for vertex in range(n)})


def _connected_after_removing(
    graph: EdgeGraph, removed: frozenset[int]
) -> bool:
    if graph.vertex_count <= 1:
        return True
    adjacency = [[] for _ in range(graph.vertex_count)]
    for edge, (left, right) in enumerate(graph.edges):
        if edge in removed:
            continue
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


def is_three_edge_connected(graph: EdgeGraph) -> bool:
    if not _connected_after_removing(graph, frozenset()):
        return False
    for size in (1, 2):
        for removed in combinations(range(len(graph.edges)), size):
            if not _connected_after_removing(graph, frozenset(removed)):
                return False
    return True


def iter_girth_six_cubic_graphs(
    order: int, shard: tuple[int, int] | None = None
) -> Iterator[EdgeGraph]:
    if order % 2:
        return
    geng = str(locate_tool("geng"))
    command = [geng, "-q", "-c", "-t", "-f", "-p", "-d3", "-D3", str(order)]
    if shard:
        command.append(f"{shard[0]}/{shard[1]}")
    for line in _pipeline((command,)):
        yield decode_graph6(line)


def run_flow_search(
    minimum_order: int,
    maximum_order: int,
    wall_seconds: float,
    per_graph_seconds: float,
    max_states: int,
    output: Path,
    shard: tuple[int, int] | None = None,
) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    state_path = output / "state.json"
    events_path = output / "events.jsonl"
    candidate_path = output / "candidate.json"
    if not state_path.exists():
        orphaned = [
            path.name for path in (events_path, candidate_path) if path.exists()
        ]
        if orphaned:
            raise ValueError(
                "search artifacts exist without state.json: "
                + ", ".join(orphaned)
            )
    fingerprint = implementation_fingerprint(
        Path(__file__), Path(__file__).with_name("opg_coloring_search.py")
    )
    tools = toolchain_fingerprint(("geng",))
    state: dict[str, object] = {
        "checkpoint_schema": FLOW_CHECKPOINT_SCHEMA,
        "implementation_sha256": fingerprint,
        "toolchain": tools,
        "problem": "opg348",
        "minimum_order": minimum_order,
        "next_order": minimum_order,
        "next_index": 0,
        "maximum_order": maximum_order,
        "generated": 0,
        "three_edge_connected": 0,
        "positive": 0,
        "nonpositive": 0,
        "timeouts": 0,
        "hard_queue": [],
        "status": "running",
        "shard": list(shard) if shard else None,
    }
    if state_path.exists():
        loaded = json.loads(state_path.read_text(encoding="utf-8"))
        if loaded.get("checkpoint_schema") != FLOW_CHECKPOINT_SCHEMA:
            raise ValueError("legacy checkpoint requires a new output directory")
        identity = (
            loaded.get("shard"),
            loaded.get("implementation_sha256"),
            loaded.get("toolchain"),
        )
        expected = (list(shard) if shard else None, fingerprint, tools)
        if identity != expected:
            raise ValueError("checkpoint identity does not match")
        if int(loaded["minimum_order"]) != minimum_order:
            raise ValueError("minimum_order cannot change when resuming a checkpoint")
        if maximum_order < int(loaded["maximum_order"]):
            raise ValueError("maximum_order cannot shrink when resuming a checkpoint")
        state.update(loaded)
        if (
            state.get("status") == "candidate_pending_independent_verification"
            or state.get("candidate") is not None
            or int(state["nonpositive"]) > 0
            or candidate_path.exists()
        ):
            if state.get("candidate") is None and candidate_path.exists():
                state["candidate"] = json.loads(
                    candidate_path.read_text(encoding="utf-8")
                )
            state["nonpositive"] = max(1, int(state["nonpositive"]))
            state["status"] = "candidate_pending_independent_verification"
            _atomic_json(state_path, state)
            return state
        state["maximum_order"] = maximum_order
        state["status"] = "running"

    deadline = time.monotonic() + wall_seconds

    def wall_expired() -> bool:
        return time.monotonic() >= deadline

    def pause_for_wall_budget() -> dict[str, object]:
        state["status"] = "paused_budget"
        _atomic_json(state_path, state)
        return state

    def evaluate_graph(
        graph: EdgeGraph,
        order: int,
        index: int,
        *,
        retry: bool = False,
    ) -> tuple[str, dict[str, object] | None]:
        event: dict[str, object] = {
            "time": time.time(),
            "order": order,
            "index": index,
            "graph6": graph.encoding,
        }
        if retry:
            event["retry"] = True
        remaining_wall = max(0.0, deadline - time.monotonic())
        try:
            result = flow_numerator_11_over_2(
                graph,
                timeout_seconds=min(per_graph_seconds, remaining_wall),
                max_states=max_states,
            )
        except FlowEvaluationBudgetExceeded as error:
            state["timeouts"] = int(state["timeouts"]) + 1
            hard = {"order": order, "index": index, "graph6": graph.encoding}
            event.update({"status": "timeout", "error": str(error)})
            outcome = "timeout"
        else:
            hard = None
            event.update(
                {
                    "status": "positive" if result.numerator > 0 else "nonpositive",
                    "numerator": result.numerator,
                    "cycle_rank": result.cycle_rank,
                    "states": result.states,
                    "elapsed_seconds": result.elapsed_seconds,
                }
            )
            if result.numerator > 0:
                state["positive"] = int(state["positive"]) + 1
                outcome = "positive"
            else:
                state["nonpositive"] = int(state["nonpositive"]) + 1
                candidate = {
                    "problem": "opg348",
                    "graph": graph_payload(graph),
                    "evaluation": event,
                    "verification_status": "pending_independent_spanning_subgraph_or_second_recurrence",
                }
                _atomic_json(candidate_path, candidate)
                state["candidate"] = candidate
                state["status"] = "candidate_pending_independent_verification"
                outcome = "candidate"
        with events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
        return outcome, hard

    if int(state["next_order"]) > maximum_order and not state["hard_queue"]:
        state["status"] = "complete"
        _atomic_json(state_path, state)
        return state

    if wall_expired():
        return pause_for_wall_budget()

    pending_hard = list(state["hard_queue"])
    retained_hard: list[object] = []
    for position, raw_hard in enumerate(pending_hard):
        if wall_expired():
            state["hard_queue"] = retained_hard + pending_hard[position:]
            return pause_for_wall_budget()
        hard = dict(raw_hard)
        graph = decode_graph6(str(hard["graph6"]))
        outcome, _ = evaluate_graph(
            graph,
            int(hard["order"]),
            int(hard["index"]),
            retry=True,
        )
        if outcome == "timeout":
            retained_hard.append(hard)
        state["hard_queue"] = retained_hard + pending_hard[position + 1 :]
        _atomic_json(state_path, state)
        if outcome == "candidate":
            return state
    state["hard_queue"] = retained_hard

    if int(state["next_order"]) > maximum_order:
        state["status"] = (
            "complete_with_hard_queue" if state["hard_queue"] else "complete"
        )
        _atomic_json(state_path, state)
        return state

    for order in range(int(state["next_order"]), maximum_order + 1):
        if wall_expired():
            return pause_for_wall_budget()
        resume_index = int(state["next_index"]) if order == int(state["next_order"]) else 0
        for index, graph in enumerate(iter_girth_six_cubic_graphs(order, shard)):
            if wall_expired():
                return pause_for_wall_budget()
            if index < resume_index:
                continue
            if not is_three_edge_connected(graph):
                state["generated"] = int(state["generated"]) + 1
                state["next_order"] = order
                state["next_index"] = index + 1
                if int(state["generated"]) % 10 == 0:
                    _atomic_json(state_path, state)
                if wall_expired():
                    return pause_for_wall_budget()
                continue
            if wall_expired():
                return pause_for_wall_budget()
            state["generated"] = int(state["generated"]) + 1
            state["next_order"] = order
            state["next_index"] = index + 1
            state["three_edge_connected"] = int(state["three_edge_connected"]) + 1
            outcome, hard = evaluate_graph(graph, order, index)
            if outcome == "timeout":
                assert hard is not None
                queue = list(state["hard_queue"])
                queue.append(hard)
                state["hard_queue"] = queue
            elif outcome == "candidate":
                _atomic_json(state_path, state)
                return state
            if int(state["generated"]) % 10 == 0:
                _atomic_json(state_path, state)
            if wall_expired():
                return pause_for_wall_budget()
        state["next_order"] = order + 1
        state["next_index"] = 0
        _atomic_json(state_path, state)
        if wall_expired() and order < maximum_order:
            return pause_for_wall_budget()
    state["status"] = (
        "complete_with_hard_queue" if state["hard_queue"] else "complete"
    )
    _atomic_json(state_path, state)
    return state


def _parse_shard(value: str | None) -> tuple[int, int] | None:
    if value is None:
        return None
    index, count = (int(item) for item in value.split("/", 1))
    if count <= 0 or not 0 <= index < count:
        raise argparse.ArgumentTypeError("shard must be index/count")
    return index, count


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Exact OPG-348 calibration search.")
    parser.add_argument("--min-order", type=int, default=14)
    parser.add_argument("--max-order", type=int, default=22)
    parser.add_argument("--wall-seconds", type=float, required=True)
    parser.add_argument("--per-graph-seconds", type=float, default=30.0)
    parser.add_argument("--max-states", type=int, default=2_000_000)
    parser.add_argument("--shard", type=_parse_shard)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    result = run_flow_search(
        arguments.min_order,
        arguments.max_order,
        arguments.wall_seconds,
        arguments.per_graph_seconds,
        arguments.max_states,
        arguments.output,
        arguments.shard,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
