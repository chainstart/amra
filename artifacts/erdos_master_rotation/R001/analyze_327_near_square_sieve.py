#!/usr/bin/env python3
"""Verify a near-square-divisor independent-set reduction for Erdős #327.

For the second question, join distinct a,b when a+b divides 2ab.  If a<b,
write a=gx, b=gy with gcd(x,y)=1 and put d=gcd(x+y,2).  The edge condition is
equivalent to (x+y)/d dividing g.  Consequently b is divisible by rs for
coprime r<s<2r with s odd.  Conversely every such rs is the larger primitive
endpoint of an edge.

Therefore integers divisible by no such rs form an independent set.  The
finite density experiment below is diagnostic only; it does not prove positive
asymptotic density.
"""

from __future__ import annotations

import argparse
import json
from math import gcd, isqrt
from pathlib import Path


def forbidden_bases(limit: int) -> dict[int, tuple[int, int]]:
    bases: dict[int, tuple[int, int]] = {}
    for smaller in range(2, isqrt(limit) + 1):
        upper = min(2 * smaller - 1, limit // smaller)
        for larger in range(smaller + 1, upper + 1):
            if larger % 2 == 0 or gcd(smaller, larger) != 1:
                continue
            base = smaller * larger
            bases.setdefault(base, (smaller, larger))
    return bases


def is_edge(a: int, b: int) -> bool:
    return a != b and (2 * a * b) % (a + b) == 0


def analyse(limit: int, verify_limit: int, checkpoints: list[int]) -> dict[str, object]:
    bases = forbidden_bases(limit)
    forbidden_multiple = bytearray(limit + 1)
    for base in bases:
        forbidden_multiple[base::base] = b"\1" * ((limit - base) // base + 1)

    prefix_good = [0] * (limit + 1)
    running = 0
    for value in range(1, limit + 1):
        running += int(not forbidden_multiple[value])
        prefix_good[value] = running

    primitive_converse_verified = True
    for base, (smaller, larger) in bases.items():
        x = 2 * smaller - larger
        y = larger
        primitive_smaller_endpoint = smaller * x
        if not (
            0 < x < y
            and gcd(x, y) == 1
            and primitive_smaller_endpoint < base
            and is_edge(primitive_smaller_endpoint, base)
        ):
            primitive_converse_verified = False
            break

    finite_edge_implication_verified = True
    good_values = [
        value for value in range(1, min(limit, verify_limit) + 1)
        if not forbidden_multiple[value]
    ]
    for index, a in enumerate(good_values):
        for b in good_values[index + 1:]:
            if is_edge(a, b):
                finite_edge_implication_verified = False
                break
        if not finite_edge_implication_verified:
            break

    selected_checkpoints = sorted({value for value in checkpoints if 1 <= value <= limit})
    densities = [
        {
            "N": value,
            "independent_set_size": prefix_good[value],
            "density": prefix_good[value] / value,
        }
        for value in selected_checkpoints
    ]
    passed = primitive_converse_verified and finite_edge_implication_verified
    return {
        "schema_version": "amra.erdos327.near_square_sieve.v1",
        "problem_id": "327",
        "question": "second",
        "limit": limit,
        "forbidden_base_count": len(bases),
        "characterisation": "larger primitive endpoints are exactly r*s with gcd(r,s)=1, r<s<2r, and s odd",
        "primitive_converse_verified": primitive_converse_verified,
        "finite_independence_verified_through": min(limit, verify_limit),
        "finite_edge_implication_verified": finite_edge_implication_verified,
        "densities": densities,
        "passed": passed,
        "scope_note": "The construction is rigorously independent for all N by the symbolic reduction, but the experiment does not prove that its lower asymptotic density is positive.",
    }


def parse_checkpoints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--verify-limit", type=int, default=2_000)
    parser.add_argument(
        "--checkpoints",
        default="1000,5000,20000,100000,500000,1000000",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = analyse(args.limit, args.verify_limit, parse_checkpoints(args.checkpoints))
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
