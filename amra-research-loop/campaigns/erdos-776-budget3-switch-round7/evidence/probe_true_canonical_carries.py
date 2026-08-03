#!/usr/bin/env python3
"""Exact bounded probe of true canonical carries on the actual K4,r9 orbit.

This is falsification evidence only.  It deliberately recomputes greedy
Macaulay words and never substitutes a proposed affine switch.
"""

from __future__ import annotations

import json
from math import comb


def C(t: int, k: int) -> int:
    return comb(t, k) if t >= k >= 0 else 0


def canonical(value: int, rank: int) -> tuple[tuple[int, int], ...]:
    assert value >= 0 and rank >= 1
    remainder = value
    ceiling = None
    out = []
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        if ceiling is None:
            hi = max(2, lower + 1)
            while C(hi, lower) <= remainder:
                hi *= 2
        else:
            hi = ceiling
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if C(mid, lower) <= remainder:
                lo = mid
            else:
                hi = mid
        if lo >= lower:
            out.append((lo, lower))
            remainder -= C(lo, lower)
            ceiling = lo
    assert remainder == 0
    return tuple(out)


def upper(word: tuple[tuple[int, int], ...]) -> int:
    return sum(C(t, k + 1) for t, k in word)


def q_of(j: int) -> int:
    assert j >= 1 and j % 2 == 1
    h = 112 * 2 ** (j - 1)
    assert (2 * h + 4) % 3 == 0
    return (2 * h + 4) // 3


def constants(last_rank: int) -> tuple[dict[int, int], dict[int, int]]:
    aa, bb = {4: 25}, {4: 58}
    for n in range(4, last_rank):
        aa[n + 1] = C(aa[n], 2) - (20 * n - 49)
        bb[n + 1] = C(bb[n], 2) - (20 * n - 52)
    return aa, bb


def stable_word(q: int, rank: int, tail: int, side: str):
    htop = 5 * q // 2
    if side == "x":
        out = [(htop, rank), (q - 1, rank - 1)]
        out += [(q - (1 + 5 * i), rank - 1 - i)
                for i in range(1, rank - 3)]
        out += [(q - (5 * rank - 15), 2), (tail, 1)]
    else:
        out = [(htop + 1, rank), (q, rank - 1)]
        out += [(q - 5 * i, rank - 1 - i)
                for i in range(1, rank - 3)]
        out += [(q - (5 * rank - 16), 2), (tail, 1)]
    return tuple(out)


def signature(word, q: int, keep: int = 6):
    # Keep exact small tails and q-offsets, but not giant full values.
    return [
        {"lower": k, "top_minus_q": t - q,
         "top": t if t.bit_length() <= 64 else None}
        for t, k in word[-keep:]
    ]


def profile(j: int, max_rank: int, aa, bb):
    q = q_of(j)
    h = 112 * 2 ** (j - 1)
    b = q + 4
    tau = 4 * q - 2
    x = C(h + b - 2, 3) + C(b - 1, 2) + 2 - 2 * h
    y = C(h + b - 1, 3) + C(b, 2) + 2 - 2 * h
    rows = []
    first = None
    for rank in range(3, max_rank + 1):
        wx, wy = canonical(x, rank), canonical(y, rank)
        ux, uy = upper(wx), upper(wy)
        gamma = uy - ux - x - tau
        stable_x = rank >= 4 and wx == stable_word(q, rank, aa[rank], "x")
        stable_y = rank >= 4 and wy == stable_word(q, rank, bb[rank], "y")
        if gamma >= 0 and first is None:
            first = {
                "rank": rank,
                "gamma_sign": 1 if gamma > 0 else 0,
                "gamma_bit_length": abs(gamma).bit_length(),
                "stable_x": stable_x,
                "stable_y": stable_y,
                "x_signature": signature(wx, q),
                "y_signature": signature(wy, q),
                "previous": rows[-1] if rows else None,
            }
            break
        rows.append({
            "rank": rank,
            "gamma_sign": -1 if gamma < 0 else 0,
            "stable_x": stable_x,
            "stable_y": stable_y,
            "B_over_q_floor_1000": (1000 * bb[rank] // q) if rank >= 4 else None,
        })
        x, y = ux - tau + 1, uy - tau
        assert x >= 0 and y >= 0
    return {"j": j, "q_bits": q.bit_length(), "first": first}


def actual_wall_rows(aa, bb, max_rank: int):
    """One actual q immediately below each B_n wall; classify rank-two carry."""
    rows = []
    for rank in range(5, max_rank + 1):
        j = 1
        while q_of(j + 2) <= bb[rank]:
            j += 2
        q = q_of(j)
        t0 = q - (5 * rank - 16)
        if t0 <= 0:
            continue
        s = 0
        while s < 4 and C(t0 + s + 1, 2) - C(t0, 2) <= bb[rank]:
            s += 1
        residual = bb[rank] - (C(t0 + s, 2) - C(t0, 2))
        previous_gamma = (
            bb[rank] - aa[rank] - aa[rank - 1] - 1 - 4 * q
        )
        rows.append({
            "rank": rank,
            "odd_j": j,
            "q_bits": q.bit_length(),
            "B_over_q_floor_1000": 1000 * bb[rank] // q,
            "rank2_shift_s": s,
            "combined_bottom_budget": s,
            "residual_legal": 0 <= residual < t0 + s,
            "previous_stable": (
                aa[rank - 1] < q - (5 * (rank - 1) - 15)
                and bb[rank - 1] < q - (5 * (rank - 1) - 16)
            ),
            "previous_gamma_negative": previous_gamma < 0,
        })
    return rows


def main() -> None:
    max_rank = 18
    aa, bb = constants(max_rank + 1)
    profiles = [profile(j, max_rank, aa, bb) for j in range(3, 402, 2)]
    assert all(item["first"] is not None for item in profiles)
    transitions = []
    last_key = None
    for item in profiles:
        first = item["first"]
        key = (first["rank"], first["stable_x"], first["stable_y"])
        if key != last_key:
            transitions.append(item)
            last_key = key
    counts = {}
    for item in profiles:
        f = item["first"]
        key = f"r{f['rank']}:x{int(f['stable_x'])}y{int(f['stable_y'])}"
        counts[key] = counts.get(key, 0) + 1
    walls = actual_wall_rows(aa, bb, max_rank)
    print(json.dumps({
        "schema": "amra.erdos776.round7.true-canonical-carry-probe.v1",
        "domain": {"odd_j": [3, 401], "max_rank": max_rank},
        "profiles": len(profiles),
        "all_recovered_in_probe": True,
        "profile_counts": counts,
        "transition_representatives": transitions,
        "actual_wall_rows": walls,
        "budget_three_wall_ranks": [
            row["rank"] for row in walls
            if row["combined_bottom_budget"] == 3
            and row["residual_legal"] and row["previous_stable"]
            and row["previous_gamma_negative"]
        ],
        "scope_warning": "finite exact probe; not an all-j adaptive recovery theorem",
    }, indent=2))


if __name__ == "__main__":
    main()
