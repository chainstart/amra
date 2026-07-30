"""Exact counterexample search for uniform-forest negative association.

The audited source claim ranges over finite simple graphs and two distinct
edges. The local problem-page text omits ``e != f``; dropping that condition
would create trivial false positives. Internal counting accepts loops and
parallel edges because graphic-matroid contraction necessarily creates them,
even though the generated source graphs are simple.
"""

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
    graph_payload,
    implementation_fingerprint,
    locate_tool,
    toolchain_fingerprint,
)


FOREST_CHECKPOINT_SCHEMA = 1


class ForestEvaluationBudgetExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class ForestStatistics:
    """Exact counts for the uniform distribution on all forests of a graph."""

    forest_count: int
    edge_forest_counts: tuple[int, ...]
    pair_forest_counts: tuple[tuple[int, ...], ...]
    states: int
    elapsed_seconds: float


@dataclass(frozen=True)
class ForestPairScore:
    """The edge pair with the greatest exact positive-correlation ratio."""

    edge_pair: tuple[int, int] | None
    forest_count_ef: int
    left_product: int
    right_product: int

    @property
    def margin(self) -> int:
        """Return right-left; a negative value is a counterexample."""

        return self.right_product - self.left_product

    @property
    def violates_negative_association(self) -> bool:
        return self.left_product > self.right_product


def _normalize_edges(
    vertex_count: int, edges: Iterable[tuple[int, int]]
) -> tuple[tuple[int, int], ...]:
    if vertex_count < 0:
        raise ValueError("vertex_count must be non-negative")
    normalized = []
    for left, right in edges:
        if not 0 <= left < vertex_count or not 0 <= right < vertex_count:
            raise ValueError(f"edge {(left, right)} is outside the vertex set")
        normalized.append((min(left, right), max(left, right)))
    return tuple(normalized)


def _canonical_partition(labels: Sequence[int]) -> tuple[int, ...]:
    """Return the restricted-growth encoding of a vertex partition."""

    canonical: dict[int, int] = {}
    result = []
    for label in labels:
        if label not in canonical:
            canonical[label] = len(canonical)
        result.append(canonical[label])
    return tuple(result)


def _merge_partition(
    partition: tuple[int, ...], left: int, right: int
) -> tuple[int, ...] | None:
    left_label = partition[left]
    right_label = partition[right]
    if left_label == right_label:
        return None
    return _canonical_partition(
        left_label if label == right_label else label for label in partition
    )


