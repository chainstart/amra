#!/usr/bin/env python3
"""Exact finite audit of the divisor/discriminant route for Erdős 829."""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import defaultdict


def primes_through(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [p for p, flag in enumerate(sieve) if flag]


def factor(n: int, primes: list[int]) -> dict[int, int]:
    answer: dict[int, int] = {}
    left = n
    for p in primes:
        if p * p > left:
            break
        if left % p:
            continue
        exponent = 0
        while left % p == 0:
            exponent += 1
            left //= p
        answer[p] = exponent
    if left > 1:
        answer[left] = 1
    return answer


def divisor_discriminant_pairs(n: int) -> list[tuple[int, int]]:
    """Return unordered positive pairs x<=y with x^3+y^3=n."""
    pairs: list[tuple[int, int]] = []
    for s in range(2, math.isqrt(4 * n) + 1):
        if 4 * n % s:
            continue
        delta = 4 * n // s - s * s
        if delta < 0 or delta % 3:
            continue
        t2 = delta // 3
        t = math.isqrt(t2)
        if t * t != t2 or t >= s or (s - t) % 2:
            continue
        x = (s - t) // 2
        y = (s + t) // 2
        if x > 0 and x * x * x + y * y * y == n:
            pairs.append((x, y))
    return pairs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root-bound", type=int, default=1200)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()
    started = time.monotonic()
    bound = args.root_bound
    n_limit = bound**3
    representations: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for x in range(1, bound + 1):
        x3 = x**3
        for y in range(x, bound + 1):
            n = x3 + y**3
            if n > n_limit:
                break
            representations[n].append((x, y))

    repeated = [(len(pairs), n, pairs) for n, pairs in representations.items() if len(pairs) >= 2]
    repeated.sort(key=lambda item: (-item[0], item[1]))
    prime_table = primes_through(math.isqrt(n_limit) + 1)
    top_rows: list[dict[str, object]] = []
    all_verified = True
    for count, n, pairs in repeated[: args.top]:
        recovered = divisor_discriminant_pairs(n)
        verified = recovered == pairs
        all_verified = all_verified and verified
        fac = factor(n, prime_table)
        top_rows.append(
            {
                "n": n,
                "unordered_representation_count": count,
                "ordered_representation_count": 2 * count - sum(x == y for x, y in pairs),
                "pairs": pairs,
                "divisor_discriminant_pairs": recovered,
                "bijection_verified": verified,
                "factorization": {str(p): e for p, e in fac.items()},
                "two_to_omega": 2 ** len(fac),
            }
        )

    output = {
        "schema_version": "amra.erdos829.divisor-discriminant-audit.v1",
        "root_bound": bound,
        "complete_for_n_at_most": n_limit,
        "distinct_represented_n": len(representations),
        "n_with_at_least_two_unordered_representations": len(repeated),
        "maximum_unordered_representation_count": repeated[0][0] if repeated else 1,
        "top": top_rows,
        "all_reported_bijections_verified": all_verified,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
