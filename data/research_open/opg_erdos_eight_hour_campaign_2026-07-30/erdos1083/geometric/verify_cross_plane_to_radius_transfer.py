#!/usr/bin/env python3
"""Verifier for the cross-plane-to-radius transfer attack."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from fractions import Fraction
from math import isqrt


def squarefree_kernel(value: int) -> int:
    """Return the squarefree kernel of a positive integer."""

    if value < 1:
        raise ValueError("value must be positive")
    kernel = 1
    prime = 2
    remaining = value
    while prime * prime <= remaining:
        parity = 0
        while remaining % prime == 0:
            remaining //= prime
            parity ^= 1
        if parity:
            kernel *= prime
        prime += 1
    if remaining > 1:
        kernel *= remaining
    return kernel


def distinct_kernel_slopes(limit: int) -> tuple[int, ...]:
    """Greedily select slopes with distinct kernels of 1+j^2."""

    if limit < 1:
        raise ValueError("limit must be positive")
    seen: set[int] = set()
    selected = []
    for slope in range(1, limit + 1):
        kernel = squarefree_kernel(1 + slope * slope)
        if kernel not in seen:
            seen.add(kernel)
            selected.append(slope)
    return tuple(selected)


def binary_form(slope: int, other_slope: int, a: int, b: int) -> int:
    """(a-b)^2+(j*a-k*b)^2."""

    return (a - b) ** 2 + (slope * a - other_slope * b) ** 2


def binary_form_determinant(slope: int, other_slope: int) -> int:
    """Determinant of the 2-by-2 coefficient matrix."""

    return (slope - other_slope) ** 2


def squared_distance(
    left: tuple[int, int, int], right: tuple[int, int, int]
) -> int:
    """Squared distance between encoded points (j,a,z)->(a,j*a,z)."""

    slope, radial_parameter, height = left
    other_slope, other_radial_parameter, other_height = right
    return (
        binary_form(
            slope, other_slope, radial_parameter, other_radial_parameter
        )
        + (height - other_height) ** 2
    )


def four_plane_identity(
    x: float,
    alpha: float,
    z: float,
    y: float,
    beta: float,
    w: float,
) -> float:
    """Squared distance in signed cylindrical coordinates."""

    from math import cos

    return x * x + y * y - 2 * x * y * cos(alpha - beta) + (z - w) ** 2


def family_points(
    t: int, use_distinct_kernels: bool = False
) -> tuple[tuple[int, int, int], ...]:
    """Return (slope, radial parameter, height) for the ruled family."""

    if t < 2:
        raise ValueError("need t >= 2")
    slopes = (
        distinct_kernel_slopes(t)
        if use_distinct_kernels
        else tuple(range(1, t + 1))
    )
    return tuple(
        (slope, radial_parameter, height)
        for slope in slopes
        for radial_parameter in range(1, t + 1)
        for height in range(t * t)
    )


def radius_angle_energy(
    points: tuple[tuple[int, int, int], ...]
) -> tuple[int, int]:
    """Return energy and number of distinct squared radii."""

    counts: Counter[int] = Counter()
    for slope, radial_parameter, _ in points:
        radius_squared = radial_parameter**2 * (1 + slope**2)
        counts[radius_squared] += 1
    return sum(value * value for value in counts.values()), len(counts)


def ruled_distance_subset(
    t: int, use_distinct_kernels: bool = True
) -> dict[str, int]:
    """Distances (a(j-k0))^2+u^2 used in the asymptotic lower bound."""

    slopes = (
        distinct_kernel_slopes(t)
        if use_distinct_kernels
        else tuple(range(1, t + 1))
    )
    base = min(slopes)
    differences = {slope - base for slope in slopes if slope > base}
    products = {
        radial_parameter * difference
        for radial_parameter in range(1, t + 1)
        for difference in differences
    }
    labels = {
        product * product + height_difference * height_difference
        for product in products
        for height_difference in range(t * t)
    }
    return {
        "slope_differences": len(differences),
        "product_inputs": t * len(differences),
        "distinct_products": len(products),
        "sum_of_two_squares_inputs": len(products) * t * t,
        "distinct_distance_labels": len(labels),
    }


def enumerated_metrics(
    t: int, use_distinct_kernels: bool = False
) -> dict[str, int | float]:
    """Exact total, diagonal, and cross-plane distance energies."""

    points = family_points(t, use_distinct_kernels)
    total_counts: Counter[int] = Counter()
    plane_pair_counts: defaultdict[
        tuple[int, int], Counter[int]
    ] = defaultdict(Counter)
    for left in points:
        for right in points:
            label = squared_distance(left, right)
            total_counts[label] += 1
            plane_pair_counts[(left[0], right[0])][label] += 1
    total_energy = sum(value * value for value in total_counts.values())
    diagonal_energy = sum(
        value * value
        for counts in plane_pair_counts.values()
        for value in counts.values()
    )
    radial_energy, radius_count = radius_angle_energy(points)
    source_mass = len(points)
    transfer_scale = (source_mass ** Fraction(3, 2)) * radial_energy
    return {
        "t": t,
        "active_planes": len({point[0] for point in points}),
        "points_per_plane": t**3,
        "source_mass": source_mass,
        "distance_labels": len(total_counts),
        "maximum_squared_distance": max(total_counts),
        "total_distance_energy": total_energy,
        "plane_pair_diagonal_energy": diagonal_energy,
        "cross_plane_codegree": total_energy - diagonal_energy,
        "radius_angle_energy": radial_energy,
        "distinct_radii": radius_count,
        "cross_over_unsaved_transfer": float(
            (total_energy - diagonal_energy) / transfer_scale
        ),
    }


def asymptotic_ledger() -> dict[str, str]:
    """Power exponents in t and in N=t^5."""

    return {
        "M": "t^(1-o(1))=N^(1/5-o(1))",
        "Q": "t^3=N^(3/5)",
        "source_mass_S": "t^(4-o(1))=N^(4/5-o(1))",
        "radius_angle_energy": "t^(6-o(1))=N^(6/5-o(1))",
        "distance_label_upper": "O(t^4)=O(N^(4/5))",
        "ruled_distance_lower": "t^(4-o(1))=N^(4/5-o(1))",
        "total_distance_energy_lower": "t^(12-o(1))",
        "plane_pair_diagonal_upper": "t^(10+o(1))",
        "cross_plane_codegree": "t^(12-o(1))",
        "unsaved_transfer_scale": "S^(3/2)*E=t^(12-o(1))",
        "critical_forced_cross_plane": "t^(13-o(1))=N^(13/5-o(1))",
        "missing_factor": "t=N^(1/5)",
    }


def main() -> None:
    print(
        json.dumps(
            {
                "asymptotic": asymptotic_ledger(),
                "finite_full_slope_family": enumerated_metrics(5),
                "finite_distinct_kernel_family": enumerated_metrics(
                    5, use_distinct_kernels=True
                ),
                "ruled_distance_subset": ruled_distance_subset(20),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
