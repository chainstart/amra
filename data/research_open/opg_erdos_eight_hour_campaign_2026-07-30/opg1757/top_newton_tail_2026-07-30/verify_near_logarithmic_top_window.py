#!/usr/bin/env python3
"""Finite exact checks for the near-logarithmic top-window refinement."""

from __future__ import annotations

import argparse
import json
import math

from verify_growing_top_window import four_stirling_table


def integer_partition_tuples(total: int, maximum: int | None = None):
    if total == 0:
        yield ()
        return
    maximum = total if maximum is None else min(maximum, total)
    for first in range(maximum, 0, -1):
        for rest in integer_partition_tuples(total - first, first):
            yield (first,) + rest


def audit(maximum_loss: int = 64, maximum_n: int = 96) -> dict[str, object]:
    partition_checks = 0
    largest_partition_ratio = 0.0
    partition_counts: dict[str, int] = {}
    for loss in range(1, maximum_loss + 1):
        partitions = list(integer_partition_tuples(loss))
        partition_counts[str(loss)] = len(partitions)
        for partition in partitions:
            cost = sum(
                (part + 1) * math.log(part + 2)
                for part in partition
            )
            ceiling = 2 * loss * math.log(loss + 2)
            if cost > ceiling + 1e-12:
                raise AssertionError("additive partition-cost bound failed")
            largest_partition_ratio = max(
                largest_partition_ratio, cost / ceiling
            )
            partition_checks += 1

    table = four_stirling_table(maximum_n)
    ratio_checks = 0
    for n in range(4, maximum_n + 1):
        for depth in range(1, n // 4 + 1):
            denominator = table[n][n - depth]
            for loss in range(1, depth + 1):
                numerator = table[n - loss][n - depth]
                # In the theorem m=2k-4, hence k=(n+4)/2.
                # Clear the harmless half-integrality by using rationals
                # represented as an integer cross multiplication.
                k_twice = n + 4
                left = numerator * k_twice ** (2 * loss)
                right = (
                    denominator
                    * 16**depth
                    * math.prod(range(depth - loss + 1, depth + 1))
                    * 2 ** (2 * loss)
                )
                if left > right:
                    raise AssertionError("4-Stirling ratio bound failed")
                ratio_checks += 1

    # Exact integer examples inside the new window and outside the old
    # clean d=(log k)^(1/3) corollary.
    scale_rows = []
    for exponent in (64, 128, 256, 512, 1024):
        log_k = 2**exponent
        log_log_k = exponent * math.log(2)
        divisor = max(1, math.ceil(log_log_k**2))
        new_depth = max(1, log_k // divisor)
        old_depth = max(1, int(2 ** (exponent / 3)))
        if new_depth <= old_depth:
            raise AssertionError("new sample window did not improve old one")
        # new_depth/log_k <= 1/divisor, avoiding a lossy conversion of
        # the enormous integer log_k to binary floating point.
        normalized_cost_upper = math.log(new_depth + 5) / divisor
        scale_rows.append(
            {
                "log_k": log_k,
                "old_clean_depth": old_depth,
                "new_clean_depth": new_depth,
                "d_log_d_over_log_k_upper": normalized_cost_upper,
            }
        )

    return {
        "schema": "amra.opg1757.near-logarithmic-top-window.v1",
        "scope": (
            "Finite stress test of the additive partition ledger, "
            "the downstream 4-Stirling ratio, and the explicit clean "
            "window. The uniform coefficient-norm bound is the human proof."
        ),
        "maximum_loss": maximum_loss,
        "partition_checks": partition_checks,
        "partition_counts": partition_counts,
        "largest_partition_ratio": largest_partition_ratio,
        "maximum_stirling_n": maximum_n,
        "stirling_ratio_checks": ratio_checks,
        "scale_rows": scale_rows,
        "status": "finite_checks_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-loss", type=int, default=64)
    parser.add_argument("--maximum-n", type=int, default=96)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_loss, args.maximum_n),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
