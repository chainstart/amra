#!/usr/bin/env python3
"""Exact finite guards for the Phi6 projection-height no-go."""

from itertools import product
from math import comb
import json


def union_support(d: int, k: int):
    # Supports of Q_A=(1+Y) product_(i in A) (1-X_i+X_i^2), |A|=k.
    for y_digit in range(2):
        for x_digits in product(range(3), repeat=d):
            if sum(digit != 0 for digit in x_digits) <= k:
                yield (y_digit,) + x_digits


def base_three_projection(point: tuple[int, ...]) -> int:
    # Y has weight 3^d; X_i have weights 3^i.  This separates the full box.
    d = len(point) - 1
    return point[0] * 3**d + sum(digit * 3**i for i, digit in enumerate(point[1:]))


def main() -> None:
    rows = []
    for d in range(2, 11):
        k = d // 2
        support = list(union_support(d, k))
        expected = 2 * sum(comb(d, s) * 2**s for s in range(k + 1))
        assert len(support) == expected == len(set(support))
        projected = [base_three_projection(point) for point in support]
        assert len(projected) == len(set(projected))
        # Any integer projection injective on this support has expected integer
        # values in an interval of length at most 2*L1(weight), hence this lower bound.
        l1_lower_bound = (expected - 1 + 1) // 2
        rows.append({
            "d": d,
            "k": k,
            "common_quotient_factor_count": d + 1,
            "equal_augmentation": 2,
            "number_of_divisor_rows": comb(d, k),
            "union_support": expected,
            "projection_l1_lower_bound": l1_lower_bound,
            "base_three_projection_injective": True,
        })
    print(json.dumps({
        "schema": "amra.erdos1083.projection-height-no-go-guard.v1",
        "rows": rows,
        "unbounded_claim_from_computation": False,
        "public_exponent_changed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
