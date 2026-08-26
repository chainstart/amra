#!/usr/bin/env python3
"""Exact finite diagnostics for M10 anchored two-prime systems.

For p=k+b the common-start coordinate is allowed iff s mod p < b.
The program scans actual prime pairs, computes their exact cyclic gap and
distinguished successor after s=k-1, and emits compact JSON.  It is finite
evidence only and is intended to run under openmath-memory-guard.
"""

from __future__ import annotations

import argparse
import json
import math
import resource
import time


def primes_below(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * n
    if n:
        sieve[0] = 0
    if n > 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p : n : p] = b"\x00" * (((n - 1 - p * p) // p) + 1)
    return [p for p in range(2, n) if sieve[p]]


def pair_stats(k: int, q: int, p: int) -> dict[str, float | int]:
    assert k < q < p < 2 * k
    aq = q - k
    ap = p - k
    period = p * q
    allowed = [s for s in range(period) if s % q < aq and s % p < ap]
    gaps = [allowed[i + 1] - allowed[i] for i in range(len(allowed) - 1)]
    gaps.append(period + allowed[0] - allowed[-1])
    max_gap = max(gaps)
    start = k - 1
    successor = next((s for s in allowed if s > start), period + allowed[0])
    reciprocal_density = period / (aq * ap)
    return {
        "k": k,
        "q": q,
        "p": p,
        "prime_gap": p - q,
        "q_offset": aq,
        "p_offset": ap,
        "period": period,
        "allowed_count": len(allowed),
        "max_cyclic_gap": max_gap,
        "max_gap_density_ratio": max_gap / reciprocal_density,
        "distinguished_successor_s": successor,
        "distinguished_distance": successor - start,
        "distinguished_density_ratio": (successor - start) / reciprocal_density,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ks", default="100,200,400,800,1200,1600,2000")
    parser.add_argument("--all-adjacent-limit", type=int, default=800)
    args = parser.parse_args()
    started = time.time()
    ks = [int(x) for x in args.ks.split(",") if x]
    plist = primes_below(2 * max(ks) + 1)
    rows = []
    for k in ks:
        ps = [p for p in plist if 3 * k // 2 < p < 2 * k]
        adjacent = list(zip(ps, ps[1:]))
        if not adjacent:
            continue
        q, p = min(adjacent, key=lambda z: z[1] - z[0])
        rows.append({"selection": "minimum_gap_upper_half", **pair_stats(k, q, p)})
        if k <= args.all_adjacent_limit:
            stats = [pair_stats(k, q0, p0) for q0, p0 in adjacent]
            worst = max(stats, key=lambda z: z["max_gap_density_ratio"])
            rows.append({"selection": "worst_ratio_upper_half", **worst})
    usage = resource.getrusage(resource.RUSAGE_SELF)
    print(
        json.dumps(
            {
                "status": "finite_exact",
                "coordinate": "s mod p in [0,p-k-1]",
                "rows": rows,
                "runtime": {
                    "wall_seconds": time.time() - started,
                    "max_rss_kib": usage.ru_maxrss,
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
