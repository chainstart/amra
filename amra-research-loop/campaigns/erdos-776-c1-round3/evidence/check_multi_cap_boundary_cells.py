#!/usr/bin/env python3
"""Finite checker for the relaxed carry-cell model, not an actual-state scan."""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path


def C(n: int, k: int) -> int:
    return math.comb(n, k) if n >= k >= 0 else 0


def top(n: int, rank: int) -> int:
    lo, hi = rank - 1, max(2 * rank, rank)
    while C(hi, rank) <= n:
        hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if C(mid, rank) <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def rank2_word(n: int) -> tuple[int, int]:
    a = top(n, 2)
    return a, n - C(a, 2)


def U2_from_word(a: int, e: int) -> int:
    return C(a, 3) + C(e, 2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-r", type=int, default=180)
    ap.add_argument("--max-s", type=int, default=8)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    started = time.time()

    by_s = {s: {"admissible": 0, "failures": 0, "first_failure": None}
            for s in range(1, args.max_s + 1)}
    for r in range(4, args.max_r + 1):
        cr = C(r, 2)
        for a in range(2, r):
            for e in range(a):
                alpha = C(a, 2) + e
                tau = cr - alpha + 1
                p = U2_from_word(a, e) - tau + 1
                if p <= 0:
                    continue
                c = top(p, 3)
                for s in range(1, args.max_s + 1):
                    u = r + s
                    beta = C(u, 2) - tau
                    if beta < 0 or beta > cr:       # gamma3 < 0 chamber
                        continue
                    A, E = rank2_word(beta)
                    v = U2_from_word(A, E) - tau
                    if v <= 0 or v - p >= cr:       # gamma4 < 0 chamber
                        continue
                    d = top(v, 3)
                    margin = C(d, 4) - C(c + 1, 4) - C(a + 1, 3)
                    row = by_s[s]
                    row["admissible"] += 1
                    if margin < 0:
                        row["failures"] += 1
                        if row["first_failure"] is None:
                            row["first_failure"] = {
                                "r": r, "s": s, "a": a, "e": e,
                                "alpha": alpha, "beta": beta, "tau": tau,
                                "p": p, "v": v, "c": c, "d": d,
                                "gamma4": v - p - cr, "margin": margin,
                            }

    out = {
        "schema": "amra.evidence.multi-cap-relaxed-cells.v1",
        "scope": (
            "Exhaustive only in the finite relaxed complement model; it does "
            "not impose the dyadic q/h lattice and is not a proof."
        ),
        "parameters": vars(args),
        "by_s": by_s,
        "elapsed_seconds": time.time() - started,
    }
    Path(args.output).write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
