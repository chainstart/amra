#!/usr/bin/env python3
"""Structured falsifier for the (++ -> ++) sufficient gate (G++)."""

from __future__ import annotations

import json
from math import comb


def upper(number: int, degree: int) -> int:
    remainder = number
    cap = None
    answer = 0
    for lower_degree in range(degree, 0, -1):
        if remainder == 0:
            break
        lo = lower_degree - 1
        hi = cap if cap is not None else max(2, lower_degree + 1)
        if cap is None:
            while comb(hi, lower_degree) <= remainder:
                hi *= 2
        while lo + 1 < hi:
            middle = (lo + hi) // 2
            if comb(middle, lower_degree) <= remainder:
                lo = middle
            else:
                hi = middle
        if lo >= lower_degree:
            remainder -= comb(lo, lower_degree)
            answer += comb(lo, lower_degree + 1)
            cap = lo
    assert remainder == 0
    return answer


def row(j: int, k: int, r: int):
    h = 112 * (1 << (j - 1))
    divisor = k - 1
    base = 2 * h - comb(k - 1, 2) - 2
    if (base + r) % divisor:
        return None
    q = (base + r) // divisor
    u = r + k - 1
    b = q + k
    if not (q >= 2 and 0 <= r < q and 0 <= u < q + 1 and 5 <= b < h):
        return None
    n = comb(q, 2) + r
    H = comb(b, 2) + 1
    tau = H - n
    z = upper(n, 2)
    w = upper(n + b - 1, 2)
    gamma3 = w - z - H
    x = n + z - H + 1
    y = n + w - H
    if gamma3 >= 0 or x < 0:
        return None
    gamma4 = upper(y, 3) - upper(x, 3) - x - tau
    alpha = comb(r + 1, 2) - k * q - comb(k, 2)
    beta = alpha + comb(u, 2) - comb(r, 2) - 1
    if min(alpha, beta) < 0:
        return {"target": False}
    p = upper(alpha, 2) - tau + 1
    v = upper(beta, 2) - tau
    e = v - p
    margin = upper(e, 3) - upper(alpha, 2) - 1 if e >= 0 else None
    return {
        "target": p >= 0 and v >= 0,
        "j": j, "q": q, "k": k, "r": r,
        "alpha": alpha, "beta": beta, "p": p, "v": v,
        "e": e, "gamma4": gamma4, "margin": margin,
    }


def first_target_r(j: int, k: int):
    h = 112 * (1 << (j - 1))
    divisor = k - 1
    base = 2 * h - comb(k - 1, 2) - 2
    residue = (-base) % divisor

    def target(index: int) -> bool:
        data = row(j, k, residue + index * divisor)
        return data is not None and bool(data.get("target"))

    low = 0
    high = 1
    while high < 10**30 and not target(high):
        high *= 2
    if high >= 10**30:
        return None
    while low + 1 < high:
        middle = (low + high) // 2
        if target(middle):
            high = middle
        else:
            low = middle
    return residue + high * divisor


def main() -> None:
    scales = list(range(6, 61)) + [70, 80, 90, 100]
    accepted = 0
    minimum = None
    counterexamples = []
    for j in scales:
        for k in range(4, 301):
            start = first_target_r(j, k)
            if start is None:
                continue
            for offset in range(-3, 301):
                data = row(j, k, start + offset * (k - 1))
                if data is None or not data.get("target") or data["gamma4"] >= 0:
                    continue
                accepted += 1
                if minimum is None or data["margin"] < minimum["margin"]:
                    minimum = data
                if data["margin"] is None or data["margin"] < 0:
                    counterexamples.append(data)
                    break
    print(json.dumps({
        "schema": "amra.erdos776.gpp-moving-boundary-search.v1",
        "domain": {
            "j": scales,
            "k": [4, 300],
            "offsets_from_first_target_boundary": [-3, 300],
        },
        "accepted_pp_to_pp_rows": accepted,
        "minimum_margin": minimum,
        "counterexample_count": len(counterexamples),
        "first_counterexample": counterexamples[:1],
        "structured_falsifier_only": True,
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
