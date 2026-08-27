#!/usr/bin/env python3
"""Exact finite search for primitive full-moment Vandermonde witnesses.

For distinct integer nodes d_i, the primitive integer vector annihilating
moments 0,...,q-2 is proportional to 1/F'(d_i).  This script records its
L1 norm for structured and extremal small node sets, and for actual-prime
offset blocks.  It is falsification evidence only, not an asymptotic proof.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math


def primitive_weights(nodes: tuple[int, ...]) -> tuple[int, ...]:
    deriv = []
    for i, x in enumerate(nodes):
        value = 1
        for j, y in enumerate(nodes):
            if i != j:
                value *= x - y
        deriv.append(value)
    common = 1
    for value in deriv:
        common = math.lcm(common, abs(value))
    weights = [common // value for value in deriv]
    divisor = 0
    for value in weights:
        divisor = math.gcd(divisor, abs(value))
    return tuple(value // divisor for value in weights)


def primes_up_to(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * (n + 1)
    if n >= 0:
        sieve[0] = 0
    if n >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(n) + 1):
        if sieve[p]:
            sieve[p * p : n + 1 : p] = b"\x00" * (((n - p * p) // p) + 1)
    return [i for i, flag in enumerate(sieve) if flag]


def structured(max_q: int) -> list[dict[str, object]]:
    rows = []
    for q in range(2, max_q + 1):
        families = {
            "consecutive": tuple(range(q)),
            "paired_gap3": tuple(sorted(3 * j + e for j in range((q + 1) // 2) for e in (0, 1)))[:q],
            "squares": tuple(j * j for j in range(q)),
        }
        for name, nodes in families.items():
            weights = primitive_weights(nodes)
            rows.append(
                {
                    "q": q,
                    "family": name,
                    "nodes": nodes,
                    "weights": weights,
                    "l1": sum(abs(x) for x in weights),
                    "root_moments_zero": all(
                        sum(w * d**t for w, d in zip(weights, nodes)) == 0
                        for t in range(q - 1)
                    ),
                }
            )
    return rows


def extremal(max_q: int, width: int) -> list[dict[str, object]]:
    rows = []
    for q in range(2, max_q + 1):
        best = None
        # Translation does not change the weights, so anchor the first node at 0.
        for tail in itertools.combinations(range(1, width + 1), q - 1):
            nodes = (0,) + tail
            weights = primitive_weights(nodes)
            l1 = sum(abs(x) for x in weights)
            candidate = (l1, nodes, weights)
            if best is None or candidate < best:
                best = candidate
        assert best is not None
        rows.append({"q": q, "width": width, "l1": best[0], "nodes": best[1], "weights": best[2]})
    return rows


def actual_blocks(max_k: int, max_q: int) -> list[dict[str, object]]:
    prime_set = set(primes_up_to(2 * max_k))
    rows = []
    for k in range(4, max_k + 1):
        scale = 1
        while scale < k:
            nodes = tuple(
                d for d in range(scale, min(2 * scale, k)) if k + d in prime_set
            )
            if 2 <= len(nodes) <= max_q:
                weights = primitive_weights(nodes)
                rows.append(
                    {
                        "k": k,
                        "scale": scale,
                        "q": len(nodes),
                        "nodes": nodes,
                        "l1": sum(abs(x) for x in weights),
                        "log_l1_per_q": math.log(sum(abs(x) for x in weights)) / len(nodes),
                    }
                )
            scale *= 2
    rows = [row for row in rows if row["q"] >= 4]
    best_by_q: dict[int, dict[str, object]] = {}
    for row in rows:
        q = int(row["q"])
        if q not in best_by_q or (
            row["log_l1_per_q"], row["k"], row["scale"]
        ) < (
            best_by_q[q]["log_l1_per_q"],
            best_by_q[q]["k"],
            best_by_q[q]["scale"],
        ):
            best_by_q[q] = row
    return [best_by_q[q] for q in sorted(best_by_q)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-q", type=int, default=9)
    parser.add_argument("--width", type=int, default=18)
    parser.add_argument("--max-k", type=int, default=300)
    args = parser.parse_args()
    result = {
        "scope": "finite exact falsification only",
        "structured": structured(args.max_q),
        "extremal": extremal(args.max_q, args.width),
        "actual_prime_blocks_smallest_log_l1_per_q": actual_blocks(args.max_k, args.max_q),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
