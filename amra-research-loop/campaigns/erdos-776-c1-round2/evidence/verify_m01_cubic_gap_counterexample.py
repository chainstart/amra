#!/usr/bin/env python3
"""Exact verifier for the first M01 cubic-gap counterexample."""

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


def main() -> None:
    j, q, k, r = 7, 4845, 4, 204
    h = 112 * (1 << (j - 1))
    b = q + k
    u = r + k - 1
    assert (k - 1) * q + comb(k - 1, 2) + 2 - r == 2 * h
    assert q >= 2 and 0 <= r < q and 0 <= u < q + 1 and 5 <= b < h
    tau = k * q + comb(k, 2) + 1 - r
    alpha = comb(r + 1, 2) - k * q - comb(k, 2)
    beta = alpha + comb(u, 2) - comb(r, 2) - 1
    assert alpha == comb(55, 2) + 39 == 1524
    assert beta == comb(65, 2) + 58 == 2138
    p = upper(alpha, 2) - tau + 1
    v = upper(beta, 2) - tau
    e = v - p
    gamma4 = e - comb(r, 2)
    cubic_gap = e - comb(54, 3)
    gpp_margin = upper(e, 3) - upper(alpha, 2) - 1
    gamma5 = upper(v, 3) - upper(p, 3) - upper(alpha, 2) - 1
    assert min(alpha, beta, p, v) >= 0 and gamma4 < 0
    assert cubic_gap == -6448 < 0
    assert gpp_margin == 183083 > 0 and gamma5 == 245481 > 0
    print(json.dumps({
        "schema": "amra.erdos776.m01-cubic-gap-counterexample.v1",
        "parameters": {"j": j, "h": h, "q": q, "k": k, "r": r, "u": u, "b": b},
        "values": {
            "tau": tau, "alpha": alpha, "beta": beta, "a": 55,
            "p": p, "v": v, "e": e, "gamma4": gamma4,
            "e_minus_C_a_minus_1_3": cubic_gap,
            "Gpp_margin": gpp_margin, "gamma5": gamma5,
        },
        "interpretation": "M01 is false, while the weaker G++ gate and actual gamma5 remain positive.",
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

