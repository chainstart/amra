#!/usr/bin/env python3
"""Independent audit of the c=1 two-row recovery normal form.

This file deliberately does not import the evidence search it audits.  It
computes the full Macaulay orbit and the normalized tail formula separately,
then compares them on actual dyadic states.
"""

from __future__ import annotations

import json
from math import comb, isqrt


def macaulay_raise(number: int, degree: int) -> int:
    if number < 0 or degree < 1:
        raise ValueError("Macaulay raise requires number >= 0 and degree >= 1")
    remainder = number
    cap: int | None = None
    raised = 0
    for lower_degree in range(degree, 0, -1):
        if remainder == 0:
            break
        low = lower_degree - 1
        high = cap if cap is not None else max(2, lower_degree + 1)
        if cap is None:
            while comb(high, lower_degree) <= remainder:
                high *= 2
        while low + 1 < high:
            middle = (low + high) // 2
            if comb(middle, lower_degree) <= remainder:
                low = middle
            else:
                high = middle
        if low >= lower_degree:
            remainder -= comb(low, lower_degree)
            raised += comb(low, lower_degree + 1)
            cap = low
    if remainder:
        raise AssertionError((number, degree, remainder))
    return raised


def actual_state(j: int, k: int, r: int) -> dict[str, int | str] | None:
    h = 112 * (1 << (j - 1))
    divisor = k - 1
    numerator = 2 * h - comb(k - 1, 2) - 2 + r
    if divisor < 1 or numerator % divisor:
        return None
    q = numerator // divisor
    u = r + k - 1
    b = q + k
    if not (q >= 2 and 0 <= r < q and 0 <= u < q + 1 and 5 <= b < h):
        return None

    n = comb(q, 2) + r
    H = comb(b, 2) + 1
    tau = H - n
    z = macaulay_raise(n, 2)
    w = macaulay_raise(n + b - 1, 2)
    gamma3 = w - z - H
    x0 = n + z - H + 1
    y0 = n + w - H
    if gamma3 >= 0 or x0 < 0:
        return None
    gamma4_full = macaulay_raise(y0, 3) - macaulay_raise(x0, 3) - x0 - tau
    if gamma4_full >= 0:
        return None

    raw_a = comb(r + 1, 2) - k * q - comb(k, 2)
    raw_b = raw_a + comb(u, 2) - comb(r, 2) - 1
    first = ("-" if raw_a < 0 else "+") + ("-" if raw_b < 0 else "+")
    borrow_a = int(raw_a < 0)
    borrow_b = int(raw_b < 0)
    a = q - borrow_a
    gap = 1 + borrow_a - borrow_b
    alpha = raw_a + borrow_a * comb(q - 1, 2)
    beta = raw_b + borrow_b * comb(q, 2)
    if not (0 <= alpha < comb(a, 2) and 0 <= beta < comb(a + gap, 2)):
        return None
    if x0 != comb(a, 3) + alpha or y0 != comb(a + gap, 3) + beta:
        raise AssertionError("first normalization disagrees with the raw orbit")

    p = macaulay_raise(alpha, 2) - tau + 1
    v = macaulay_raise(beta, 2) - tau
    second = ("-" if p < 0 else "+") + ("-" if v < 0 else "+")
    transition = first + " -> " + second
    if transition not in {"++ -> ++", "-- -> ++"}:
        return {"transition": transition, "gamma4": gamma4_full}

    # Target ++: compare a fresh full-orbit step against the tail identity.
    if not (0 <= p < comb(a, 3) and 0 <= v < comb(a + 1, 3)):
        raise AssertionError("target ++ tail is outside its advertised cap")
    x1 = macaulay_raise(x0, 3) - tau + 1
    y1 = macaulay_raise(y0, 3) - tau
    if x1 != comb(a, 4) + p or y1 != comb(a + 1, 4) + v:
        raise AssertionError("second normalization disagrees with the raw orbit")
    gamma5_full = macaulay_raise(y1, 4) - macaulay_raise(x1, 4) - x1 - tau
    gamma5_tail = (
        macaulay_raise(v, 3) - macaulay_raise(p, 3)
        - macaulay_raise(alpha, 2) - 1
    )
    if gamma5_full != gamma5_tail:
        raise AssertionError("gamma5 formula disagrees with the raw orbit")

    P = macaulay_raise(p, 3) - tau + 1
    V = macaulay_raise(v, 3) - tau
    gamma6_full: int | None = None
    gamma6_tail: int | None = None
    if P >= 0 and V >= 0:
        if not (P < comb(a, 4) and V < comb(a + 1, 4)):
            raise AssertionError("rank-six tail is outside its advertised cap")
        x2 = macaulay_raise(x1, 4) - tau + 1
        y2 = macaulay_raise(y1, 4) - tau
        gamma6_full = macaulay_raise(y2, 5) - macaulay_raise(x2, 5) - x2 - tau
        gamma6_tail = (
            macaulay_raise(V, 4) - macaulay_raise(P, 4)
            - macaulay_raise(p, 3) - 1
        )
        if gamma6_full != gamma6_tail:
            raise AssertionError("gamma6 formula disagrees with the raw orbit")

    e = v - p
    sufficient_margin = None
    if e >= 0:
        sufficient_margin = macaulay_raise(e, 3) - macaulay_raise(alpha, 2) - 1
    return {
        "j": j, "q": q, "k": k, "r": r, "transition": transition,
        "gamma4": gamma4_full, "gamma5": gamma5_full,
        "P": P, "V": V, "gamma6": gamma6_full,
        "sufficient_margin": sufficient_margin,
    }


