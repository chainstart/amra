#!/usr/bin/env python3
"""Finite replay for the exact carry and residue lemmas in #354."""

from __future__ import annotations

import argparse
import json
import math
import os
from fractions import Fraction
from pathlib import Path


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def reachable_residues(values: list[int], modulus: int) -> set[int]:
    reachable = {0}
    for value in values:
        reachable |= {(old + value) % modulus for old in tuple(reachable)}
    return reachable


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=28)
    parser.add_argument("--max-q", type=int, default=64)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    # Exact rational truncations of non-eventually-zero binary patterns.  The
    # computation is finite evidence only; the accompanying note proves the
    # universal lemmas.
    samples = [
        Fraction(1, 1) + sum((Fraction(1, 2 ** (j * j + 1)) for j in range(1, 12)), Fraction()),
        Fraction(3, 2) + sum((Fraction(1, 2 ** (2**j)) for j in range(1, 7)), Fraction()),
        Fraction(7, 5),
    ]
    rows = []
    for theta in samples:
        values = [floor_fraction((2**s) * theta) for s in range(args.depth)]
        carries = [values[s + 1] - 2 * values[s] for s in range(args.depth - 1)]
        if any(bit not in (0, 1) for bit in carries):
            raise AssertionError("invalid binary carry")
        defects = [
            values[n + 1] - sum(values[: n + 1])
            for n in range(args.depth - 1)
        ]
        expected = [values[0] + sum(carries[: n + 1]) for n in range(args.depth - 1)]
        if defects != expected:
            raise AssertionError("carry-defect identity failed")
        coverage = {
            str(q): len(reachable_residues(values, q))
            for q in range(2, args.max_q + 1)
        }
        rows.append({
            "theta": f"{theta.numerator}/{theta.denominator}",
            "values": values,
            "carries": carries,
            "defects": defects,
            "residue_coverage_counts": coverage,
        })
    cgroup = Path("/proc/self/cgroup").read_text().strip()
    payload = {
        "schema_version": "amra.erdos354-carry-residue-replay.v1",
        "claim_scope": "finite replay supporting separately proved identities",
        "depth": args.depth,
        "max_modulus": args.max_q,
        "rows": rows,
        "resource_guard": {
            "observed_cgroup": cgroup,
            "inside_openmath_slice": "openmath.slice" in cgroup,
        },
        "pid": os.getpid(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"samples": len(rows), "depth": args.depth, "max_q": args.max_q}))


if __name__ == "__main__":
    main()
