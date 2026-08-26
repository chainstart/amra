#!/usr/bin/env python3
"""Exact rank-4 actual-gap and single-dual-hyperplane certificate."""

from __future__ import annotations

import json
import math
from fractions import Fraction


def crt_pair(a: int, q: int, b: int, r: int) -> int:
    return a + q * (((b - a) * pow(q, -1, r)) % r)


def main() -> None:
    k = 168
    primes = (191, 193, 197, 199)
    widths = tuple(p - k for p in primes)
    period = 1
    rows = [0]
    for p, width in zip(primes, widths):
        rows = [crt_pair(a, period, b, p) for a in rows for b in range(width)]
        period *= p
    rows.sort()

    candidates = []
    for index, left in enumerate(rows):
        right = rows[index + 1] if index + 1 < len(rows) else period + rows[0]
        candidates.append((right - left, left, right))
    gap, left, right = max(candidates)

    # The actual 451 residues are the negatives of rows.  Reflection keeps
    # the gap length and changes the center sign, which does not change the
    # distance of its dual phase to the nearest integer.
    center = Fraction(left + right, 2)
    vector = (-1, 2, -2, 1)
    numerator = sum(z * (period // p) for z, p in zip(vector, primes))
    scale = 16
    w = (scale - 1) // 2
    coordinate_half_width = Fraction(2 * w + 1, 2)
    time_half_width = Fraction(gap, 2) - w
    support = time_half_width * abs(numerator) / period + sum(
        coordinate_half_width * abs(z) / p for z, p in zip(vector, primes)
    )
    phase = (-center * numerator / period) % 1
    phase_distance = min(phase, 1 - phase)

    assert gap == 4_327_275
    assert numerator == -96
    assert phase_distance > support
    print(
        json.dumps(
            {
                "classification": "finite_exact_hyperplane_certificate",
                "k": k,
                "primes": primes,
                "widths": widths,
                "period": period,
                "allowed_residue_count": len(rows),
                "positive_residue_gap": {
                    "left": left,
                    "right_unwrapped": right,
                    "length": gap,
                },
                "actual_451_gap_center_is_negative_of": str(center),
                "dual_vector": vector,
                "A": numerator,
                "time_half_width": str(time_half_width),
                "coordinate_half_width": str(coordinate_half_width),
                "support_R_exact": str(support),
                "support_R_float": float(support),
                "center_phase_distance_exact": str(phase_distance),
                "center_phase_distance_float": float(phase_distance),
                "strict_single_hyperplane_certificate": phase_distance > support,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
