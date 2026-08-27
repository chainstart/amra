#!/usr/bin/env python3
"""Exact finite replay for the faithful linear-hypergraph embedding theorem.

The replay uses a three-edge linear host whose pairwise intersections are
three different vertices.  Each edge has 129 vertices, so K=128 satisfies
the theorem's strict minimum-edge-size condition.  Finite replay checks the
encoded identities and invariants; it is not used to infer the theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


K = 128
B = 10_000
EDGE_SIZE = 129


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for value in range(2, math.isqrt(limit) + 1):
        if sieve[value]:
            sieve[value * value : limit + 1 : value] = b"\x00" * (
                (limit - value * value) // value + 1
            )
    return [value for value in range(2, limit + 1) if sieve[value]]


def nontrivial_partitions(block: tuple[int, ...]) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    full = (1 << len(block)) - 1
    result: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for mask in range(1, full):
        complement = full ^ mask
        if mask >= complement:
            continue
        left = tuple(block[index] for index in range(len(block)) if mask & (1 << index))
        right = tuple(block[index] for index in range(len(block)) if complement & (1 << index))
        result.append((left, right))
    return result


def product(values) -> int:
    answer = 1
    for value in values:
        answer *= value
    return answer


def ceil_log2(value: int) -> int:
    assert value > 0
    return (value - 1).bit_length()


def cover_number(masks: set[int], edge_count: int) -> int:
    target = (1 << edge_count) - 1
    useful = sorted(mask for mask in masks if mask)
    for size in range(1, edge_count + 1):
        for chosen in itertools.combinations(useful, size):
            union = 0
            for mask in chosen:
                union |= mask
            if union == target:
                return size
    raise AssertionError("host has no transversal")


def matching_number(edges: list[set[int]]) -> int:
    best = 0
    for size in range(1, len(edges) + 1):
        for selected in itertools.combinations(edges, size):
            if all(left.isdisjoint(right) for left, right in itertools.combinations(selected, 2)):
                best = size
    return best


def main() -> None:
    next_vertex = 3
    edges: list[list[int]] = []
    for shared_pair in ((0, 1), (0, 2), (1, 2)):
        private = list(range(next_vertex, next_vertex + EDGE_SIZE - 2))
        next_vertex += EDGE_SIZE - 2
        edges.append([*shared_pair, *private])
    vertex_count = next_vertex

    degrees = [sum(vertex in edge for edge in edges) for vertex in range(vertex_count)]
    maximum_degree = max(degrees)
    r = math.ceil(math.log2(maximum_degree + 1)) + 1
    primes = [prime for prime in primes_up_to(B) if prime != 2]
    assert len(primes) >= r * vertex_count
    assert 2 * r * math.log2(B) + 5 <= K
    assert min(map(len, edges)) > K

    blocks = {
        vertex: tuple(primes[r * vertex : r * (vertex + 1)])
        for vertex in range(vertex_count)
    }
    incident = {
        vertex: [edge_id for edge_id, edge in enumerate(edges) if vertex in edge]
        for vertex in range(vertex_count)
    }
    factors: dict[tuple[int, int], tuple[tuple[int, ...], tuple[int, ...]]] = {}
    for vertex in range(vertex_count):
        partitions = nontrivial_partitions(blocks[vertex])
        assert len(partitions) >= degrees[vertex]
        for index, edge_id in enumerate(incident[vertex]):
            factors[(vertex, edge_id)] = partitions[index]

    shared_raw = {vertex: product(blocks[vertex]) for vertex in range(vertex_count)}
    shared_values = {
        vertex: (1 << (K - ceil_log2(raw) - 2)) * raw
        for vertex, raw in shared_raw.items()
    }

    supports: list[set[int]] = []
    relation_records: list[dict[str, int]] = []
    membership: dict[int, int] = {}
    for edge_id, edge in enumerate(edges):
        alpha_sets = [factors[(vertex, edge_id)][0] for vertex in edge]
        beta_sets = [factors[(vertex, edge_id)][1] for vertex in edge]
        alphas = [product(part) for part in alpha_sets]
        betas = [product(part) for part in beta_sets]
        private_raw = [alphas[0]]
        private_raw.extend(betas[index] * alphas[index + 1] for index in range(len(edge) - 1))
        private_raw.append(betas[-1])

        c_values = [ceil_log2(shared_raw[vertex]) for vertex in edge]
        d_values = [ceil_log2(value) for value in private_raw]
        ceiling_discrepancy = sum(d_values) - sum(c_values)
        delta = K - ceiling_discrepancy + 2 * len(edge)
        quotient, remainder = divmod(delta, len(edge) + 1)
        decrements = [quotient + (index < remainder) for index in range(len(edge) + 1)]
        assert sum(decrements) == delta
        assert max(decrements) <= 4

        private_values = [
            (1 << (K - d_value - decrement)) * raw
            for raw, d_value, decrement in zip(private_raw, d_values, decrements, strict=True)
        ]
        shared_shore = [shared_values[vertex] for vertex in edge]
        assert product(shared_shore) == product(private_values)
        assert len(set(shared_shore)) == len(shared_shore)
        assert len(set(private_values)) == len(private_values)
        assert set(shared_shore).isdisjoint(private_values)
        assert all((1 << K) // 32 < value <= (1 << K) for value in shared_shore + private_values)

        path_values: list[int] = [private_values[0]]
        for index, shared_value in enumerate(shared_shore):
            path_values.extend((shared_value, private_values[index + 1]))
        path_labels: list[tuple[int, ...]] = []
        for alpha_set, beta_set in zip(alpha_sets, beta_sets, strict=True):
            path_labels.extend((alpha_set, beta_set))
        for index, label in enumerate(path_labels):
            witness_prime = min(label)
            occurrences = [position for position, value in enumerate(path_values) if value % witness_prime == 0]
            assert occurrences == [index, index + 1]

        support = set(shared_shore + private_values)
        supports.append(support)
        for value in support:
            membership[value] = membership.get(value, 0) | (1 << edge_id)
        relation_records.append(
            {
                "edge_size": len(edge),
                "support_size": len(support),
                "delta": delta,
                "maximum_decrement": max(decrements),
            }
        )

    for left, right in itertools.combinations(range(len(edges)), 2):
        assert len(supports[left] & supports[right]) == len(set(edges[left]) & set(edges[right])) == 1

    host_masks = {
        sum(1 << edge_id for edge_id, edge in enumerate(edges) if vertex in edge)
        for vertex in range(vertex_count)
    }
    host_edge_sets = [set(edge) for edge in edges]
    host_tau = cover_number(host_masks, len(edges))
    arithmetic_tau = cover_number(set(membership.values()), len(edges))
    host_nu = matching_number(host_edge_sets)
    arithmetic_nu = matching_number(supports)
    assert (host_tau, arithmetic_tau) == (2, 2)
    assert (host_nu, arithmetic_nu) == (1, 1)

    source_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(
        json.dumps(
            {
                "schema_version": "amra.faithful_linear_embedding_replay.v1",
                "status": "PASS",
                "parameters": {
                    "K": K,
                    "B": B,
                    "edge_count": len(edges),
                    "edge_size": EDGE_SIZE,
                    "vertex_count": vertex_count,
                    "maximum_degree": maximum_degree,
                    "block_size": r,
                },
                "relations": relation_records,
                "verified": {
                    "prime_budget": True,
                    "bit_budget": True,
                    "equal_products": True,
                    "distinct_shores": True,
                    "fixed_band": True,
                    "path_prime_propagation": True,
                    "exact_intersections": True,
                    "transversal_number_preserved": arithmetic_tau == host_tau,
                    "matching_number_preserved": arithmetic_nu == host_nu,
                },
                "host_tau": host_tau,
                "arithmetic_tau": arithmetic_tau,
                "host_nu": host_nu,
                "arithmetic_nu": arithmetic_nu,
                "script_sha256": source_sha256,
                "scope": "Finite replay only; the all-parameter theorem is proved in FAITHFUL_LINEAR_EMBEDDING.md.",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
