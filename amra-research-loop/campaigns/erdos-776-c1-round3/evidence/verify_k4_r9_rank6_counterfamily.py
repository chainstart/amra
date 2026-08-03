#!/usr/bin/env python3
"""Exact certificate for an actual c=1 rank-five/rank-six counterfamily."""

from math import comb
from pathlib import Path
import hashlib
import json


def canonical(number: int, rank: int) -> tuple[tuple[int, int], ...]:
    assert number >= 0
    remainder = number
    ceiling = None
    word = []
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        hi = ceiling if ceiling is not None else max(2, lower + 1)
        if ceiling is None:
            while comb(hi, lower) <= remainder:
                hi *= 2
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if comb(mid, lower) <= remainder:
                lo = mid
            else:
                hi = mid
        if lo >= lower:
            word.append((lo, lower))
            remainder -= comb(lo, lower)
            ceiling = lo
    assert remainder == 0
    return tuple(word)


def upper(number: int, rank: int) -> int:
    return sum(comb(top, lower + 1) for top, lower in canonical(number, rank))


def family(j: int) -> dict[str, int]:
    assert j >= 3 and j % 2 == 1
    h = 112 * (1 << (j - 1))
    assert h % 3 == 1
    q = (2 * h + 4) // 3
    k, r, u = 4, 9, 12
    b = q + k
    n = comb(q, 2) + r
    tau = 4 * q - 2
    assert n == comb(b - 1, 2) + 2 - 2 * h
    assert tau == comb(b, 2) + 1 - n == 2 * h + b - 2
    assert 0 <= r < q and 0 <= u < q + 1 and 5 <= b < h
    return {"j": j, "h": h, "q": q, "k": k, "r": r,
            "u": u, "b": b, "n": n, "tau": tau}


def direct_orbit(h: int, b: int, through: int = 7) -> dict[int, int]:
    cap = h + b - 2
    tau = 2 * h + b - 2
    x = comb(cap, 3) + comb(b - 1, 2) + 2 - 2 * h
    y = comb(cap + 1, 3) + comb(b, 2) + 2 - 2 * h
    result = {}
    for rank in range(3, through + 1):
        ux, uy = upper(x, rank), upper(y, rank)
        result[rank] = uy - ux - x - tau
        x, y = ux - tau + 1, uy - tau
        assert x >= 0 and y >= 0
    return result


def normalized(q: int) -> dict[str, int]:
    tau = 4 * q - 2
    alpha = comb(q - 5, 2) + 25
    beta = comb(q - 4, 2) + 58
    p = upper(alpha, 2) - tau + 1
    v = upper(beta, 2) - tau
    P = upper(p, 3) - tau + 1
    V = upper(v, 3) - tau
    return {"alpha": alpha, "beta": beta, "p": p, "v": v,
            "P": P, "V": V, "tau": tau}


def main() -> None:
    first = family(33)
    q = first["q"]
    state = normalized(q)

    expected_words = {
        "alpha": ((q - 5, 2), (25, 1)),
        "beta": ((q - 4, 2), (58, 1)),
        "p": ((q - 6, 3), (q - 10, 2), (269, 1)),
        "v": ((q - 5, 3), (q - 9, 2), (1625, 1)),
        "P": ((q - 6, 4), (q - 11, 3), (q - 15, 2), (35995, 1)),
        "V": ((q - 5, 4), (q - 10, 3), (q - 14, 2), (1319452, 1)),
    }
    for name, word in expected_words.items():
        rank = word[0][1]
        assert canonical(state[name], rank) == word

    formulas = {
        3: 23 - 4 * q,
        4: 1330 - 4 * q,
        5: 1283187 - 4 * q,
        6: 869828292418 - 4 * q,
    }
    orbit = direct_orbit(first["h"], first["b"], 7)
    assert all(orbit[rank] == value for rank, value in formulas.items())
    assert orbit[5] < 0 and orbit[6] < 0 and orbit[7] > 0

    # The displayed canonical forms are stable for every odd j>=33.
    # Hence the linear formulas prove infinitely many literal counterexamples.
    checked = []
    for j in (33, 35, 37, 55):
        row = family(j)
        got = direct_orbit(row["h"], row["b"], 7)
        assert got[5] == 1283187 - 4 * row["q"] < 0
        assert got[6] == 869828292418 - 4 * row["q"] < 0
        checked.append({**row, "gamma3": got[3], "gamma4": got[4],
                        "gamma5": got[5], "gamma6": got[6],
                        "gamma7": got[7]})

    output = {
        "schema": "amra.erdos776.k4-r9-rank6-counterfamily.v1",
        "family": "odd j>=33; h=112*2^(j-1), q=(2h+4)/3, (k,r,u,b)=(4,9,12,q+4)",
        "stable_formulas": {f"gamma{rank}": str(value).replace(str(q), "q")
                            for rank, value in formulas.items()},
        "literal_formulas": {
            "gamma3": "23-4q", "gamma4": "1330-4q",
            "gamma5": "1283187-4q", "gamma6": "869828292418-4q",
        },
        "first_checked_counterexample": checked[0],
        "selected_checks": checked,
        "conclusion": "M305 rank-six positivity and the inherited c=1 two-row recovery candidate are false on an infinite actual dyadic family; rank seven recovers at the first witness.",
        "scope": "Does not refute adaptive recovery, the global interface, or the public antichain statement.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "public_problem_closed": False,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
