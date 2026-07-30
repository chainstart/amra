#!/usr/bin/env python3
"""Exact certificates for affine-height ruled-column expansion."""

from __future__ import annotations

import json
from collections import Counter


def divisor_count(value: int) -> int:
    """Return the number of positive divisors of value."""

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


def squared_distance(left, right) -> int:
    """Distance for encoded (slope, radial parameter, height) points."""

    slope, radial, height = left
    other_slope, other_radial, other_height = right
    return (
        (radial-other_radial)**2
        +(slope*radial-other_slope*other_radial)**2
        +(height-other_height)**2
    )


def affine_shift_table(
    slopes,
    radial_parameters,
    coefficients,
    intercepts,
):
    """Return sigma_(j,a)=coefficient_j*a+intercept_j."""

    return {
        (slope, radial): coefficients[slope]*radial+intercepts[slope]
        for slope in slopes
        for radial in radial_parameters
    }


def ruled_column_certificate(
    slopes,
    radial_parameters,
    height_length,
    shifts,
):
    """Construct and audit the distance subset in the theorem."""

    slopes = tuple(sorted(set(slopes)))
    radial_parameters = tuple(sorted(set(radial_parameters)))
    if len(slopes) < 2:
        raise ValueError("need at least two slopes")
    if not radial_parameters or radial_parameters[0] < 1:
        raise ValueError("need positive radial parameters")
    if height_length < 1:
        raise ValueError("height_length must be positive")
    if any(
        (slope, radial) not in shifts
        for slope in slopes
        for radial in radial_parameters
    ):
        raise ValueError("missing a column shift")

    base = slopes[0]
    product_representations = {}
    for slope in slopes[1:]:
        difference = slope-base
        for radial in radial_parameters:
            product = radial*difference
            product_representations.setdefault(product, []).append(
                (slope, radial)
            )

    maximum_product_fibre = max(map(
        len, product_representations.values()
    ))
    product_divisor_bound = max(
        divisor_count(product) for product in product_representations
    )
    assert maximum_product_fibre <= product_divisor_bound

    label_fibres = Counter()
    for product, representations in product_representations.items():
        slope, radial = representations[0]
        base_height = shifts[(base, radial)]
        for height_index in range(height_length):
            other_height = shifts[(slope, radial)]+height_index
            left = (slope, radial, other_height)
            right = (base, radial, base_height)
            label = squared_distance(left, right)
            expected = (
                product*product
                +(other_height-base_height)**2
            )
            assert label == expected
            label_fibres[label] += 1

    maximum_distance_fibre = max(label_fibres.values())
    r2_divisor_bound = max(
        4*divisor_count(label) for label in label_fibres
    )
    assert maximum_distance_fibre <= r2_divisor_bound

    raw_inputs = (
        len(radial_parameters)*(len(slopes)-1)*height_length
    )
    product_inputs = len(product_representations)*height_length
    theorem_denominator = product_divisor_bound*r2_divisor_bound
    theorem_lower_bound = raw_inputs/theorem_denominator
    assert len(label_fibres) >= theorem_lower_bound
    assert len(label_fibres) >= product_inputs/r2_divisor_bound

    return {
        "slopes": len(slopes),
        "radial_parameters": len(radial_parameters),
        "height_length": height_length,
        "raw_inputs": raw_inputs,
        "distinct_products": len(product_representations),
        "maximum_product_fibre": maximum_product_fibre,
        "product_divisor_bound": product_divisor_bound,
        "post_product_inputs": product_inputs,
        "distinct_distance_labels": len(label_fibres),
        "maximum_distance_fibre": maximum_distance_fibre,
        "r2_divisor_bound": r2_divisor_bound,
        "theorem_denominator": theorem_denominator,
        "theorem_lower_bound": theorem_lower_bound,
        "maximum_squared_distance": max(label_fibres),
    }


def audit():
    t = 10
    slopes = tuple(range(1, t+1))
    radial_parameters = tuple(range(1, t+1))
    coefficients = {
        slope: slope % 3-1 for slope in slopes
    }
    intercepts = {
        slope: 2*slope for slope in slopes
    }
    shifts = affine_shift_table(
        slopes,
        radial_parameters,
        coefficients,
        intercepts,
    )
    certificate = ruled_column_certificate(
        slopes, radial_parameters, t*t, shifts
    )
    return {
        "schema": "amra.erdos1083.affine-height-ruled-columns.v1",
        "verdict": "PASS",
        "theorem": (
            "|Delta^2(P)| >= |A|(|J|-1)H/(T_product*T_r2)"
        ),
        "covers_common_height": True,
        "covers_affine_height_shifts": True,
        "finite_t": t,
        "finite_distinct_products": (
            certificate["distinct_products"]
        ),
        "finite_distinct_distance_labels": (
            certificate["distinct_distance_labels"]
        ),
        "finite_theorem_lower_bound": (
            certificate["theorem_lower_bound"]
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
