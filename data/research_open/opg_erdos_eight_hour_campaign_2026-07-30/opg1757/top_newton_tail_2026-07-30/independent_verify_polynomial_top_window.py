#!/usr/bin/env python3
"""Independent finite audit for the polynomial top-window theorem.

This module implements the 4-Stirling recurrence locally.  It imports
no existing OPG verifier and records both the failure in the printed
constant ledger and the corrected j-sensitive exponent certificate.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction


def four_stirling_table(maximum_n: int) -> list[list[int]]:
    """Return coefficients {n \\brace q}_4 for 0 <= n <= maximum_n."""
    rows = [[1]]
    for power in range(1, maximum_n + 1):
        previous = rows[-1]
        row = [0] * (power + 1)
        for falling_degree in range(power + 1):
            row[falling_degree] = (
                (falling_degree + 4)
                * (
                    previous[falling_degree]
                    if falling_degree < len(previous)
                    else 0
                )
                + (
                    previous[falling_degree - 1]
                    if falling_degree
                    else 0
                )
            )
        rows.append(row)
    return rows


def falling(value: int, degree: int) -> int:
    result = 1
    for offset in range(degree):
        result *= value - offset
    return result


def matching_lower(n: int, depth: int) -> Fraction:
    return Fraction(
        falling(n, 2 * depth),
        2**depth * math.factorial(depth),
    )


def star_graph_upper(n: int, depth: int) -> int:
    return math.comb(math.comb(n + 4, 2), depth)


def coarse_exponent_failure(maximum_depth: int = 32) -> list[dict[str, int]]:
    """Counterexamples to 4d^2+8d <= 6d^2 in the claimed d>=2 range."""
    return [
        {
            "d": depth,
            "printed_left_coefficient": 4 * depth**2 + 8 * depth,
            "target_coefficient": 6 * depth**2,
        }
        for depth in range(2, maximum_depth + 1)
        if 4 * depth**2 + 8 * depth > 6 * depth**2
    ]


def corrected_exponent_certificate(
    maximum_depth: int = 256,
) -> int:
    """Check 4d^2+2(d-j)(4-j)_+ <= 6d^2 for every j>=1."""
    checks = 0
    for depth in range(1, maximum_depth + 1):
        for loss in range(1, depth + 1):
            numerator_cost = (
                2 * (depth - loss) * max(4 - loss, 0)
            )
            assert 4 * depth**2 + numerator_cost <= 6 * depth**2
            checks += 1
    return checks


def log_integer(value: int) -> float:
    """Stable natural logarithm for arbitrarily large positive integers."""
    if value <= 0:
        raise ValueError(value)
    shift = max(0, value.bit_length() - 53)
    return math.log(value >> shift) + shift * math.log(2)


def audit(maximum_n: int = 160) -> dict[str, object]:
    table = four_stirling_table(maximum_n)
    pair_checks = 0
    star_checks = 0
    intermediate_checks = 0
    final_ratio_checks = 0
    maximum_log_slack = -math.inf

    for n in range(4, maximum_n + 1):
        for depth in range(1, n // 4 + 1):
            denominator = table[n][n - depth]

            lower = matching_lower(n, depth)
            assert Fraction(denominator) >= lower
            pair_checks += 1

            falling_n = falling(n, 2 * depth)
            for loss in range(depth + 1):
                reduced_n = n - loss
                reduced_depth = depth - loss
                numerator = table[reduced_n][reduced_n - reduced_depth]

                graph_upper = star_graph_upper(
                    reduced_n,
                    reduced_depth,
                )
                assert numerator <= graph_upper
                star_checks += 1

                falling_depth = falling(depth, loss)
                intermediate_right = (
                    denominator
                    * 2**loss
                    * falling_depth
                    * (n - loss + 4) ** (2 * reduced_depth)
                )
                assert numerator * falling_n <= intermediate_right
                intermediate_checks += 1

                log_actual = (
                    log_integer(numerator)
                    - log_integer(denominator)
                )
                log_bound = (
                    Fraction(6 * depth**2, n)
                    + loss
                    * (
                        math.log(2 * depth)
                        - 2 * math.log(n)
                    )
                )
                assert log_actual <= float(log_bound) + 2e-12
                maximum_log_slack = max(
                    maximum_log_slack,
                    log_actual - float(log_bound),
                )
                final_ratio_checks += 1

    failed_coarse_cases = coarse_exponent_failure()
    assert [record["d"] for record in failed_coarse_cases] == [2, 3]
    corrected_checks = corrected_exponent_certificate()

    # A canonical absolute choice once A is fixed:
    # eta=1/(2(A+1)).  It has both required positive margins.
    eta_records = []
    for coefficient_constant in range(1, 33):
        eta = Fraction(1, 2 * (coefficient_constant + 1))
        square_margin = 1 - 2 * eta
        geometric_margin = (
            1 - eta * (coefficient_constant + 1)
        )
        assert square_margin > 0
        assert geometric_margin == Fraction(1, 2)
        eta_records.append(
            {
                "A": coefficient_constant,
                "eta": str(eta),
                "1_minus_2eta": str(square_margin),
                "1_minus_eta_A_plus_1": str(
                    geometric_margin
                ),
            }
        )

    return {
        "schema": "amra.opg1757.independent-polynomial-top-window.v1",
        "imports_existing_opg_verifier": False,
        "maximum_n": maximum_n,
        "pair_lower_checks": pair_checks,
        "star_graph_upper_checks": star_checks,
        "intermediate_ratio_checks": intermediate_checks,
        "final_ratio_checks": final_ratio_checks,
        "maximum_log_actual_minus_bound": maximum_log_slack,
        "printed_coarse_exponent_counterexamples": failed_coarse_cases,
        "corrected_exponent_checks": corrected_checks,
        "eta_records": eta_records,
        "historical_coarse_step_verdict": "FAIL",
        "current_revision_verdict": "PASS",
        "mathematical_verdict_after_local_repair": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-n", type=int, default=160)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_n), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
