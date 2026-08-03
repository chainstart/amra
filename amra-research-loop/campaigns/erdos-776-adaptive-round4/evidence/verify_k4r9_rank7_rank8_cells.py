#!/usr/bin/env python3
"""Exact K4,r9 rank-seven/rank-eight canonical-cell verifier."""

from __future__ import annotations

import json
from math import comb
import sympy as sp


def C(n: int, k: int) -> int:
    return comb(n, k) if n >= k >= 0 else 0


def largest(value: int, rank: int, upper: int | None = None) -> int:
    lo = rank - 1
    hi = upper if upper is not None else max(rank, 2)
    if upper is None:
        while C(hi, rank) <= value:
            hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if C(mid, rank) <= value:
            lo = mid
        else:
            hi = mid
    if upper is not None and C(hi, rank) <= value:
        return hi
    return lo


def word(value: int, rank: int) -> tuple[tuple[int, int], ...]:
    rem = value
    upper = None
    out = []
    for k in range(rank, 0, -1):
        if rem == 0:
            break
        t = largest(rem, k, upper)
        if t >= k:
            out.append((t, k))
            rem -= C(t, k)
            upper = t - 1
    assert rem == 0
    return tuple(out)


def value(w):
    return sum(C(t, k) for t, k in w)


def upper(w):
    return sum(C(t, k + 1) for t, k in w)


def q_of(j: int) -> int:
    assert j % 2 == 1
    h = 112 * 2 ** (j - 1)
    assert (2 * h + 4) % 3 == 0
    return (2 * h + 4) // 3


def expected_P(q):
    return ((q - 6, 4), (q - 11, 3), (q - 15, 2), (35995, 1))


def expected_V(q):
    return ((q - 5, 4), (q - 10, 3), (q - 14, 2), (1319452, 1))


def A_word(q):
    return ((q - 6, 5), (q - 11, 4), (q - 16, 3), (q - 20, 2), (647801944, 1))


def B33_word(q):
    return ((q - 5, 5), (q - 10, 4), (q - 15, 3), (q - 17, 2), (229094347523, 1))


def Bstable_word(q):
    return ((q - 5, 5), (q - 10, 4), (q - 15, 3), (q - 19, 2), (870476130358, 1))


def C_word(q):
    return ((q - 6, 6), (q - 11, 5), (q - 16, 4), (q - 21, 3), (q - 25, 2), (209823679001188505, 1))


def D73_word(q):
    return ((q - 5, 6), (q - 10, 5), (q - 15, 4), (q - 20, 3), (q - 23, 2), (26260982706816823916203, 1))


def Dstable_word(q):
    return ((q - 5, 6), (q - 10, 5), (q - 15, 4), (q - 20, 3), (q - 24, 2), (378864346761083666538815, 1))


def row(j: int):
    q = q_of(j)
    tau = 4 * q - 2
    P, V = value(expected_P(q)), value(expected_V(q))
    A = upper(expected_P(q)) - tau + 1
    B = upper(expected_V(q)) - tau
    Ctail = upper(word(A, 5)) - tau + 1
    Dtail = upper(word(B, 5)) - tau
    gamma7 = upper(word(B, 5)) - upper(word(A, 5)) - upper(expected_P(q)) - 1
    gamma8 = upper(word(Dtail, 6)) - upper(word(Ctail, 6)) - upper(word(A, 5)) - 1
    return {"j": j, "q": q, "tau": tau, "P": P, "V": V, "A": A, "B": B,
            "C": Ctail, "D": Dtail, "Aword": word(A, 5), "Bword": word(B, 5),
            "Cword": word(Ctail, 6), "Dword": word(Dtail, 6),
            "gamma7": gamma7, "gamma8": gamma8}


def symbolic_guards():
    q = sp.symbols("q", integer=True, positive=True)
    cb = sp.binomial
    U = lambda w: sum(cb(t, k + 1) for t, k in w)
    P = expected_P(q)
    Aw = A_word(q)
    B33 = B33_word(q)
    Bs = Bstable_word(q)
    Cw = C_word(q)
    D73 = D73_word(q)
    Ds = Dstable_word(q)
    tau = 4 * q - 2
    assert sp.simplify(U(P) - tau + 1 - sum(cb(t, k) for t, k in Aw)) == 0
    gamma7_33 = sp.simplify(U(B33) - U(Aw) - U(P) - 1)
    gamma7_stable = sp.simplify(U(Bs) - U(Aw) - U(P) - 1)
    assert sp.expand_func(gamma7_33).expand() == q*q - 42*q + 26241900209700351953826
    assert sp.expand_func(gamma7_stable).expand() == 378864136937404017548365 - 4*q
    assert sp.simplify(U(Aw) - tau + 1 - sum(cb(t, k) for t, k in Cw)) == 0
    gamma8_stable = sp.simplify(U(Ds) - U(Cw) - U(Aw) - 1)
    assert sp.expand_func(gamma8_stable).expand() == 71769096623329310875999415996803170658344870942 - 4*q
    return {
        "gamma7_j33_cell": str(sp.expand_func(gamma7_33).expand()),
        "gamma7_stable_j_ge_35_cell": str(sp.expand_func(gamma7_stable).expand()),
        "gamma8_stable_j_ge_75_cell": str(sp.expand_func(gamma8_stable).expand()),
    }


def main():
    symbolic = symbolic_guards()
    checks = []
    for j in (33, 35, 37, 71, 73, 75, 77, 147, 149):
        r = row(j)
        q = r["q"]
        assert r["Aword"] == A_word(q)
        if j == 33:
            assert r["Bword"] == B33_word(q)
            assert r["gamma7"] == q*q - 42*q + 26241900209700351953826
        else:
            assert r["Bword"] == Bstable_word(q)
            assert r["gamma7"] == 378864136937404017548365 - 4*q
        if j == 73:
            assert r["Cword"] == C_word(q) and r["Dword"] == D73_word(q)
        if j >= 75:
            assert r["Cword"] == C_word(q) and r["Dword"] == Dstable_word(q)
            assert r["gamma8"] == 71769096623329310875999415996803170658344870942 - 4*q
        checks.append({k: r[k] for k in ("j", "q", "gamma7", "gamma8")})
    assert row(71)["gamma7"] > 0 > row(73)["gamma7"]
    assert row(147)["gamma8"] > 0 > row(149)["gamma8"]
    print(json.dumps({
        "schema": "amra.erdos776.adaptive-round4.k4r9-canonical-cells.v1",
        "symbolic": symbolic,
        "selected_actual_rows": checks,
        "first_odd_stable_gamma7_negative_j": 73,
        "first_odd_stable_gamma8_negative_j": 149,
        "verdict": "j33 quadratic is a single cell; stable later cells are linear and eventually negative",
        "scope_warning": "fixed K4,r9 family only; no public promotion",
    }, indent=2))


if __name__ == "__main__":
    main()
