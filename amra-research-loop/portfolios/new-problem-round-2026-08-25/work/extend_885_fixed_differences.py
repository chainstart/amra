#!/usr/bin/env python3
"""Enumerate every N having a fixed list of factor differences."""

from __future__ import annotations

import argparse
import json
import math


def factor_pair(n: int, d: int) -> tuple[int, int] | None:
    disc = d * d + 4 * n
    y = math.isqrt(disc)
    if y * y != disc or y <= d or (y - d) % 2:
        return None
    a = (y - d) // 2
    b = (y + d) // 2
    return (a, b) if a > 0 and a * b == n else None


def divisors(n: int) -> list[int]:
    result: list[int] = []
    for d in range(1, math.isqrt(n) + 1):
        if n % d == 0:
            result.append(d)
            if d * d != n:
                result.append(n // d)
    return sorted(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("differences", type=int, nargs="+")
    args = parser.parse_args()
    ds = sorted(set(args.differences))
    if len(ds) < 2 or ds[0] < 0:
        raise SystemExit("need at least two distinct nonnegative differences")

    d0, d1 = ds[:2]
    gap = d1 * d1 - d0 * d0
    candidates: dict[int, dict[int, tuple[int, int]]] = {}
    pair_factorizations = 0
    for u in divisors(gap):
        v = gap // u
        if u >= v or (u + v) % 2:
            continue
        # y1-y0=u and y1+y0=v.
        y0 = (v - u) // 2
        y1 = (v + u) // 2
        pair_factorizations += 1
        delta = y0 * y0 - d0 * d0
        if delta <= 0 or delta % 4:
            continue
        n = delta // 4
        certificate = {d: factor_pair(n, d) for d in ds}
        if all(pair is not None for pair in certificate.values()):
            candidates[n] = {d: pair for d, pair in certificate.items() if pair is not None}

    print(
        json.dumps(
            {
                "schema_version": "amra.erdos885.fixed-difference-extension.v1",
                "differences": ds,
                "first_pair_square_gap": gap,
                "admissible_factorizations_checked": pair_factorizations,
                "complete": True,
                "common_n_count": len(candidates),
                "common_n": [
                    {
                        "n": n,
                        "four_n": 4 * n,
                        "factor_pairs": {str(d): pair for d, pair in certificate.items()},
                    }
                    for n, certificate in sorted(candidates.items())
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
