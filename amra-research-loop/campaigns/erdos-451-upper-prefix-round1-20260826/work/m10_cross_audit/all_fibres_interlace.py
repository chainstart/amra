#!/usr/bin/env python3
"""Exact actual-451 diagnostics for the all-fibres merge question.

Finite search only.  The two ratios distinguished below are

  direct = G(A intersection B)/(G(A)G(B)),
  fibre  = G(A intersection B)/(G(A)G(Q^{-1}B)).

The second tests whether the exact one-fibre pullback gap can be upgraded to
an all-fibres product inequality.  It is not assumed by the audit proof.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from itertools import combinations


def primes_below(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * n
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p : n : p] = b"\x00" * (((n - 1 - p * p) // p) + 1)
    return [p for p in range(2, n) if sieve[p]]


def gap(period: int, values: list[int]) -> tuple[int, int, int]:
    values.sort()
    best = (period + values[0] - values[-1], values[-1], values[0])
    for left, right in zip(values, values[1:]):
        best = max(best, (right - left, left, right))
    return best


def box(moduli: tuple[int, ...], k: int) -> tuple[int, list[int]]:
    period = 1
    values = [0]
    for p in moduli:
        inv = pow(period, -1, p)
        values = [
            a + period * (((b - a) * inv) % p)
            for a in values
            for b in range(p - k)
        ]
        period *= p
    values.sort()
    return period, values


def combine(q: int, aa: list[int], r: int, bb: list[int]) -> tuple[int, list[int]]:
    inv = pow(q, -1, r)
    values = [a + q * (((b - a) * inv) % r) for a in aa for b in bb]
    values.sort()
    return q * r, values


def phase_record(row: dict[str, object]) -> dict[str, object]:
    """Evaluate the exact fibre phases inside the recorded empty gap."""
    k = int(row["k"])
    left = tuple(int(p) for p in row["left"])
    right = tuple(int(p) for p in row["right"])
    q, aa = box(left, k)
    r, bb = box(right, k)
    inv = pow(q, -1, r)
    record = row["gaps"]["intersection"]
    x = int(record[1]) + 1
    length = int(record[0]) - 1
    ell_count = length // q
    phases = [(-((a - x) // q) + inv * a) % r for a in aa]
    multiplicities = Counter(phases)
    pulled = {(b * inv) % r for b in bb}
    exact_count = sum(
        1 for phase in phases for ell in range(ell_count) if (phase + ell) % r in pulled
    )
    return {
        "empty_interval_start": x,
        "whole_Q_rows": ell_count,
        "phase_collision_energy": sum(value * value for value in multiplicities.values()),
        "distinct_phases": len(multiplicities),
        "number_of_fibres": len(aa),
        "exact_count_in_LQ_subinterval": exact_count,
        "mean_count": len(aa) * len(bb) * ell_count / r,
    }


def search(max_k: int, point_cap: int, left_size: int, right_size: int) -> dict[str, object]:
    plist = primes_below(2 * max_k + 1)
    tested = 0
    fibre_failures = 0
    best_direct: dict[str, object] | None = None
    best_fibre: dict[str, object] | None = None
    for k in range(5, max_k + 1):
        ps = [p for p in plist if k < p < 2 * k]
        if len(ps) < left_size + right_size:
            continue
        left = tuple(ps[:left_size])
        q, aa = box(left, k)
        ga = gap(q, aa)[0]
        for right in combinations(ps[left_size:], right_size):
            widths = tuple(p - k for p in right)
            if max(widths) >= 2 * min(widths):
                continue
            if len(aa) * math.prod(widths) > point_cap:
                continue
            r, bb = box(right, k)
            gb = gap(r, bb)[0]
            pulled = sorted((b * pow(q, -1, r)) % r for b in bb)
            gc = gap(r, pulled)[0]
            qr, both = combine(q, aa, r, bb)
            gi_record = gap(qr, both)
            gi = gi_record[0]
            direct = gi / (ga * gb)
            fibre = gi / (ga * gc)
            row = {
                "k": k,
                "left": left,
                "right": right,
                "widths": tuple(p - k for p in left + right),
                "cardinalities": (len(aa), len(bb)),
                "gaps": {"A": ga, "B": gb, "Q_inverse_B": gc, "intersection": gi_record},
                "direct_factor": direct,
                "fibre_product_factor": fibre,
                "direct_over_k": direct / k,
            }
            tested += 1
            if fibre > 1 + 1e-12:
                fibre_failures += 1
            if best_direct is None or direct > float(best_direct["direct_factor"]):
                best_direct = row
            if best_fibre is None or fibre > float(best_fibre["fibre_product_factor"]):
                best_fibre = row
    if best_direct is not None:
        best_direct["phase_record"] = phase_record(best_direct)
    if best_fibre is not None:
        best_fibre["phase_record"] = phase_record(best_fibre)
    return {
        "classification": "finite_actual_451_diagnostic_only",
        "left_size": left_size,
        "right_size": right_size,
        "tested": tested,
        "fibre_product_failures": fibre_failures,
        "best_direct": best_direct,
        "best_fibre_product": best_fibre,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=140)
    parser.add_argument("--point-cap", type=int, default=250000)
    parser.add_argument("--left-size", type=int, default=2, choices=(1, 2, 3))
    parser.add_argument("--right-size", type=int, default=2, choices=(2, 3))
    args = parser.parse_args()
    print(
        json.dumps(
            search(args.max_k, args.point_cap, args.left_size, args.right_size),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
