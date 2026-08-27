#!/usr/bin/env python3
"""Finite exhaustive replay of the affine echo-to-multiples equivalence."""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations
from pathlib import Path


def finite_check(c: int, b: int, selected: tuple[int, ...], limit: int) -> int:
    direct = {
        k
        for r in selected
        for step in (c * r + b,)
        for k in range(r, limit + 1, step)
    }
    transformed = {
        k
        for k in range(1, limit + 1)
        if any((c * k + b) % (c * r + b) == 0 for r in selected)
    }
    assert direct == transformed
    return len(direct)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    checks = 0
    for c in range(2, 13):
        for b in range(-c + 1, c + 1):
            if math.gcd(b, c) != 1:
                continue
            candidates = tuple(r for r in range(2, 9) if c * r + b > r)
            for size in range(0, 4):
                for selected in combinations(candidates, size):
                    deleted = finite_check(c, b, selected, args.limit)
                    checks += 1
                    if size in (0, 3):
                        rows.append({"c": c, "b": b, "selected": selected, "deleted_through_limit": deleted})
    payload = {
        "schema_version": "erdos-25.affine-echo-mapping-replay.v1",
        "status": "passed",
        "limit": args.limit,
        "exact_subset_checks": checks,
        "sample_rows": rows,
        "proved_identity": "k=r+h(cr+b) iff (cr+b) divides (ck+b), when gcd(b,c)=1",
        "interpretation_limit": "Finite replay checks the algebraic map; logarithmic-density existence uses the published Davenport--Erdos theorem and the written squeeze proof.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "passed", "exact_subset_checks": checks, "limit": args.limit}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
