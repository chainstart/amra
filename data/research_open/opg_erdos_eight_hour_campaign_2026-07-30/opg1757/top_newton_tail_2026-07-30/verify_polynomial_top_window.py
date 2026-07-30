#!/usr/bin/env python3
"""Finite exact audit for the sharp near-diagonal 4-Stirling ratio."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction

from verify_growing_top_window import four_stirling_table


def ratio_majorant(n: int, depth: int, loss: int) -> Fraction:
    """A rational majorant slightly stronger than exp(6d^2/n)*(2d/n^2)^j."""

    # Use exp(x) >= 1+x to replace the transcendental factor by a
    # deliberately weaker rational certificate only for finite tests:
    # exp(6d^2/n) is evaluated separately in audit().
    return Fraction((2 * depth) ** loss, n ** (2 * loss))


def audit(maximum_n: int = 160) -> dict[str, object]:
    import math

    table = four_stirling_table(maximum_n)
    checks = 0
    maximum_normalized_ratio = 0.0
    rows = []
    for n in range(4, maximum_n + 1):
        local_checks = 0
        for depth in range(1, n // 4 + 1):
            denominator = table[n][n - depth]
            for loss in range(0, depth + 1):
                numerator = table[n - loss][n - depth]
                actual = Fraction(numerator, denominator)
                bound = float(ratio_majorant(n, depth, loss)) * math.exp(
                    6 * depth * depth / n
                )
                if float(actual) > bound * (1 + 1e-13):
                    raise AssertionError(
                        f"ratio failed at n={n}, d={depth}, j={loss}"
                    )
                if bound:
                    maximum_normalized_ratio = max(
                        maximum_normalized_ratio,
                        float(actual) / bound,
                    )
                checks += 1
                local_checks += 1
        rows.append({"n": n, "checks": local_checks})

    # Exact check of the intermediate combinatorial quotient (6), which
    # avoids floating point and is the actual proof input.
    intermediate_checks = 0
    for n in range(4, maximum_n + 1):
        for depth in range(1, n // 4 + 1):
            denominator = table[n][n - depth]
            falling_n = 1
            for offset in range(2 * depth):
                falling_n *= n - offset
            for loss in range(depth + 1):
                numerator = table[n - loss][n - depth]
                falling_depth = 1
                for offset in range(loss):
                    falling_depth *= depth - offset
                # T_num/T_den <= 2^j(d)_j(n-j+4)^(2(d-j))/(n)_(2d).
                left = numerator * falling_n
                right = (
                    denominator
                    * 2**loss
                    * falling_depth
                    * (n - loss + 4) ** (2 * (depth - loss))
                )
                if left > right:
                    raise AssertionError("intermediate graph/pair bound failed")
                intermediate_checks += 1

    return {
        "schema": "amra.opg1757.polynomial-top-window.v1",
        "scope": (
            "Exact finite checks of the pair lower bound / graph upper "
            "bound quotient and numerical stress tests of the final "
            "ratio. The all-parameter result is the human proof."
        ),
        "maximum_n": maximum_n,
        "ratio_checks": checks,
        "intermediate_exact_checks": intermediate_checks,
        "maximum_actual_over_bound": maximum_normalized_ratio,
        "rows": rows,
        "status": "finite_checks_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-n", type=int, default=160)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_n), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
