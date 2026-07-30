#!/usr/bin/env python3
"""Independent exact searches for OPG-1757 transformation closures.

This file deliberately does not import AMRA's production forest counter.  It
uses a small deletion--contraction dynamic program on canonical vertex
partitions and the cached nauty ``geng`` binary only as a graph catalogue.

The central observation used by ``weighted`` is that replacing one edge by a
two-terminal series/parallel gadget changes only that edge's activity.  For
three distinct edges e,a,b, the a,b negative-correlation margin is therefore
a quadratic polynomial in the activity of e.  We certify its sign on the
whole positive half-line, rather than sampling a few gadget sizes.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import subprocess
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator, Sequence


DEFAULT_GENG = Path(
    "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/bin/nauty-geng"
)


def canonical_partition(labels: Sequence[int]) -> tuple[int, ...]:
    relabel: dict[int, int] = {}
    answer: list[int] = []
    for label in labels:
        answer.append(relabel.setdefault(label, len(relabel)))
    return tuple(answer)


def merge_partition(
    partition: tuple[int, ...], left: int, right: int
) -> tuple[int, ...] | None:
    a = partition[left]
    b = partition[right]
    if a == b:
        return None
    return canonical_partition(a if label == b else label for label in partition)


@dataclass(frozen=True)
class Graph:
    order: int
    edges: tuple[tuple[int, int], ...]
    graph6: str = ""

    def __post_init__(self) -> None:
        if len(set(self.edges)) != len(self.edges):
            raise ValueError("duplicate edge")
        if any(not (0 <= u < v < self.order) for u, v in self.edges):
            raise ValueError("edges must be normalized, simple, and in range")


def decode_graph6(line: str) -> Graph:
    """Decode the compact graph6 form used here (orders at most 62)."""

    line = line.strip()
    if not line or line[0] == "~":
        raise ValueError("only compact graph6 orders at most 62 are supported")
    order = ord(line[0]) - 63
    needed = order * (order - 1) // 2
    bits: list[int] = []
    for char in line[1:]:
        value = ord(char) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(bits) < needed or any(bits[needed:]):
        raise ValueError("invalid graph6 payload length or padding")
    pairs = (
        (left, right)
        for right in range(1, order)
        for left in range(right)
    )
    edges = tuple(pair for pair, bit in zip(pairs, bits) if bit)
    return Graph(order, edges, line)


def iter_connected_graphs(
    order: int,
    *,
    shard: tuple[int, int] | None = None,
    geng: Path = DEFAULT_GENG,
) -> Iterator[Graph]:
    command = [
        str(geng),
        "-q",
        "-c",
        str(order),
        f"{max(0, order - 1)}:{order * (order - 1) // 2}",
    ]
    if shard is not None:
        command.append(f"{shard[0]}/{shard[1]}")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={
            **os.environ,
            "LD_LIBRARY_PATH": ":".join(
                (
                    "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/lib",
                    "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/lib/"
                    "x86_64-linux-gnu",
                    os.environ.get("LD_LIBRARY_PATH", ""),
                )
            ),
        },
    )
    assert process.stdout is not None
    for line in process.stdout:
        if line.strip():
            yield decode_graph6(line)
    _, stderr = process.communicate()
    if process.returncode:
        raise RuntimeError(f"geng failed with code {process.returncode}: {stderr}")


class ForestCounter:
    """Count forests containing forced edge identities exactly."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        degrees = [0] * graph.order
        for u, v in graph.edges:
            degrees[u] += 1
            degrees[v] += 1
        self.ordered_edges = tuple(
            sorted(
                graph.edges,
                key=lambda edge: (
                    -(degrees[edge[0]] + degrees[edge[1]]),
                    edge,
                ),
            )
        )
        self.memo: dict[tuple[int, tuple[int, ...]], int] = {}

    def visit(self, position: int, partition: tuple[int, ...]) -> int:
        key = (position, partition)
        cached = self.memo.get(key)
        if cached is not None:
            return cached
        if position == len(self.ordered_edges):
            self.memo[key] = 1
            return 1
        u, v = self.ordered_edges[position]
        answer = self.visit(position + 1, partition)
        merged = merge_partition(partition, u, v)
        if merged is not None:
            answer += self.visit(position + 1, merged)
        self.memo[key] = answer
        return answer

    def count(self, forced: Iterable[int] = ()) -> int:
        partition = tuple(range(self.graph.order))
        seen: set[int] = set()
        for index in forced:
            if index in seen:
                continue
            seen.add(index)
            u, v = self.graph.edges[index]
            merged = merge_partition(partition, u, v)
            if merged is None:
                return 0
            partition = merged
        return self.visit(0, partition)


