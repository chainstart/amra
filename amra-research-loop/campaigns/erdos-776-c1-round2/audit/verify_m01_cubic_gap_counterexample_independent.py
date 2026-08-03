#!/usr/bin/env python3
"""Independent raw-recurrence audit of the M01 counterexample.

No code or precomputed intermediate value is imported from the search that
found the witness.  The full Macaulay orbit is rebuilt from (j,q,k,r).
"""

from __future__ import annotations

import json
from math import comb


def macaulay(number: int, degree: int) -> tuple[int, list[tuple[int, int]]]:
    if number < 0 or degree < 1:
        raise ValueError((number, degree))
    remainder = number
    cap: int | None = None
    expansion: list[tuple[int, int]] = []
    for lower in range(degree, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        hi = cap if cap is not None else max(2, lower + 1)
        if cap is None:
            while comb(hi, lower) <= remainder:
                hi *= 2
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if comb(mid, lower) <= remainder:
                lo = mid
            else:
                hi = mid
        if lo >= lower:
            remainder -= comb(lo, lower)
            expansion.append((lo, lower))
            cap = lo
    if remainder:
        raise AssertionError((number, degree, remainder))
    raised = sum(comb(top, lower + 1) for top, lower in expansion)
    return raised, expansion


def up(number: int, degree: int) -> int:
    return macaulay(number, degree)[0]


def main() -> None:
    j, q, k, r = 7, 4845, 4, 204
    h = 112 * 2 ** (j - 1)
    b, u = q + k, r + k - 1

    # Actual c=1 state, reconstructed from both adjacent rank-2 expansions.
    n = comb(q, 2) + r
    assert n == comb(b - 1, 2) + 2 - 2 * h
    assert n + b - 1 == comb(q + 1, 2) + u
    assert 0 <= r < q and 0 <= u < q + 1 and 5 <= b < h
    c = 1

    H = comb(b, 2) + 1
    tau = H - n
    z = up(n, 2)
    w = up(n + b - 1, 2)
    gamma3 = w - z - H
    x0 = n + z - H + 1
    y0 = n + w - H
    assert gamma3 < 0 and x0 >= 0

    # First raw recurrence and its independently checked positive tails.
    gamma4 = up(y0, 3) - up(x0, 3) - x0 - tau
    alpha = x0 - comb(q, 3)
    beta = y0 - comb(q + 1, 3)
    assert alpha == 1524 and beta == 2138
    assert 0 <= alpha < comb(q, 2) and 0 <= beta < comb(q + 1, 2)
    assert gamma4 < 0

    # Second raw recurrence.  Equality with the tail form proves the actual
    # transition is (++ -> ++), not merely a formal tail construction.
    x1 = up(x0, 3) - tau + 1
    y1 = up(y0, 3) - tau
    p = x1 - comb(q, 4)
    v = y1 - comb(q + 1, 4)
    assert p == 7794 and v == 26150
    assert 0 <= p < comb(q, 3) and 0 <= v < comb(q + 1, 3)
    transition = "++ -> ++"

    gamma5_raw = up(y1, 4) - up(x1, 4) - x1 - tau
    gamma5_tail = up(v, 3) - up(p, 3) - up(alpha, 2) - 1
    assert gamma5_raw == gamma5_tail == 245481 > 0

    # Audit the rejected strengthening and the surviving weaker gate.
    rank2_index = 55
    rank2_remainder = alpha - comb(rank2_index, 2)
    assert rank2_remainder == 39
    e = v - p
    cubic_threshold = comb(rank2_index - 1, 3)
    cubic_gap = e - cubic_threshold
    gpp_margin = up(e, 3) - up(alpha, 2) - 1
    assert e == 18356 and cubic_threshold == 24804 and cubic_gap == -6448
    assert gpp_margin == 183083 > 0

    output = {
        "schema": "amra.erdos776.m01-independent-raw-audit.v1",
        "independence": {
            "imports_author_evidence": False,
            "starting_data": {"j": j, "q": q, "k": k, "r": r},
            "method": "canonical Macaulay expansion plus full raw recurrence",
        },
        "actual_state": {
            "h": h, "b": b, "u": u, "c": c, "n": n, "H": H,
            "tau": tau, "gamma3": gamma3,
        },
        "raw_orbit": {
            "x0": x0, "y0": y0, "alpha": alpha, "beta": beta,
            "gamma4": gamma4, "x1": x1, "y1": y1, "p": p, "v": v,
            "transition": transition, "gamma5_raw": gamma5_raw,
            "gamma5_tail": gamma5_tail,
        },
        "decisive_checks": {
            "alpha_decomposition": "C(55,2)+39",
            "e": e,
            "C(54,3)": cubic_threshold,
            "e_minus_C(54,3)": cubic_gap,
            "Gpp_margin": gpp_margin,
            "gamma5": gamma5_raw,
        },
        "verdict": "witness independently reproduced; M01 false while G++ and gamma5 stay positive",
        "public_problem_closed": False,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
