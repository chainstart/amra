#!/usr/bin/env python3
"""Exact falsification of single-hyperplane certificates for actual gaps.

For each retained block, the coefficient box is exhaustive: outside it the
coordinate part of R exceeds 1/2, while a centered phase distance is at most
1/2.  Thus a reported no-certificate row rigorously kills the split-only
claim for that finite actual 451 block.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def crt_pair(a: int, q: int, b: int, r: int) -> int:
    return a + q * (((b - a) * pow(q, -1, r)) % r)


def residues(primes: tuple[int, ...], widths: tuple[int, ...]) -> tuple[int, list[int]]:
    period = 1
    rows = [0]
    for p, width in zip(primes, widths):
        rows = [crt_pair(a, period, b, p) for a in rows for b in range(width)]
        period *= p
    rows.sort()
    return period, rows


def maximum_gap(period: int, rows: list[int]) -> tuple[int, int, int]:
    gaps = []
    for index, left in enumerate(rows):
        right = rows[index + 1] if index + 1 < len(rows) else period + rows[0]
        gaps.append((right - left, left, right))
    return max(gaps)


def centered_distance(value: Fraction) -> Fraction:
    residue = value % 1
    return min(residue, 1 - residue)


def certificate(
    k: int,
    scale: int,
    primes: tuple[int, ...],
    period: int,
    gap: int,
    left: int,
    right: int,
) -> dict[str, object]:
    w = (scale - 1) // 2
    b = Fraction(2 * w + 1, 2)
    # Leave a full unit at both gap endpoints, so the closed located body is
    # rigorously contained in the open gap between allowed CRT residues.
    h = Fraction(gap, 2) - w - 1
    center = -Fraction(left + right, 2)  # sign-reflected actual 451 gap
    exhaustive_m = math.floor(Fraction(k, 1) / b) + 1
    cofactors = tuple(period // p for p in primes)
    best = None
    witness = None
    minimum_support = None
    minimum_support_vector = None
    checked = 0
    for vector in itertools.product(range(-exhaustive_m, exhaustive_m + 1), repeat=len(primes)):
        if not any(vector):
            continue
        checked += 1
        numerator = sum(z * cofactor for z, cofactor in zip(vector, cofactors))
        if numerator == 0:
            continue
        support = h * abs(numerator) / period + sum(
            b * abs(z) / p for z, p in zip(vector, primes)
        )
        distance = centered_distance(center * numerator / period)
        margin = distance - support
        candidate = (margin, tuple(-z for z in vector), -numerator, support, distance)
        if best is None or candidate > best:
            best = candidate
            witness = vector
        support_candidate = (support, vector)
        if minimum_support is None or support_candidate < minimum_support:
            minimum_support = support_candidate
            minimum_support_vector = vector
    assert best is not None
    assert minimum_support is not None
    outside_lower = b * (exhaustive_m + 1) / (2 * k)
    assert outside_lower > Fraction(1, 2)
    return {
        "k": k,
        "scale": scale,
        "primes": primes,
        "rank": len(primes),
        "period": period,
        "gap": gap,
        "gap_left_positive_model": left,
        "gap_right_positive_model": right,
        "coefficient_bound": exhaustive_m,
        "vectors_checked": checked,
        "outside_box_transverse_lower": str(outside_lower),
        "best_vector": witness,
        "best_margin_exact": str(best[0]),
        "best_margin": float(best[0]),
        "best_support_exact": str(best[3]),
        "best_support": float(best[3]),
        "best_phase_distance_exact": str(best[4]),
        "best_phase_distance": float(best[4]),
        "minimum_R_exact": str(minimum_support[0]),
        "minimum_R": float(minimum_support[0]),
        "minimum_R_over_rank": float(minimum_support[0] / len(primes)),
        "minimum_R_vector": minimum_support_vector,
        "single_hyperplane_certificate_exists": best[0] > 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=80)
    parser.add_argument("--max-rank", type=int, default=4)
    parser.add_argument("--max-cardinality", type=int, default=300_000)
    parser.add_argument("--max-vectors", type=int, default=5_000_000)
    args = parser.parse_args()
    rows = []
    for k in range(5, args.max_k + 1):
        blocks: dict[int, list[int]] = {}
        for p in range(k + 1, 2 * k):
            if is_prime(p):
                d = p - k
                scale = 1 << (d.bit_length() - 1)
                blocks.setdefault(scale, []).append(p)
        for scale, block in blocks.items():
            primes = tuple(block)
            widths = tuple(p - k for p in primes)
            if not 2 <= len(primes) <= args.max_rank:
                continue
            if math.prod(widths) > args.max_cardinality:
                continue
            w = (scale - 1) // 2
            b = Fraction(2 * w + 1, 2)
            exhaustive_m = math.floor(Fraction(k, 1) / b) + 1
            if (2 * exhaustive_m + 1) ** len(primes) > args.max_vectors:
                continue
            period, allowed = residues(primes, widths)
            gap, left, right = maximum_gap(period, allowed)
            rows.append(certificate(k, scale, primes, period, gap, left, right))
    failures = [row for row in rows if not row["single_hyperplane_certificate_exists"]]
    print(
        json.dumps(
            {
                "classification": "finite_exact_split_falsification",
                "blocks_tested": len(rows),
                "split_failures": len(failures),
                "first_failure": failures[0] if failures else None,
                "largest_minimum_R_over_rank_among_failures": max(
                    failures,
                    key=lambda row: row["minimum_R_over_rank"],
                    default=None,
                ),
                "smallest_margins": sorted(rows, key=lambda row: row["best_margin"])[:10],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
