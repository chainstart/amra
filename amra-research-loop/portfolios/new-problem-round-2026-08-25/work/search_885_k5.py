#!/usr/bin/env python3
"""Exact bounded K_{5,5} search for Erdős Problem 885.

For every N <= limit, construct D(N) from all positive factor pairs.  If five
integers share five differences, then they share some four-difference key.  We
index those keys and then search for a fifth common difference.  The search is
complete up to ``limit`` unless ``--max-key-group`` truncates a key group; the
JSON output records whether any truncation occurred.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from collections import defaultdict


def factor_differences(limit: int) -> list[list[int]]:
    differences: list[list[int]] = [[] for _ in range(limit + 1)]
    for a in range(1, math.isqrt(limit) + 1):
        for b in range(a, limit // a + 1):
            differences[a * b].append(b - a)
    return differences


def factor_pair(n: int, d: int) -> tuple[int, int] | None:
    disc = d * d + 4 * n
    y = math.isqrt(disc)
    if y * y != disc or (y - d) % 2:
        return None
    a = (y - d) // 2
    b = (y + d) // 2
    if a <= 0 or a * b != n:
        return None
    return a, b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=200_000)
    parser.add_argument("--max-key-group", type=int, default=20_000)
    parser.add_argument(
        "--buckets",
        type=int,
        default=32,
        help="process four-difference keys in this many deterministic hash buckets",
    )
    args = parser.parse_args()
    started = time.monotonic()

    differences = factor_differences(args.limit)
    eligible = 0
    max_degree = 0
    for n, ds in enumerate(differences):
        if len(ds) < 5:
            continue
        eligible += 1
        max_degree = max(max_degree, len(ds))

    solution: dict[str, object] | None = None
    candidate_keys = 0
    emitted_memberships = 0
    distinct_four_keys = 0
    truncated_key_count = 0
    completed_buckets = 0
    for bucket_id in range(args.buckets):
        four_to_n: dict[tuple[int, int, int, int], list[int]] = defaultdict(list)
        truncated_keys: set[tuple[int, int, int, int]] = set()
        for n, ds in enumerate(differences):
            if len(ds) < 5:
                continue
            for key in itertools.combinations(ds, 4):
                if hash(key) % args.buckets != bucket_id:
                    continue
                group = four_to_n[key]
                if len(group) < args.max_key_group:
                    group.append(n)
                    emitted_memberships += 1
                else:
                    truncated_keys.add(key)

        distinct_four_keys += len(four_to_n)
        truncated_key_count += len(truncated_keys)
        for key, ns in four_to_n.items():
            if len(ns) < 5:
                continue
            candidate_keys += 1
            extra_to_n: dict[int, list[int]] = defaultdict(list)
            key_set = set(key)
            for n in ns:
                for d in differences[n]:
                    if d not in key_set:
                        extra_to_n[d].append(n)
            for extra, witnesses in extra_to_n.items():
                if len(witnesses) < 5:
                    continue
                chosen_n = witnesses[:5]
                chosen_d = [*key, extra]
                certificate = {
                    str(n): {
                        str(d): factor_pair(n, d)
                        for d in chosen_d
                    }
                    for n in chosen_n
                }
                if all(pair is not None for row in certificate.values() for pair in row.values()):
                    solution = {
                        "N": chosen_n,
                        "differences": chosen_d,
                        "factor_pairs": certificate,
                        "four_key_bucket": bucket_id,
                    }
                    break
            if solution is not None:
                break
        completed_buckets += 1
        if solution is not None:
            break

    output = {
        "schema_version": "amra.erdos885.k5-bounded-search.v1",
        "limit": args.limit,
        "hash_bucket_count": args.buckets,
        "completed_hash_buckets": completed_buckets,
        "complete_through_limit": solution is None
        and completed_buckets == args.buckets
        and truncated_key_count == 0,
        "truncated_key_count": truncated_key_count,
        "eligible_n_count": eligible,
        "max_factor_difference_degree": max_degree,
        "four_key_count": distinct_four_keys,
        "four_key_memberships": emitted_memberships,
        "candidate_four_keys_with_at_least_five_n": candidate_keys,
        "solution": solution,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
