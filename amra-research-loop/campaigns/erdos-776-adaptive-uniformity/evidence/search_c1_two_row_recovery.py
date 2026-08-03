#!/usr/bin/env python3
"""Adversarial actual-state search for c=1 two-row recovery."""

from math import comb, isqrt
import json


def upper(number: int, rank: int) -> int:
    assert number >= 0
    remainder = number
    ceiling = None
    answer = 0
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
            remainder -= comb(lo, lower)
            answer += comb(lo, lower + 1)
            ceiling = lo
    assert remainder == 0
    return answer


def candidate(j: int, k: int, r: int):
    h = 112 * (1 << (j - 1))
    numerator = 2 * h - comb(k - 1, 2) - 2 + r
    if k <= 1 or numerator % (k - 1):
        return None
    q = numerator // (k - 1)
    u = r + k - 1
    b = q + k
    if not (q >= 2 and 0 <= r < q and 0 <= u < q + 1 and 5 <= b < h):
        return None
    n = comb(q, 2) + r
    assert n == comb(b - 1, 2) + 2 - 2 * h
    H = comb(b, 2) + 1
    tau = H - n
    z = comb(q, 3) + comb(r, 2)
    w = comb(q + 1, 3) + comb(u, 2)
    gamma3 = w - z - H
    x = n + z - H + 1
    y = n + w - H
    if gamma3 >= 0 or x < 0:
        return None
    gamma4 = upper(y, 3) - upper(x, 3) - z - 1
    if gamma4 >= 0:
        return None

    a_tail = comb(r + 1, 2) - k * q - comb(k, 2)
    b_tail = a_tail + comb(u, 2) - comb(r, 2) - 1
    eps_a, eps_b = int(a_tail < 0), int(b_tail < 0)
    a = q - eps_a
    gap = 1 + eps_a - eps_b
    alpha = a_tail + eps_a * comb(q - 1, 2)
    beta = b_tail + eps_b * comb(q, 2)
    if not (0 <= alpha < comb(a, 2) and 0 <= beta < comb(a + gap, 2)):
        return None
    p = upper(alpha, 2) - tau + 1
    v = upper(beta, 2) - tau
    second = ("-" if p < 0 else "+") + ("-" if v < 0 else "+")
    first = ("-" if a_tail < 0 else "+") + ("-" if b_tail < 0 else "+")
    transition = first + " -> " + second
    if first in {"++", "--"}:
        assert gamma4 == upper(beta, 2) - upper(alpha, 2) - alpha - tau

    # The target adversarial chambers have p,v>=0, so the adjacent leading
    # blocks remain explicit for two further rows.
    if min(p, v) < 0:
        return None
    gamma5 = upper(v, 3) - upper(p, 3) - upper(alpha, 2) - 1
    P = upper(p, 3) - tau + 1
    V = upper(v, 3) - tau
    if min(P, V) < 0:
        gamma6 = None
    else:
        gamma6 = upper(V, 4) - upper(P, 4) - upper(p, 3) - 1
    return {"j": j, "h": h, "b": b, "q": q, "k": k, "r": r, "u": u,
            "transition": transition, "alpha": alpha, "beta": beta,
            "p": p, "v": v, "P": P, "V": V, "tau": tau,
            "gamma4": gamma4, "gamma5": gamma5, "gamma6": gamma6}


def main() -> None:
    targets = {"++ -> ++", "-- -> ++"}
    counts = {target: 0 for target in targets}
    minima5 = {}
    minima6 = {}
    first_negative5 = {}
    negative5_fibres = {}
    double_negative = []
    rank6_borrow_failures = []
    tested_parameter_triples = 0
    for j in range(2, 31):
        h = 112 * (1 << (j - 1))
        for k in range(2, 2001):
            divisor = k - 1
            base = 2 * h - comb(k - 1, 2) - 2
            residue = (-base) % divisor

            # Test every admissible low-r residue, where all known gamma5<0
            # families live, plus a moving window around the ++/-- wall
            # C(r+1,2) = k*q + C(k,2).  The latter keeps the ++ search
            # adversarial when q grows far beyond the fixed low-r box.
            rs = set(range(residue, 2001, divisor))
            q0 = max(0, base // divisor)
            wall = isqrt(max(0, 2 * k * q0 + k * (k - 1)))
            wall_index = round((wall - residue) / divisor)
            for offset in range(-24, 25):
                r_wall = residue + (wall_index + offset) * divisor
                if r_wall >= 0:
                    rs.add(r_wall)
            for r in sorted(rs):
                tested_parameter_triples += 1
                row = candidate(j, k, r)
                if row is None or row["transition"] not in targets:
                    continue
                transition = row["transition"]
                counts[transition] += 1
                if transition not in minima5 or row["gamma5"] < minima5[transition]["gamma5"]:
                    minima5[transition] = row
                if row["gamma6"] is not None and (transition not in minima6 or row["gamma6"] < minima6[transition]["gamma6"]):
                    minima6[transition] = row
                if row["gamma5"] < 0:
                    first_negative5.setdefault(transition, row)
                    fibre = negative5_fibres.setdefault(row["k"], {
                        "state_count": 0, "r_values": set()})
                    fibre["state_count"] += 1
                    fibre["r_values"].add(row["r"])
                    if row["gamma6"] is None:
                        rank6_borrow_failures.append(row)
                    elif row["gamma6"] < 0:
                        double_negative.append(row)
    assert all(counts.values())
    print(json.dumps({
        "schema": "amra.erdos776.c1-two-row-adversarial-search.v1",
        "domain": {
            "j": [2, 30],
            "k": [2, 2000],
            "r_strategy": [
                "all divisibility-compatible r in [0,2000]",
                "49 divisibility-compatible probes around the first-tail sign wall"
            ],
            "tested_parameter_triples": tested_parameter_triples
        },
        "counts": counts,
        "minimum_gamma5": minima5,
        "minimum_gamma6_where_nonnegative_tails": minima6,
        "first_negative_gamma5": first_negative5,
        "negative_gamma5_fibres": {
            str(k): {
                "state_count": fibre["state_count"],
                "r_values": sorted(fibre["r_values"])
            }
            for k, fibre in sorted(negative5_fibres.items())
        },
        "negative_gamma5_and_gamma6_count": len(double_negative),
        "first_double_negative": double_negative[:1],
        "negative_gamma5_with_rank6_borrow_count": len(rank6_borrow_failures),
        "first_negative_gamma5_with_rank6_borrow": rank6_borrow_failures[:1],
        "candidate_invariant_failure_count": (
            len(rank6_borrow_failures) + len(double_negative)
        ),
        "finite_search_only": True,
        "public_problem_closed": False
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
