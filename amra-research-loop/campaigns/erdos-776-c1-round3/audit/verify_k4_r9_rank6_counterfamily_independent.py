#!/usr/bin/env python3
"""Blind full-orbit audit of the k=4, r=9 rank-six counterfamily.

This file imports no author verifier and reconstructs Macaulay expansions by
an independent greedy/binomial engine.
"""

from math import comb
import json


def c(n: int, k: int) -> int:
    if n < k or k < 0:
        return 0
    return comb(n, k)


def largest_top_leq(value: int, lower: int, upper: int | None) -> int:
    lo = lower - 1
    hi = max(lower, 1)
    if upper is not None:
        hi = upper
    else:
        while c(hi, lower) <= value:
            hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if c(mid, lower) <= value:
            lo = mid
        else:
            hi = mid
    if upper is not None and c(hi, lower) <= value:
        return hi
    return lo


def canonical(value: int, rank: int) -> tuple[tuple[int, int], ...]:
    assert value >= 0 and rank >= 1
    remaining = value
    previous_top: int | None = None
    descending: list[tuple[int, int]] = []
    for lower in range(rank, 0, -1):
        if remaining == 0:
            break
        upper = None if previous_top is None else previous_top - 1
        top = largest_top_leq(remaining, lower, upper)
        if top >= lower:
            descending.append((top, lower))
            remaining -= c(top, lower)
            previous_top = top
    assert remaining == 0
    return tuple(descending)


def raise_u(value: int, rank: int) -> int:
    return sum(c(top, lower + 1) for top, lower in canonical(value, rank))


def family(j: int) -> dict[str, int]:
    assert j % 2 == 1
    h = 112 * 2 ** (j - 1)
    q_num = 2 * h + 4
    assert q_num % 3 == 0
    q = q_num // 3
    k, r, u, b = 4, 9, 12, q + 4
    n = c(q, 2) + r
    H = c(b, 2) + 1
    tau = H - n
    assert c(b - 1, 2) + 2 - (c(q, 2) + r) == 2 * h

    n_right = n + b - 1
    x3 = n + raise_u(n, 2) - H + 1
    y3 = x3 + (raise_u(n_right, 2) - raise_u(n, 2) - 1)
    alpha = x3 - c(q - 1, 3)
    beta = y3 - c(q, 3)

    p = raise_u(alpha, 2) - tau + 1
    v = raise_u(beta, 2) - tau
    x4 = c(q - 1, 4) + p
    y4 = c(q, 4) + v

    P = raise_u(p, 3) - tau + 1
    V = raise_u(v, 3) - tau
    x5 = c(q - 1, 5) + P
    y5 = c(q, 5) + V

    A = raise_u(P, 4) - tau + 1
    B = raise_u(V, 4) - tau
    x6 = c(q - 1, 6) + A
    y6 = c(q, 6) + B

    gamma3 = raise_u(n_right, 2) - raise_u(n, 2) - H
    gamma4 = raise_u(y3, 3) - raise_u(x3, 3) - raise_u(n, 2) - 1
    gamma5 = raise_u(y4, 4) - raise_u(x4, 4) - raise_u(x3, 3) - 1
    gamma6 = raise_u(y5, 5) - raise_u(x5, 5) - raise_u(x4, 4) - 1
    gamma7 = raise_u(y6, 6) - raise_u(x6, 6) - raise_u(x5, 5) - 1

    # Independently normalized cancellations must agree with full orbit.
    assert gamma5 == V - P - raise_u(alpha, 2)
    assert gamma6 == B - A - raise_u(p, 3)
    C = raise_u(A, 5) - tau + 1
    D = raise_u(B, 5) - tau
    assert gamma7 == D - C - raise_u(P, 4)

    return {
        "j": j, "h": h, "q": q, "k": k, "r": r, "u": u,
        "b": b, "n": n, "H": H, "tau": tau,
        "alpha": alpha, "beta": beta, "p": p, "v": v,
        "P": P, "V": V, "A": A, "B": B,
        "gamma3": gamma3, "gamma4": gamma4, "gamma5": gamma5,
        "gamma6": gamma6, "gamma7": gamma7,
    }


