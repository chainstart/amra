#!/usr/bin/env python3
"""Exact guards for round 2 of the P776 rank-14 bridge.

Selected actual parameters are identity/falsifier checks only.  The synthetic
pair is an algebraic all-parameter counterfamily to a *local implication*;
it is not claimed to be the actual zero-seed orbit.
"""

from __future__ import annotations

from hashlib import sha256
from math import comb
from pathlib import Path
import json


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    answer: list[tuple[int, int]] = []
    remainder = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        hi = cap if cap is not None else max(lower + 1, 2 * lower)
        if cap is None:
            while comb(hi, lower) <= remainder:
                hi *= 2
        while lo + 1 < hi:
            middle = (lo + hi) // 2
            if comb(middle, lower) <= remainder:
                lo = middle
            else:
                hi = middle
        upper = lo if cap is None else min(lo, cap - 1)
        while upper >= lower and comb(upper, lower) > remainder:
            upper -= 1
        if upper >= lower:
            answer.append((upper, lower))
            remainder -= comb(upper, lower)
            cap = upper
    if remainder:
        raise AssertionError((number, rank, remainder, answer))
    return answer


def kk(number: int, rank: int) -> int:
    return sum(comb(upper, lower - 1) for upper, lower in canonical(number, rank))


def zero_seed_orbit(parameter: int, offset: int, target: int) -> dict[int, int]:
    rank = parameter - offset
    value = 0
    rows = {rank: value}
    while rank > target:
        value = parameter + kk(value, rank)
        rank -= 1
        rows[rank] = value
    return rows


def actual_fixed_rank_identities(parameter: int) -> dict[str, object]:
    v = parameter
    n = v - 25
    d = zero_seed_orbit(v, 12, 16)
    e = zero_seed_orbit(v, 26, 3)
    differences: dict[int, int] = {}
    for small_rank in (5, 4, 3):
        d_rank = small_rank + 13
        p = comb(v - 12, d_rank) + comb(v - 13, d_rank - 1)
        left = d[d_rank] - p
        right = e[small_rank] - comb(n, small_rank)
        assert left == right
        differences[d_rank] = left

    j4 = comb(n - 1, 4) + comb(n - 2, 3)
    b2 = e[4] - j4
    capacity = comb(n - 2, 2)
    assert 0 <= b2 <= capacity
    w14 = d[16] - comb(v - 12, 16) - comb(v - 13, 15)
    assert w14 == 27 + kk(b2, 2)
    return {
        "V": v,
        "D_minus_P": differences,
        "B2": b2,
        "B2_capacity": capacity,
        "W14": w14,
        "W14_from_B2": 27 + kk(b2, 2),
    }


def rank2_galois_checks() -> dict[str, int]:
    cases = 0
    for x in range(0, 501):
        threshold = comb(kk(x, 2) + 1, 2)
        for y in range(0, 501):
            assert (kk(y, 2) <= kk(x, 2) + 1) == (y <= threshold)
            cases += 1
    return {"checked_cases": cases}


def synthetic_local_counterfamily(parameter: int) -> dict[str, int]:
    """A full-V local pair satisfying capacity but with W14 jump two."""

    v = parameter
    if v < 125:
        raise ValueError(v)
    b_v = comb(v - 30, 2)
    b_next = comb(v - 28, 2)
    cap_v = comb(v - 27, 2)
    cap_next = comb(v - 26, 2)
    assert 0 <= b_v <= cap_v
    assert 0 <= b_next <= cap_next
    w_v = 27 + kk(b_v, 2)
    w_next = 27 + kk(b_next, 2)
    assert w_v == v - 3
    assert w_next == v - 1
    assert 0 <= w_v <= v
    assert 0 <= w_next <= v + 1
    assert w_next - w_v == 2
    return {
        "V": v,
        "B2_V": b_v,
        "B2_Vplus1": b_next,
        "W14_V": w_v,
        "W14_Vplus1": w_next,
        "W14_jump": 2,
    }


def fixed_depth_constants() -> dict[int, int]:
    values = {14: 1}
    for rank in range(14, 6, -1):
        values[rank - 1] = 1 + rank * values[rank]
    assert values[6] == 130_455_928
    assert values[6] < comb(112, 5)
    return values


def main() -> None:
    actual = [actual_fixed_rank_identities(v) for v in (125, 288, 500)]
    payload = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "actual_identity_falsifiers": actual,
        "rank2_galois_checks": rank2_galois_checks(),
        "synthetic_all_parameter_formula_guards": [
            synthetic_local_counterfamily(v) for v in (125, 288, 1000)
        ],
        "fixed_depth_constants": fixed_depth_constants(),
        "scope": (
            "The canonical identities, rank-2 adjunction, fixed-depth implication, "
            "and symbolic synthetic formulas are exact. Selected actual V rows are "
            "identity/falsifier checks only and are not extrapolated."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
