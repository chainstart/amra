#!/usr/bin/env python3
"""Exact verifier for weighted ruled-column layer cake."""

from __future__ import annotations

import json
import math
from collections import Counter


def divisor_count(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive")
    remaining = value
    result = 1
    prime = 2
    while prime*prime <= remaining:
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        result *= exponent+1
        prime += 1
    if remaining > 1:
        result *= 2
    return result


def normalized_height_sets(slopes, radii, height_sets):
    """Deduplicate heights and insert explicit empty fibres."""

    return {
        (slope, radius): tuple(sorted(set(
            height_sets.get((slope, radius), ())
        )))
        for slope in slopes
        for radius in radii
    }


def weighted_overlap(slopes, radii, height_sets) -> int:
    """Omega=sum_a sum_(j!=k) min(h_ja,h_ka)."""

    return sum(
        min(
            len(height_sets[(slope, radius)]),
            len(height_sets[(other, radius)]),
        )
        for radius in radii
        for slope in slopes
        for other in slopes
        if slope != other
    )


def squared_distance(left, right) -> int:
    """Cartesian distance for encoded (j,a,z)->(a,j*a,z)."""

    slope, radius, height = left
    other_slope, other_radius, other_height = right
    return (
        (radius-other_radius)**2
        +(slope*radius-other_slope*other_radius)**2
        +(height-other_height)**2
    )


def layer_cake_certificate(slopes, radii, height_sets):
    """Execute every selection in the proof and return its ledger."""

    slopes = tuple(sorted(set(slopes)))
    radii = tuple(sorted(set(radii)))
    if len(slopes) < 2:
        raise ValueError("need at least two slopes")
    if not radii or radii[0] < 1:
        raise ValueError("need positive radii")
    heights = normalized_height_sets(slopes, radii, height_sets)
    omega = weighted_overlap(slopes, radii, heights)
    if omega <= 0:
        raise ValueError("positive weighted overlap is required")

    sizes = {
        key: len(value) for key, value in heights.items()
    }
    maximum_height_size = max(sizes.values())
    levels = tuple(
        2**power
        for power in range(1+math.floor(math.log2(maximum_height_size)))
    )

    star_weights = {
        base: sum(
            min(sizes[(slope, radius)], sizes[(base, radius)])
            for radius in radii
            for slope in slopes
            if slope != base
        )
        for base in slopes
    }
    base = max(slopes, key=lambda slope: star_weights[slope])
    assert star_weights[base]*len(slopes) >= omega

    star_pairs = [
        (slope, radius)
        for slope in slopes
        for radius in radii
        if slope != base
        and min(
            sizes[(slope, radius)], sizes[(base, radius)]
        ) > 0
    ]
    selected_star_weight = sum(
        min(sizes[pair], sizes[(base, pair[1])])
        for pair in star_pairs
    )
    assert selected_star_weight == star_weights[base]

    superlevels = {}
    for threshold in levels:
        pairs = [
            pair for pair in star_pairs
            if min(sizes[pair], sizes[(base, pair[1])]) >= threshold
        ]
        superlevels[threshold] = pairs
    layer_sum = sum(
        threshold*len(pairs)
        for threshold, pairs in superlevels.items()
    )
    assert layer_sum >= selected_star_weight
    threshold = max(
        levels,
        key=lambda value: value*len(superlevels[value]),
    )
    selected_pairs = superlevels[threshold]
    assert (
        threshold*len(selected_pairs)*len(levels)
        >= selected_star_weight
    )

    product_representations = {}
    for slope, radius in selected_pairs:
        product = radius*(slope-base)
        product_representations.setdefault(product, []).append(
            (slope, radius)
        )
    maximum_product_fibre = max(map(
        len, product_representations.values()
    ))
    product_divisor_bound = max(
        divisor_count(abs(product))
        for product in product_representations
    )
    assert maximum_product_fibre <= product_divisor_bound

    distance_fibres = Counter()
    for product, representations in product_representations.items():
        slope, radius = representations[0]
        anchor = heights[(base, radius)][0]
        selected_heights = heights[(slope, radius)][:threshold]
        assert len(selected_heights) == threshold
        for height in selected_heights:
            label = squared_distance(
                (slope, radius, height),
                (base, radius, anchor),
            )
            assert label == product**2+(height-anchor)**2
            distance_fibres[label] += 1

    maximum_distance_fibre = max(distance_fibres.values())
    r2_divisor_bound = max(
        4*divisor_count(label) for label in distance_fibres
    )
    assert maximum_distance_fibre <= r2_divisor_bound

    z_bound = max(
        abs(height)
        for values in heights.values()
        for height in values
    )
    radial_bound = max(radii)
    slope_diameter = max(slopes)-min(slopes)
    maximum_label_bound = (
        (radial_bound*slope_diameter)**2+(2*z_bound)**2
    )
    assert max(distance_fibres) <= maximum_label_bound

    layer_count = len(levels)
    theorem_denominator = (
        len(slopes)*layer_count
        *product_divisor_bound*r2_divisor_bound
    )
    theorem_lower_bound = omega/theorem_denominator
    assert len(distance_fibres) >= theorem_lower_bound

    return {
        "slopes": len(slopes),
        "radii": len(radii),
        "U": maximum_height_size,
        "dyadic_levels": layer_count,
        "Omega": omega,
        "base_slope": base,
        "base_star_weight": star_weights[base],
        "selected_star_weight": selected_star_weight,
        "selected_H": threshold,
        "selected_pairs": len(selected_pairs),
        "layer_product": threshold*len(selected_pairs),
        "distinct_products": len(product_representations),
        "maximum_product_fibre": maximum_product_fibre,
        "product_divisor_bound": product_divisor_bound,
        "distance_inputs": (
            threshold*len(product_representations)
        ),
        "distinct_distance_labels": len(distance_fibres),
        "maximum_distance_fibre": maximum_distance_fibre,
        "r2_divisor_bound": r2_divisor_bound,
        "Z": z_bound,
        "maximum_label_bound": maximum_label_bound,
        "theorem_denominator": theorem_denominator,
        "theorem_lower_bound": theorem_lower_bound,
    }


def audit():
    slopes = tuple(range(-3, 4))
    radii = tuple(range(1, 8))
    height_sets = {}
    for slope in slopes:
        for radius in radii:
            size = (3*slope+5*radius) % 17
            if (slope+radius) % 5 == 0:
                size = 0
            height_sets[(slope, radius)] = {
                11*value+2*slope-radius
                for value in range(size)
            }
    result = layer_cake_certificate(
        slopes, radii, height_sets
    )
    return {
        "schema": "amra.erdos1083.weighted-ruled-layer-cake.v1",
        "verdict": "PASS",
        "theorem": (
            "|Delta^2(P)| >= Omega/"
            "(|J|*L_U*T_product*T_r2)"
        ),
        "finite_ledger": result,
        "critical_interface": (
            "Omega=t^(4+eta-o(1)) implies "
            "|Delta^2(P)|=t^(3+eta-o(1))"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
