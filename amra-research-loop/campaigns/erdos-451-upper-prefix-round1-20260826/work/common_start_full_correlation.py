#!/usr/bin/env python3
"""Exact kill test for signed full-support common-start correlations."""

from __future__ import annotations

import argparse
import itertools
import json
import math


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for divisor in range(2, math.isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True


def scaled_correlation_range(k: int, moduli: tuple[int, ...]) -> dict[str, object]:
    offsets = tuple(p - k for p in moduli)
    period = math.prod(moduli)
    prefix = 0
    minimum = 0
    maximum = 0
    minimum_at = 0
    maximum_at = 0
    for n in range(period):
        value = math.prod(
            k if n % p < b else -b
            for p, b in zip(moduli, offsets, strict=True)
        )
        prefix += value
        if prefix < minimum:
            minimum = prefix
            minimum_at = n + 1
        if prefix > maximum:
            maximum = prefix
            maximum_at = n + 1
    assert prefix == 0
    correlation_range = maximum - minimum
    baseline = k ** (len(moduli) + 1)
    return {
        "k": k,
        "moduli": list(moduli),
        "offsets": list(offsets),
        "rank": len(moduli),
        "period": period,
        "scaled_maximum_interval_correlation": correlation_range,
        "candidate_baseline_k_to_r_plus_1": baseline,
        "ratio_to_candidate_baseline": correlation_range / baseline,
        "minimum_prefix_at": minimum_at,
        "maximum_prefix_at": maximum_at,
    }


def exhaustive(max_period: int) -> dict[str, object]:
    best = None
    best_by_rank: dict[int, dict[str, object]] = {}
    tested = 0
    for k in range(5, 31):
        interval_primes = [p for p in range(k + 1, 2 * k) if is_prime(p)]
        for rank in range(1, len(interval_primes) + 1):
            for moduli in itertools.combinations(interval_primes, rank):
                if math.prod(moduli) > max_period:
                    continue
                tested += 1
                row = scaled_correlation_range(k, moduli)
                if best is None or row["ratio_to_candidate_baseline"] > best["ratio_to_candidate_baseline"]:
                    best = row
                if (
                    rank not in best_by_rank
                    or row["ratio_to_candidate_baseline"]
                    > best_by_rank[rank]["ratio_to_candidate_baseline"]
                ):
                    best_by_rank[rank] = row
    assert best is not None
    return {
        "tested_systems": tested,
        "maximum_period": max_period,
        "maximum_ratio": best,
        "maximum_ratio_by_rank": {
            str(rank): row for rank, row in sorted(best_by_rank.items())
        },
    }


def selected_blocks(max_period: int) -> list[dict[str, object]]:
    rows = []
    for k in [32, 36, 42, 48, 54, 60, 70]:
        interval_primes = [p for p in range(k + 1, 2 * k) if is_prime(p)]
        for start in range(len(interval_primes)):
            block = []
            period = 1
            for p in interval_primes[start:]:
                if period * p > max_period:
                    break
                block.append(p)
                period *= p
            if len(block) >= 2:
                rows.append(scaled_correlation_range(k, tuple(block)))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-period", type=int, default=200_000)
    args = parser.parse_args()
    selected = selected_blocks(args.max_period)
    print(
        json.dumps(
            {
                "schema_version": "erdos451.common_start_full_correlation.v1",
                "exhaustive": exhaustive(args.max_period),
                "selected_block_count": len(selected),
                "selected_block_maximum": max(
                    selected, key=lambda row: row["ratio_to_candidate_baseline"]
                ),
                "boundary": (
                    "Exact finite falsification only. Passing systems do not prove the proposed "
                    "uniform signed-correlation inequality."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
