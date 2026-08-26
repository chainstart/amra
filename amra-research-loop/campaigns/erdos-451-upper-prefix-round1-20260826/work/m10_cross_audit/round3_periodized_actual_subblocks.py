#!/usr/bin/env python3
"""Finite L=2 periodized-majorant scan on actual-prime dyadic subblocks.

Every q=3..5 subblock on the selected k-grid is included when its complete
small-frequency box has at most --word-cap words and some tested C gives
1 <= h=floor(k^2 C^q P/prod(d_i)) < P/2.  Results are empirical floats;
the exact normalization is checked separately in round3_periodized_rescue_check.py.
"""

from __future__ import annotations

import argparse
import bisect
import itertools
import json
import math


def primes_below(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * n
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p : n : p] = b"\x00" * (((n - 1 - p * p) // p) + 1)
    return [p for p in range(2, n) if sieve[p]]


def centered(value: int, modulus: int) -> int:
    value %= modulus
    return value if 2 * value <= modulus else value - modulus


def scan_subblock(k: int, delta: int, moduli: tuple[int, ...],
                  c_grid: tuple[int, ...]) -> dict[str, object]:
    q = len(moduli)
    offsets = tuple(p - k for p in moduli)
    period = math.prod(moduli)
    width_product = math.prod(offsets)
    b = math.floor((delta - 1) / 2) + 0.5
    n = math.floor(b)
    residues = tuple(range(-n, n + 1))
    beta = {a: (b - abs(a)) / (b * b) for a in residues}
    bases = []
    for p in moduli:
        cofactor = period // p
        bases.append(cofactor * pow(cofactor, -1, p))

    shells: list[tuple[int, float]] = []
    for word in itertools.product(residues, repeat=q):
        lift = abs(centered(sum(a * base for a, base in zip(word, bases)), period))
        weight = math.prod(beta[a] for a in word)
        shells.append((lift, weight))
    shells.sort()
    locations = [item[0] for item in shells]
    prefix_weight = [0.0]
    prefix_weighted_location = [0.0]
    for location, weight in shells:
        prefix_weight.append(prefix_weight[-1] + weight)
        prefix_weighted_location.append(prefix_weighted_location[-1] + weight * location)

    values = []
    for c_num in c_grid:
        h = (k * k * (c_num ** q) * period) // ((100 ** q) * width_product)
        if h < 1 or 2 * h >= period:
            continue
        stop = bisect.bisect_left(locations, h)
        mass = prefix_weight[stop] - prefix_weighted_location[stop] / h
        s_value = period * mass / h
        values.append({"C": c_num / 100, "h": h, "S": s_value, "S_lt_2": s_value < 2})

    passing = [row for row in values if row["S_lt_2"]]
    return {
        "k": k,
        "Delta": delta,
        "q": q,
        "moduli": moduli,
        "offsets": offsets,
        "word_count": len(shells),
        "tested": values,
        "first_grid_C_with_S_lt_2": passing[0]["C"] if passing else None,
        "first_grid_S_lt_2": passing[0]["S"] if passing else None,
        "minimum_tested_S": min((row["S"] for row in values), default=None),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-k", type=int, default=50)
    parser.add_argument("--max-k", type=int, default=250)
    parser.add_argument("--step", type=int, default=10)
    parser.add_argument("--word-cap", type=int, default=1_000_000)
    args = parser.parse_args()
    c_grid = tuple(range(105, 601, 5))
    primes = primes_below(2 * args.max_k + 1)
    rows = []
    skipped_word_cap = 0
    skipped_no_valid_h = 0
    for k in range(args.min_k, args.max_k + 1, args.step):
        blocks: dict[int, list[int]] = {}
        for p in primes:
            if p <= k:
                continue
            if p >= 2 * k:
                break
            d = p - k
            delta = 1 << (d.bit_length() - 1)
            blocks.setdefault(delta, []).append(p)
        for delta, block in sorted(blocks.items()):
            b = math.floor((delta - 1) / 2) + 0.5
            side = 2 * math.floor(b) + 1
            for q in range(3, min(5, len(block)) + 1):
                if side ** q > args.word_cap:
                    skipped_word_cap += math.comb(len(block), q)
                    continue
                for subblock in itertools.combinations(block, q):
                    period = math.prod(subblock)
                    width_product = math.prod(p - k for p in subblock)
                    valid = any(
                        1 <= (h_value := (k * k * (c_num ** q) * period)
                              // ((100 ** q) * width_product))
                        and 2 * h_value < period
                        for c_num in c_grid
                    )
                    if not valid:
                        skipped_no_valid_h += 1
                        continue
                    rows.append(scan_subblock(k, delta, subblock, c_grid))

    passing = [row for row in rows if row["first_grid_C_with_S_lt_2"] is not None]
    failing = [row for row in rows if row["first_grid_C_with_S_lt_2"] is None]
    thresholds = [row["first_grid_C_with_S_lt_2"] for row in passing]
    worst_threshold = max(thresholds, default=None)
    worst_rows = [row for row in passing if row["first_grid_C_with_S_lt_2"] == worst_threshold]

    def brief(row: dict[str, object]) -> dict[str, object]:
        return {
            key: row[key]
            for key in (
                "k",
                "Delta",
                "q",
                "moduli",
                "offsets",
                "word_count",
                "first_grid_C_with_S_lt_2",
                "first_grid_S_lt_2",
                "minimum_tested_S",
            )
        }
    print(json.dumps({
        "classification": "finite_actual_prime_subblock_scan_only",
        "parameters": vars(args) | {"C_grid": [c_grid[0] / 100, c_grid[-1] / 100, 0.05],
                                    "h_arithmetic": "exact integer floor"},
        "scanned_subblocks": len(rows),
        "q_histogram": {
            str(q): sum(row["q"] == q for row in rows) for q in range(3, 6)
        },
        "skipped_by_word_cap": skipped_word_cap,
        "skipped_no_valid_h_on_grid": skipped_no_valid_h,
        "subblocks_with_some_S_lt_2": len(passing),
        "subblocks_without_S_lt_2_on_grid": len(failing),
        "worst_first_grid_C": worst_threshold,
        "worst_threshold_examples": [brief(row) for row in worst_rows[:5]],
        "smallest_observed_S": min(
            ({"S": row["minimum_tested_S"], "row": brief(row)} for row in rows),
            key=lambda item: item["S"],
            default=None,
        ),
        "failed_examples": [brief(row) for row in failing[:5]],
    }, indent=2))


if __name__ == "__main__":
    main()
