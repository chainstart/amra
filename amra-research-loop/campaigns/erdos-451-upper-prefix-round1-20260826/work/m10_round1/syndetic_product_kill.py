#!/usr/bin/env python3
"""Exhaust the candidate W(A intersect B)+1 <= (W(A)+1)(W(B)+1).

This is a finite kill test for a possible two-parameter block composition.
The sets are arbitrary nonempty periodic subsets on coprime small moduli.
"""

from __future__ import annotations

import itertools
import json
import math
import resource
import time


def max_gap(modulus: int, residues: tuple[int, ...] | list[int]) -> int:
    xs = sorted(residues)
    return max([xs[i + 1] - xs[i] for i in range(len(xs) - 1)] + [modulus + xs[0] - xs[-1]])


def subsets(q: int):
    for mask in range(1, 1 << q):
        yield tuple(i for i in range(q) if mask >> i & 1)


def main() -> None:
    started = time.time()
    tested = 0
    witness = None
    for q, r in itertools.combinations(range(2, 12), 2):
        if math.gcd(q, r) != 1:
            continue
        for aa in subsets(q):
            ga = max_gap(q, aa)
            for bb in subsets(r):
                gb = max_gap(r, bb)
                inter = [x for x in range(q * r) if x % q in aa and x % r in bb]
                gi = max_gap(q * r, inter)
                tested += 1
                if gi > ga * gb:
                    witness = {
                        "q": q,
                        "r": r,
                        "A": aa,
                        "B": bb,
                        "gap_A": ga,
                        "gap_B": gb,
                        "gap_intersection": gi,
                        "product_bound": ga * gb,
                    }
                    break
            if witness:
                break
        if witness:
            break
    anchored_tested = 0
    anchored_witness = None
    for q, r in itertools.combinations(range(2, 26), 2):
        if math.gcd(q, r) != 1:
            continue
        for a in range(1, q):
            aa = tuple(range(a))
            ga = max_gap(q, aa)
            for b in range(1, r):
                bb = tuple(range(b))
                gb = max_gap(r, bb)
                inter = [x for x in range(q * r) if x % q < a and x % r < b]
                gi = max_gap(q * r, inter)
                anchored_tested += 1
                if gi > ga * gb:
                    anchored_witness = {
                        "q": q,
                        "r": r,
                        "a": a,
                        "b": b,
                        "gap_A": ga,
                        "gap_B": gb,
                        "gap_intersection": gi,
                        "product_bound": ga * gb,
                    }
                    break
            if anchored_witness:
                break
        if anchored_witness:
            break
    usage = resource.getrusage(resource.RUSAGE_SELF)
    print(
        json.dumps(
            {
                "status": "killed" if witness else "finite_survivor",
                "claim": "G(A intersection B) <= G(A) G(B)",
                "systems_tested": tested,
                "witness": witness,
                "anchored_interval_test": {
                    "status": "killed" if anchored_witness else "finite_survivor",
                    "systems_tested": anchored_tested,
                    "witness": anchored_witness,
                },
                "runtime": {
                    "wall_seconds": time.time() - started,
                    "max_rss_kib": usage.ru_maxrss,
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
