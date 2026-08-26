#!/usr/bin/env python3
"""Exact finite max-gap scan for actual 451 dyadic width blocks.

Finite diagnostic only; no row is promoted to an asymptotic theorem.
"""

from __future__ import annotations

import json
import math


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def crt_pair(a, q, b, r):
    return a + q * (((b - a) * pow(q, -1, r)) % r)


def residues(moduli, widths):
    period = 1
    rows = [0]
    for p, d in zip(moduli, widths):
        rows = [crt_pair(a, period, b, p) for a in rows for b in range(d)]
        period *= p
    rows.sort()
    return period, rows


def max_gap(period, rows):
    return max(
        [rows[i + 1] - rows[i] for i in range(len(rows) - 1)]
        + [period + rows[0] - rows[-1]]
    )


tested = 0
worst = None
selected = []

for k in range(5, 101):
    blocks = {}
    for p in range(k + 1, 2 * k):
        if not is_prime(p):
            continue
        d = p - k
        scale = 1 << (d.bit_length() - 1)
        blocks.setdefault(scale, []).append(p)
    for scale, moduli in blocks.items():
        widths = [p - k for p in moduli]
        cardinality = math.prod(widths)
        if cardinality > 2_000_000:
            continue
        period, rows = residues(moduli, widths)
        gap = max_gap(period, rows)
        density = cardinality / period
        ratio = gap * density
        normalized = ratio / (k * k)
        row = {
            "k": k,
            "scale": scale,
            "rank": len(moduli),
            "moduli": moduli,
            "widths": widths,
            "period": period,
            "cardinality": cardinality,
            "max_gap": gap,
            "gap_over_reciprocal_density": ratio,
            "normalized_by_k_squared": normalized,
        }
        tested += 1
        if worst is None or normalized > worst[0]:
            worst = (normalized, row)
        if k in (20, 30, 50, 80, 100):
            selected.append(row)

print(
    json.dumps(
        {
            "classification": "finite_diagnostic_only",
            "tested_blocks": tested,
            "worst_k2_normalized_row": worst[1],
            "selected_rows": selected,
        },
        sort_keys=True,
    )
)
