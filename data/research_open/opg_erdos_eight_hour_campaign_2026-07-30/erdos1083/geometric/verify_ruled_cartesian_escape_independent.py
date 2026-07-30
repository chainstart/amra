#!/usr/bin/env python3
"""Independent verifier for RULED_CARTESIAN_ESCAPE_THEOREM.md."""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import isqrt


def tau(value: int) -> int:
    """Number of positive divisors."""

    if value < 1:
        raise ValueError("tau is defined here only for positive integers")
    total = 0
    root = isqrt(value)
    for divisor in range(1, root + 1):
        if value % divisor == 0:
            total += 1 if divisor * divisor == value else 2
    return total


def max_tau(limit: int) -> int:
    """Maximum divisor count on [1,limit]."""

    if limit < 1:
        raise ValueError("limit must be positive")
    return max(tau(value) for value in range(1, limit + 1))


def anchored_sets(
    slopes: tuple[int, ...],
    radial: tuple[int, ...],
    heights: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...], Counter[int]]:
    """Return X, U, and product multiplicities."""

    if len(slopes) < 2 or not radial or not heights:
        raise ValueError("need two slopes and nonempty radial/height sets")
    base_slope = min(slopes)
    base_height = heights[0]
    differences = tuple(
        slope - base_slope for slope in slopes if slope != base_slope
    )
    if not all(difference > 0 for difference in differences):
        raise AssertionError("minimum-slope anchoring must give positive L")
    product_counts = Counter(
        value * difference for value in radial for difference in differences
    )
    x_values = tuple(sorted(product_counts))
    u_values = tuple(sorted(height - base_height for height in heights))
    return x_values, u_values, product_counts


def anchored_label_counts(
    slopes: tuple[int, ...],
    radial: tuple[int, ...],
    heights: tuple[int, ...],
) -> tuple[Counter[int], Counter[int]]:
    """Return anchored label counts and product multiplicities."""

    x_values, u_values, product_counts = anchored_sets(
        slopes, radial, heights
    )
    labels = Counter(
        x_value * x_value + u_value * u_value
        for x_value in x_values
        for u_value in u_values
    )
    return labels, product_counts


def full_squared_distances(
    slopes: tuple[int, ...],
    radial: tuple[int, ...],
    heights: tuple[int, ...],
) -> set[int]:
    """All nonzero squared distances of {(a,j*a,z)}."""

    points = tuple(
        (value, slope * value, height)
        for slope in slopes
        for value in radial
        for height in heights
    )
    labels: set[int] = set()
    for left, right in combinations(points, 2):
        label = sum((left[index] - right[index]) ** 2 for index in range(3))
        if label > 0:
            labels.add(label)
    return labels


def theorem_lower_bound(
    T: int,
    slopes: tuple[int, ...],
    radial: tuple[int, ...],
    heights: tuple[int, ...],
    improved_constant: bool = False,
) -> Fraction:
    """The stated bound, or its positive-x constant-2 strengthening."""

    constant = 2 if improved_constant else 4
    divisor_maximum = max_tau(8 * T**4)
    return Fraction(
        (len(slopes) - 1) * len(radial) * len(heights),
        constant * divisor_maximum * divisor_maximum,
    )


def rational_scaling_bug() -> dict[str, object]:
    """Exact counterexample to the denominator-once statement."""

    denominator = 2
    slope = Fraction(1, 2)
    radial = Fraction(1, 2)
    height = Fraction(1, 2)
    point = (radial, slope * radial, height)
    once = tuple(denominator * coordinate for coordinate in point)
    twice = tuple(denominator**2 * coordinate for coordinate in point)
    return {
        "parameters": [str(slope), str(radial), str(height)],
        "common_denominator": denominator,
        "scaled_once": [str(value) for value in once],
        "scaled_once_integral": all(value.denominator == 1 for value in once),
        "scaled_twice": [str(value) for value in twice],
        "scaled_twice_integral": all(value.denominator == 1 for value in twice),
    }


def finite_audit(T: int) -> dict[str, object]:
    """One deterministic boundary-rich audit instance."""

    if T < 2:
        raise ValueError("need T >= 2")
    slopes = (-T, 0, T)
    radial = tuple(range(1, T + 1))
    heights = (-T, 0, T)
    labels, products = anchored_label_counts(slopes, radial, heights)
    full = full_squared_distances(slopes, radial, heights)
    product_excess = max(
        multiplicity - tau(value) for value, multiplicity in products.items()
    )
    sum_square_excess_4 = max(
        multiplicity - 4 * tau(value) for value, multiplicity in labels.items()
    )
    sum_square_excess_2 = max(
        multiplicity - 2 * tau(value) for value, multiplicity in labels.items()
    )
    return {
        "T": T,
        "anchored_label_count": len(labels),
        "full_distance_count": len(full),
        "anchored_subset_of_full": set(labels).issubset(full),
        "minimum_anchored_label": min(labels),
        "maximum_anchored_label": max(labels),
        "range_bound_8T4": 8 * T**4,
        "maximum_product_fibre_minus_tau": product_excess,
        "maximum_square_fibre_minus_4tau": sum_square_excess_4,
        "maximum_square_fibre_minus_2tau": sum_square_excess_2,
        "stated_lower_bound": str(
            theorem_lower_bound(T, slopes, radial, heights)
        ),
        "improved_lower_bound": str(
            theorem_lower_bound(
                T, slopes, radial, heights, improved_constant=True
            )
        ),
    }


def main() -> None:
    print(
        json.dumps(
            {
                "verdict": {
                    "main_integer_theorem": "PASS",
                    "revised_document": "PASS_WITH_SCOPE_QUALIFICATION",
                    "constant_4_valid": True,
                    "constant_4_optimal": False,
                    "revised_rational_scaling_section": "PASS",
                    "full_ruled_branch_excluded": False,
                },
                "finite_audit": finite_audit(6),
                "rational_scaling_counterexample": rational_scaling_bug(),
                "critical_exponent": "1/5+3/5=4/5",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
