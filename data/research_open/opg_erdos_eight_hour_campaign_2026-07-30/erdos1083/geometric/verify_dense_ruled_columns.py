#!/usr/bin/env python3
"""Exact certificate for dense, incomplete ruled-column expansion."""

from __future__ import annotations

import json
from collections import Counter, defaultdict

from verify_affine_height_ruled_columns import divisor_count


def dense_lattice_column_certificate(
    slopes,
    radial_parameters,
    occupied_columns,
    height_length,
    height_sets,
):
    """Audit the proof for arbitrary bounded integral height fibres."""

    slopes = tuple(sorted(set(slopes)))
    radial_parameters = tuple(sorted(set(radial_parameters)))
    occupied_columns = set(occupied_columns)
    if len(slopes) < 2:
        raise ValueError("need at least two slopes")
    if not radial_parameters or radial_parameters[0] < 1:
        raise ValueError("radial parameters must be positive")
    if height_length < 1:
        raise ValueError("height length must be positive")
    universe = {
        (slope, radial)
        for slope in slopes
        for radial in radial_parameters
    }
    if not occupied_columns <= universe:
        raise ValueError("occupied column outside the declared universe")
    if any(column not in height_sets for column in occupied_columns):
        raise ValueError("missing heights for an occupied column")
    normalized_heights = {
        column: tuple(sorted(set(height_sets[column])))
        for column in occupied_columns
    }
    if any(
        len(normalized_heights[column]) < height_length
        for column in occupied_columns
    ):
        raise ValueError("an occupied column has too few heights")

    by_radial = defaultdict(set)
    for slope, radial in occupied_columns:
        by_radial[radial].add(slope)
    psi = sum(
        len(neighbours) * (len(neighbours) - 1)
        for neighbours in by_radial.values()
    )

    star_pairs = {}
    for base in slopes:
        star_pairs[base] = [
            (slope, radial)
            for radial, neighbours in by_radial.items()
            if base in neighbours
            for slope in neighbours
            if slope != base
        ]
    assert sum(map(len, star_pairs.values())) == psi
    base = max(slopes, key=lambda slope: len(star_pairs[slope]))
    star = star_pairs[base]
    assert len(star) * len(slopes) >= psi

    product_representations = defaultdict(list)
    for slope, radial in star:
        product = radial * (slope - base)
        product_representations[product].append((slope, radial))

    slope_diameter = max(slopes) - min(slopes)
    maximum_radial = max(radial_parameters)
    maximum_product = maximum_radial * slope_diameter
    t_product = max(
        divisor_count(value)
        for value in range(1, maximum_product + 1)
    )
    assert all(
        len(representations) <= t_product
        for representations in product_representations.values()
    )
    assert (
        len(product_representations) * t_product
        >= len(star)
    )

    maximum_height = max(
        (
            abs(height)
            for column in occupied_columns
            for height in normalized_heights[column]
        ),
        default=0,
    )
    maximum_label = (
        maximum_product**2
        + (2 * maximum_height) ** 2
    )
    t_two_squares = max(
        4 * divisor_count(value)
        for value in range(1, maximum_label + 1)
    )

    label_fibres = Counter()
    for product, representations in product_representations.items():
        slope, radial = representations[0]
        base_height = normalized_heights[(base, radial)][0]
        for height in normalized_heights[
            (slope, radial)
        ][:height_length]:
            vertical = height - base_height
            label_fibres[product**2 + vertical**2] += 1
    assert all(
        multiplicity <= t_two_squares
        for multiplicity in label_fibres.values()
    )

    exact_bound = (
        height_length
        * psi
        / (len(slopes) * t_product * t_two_squares)
    )
    moment_bound = (
        height_length
        * (
            len(occupied_columns) ** 2 / len(radial_parameters)
            - len(occupied_columns)
        )
        / (len(slopes) * t_product * t_two_squares)
    )
    assert len(label_fibres) >= exact_bound
    assert psi >= (
        len(occupied_columns) ** 2 / len(radial_parameters)
        - len(occupied_columns)
    )

    return {
        "slopes": len(slopes),
        "radial_parameters": len(radial_parameters),
        "occupied_columns": len(occupied_columns),
        "psi": psi,
        "base_slope": base,
        "base_star": len(star),
        "retained_signed_star": len(star),
        "distinct_products": len(product_representations),
        "product_divisor_bound": t_product,
        "distance_inputs": (
            len(product_representations) * height_length
        ),
        "two_square_divisor_bound": t_two_squares,
        "distinct_distance_labels": len(label_fibres),
        "exact_theorem_bound": exact_bound,
        "moment_theorem_bound": moment_bound,
    }


def dense_ruled_column_certificate(
    slopes,
    radial_parameters,
    occupied_columns,
    height_length,
    shifts,
):
    """Compatibility wrapper for independently translated intervals."""

    height_sets = {
        column: tuple(
            shifts[column] + index
            for index in range(height_length)
        )
        for column in occupied_columns
    }
    return dense_lattice_column_certificate(
        slopes,
        radial_parameters,
        occupied_columns,
        height_length,
        height_sets,
    )


def audit():
    slopes = tuple(range(-4, 6))
    radial_parameters = tuple(range(1, 10))
    occupied = {
        (slope, radial)
        for slope in slopes
        for radial in radial_parameters
        if (3 * slope + 5 * radial) % 7 not in {0, 1}
    }
    shifts = {
        (slope, radial): (
            (slope % 3 - 1) * radial
            + 2 * slope
            + (radial % 2)
        )
        for slope, radial in occupied
    }
    certificate = dense_ruled_column_certificate(
        slopes,
        radial_parameters,
        occupied,
        18,
        shifts,
    )
    return {
        "schema": "amra.erdos1083.dense-ruled-columns.v1",
        "verdict": "PASS",
        "theorem": (
            "arbitrary lattice fibres: |Delta^2(P)| >= H*Psi/"
            "(|J|*T_product*T_r2)"
        ),
        "certificate": certificate,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
