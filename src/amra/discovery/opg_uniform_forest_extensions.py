"""Bounded labelled one-vertex extensions for OPG-1757.

This module deliberately lives outside the exhaustive runner.  It fixes an
order-9, order-10, or order-11 seed graph's graph6 labelling, appends the next
vertex, and enumerates all neighbour subsets of sizes two through
``min(5, n)``.  Different label indexes may describe isomorphic graphs; no
non-isomorphic exhaustion claim is made.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from amra.discovery.opg_coloring_search import EdgeGraph, decode_graph6
from amra.discovery.opg_uniform_forest_search import (
    ForestEvaluationBudgetExceeded,
    GraphicMatroidForestCounter,
    strongest_edge_pair,
)


SUPPORTED_SEED_ORDERS = (9, 10, 11)
DEFAULT_SEED_ORDER = 9
EXTENSION_VERTEX = DEFAULT_SEED_ORDER
MINIMUM_NEIGHBOURS = 2
MAXIMUM_NEIGHBOURS = 5


def expected_labelled_extension_count(seed_order: int) -> int:
    """Return the fixed-labelling extension count for a supported seed order."""

    if (
        not isinstance(seed_order, int)
        or isinstance(seed_order, bool)
        or seed_order not in SUPPORTED_SEED_ORDERS
    ):
        raise ValueError("seed order must be nine, ten, or eleven")
    return sum(
        math.comb(seed_order, size)
        for size in range(
            MINIMUM_NEIGHBOURS,
            min(MAXIMUM_NEIGHBOURS, seed_order) + 1,
        )
    )


# Backward-compatible name for the original order-nine search space.
EXPECTED_LABELLED_EXTENSIONS = expected_labelled_extension_count(
    DEFAULT_SEED_ORDER
)


@dataclass(frozen=True)
class LabelledVertexExtension:
    label_index: int
    neighbours: tuple[int, ...]
    graph: EdgeGraph


@dataclass(frozen=True)
class InheritedPairEvaluation:
    label_index: int
    neighbours: tuple[int, ...]
    graph6: str
    forest_count: int
    forest_count_e: int
    forest_count_f: int
    forest_count_ef: int
    left_product: int
    right_product: int
    states: int
    elapsed_seconds: float

    @property
    def margin(self) -> int:
        return self.right_product - self.left_product

    @property
    def violates_negative_association(self) -> bool:
        return self.left_product > self.right_product

    @property
    def ratio(self) -> Fraction:
        return Fraction(self.left_product, self.right_product)

    def as_dict(self) -> dict[str, object]:
        ratio = self.ratio
        return {
            "label_index": self.label_index,
            "neighbours": list(self.neighbours),
            "graph6": self.graph6,
            "forest_count": self.forest_count,
            "forest_count_e": self.forest_count_e,
            "forest_count_f": self.forest_count_f,
            "forest_count_ef": self.forest_count_ef,
            "left_product": self.left_product,
            "right_product": self.right_product,
            "margin": self.margin,
            "ratio_numerator": ratio.numerator,
            "ratio_denominator": ratio.denominator,
            "states": self.states,
            "elapsed_seconds": self.elapsed_seconds,
        }


@dataclass(frozen=True)
class ExtensionSearchResult:
    status: str
    seed_graph6: str
    seed_order: int
    inherited_edge_indexes: tuple[int, int]
    inherited_edges: tuple[tuple[int, int], tuple[int, int]]
    attempted: int
    evaluated: int
    next_label_index: int
    timeout_records: tuple[dict[str, object], ...]
    top_evaluations: tuple[InheritedPairEvaluation, ...]
    candidate: dict[str, object] | None
    pending_inherited_violation: dict[str, object] | None
    elapsed_seconds: float

    def as_dict(self) -> dict[str, object]:
        extension_vertex = self.seed_order
        maximum_neighbours = min(MAXIMUM_NEIGHBOURS, self.seed_order)
        expected_labels = expected_labelled_extension_count(self.seed_order)
        return {
            "schema": "amra.opg1757.labelled-extension.v1",
            "status": self.status,
            "seed_graph6": self.seed_graph6,
            "seed_order": self.seed_order,
            "inherited_edge_indexes": list(self.inherited_edge_indexes),
            "inherited_edges": [list(edge) for edge in self.inherited_edges],
            "attempted": self.attempted,
            "evaluated": self.evaluated,
            "next_label_index": self.next_label_index,
            "timeouts": len(self.timeout_records),
            "timeout_records": list(self.timeout_records),
            "top_evaluations": [
                evaluation.as_dict() for evaluation in self.top_evaluations
            ],
            "candidate": self.candidate,
            "pending_inherited_violation": (
                self.pending_inherited_violation
            ),
            "elapsed_seconds": self.elapsed_seconds,
            "label_enumeration": {
                "kind": "fixed-seed-labelled-one-vertex-extension",
                "extension_vertex": extension_vertex,
                "neighbour_subset_size_range": [
                    MINIMUM_NEIGHBOURS,
                    maximum_neighbours,
                ],
                "expected_labelled_extensions": expected_labels,
                "label_index_range": [
                    0,
                    expected_labels - 1,
                ],
                "isomorphism_deduplicated": False,
                "possible_isomorphic_duplicate_label_range": [
                    0,
                    expected_labels - 1,
                ],
                "nonisomorphic_exhaustion_claimed": False,
            },
            "pair_screening": {
                "screened_before_trigger": "inherited edge pair only",
                "full_pair_trigger": "inherited left_product > right_product",
                "all_pairs_checked_for_nontriggering_extensions": False,
                "counterexample_exhaustion_claimed": False,
            },
        }


def encode_simple_graph6(
    vertex_count: int,
    edges: Iterable[tuple[int, int]],
) -> str:
    """Return compact graph6 for a simple graph of order at most 62."""

    if not isinstance(vertex_count, int) or isinstance(vertex_count, bool):
        raise ValueError("vertex_count must be an integer")
    if not 0 <= vertex_count <= 62:
        raise ValueError("compact graph6 requires order in 0..62")
    normalized: set[tuple[int, int]] = set()
    for raw_left, raw_right in edges:
        if (
            not isinstance(raw_left, int)
            or isinstance(raw_left, bool)
            or not isinstance(raw_right, int)
            or isinstance(raw_right, bool)
        ):
            raise ValueError("edge endpoints must be integers")
        left, right = sorted((raw_left, raw_right))
        if not 0 <= left < right < vertex_count:
            raise ValueError(f"invalid simple edge {(raw_left, raw_right)}")
        edge = (left, right)
        if edge in normalized:
            raise ValueError(f"duplicate simple edge {edge}")
        normalized.add(edge)

    bits = [
        int((left, right) in normalized)
        for right in range(1, vertex_count)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(vertex_count + 63) + "".join(payload)


def _seed_and_pair(
    seed_graph6: str,
    inherited_edge_indexes: tuple[int, int],
) -> tuple[EdgeGraph, tuple[int, int]]:
    seed = decode_graph6(seed_graph6)
    if seed.vertex_count not in SUPPORTED_SEED_ORDERS:
        raise ValueError(
            "seed graph6 must have exactly nine, ten, or eleven vertices"
        )
    if (
        not isinstance(inherited_edge_indexes, tuple)
        or len(inherited_edge_indexes) != 2
        or any(
            not isinstance(index, int) or isinstance(index, bool)
            for index in inherited_edge_indexes
        )
    ):
        raise ValueError("inherited edge indexes must be an integer pair")
    first, second = inherited_edge_indexes
    if first == second:
        raise ValueError("inherited edges must be distinct")
    if not (
        0 <= first < len(seed.edges)
        and 0 <= second < len(seed.edges)
    ):
        raise ValueError("inherited edge index is outside the seed edge list")
    return seed, inherited_edge_indexes


def iter_labelled_vertex_extensions(
    seed_graph6: str,
) -> Iterator[LabelledVertexExtension]:
    """Yield every supported fixed-labelling extension in stable order."""

    seed = decode_graph6(seed_graph6)
    if seed.vertex_count not in SUPPORTED_SEED_ORDERS:
        raise ValueError(
            "seed graph6 must have exactly nine, ten, or eleven vertices"
        )
    extension_vertex = seed.vertex_count
    maximum_neighbours = min(MAXIMUM_NEIGHBOURS, seed.vertex_count)
    expected_labels = expected_labelled_extension_count(seed.vertex_count)
    label_index = 0
    for size in range(MINIMUM_NEIGHBOURS, maximum_neighbours + 1):
        for neighbours in combinations(range(seed.vertex_count), size):
            new_edges = tuple(
                (vertex, extension_vertex) for vertex in neighbours
            )
            edges = seed.edges + new_edges
            encoding = encode_simple_graph6(seed.vertex_count + 1, edges)
            yield LabelledVertexExtension(
                label_index,
                neighbours,
                EdgeGraph(seed.vertex_count + 1, edges, encoding),
            )
            label_index += 1
    if label_index != expected_labels:
        raise RuntimeError("labelled extension count invariant failed")


def evaluate_inherited_pair(
    extension: LabelledVertexExtension,
    inherited_edge_indexes: tuple[int, int],
    *,
    timeout_seconds: float,
    max_states: int,
) -> InheritedPairEvaluation:
    """Evaluate only N, N_e, N_f and N_ef with one shared memo."""

    first, second = inherited_edge_indexes
    if (
        first == second
        or not 0 <= first < len(extension.graph.edges)
        or not 0 <= second < len(extension.graph.edges)
    ):
        raise ValueError("invalid inherited edge pair")
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
    ):
        raise ValueError("timeout_seconds must be positive and finite")
    if (
        not isinstance(max_states, int)
        or isinstance(max_states, bool)
        or max_states <= 0
    ):
        raise ValueError("max_states must be positive")
    counter = GraphicMatroidForestCounter(
        extension.graph.vertex_count,
        extension.graph.edges,
        timeout_seconds=timeout_seconds,
        max_states=max_states,
    )
    forest_count = counter.count_after_contracting()
    forest_count_e = counter.count_after_contracting((first,))
    forest_count_f = counter.count_after_contracting((second,))
    forest_count_ef = counter.count_after_contracting((first, second))
    left_product = forest_count * forest_count_ef
    right_product = forest_count_e * forest_count_f
    if right_product <= 0:
        raise RuntimeError("a simple inherited edge has zero forest support")
    return InheritedPairEvaluation(
        extension.label_index,
        extension.neighbours,
        extension.graph.encoding,
        forest_count,
        forest_count_e,
        forest_count_f,
        forest_count_ef,
        left_product,
        right_product,
        counter.states,
        counter.elapsed_seconds,
    )


def _rank_evaluations(
    evaluations: list[InheritedPairEvaluation],
    top_k: int,
) -> None:
    evaluations.sort(
        key=lambda evaluation: (
            evaluation.ratio,
            -evaluation.label_index,
        ),
        reverse=True,
    )
    del evaluations[top_k:]


def _full_pair_candidate(
    extension: LabelledVertexExtension,
    inherited_edge_indexes: tuple[int, int],
    screen: InheritedPairEvaluation,
    *,
    timeout_seconds: float,
    max_states: int,
) -> dict[str, object]:
    counter = GraphicMatroidForestCounter(
        extension.graph.vertex_count,
        extension.graph.edges,
        timeout_seconds=timeout_seconds,
        max_states=max_states,
    )
    statistics = counter.statistics()
    first, second = inherited_edge_indexes
    replay = (
        statistics.forest_count,
        statistics.edge_forest_counts[first],
        statistics.edge_forest_counts[second],
        statistics.pair_forest_counts[first][second],
    )
    expected = (
        screen.forest_count,
        screen.forest_count_e,
        screen.forest_count_f,
        screen.forest_count_ef,
    )
    if replay != expected:
        raise RuntimeError("full-pair replay disagrees with inherited screening")
    strongest = strongest_edge_pair(statistics)
    if not strongest.violates_negative_association:
        raise RuntimeError(
            "full-pair replay lost an exact inherited-edge violation"
        )
    assert strongest.edge_pair is not None
    strongest_first, strongest_second = strongest.edge_pair
    return {
        "problem": "opg1757",
        "verification_status": "pending_independent_verification",
        "full_pair_recheck": (
            "same deletion-contraction implementation over every edge pair"
        ),
        "label_index": extension.label_index,
        "neighbours": list(extension.neighbours),
        "graph6": extension.graph.encoding,
        "vertices": extension.graph.vertex_count,
        "edges": [list(edge) for edge in extension.graph.edges],
        "inherited_pair": {
            "edge_indexes": list(inherited_edge_indexes),
            "edges": [
                list(extension.graph.edges[first]),
                list(extension.graph.edges[second]),
            ],
            **screen.as_dict(),
        },
        "strongest_full_pair": {
            "edge_indexes": [strongest_first, strongest_second],
            "edges": [
                list(extension.graph.edges[strongest_first]),
                list(extension.graph.edges[strongest_second]),
            ],
            "forest_count": statistics.forest_count,
            "forest_count_e": statistics.edge_forest_counts[
                strongest_first
            ],
            "forest_count_f": statistics.edge_forest_counts[
                strongest_second
            ],
            "forest_count_ef": strongest.forest_count_ef,
            "left_product": strongest.left_product,
            "right_product": strongest.right_product,
            "margin": strongest.margin,
        },
        "full_pair_states": counter.states,
        "full_pair_elapsed_seconds": counter.elapsed_seconds,
    }


def search_labelled_vertex_extensions(
    seed_graph6: str,
    inherited_edge_indexes: tuple[int, int],
    *,
    top_k: int = 20,
    per_graph_seconds: float = 5.0,
    wall_seconds: float = 60.0,
    max_states: int = 2_000_000,
) -> ExtensionSearchResult:
    """Screen labelled one-vertex extensions for one inherited edge pair.

    A ratio greater than one is replayed over all edge pairs before a pending
    candidate is returned.  The all-pair replay uses the same mathematical
    implementation and is not an independent verification.
    """

    seed, inherited_edge_indexes = _seed_and_pair(
        seed_graph6,
        inherited_edge_indexes,
    )
    expected_labels = expected_labelled_extension_count(seed.vertex_count)
    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 0:
        raise ValueError("top_k must be non-negative")
    if (
        isinstance(per_graph_seconds, bool)
        or not isinstance(per_graph_seconds, (int, float))
        or not math.isfinite(per_graph_seconds)
        or per_graph_seconds <= 0
    ):
        raise ValueError("per_graph_seconds must be positive and finite")
    if (
        isinstance(wall_seconds, bool)
        or not isinstance(wall_seconds, (int, float))
        or not math.isfinite(wall_seconds)
        or wall_seconds < 0
    ):
        raise ValueError("wall_seconds must be non-negative and finite")
    if (
        not isinstance(max_states, int)
        or isinstance(max_states, bool)
        or max_states <= 0
    ):
        raise ValueError("max_states must be positive")

    started = time.monotonic()
    deadline = started + wall_seconds
    attempted = 0
    evaluated = 0
    next_label_index = 0
    timeouts: list[dict[str, object]] = []
    top: list[InheritedPairEvaluation] = []
    candidate: dict[str, object] | None = None
    pending: dict[str, object] | None = None
    status = "complete"

    for extension in iter_labelled_vertex_extensions(seed.encoding):
        now = time.monotonic()
        if now >= deadline:
            status = "paused_wall_budget"
            break
        attempted += 1
        next_label_index = extension.label_index + 1
        extension_deadline = min(deadline, now + per_graph_seconds)
        screen_seconds = extension_deadline - time.monotonic()
        if screen_seconds <= 0:
            if time.monotonic() >= deadline:
                status = "paused_wall_budget"
                break
            timeouts.append(
                {
                    "phase": "inherited_pair_screen",
                    "label_index": extension.label_index,
                    "neighbours": list(extension.neighbours),
                    "graph6": extension.graph.encoding,
                    "error": "per-graph budget expired before screening",
                }
            )
            continue
        try:
            screen = evaluate_inherited_pair(
                extension,
                inherited_edge_indexes,
                timeout_seconds=screen_seconds,
                max_states=max_states,
            )
        except ForestEvaluationBudgetExceeded as error:
            timeouts.append(
                {
                    "phase": "inherited_pair_screen",
                    "label_index": extension.label_index,
                    "neighbours": list(extension.neighbours),
                    "graph6": extension.graph.encoding,
                    "error": str(error),
                }
            )
            if time.monotonic() >= deadline:
                status = "paused_wall_budget"
                break
            continue

        evaluated += 1
        if top_k:
            top.append(screen)
            _rank_evaluations(top, top_k)
        if not screen.violates_negative_association:
            continue

        remaining = extension_deadline - time.monotonic()
        if remaining <= 0:
            pending = {
                "status": "inherited_violation_pending_full_pair_recheck",
                **screen.as_dict(),
            }
            status = "inherited_violation_pending_full_pair_recheck"
            break
        try:
            candidate = _full_pair_candidate(
                extension,
                inherited_edge_indexes,
                screen,
                timeout_seconds=remaining,
                max_states=max_states,
            )
        except ForestEvaluationBudgetExceeded as error:
            pending = {
                "status": "inherited_violation_pending_full_pair_recheck",
                "error": str(error),
                **screen.as_dict(),
            }
            status = "inherited_violation_pending_full_pair_recheck"
        else:
            status = "candidate_pending_independent_verification"
        break
    else:
        next_label_index = expected_labels
        if timeouts:
            status = "complete_with_timeouts"

    return ExtensionSearchResult(
        status,
        seed.encoding,
        seed.vertex_count,
        inherited_edge_indexes,
        (
            seed.edges[inherited_edge_indexes[0]],
            seed.edges[inherited_edge_indexes[1]],
        ),
        attempted,
        evaluated,
        next_label_index,
        tuple(timeouts),
        tuple(top),
        candidate,
        pending,
        time.monotonic() - started,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Screen labelled one-vertex extensions for OPG-1757."
    )
    parser.add_argument("--seed-graph6", required=True)
    parser.add_argument(
        "--edge-indexes",
        nargs=2,
        type=int,
        metavar=("E", "F"),
        required=True,
    )
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--per-graph-seconds", type=float, default=5.0)
    parser.add_argument("--wall-seconds", type=float, default=600.0)
    parser.add_argument("--max-states", type=int, default=2_000_000)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    result = search_labelled_vertex_extensions(
        arguments.seed_graph6,
        tuple(arguments.edge_indexes),
        top_k=arguments.top_k,
        per_graph_seconds=arguments.per_graph_seconds,
        wall_seconds=arguments.wall_seconds,
        max_states=arguments.max_states,
    ).as_dict()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
