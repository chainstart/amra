#!/usr/bin/env python3
"""Bounded exact wall-budget sequence without full orbit replay."""

from __future__ import annotations

import json
from math import comb


def C(t: int, k: int) -> int:
    return comb(t, k) if t >= k >= 0 else 0


def q_of(j: int) -> int:
    assert j >= 1 and j % 2 == 1
    return (224 * 2 ** (j - 1) + 4) // 3


def largest_odd_j_below(bound: int) -> int:
    # q_j has bit length j+O(1); start locally, then certify by adjustment.
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
    last_rank = 22
    aa, bb = {4: 25}, {4: 58}
    for n in range(4, last_rank):
        aa[n + 1] = C(aa[n], 2) - (20 * n - 49)
        bb[n + 1] = C(bb[n], 2) - (20 * n - 52)

    rows = []
    for rank in range(5, last_rank + 1):
        j = largest_odd_j_below(bb[rank])
        q = q_of(j)
        t = q - (5 * rank - 16)
        s = 0
        while C(t + s + 1, 2) - C(t, 2) <= bb[rank]:
            s += 1
            if s > 8:
                break
        residual = bb[rank] - (C(t + s, 2) - C(t, 2))
        previous_gamma = bb[rank] - aa[rank] - aa[rank - 1] - 1 - 4 * q
        rows.append({
            "rank": rank,
            "odd_j": j,
            "q_bit_length": q.bit_length(),
            "B_bit_length": bb[rank].bit_length(),
            "B_over_q_floor_1000000": 1_000_000 * bb[rank] // q,
            "bottom_shift": s,
            "one_wall_legal": s <= 3 and 0 <= residual < t + s,
            "previous_stable": (
                aa[rank - 1] < q - (5 * (rank - 1) - 15)
                and bb[rank - 1] < q - (5 * (rank - 1) - 16)
            ),
            "previous_gamma_negative": previous_gamma < 0,
        })

    print(json.dumps({
        "schema": "amra.erdos776.round7.wall-budget-sequence.v1",
        "rank_domain": [5, last_rank],
        "rows": rows,
        "budget_three_ranks": [r["rank"] for r in rows if r["bottom_shift"] == 3],
        "higher_carry_ranks": [r["rank"] for r in rows if r["bottom_shift"] >= 4],
        "scope_warning": "finite recurrence/wall classification only; no all-rank frequency claim",
    }, indent=2))


if __name__ == "__main__":
    main()