def compatible_near_wall(j: int, k: int, wall: str, radius: int = 25) -> set[int]:
    """Find compatible r near the exact raw-a or raw-b sign wall."""
    h = 112 * (1 << (j - 1))
    divisor = k - 1
    base = 2 * h - comb(k - 1, 2) - 2
    residue = (-base) % divisor

    def wall_value(r: int) -> int:
        q = (base + r) // divisor
        raw_a = comb(r + 1, 2) - k * q - comb(k, 2)
        if wall == "a":
            return raw_a
        u = r + k - 1
        return raw_a + comb(u, 2) - comb(r, 2) - 1

    # Both expressions are eventually increasing.  Start beyond the small
    # non-monotone prefix, bracket the first nonnegative compatible point,
    # and binary-search in the residue-class index.
    start_index = max(0, (k + 2 - residue + divisor - 1) // divisor)
    low_index = start_index
    high_index = max(start_index + 1, isqrt(4 * h * max(2, k)) // divisor + 4)
    while wall_value(residue + high_index * divisor) < 0:
        high_index *= 2
    while low_index + 1 < high_index:
        middle = (low_index + high_index) // 2
        if wall_value(residue + middle * divisor) < 0:
            low_index = middle
        else:
            high_index = middle
    return {
        residue + index * divisor
        for index in range(max(0, high_index - radius), high_index + radius + 1)
    }


def compact(row: dict[str, int | str | None]) -> dict[str, int | str | None]:
    keys = ("j", "q", "k", "r", "transition", "gamma4", "gamma5", "P", "V", "gamma6", "sufficient_margin")
    return {key: row[key] for key in keys}


def main() -> None:
    counts: dict[str, int] = {}
    minima5: dict[str, dict[str, int | str | None]] = {}
    minima_margin: dict[str, dict[str, int | str | None]] = {}
    minima6_after_negative: dict[str, int | str | None] | None = None
    gamma5_negative = 0
    negative_k: set[int] = set()
    negative_r: set[int] = set()
    borrowed_after_negative = 0
    double_negative = 0
    target_rows = 0
    parameter_probes = 0
    unexpected_target_sources: dict[str, int] = {}

    for j in range(2, 33):
        h = 112 * (1 << (j - 1))
        for k in range(2, 3001):
            divisor = k - 1
            base = 2 * h - comb(k - 1, 2) - 2
            residue = (-base) % divisor
            probes = set(range(residue, 3001, divisor))
            probes.update(compatible_near_wall(j, k, "a"))
            probes.update(compatible_near_wall(j, k, "b"))
            for r in probes:
                parameter_probes += 1
                row = actual_state(j, k, r)
                if row is None:
                    continue
                transition = str(row["transition"])
                if transition.endswith("-> ++") and transition not in {"++ -> ++", "-- -> ++"}:
                    unexpected_target_sources[transition] = unexpected_target_sources.get(transition, 0) + 1
                if transition not in {"++ -> ++", "-- -> ++"}:
                    continue
                target_rows += 1
                counts[transition] = counts.get(transition, 0) + 1
                old = minima5.get(transition)
                if old is None or int(row["gamma5"]) < int(old["gamma5"]):
                    minima5[transition] = compact(row)
                if row["sufficient_margin"] is not None:
                    old_margin = minima_margin.get(transition)
                    if old_margin is None or int(row["sufficient_margin"]) < int(old_margin["sufficient_margin"]):
                        minima_margin[transition] = compact(row)
                if int(row["gamma5"]) < 0:
                    gamma5_negative += 1
                    negative_k.add(int(row["k"]))
                    negative_r.add(int(row["r"]))
                    if int(row["P"]) < 0 or int(row["V"]) < 0:
                        borrowed_after_negative += 1
                    elif row["gamma6"] is not None:
                        if minima6_after_negative is None or int(row["gamma6"]) < int(minima6_after_negative["gamma6"]):
                            minima6_after_negative = compact(row)
                        if int(row["gamma6"]) < 0:
                            double_negative += 1

    # A cheap forward probe tests whether the originally observed bounds
    # k<=17, r<=46 persist when the dyadic scale j is enlarged.
    forward_negative_ranges = {}
    for j in range(31, 41):
        ks: list[int] = []
        rs: list[int] = []
        for k in range(2, 101):
            h = 112 * (1 << (j - 1))
            divisor = k - 1
            base = 2 * h - comb(k - 1, 2) - 2
            residue = (-base) % divisor
            for r in range(residue, 201, divisor):
                row = actual_state(j, k, r)
                if (row is not None and row.get("transition") == "-- -> ++"
                        and int(row.get("gamma5", 0)) < 0):
                    ks.append(k)
                    rs.append(r)
        forward_negative_ranges[str(j)] = {
            "count": len(ks),
            "k_range": [min(ks), max(ks)] if ks else None,
            "r_range": [min(rs), max(rs)] if rs else None,
        }

    print(json.dumps({
        "schema": "amra.erdos776.independent-c1-two-row-audit.v1",
        "domain": {
            "j": [2, 32], "k": [2, 3000],
            "low_r": [0, 3000],
            "wall_probes": "51 compatible points centered at each exact A=0 and B=0 wall",
            "parameter_probes": parameter_probes,
        },
        "target_rows": target_rows,
        "counts": counts,
        "minimum_gamma5": minima5,
        "minimum_sufficient_margin": minima_margin,
        "minimum_gamma6_after_negative_gamma5": minima6_after_negative,
        "gamma5_negative_rows": gamma5_negative,
        "gamma5_negative_k_range": [min(negative_k), max(negative_k)] if negative_k else None,
        "gamma5_negative_r_range": [min(negative_r), max(negative_r)] if negative_r else None,
        "gamma5_negative_with_rank6_borrow": borrowed_after_negative,
        "gamma5_gamma6_double_negative": double_negative,
        "unexpected_sources_reaching_target_pp": unexpected_target_sources,
        "forward_probe": {
            "domain": {"j": [31, 40], "k": [2, 100], "r": [0, 200]},
            "negative_ranges_by_j": forward_negative_ranges,
            "interpretation": "the earlier observed k<=17,r<=46 box is not stable as j grows",
        },
        "identity_checks": [
            "raw x0,y0 equal the independently normalized first tails",
            "full-orbit gamma5 equals the normalized gamma5 formula",
            "when P,V>=0, full-orbit gamma6 equals the normalized gamma6 formula",
            "all nonnegative normalized tails lie strictly below their next Macaulay caps",
        ],
        "finite_search_only": True,
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
