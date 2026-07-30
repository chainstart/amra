#!/usr/bin/env python3
"""Exact finite verifier for the ruled Cartesian distance subset."""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter


def divisor_count(value: int) -> int:
    if value < 1:
        raise ValueError("positive integer required")
    result = 1
    prime = 2
    remaining = value
    while prime * prime <= remaining:
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        result *= exponent + 1
        prime += 1
    if remaining > 1:
        result *= 2
    return result


def certificate(
    slopes: tuple[int, ...],
    radial: tuple[int, ...],
    heights: tuple[int, ...],
) -> dict[str, object]:
    if len(slopes) < 2 or not radial or not heights:
        raise ValueError("need two slopes and nonempty radial/height sets")
    base = min(slopes)
    differences = {slope - base for slope in slopes if slope != base}
    anchor = heights[0]
    height_differences = {height - anchor for height in heights}

    product_counts = Counter(
        a * difference for a in radial for difference in differences
    )
    products = set(product_counts)
    label_counts = Counter(
        product * product + difference * difference
        for product in products
        for difference in height_differences
    )
    labels = set(label_counts)

    realized = {
        (a - a) ** 2
        + (slope * a - base * a) ** 2
        + (height - anchor) ** 2
        for slope in slopes
        if slope != base
        for a in radial
        for height in heights
    }
    if labels != realized:
        raise AssertionError("distance subset realization failed")

    maximum_product_tau = max(divisor_count(abs(value)) for value in products)
    maximum_label_tau = max(divisor_count(value) for value in labels)
    theorem_floor = (
        (len(slopes) - 1) * len(radial) * len(heights)
    ) // (4 * maximum_product_tau * maximum_label_tau)
    if len(labels) < theorem_floor:
        raise AssertionError("theorem lower bound failed")

    return {
        "slopes": list(slopes),
        "radial": list(radial),
        "heights": list(heights),
        "input_triples": (
            (len(slopes) - 1) * len(radial) * len(heights)
        ),
        "distinct_products": len(products),
        "maximum_product_fibre": max(product_counts.values()),
        "distinct_labels": len(labels),
        "maximum_sum_of_squares_fibre": max(label_counts.values()),
        "maximum_product_tau": maximum_product_tau,
        "maximum_label_tau": maximum_label_tau,
        "theorem_integer_floor": theorem_floor,
    }


def audit(maximum_t: int = 9) -> dict[str, object]:
    generator = random.Random(1083)
    rows = []
    for t in range(2, maximum_t + 1):
        rows.append(
            certificate(
                tuple(range(1, t + 1)),
                tuple(range(1, t + 1)),
                tuple(range(0, t + 1)),
            )
        )
        slopes = tuple(
            sorted(generator.sample(range(-2 * t, 2 * t + 1), t))
        )
        radial = tuple(
            sorted(generator.sample(range(1, 3 * t + 1), t))
        )
        heights = tuple(
            sorted(generator.sample(range(-3 * t, 3 * t + 1), t))
        )
        rows.append(certificate(slopes, radial, heights))
    return {
        "schema": "amra.erdos1083.ruled-cartesian-escape.v1",
        "scope": (
            "Exact realization and two fibre ledgers for interval and "
            "random integer Cartesian grids. The asymptotic divisor "
            "bound is the human proof."
        ),
        "rows": rows,
        "status": "finite_checks_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-t", type=int, default=9)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_t), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