class WeightedForestCounter:
    """Evaluate the multivariate forest polynomial and its derivatives."""

    def __init__(self, graph: Graph, weights: Sequence[float]) -> None:
        if len(weights) != len(graph.edges):
            raise ValueError("one positive weight is required per edge")
        if any(not math.isfinite(weight) or weight <= 0 for weight in weights):
            raise ValueError("weights must be finite and positive")
        self.graph = graph
        self.weights = tuple(float(weight) for weight in weights)
        degrees = [0] * graph.order
        for u, v in graph.edges:
            degrees[u] += 1
            degrees[v] += 1
        order = sorted(
            range(len(graph.edges)),
            key=lambda index: (
                -(degrees[graph.edges[index][0]] + degrees[graph.edges[index][1]]),
                graph.edges[index],
            ),
        )
        self.ordered = tuple(
            (graph.edges[index], self.weights[index]) for index in order
        )
        self.memo: dict[tuple[int, tuple[int, ...]], float] = {}

    def visit(self, position: int, partition: tuple[int, ...]) -> float:
        key = (position, partition)
        cached = self.memo.get(key)
        if cached is not None:
            return cached
        if position == len(self.ordered):
            self.memo[key] = 1.0
            return 1.0
        (u, v), weight = self.ordered[position]
        answer = self.visit(position + 1, partition)
        merged = merge_partition(partition, u, v)
        if merged is not None:
            answer += weight * self.visit(position + 1, merged)
        self.memo[key] = answer
        return answer

    def derivative(self, forced: Iterable[int] = ()) -> float:
        partition = tuple(range(self.graph.order))
        seen: set[int] = set()
        for index in forced:
            if index in seen:
                continue
            seen.add(index)
            u, v = self.graph.edges[index]
            merged = merge_partition(partition, u, v)
            if merged is None:
                return 0.0
            partition = merged
        # The forced edge is encountered as a loop in ``visit`` and therefore
        # contributes no weight.  The returned value is the corresponding
        # partial derivative, exactly as required by the Rayleigh difference.
        return self.visit(0, partition)


def weighted_all_pair_log_ratios(
    graph: Graph, weights: Sequence[float]
) -> tuple[float, tuple[int, int] | None, dict[str, float]]:
    """Return max log(Z Z_ef / (Z_e Z_f)); positive means a violation."""

    counter = WeightedForestCounter(graph, weights)
    total = counter.derivative()
    singles = tuple(
        counter.derivative((edge,)) for edge in range(len(graph.edges))
    )
    best = -math.inf
    best_pair: tuple[int, int] | None = None
    best_counts: dict[str, float] = {}
    for a, b in combinations(range(len(graph.edges)), 2):
        both = counter.derivative((a, b))
        if both <= 0 or singles[a] <= 0 or singles[b] <= 0:
            continue
        log_ratio = (
            math.log(total)
            + math.log(both)
            - math.log(singles[a])
            - math.log(singles[b])
        )
        if log_ratio > best:
            best = log_ratio
            best_pair = (a, b)
            best_counts = {
                "forest_polynomial": total,
                "derivative_a": singles[a],
                "derivative_b": singles[b],
                "derivative_ab": both,
            }
    return best, best_pair, best_counts


@dataclass(frozen=True)
class PairAudit:
    total: int
    single: tuple[int, ...]
    pair: dict[tuple[int, int], int]
    minimum_margin: int | None
    violation: dict[str, object] | None


def audit_all_pairs(graph: Graph) -> PairAudit:
    counter = ForestCounter(graph)
    total = counter.count()
    single = tuple(counter.count((edge,)) for edge in range(len(graph.edges)))
    pair: dict[tuple[int, int], int] = {}
    minimum: int | None = None
    violation = None
    for a, b in combinations(range(len(graph.edges)), 2):
        both = counter.count((a, b))
        pair[a, b] = both
        margin = single[a] * single[b] - total * both
        if minimum is None or margin < minimum:
            minimum = margin
        if margin < 0 and violation is None:
            violation = {
                "edge_indexes": [a, b],
                "edges": [list(graph.edges[a]), list(graph.edges[b])],
                "forest_count": total,
                "forest_count_a": single[a],
                "forest_count_b": single[b],
                "forest_count_ab": both,
                "margin": margin,
            }
    return PairAudit(total, single, pair, minimum, violation)


