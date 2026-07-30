#!/usr/bin/env python3
"""Verifier for the cross-plane to weighted-chart interface."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from fractions import Fraction

import sympy as sp


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


def lcm(values) -> int:
    result = 1
    for value in values:
        result = math.lcm(result, value)
    return result


def radial_statistics(height_sizes):
    """Return cross radial energy and weighted overlap."""

    cross_energy = 0
    overlap = 0
    maximum = 0
    for sizes in height_sizes.values():
        maximum = max(maximum, *sizes)
        for left, right in itertools.permutations(sizes, 2):
            cross_energy += left*right
            overlap += min(left, right)
    return {
        "cross_energy": cross_energy,
        "weighted_overlap": overlap,
        "U": maximum,
    }


def rational_sqrt(value: Fraction) -> Fraction:
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if (
        numerator*numerator != value.numerator
        or denominator*denominator != value.denominator
    ):
        raise ValueError(f"{value} is not a rational square")
    return Fraction(numerator, denominator)


def rational_unit_point(parameter: Fraction):
    """Rational parametrization of the unit circle."""

    denominator = 1+parameter*parameter
    return (
        (1-parameter*parameter)/denominator,
        2*parameter/denominator,
    )


def chord_length(left, right) -> Fraction:
    squared = sum(
        (a-b)**2 for a, b in zip(left, right)
    )
    return rational_sqrt(squared)


def rational_chord_certificate(
    parameters,
    radii,
    height_sets,
):
    """Execute the rational-chord layer-cake proof."""

    rays = tuple(range(len(parameters)))
    points = {
        ray: rational_unit_point(Fraction(parameters[ray]))
        for ray in rays
    }
    heights = {
        (ray, radius): tuple(sorted(set(
            height_sets.get((ray, radius), ())
        )))
        for ray in rays
        for radius in radii
    }
    sizes = {
        key: len(value) for key, value in heights.items()
    }
    maximum_size = max(sizes.values())
    levels = tuple(
        2**power
        for power in range(1+math.floor(math.log2(maximum_size)))
    )

    chords = {
        (ray, other): chord_length(points[ray], points[other])
        for ray in rays
        for other in rays
        if ray != other
    }
    denominators = [
        value.denominator for value in chords.values()
    ]
    denominators.extend(
        Fraction(height).denominator
        for values in heights.values()
        for height in values
    )
    scale = lcm(denominators)

    omega = sum(
        min(sizes[(ray, radius)], sizes[(other, radius)])
        for radius in radii
        for ray in rays
        for other in rays
        if ray != other
    )
    stars = {
        base: sum(
            min(sizes[(ray, radius)], sizes[(base, radius)])
            for radius in radii
            for ray in rays
            if ray != base
        )
        for base in rays
    }
    base = max(rays, key=lambda ray: stars[ray])
    assert stars[base]*len(rays) >= omega

    superlevels = {}
    for threshold in levels:
        superlevels[threshold] = [
            (ray, radius)
            for ray in rays
            for radius in radii
            if ray != base
            and min(
                sizes[(ray, radius)], sizes[(base, radius)]
            ) >= threshold
        ]
    threshold = max(
        levels,
        key=lambda value: value*len(superlevels[value]),
    )
    selected = superlevels[threshold]
    assert (
        threshold*len(selected)*len(levels)
        >= stars[base]
    )

    chord_fibres = {}
    for ray, radius in selected:
        scaled = scale*radius*chords[(ray, base)]
        assert scaled.denominator == 1 and scaled > 0
        chord_fibres.setdefault(int(scaled), []).append(
            (ray, radius)
        )
    multiplicity = max(map(len, chord_fibres.values()))

    distance_fibres = Counter()
    for scaled_chord, representations in chord_fibres.items():
        ray, radius = representations[0]
        anchor = heights[(base, radius)][0]
        for height in heights[(ray, radius)][:threshold]:
            vertical = scale*(Fraction(height)-Fraction(anchor))
            assert vertical.denominator == 1
            scaled_label = (
                scaled_chord**2+int(vertical)**2
            )
            direct = (
                radius**2*chords[(ray, base)]**2
                +(Fraction(height)-Fraction(anchor))**2
            )
            assert Fraction(scaled_label, scale**2) == direct
            distance_fibres[scaled_label] += 1

    r2_bound = max(
        4*divisor_count(label) for label in distance_fibres
    )
    assert max(distance_fibres.values()) <= r2_bound
    theorem_lower = (
        omega
        /(len(rays)*len(levels)*multiplicity*r2_bound)
    )
    assert len(distance_fibres) >= theorem_lower
    return {
        "rays": len(rays),
        "radii": len(radii),
        "Omega": omega,
        "U": maximum_size,
        "levels": len(levels),
        "scale_q": scale,
        "base": base,
        "selected_H": threshold,
        "selected_pairs": len(selected),
        "distinct_chords": len(chord_fibres),
        "chord_multiplicity_K": multiplicity,
        "distance_inputs": threshold*len(chord_fibres),
        "distance_labels": len(distance_fibres),
        "r2_bound": r2_bound,
        "theorem_lower_bound": theorem_lower,
    }


def pentagonal_prism_ledger(height: int):
    """Exact symbolic ledger for the five-column no-go."""

    if height < 1:
        raise ValueError("height must be positive")
    sqrt5 = sp.sqrt(5)
    short = (5-sqrt5)/2
    long = (5+sqrt5)/2
    ratio = sp.simplify(long/short)
    representation_energy = (
        height*height
        +sum(4*(height-difference)**2
            for difference in range(1, height))
    )
    labels = {
        sp.Integer(difference*difference)
        for difference in range(height)
    }
    labels |= {
        sp.expand(short+difference*difference)
        for difference in range(height)
    }
    labels |= {
        sp.expand(long+difference*difference)
        for difference in range(height)
    }
    assert len(labels) == 3*height
    assert ratio.is_rational is False
    return {
        "height": height,
        "points": 5*height,
        "Omega_cyl": 20*height,
        "distance_labels": len(labels),
        "short_chord_squared": str(short),
        "long_chord_squared": str(long),
        "squared_ratio": str(ratio),
        "ratio_is_rational": False,
        "one_plane_pair_energy": representation_energy,
        "cross_plane_codegree": 180*representation_energy,
    }


def audit():
    radial = radial_statistics({
        "rho1": [0, 3, 7, 10],
        "rho2": [1, 1, 8, 12],
        "rho3": [0, 0, 2, 9],
    })
    assert (
        radial["weighted_overlap"]*radial["U"]
        >= radial["cross_energy"]
    )

    parameters = (
        Fraction(0),
        Fraction(3, 4),
        Fraction(5, 12),
    )
    radii = (1, 2, 3, 4)
    height_sets = {
        (ray, radius): {
            3*index+ray-radius
            for index in range(1+(2*ray+3*radius) % 9)
        }
        for ray in range(len(parameters))
        for radius in radii
    }
    rational = rational_chord_certificate(
        parameters, radii, height_sets
    )
    pentagon = pentagonal_prism_ledger(20)
    return {
        "schema": "amra.erdos1083.cross-plane-weighted-chart.v1",
        "verdict": "PARTIAL_THEOREMS_PASS_FULL_EXTRACTION_OPEN",
        "radial_energy_to_overlap": radial,
        "rational_chord_certificate": rational,
        "pentagonal_no_go": pentagon,
        "critical_success_condition": "chi+kappa<1 at gamma=7,u=2",
        "missing_branches": [
            "cross-plane codegree to radial cross-angle energy",
            "radial overlap to polynomial rational/number-field chart",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
