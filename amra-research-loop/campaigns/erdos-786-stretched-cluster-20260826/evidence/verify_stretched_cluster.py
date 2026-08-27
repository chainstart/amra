#!/usr/bin/env python3
"""Finite and exact-arithmetic guards for the stretched-cluster proof.

The universal theorem is proved symbolically in STRETCHED_CLUSTER_THEOREM.md.
This script checks projective-plane incidence parameters at small prime
orders and exact integer inequalities used by the quantitative ledger.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


def projective_points(q: int) -> list[tuple[int, int, int]]:
    points: set[tuple[int, int, int]] = set()
    for x, y, z in itertools.product(range(q), repeat=3):
        if (x, y, z) == (0, 0, 0):
            continue
        vector = (x, y, z)
        first = next(value for value in vector if value)
        inv = pow(first, -1, q)
        points.add(tuple((value * inv) % q for value in vector))
    return sorted(points)


def plane_rows(q: int) -> dict[str, int | bool]:
    points = projective_points(q)
    lines = projective_points(q)
    supports = [
        {point for point in points if sum(a * b for a, b in zip(line, point)) % q == 0}
        for line in lines
    ]
    intersections = [len(a & b) for a, b in itertools.combinations(supports, 2)]
    tau = None
    for size in range(q + 2):
        if any(all(set(candidate) & edge for edge in supports)
               for candidate in itertools.combinations(points, size)):
            tau = size
            break
    return {
        "q": q,
        "points": len(points),
        "lines": len(lines),
        "line_size": min(map(len, supports)),
        "pairwise_intersection_one": set(intersections) == {1},
        "matching_number": 1 if set(intersections) == {1} else -1,
        "transversal_number": tau if tau is not None else -1,
    }


def quantitative_row(k: int) -> dict[str, int | bool]:
    root_floor = math.isqrt(k) // 100
    ell_upper = root_floor + 1
    r_upper = ell_upper + 3
    private_bits = 12 * r_upper * ell_upper
    # It suffices to compare against N in [2^K,2^(K+1)).
    stretched_guard = (root_floor * 200) ** 2 > k + 1
    return {
        "K": k,
        "floor_sqrt_over_100": root_floor,
        "private_bit_upper": private_bits,
        "private_bits_below_K_over_4": 4 * private_bits < k,
        "all_N_stretched_guard": stretched_guard,
    }


def partition_row(q: int) -> dict[str, int | bool]:
    r = math.ceil(math.log2(q + 2)) + 1
    return {
        "q": q,
        "r": r,
        "available_unordered_nontrivial_bipartitions": 2 ** (r - 1) - 1,
        "covers_q_plus_one_lines": 2 ** (r - 1) - 1 >= q + 1,
    }


def main() -> None:
    source = Path(__file__)
    payload = {
        "status": "PASS",
        "scope": (
            "finite incidence replays and exact integer guards only; "
            "the all-parameter proof is STRETCHED_CLUSTER_THEOREM.md"
        ),
        "projective_planes": [plane_rows(q) for q in (2, 3, 5)],
        "partition_counts": [partition_row(q) for q in (2, 3, 5, 101, 1009)],
        "quantitative_guards": [quantitative_row(k) for k in (10**8, 10**10, 10**12)],
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    }
    assert all(row["pairwise_intersection_one"] for row in payload["projective_planes"])
    assert all(row["transversal_number"] == row["q"] + 1 for row in payload["projective_planes"])
    assert all(row["covers_q_plus_one_lines"] for row in payload["partition_counts"])
    assert all(row["private_bits_below_K_over_4"] for row in payload["quantitative_guards"])
    assert all(row["all_N_stretched_guard"] for row in payload["quantitative_guards"])
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
