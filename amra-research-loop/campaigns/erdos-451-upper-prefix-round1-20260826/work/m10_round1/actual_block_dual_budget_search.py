#!/usr/bin/env python3
"""Exact small-coefficient dual search on selected actual 451 blocks.

The coefficient vectors are centered automatically because max_coeff < k.
For each L1 budget the script records the smallest exact numerator
A=sum_i z_i(P/p_i), then evaluates the density-scale affine support ledger.
Finite output is falsification evidence only.
"""

from __future__ import annotations

import argparse
import bisect
import itertools
import json
import math
from fractions import Fraction


SYSTEMS = (
    {"k": 168, "scale": 16, "offsets": (23, 25, 29, 31), "default_m": 16},
    {"k": 58, "scale": 32, "offsets": (39, 43, 45, 49, 51, 55), "default_m": 5},
    {"k": 116, "scale": 32, "offsets": (33, 35, 41, 47, 51, 57, 63), "default_m": 4},
    {
        "k": 176,
        "scale": 64,
        "offsets": (65, 75, 81, 87, 93, 95, 101, 105, 107, 117),
        "default_m": 2,
    },
)


def moment_order(vector: tuple[int, ...], offsets: tuple[int, ...]) -> int:
    for degree in range(len(offsets)):
        if sum(z * d**degree for z, d in zip(vector, offsets)) != 0:
            return degree
    raise AssertionError("a nonzero vector cannot annihilate q moments")


def exact_minima_bruteforce(
    cofactors: tuple[int, ...], max_coeff: int
) -> tuple[dict[int, tuple[int, tuple[int, ...]]], int]:
    q = len(cofactors)
    best_by_l1: dict[int, tuple[int, tuple[int, ...]]] = {}
    total = 0
    for vector in itertools.product(range(-max_coeff, max_coeff + 1), repeat=q):
        if not any(vector):
            continue
        total += 1
        l1 = sum(abs(z) for z in vector)
        numerator = sum(z * cofactor for z, cofactor in zip(vector, cofactors))
        if numerator == 0:
            raise AssertionError("a centered nonzero vector gave zero reciprocal sum")
        candidate = (abs(numerator), vector)
        if l1 not in best_by_l1 or candidate < best_by_l1[l1]:
            best_by_l1[l1] = candidate
    return best_by_l1, total


def half_buckets(
    cofactors: tuple[int, ...], max_coeff: int
) -> dict[int, list[tuple[int, tuple[int, ...]]]]:
    buckets: dict[int, list[tuple[int, tuple[int, ...]]]] = {}
    for vector in itertools.product(range(-max_coeff, max_coeff + 1), repeat=len(cofactors)):
        l1 = sum(abs(z) for z in vector)
        numerator = sum(z * cofactor for z, cofactor in zip(vector, cofactors))
        buckets.setdefault(l1, []).append((numerator, vector))
    for bucket in buckets.values():
        bucket.sort()
    return buckets


def exact_minima_mitm(
    cofactors: tuple[int, ...], max_coeff: int
) -> tuple[dict[int, tuple[int, tuple[int, ...]]], int]:
    split = len(cofactors) // 2
    left = half_buckets(cofactors[:split], max_coeff)
    right = half_buckets(cofactors[split:], max_coeff)
    right_sums = {l1: [entry[0] for entry in bucket] for l1, bucket in right.items()}
    best_by_l1: dict[int, tuple[int, tuple[int, ...]]] = {}
    for left_l1, left_bucket in left.items():
        for right_l1, right_bucket in right.items():
            total_l1 = left_l1 + right_l1
            if total_l1 == 0:
                continue
            sums = right_sums[right_l1]
            incumbent = best_by_l1.get(total_l1)
            for left_sum, left_vector in left_bucket:
                position = bisect.bisect_left(sums, -left_sum)
                for index in (position - 1, position):
                    if not 0 <= index < len(right_bucket):
                        continue
                    right_sum, right_vector = right_bucket[index]
                    numerator = left_sum + right_sum
                    if numerator == 0:
                        raise AssertionError(
                            "a centered nonzero vector gave zero reciprocal sum"
                        )
                    vector = left_vector + right_vector
                    candidate = (abs(numerator), vector)
                    if incumbent is None or candidate < incumbent:
                        incumbent = candidate
            if incumbent is not None:
                best_by_l1[total_l1] = incumbent
    total = (2 * max_coeff + 1) ** len(cofactors) - 1
    return best_by_l1, total


