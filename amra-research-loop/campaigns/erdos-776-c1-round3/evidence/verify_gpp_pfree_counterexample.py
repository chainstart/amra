#!/usr/bin/env python3
"""Exact actual-state counterexample to the p-free G++ sufficient gate."""

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


def main() -> None:
    j, k, r = 21, 4, 26466
    h = 112 * (1 << (j - 1))
    q = (2 * h - comb(k - 1, 2) - 2 + r) // (k - 1)
    u, b = r + k - 1, q + k
    n = comb(q, 2) + r
    H = comb(b, 2) + 1
    tau = H - n
    assert (q, h, u, b) == (78302495, 117440512, 26469, 78302499)
    assert n == comb(b - 1, 2) + 2 - 2 * h
    assert 0 <= r < q and 0 <= u < q + 1 and 5 <= b < h

    z = upper(n, 2)
    w = upper(n + b - 1, 2)
    gamma3 = w - z - H
    x = n + z - H + 1
    y = n + w - H
    gamma4_direct = upper(y, 3) - upper(x, 3) - z - 1

    alpha = comb(r + 1, 2) - k * q - comb(k, 2)
    beta = alpha + comb(u, 2) - comb(r, 2) - 1
    assert alpha >= 0 and beta >= 0
    p = upper(alpha, 2) - tau + 1
    v = upper(beta, 2) - tau
    e = v - p
    assert p >= 0 and v >= 0
    gamma4_chart = upper(beta, 2) - upper(alpha, 2) - alpha - tau
    pfree_margin = upper(e, 3) - upper(alpha, 2) - 1
    gamma5_exact = upper(v, 3) - upper(p, 3) - upper(alpha, 2) - 1

    # Independent full-state next row.
    x4, y4 = upper(x, 3) - tau + 1, upper(y, 3) - tau
    gamma5_direct = upper(y4, 4) - upper(x4, 4) - upper(x, 3) - 1
    assert gamma4_direct == gamma4_chart == -13858416
    assert pfree_margin == -136419183
    assert gamma5_exact == gamma5_direct == 859354068710

    result = {
        "schema": "amra.erdos776.gpp-pfree-counterexample.v1",
        "parameters": {"j": j, "h": h, "q": q, "k": k,
                       "r": r, "u": u, "b": b},
        "values": {"tau": tau, "alpha": alpha, "beta": beta,
                   "p": p, "v": v, "e": e, "gamma3": gamma3,
                   "gamma4": gamma4_direct,
                   "p_free_Gpp_margin": pfree_margin,
                   "exact_gamma5": gamma5_exact},
        "conclusion": "The p-free superadditivity gate U_3(e)>=U_2(alpha)+1 and M303's nested e threshold are false on an actual (++ -> ++) state, while the exact base-dependent rank-five surplus is positive.",
        "scope": "Refutes the sufficient reduction, not exact (++ -> ++) recovery or the public problem.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "public_problem_closed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
