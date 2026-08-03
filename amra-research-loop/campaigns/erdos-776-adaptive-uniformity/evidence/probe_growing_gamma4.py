#!/usr/bin/env python3
"""Exact bounded survivor falsifier for growing-promotion gamma4 positivity."""

from __future__ import annotations

import argparse
import hashlib
import json
from math import comb
from pathlib import Path

from probe_growing_promotions import admissible


def upper(number: int, rank: int) -> int:
    if number < 0:
        raise ValueError(number)
    remaining = number
    ceiling: int | None = None
    answer = 0
    for lower in range(rank, 0, -1):
        if remaining == 0:
            break
        left = lower - 1
        if ceiling is None:
            right = lower
            while comb(right, lower) <= remaining:
                left = right
                right *= 2
        else:
            right = ceiling
        while left + 1 < right:
            middle = (left + right) // 2
            if comb(middle, lower) <= remaining:
                left = middle
            else:
                right = middle
        if left >= lower:
            remaining -= comb(left, lower)
            answer += comb(left, lower + 1)
            ceiling = left
    assert remaining == 0
    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q-min", type=int, default=61)
    parser.add_argument("--q-max", type=int, default=160)
    parser.add_argument("--c-min", type=int, default=6)
    parser.add_argument("--c-max", type=int, default=10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    retained = 0
    counts: dict[int, int] = {}
    minima: dict[int, dict[str, int]] = {}
    nonpositive: list[dict[str, int]] = []
    for q in range(args.q_min, args.q_max + 1):
        for c in range(args.c_min, args.c_max + 1):
            for r in range(q):
                for u in range(q + c):
                    state = admissible(q, c, r, u)
                    if state is None:
                        continue
                    retained += 1
                    counts[c] = counts.get(c, 0) + 1
                    z = comb(q, 3) + comb(r, 2)
                    gamma4 = upper(state["y"], 3) - upper(state["x"], 3) - z - 1
                    row = {**state, "gamma4": gamma4}
                    if c not in minima or gamma4 < minima[c]["gamma4"]:
                        minima[c] = row
                    if gamma4 <= 0 and len(nonpositive) < 20:
                        nonpositive.append(row)

    payload = {
        "classification": "finite_exact_survivor_falsifier",
        "domain": vars(args) | {"output": str(args.output)},
        "retained": retained,
        "counts_by_c": {str(c): counts[c] for c in sorted(counts)},
        "minimum_gamma4_by_c": {str(c): minima[c] for c in sorted(minima)},
        "nonpositive_count_capped_at_20": len(nonpositive),
        "first_nonpositive": nonpositive,
        "unbounded_claim_made": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    args.output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
