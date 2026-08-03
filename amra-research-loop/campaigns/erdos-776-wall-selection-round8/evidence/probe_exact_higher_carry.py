#!/usr/bin/env python3
"""Exact bounded first-kill test for the higher-carry narrow window."""

from __future__ import annotations

import json


def q_of(j: int) -> int:
    assert j >= 1 and j % 2 == 1
    return (224 * (1 << (j - 1)) + 4) // 3


def largest_odd_j_below(bound: int) -> int:
    j = max(1, bound.bit_length() - 6)
    if j % 2 == 0:
        j -= 1
    while j > 1 and q_of(j) > bound:
        j -= 2
    while q_of(j + 2) <= bound:
        j += 2
    assert q_of(j) <= bound < q_of(j + 2)
    return j


def main() -> None:
    last_rank = 24
    aa, bb = 25, 58
    rows = []
    for n in range(4, last_rank):
        aa = aa * (aa - 1) // 2 - (20 * n - 49)
        bb = bb * (bb - 1) // 2 - (20 * n - 52)
        rank = n + 1
        if rank < 20:
            continue
        j = largest_odd_j_below(bb)
        qminus = q_of(j)
        qplus = q_of(j + 2)
        distance = qplus - bb
        narrow_width = 20 * rank - 74
        t = qminus - (5 * rank - 16)
        shift = 0
        while ((t + shift + 1) * (t + shift) - t * (t - 1)) // 2 <= bb:
            shift += 1
            if shift > 6:
                break
        rows.append({
            "rank": rank,
            "odd_j_below": j,
            "B_bit_length": bb.bit_length(),
            "q_minus_bit_length": qminus.bit_length(),
            "q_plus_minus_B": distance if distance.bit_length() <= 64 else None,
            "q_plus_minus_B_bit_length": distance.bit_length(),
            "higher_carry_narrow_width": narrow_width,
            "in_higher_carry_window": distance <= narrow_width,
            "bottom_shift": shift,
        })
    print(json.dumps({
        "schema": "amra.erdos776.round8.exact-higher-carry-kill-test.v1",
        "rank_domain": [20, last_rank],
        "rows": rows,
        "verdict": (
            "higher-carry window realized"
            if any(r["in_higher_carry_window"] for r in rows)
            else "no higher-carry window in bounded exact domain"
        ),
        "scope_warning": "bounded exact recurrence through rank 24 only",
    }, indent=2))


if __name__ == "__main__":
    main()