def weighted_margin_polynomial(
    counter: ForestCounter,
    total: int,
    single: Sequence[int],
    pair: dict[tuple[int, int], int],
    e: int,
    a: int,
    b: int,
) -> tuple[int, int, int]:
    """Return d0,d1,d2 for Delta_ab when edge e has activity t."""

    def pair_count(i: int, j: int) -> int:
        return pair[min(i, j), max(i, j)]

    e_count = single[e]
    a1 = pair_count(a, e)
    a0 = single[a] - a1
    b1 = pair_count(b, e)
    b0 = single[b] - b1
    c1 = counter.count((a, b, e))
    c0 = pair_count(a, b) - c1
    z1 = e_count
    z0 = total - e_count
    return (
        a0 * b0 - z0 * c0,
        a0 * b1 + a1 * b0 - z0 * c1 - z1 * c0,
        a1 * b1 - z1 * c1,
    )


def positive_half_line_certificate(
    polynomial: tuple[int, int, int]
) -> tuple[bool, dict[str, object]]:
    """Certify d0+d1*t+d2*t^2 >= 0 for every real t >= 0."""

    d0, d1, d2 = polynomial
    if d0 < 0:
        return False, {"reason": "negative_at_zero", "value": d0}
    if d2 < 0:
        return False, {"reason": "negative_leading_coefficient", "value": d2}
    if d2 == 0:
        if d1 < 0:
            return False, {"reason": "negative_linear_slope", "value": d1}
        return True, {"reason": "nonnegative_linear_coefficients"}
    if d1 >= 0:
        return True, {"reason": "minimum_at_zero"}
    discriminant_slack = 4 * d0 * d2 - d1 * d1
    return (
        discriminant_slack >= 0,
        {
            "reason": "interior_vertex",
            "four_d0_d2_minus_d1_squared": discriminant_slack,
            "vertex": str(Fraction(-d1, 2 * d2)),
        },
    )


def gadget_grid_witness(
    polynomial: tuple[int, int, int],
    *,
    max_path_length: int = 40,
    max_parallel_paths: int = 100_000,
) -> dict[str, object] | None:
    d0, d1, d2 = polynomial

    def value(activity: Fraction) -> Fraction:
        return d0 + d1 * activity + d2 * activity * activity

    for length in range(2, max_path_length + 1):
        activity = Fraction(1, 2**length - 1)
        margin = value(activity)
        if margin < 0:
            return {
                "kind": "series_path_replacing_e",
                "path_length": length,
                "activity": str(activity),
                "weighted_margin": str(margin),
            }
    for paths in range(1, max_parallel_paths + 1):
        activity = Fraction(3 + paths, 3)
        margin = value(activity)
        if margin < 0:
            return {
                "kind": "parallel_length_two_paths_retaining_e",
                "parallel_paths": paths,
                "activity": str(activity),
                "weighted_margin": str(margin),
            }
    return None


