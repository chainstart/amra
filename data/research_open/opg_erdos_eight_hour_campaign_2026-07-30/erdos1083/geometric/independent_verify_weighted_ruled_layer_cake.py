#!/usr/bin/env python3
"""Independent red-team verifier for weighted ruled-column layer cake.

This file imports no AMRA verifier.  It reconstructs ordered weighted
overlap tokens, dyadic superlevels, signed multiplication fibres, anchored
height inputs, brute two-square fibres, and the full Euclidean distance set.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction


def trial_divisor_count(value: int) -> int:
    if value < 1:
        raise ValueError("divisor count requires a positive integer")
    count = 0
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor == 0:
            count += 1 if divisor * divisor == value else 2
    return count


def brute_r2(value: int) -> int:
    if value < 1:
        raise ValueError("r2 requires a positive integer")
    count = 0
    radius = math.isqrt(value)
    for horizontal in range(-radius, radius + 1):
        vertical_square = value - horizontal * horizontal
        vertical = math.isqrt(vertical_square)
        if vertical * vertical == vertical_square:
            count += 1 if vertical == 0 else 2
    return count


def full_distance_labels(points):
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


def independent_weighted_certificate(slopes, radii, raw_height_sets):
    slopes = tuple(sorted(set(slopes)))
    radii = tuple(sorted(set(radii)))
    if len(slopes) < 2:
        raise ValueError("at least two slopes are required")
    if not radii or min(radii) <= 0:
        raise ValueError("a nonempty set of positive radii is required")

    heights = {}
    for slope in slopes:
        for radius in radii:
            values = tuple(
                sorted(set(raw_height_sets.get((slope, radius), ())))
            )
            if any(not isinstance(value, int) for value in values):
                raise ValueError("all heights must be integers")
            heights[(slope, radius)] = values
    sizes = {column: len(values) for column, values in heights.items()}
    maximum_size = max(1, max(sizes.values()))

    # Expand min(h_j,a,h_k,a) into explicit ordered layer tokens.
    overlap_tokens = []
    for radius in radii:
        for left in slopes:
            for right in slopes:
                if left == right:
                    continue
                for rank in range(
                    min(sizes[(left, radius)], sizes[(right, radius)])
                ):
                    overlap_tokens.append((left, right, radius, rank))
    omega = len(overlap_tokens)
    direct_omega = sum(
        min(sizes[(left, radius)], sizes[(right, radius)])
        for radius in radii
        for left in slopes
        for right in slopes
        if left != right
    )
    assert omega == direct_omega
    if omega == 0:
        return {
            "Omega": 0,
            "status": "vacuous_zero_overlap",
        }

    stars = {
        base: [
            token
            for token in overlap_tokens
            if token[1] == base
        ]
        for base in slopes
    }
    assert sum(len(tokens) for tokens in stars.values()) == omega
    base = max(slopes, key=lambda slope: len(stars[slope]))
    star_weight = len(stars[base])
    assert len(slopes) * star_weight >= omega

    weighted_pairs = {}
    for other in slopes:
        if other == base:
            continue
        for radius in radii:
            weight = min(
                sizes[(other, radius)], sizes[(base, radius)]
            )
            if weight:
                weighted_pairs[(other, radius)] = weight
    assert sum(weighted_pairs.values()) == star_weight

    level_count = 1 + math.floor(math.log2(maximum_size))
    levels = tuple(2**power for power in range(level_count))
    for weight in weighted_pairs.values():
        exact_layer_sum = sum(
            threshold for threshold in levels if threshold <= weight
        )
        assert exact_layer_sum == (
            2 ** (1 + math.floor(math.log2(weight))) - 1
        )
        assert exact_layer_sum >= weight

    superlevels = {
        threshold: tuple(
            pair
            for pair, weight in weighted_pairs.items()
            if weight >= threshold
        )
        for threshold in levels
    }
    layer_sum = sum(
        threshold * len(pairs)
        for threshold, pairs in superlevels.items()
    )
    assert layer_sum >= star_weight
    threshold = max(
        levels,
        key=lambda value: value * len(superlevels[value]),
    )
    selected_pairs = superlevels[threshold]
    layer_product = threshold * len(selected_pairs)
    assert level_count * layer_product >= star_weight

    signed_products = defaultdict(list)
    for other, radius in selected_pairs:
        product = radius * (other - base)
        assert product
        signed_products[product].append((other, radius))
    for product, representations in signed_products.items():
        assert len(representations) <= trial_divisor_count(abs(product))

    slope_diameter = max(slopes) - min(slopes)
    maximum_radius = max(radii)
    maximum_product = maximum_radius * slope_diameter
    product_bound = max(
        trial_divisor_count(value)
        for value in range(1, maximum_product + 1)
    )
    assert all(
        len(representations) <= product_bound
        for representations in signed_products.values()
    )
    assert (
        len(signed_products) * product_bound >= len(selected_pairs)
    )

    selected_inputs = set()
    anchors = {}
    for product, representations in signed_products.items():
        other, radius = min(representations)
        base_heights = heights[(base, radius)]
        other_heights = heights[(other, radius)]
        assert len(base_heights) >= threshold
        assert len(other_heights) >= threshold
        # Use a nonmatching extreme anchor to stress that only one base
        # height, not an H-element pairing, is required.
        anchor = base_heights[-1]
        anchors[product] = anchor
        for height in other_heights[:threshold]:
            selected_inputs.add((product, height - anchor))
    assert len(selected_inputs) == threshold * len(signed_products)

    selected_label_fibres = Counter(
        horizontal * horizontal + vertical * vertical
        for horizontal, vertical in selected_inputs
    )
    assert selected_label_fibres
    for label, multiplicity in selected_label_fibres.items():
        exact_fibre = brute_r2(label)
        assert multiplicity <= exact_fibre
        assert exact_fibre <= 4 * trial_divisor_count(label)

    height_bound = max(
        abs(height)
        for values in heights.values()
        for height in values
    )
    maximum_label = maximum_product**2 + (2 * height_bound) ** 2
    two_square_bound = max(
        4 * trial_divisor_count(value)
        for value in range(1, maximum_label + 1)
    )
    assert max(selected_label_fibres) <= maximum_label
    assert all(
        multiplicity <= two_square_bound
        for multiplicity in selected_label_fibres.values()
    )

    points = [
        (radius, slope * radius, height)
        for slope in slopes
        for radius in radii
        for height in heights[(slope, radius)]
    ]
    actual_labels = full_distance_labels(points)
    assert set(selected_label_fibres) <= actual_labels

    denominator = (
        len(slopes)
        * level_count
        * product_bound
        * two_square_bound
    )
    assert len(actual_labels) * denominator >= omega

    return {
        "Omega": omega,
        "ordered_overlap_tokens": len(overlap_tokens),
        "star_sum": sum(len(tokens) for tokens in stars.values()),
        "base": base,
        "base_star_weight": star_weight,
        "U": maximum_size,
        "dyadic_levels": level_count,
        "layer_sum": layer_sum,
        "selected_H": threshold,
        "selected_pairs": len(selected_pairs),
        "layer_product": layer_product,
        "signed_negative_pairs": sum(
            other < base for other, _ in selected_pairs
        ),
        "signed_positive_pairs": sum(
            other > base for other, _ in selected_pairs
        ),
        "signed_products": len(signed_products),
        "product_bound": product_bound,
        "anchored_inputs": len(selected_inputs),
        "selected_distance_labels": len(selected_label_fibres),
        "actual_distance_labels": len(actual_labels),
        "two_square_bound": two_square_bound,
        "theorem_bound": str(Fraction(omega, denominator)),
        "constant_two_removed": True,
        "status": "nonvacuous_checks_passed",
    }


def exhaustive_height_size_audit():
    """Exhaust all 3^6 small fibre-size profiles."""
    slopes = (-2, 0, 3)
    radii = (1, 2)
    columns = tuple(itertools.product(slopes, radii))
    checked = 0
    nonvacuous = 0
    for size_profile in itertools.product(range(3), repeat=len(columns)):
        height_sets = {
            column: tuple(
                7 * index + 2 * column[0] - 3 * column[1]
                for index in range(size)
            )
            for column, size in zip(columns, size_profile)
        }
        result = independent_weighted_certificate(
            slopes, radii, height_sets
        )
        checked += 1
        if result["Omega"]:
            nonvacuous += 1
            assert result["constant_two_removed"]
    assert checked == 3**6
    return {
        "profiles": checked,
        "nonvacuous_profiles": nonvacuous,
    }


def audit(exhaustive: bool = True):
    slopes = (-7, -2, 1, 5, 11)
    radii = (1, 2, 4, 7, 9, 11)
    prescribed_sizes = {
        (1, 1): 12,
        (1, 2): 9,
        (1, 4): 7,
        (1, 7): 5,
        (1, 9): 3,
        (1, 11): 2,
        (-7, 1): 3,
        (-2, 2): 4,
        (5, 4): 5,
        (11, 7): 3,
        (-7, 9): 2,
        (11, 11): 2,
    }
    height_sets = {
        (slope, radius): {
            5 * index * index
            - 11 * index
            + 3 * slope
            - 2 * radius
            for index in range(
                prescribed_sizes.get((slope, radius), 0)
            )
        }
        for slope in slopes
        for radius in radii
    }
    primary = independent_weighted_certificate(
        slopes, radii, height_sets
    )
    assert primary["signed_negative_pairs"] > 0
    assert primary["signed_positive_pairs"] > 0
    exhaustive_result = (
        exhaustive_height_size_audit()
        if exhaustive
        else {"profiles": 0, "nonvacuous_profiles": 0}
    )
    return {
        "schema": (
            "amra.erdos1083.weighted-ruled-layer-cake-independent.v1"
        ),
        "verdict": "PASS",
        "scope": (
            "Independent exact finite audit. Signed products retain both "
            "sides with no factor 2; r2 already counts both signs. "
            "The proof requires finite integer height sets, positive "
            "integer radii, and bounded ranges."
        ),
        "primary": primary,
        "exhaustive": exhaustive_result,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-exhaustive", action="store_true")
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