def search(
    system: dict[str, object], max_coeff_override: int | None, use_mitm: bool
) -> dict[str, object]:
    k = int(system["k"])
    scale = int(system["scale"])
    offsets = tuple(int(d) for d in system["offsets"])
    primes = tuple(k + d for d in offsets)
    q = len(primes)
    max_coeff = int(max_coeff_override or system["default_m"])
    if max_coeff >= k:
        raise ValueError("the centered-representative certificate requires max_coeff < k")

    period = math.prod(primes)
    cofactors = tuple(period // p for p in primes)
    width_product = math.prod(offsets)
    half_width = math.floor((scale - 1) / 2) + Fraction(1, 2)
    h_multiplier = k * k * 6**q  # h/P = k^2 6^q / product(d_i)

    if use_mitm:
        best_by_l1, total = exact_minima_mitm(cofactors, max_coeff)
    else:
        best_by_l1, total = exact_minima_bruteforce(cofactors, max_coeff)

    # Prefix minima answer the coefficient-budget question.
    rows = []
    incumbent: tuple[int, tuple[int, ...]] | None = None
    for budget in range(1, max(best_by_l1) + 1):
        if budget in best_by_l1 and (
            incumbent is None or best_by_l1[budget] < incumbent
        ):
            incumbent = best_by_l1[budget]
        if incumbent is None:
            continue
        abs_a, vector = incumbent
        l1 = sum(abs(z) for z in vector)
        support = sum(z != 0 for z in vector)
        h_phase = Fraction(h_multiplier * abs_a, width_product)
        transverse = sum(half_width * abs(z) / p for z, p in zip(vector, primes))
        rows.append(
            {
                "budget": budget,
                "attained_l1": l1,
                "vector": vector,
                "support": support,
                "first_nonzero_moment": moment_order(vector, offsets),
                "abs_A": abs_a,
                "minus_log_phase": -math.log(abs_a / period),
                "h_phase_float": float(h_phase),
                "transverse_float": float(transverse),
                "R_over_q": float((h_phase + transverse) / q),
                "alternative_q_score": float(max(h_phase / q, transverse / q)),
                "alternative_support_score": float(
                    max(h_phase / support, transverse / support)
                ),
            }
        )

    best_r = min(rows, key=lambda row: row["R_over_q"])
    best_alt_q = min(rows, key=lambda row: row["alternative_q_score"])
    best_alt_support = min(rows, key=lambda row: row["alternative_support_score"])
    return {
        "k": k,
        "scale": scale,
        "offsets": offsets,
        "primes": primes,
        "rank": q,
        "max_coeff": max_coeff,
        "algorithm": "exact_mitm" if use_mitm else "exact_bruteforce",
        "coefficient_vectors_covered": total,
        "target_h": "k^2 * 6^q * density^(-1)",
        "best_R_over_q": best_r,
        "best_alternative_q": best_alt_q,
        "best_alternative_support": best_alt_support,
        "budget_frontier": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", type=int, choices=range(len(SYSTEMS)))
    parser.add_argument("--max-coeff", type=int)
    parser.add_argument("--mitm", action="store_true")
    args = parser.parse_args()
    systems = SYSTEMS if args.system is None else (SYSTEMS[args.system],)
    payload = {
        "scope": "finite exact falsification only",
        "support_ledger": "h=k^2*6^q/density; exact centered coefficient box",
        "systems": [search(system, args.max_coeff, args.mitm) for system in systems],
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