def weighted_scan(args: argparse.Namespace) -> dict[str, object]:
    shard = (args.shard_index, args.shard_count)
    started = time.monotonic()
    graph_count = 0
    triple_count = 0
    base_violations = 0
    half_line_failures: list[dict[str, object]] = []
    gadget_failures: list[dict[str, object]] = []
    certificate_reasons: dict[str, int] = {}
    for graph in iter_connected_graphs(args.order, shard=shard, geng=args.geng):
        graph_count += 1
        audit = audit_all_pairs(graph)
        if audit.violation is not None:
            base_violations += 1
            if len(half_line_failures) < args.keep:
                half_line_failures.append(
                    {
                        "kind": "base_uniform_violation",
                        "graph6": graph.graph6,
                        "violation": audit.violation,
                    }
                )
            continue
        counter = ForestCounter(graph)
        total = counter.count()
        single = tuple(counter.count((i,)) for i in range(len(graph.edges)))
        pair = {
            (a, b): counter.count((a, b))
            for a, b in combinations(range(len(graph.edges)), 2)
        }
        for e in range(len(graph.edges)):
            others = [i for i in range(len(graph.edges)) if i != e]
            for a, b in combinations(others, 2):
                triple_count += 1
                polynomial = weighted_margin_polynomial(
                    counter, total, single, pair, e, a, b
                )
                certified, detail = positive_half_line_certificate(polynomial)
                reason = str(detail["reason"])
                certificate_reasons[reason] = certificate_reasons.get(reason, 0) + 1
                if not certified and len(half_line_failures) < args.keep:
                    failure = {
                        "graph6": graph.graph6,
                        "edges": [list(edge) for edge in graph.edges],
                        "weighted_edge_index": e,
                        "weighted_edge": list(graph.edges[e]),
                        "tested_edge_indexes": [a, b],
                        "tested_edges": [list(graph.edges[a]), list(graph.edges[b])],
                        "polynomial": list(polynomial),
                        "failure": detail,
                    }
                    half_line_failures.append(failure)
                    witness = gadget_grid_witness(
                        polynomial,
                        max_path_length=args.max_path_length,
                        max_parallel_paths=args.max_parallel_paths,
                    )
                    if witness is not None and len(gadget_failures) < args.keep:
                        gadget_failures.append({**failure, "gadget_witness": witness})
        if args.progress_every and graph_count % args.progress_every == 0:
            print(
                f"weighted progress graphs={graph_count} triples={triple_count}",
                file=sys.stderr,
                flush=True,
            )
        if args.max_graphs and graph_count >= args.max_graphs:
            break
    return {
        "mode": "weighted",
        "order": args.order,
        "shard": list(shard),
        "graphs": graph_count,
        "edge_triples": triple_count,
        "base_uniform_violations": base_violations,
        "positive_half_line_failures": len(half_line_failures),
        "gadget_grid_failures": len(gadget_failures),
        "certificate_reasons": certificate_reasons,
        "failure_records": half_line_failures,
        "gadget_failure_records": gadget_failures,
        "elapsed_seconds": time.monotonic() - started,
    }


def add_false_twin(graph: Graph, vertex: int) -> Graph:
    neighbours = {
        v if u == vertex else u
        for u, v in graph.edges
        if u == vertex or v == vertex
    }
    new_vertex = graph.order
    added = tuple(sorted((min(new_vertex, w), max(new_vertex, w)) for w in neighbours))
    return Graph(graph.order + 1, tuple(sorted(graph.edges + added)))


def add_leaf(graph: Graph, vertex: int) -> Graph:
    new_vertex = graph.order
    return Graph(
        graph.order + 1,
        tuple(sorted(graph.edges + ((min(vertex, new_vertex), max(vertex, new_vertex)),))),
    )


def add_parallel_two_path(graph: Graph, edge_index: int) -> Graph:
    u, v = graph.edges[edge_index]
    new_vertex = graph.order
    return Graph(
        graph.order + 1,
        tuple(sorted(graph.edges + ((u, new_vertex), (v, new_vertex)))),
    )


def subdivide_edge(graph: Graph, edge_index: int) -> Graph:
    u, v = graph.edges[edge_index]
    new_vertex = graph.order
    remaining = graph.edges[:edge_index] + graph.edges[edge_index + 1 :]
    return Graph(
        graph.order + 1,
        tuple(sorted(remaining + ((u, new_vertex), (v, new_vertex)))),
    )


