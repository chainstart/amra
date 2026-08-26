#!/usr/bin/env python3
"""Exact rank-three audit for the canonical affine Erdos-451 block."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for divisor in range(2, math.isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True


def correlation_range(k: int, absorber: int, moduli: tuple[int, ...]) -> int:
    period = math.prod(moduli)
    prefix = 0
    minimum = 0
    maximum = 0
    for t in range(period):
        value = 1
        for p in moduli:
            b = p - k
            residue = (absorber * t - (k + 1)) % p
            value *= k if residue < b else -b
        prefix += value
        minimum = min(minimum, prefix)
        maximum = max(maximum, prefix)
    assert prefix == 0
    return maximum - minimum


def exact_rank_three_identities(
    k: int, A: int, moduli: tuple[int, int, int]
) -> dict[str, object]:
    absorber = math.comb(k + A, A)
    period = math.prod(moduli)
    offsets = tuple(p - k for p in moduli)
    local_rows = []
    inverse_sum = Fraction(0)
    carry_sum = Fraction(0)

    for index, (p, b) in enumerate(zip(moduli, offsets, strict=True)):
        derivative = math.prod(
            b - other for other_index, other in enumerate(offsets) if other_index != index
        )
        binomial = (-1) ** A * math.comb(b - 1, A)
        combined = binomial * derivative
        assert combined % p == absorber * (period // p) % p
        inverse = pow(combined, -1, p)
        carry = (combined * inverse - 1) // p
        inverse_sum += Fraction(1, p * combined)
        carry_sum += Fraction(carry, combined)
        local_rows.append(
            {
                "p": p,
                "b": b,
                "F_prime_at_b": derivative,
                "R_A_at_b": binomial,
                "combined_integer": combined,
                "least_positive_inverse": inverse,
                "modular_carry": carry,
            }
        )

    root_sum = sum(
        (
            Fraction(
                (-1) ** a * a * math.comb(A, a),
                k + a,
            )
            / math.prod(b - a for b in offsets)
        )
        for a in range(1, A + 1)
    )
    expected_inverse_sum = Fraction(1, absorber * period) + root_sum
    assert inverse_sum == expected_inverse_sum

    crt_numerator = sum(
        row["least_positive_inverse"] * (period // row["p"])
        for row in local_rows
    )
    assert (absorber * crt_numerator - 1) % period == 0
    global_carry = (absorber * crt_numerator - 1) // period
    assert carry_sum + root_sum == Fraction(global_carry, absorber)

    assert sum(Fraction(1, row["F_prime_at_b"]) for row in local_rows) == 0
    assert sum(
        Fraction(row["b"], row["F_prime_at_b"]) for row in local_rows
    ) == 0
    assert sum(
        Fraction(row["b"] ** 2, row["F_prime_at_b"]) for row in local_rows
    ) == 1

    return {
        "local_rows": local_rows,
        "partial_fraction_root_sum": str(root_sum),
        "inverse_rational_sum": str(inverse_sum),
        "global_crt_carry": global_carry,
        "global_carry_over_absorber": str(Fraction(global_carry, absorber)),
    }


def audit_system(k: int, A: int, moduli: tuple[int, int, int]) -> dict[str, object]:
    absorber = math.comb(k + A, A)
    triple = correlation_range(k, absorber, moduli)
    pair_ranges = {
        f"{p},{q}": correlation_range(k, absorber, (p, q))
        for p, q in itertools.combinations(moduli, 2)
    }
    maximum_pair = max(pair_ranges.values())
    minimum_pair = min(pair_ranges.values())
    return {
        "k": k,
        "A": A,
        "Q": absorber,
        "moduli": list(moduli),
        "offsets": [p - k for p in moduli],
        "period": math.prod(moduli),
        "scaled_rank_three_interval_correlation": triple,
        "scaled_pair_interval_correlations": pair_ranges,
        "ratio_to_k_times_maximum_pair": triple / (k * maximum_pair),
        "ratio_to_k_times_minimum_pair": triple / (k * minimum_pair),
        "ratio_to_k_to_5": triple / k**5,
        "exact_identities": exact_rank_three_identities(k, A, moduli),
    }


def exhaustive(max_k: int, max_period: int) -> dict[str, object]:
    tested = 0
    best_max_pair = None
    best_min_pair = None
    best_k5 = None
    for k in range(8, max_k + 1):
        A = max(1, int(k / math.log(k) ** 2))
        primes = [p for p in range(k + A + 1, 2 * k) if is_prime(p)]
        for moduli in itertools.combinations(primes, 3):
            if math.prod(moduli) > max_period:
                continue
            tested += 1
            row = audit_system(k, A, moduli)
            if (
                best_max_pair is None
                or row["ratio_to_k_times_maximum_pair"]
                > best_max_pair["ratio_to_k_times_maximum_pair"]
            ):
                best_max_pair = row
            if (
                best_min_pair is None
                or row["ratio_to_k_times_minimum_pair"]
                > best_min_pair["ratio_to_k_times_minimum_pair"]
            ):
                best_min_pair = row
            if best_k5 is None or row["ratio_to_k_to_5"] > best_k5["ratio_to_k_to_5"]:
                best_k5 = row
    assert best_max_pair is not None and best_min_pair is not None and best_k5 is not None
    return {
        "tested_systems": tested,
        "maximum_period": max_period,
        "largest_ratio_to_k_times_maximum_pair": best_max_pair,
        "largest_ratio_to_k_times_minimum_pair": best_min_pair,
        "largest_ratio_to_k_to_5": best_k5,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=34)
    parser.add_argument("--max-period", type=int, default=1_000_000)
    args = parser.parse_args()
    print(
        json.dumps(
            {
                "schema_version": "erdos451.affine_rank3_tensor_audit.v1",
                "exhaustive": exhaustive(args.max_k, args.max_period),
                "boundary": (
                    "Exact finite-period arithmetic and rational identities only. "
                    "A finite ratio can kill a stated constant-one tensor inequality but "
                    "cannot prove or disprove a uniform polynomial block theorem."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
