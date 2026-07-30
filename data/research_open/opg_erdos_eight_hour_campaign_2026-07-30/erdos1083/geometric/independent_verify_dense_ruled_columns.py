#!/usr/bin/env python3
"""Independent red-team verifier for dense ruled-column stability.

This implementation imports no project verifier.  It rebuilds the radial
second moment, star decomposition, one-sided argument, signed-product
sharpening, two-square fibres, and actual Euclidean distance set directly.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction


def independent_divisor_count(value: int) -> int:
    if value < 1:
        raise ValueError("divisor count requires a positive integer")
    count = 0
    root = math.isqrt(value)
    for divisor in range(1, root + 1):
        if value % divisor == 0:
            count += 1 if divisor * divisor == value else 2
    return count


def brute_two_square_count(value: int) -> int:
    """Count ordered signed pairs (x,y) with x^2+y^2=value."""
    if value < 1:
        raise ValueError("two-square count requires a positive integer")
    count = 0
    radius = math.isqrt(value)
    for horizontal in range(-radius, radius + 1):
        vertical_square = value - horizontal * horizontal
        vertical = math.isqrt(vertical_square)
        if vertical * vertical == vertical_square:
            count += 1 if vertical == 0 else 2
    return count


def all_squared_distances(points):
    labels = set()
    for index, left in enumerate(points):
        for right in points[index + 1 :]:
            label = sum(
                (left[coordinate] - right[coordinate]) ** 2
                for coordinate in range(3)
            )
            if label:
                labels.add(label)
    return labels


def independent_dense_certificate(
    slopes,
    radial_parameters,
    occupied_columns,
    height_sets,
    height_length,
):
    slopes = tuple(sorted(set(slopes)))
    radial_parameters = tuple(sorted(set(radial_parameters)))
    occupied_columns = frozenset(occupied_columns)
    if len(slopes) < 2:
        raise ValueError("at least two slopes are required")
    if not radial_parameters or radial_parameters[0] <= 0:
        raise ValueError("radial parameters must be positive")
    if height_length < 1:
        raise ValueError("height_length must be positive")
    universe = frozenset(itertools.product(slopes, radial_parameters))
    if not occupied_columns <= universe:
        raise ValueError("occupied column outside declared universe")

    heights = {}
    for column in occupied_columns:
        if column not in height_sets:
            raise ValueError("missing occupied-column height set")
        values = tuple(sorted(set(height_sets[column])))
        if len(values) < height_length:
            raise ValueError("occupied column has too few distinct heights")
        if any(not isinstance(value, int) for value in values):
            raise ValueError("the theorem requires integer heights")
        heights[column] = values

    # Rebuild Psi by explicit ordered triples, independently of d_a(d_a-1).
    ordered_shared = []
    by_radial = defaultdict(set)
    for slope, radial in occupied_columns:
        by_radial[radial].add(slope)
    for radial in radial_parameters:
        for left in by_radial[radial]:
            for right in by_radial[radial]:
                if left != right:
                    ordered_shared.append((left, right, radial))
    psi = len(ordered_shared)
    degree_formula = sum(
        len(by_radial[radial]) * (len(by_radial[radial]) - 1)
        for radial in radial_parameters
    )
    assert psi == degree_formula

    stars = {
        base: [
            (other, radial)
            for left, other, radial in ordered_shared
            if left == base
        ]
        for base in slopes
    }
    assert sum(len(star) for star in stars.values()) == psi
    base = max(slopes, key=lambda value: len(stars[value]))
    star = stars[base]
    assert len(slopes) * len(star) >= psi

    left_side = [pair for pair in star if pair[0] < base]
    right_side = [pair for pair in star if pair[0] > base]
    retained_side = max((left_side, right_side), key=len)
    assert 2 * len(retained_side) >= len(star)

    # Reproduce the manuscript's positive one-sided product fibres.
    positive_products = defaultdict(list)
    for other, radial in retained_side:
        positive_products[radial * abs(other - base)].append(
            (other, radial)
        )

    # Sharpening: retain the full star and use signed nonzero products.
    signed_products = defaultdict(list)
    for other, radial in star:
        signed_products[radial * (other - base)].append((other, radial))

    slope_diameter = max(slopes) - min(slopes)
    maximum_radial = max(radial_parameters)
    maximum_product = maximum_radial * slope_diameter
    product_bound = max(
        independent_divisor_count(value)
        for value in range(1, maximum_product + 1)
    )
    for product, representations in positive_products.items():
        assert len(representations) <= independent_divisor_count(product)
    for product, representations in signed_products.items():
        assert len(representations) <= independent_divisor_count(abs(product))

    maximum_height = max(
        (
            abs(height)
            for column in occupied_columns
            for height in heights[column]
        ),
        default=0,
    )
    maximum_label = maximum_product**2 + (2 * maximum_height) ** 2
    two_square_bound = max(
        4 * independent_divisor_count(value)
        for value in range(1, maximum_label + 1)
    )

    def selected_inputs(product_fibres):
        inputs = set()
        for product, representations in product_fibres.items():
            other, radial = min(representations)
            anchor = heights[(base, radial)][-1]
            selected = heights[(other, radial)][:height_length]
            for height in selected:
                inputs.add((product, height - anchor))
        assert len(inputs) == len(product_fibres) * height_length
        return inputs

    positive_inputs = selected_inputs(positive_products)
    signed_inputs = selected_inputs(signed_products)
    positive_label_fibres = Counter(
        horizontal * horizontal + vertical * vertical
        for horizontal, vertical in positive_inputs
    )
    signed_label_fibres = Counter(
        horizontal * horizontal + vertical * vertical
        for horizontal, vertical in signed_inputs
    )

    for fibres in (positive_label_fibres, signed_label_fibres):
        for label, multiplicity in fibres.items():
            exact_r2 = brute_two_square_count(label)
            assert multiplicity <= exact_r2
            assert exact_r2 <= 4 * independent_divisor_count(label)
            assert multiplicity <= two_square_bound

    points = [
        (radial, slope * radial, height)
        for slope, radial in occupied_columns
        for height in heights[(slope, radial)]
    ]
    actual_labels = all_squared_distances(points)
    assert set(positive_label_fibres) <= actual_labels
    assert set(signed_label_fibres) <= actual_labels

    original_denominator = (
        2 * len(slopes) * product_bound * two_square_bound
    )
    sharpened_denominator = (
        len(slopes) * product_bound * two_square_bound
    )
    assert (
        len(actual_labels) * original_denominator
        >= height_length * psi
    )
    assert (
        len(actual_labels) * sharpened_denominator
        >= height_length * psi
    )

    edge_count = len(occupied_columns)
    radial_count = len(radial_parameters)
    moment_numerator = edge_count * edge_count - edge_count * radial_count
    assert psi * radial_count >= moment_numerator
    assert (
        len(actual_labels)
        * sharpened_denominator
        * radial_count
        >= height_length * moment_numerator
    )

    return {
        "slopes": len(slopes),
        "radial_parameters": radial_count,
        "occupied_columns": edge_count,
        "psi": psi,
        "star_sum": sum(len(star) for star in stars.values()),
        "base": base,
        "base_star": len(star),
        "left_star": len(left_side),
        "right_star": len(right_side),
        "retained_side": len(retained_side),
        "positive_products": len(positive_products),
        "signed_products": len(signed_products),
        "product_bound": product_bound,
        "two_square_bound": two_square_bound,
        "positive_selected_inputs": len(positive_inputs),
        "signed_selected_inputs": len(signed_inputs),
        "actual_distance_labels": len(actual_labels),
        "original_bound": str(
            Fraction(height_length * psi, original_denominator)
        ),
        "sharpened_bound": str(
            Fraction(height_length * psi, sharpened_denominator)
        ),
        "moment_bound_sharpened": str(
            Fraction(
                height_length * moment_numerator,
                sharpened_denominator * radial_count,
            )
        ),
    }


def critical_exponent_audit():
    """Exact exponent ledger; divisor maxima contribute only o(1)."""
    edge_exponent = Fraction(2)
    radial_class_upper_exponent = Fraction(1)
    slope_upper_exponent = Fraction(1)
    height_exponent = Fraction(2)
    radial_moment_exponent = (
        2 * edge_exponent - radial_class_upper_exponent
    )
    distance_exponent = (
        height_exponent
        + radial_moment_exponent
        - slope_upper_exponent
    )
    assert radial_moment_exponent == 3
    assert distance_exponent == 4
    return {
        "radial_second_moment_exponent": str(radial_moment_exponent),
        "distance_exponent": str(distance_exponent),
        "divisor_loss": "t^o(1) on fixed polynomial ranges",
    }


def common_denominator_scaling_audit(denominator, slope_numerators,
                                     radial_numerators, height_numerators):
    """Check the limited common-denominator extension.

    Parameters j, a, z lie in denominator^{-1} Z.  Scaling coordinates by
    denominator^2 gives integer coordinates
    (q*A, J*A, q*Z), preserving distance-label cardinality.
    """
    q = int(denominator)
    if q < 1:
        raise ValueError("denominator must be positive")
    slope_numerators = tuple(set(slope_numerators))
    radial_numerators = tuple(set(radial_numerators))
    height_numerators = tuple(set(height_numerators))
    if not slope_numerators or not radial_numerators or not height_numerators:
        raise ValueError("numerator sets must be nonempty")
    if min(radial_numerators) <= 0:
        raise ValueError("radial numerators must be positive")
    scaled = set()
    for slope in slope_numerators:
        for radial in radial_numerators:
            for height in height_numerators:
                scaled.add((q * radial, slope * radial, q * height))
    expected_size = (
        len(slope_numerators)
        * len(radial_numerators)
        * len(height_numerators)
    )
    assert len(scaled) == expected_size
    return {
        "denominator": q,
        "coordinate_scale": q * q,
        "squared_distance_scale": q**4,
        "scaled_points": len(scaled),
    }


def audit(exhaustive: bool = True):
    slopes = (-4, -1, 0, 3, 7)
    radial_parameters = (1, 2, 4, 7)
    occupied = {
        (slope, radial)
        for slope in slopes
        for radial in radial_parameters
        if (2 * slope + 3 * radial) % 5 != 1
    }
    heights = {
        column: tuple(
            sorted(
                {
                    5 * index * index
                    - 3 * index
                    + 2 * column[0]
                    - column[1]
                    for index in range(7)
                }
            )
        )
        for column in occupied
    }
    primary = independent_dense_certificate(
        slopes,
        radial_parameters,
        occupied,
        heights,
        7,
    )

    exhaustive_cases = 0
    if exhaustive:
        small_slopes = (-2, 0, 3)
        small_radials = (1, 3)
        universe = tuple(itertools.product(small_slopes, small_radials))
        for mask in range(1 << len(universe)):
            small_occupied = {
                column
                for index, column in enumerate(universe)
                if mask & (1 << index)
            }
            small_heights = {
                column: (
                    column[0] - 2 * column[1] - 5,
                    column[0] * column[1] + 1,
                    column[0] * column[1] + 8,
                )
                for column in small_occupied
            }
            independent_dense_certificate(
                small_slopes,
                small_radials,
                small_occupied,
                small_heights,
                3,
            )
            exhaustive_cases += 1

    return {
        "schema": "amra.erdos1083.dense-ruled-columns-independent.v1",
        "verdict": "PASS_WITH_SHARPENING",
        "scope": (
            "Independent finite red-team audit of the integer theorem. "
            "The original one-sided bound is valid; signed products remove "
            "its factor 2. The asymptotic common-denominator observation "
            "requires a single polynomially bounded denominator."
        ),
        "primary": primary,
        "exhaustive_occupancy_patterns": exhaustive_cases,
        "critical_exponents": critical_exponent_audit(),
        "common_denominator": common_denominator_scaling_audit(
            6,
            (-5, -1, 2, 7),
            (1, 5, 11),
            (-13, -2, 8),
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-exhaustive",
        action="store_true",
        help="run only the primary irregular instance",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            audit(exhaustive=not args.skip_exhaustive),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