def direct_transform_scan(args: argparse.Namespace) -> dict[str, object]:
    operations = {
        "false_twin": lambda graph, index: add_false_twin(graph, index),
        "leaf": lambda graph, index: add_leaf(graph, index),
        "parallel_two_path": lambda graph, index: add_parallel_two_path(graph, index),
        "subdivide_edge": lambda graph, index: subdivide_edge(graph, index),
    }
    operation = operations[args.operation]
    index_kind = "vertex" if args.operation in {"false_twin", "leaf"} else "edge"
    started = time.monotonic()
    bases = 0
    configurations = 0
    violations: list[dict[str, object]] = []
    for graph in iter_connected_graphs(args.order, geng=args.geng):
        bases += 1
        base_audit = audit_all_pairs(graph)
        if base_audit.violation is not None:
            raise RuntimeError(
                f"base graph {graph.graph6} already violates the conjecture"
            )
        count = graph.order if index_kind == "vertex" else len(graph.edges)
        for index in range(count):
            configurations += 1
            transformed = operation(graph, index)
            audit = audit_all_pairs(transformed)
            if audit.violation is not None and len(violations) < args.keep:
                violations.append(
                    {
                        "base_graph6": graph.graph6,
                        "base_edges": [list(edge) for edge in graph.edges],
                        "operation": args.operation,
                        "operation_index": index,
                        "operation_object": (
                            index
                            if index_kind == "vertex"
                            else list(graph.edges[index])
                        ),
                        "transformed_order": transformed.order,
                        "transformed_edges": [
                            list(edge) for edge in transformed.edges
                        ],
                        "violation": audit.violation,
                    }
                )
        if args.progress_every and bases % args.progress_every == 0:
            print(
                f"{args.operation} progress bases={bases} "
                f"configurations={configurations}",
                file=sys.stderr,
                flush=True,
            )
        if args.max_graphs and bases >= args.max_graphs:
            break
    return {
        "mode": "direct_transform",
        "operation": args.operation,
        "base_order": args.order,
        "base_graphs": bases,
        "configurations": configurations,
        "violations": len(violations),
        "violation_records": violations,
        "elapsed_seconds": time.monotonic() - started,
    }


def random_weight_false_twin_scan(args: argparse.Namespace) -> dict[str, object]:
    """Log-uniform I-Rayleigh screening after cloning each base vertex."""

    rng = random.Random(args.seed)
    base = decode_graph6(args.graph6)
    started = time.monotonic()
    evaluations = 0
    numerical_violations: list[dict[str, object]] = []
    best_record: dict[str, object] | None = None
    vertices = (
        tuple(args.vertices)
        if args.vertices
        else tuple(range(base.order))
    )
    for vertex in vertices:
        graph = add_false_twin(base, vertex)
        for trial in range(args.samples):
            exponents = [
                rng.uniform(-args.log10_span, args.log10_span)
                for _ in graph.edges
            ]
            weights = [10.0**exponent for exponent in exponents]
            log_ratio, pair, counts = weighted_all_pair_log_ratios(
                graph, weights
            )
            evaluations += 1
            if pair is None:
                raise RuntimeError("transformed graph has no testable edge pair")
            record = {
                "base_graph6": base.graph6,
                "cloned_vertex": vertex,
                "cloned_neighbourhood": sorted(
                    v if u == vertex else u
                    for u, v in base.edges
                    if u == vertex or v == vertex
                ),
                "trial": trial,
                "tested_pair_indexes": list(pair),
                "tested_edges": [
                    list(graph.edges[pair[0]]),
                    list(graph.edges[pair[1]]),
                ],
                "max_log_ratio": log_ratio,
                "weights": weights,
                "counts": counts,
            }
            if (
                best_record is None
                or log_ratio > float(best_record["max_log_ratio"])
            ):
                best_record = record
            if log_ratio > args.violation_tolerance:
                numerical_violations.append(record)
                if len(numerical_violations) >= args.keep:
                    return {
                        "mode": "random_weight_false_twin",
                        "base_graph6": base.graph6,
                        "base_order": base.order,
                        "base_edges": len(base.edges),
                        "vertices": list(vertices),
                        "samples_per_vertex": args.samples,
                        "log10_span": args.log10_span,
                        "seed": args.seed,
                        "evaluations": evaluations,
                        "numerical_violations": numerical_violations,
                        "best_record": best_record,
                        "truncated_after_violation_limit": True,
                        "elapsed_seconds": time.monotonic() - started,
                    }
        print(
            f"random-weight false-twin vertex={vertex} "
            f"evaluations={evaluations} "
            f"best_log_ratio={best_record['max_log_ratio'] if best_record else None}",
            file=sys.stderr,
            flush=True,
        )
    return {
        "mode": "random_weight_false_twin",
        "base_graph6": base.graph6,
        "base_order": base.order,
        "base_edges": len(base.edges),
        "vertices": list(vertices),
        "samples_per_vertex": args.samples,
        "log10_span": args.log10_span,
        "seed": args.seed,
        "evaluations": evaluations,
        "numerical_violations": numerical_violations,
        "best_record": best_record,
        "truncated_after_violation_limit": False,
        "elapsed_seconds": time.monotonic() - started,
    }


