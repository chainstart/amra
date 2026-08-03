#!/usr/bin/env python3
"""Exact guard for the minimal borrow-aware capacity-flow obstruction."""

from itertools import combinations
from math import comb
import json


def upper(number: int, rank: int) -> int:
    assert number >= 0
    remainder = number
    ceiling = None
    result = 0
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
            result += comb(lo, lower + 1)
            ceiling = lo
    assert remainder == 0
    return result


def relaxed_row(q: int, c: int, r: int, u: int) -> dict[str, int]:
    n = comb(q, 2) + r
    b = c * q + comb(c, 2) + u - r + 1
    h = (comb(b - 1, 2) + 2 - n) // 2
    z = comb(q, 3) + comb(r, 2)
    w = comb(q + c, 3) + comb(u, 2)
    cap = comb(b, 2) + 1
    x = n + z - cap + 1
    y = n + w - cap
    gamma4 = upper(y, 3) - upper(x, 3) - z - 1
    return {"q": q, "c": c, "r": r, "u": u, "n": n, "b": b, "h": h,
            "z": z, "w": w, "x": x, "y": y, "gamma4": gamma4}


def hall_deficiencies(neighbours: list[set[int]], capacities: list[int]):
    failures = []
    tokens = range(len(neighbours))
    for size in range(1, len(neighbours) + 1):
        for subset in combinations(tokens, size):
            union = set().union(*(neighbours[i] for i in subset))
            capacity = sum(capacities[j] for j in union)
            if capacity < len(subset):
                failures.append({"tokens": list(subset), "demand": len(subset),
                                 "neighbour_slots": sorted(union), "capacity": capacity})
    return failures


def main() -> None:
    row = relaxed_row(16, 2, 0, 3)
    assert row == {"q": 16, "c": 2, "r": 0, "u": 3, "n": 120, "b": 37,
                   "h": 256, "z": 560, "w": 819, "x": 14, "y": 272,
                   "gamma4": 69}
    capacities = [1, 1, 1]
    feasible = [{0}, {1}]
    deficient = [{0}, {0}]
    feasible_failures = hall_deficiencies(feasible, capacities)
    deficient_failures = hall_deficiencies(deficient, capacities)
    assert not feasible_failures
    assert deficient_failures == [{"tokens": [0, 1], "demand": 2,
                                    "neighbour_slots": [0], "capacity": 1}]
    assert sum(capacities) - len(feasible) == sum(capacities) - len(deficient) == 1
    print(json.dumps({
        "schema": "amra.erdos776.borrow-capacity-flow-guard.v1",
        "relaxed_positive_row": row,
        "aggregate_network_data": {"unit_demands": 2, "unit_slots": 3,
                                   "total_surplus": 1},
        "feasible_completion": {"neighbours": [[0], [1]], "hall_failures": []},
        "infeasible_completion": {"neighbours": [[0], [0]],
                                  "hall_failures": deficient_failures},
        "interpretation": "The same relaxed row and aggregate capacity admit both Hall outcomes; adjacency/accessibility data are not functions of gamma4.",
        "public_problem_refuted": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
