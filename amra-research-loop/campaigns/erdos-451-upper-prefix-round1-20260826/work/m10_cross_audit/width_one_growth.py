#!/usr/bin/env python3
"""Targeted growth search for width-one old blocks and nearby dyadic pairs.

For k+1=p prime, the old block is {0} modulo p.  The merge ratio is exactly
G(p^{-1}B)/G(B), so no full three-modulus CRT enumeration is needed.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations


def primes_below(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * n
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p : n : p] = b"\x00" * (((n - 1 - p * p) // p) + 1)
    return [p for p in range(2, n) if sieve[p]]


def gap(period: int, values: list[int]) -> int:
    values.sort()
    answer = period + values[0] - values[-1]
    for a, b in zip(values, values[1:]):
        answer = max(answer, b - a)
    return answer


def pair_box(k: int, q: int, r: int) -> tuple[int, list[int]]:
    aq, ar = q - k, r - k
    inverse = pow(q, -1, r)
    values = [a + q * (((b - a) * inverse) % r) for a in range(aq) for b in range(ar)]
    return q * r, values


def structural_resonance(max_u: int) -> dict[str, object]:
    """Coprime fixed-k family; moduli are not asserted prime.

    k=2u^2, p=k+1, q=k+u+1, r=k+2u+1.  The widths u+1 and 2u+1 are one
    dyadic block, and all three moduli are pairwise coprime.
    """
    rows = []
    for u in range(2, max_u + 1):
        k = 2 * u * u
        p, q, r = k + 1, k + u + 1, k + 2 * u + 1
        assert math.gcd(p, q) == math.gcd(p, r) == math.gcd(q, r) == 1
        period, values = pair_box(k, q, r)
        ordinary_gap = gap(period, values.copy())
        pullback_gap = gap(period, [(x * pow(p, -1, period)) % period for x in values])
        rows.append(
            {
                "u": u,
                "k": k,
                "moduli": (p, q, r),
                "widths": (1, u + 1, 2 * u + 1),
                "ordinary_gap": ordinary_gap,
                "pullback_gap": pullback_gap,
                "ratio": pullback_gap / ordinary_gap,
                "ratio_over_u": pullback_gap / (ordinary_gap * u),
            }
        )
    return {"family": "k=2u^2; widths 1,u+1,2u+1", "tail": rows[-12:]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=5000)
    parser.add_argument("--neighbors", type=int, default=7)
    parser.add_argument("--point-cap", type=int, default=200000)
    parser.add_argument("--structural-max-u", type=int, default=80)
    args = parser.parse_args()

    plist = primes_below(2 * args.max_k + 1)
    pset = set(plist)
    tested = 0
    violations = 0
    top: list[dict[str, object]] = []
    best_by_cutoff: dict[int, dict[str, object] | None] = {
        cutoff: None
        for cutoff in (100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000)
        if cutoff <= args.max_k
    }

    for k in range(4, args.max_k + 1):
        p = k + 1
        if p not in pset:
            continue
        right_primes = [r for r in plist if p < r < 2 * k][: args.neighbors]
        for q, r in combinations(right_primes, 2):
            aq, ar = q - k, r - k
            if ar >= 2 * aq or aq * ar > args.point_cap:
                continue
            period, values = pair_box(k, q, r)
            ordinary_gap = gap(period, values.copy())
            invp = pow(p, -1, period)
            pullback_gap = gap(period, [(x * invp) % period for x in values])
            ratio = pullback_gap / ordinary_gap

            # Exact pair lower witness and universal cardinality upper bounds.
            delta = r - q
            j0 = (aq - 1) // delta
            j1 = k // delta + 1
            pair_lower = (j1 - j0) * q - aq + 1
            assert pair_lower <= ordinary_gap
            b = aq * ar
            cardinality_upper = (period - b + 1) / math.ceil(period / b)
            pair_phase_upper = (period - b + 1) / pair_lower
            assert ratio <= cardinality_upper + 1e-12
            assert ratio <= pair_phase_upper + 1e-12

            row = {
                "k": k,
                "old_prime": p,
                "new_pair": (q, r),
                "new_widths": (aq, ar),
                "ordinary_gap": ordinary_gap,
                "pullback_gap": pullback_gap,
                "ratio": ratio,
                "cardinality": b,
                "cardinality_upper": cardinality_upper,
                "pair_phase_upper": pair_phase_upper,
            }
            tested += 1
            if ratio > 1:
                violations += 1
            top.append(row)
            top.sort(key=lambda item: float(item["ratio"]), reverse=True)
            del top[12:]
            for cutoff in best_by_cutoff:
                if k <= cutoff:
                    old = best_by_cutoff[cutoff]
                    if old is None or ratio > float(old["ratio"]):
                        best_by_cutoff[cutoff] = row

    print(
        json.dumps(
            {
                "classification": "finite_growth_diagnostic_only",
                "formula": "merge_ratio = G(p^{-1} B) / G(B)",
                "max_k": args.max_k,
                "neighbors": args.neighbors,
                "tested": tested,
                "violations": violations,
                "best_by_cutoff": best_by_cutoff,
                "top": top,
                "structural_resonance": structural_resonance(args.structural_max_u),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
