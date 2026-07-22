#!/usr/bin/env python3
"""Exact finite audit for the simplex-slab positive-part difference formula."""

from __future__ import annotations

import itertools
import json
import math


def weak_compositions(total: int, dimension: int):
    if dimension == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, dimension - 1):
            yield (first,) + tail


def slab(dimension: int, lower: int, width: int):
    return {
        point
        for total in range(lower, lower + width)
        for point in weak_compositions(total, dimension)
    }


def positive_part_difference(points):
    return {
        tuple(max(xi - yi, 0) for xi, yi in zip(x, y))
        for x in points
        for y in points
    }


def expected_size(dimension: int, lower: int, width: int) -> int:
    return math.comb(lower + width - 1 + dimension, dimension) - math.comb(
        lower + dimension - 1, dimension
    )


def expected_difference_size(dimension: int, lower: int, width: int) -> int:
    top = lower + width - 1
    # Boundary of the large simplex, plus the small full-support simplex.
    return (
        math.comb(top + dimension, dimension)
        - math.comb(top, dimension)
        + math.comb(width - 1, dimension)
    )


def expected_difference_set(dimension: int, lower: int, width: int):
    top = lower + width - 1
    answer = set()
    for total in range(top + 1):
        for point in weak_compositions(total, dimension):
            if 0 in point:
                answer.add(point)
            elif total <= width - 1:
                answer.add(point)
    return answer


def main() -> None:
    rows = []
    for dimension, lower, width in itertools.product(range(2, 5), range(1, 6), range(1, 5)):
        points = slab(dimension, lower, width)
        actual_d = positive_part_difference(points)
        formula_d = expected_difference_set(dimension, lower, width)
        row = {
            "dimension": dimension,
            "lower": lower,
            "width": width,
            "slab_size": len(points),
            "positive_difference_size": len(actual_d),
            "expected_slab_size": expected_size(dimension, lower, width),
            "expected_positive_difference_size": expected_difference_size(
                dimension, lower, width
            ),
            "sets_equal": actual_d == formula_d,
            "uniform_two_thirds_bound": (
                8 * len(actual_d) ** 3 >= 27 * len(points) ** 2
                if width <= lower
                else None
            ),
        }
        assert row["slab_size"] == row["expected_slab_size"]
        assert (
            row["positive_difference_size"]
            == row["expected_positive_difference_size"]
        )
        assert row["sets_equal"]
        if width <= lower:
            assert row["uniform_two_thirds_bound"]
        rows.append(row)
    formula_scan_instances = 0
    for dimension in range(2, 21):
        for lower in range(1, 101):
            for width in range(1, lower + 1):
                size = expected_size(dimension, lower, width)
                difference_size = expected_difference_size(dimension, lower, width)
                assert 8 * difference_size ** 3 >= 27 * size ** 2
                formula_scan_instances += 1
    print(
        json.dumps(
            {
                "status": "PASS",
                "scope": "60 small exact instances; asymptotic proof is in attempt.md",
                "instances": len(rows),
                "uniform_bound_formula_scan": {
                    "dimension_range": [2, 20],
                    "lower_range": [1, 100],
                    "condition": "1 <= width <= lower",
                    "instances": formula_scan_instances,
                    "failures": 0,
                },
                "rows": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