def graph_one_sum(left: Graph, right: Graph, lv: int, rv: int) -> Graph:
    """Identify lv and rv, retaining every edge."""

    mapping: dict[int, int] = {}
    next_vertex = left.order
    for vertex in range(right.order):
        if vertex == rv:
            mapping[vertex] = lv
        else:
            mapping[vertex] = next_vertex
            next_vertex += 1
    edges = list(left.edges)
    edges.extend(
        tuple(sorted((mapping[u], mapping[v]))) for u, v in right.edges
    )
    return Graph(left.order + right.order - 1, tuple(sorted(edges)))


def graph_two_sum(
    left: Graph, right: Graph, left_edge: int, right_edge: int
) -> Graph:
    """Standard graphic 2-sum: identify distinguished edges, then delete it."""

    lu, lv = left.edges[left_edge]
    ru, rv = right.edges[right_edge]
    mapping = {ru: lu, rv: lv}
    next_vertex = left.order
    for vertex in range(right.order):
        if vertex not in mapping:
            mapping[vertex] = next_vertex
            next_vertex += 1
    edges = [
        edge for index, edge in enumerate(left.edges) if index != left_edge
    ]
    edges.extend(
        tuple(sorted((mapping[u], mapping[v])))
        for index, (u, v) in enumerate(right.edges)
        if index != right_edge
    )
    if len(edges) != len(set(edges)):
        raise ValueError("2-sum produced a parallel edge; input was degenerate")
    return Graph(left.order + right.order - 2, tuple(sorted(edges)))


def sum_scan(args: argparse.Namespace) -> dict[str, object]:
    started = time.monotonic()
    catalogue = {
        order: tuple(iter_connected_graphs(order, geng=args.geng))
        for order in range(2, args.max_component_order + 1)
    }
    configurations = 0
    skipped_parallel = 0
    violations: list[dict[str, object]] = []
    for left_order in catalogue:
        for right_order in catalogue:
            if left_order > right_order:
                continue
            output_order = (
                left_order + right_order - (1 if args.operation == "one_sum" else 2)
            )
            if output_order > args.max_output_order:
                continue
            for left in catalogue[left_order]:
                for right in catalogue[right_order]:
                    if args.operation == "one_sum":
                        indices = (
                            (lv, rv)
                            for lv in range(left.order)
                            for rv in range(right.order)
                        )
                    else:
                        indices = (
                            (le, re)
                            for le in range(len(left.edges))
                            for re in range(len(right.edges))
                        )
                    for first, second in indices:
                        try:
                            transformed = (
                                graph_one_sum(left, right, first, second)
                                if args.operation == "one_sum"
                                else graph_two_sum(left, right, first, second)
                            )
                        except ValueError:
                            skipped_parallel += 1
                            continue
                        configurations += 1
                        audit = audit_all_pairs(transformed)
                        if audit.violation is not None and len(violations) < args.keep:
                            violations.append(
                                {
                                    "left_graph6": left.graph6,
                                    "right_graph6": right.graph6,
                                    "operation_indexes": [first, second],
                                    "result_order": transformed.order,
                                    "result_edges": [
                                        list(edge) for edge in transformed.edges
                                    ],
                                    "violation": audit.violation,
                                }
                            )
                        if args.max_configurations and configurations >= args.max_configurations:
                            return {
                                "mode": "sum_scan",
                                "operation": args.operation,
                                "configurations": configurations,
                                "skipped_parallel": skipped_parallel,
                                "violations": len(violations),
                                "violation_records": violations,
                                "truncated": True,
                                "elapsed_seconds": time.monotonic() - started,
                            }
    return {
        "mode": "sum_scan",
        "operation": args.operation,
        "component_orders": [2, args.max_component_order],
        "maximum_output_order": args.max_output_order,
        "configurations": configurations,
        "skipped_parallel": skipped_parallel,
        "violations": len(violations),
        "violation_records": violations,
        "truncated": False,
        "elapsed_seconds": time.monotonic() - started,
    }


