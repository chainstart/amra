#!/usr/bin/env python3
"""Exact certificate for a literal alpha=3 K4,r9 Macaulay switch.

The universal part is the rank-two wall identity.  The witness part directly
replays the actual odd-j=1231 orbit with greedy canonical expansions.
"""

from __future__ import annotations

from hashlib import sha256
import json
from math import comb


def C(t: int, k: int) -> int:
    return comb(t, k) if t >= k >= 0 else 0


def canonical(value: int, rank: int) -> tuple[tuple[int, int], ...]:
    assert value >= 0 and rank >= 1
    rem = value
    ceiling = None
    out = []
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


def value(word) -> int:
    return sum(C(t, k) for t, k in word)


def upper(word) -> int:
    return sum(C(t, k + 1) for t, k in word)


def q_of(j: int) -> int:
    h = 112 * 2 ** (j - 1)
    assert j % 2 == 1 and (2 * h + 4) % 3 == 0
    return (2 * h + 4) // 3


def constants(last_rank: int):
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


def digest(number: int) -> str:
    return sha256(str(number).encode()).hexdigest()


def main() -> None:
    j = 1231
    switched_rank = 12
    q = q_of(j)
    h = 112 * 2 ** (j - 1)
    b = q + 4
    tau = 4 * q - 2
    aa, bb = constants(switched_rank + 1)

    # Literal actual dyadic family, not a relaxed point.
    assert 2 * h == 3 * q - 4
    assert C(b - 1, 2) + 2 - (C(q, 2) + 9) == 2 * h
    assert C(b, 2) + 1 - (C(q, 2) + 9) == tau

    x = C(h + b - 2, 3) + C(b - 1, 2) + 2 - 2 * h
    y = C(h + b - 1, 3) + C(b, 2) + 2 - 2 * h
    gammas = {}
    words = {}
    for rank in range(3, switched_rank + 1):
        wx, wy = canonical(x, rank), canonical(y, rank)
        ux, uy = upper(wx), upper(wy)
        gammas[rank] = uy - ux - x - tau
        words[rank] = (wx, wy)
        if rank < switched_rank:
            x, y = ux - tau + 1, uy - tau
            assert x >= 0 and y >= 0

    # The preceding state is completely stable and still negative.
    assert words[11][0] == stable_word(q, 11, aa[11], "x")
    assert words[11][1] == stable_word(q, 11, bb[11], "y")
    assert gammas[11] < 0

    # Universal budget-three rank-two wall identity at resulting rank m.
    m = switched_rank
    t = q - (5 * m - 16)
    residual = bb[m] - 3 * t - 3
    assert C(t, 2) + bb[m] == C(t + 3, 2) + residual
    assert residual == C(bb[m - 1], 2) - 3 * q - (5 * m - 21)
    assert 0 <= residual < t + 3
    assert 3 * t + 3 <= bb[m] < 4 * t + 6

    expected_x = stable_word(q, m, aa[m], "x")
    expected_y_list = list(stable_word(q, m, bb[m], "y")[:-2])
    expected_y_list.extend(((t + 3, 2), (residual, 1)))
    expected_y = tuple(expected_y_list)
    assert words[m][0] == expected_x
    assert words[m][1] == expected_y
    assert value(expected_y) == y
    assert all(expected_y[i][0] > expected_y[i + 1][0]
               for i in range(len(expected_y) - 1))

    # The literal switch realizes alpha=3, delta=0 and recovers immediately.
    assert gammas[m] > 0
    assert aa[m] < t - 1
    assert q_of(j + 2) == 4 * q - 4

    print(json.dumps({
        "schema": "amra.erdos776.round7.actual-budget-three-switch.v1",
        "verdict": "PASS",
        "actual_member": {"odd_j": j, "q_bit_length": q.bit_length()},
        "switch": {
            "from_rank": 11,
            "to_rank": 12,
            "alpha": 3,
            "delta": 0,
            "combined_budget": 3,
            "bottom_top_shift": 3,
            "residual_formula": "C(B_11,2)-3q-(5*12-21)",
            "rank_two_wall_interval": "3t+3 <= B_12 < 4t+6",
            "strict_canonical": True,
        },
        "signs": {
            "gamma_11": -1,
            "gamma_12": 1,
            "gamma_11_bit_length": abs(gammas[11]).bit_length(),
            "gamma_12_bit_length": gammas[12].bit_length(),
        },
        "digests": {
            "q": digest(q),
            "B_12": digest(bb[12]),
            "residual": digest(residual),
            "gamma_12": digest(gammas[12]),
            "rank12_words": sha256(repr(words[12]).encode()).hexdigest(),
        },
        "scope_warning": (
            "proves one real legal local budget-three switch and its immediate "
            "recovery; does not prove a uniform switch, suffix persistence, or "
            "the public Erdos-776 antichain bound"
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
