"""Read-only strict-pair analysis for the OPG-1757 search.

The production search records the maximum ratio

    (#F * #F_ef) / (#F_e * #F_f).

Pairs from different graphic-matroid blocks are structurally independent and
have ratio exactly one. Such an equality permanently dominates every
informative pair for which negative association is strict. This helper leaves
the production runner untouched and ranks only strict pairs, using exact
integer cross-products rather than floating-point comparisons.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from decimal import Decimal, localcontext
from functools import cmp_to_key
from pathlib import Path
from typing import Iterator, Sequence

from amra.discovery.opg_coloring_search import (
    EdgeGraph,
    _pipeline,
    decode_graph6,
    locate_tool,
)
from amra.discovery.opg_uniform_forest_search import exact_forest_statistics


@dataclass(frozen=True)
class StrictPair:
    first: int
    second: int
    forest_count_e: int
    forest_count_f: int
    forest_count_ef: int
    left_product: int
    right_product: int

    @property
    def margin(self) -> int:
        return self.right_product - self.left_product


def biconnected_edge_blocks(graph: EdgeGraph) -> tuple[int, ...]:
    """Return Tarjan edge-block labels for a finite simple graph."""

    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(graph.vertex_count)
    ]
    for edge, (left, right) in enumerate(graph.edges):
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))

    discovery = [-1] * graph.vertex_count
    low = [0] * graph.vertex_count
    stack: list[int] = []
    blocks: list[list[int]] = []
    clock = 0

    def visit(vertex: int, parent_edge: int) -> None:
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        for other, edge in adjacency[vertex]:
            if edge == parent_edge:
                continue
            if discovery[other] < 0:
                stack.append(edge)
                visit(other, edge)
                low[vertex] = min(low[vertex], low[other])
                if low[other] >= discovery[vertex]:
                    block = []
                    while stack:
                        popped = stack.pop()
                        block.append(popped)
                        if popped == edge:
                            break
                    blocks.append(block)
            elif discovery[other] < discovery[vertex]:
                stack.append(edge)
                low[vertex] = min(low[vertex], discovery[other])

    for root in range(graph.vertex_count):
        if discovery[root] >= 0:
            continue
        visit(root, -1)
        if stack:
            blocks.append(list(reversed(stack)))
            stack.clear()

    labels = [-1] * len(graph.edges)
    for block, edge_indexes in enumerate(blocks):
        for edge in edge_indexes:
            if labels[edge] >= 0:
                raise RuntimeError("an edge appeared in two biconnected blocks")
            labels[edge] = block
    if any(label < 0 for label in labels):
        raise RuntimeError("the edge-block decomposition lost an edge")
    return tuple(labels)


def _compare_strict_pairs(left: StrictPair, right: StrictPair) -> int:
    """Sort decreasing by exact left/right ratio."""

    comparison = (
        left.left_product * right.right_product
        - right.left_product * left.right_product
    )
    if comparison:
        return -1 if comparison > 0 else 1
    if left.margin != right.margin:
        return -1 if left.margin < right.margin else 1
    return -1 if (left.first, left.second) < (right.first, right.second) else (
        1
        if (left.first, left.second) > (right.first, right.second)
        else 0
    )


def _compare_pair_records(
    left: dict[str, object], right: dict[str, object]
) -> int:
    """Sort cross-graph pair records by an exact integer ratio comparison."""

    left_numerator = int(left["left_product"])
    left_denominator = int(left["right_product"])
    right_numerator = int(right["left_product"])
    right_denominator = int(right["right_product"])
    comparison = (
        left_numerator * right_denominator
        - right_numerator * left_denominator
    )
    if comparison:
        return -1 if comparison > 0 else 1
    left_identity = (
        int(left["margin"]),
        int(left["index"]),
        str(left["graph6"]),
        tuple(int(item) for item in left["edge_indexes"]),
    )
    right_identity = (
        int(right["margin"]),
        int(right["index"]),
        str(right["graph6"]),
        tuple(int(item) for item in right["edge_indexes"]),
    )
    return -1 if left_identity < right_identity else (
        1 if left_identity > right_identity else 0
    )


def _decimal_ratio(numerator: int, denominator: int) -> str:
    with localcontext() as context:
        context.prec = 24
        return format(Decimal(numerator) / Decimal(denominator), ".20f")


def analyze_strict_pairs(
    graph: EdgeGraph,
    *,
    top_k: int = 10,
    timeout_seconds: float = 30.0,
    max_states: int = 2_000_000,
) -> dict[str, object]:
    if top_k < 0:
        raise ValueError("top_k must be non-negative")
    statistics = exact_forest_statistics(
        graph.vertex_count,
        graph.edges,
        timeout_seconds=timeout_seconds,
        max_states=max_states,
    )
    block_labels = biconnected_edge_blocks(graph)
    equality_pairs = 0
    structural_equality_pairs = 0
    within_block_equality_pairs = 0
    violations = 0
    strict: list[StrictPair] = []

    for first in range(len(graph.edges)):
        for second in range(first + 1, len(graph.edges)):
            pair_count = statistics.pair_forest_counts[first][second]
            left = statistics.forest_count * pair_count
            right = (
                statistics.edge_forest_counts[first]
                * statistics.edge_forest_counts[second]
            )
            if left == right:
                equality_pairs += 1
                if block_labels[first] != block_labels[second]:
                    structural_equality_pairs += 1
                else:
                    within_block_equality_pairs += 1
                continue
            if left > right:
                violations += 1
                continue
            strict.append(
                StrictPair(
                    first=first,
                    second=second,
                    forest_count_e=statistics.edge_forest_counts[first],
                    forest_count_f=statistics.edge_forest_counts[second],
                    forest_count_ef=pair_count,
                    left_product=left,
                    right_product=right,
                )
            )

    strict.sort(key=cmp_to_key(_compare_strict_pairs))
    top_pairs = []
    for pair in strict[:top_k]:
        top_pairs.append(
            {
                "edge_indexes": [pair.first, pair.second],
                "edge_e": list(graph.edges[pair.first]),
                "edge_f": list(graph.edges[pair.second]),
                "block_ids": [
                    block_labels[pair.first],
                    block_labels[pair.second],
                ],
                "forest_count": statistics.forest_count,
                "forest_count_e": pair.forest_count_e,
                "forest_count_f": pair.forest_count_f,
                "forest_count_ef": pair.forest_count_ef,
                "left_product": pair.left_product,
                "right_product": pair.right_product,
                "margin": pair.margin,
                "left_over_right": _decimal_ratio(
                    pair.left_product, pair.right_product
                ),
                "relative_gap": _decimal_ratio(
                    pair.margin, pair.right_product
                ),
            }
        )

    pair_count = len(graph.edges) * (len(graph.edges) - 1) // 2
    return {
        "graph6": graph.encoding,
        "vertices": graph.vertex_count,
        "edges": len(graph.edges),
        "edge_block_count": len(set(block_labels)),
        "pair_count": pair_count,
        "strict_pair_count": len(strict),
        "equality_pair_count": equality_pairs,
        "structural_equality_pair_count": structural_equality_pairs,
        "within_block_equality_pair_count": within_block_equality_pairs,
        "violation_pair_count": violations,
        "states": statistics.states,
        "elapsed_seconds": statistics.elapsed_seconds,
        "top_strict_pairs": top_pairs,
    }


def iter_biconnected_simple_graphs(
    order: int,
    minimum_edges: int,
    maximum_edges: int,
    shard: tuple[int, int] | None = None,
) -> Iterator[EdgeGraph]:
    geng = str(locate_tool("geng"))
    command = [
        geng,
        "-q",
        "-C",
        str(order),
        f"{minimum_edges}:{maximum_edges}",
    ]
    if shard:
        command.append(f"{shard[0]}/{shard[1]}")
    yield from (decode_graph6(line) for line in _pipeline((command,)))


def analyze_biconnected_sample(
    order: int,
    minimum_edges: int,
    maximum_edges: int,
    *,
    max_cases: int,
    top_k: int,
    timeout_seconds: float,
    max_states: int,
    shard: tuple[int, int] | None = None,
) -> dict[str, object]:
    if max_cases <= 0:
        raise ValueError("max_cases must be positive for a bounded sample")
    analyses = []
    for index, graph in enumerate(
        iter_biconnected_simple_graphs(
            order, minimum_edges, maximum_edges, shard
        )
    ):
        if index >= max_cases:
            break
        analyses.append(
            {
                "index": index,
                **analyze_strict_pairs(
                    graph,
                    top_k=top_k,
                    timeout_seconds=timeout_seconds,
                    max_states=max_states,
                ),
            }
        )
    # Per-graph top_k is sufficient for a global top_k: a pair below rank k
    # already has k pairs from its own graph ranked ahead of it.
    global_candidates = [
        {
            "index": int(graph["index"]),
            "graph6": str(graph["graph6"]),
            "graph_pair_rank": pair_rank,
            **pair,
        }
        for graph in analyses
        for pair_rank, pair in enumerate(graph["top_strict_pairs"], start=1)
    ]
    global_candidates.sort(key=cmp_to_key(_compare_pair_records))
    return {
        "mode": "bounded_biconnected_sample",
        "order": order,
        "minimum_edges": minimum_edges,
        "maximum_edges": maximum_edges,
        "shard": list(shard) if shard else None,
        "max_cases": max_cases,
        "analyzed_cases": len(analyses),
        "equality_pair_count": sum(
            int(item["equality_pair_count"]) for item in analyses
        ),
        "structural_equality_pair_count": sum(
            int(item["structural_equality_pair_count"]) for item in analyses
        ),
        "within_block_equality_pair_count": sum(
            int(item["within_block_equality_pair_count"]) for item in analyses
        ),
        "violation_pair_count": sum(
            int(item["violation_pair_count"]) for item in analyses
        ),
        "global_top_strict_pairs": global_candidates[:top_k],
        "graphs": analyses,
    }


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
            "Read-only exact top-k analysis of strictly negatively associated "
            "edge pairs for OPG-1757."
        )
    )
    parser.add_argument("--graph6")
    parser.add_argument("--order", type=int)
    parser.add_argument("--min-edges", type=int)
    parser.add_argument("--max-edges", type=int)
    parser.add_argument("--max-cases", type=int, default=10)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--per-graph-seconds", type=float, default=30.0)
    parser.add_argument("--max-states", type=int, default=2_000_000)
    parser.add_argument("--shard", type=_parse_shard)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(argv)

    if arguments.graph6:
        if arguments.order is not None:
            parser.error("--graph6 and --order are mutually exclusive")
        result = {
            "mode": "single_graph",
            **analyze_strict_pairs(
                decode_graph6(arguments.graph6),
                top_k=arguments.top_k,
                timeout_seconds=arguments.per_graph_seconds,
                max_states=arguments.max_states,
            ),
        }
    else:
        if arguments.order is None:
            parser.error("provide either --graph6 or --order")
        maximum_possible = arguments.order * (arguments.order - 1) // 2
        minimum_edges = (
            arguments.min_edges
            if arguments.min_edges is not None
            else arguments.order
        )
        maximum_edges = (
            arguments.max_edges
            if arguments.max_edges is not None
            else maximum_possible
        )
        if not 0 <= minimum_edges <= maximum_edges <= maximum_possible:
            parser.error("invalid edge range")
        result = analyze_biconnected_sample(
            arguments.order,
            minimum_edges,
            maximum_edges,
            max_cases=arguments.max_cases,
            top_k=arguments.top_k,
            timeout_seconds=arguments.per_graph_seconds,
            max_states=arguments.max_states,
            shard=arguments.shard,
        )

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
