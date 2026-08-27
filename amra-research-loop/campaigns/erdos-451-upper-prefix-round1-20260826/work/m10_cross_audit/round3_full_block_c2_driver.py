#!/usr/bin/env python3
"""Finite exact-C=2 scan driver for complete actual 451 dyadic blocks.

The C++ scanner remains the source of exact membership and the Fejer sum.
This driver only enumerates candidate (k, Delta) pairs, precomputes the exact
integer h, applies declared affordability/128-bit-safety caps, and collates
the JSON results.  Nothing here is an asymptotic argument.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from collections import Counter, defaultdict


I128_MAX = (1 << 127) - 1


def primes_below(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * limit
    if limit:
        sieve[0] = 0
    if limit > 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(limit - 1) + 1):
        if sieve[p]:
            sieve[p * p : limit : p] = b"\x00" * (((limit - 1 - p * p) // p) + 1)
    return [p for p in range(2, limit) if sieve[p]]


def candidates(min_k: int, max_k: int, max_q: int, max_h: int) -> list[dict]:
    out = []
    for k in range(min_k, max_k + 1):
        primes = primes_below(2 * k)
        delta = 1
        while delta < k:
            moduli = [p for p in primes if delta <= p - k < 2 * delta]
            q = len(moduli)
            if 3 <= q <= max_q:
                period = math.prod(moduli)
                width_product = math.prod(p - k for p in moduli)
                c_power = 2**q
                numerator = k * k * c_power * period
                h = (numerator + width_product - 1) // width_product
                if (
                    numerator <= I128_MAX
                    and h <= (1 << 63) - 1
                    and 2 * h < period
                    and h <= max_h
                ):
                    out.append(
                        {
                            "k": k,
                            "Delta": delta,
                            "q": q,
                            "h": h,
                            "P": period,
                            "D": width_product,
                        }
                    )
            delta *= 2
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True)
    parser.add_argument("--min-k", type=int, default=30)
    parser.add_argument("--max-k", type=int, default=250)
    parser.add_argument("--max-q", type=int, default=10)
    parser.add_argument("--max-h", type=int, default=5_000_000)
    parser.add_argument("--total-h-budget", type=int, default=30_000_000)
    parser.add_argument("--list-only", action="store_true")
    args = parser.parse_args()

    pool = candidates(args.min_k, args.max_k, args.max_q, args.max_h)
    # Give larger ranks priority, then spend the remaining exact-H budget on
    # the cheapest blocks.  This rule is fixed before looking at any S value.
    pool.sort(key=lambda x: (-x["q"], x["h"], x["k"], x["Delta"]))
    if args.list_only:
        by_q = defaultdict(list)
        for case in pool:
            by_q[case["q"]].append(case)
        print(
            json.dumps(
                {
                    "classification": "finite_candidate_inventory_only",
                    "eligible_candidates": len(pool),
                    "minimum_h_by_q": {
                        str(q): min(rows, key=lambda row: row["h"])
                        for q, rows in sorted(by_q.items())
                    },
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    chosen = []
    spent = 0
    for case in pool:
        if spent + case["h"] > args.total_h_budget:
            continue
        chosen.append(case)
        spent += case["h"]

    results = []
    for case in chosen:
        proc = subprocess.run(
            [args.binary, str(case["k"]), str(case["Delta"]), "2"],
            text=True,
            check=True,
            capture_output=True,
        )
        row = json.loads(proc.stdout)
        assert row["q"] == case["q"] and int(row["h"]) == case["h"]
        results.append(row)

    by_q = defaultdict(list)
    for row in results:
        by_q[row["q"]].append(row)
    maxima = {
        str(q): max(rows, key=lambda r: r["S_long_double"])
        for q, rows in sorted(by_q.items())
    }
    failures = [row for row in results if not row["S_lt_2"]]
    summary = {
        "classification": "finite_complete_actual_blocks_exact_membership_only",
        "selection_rule": "all affordable candidates sorted by (-q,h,k,Delta), greedily under total_h_budget",
        "parameters": {
            "C": 2,
            "min_k": args.min_k,
            "max_k": args.max_k,
            "max_q": args.max_q,
            "max_h": args.max_h,
            "total_h_budget": args.total_h_budget,
        },
        "eligible_candidates": len(pool),
        "eligible_rank_histogram": dict(sorted(Counter(x["q"] for x in pool).items())),
        "scanned_candidates": len(results),
        "scanned_rank_histogram": dict(sorted(Counter(x["q"] for x in chosen).items())),
        "sum_h": sum(int(x["h"]) for x in results),
        "failures": failures,
        "max_S_by_q": maxima,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
