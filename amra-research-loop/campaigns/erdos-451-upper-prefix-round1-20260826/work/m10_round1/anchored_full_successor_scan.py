#!/usr/bin/env python3
"""Finite prefix sieve for the actual M10 distinguished successor.

The search coordinate is s=n-(k+1); allowed means s mod p < p-k for every
prime k<p<2k, and the distinguished start is s=k-1.  Exact finite data only.
Run under openmath-memory-guard.
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


def first_successor(k: int, primes: list[int], limit: int) -> dict[str, object]:
    start = k - 1
    alive = bytearray(b"\x01") * (limit + 1)
    alive[: start + 1] = b"\x00" * (start + 1)
    interval_primes = [p for p in primes if k < p < 2 * k]
    for p in interval_primes:
        b = p - k
        first_block = max(0, (start + 1 - b) // p)
        for j in range(first_block, limit // p + 2):
            lo = j * p + b
            hi = min((j + 1) * p, limit + 1)
            if hi > start + 1 and lo < limit + 1:
                lo = max(lo, start + 1)
                alive[lo:hi] = b"\x00" * (hi - lo)
    try:
        distance = alive[start + 1 :].index(1) + 1
        s = start + distance
        found = True
    except ValueError:
        distance = None
        s = None
        found = False
    reciprocal_density_log = sum(math.log(p / (p - k)) for p in interval_primes)
    return {
        "k": k,
        "prime_count": len(interval_primes),
        "limit": limit,
        "found": found,
        "successor_s": s,
        "successor_n": None if s is None else s + k + 1,
        "distance_after_start": distance,
        "log_reciprocal_density": reciprocal_density_log,
        "distance_over_density_scale": None
        if distance is None
        else distance / math.exp(reciprocal_density_log),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ks", default="20,30,50,80,100,150,200,300,400,600,800,1000")
    parser.add_argument("--limit", type=int, default=10_000_000)
    args = parser.parse_args()
    ks = [int(x) for x in args.ks.split(",") if x]
    primes = primes_below(2 * max(ks) + 1)
    started = time.time()
    rows = [first_successor(k, primes, args.limit) for k in ks]
    usage = resource.getrusage(resource.RUSAGE_SELF)
    print(
        json.dumps(
            {
                "status": "finite_exact",
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
