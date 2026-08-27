#!/usr/bin/env python3
"""Independent replay of the exact predicates and support arithmetic."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


def primes_below(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * limit
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit - 1) + 1):
        if sieve[p]:
            sieve[p * p : limit : p] = b"\x00" * (((limit - 1 - p * p) // p) + 1)
    return [p for p in range(2, limit) if sieve[p]]


def survives(n: int, k: int, primes: list[int]) -> bool:
    return all(not (1 <= n % p <= k) for p in primes)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    data = json.loads(raw)
    checks: list[dict[str, object]] = []
    for row in data["exact_scans"]:
        k = int(row["k"])
        ps = [p for p in primes_below(2 * k) if p > k]
        assert len(ps) == row["prime_count"]
        recomputed = sum(math.log(p / (p - k)) for p in ps)
        assert abs(recomputed - row["log_inverse_density"]) < 1e-11
        first = row["first_survivor"]
        if first is not None:
            first = int(first)
            assert survives(first, k, ps)
            # Boundary-focused replay catches off-by-one errors independently.
            for n in range(max(2 * k + 1, first - 10000), first):
                assert not survives(n, k, ps)
        checks.append({"k": k, "predicate_replayed": True, "boundary_replay": 10000})

    log4 = math.log(4.0)
    for row in data["support_barrier"]:
        k = int(row["k"])
        expected = math.floor((log4 * k / math.log(k)) / math.log(k))
        assert expected == row["max_squarefree_support_below_H"]

    result = {
        "schema_version": "erdos451.crt_admission.audit.v1",
        "status": "pass",
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "checks": checks,
        "scope": "Predicate, density, candidate boundary, and support arithmetic only; no asymptotic estimate is certified.",
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