def expected_words(q: int) -> dict[str, tuple[tuple[int, int], ...]]:
    return {
        "alpha": ((q - 5, 2), (25, 1)),
        "beta": ((q - 4, 2), (58, 1)),
        "p": ((q - 6, 3), (q - 10, 2), (269, 1)),
        "v": ((q - 5, 3), (q - 9, 2), (1625, 1)),
        "P": ((q - 6, 4), (q - 11, 3), (q - 15, 2), (35995, 1)),
        "V": ((q - 5, 4), (q - 10, 3), (q - 14, 2), (1319452, 1)),
    }


def main() -> None:
    first = family(33)
    expected_first = {
        "q": 320690891436,
        "gamma3": -1282763565721,
        "gamma4": -1282763564414,
        "gamma5": -1282762282557,
        "gamma6": -412935273326,
        "gamma7": 129084548046247672655610,
    }
    for key, value in expected_first.items():
        assert first[key] == value

    words = expected_words(first["q"])
    for name, expected in words.items():
        rank = expected[0][1]
        assert canonical(first[name], rank) == expected

    # Pascal cancellation formulas are literal throughout the stable range.
    checked = []
    for j in (17, 29, 31, 33, 35, 37, 55):
        row = family(j)
        q = row["q"]
        for name, expected in expected_words(q).items():
            rank = expected[0][1]
            assert canonical(row[name], rank) == expected
        formulas = {
            "gamma3": 23 - 4 * q,
            "gamma4": 1330 - 4 * q,
            "gamma5": 1283187 - 4 * q,
            "gamma6": 869828292418 - 4 * q,
        }
        for name, expected in formulas.items():
            assert row[name] == expected
        checked.append({name: row[name] for name in (
            "j", "q", "gamma3", "gamma4", "gamma5", "gamma6", "gamma7"
        )})

    # Exact thresholds. All displayed words are canonical iff q>1,319,466.
    stable_q_threshold = 1_319_466
    assert family(15)["q"] <= stable_q_threshold
    assert family(17)["q"] > stable_q_threshold

    gamma5_q_floor = 320_796  # gamma5<0 iff integer q>=320797.
    gamma6_q_floor = 217_457_073_104  # gamma6<0 iff q>=217457073105.
    row31 = family(31)
    assert row31["q"] > gamma5_q_floor and row31["q"] <= gamma6_q_floor
    assert row31["gamma5"] < 0 < row31["gamma6"]
    assert first["q"] > gamma6_q_floor
    assert first["gamma5"] < 0 and first["gamma6"] < 0

    # q_(j+2)=4q_j-4 is increasing, so every odd j>=33 stays double negative.
    assert family(35)["q"] == 4 * first["q"] - 4

    print(json.dumps({
        "schema": "amra.erdos776.k4-r9-rank6-counterfamily-independent-audit.v1",
        "engine": "independent greedy Macaulay full-orbit; no author-verifier import",
        "actual_family": {
            "identity": "C(b-1,2)+2-(C(q,2)+9)=2h",
            "integrality": "odd j gives h=1 mod 3 and q=(2h+4)/3 in Z",
            "recurrence": "q_(j+2)=4q_j-4",
        },
        "canonical_stability": {
            "all_six_words": "q>1319466",
            "first_odd_j_in_stable_range": 17,
        },
        "sign_thresholds": {
            "gamma5_negative": "q>=320797",
            "gamma6_negative": "q>=217457073105",
            "j31": {"q": row31["q"], "gamma5": row31["gamma5"], "gamma6": row31["gamma6"]},
            "first_stable_odd_double_negative_j": 33,
            "all_odd_j_at_least_33_double_negative": True,
        },
        "first_witness": {key: first[key] for key in (
            "j", "h", "q", "b", "n", "tau", "gamma3", "gamma4",
            "gamma5", "gamma6", "gamma7"
        )},
        "first_witness_canonical_words": {
            name: [list(pair) for pair in canonical(first[name], expected[0][1])]
            for name, expected in words.items()
        },
        "selected_full_orbit_checks": checked,
        "verdict": "pass_infinite_actual_family; scoped_refutation_only",
        "scope": {
            "refutes": ["M305-rank6-deficit-domination", "fixed two-row rank-five/rank-six recovery"],
            "does_not_refute": ["adaptive recovery", "global interface", "public Erdos-776 problem"],
        },
        "lean_used": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
