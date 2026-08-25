#!/usr/bin/env python3
"""Exact finite replay of the r=2 squarefree rank-two reduction in #538."""

from __future__ import annotations

import argparse
import itertools
import json
import os
import time
from fractions import Fraction
from pathlib import Path


PRIMES = [2, 3, 5, 7, 11, 13, 17, 19]


def edges(k: int) -> list[tuple[int, int]]:
    return list(itertools.combinations(range(k), 2))


def triangle_free(k: int, chosen: set[tuple[int, int]]) -> bool:
    return all(
        sum(tuple(sorted(edge)) in chosen for edge in ((a, b), (a, c), (b, c))) <= 2
        for a, b, c in itertools.combinations(range(k), 3)
    )


def edge_weight(edge: tuple[int, int], primes: list[int]) -> Fraction:
    i, j = edge
    return Fraction(1, primes[i] * primes[j])


def best_graph_bruteforce(k: int, primes: list[int]) -> tuple[Fraction, list[tuple[int, int]], int]:
    all_edges = edges(k)
    best = Fraction(-1)
    best_edges: list[tuple[int, int]] = []
    checked = 0
    for mask in range(1 << len(all_edges)):
        chosen = {edge for bit, edge in enumerate(all_edges) if mask & (1 << bit)}
        if not triangle_free(k, chosen):
            continue
        checked += 1
        value = sum((edge_weight(edge, primes) for edge in chosen), Fraction())
        if value > best:
            best = value
            best_edges = sorted(chosen)
    return best, best_edges, checked


def best_complete_bipartite(k: int, primes: list[int]) -> tuple[Fraction, list[int]]:
    vertex_weights = [Fraction(1, p) for p in primes[:k]]
    total = sum(vertex_weights, Fraction())
    best = Fraction(-1)
    best_side: list[int] = []
    # Quotient by swapping the two sides: keep vertex zero on the first side.
    for mask in range(1 << (k - 1)):
        side = [0] + [i for i in range(1, k) if mask & (1 << (i - 1))]
        side_weight = sum((vertex_weights[i] for i in side), Fraction())
        value = side_weight * (total - side_weight)
        if value > best:
            best = value
            best_side = side
    return best, best_side


def representation_count_rank_two(
    exponents: tuple[int, ...], chosen: set[tuple[int, int]]
) -> int:
    count = 0
    for index, exponent in enumerate(exponents):
        if exponent == 0:
            continue
        reduced = list(exponents)
        reduced[index] -= 1
        support = tuple(i for i, value in enumerate(reduced) if value == 1)
        if all(value in (0, 1) for value in reduced) and len(support) == 2:
            if tuple(sorted(support)) in chosen:
                count += 1
    return count


def replay_original_constraint(k: int, chosen: set[tuple[int, int]]) -> int:
    maximum = 0
    # Exponent 2 detects the only repeated-prime boundary that can land back in
    # a squarefree rank.  One extra external prime is included as vertex k.
    for exponents in itertools.product((0, 1, 2), repeat=k + 1):
        maximum = max(maximum, representation_count_rank_two(exponents, chosen))
    return maximum


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_k > 6:
        raise SystemExit("brute-force certificate is deliberately capped at k=6")

    started = time.monotonic()
    rows: list[dict[str, object]] = []
    for k in range(2, args.max_k + 1):
        optimum, optimum_edges, checked = best_graph_bruteforce(k, PRIMES)
        cut_optimum, side = best_complete_bipartite(k, PRIMES)
        if optimum != cut_optimum:
            raise AssertionError(
                f"weighted triangle-free optimum differs from cut optimum at k={k}"
            )
        maximum_representations = replay_original_constraint(k, set(optimum_edges))
        if maximum_representations > 2:
            raise AssertionError(f"original constraint violated at k={k}")
        rows.append(
            {
                "prime_support": PRIMES[:k],
                "triangle_free_graphs_checked": checked,
                "optimum_numerator": optimum.numerator,
                "optimum_denominator": optimum.denominator,
                "optimum_edges_as_prime_products": [
                    [PRIMES[i], PRIMES[j]] for i, j in optimum_edges
                ],
                "complete_bipartite_side": [PRIMES[i] for i in side],
                "cut_optimum_numerator": cut_optimum.numerator,
                "cut_optimum_denominator": cut_optimum.denominator,
                "maximum_rank_two_representations_in_replay": maximum_representations,
            }
        )
        print(f"k={k} checked={checked} optimum={optimum}", flush=True)

    payload = {
        "schema_version": "amra.erdos538-squarefree-rank2-evidence.v1",
        "claim_scope": "finite replay supporting a separately proved scoped theorem",
        "resource_guard": {
            "required_slice": "openmath.slice",
            "observed_cgroup": Path("/proc/self/cgroup").read_text().strip(),
            "inside_openmath_slice": "openmath.slice" in Path("/proc/self/cgroup").read_text(),
        },
        "elapsed_seconds": time.monotonic() - started,
        "pid": os.getpid(),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"elapsed_seconds": payload["elapsed_seconds"], "rows": len(rows)}))


if __name__ == "__main__":
    main()
