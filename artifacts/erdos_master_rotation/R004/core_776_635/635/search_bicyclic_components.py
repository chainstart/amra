#!/usr/bin/env python3
"""Exact component search in the all-prime semiprime swap graph for #635.

Every odd right vertex b <= LIMIT having full graph degree at least three is
used as a seed.  Its entire connected component is then expanded by exact
factorisation/inversion, with no label or neighbour cutoff.  Consequently a
PASS excludes every bicyclic component having a branch vertex <= LIMIT.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from math import isqrt


@dataclass(frozen=True, order=True)
class Edge:
    lo: int
    hi: int
    label: int
    scale: int
    p: int
    q: int


def sieve_spf(limit: int) -> list[int]:
    spf = list(range(limit + 2))
    for prime in range(2, isqrt(limit + 1) + 1):
        if spf[prime] != prime:
            continue
        for value in range(prime * prime, limit + 2, prime):
            if spf[value] == value:
                spf[value] = prime
    return spf


class Arithmetic:
    def __init__(self, limit: int):
        self.limit = limit
        self.spf = sieve_spf(limit)

    def is_prime(self, value: int) -> bool:
        if value < 2:
            return False
        if value <= self.limit + 1:
            return self.spf[value] == value
        if value % 2 == 0:
            return value == 2
        for divisor in range(3, isqrt(value) + 1, 2):
            if value % divisor == 0:
                return False
        return True

    def distinct_prime_factors(self, value: int) -> list[int]:
        original = value
        answer: list[int] = []
        if value <= self.limit + 1:
            while value > 1:
                prime = self.spf[value]
                answer.append(prime)
                while value % prime == 0:
                    value //= prime
        else:
            if value % 2 == 0:
                answer.append(2)
                while value % 2 == 0:
                    value //= 2
            divisor = 3
            while divisor * divisor <= value:
                if value % divisor == 0:
                    answer.append(divisor)
                    while value % divisor == 0:
                        value //= divisor
                divisor += 2
            if value > 1:
                answer.append(value)
        product_divides = 1
        for prime in answer:
            assert self.is_prime(prime)
            product_divides *= prime
        assert original % product_divides == 0
        return answer

    def incident_edges(self, vertex: int) -> list[Edge]:
        edges: list[Edge] = []
        for deleted_prime in self.distinct_prime_factors(vertex):
            if deleted_prime == 2:
                continue
            quotient_plus_one = vertex // deleted_prime + 1
            scale = quotient_plus_one & -quotient_plus_one
            partner_prime = quotient_plus_one // scale
            if (
                scale < 2
                or partner_prime == deleted_prime
                or not self.is_prime(partner_prime)
            ):
                continue
            other = vertex + deleted_prime - partner_prime
            label = vertex + deleted_prime
            assert label == scale * deleted_prime * partner_prime
            assert other == label - partner_prime
            assert other > 0 and other % 2 == 1
            edges.append(
                Edge(
                    min(vertex, other),
                    max(vertex, other),
                    label,
                    scale,
                    min(deleted_prime, partner_prime),
                    max(deleted_prime, partner_prime),
                )
            )
        return sorted(set(edges))


def closed_component(
    arithmetic: Arithmetic, start: int, safety_limit: int
) -> tuple[set[int], list[Edge]]:
    vertices = {start}
    queue = deque([start])
    edges: set[Edge] = set()
    while queue:
        vertex = queue.popleft()
        for edge in arithmetic.incident_edges(vertex):
            edges.add(edge)
            other = edge.hi if edge.lo == vertex else edge.lo
            if other not in vertices:
                vertices.add(other)
                if len(vertices) > safety_limit:
                    raise RuntimeError(
                        "component safety limit reached; no finite claim allowed"
                    )
                queue.append(other)
    return vertices, sorted(edges)


def cycle_core(vertices: set[int], edges: list[Edge]) -> list[Edge]:
    active = set(range(len(edges)))
    incident: dict[int, set[int]] = defaultdict(set)
    for index, edge in enumerate(edges):
        incident[edge.lo].add(index)
        incident[edge.hi].add(index)
    queue = deque(
        vertex for vertex in vertices if len(incident[vertex]) <= 1
    )
    while queue:
        vertex = queue.popleft()
        live = incident[vertex] & active
        if len(live) > 1:
            continue
        for index in list(live):
            active.remove(index)
            edge = edges[index]
            other = edge.hi if edge.lo == vertex else edge.lo
            if len(incident[other] & active) <= 1:
                queue.append(other)
    return [edges[index] for index in sorted(active)]


def label_conflicts(labels: list[int]) -> list[list[int]]:
    conflicts: list[list[int]] = []
    for index, first in enumerate(labels):
        for second in labels[index + 1 :]:
            difference = second - first
            if first % difference == 0:
                assert second % difference == 0
                conflicts.append([first, second, difference])
    return conflicts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=2_000_000)
    parser.add_argument("--component-safety-limit", type=int, default=100_000)
    args = parser.parse_args()
    if args.limit < 100:
        raise ValueError(args.limit)

    arithmetic = Arithmetic(args.limit + 1)
    branch_seeds: list[tuple[int, int]] = []
    upward_branch_seeds: list[tuple[int, int]] = []
    maximum_degree = 0
    maximum_upward_degree = 0
    for vertex in range(1, args.limit + 1, 2):
        incident = arithmetic.incident_edges(vertex)
        degree = len(incident)
        upward_degree = sum(edge.lo == vertex for edge in incident)
        maximum_degree = max(maximum_degree, degree)
        maximum_upward_degree = max(maximum_upward_degree, upward_degree)
        if degree >= 3:
            branch_seeds.append((vertex, degree))
        if upward_degree >= 2:
            upward_branch_seeds.append((vertex, upward_degree))

    globally_seen: set[int] = set()
    component_count = 0
    maximum_component_vertices = 0
    maximum_component_edges = 0
    maximum_reached_vertex = 0
    cyclomatic_histogram: dict[int, int] = defaultdict(int)
    cyclic_components: list[dict[str, object]] = []

    for seed, seed_degree in branch_seeds:
        if seed in globally_seen:
            continue
        vertices, edges = closed_component(
            arithmetic, seed, args.component_safety_limit
        )
        globally_seen.update(vertices)
        component_count += 1
        maximum_component_vertices = max(
            maximum_component_vertices, len(vertices)
        )
        maximum_component_edges = max(maximum_component_edges, len(edges))
        maximum_reached_vertex = max(maximum_reached_vertex, max(vertices))
        cyclomatic = len(edges) - len(vertices) + 1
        assert cyclomatic >= 0
        cyclomatic_histogram[cyclomatic] += 1
        if cyclomatic:
            core = cycle_core(vertices, edges)
            labels = sorted(edge.label for edge in core)
            cyclic_components.append(
                {
                    "seed": seed,
                    "seed_degree": seed_degree,
                    "vertex_count": len(vertices),
                    "edge_count": len(edges),
                    "cyclomatic_number": cyclomatic,
                    "vertices": sorted(vertices),
                    "core_edges": [asdict(edge) for edge in core],
                    "core_labels": labels,
                    "core_label_conflicts": label_conflicts(labels),
                }
            )

    assert all(
        component["cyclomatic_number"] == 1
        for component in cyclic_components
    )
    known_cycle_seeds = {component["seed"] for component in cyclic_components}
    assert known_cycle_seeds == {273, 5_355, 29_165}

    # A second, independent seed condition comes from orienting every edge
    # toward its larger endpoint.  For a finite connected component,
    #   mu = E-V+1 = 1-sum_v(1-d_+(v))
    #      = 1-s + sum_{d_+>=2}(d_+-1),
    # where s is the number of upward sinks.  Thus a bicyclic component must
    # contain an upward-branching vertex.  Expanding all such small vertices
    # gives a second finite exclusion with a different completeness proof.
    upward_seen: set[int] = set()
    upward_component_count = 0
    upward_maximum_reached = 0
    upward_cyclomatic_histogram: dict[int, int] = defaultdict(int)
    upward_cyclic_seeds: list[int] = []
    upward_cyclic_components: list[dict[str, object]] = []
    for seed, _ in upward_branch_seeds:
        if seed in upward_seen:
            continue
        vertices, edges = closed_component(
            arithmetic, seed, args.component_safety_limit
        )
        upward_seen.update(vertices)
        upward_component_count += 1
        upward_maximum_reached = max(
            upward_maximum_reached, max(vertices)
        )
        cyclomatic = len(edges) - len(vertices) + 1
        assert cyclomatic >= 0
        upward_cyclomatic_histogram[cyclomatic] += 1
        if cyclomatic:
            upward_cyclic_seeds.append(seed)
            core = cycle_core(vertices, edges)
            labels = sorted(edge.label for edge in core)
            upward_cyclic_components.append(
                {
                    "seed": seed,
                    "vertex_count": len(vertices),
                    "edge_count": len(edges),
                    "cyclomatic_number": cyclomatic,
                    "core_edges": [asdict(edge) for edge in core],
                    "core_labels": labels,
                    "core_label_conflicts": label_conflicts(labels),
                }
            )
    assert max(upward_cyclomatic_histogram, default=0) <= 1
    assert set(upward_cyclic_seeds) == {
        253,
        4_979,
        24_485,
        29_149,
        39_783,
        1_244_919,
    }, upward_cyclic_seeds

    result = {
        "schema": "amra.erdos635.r004-bicyclic-component-search.v1",
        "status": "PASS",
        "branch_vertex_limit": args.limit,
        "branch_seed_count": len(branch_seeds),
        "distinct_seeded_component_count": component_count,
        "maximum_full_graph_degree_observed": maximum_degree,
        "maximum_upward_degree_observed": maximum_upward_degree,
        "maximum_component_vertex_count": maximum_component_vertices,
        "maximum_component_edge_count": maximum_component_edges,
        "maximum_vertex_reached_during_exact_expansion": maximum_reached_vertex,
        "cyclomatic_histogram": {
            str(key): value for key, value in sorted(cyclomatic_histogram.items())
        },
        "cyclic_components": cyclic_components,
        "bicyclic_components_found": 0,
        "upward_orientation_audit": {
            "identity": (
                "mu=E-V+1=1-s+sum_{d_plus>=2}(d_plus-1)"
            ),
            "upward_branch_seed_count": len(upward_branch_seeds),
            "distinct_seeded_component_count": upward_component_count,
            "maximum_vertex_reached_during_exact_expansion":
                upward_maximum_reached,
            "cyclomatic_histogram": {
                str(key): value
                for key, value in sorted(
                    upward_cyclomatic_histogram.items()
                )
            },
            "cyclic_component_first_seeds": upward_cyclic_seeds,
            "cyclic_components": upward_cyclic_components,
            "bicyclic_components_found": 0,
        },
        "strict_consequence": (
            "Every all-prime semiprime swap-graph bicyclic core has all "
            f"undirected and upward branch vertices greater than {args.limit}."
        ),
        "completeness": (
            "Every odd vertex up to the branch limit was tested using all "
            "of its distinct prime divisors.  Every degree>=3 seed's entire "
            "component was then expanded by the exact inversion formula; "
            "the safety limit was never reached."
        ),
        "scope": (
            "This is a finite branch-vertex exclusion, not an unbounded "
            "pseudoforest theorem and not a solution of the original problem."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