class GraphicMatroidForestCounter:
    """Count graphic-matroid independent sets by deletion-contraction.

    A state consists of an edge position and a canonical partition of the
    original vertices. Including the next edge contracts its two current
    blocks. If both endpoints are already in one block, the edge is a loop in
    the contracted minor and can only be deleted. Parallel edge identities
    remain in the fixed edge list; after one is included, every later parallel
    edge becomes a loop. Thus loops and parallel edges need no special-case
    graph rewriting.
    """

    def __init__(
        self,
        vertex_count: int,
        edges: Iterable[tuple[int, int]],
        *,
        timeout_seconds: float = 30.0,
        max_states: int = 2_000_000,
    ) -> None:
        if timeout_seconds <= 0:
            raise ForestEvaluationBudgetExceeded(
                "forest recurrence received no positive time budget"
            )
        if max_states <= 0:
            raise ForestEvaluationBudgetExceeded(
                "forest recurrence received no positive state budget"
            )
        self.vertex_count = vertex_count
        self.edges = _normalize_edges(vertex_count, edges)
        degrees = [0] * vertex_count
        multiplicities: dict[tuple[int, int], int] = {}
        for left, right in self.edges:
            if left != right:
                degrees[left] += 1
                degrees[right] += 1
            multiplicities[(left, right)] = (
                multiplicities.get((left, right), 0) + 1
            )
        order = sorted(
            range(len(self.edges)),
            key=lambda index: (
                self.edges[index][0] != self.edges[index][1],
                -multiplicities[self.edges[index]],
                -sum(degrees[vertex] for vertex in self.edges[index]),
                self.edges[index],
                index,
            ),
        )
        self._ordered_edges = tuple(self.edges[index] for index in order)
        self._memo: dict[tuple[int, tuple[int, ...]], int] = {}
        self._max_states = max_states
        self._started = time.monotonic()
        self._deadline = self._started + timeout_seconds
        self._expanded_states = 0

    @property
    def states(self) -> int:
        return self._expanded_states

    @property
    def elapsed_seconds(self) -> float:
        return time.monotonic() - self._started

    def _check_budget(self) -> None:
        if self._expanded_states > self._max_states:
            raise ForestEvaluationBudgetExceeded(
                f"forest recurrence exceeded {self._max_states} states"
            )
        if time.monotonic() >= self._deadline:
            raise ForestEvaluationBudgetExceeded(
                "forest recurrence exceeded its time budget"
            )

    def _visit(self, position: int, partition: tuple[int, ...]) -> int:
        key = (position, partition)
        cached = self._memo.get(key)
        if cached is not None:
            return cached
        self._expanded_states += 1
        if self._expanded_states > self._max_states:
            raise ForestEvaluationBudgetExceeded(
                f"forest recurrence exceeded {self._max_states} states"
            )
        if self._expanded_states == 1 or self._expanded_states % 256 == 0:
            self._check_budget()
        if position == len(self._ordered_edges):
            self._memo[key] = 1
            return 1
        left, right = self._ordered_edges[position]
        deleted = self._visit(position + 1, partition)
        contracted_partition = _merge_partition(partition, left, right)
        if contracted_partition is None:
            value = deleted
        else:
            value = deleted + self._visit(
                position + 1, contracted_partition
            )
        self._memo[key] = value
        return value

    def count_after_contracting(self, edge_indexes: Iterable[int] = ()) -> int:
        """Count forests containing every specified edge.

        Contracting a cyclic set is invalid in the graphic matroid and returns
        zero. Specified edges remain in the fixed list, where they are loops
        and therefore contribute no second choice.
        """

        partition = tuple(range(self.vertex_count))
        seen: set[int] = set()
        for edge_index in edge_indexes:
            if not 0 <= edge_index < len(self.edges):
                raise IndexError(f"edge index {edge_index} is out of range")
            if edge_index in seen:
                continue
            seen.add(edge_index)
            left, right = self.edges[edge_index]
            merged = _merge_partition(partition, left, right)
            if merged is None:
                return 0
            partition = merged
        return self._visit(0, partition)

    def statistics(self) -> ForestStatistics:
        total = self.count_after_contracting()
        edge_counts = tuple(
            self.count_after_contracting((edge,))
            for edge in range(len(self.edges))
        )
        pair_counts = [
            [0] * len(self.edges) for _ in range(len(self.edges))
        ]
        for first, second in combinations(range(len(self.edges)), 2):
            count = self.count_after_contracting((first, second))
            pair_counts[first][second] = count
            pair_counts[second][first] = count
        return ForestStatistics(
            forest_count=total,
            edge_forest_counts=edge_counts,
            pair_forest_counts=tuple(tuple(row) for row in pair_counts),
            states=self.states,
            elapsed_seconds=self.elapsed_seconds,
        )


def exact_forest_statistics(
    vertex_count: int,
    edges: Iterable[tuple[int, int]],
    *,
    timeout_seconds: float = 30.0,
    max_states: int = 2_000_000,
) -> ForestStatistics:
    return GraphicMatroidForestCounter(
        vertex_count,
        edges,
        timeout_seconds=timeout_seconds,
        max_states=max_states,
    ).statistics()


def brute_force_forest_statistics(
    vertex_count: int, edges: Iterable[tuple[int, int]]
) -> ForestStatistics:
    """Independent 2^m oracle, intended only for small regression graphs."""

    normalized = _normalize_edges(vertex_count, edges)
    total = 0
    edge_counts = [0] * len(normalized)
    pair_counts = [
        [0] * len(normalized) for _ in range(len(normalized))
    ]
    started = time.monotonic()
    for selected in range(1 << len(normalized)):
        parent = list(range(vertex_count))

        def find(vertex: int) -> int:
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        present = []
        acyclic = True
        for index, (left, right) in enumerate(normalized):
            if not selected & (1 << index):
                continue
            left_root = find(left)
            right_root = find(right)
            if left_root == right_root:
                acyclic = False
                break
            parent[right_root] = left_root
            present.append(index)
        if not acyclic:
            continue
        total += 1
        for edge in present:
            edge_counts[edge] += 1
        for first, second in combinations(present, 2):
            pair_counts[first][second] += 1
            pair_counts[second][first] += 1
    return ForestStatistics(
        forest_count=total,
        edge_forest_counts=tuple(edge_counts),
        pair_forest_counts=tuple(tuple(row) for row in pair_counts),
        states=1 << len(normalized),
        elapsed_seconds=time.monotonic() - started,
    )


def strongest_edge_pair(statistics: ForestStatistics) -> ForestPairScore:
    best_pair: tuple[int, int] | None = None
    best_pair_count = 0
    best_left = 0
    best_right = 0
    for first, second in combinations(
        range(len(statistics.edge_forest_counts)), 2
    ):
        pair_count = statistics.pair_forest_counts[first][second]
        left = statistics.forest_count * pair_count
        right = (
            statistics.edge_forest_counts[first]
            * statistics.edge_forest_counts[second]
        )
        if right == 0:
            continue
        if best_pair is None or left * best_right > best_left * right:
            best_pair = (first, second)
            best_pair_count = pair_count
            best_left = left
            best_right = right
    return ForestPairScore(
        edge_pair=best_pair,
        forest_count_ef=best_pair_count,
        left_product=best_left,
        right_product=best_right,
    )


