#!/usr/bin/env python3
"""Exact guards for the all-j K4,r9 first-wall recovery theorem."""

from __future__ import annotations

import json
from math import comb


def C(t: int, k: int) -> int:
    return comb(t, k) if t >= k >= 0 else 0


def canonical(value: int, rank: int):
    assert value >= 0
    rem, ceiling, out = value, None, []
    for lower in range(rank, 0, -1):
        if rem == 0:
            break
        lo = lower - 1
        if ceiling is None:
            hi = max(2, lower + 1)
            while C(hi, lower) <= rem:
                hi *= 2
        else:
            hi = ceiling
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if C(mid, lower) <= rem:
                lo = mid
            else:
                hi = mid
        if lo >= lower:
            out.append((lo, lower))
            rem -= C(lo, lower)
            ceiling = lo
    assert rem == 0
    return tuple(out)


def upper(word) -> int:
    return sum(C(t, k + 1) for t, k in word)


def value(word) -> int:
    return sum(C(t, k) for t, k in word)


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


def q_of(j: int) -> int:
    assert j >= 1 and j % 2 == 1
    return (224 * (1 << (j - 1)) + 4) // 3


def constants(last_rank: int):
    aa, bb = {4: 25}, {4: 58}
    for n in range(4, last_rank):
        aa[n + 1] = C(aa[n], 2) - (20 * n - 49)
        bb[n + 1] = C(bb[n], 2) - (20 * n - 52)
    return aa, bb


def direct_first_recovery(j: int, max_rank: int = 18):
    q = q_of(j)
    h, b, tau = 112 * 2 ** (j - 1), q + 4, 4 * q - 2
    x = C(h + b - 2, 3) + C(b - 1, 2) + 2 - 2 * h
    y = C(h + b - 1, 3) + C(b, 2) + 2 - 2 * h
    for rank in range(3, max_rank + 1):
        wx, wy = canonical(x, rank), canonical(y, rank)
        ux, uy = upper(wx), upper(wy)
        gamma = uy - ux - x - tau
        if gamma >= 0:
            return rank, gamma
        x, y = ux - tau + 1, uy - tau
        assert x >= 0 and y >= 0
    return None, None


def main() -> None:
    aa, bb = constants(20)
    assert (aa[5], bb[5]) == (269, 1625)
    assert aa[5] >= 20 * 5 and bb[5] >= 20 * 5
    assert (aa[6], bb[6]) == (35995, 1319452)
    assert bb[6] >= 30 * aa[6]
    for n in range(6, 20):
        assert bb[n] >= 30 * aa[n]
        assert aa[n] > aa[n - 1] > 0
        assert aa[n] >= 20 * n and bb[n] >= 20 * n
        assert 200 * n * n - 50 * n + 29 > 0
        gap_next = bb[n + 1] - 30 * aa[n + 1]
        symbolic_lower = 435 * aa[n] ** 2 + 580 * n - 1418
        assert gap_next >= symbolic_lower > 0
        d_n = C(bb[n], 2) - C(aa[n] + 1, 2) + 2
        assert d_n == bb[n + 1] - aa[n + 1] - aa[n] - 1

    # Direct algebra guard for the minimum-wall comparison used universally.
    q_guard = 10**500
    tau_guard = 4 * q_guard - 2
    for rank in range(6, 13):
        t = q_guard - (5 * rank - 16)
        wx = stable_word(q_guard, rank, aa[rank], "x")
        wy0_list = list(stable_word(q_guard, rank, t, "y")[:-2])
        wy0_list.append((t + 1, 2))
        wy0 = tuple(wy0_list)
        assert all(wx[i][0] > wx[i + 1][0] for i in range(len(wx) - 1))
        assert all(wy0[i][0] > wy0[i + 1][0] for i in range(len(wy0) - 1))
        gamma0 = upper(wy0) - upper(wx) - value(wx) - tau_guard
        lower_formula = C(t, 2) - C(aa[rank] + 1, 2) + 2 - 4 * q_guard
        assert gamma0 == lower_formula

    # Exact finite base and a broad direct guard.  The theorem does not use
    # the bounded guard as its universal step.
    base = {}
    for j in (1, 3, 5):
        rank, gamma = direct_first_recovery(j)
        base[str(j)] = {"q": q_of(j), "rank": rank, "gamma": gamma}
    assert base["1"]["rank"] == 4
    assert base["3"]["rank"] == 4
    assert base["5"]["rank"] == 5
    assert all(item["gamma"] > 0 for item in base.values())

    profiles = []
    for j in range(1, 402, 2):
        rank, gamma = direct_first_recovery(j)
        assert rank is not None and gamma is not None and gamma >= 0
        profiles.append(rank)

    # Coarse wall inequality used in the natural proof.
    for q in (1196, 4780, 1_223_340, 10**8):
        assert q * q / 9 - 15 * q / 4 + 2 > 0

    print(json.dumps({
        "schema": "amra.erdos776.round8.all-j-first-wall-recovery.v1",
        "verdict": "PASS",
        "finite_base": base,
        "ratio_induction_checked_through_rank": 20,
        "direct_guard": {
            "odd_j": [1, 401],
            "members": len(profiles),
            "max_first_recovery_rank": max(profiles),
            "all_recovered": True,
        },
        "universal_inputs": [
            "B_n>=30A_n for n>=6 by induction",
            "A_n,B_n>=20n for n>=5 by induction",
            "negative previous stable surplus implies A_m+1<q/6",
            "previous stability implies t>q/2",
            "monotonicity of fixed-rank Macaulay raise",
            "unbounded B_m forces termination at a wall"
        ],
        "scope_warning": "all actual odd j in fixed K4,r9 only; no rank-42 bound, suffix theorem, or public closure",
    }, indent=2))


if __name__ == "__main__":
    main()
