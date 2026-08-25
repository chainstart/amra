#!/usr/bin/env python3
"""Finite modular certificates for the equality case in Erdos #317.

If p is prime and n/2 < p <= n, reduction of
    sum_{k=1}^n delta_k L_n/k = 1
modulo p leaves only k=p.  Thus delta_p must be the inverse of L_n/p mod p.
When that residue is not +/-1, equality is impossible.
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import math
import os
import time
from pathlib import Path


def sieve(limit: int) -> tuple[list[int], bytearray]:
    is_prime = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if is_prime[p]:
            start = p * p
            is_prime[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [n for n in range(2, limit + 1) if is_prime[n]], is_prime


def prime_power_increments(limit: int, primes: list[int]) -> list[int]:
    increment = [1] * (limit + 1)
    for p in primes:
        power = p
        while power <= limit:
            increment[power] = p
            if power > limit // p:
                break
            power *= p
    return increment


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=100_000)
    parser.add_argument("--include-intervals", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_n < 5:
        raise SystemExit("max-n must be at least 5")

    started = time.monotonic()
    primes, _ = sieve(args.max_n)
    increments = prime_power_increments(args.max_n, primes)
    active_primes: list[int] = []
    next_prime_index = 0
    lcm_value = 1
    uncovered: list[int] = []
    intervals: list[dict[str, int]] = []

    for n in range(1, args.max_n + 1):
        lcm_value *= increments[n]
        if next_prime_index < len(primes) and primes[next_prime_index] == n:
            active_primes.append(n)
            next_prime_index += 1
        if n < 5:
            continue
        lower_index = bisect.bisect_right(active_primes, n // 2)
        witness: tuple[int, int, int] | None = None
        for p in reversed(active_primes[lower_index:]):
            quotient_mod_p = (lcm_value // p) % p
            required_delta = pow(quotient_mod_p, -1, p)
            if required_delta not in (1, p - 1):
                witness = (p, quotient_mod_p, required_delta)
                break
        if witness is None:
            uncovered.append(n)
            continue
        p, quotient_mod_p, required_delta = witness
        if (
            intervals
            and intervals[-1]["end_n"] + 1 == n
            and intervals[-1]["prime"] == p
            and intervals[-1]["lcm_quotient_mod_prime"] == quotient_mod_p
            and intervals[-1]["required_delta_mod_prime"] == required_delta
        ):
            intervals[-1]["end_n"] = n
        else:
            intervals.append(
                {
                    "start_n": n,
                    "end_n": n,
                    "prime": p,
                    "lcm_quotient_mod_prime": quotient_mod_p,
                    "required_delta_mod_prime": required_delta,
                }
            )

    interval_encoding = json.dumps(intervals, sort_keys=True, separators=(",", ":")).encode()
    payload = {
        "schema_version": "amra.erdos317-singleton-prime-certificate.v1",
        "claim": (
            "For every integer n in the certified range, no coefficients "
            "delta_1,...,delta_n in {-1,0,1} satisfy "
            "sum delta_k*lcm(1,...,n)/k = 1."
        ),
        "proof_rule": (
            "For the listed prime p with n/2 < p <= n, only k=p has maximal "
            "p-adic valuation. Modulo p, delta_p*(L_n/p)=1, but the required "
            "delta_p residue is neither 1 nor -1."
        ),
        "coverage_start": 5,
        "coverage_end": args.max_n,
        "uncovered": uncovered,
        "coverage_complete": not uncovered,
        "interval_count": len(intervals),
        "intervals_sha256": hashlib.sha256(interval_encoding).hexdigest(),
        "resource_guard": {
            "required_slice": "openmath.slice",
            "observed_cgroup": Path("/proc/self/cgroup").read_text().strip(),
            "inside_openmath_slice": "openmath.slice" in Path("/proc/self/cgroup").read_text(),
        },
        "elapsed_seconds": time.monotonic() - started,
        "pid": os.getpid(),
    }
    if args.include_intervals:
        payload["compressed_witness_intervals"] = intervals
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        json.dumps(
            {
                "coverage_complete": payload["coverage_complete"],
                "uncovered_count": len(uncovered),
                "interval_count": len(intervals),
                "elapsed_seconds": payload["elapsed_seconds"],
            }
        )
    )


if __name__ == "__main__":
    main()