def self_test() -> dict[str, object]:
    # Triangle: 7 forests; each edge appears 3 times, each pair once.
    triangle = Graph(3, ((0, 1), (0, 2), (1, 2)))
    audit = audit_all_pairs(triangle)
    assert audit.total == 7
    assert audit.single == (3, 3, 3)
    assert set(audit.pair.values()) == {1}
    assert audit.minimum_margin == 2

    # A tree has every edge as a free Bernoulli coordinate.
    path = Graph(4, ((0, 1), (1, 2), (2, 3)))
    audit = audit_all_pairs(path)
    assert audit.total == 8
    assert audit.single == (4, 4, 4)
    assert set(audit.pair.values()) == {2}
    assert audit.minimum_margin == 0

    # Directly check graph6 bit order.
    assert decode_graph6("Bw").edges == triangle.edges

    # Formula sanity: weighting one triangle edge leaves the other two with
    # margin t+t^2, nonnegative for every positive t.
    counter = ForestCounter(triangle)
    total = counter.count()
    single = tuple(counter.count((i,)) for i in range(3))
    pair = {
        (a, b): counter.count((a, b)) for a, b in combinations(range(3), 2)
    }
    polynomial = weighted_margin_polynomial(
        counter, total, single, pair, 0, 1, 2
    )
    assert polynomial == (0, 1, 1)
    assert positive_half_line_certificate(polynomial)[0]

    # Recount representative transformations rather than relying on formulae.
    for transformed in (
        add_false_twin(triangle, 0),
        add_leaf(triangle, 0),
        add_parallel_two_path(triangle, 0),
        subdivide_edge(triangle, 0),
        graph_one_sum(triangle, triangle, 0, 0),
        graph_two_sum(triangle, triangle, 0, 0),
    ):
        assert audit_all_pairs(transformed).violation is None
    return {"mode": "self_test", "status": "passed"}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--geng", type=Path, default=DEFAULT_GENG)
    subparsers = result.add_subparsers(dest="command", required=True)

    subparsers.add_parser("self-test")

    weighted = subparsers.add_parser("weighted")
    weighted.add_argument("--order", type=int, required=True)
    weighted.add_argument("--shard-index", type=int, default=0)
    weighted.add_argument("--shard-count", type=int, default=1)
    weighted.add_argument("--max-graphs", type=int, default=0)
    weighted.add_argument("--keep", type=int, default=3)
    weighted.add_argument("--max-path-length", type=int, default=40)
    weighted.add_argument("--max-parallel-paths", type=int, default=100_000)
    weighted.add_argument("--progress-every", type=int, default=100)

    direct = subparsers.add_parser("direct")
    direct.add_argument(
        "--operation",
        choices=("false_twin", "leaf", "parallel_two_path", "subdivide_edge"),
        required=True,
    )
    direct.add_argument("--order", type=int, required=True)
    direct.add_argument("--max-graphs", type=int, default=0)
    direct.add_argument("--keep", type=int, default=3)
    direct.add_argument("--progress-every", type=int, default=100)

    sums = subparsers.add_parser("sums")
    sums.add_argument("--operation", choices=("one_sum", "two_sum"), required=True)
    sums.add_argument("--max-component-order", type=int, default=4)
    sums.add_argument("--max-output-order", type=int, default=7)
    sums.add_argument("--max-configurations", type=int, default=0)
    sums.add_argument("--keep", type=int, default=3)

    random_twins = subparsers.add_parser("random-weight-false-twin")
    random_twins.add_argument("--graph6", required=True)
    random_twins.add_argument("--vertices", type=int, nargs="*", default=())
    random_twins.add_argument("--samples", type=int, default=100)
    random_twins.add_argument("--log10-span", type=float, default=6.0)
    random_twins.add_argument("--seed", type=int, default=1757)
    random_twins.add_argument("--violation-tolerance", type=float, default=1e-10)
    random_twins.add_argument("--keep", type=int, default=3)
    return result


def main() -> int:
    args = parser().parse_args()
    if args.command == "self-test":
        payload = self_test()
    elif args.command == "weighted":
        if not 0 <= args.shard_index < args.shard_count:
            raise ValueError("invalid shard")
        payload = weighted_scan(args)
    elif args.command == "direct":
        payload = direct_transform_scan(args)
    elif args.command == "random-weight-false-twin":
        payload = random_weight_false_twin_scan(args)
    else:
        payload = sum_scan(args)
    print(json.dumps(payload, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