def iter_connected_simple_graphs(
    order: int,
    minimum_edges: int,
    maximum_edges: int,
    shard: tuple[int, int] | None = None,
) -> Iterator[EdgeGraph]:
    """Yield the connected graph6 catalogue slice from nauty geng.

    Restricting to connected graphs is sound for counterexample discovery:
    forest choices factor across components. Edges in different components
    are independent, while a same-component pair has exactly the correlation
    it has inside that component.
    """

    geng = str(locate_tool("geng"))
    command = [
        geng,
        "-q",
        "-c",
        str(order),
        f"{minimum_edges}:{maximum_edges}",
    ]
    if shard:
        command.append(f"{shard[0]}/{shard[1]}")
    yield from (decode_graph6(line) for line in _pipeline((command,)))


def _better_pair_event(
    candidate: dict[str, object], incumbent: object
) -> bool:
    if not isinstance(incumbent, dict):
        return True
    left = int(candidate["left_product"])
    right = int(candidate["right_product"])
    old_left = int(incumbent["left_product"])
    old_right = int(incumbent["right_product"])
    return left * old_right > old_left * right


def run_uniform_forest_search(
    order: int,
    minimum_edges: int,
    maximum_edges: int,
    wall_seconds: float,
    per_graph_seconds: float,
    max_states: int,
    output: Path,
    shard: tuple[int, int] | None = None,
    *,
    max_cases: int = 0,
    checkpoint_every: int = 25,
) -> dict[str, object]:
    if not 0 <= minimum_edges <= maximum_edges <= order * (order - 1) // 2:
        raise ValueError("invalid edge range for the requested graph order")
    if wall_seconds < 0 or per_graph_seconds <= 0 or max_states <= 0:
        raise ValueError("search budgets must be positive")
    if max_cases < 0 or checkpoint_every <= 0:
        raise ValueError(
            "max_cases must be non-negative and checkpoint_every positive"
        )

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
    identity = {
        "order": order,
        "minimum_edges": minimum_edges,
        "maximum_edges": maximum_edges,
        "shard": list(shard) if shard else None,
        "implementation_sha256": fingerprint,
        "toolchain": tools,
    }
    state: dict[str, object] = {
        "checkpoint_schema": FOREST_CHECKPOINT_SCHEMA,
        **identity,
        "problem": "opg1757",
        "connected_only": True,
        "next_index": 0,
        "generated": 0,
        "evaluated": 0,
        "nonviolating": 0,
        "violations": 0,
        "timeouts": 0,
        "hard_queue": [],
        "best_pair": None,
        "status": "running",
    }
    if state_path.exists():
        loaded = json.loads(state_path.read_text(encoding="utf-8"))
        if loaded.get("checkpoint_schema") != FOREST_CHECKPOINT_SCHEMA:
            raise ValueError("legacy checkpoint requires a new output directory")
        for field, expected in identity.items():
            if loaded.get(field) != expected:
                raise ValueError(f"checkpoint {field} does not match")
        state.update(loaded)
        if (
            state.get("candidate") is not None
            or int(state["violations"]) > 0
            or candidate_path.exists()
        ):
            if state.get("candidate") is None and candidate_path.exists():
                state["candidate"] = json.loads(
                    candidate_path.read_text(encoding="utf-8")
                )
            state["violations"] = max(1, int(state["violations"]))
            state["status"] = "candidate_pending_independent_verification"
            _atomic_json(state_path, state)
            return state
        if state.get("status") == "complete" and not state["hard_queue"]:
            return state
        state["status"] = "running"
    else:
        _atomic_json(state_path, state)

    deadline = time.monotonic() + wall_seconds
    cases_this_run = 0

    def budget_exhausted() -> bool:
        return time.monotonic() >= deadline or (
            max_cases > 0 and cases_this_run >= max_cases
        )

    def pause() -> dict[str, object]:
        state["status"] = (
            "paused_case_budget"
            if max_cases > 0 and cases_this_run >= max_cases
            else "paused_wall_budget"
        )
        _atomic_json(state_path, state)
        return state

    def evaluate_graph(
        graph: EdgeGraph, index: int, *, retry: bool = False
    ) -> tuple[str, dict[str, object] | None]:
        nonlocal cases_this_run
        cases_this_run += 1
        event: dict[str, object] = {
            "time": time.time(),
            "index": index,
            "graph6": graph.encoding,
            "vertices": graph.vertex_count,
            "edges": len(graph.edges),
        }
        if retry:
            event["retry"] = True
        remaining = max(0.0, deadline - time.monotonic())
        try:
            statistics = exact_forest_statistics(
                graph.vertex_count,
                graph.edges,
                timeout_seconds=min(per_graph_seconds, remaining),
                max_states=max_states,
            )
        except ForestEvaluationBudgetExceeded as error:
            state["timeouts"] = int(state["timeouts"]) + 1
            hard = {"index": index, "graph6": graph.encoding}
            event.update({"status": "timeout", "error": str(error)})
            outcome = "timeout"
        else:
            hard = None
            score = strongest_edge_pair(statistics)
            pair = score.edge_pair
            pair_event: dict[str, object] | None = None
            if pair is not None:
                first, second = pair
                pair_event = {
                    "edge_indexes": [first, second],
                    "edge_e": list(graph.edges[first]),
                    "edge_f": list(graph.edges[second]),
                    "forest_count": statistics.forest_count,
                    "forest_count_e": statistics.edge_forest_counts[first],
                    "forest_count_f": statistics.edge_forest_counts[second],
                    "forest_count_ef": score.forest_count_ef,
                    "left_product": score.left_product,
                    "right_product": score.right_product,
                    "margin": score.margin,
                }
                if _better_pair_event(pair_event, state.get("best_pair")):
                    state["best_pair"] = {
                        "index": index,
                        "graph6": graph.encoding,
                        **pair_event,
                    }
            event.update(
                {
                    "status": (
                        "violation"
                        if score.violates_negative_association
                        else "nonviolating"
                    ),
                    "states": statistics.states,
                    "elapsed_seconds": statistics.elapsed_seconds,
                    "strongest_pair": pair_event,
                }
            )
            state["evaluated"] = int(state["evaluated"]) + 1
            if score.violates_negative_association:
                state["violations"] = int(state["violations"]) + 1
                candidate = {
                    "problem": "opg1757",
                    "semantic_scope": (
                        "finite simple connected graph and two distinct edges"
                    ),
                    "graph": graph_payload(graph),
                    "evaluation": event,
                    "verification_status": (
                        "pending_independent_bruteforce_or_second_recurrence"
                    ),
                }
                _atomic_json(candidate_path, candidate)
                state["candidate"] = candidate
                state["status"] = (
                    "candidate_pending_independent_verification"
                )
                outcome = "candidate"
            else:
                state["nonviolating"] = int(state["nonviolating"]) + 1
                outcome = "nonviolating"
        with events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
        return outcome, hard

    if budget_exhausted():
        return pause()

    pending_hard = list(state["hard_queue"])
    retained_hard: list[object] = []
    for position, raw_hard in enumerate(pending_hard):
        if budget_exhausted():
            state["hard_queue"] = retained_hard + pending_hard[position:]
            return pause()
        hard = dict(raw_hard)
        graph = decode_graph6(str(hard["graph6"]))
        outcome, _ = evaluate_graph(
            graph, int(hard["index"]), retry=True
        )
        if outcome == "timeout":
            retained_hard.append(hard)
        state["hard_queue"] = retained_hard + pending_hard[position + 1 :]
        _atomic_json(state_path, state)
        if outcome == "candidate":
            return state
    state["hard_queue"] = retained_hard

    start = int(state["next_index"])
    for index, graph in enumerate(
        iter_connected_simple_graphs(
            order, minimum_edges, maximum_edges, shard
        )
    ):
        if index < start:
            if budget_exhausted():
                return pause()
            continue
        if budget_exhausted():
            return pause()
        state["generated"] = int(state["generated"]) + 1
        outcome, hard = evaluate_graph(graph, index)
        state["next_index"] = index + 1
        if outcome == "timeout":
            assert hard is not None
            queue = list(state["hard_queue"])
            queue.append(hard)
            state["hard_queue"] = queue
        elif outcome == "candidate":
            _atomic_json(state_path, state)
            return state
        if int(state["generated"]) % checkpoint_every == 0:
            _atomic_json(state_path, state)
        if budget_exhausted():
            return pause()

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
    parser = argparse.ArgumentParser(
        description=(
            "Exact deletion-contraction search for OPG-1757 uniform-forest "
            "negative association."
        )
    )
    parser.add_argument("--order", type=int, default=9)
    parser.add_argument("--min-edges", type=int, default=19)
    parser.add_argument("--max-edges", type=int, default=36)
    parser.add_argument("--wall-seconds", type=float, required=True)
    parser.add_argument("--per-graph-seconds", type=float, default=30.0)
    parser.add_argument("--max-states", type=int, default=2_000_000)
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--checkpoint-every", type=int, default=25)
    parser.add_argument("--shard", type=_parse_shard)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    result = run_uniform_forest_search(
        arguments.order,
        arguments.min_edges,
        arguments.max_edges,
        arguments.wall_seconds,
        arguments.per_graph_seconds,
        arguments.max_states,
        arguments.output,
        arguments.shard,
        max_cases=arguments.max_cases,
        checkpoint_every=arguments.checkpoint_every,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
