#!/usr/bin/env python3
"""Exact arithmetic certificates for the angular-starvation attack."""

from __future__ import annotations

import json
from fractions import Fraction


def square_difference_energy(size: int) -> int:
    """Ordered energy of squared differences of {0,...,size-1}."""

    if size < 1:
        raise ValueError("size must be positive")
    square_sum = (size - 1) * size * (2 * size - 1) // 6
    return size * size + 4 * square_sum


def enumerate_square_difference_energy(size: int) -> int:
    """Direct enumeration of the same energy."""

    counts: dict[int, int] = {}
    for left in range(size):
        for right in range(size):
            label = (left - right) ** 2
            counts[label] = counts.get(label, 0) + 1
    return sum(value * value for value in counts.values())


def normalized_rotation_codegree(
    masses: list[int], weights_by_angle: list[list[int]]
) -> Fraction:
    """Sum_C (sum_alpha w(C,alpha))^2/a_C."""

    if not masses or not weights_by_angle:
        raise ValueError("need nonempty data")
    fibre_count = len(masses)
    if any(len(row) != fibre_count for row in weights_by_angle):
        raise ValueError("weight rows must match masses")
    if any(mass <= 0 for mass in masses):
        raise ValueError("masses must be positive")
    for row in weights_by_angle:
        if any(weight < 0 or weight > mass for weight, mass in zip(row, masses)):
            raise ValueError("weights must lie in [0,a_C]")
    return sum(
        (
            Fraction(
                sum(row[index] for row in weights_by_angle) ** 2,
                masses[index],
            )
            for index in range(fibre_count)
        ),
        Fraction(0),
    )


def rotation_cauchy_lower(
    masses: list[int], weights_by_angle: list[list[int]]
) -> Fraction:
    """(sum_{alpha,C} w)^2 / sum_C a_C."""

    total_weight = sum(sum(row) for row in weights_by_angle)
    return Fraction(total_weight * total_weight, sum(masses))


def barrier_ledger(t: int) -> dict[str, int | str]:
    """Exact critical ledger for the Euclidean old-marginal barrier."""

    if t < 3:
        raise ValueError("need t >= 3")
    active_planes = t
    source_per_plane = t**3
    angular_size = t**2
    reservoir_fibres = t**2 * (t - 1)
    point_count = t**5
    rotation_counts = [
        reservoir_fibres * (angular_size - 2 * index)
        for index in range(1, active_planes + 1)
    ]
    rotation_codegree = Fraction(reservoir_fibres, angular_size) * (
        sum(angular_size - 2 * index for index in range(1, active_planes + 1))
        ** 2
    )
    source_mass = active_planes * source_per_plane
    forced_global_energy = Fraction(
        source_mass**4, source_per_plane
    )
    individual_pair_energy = square_difference_energy(source_per_plane)
    return {
        "t": t,
        "N": point_count,
        "D0": source_per_plane,
        "M": active_planes,
        "Q": source_per_plane,
        "S": angular_size,
        "reservoir_fibres": reservoir_fibres,
        "reservoir_points": reservoir_fibres * angular_size,
        "source_points": source_mass,
        "total_points": reservoir_fibres * angular_size + source_mass,
        "minimum_rotation_count": min(rotation_counts),
        "joint_qr_mass": source_per_plane * sum(rotation_counts),
        "normalized_rotation_codegree": str(rotation_codegree),
        "source_radius_angle_energy": active_planes * source_per_plane**2,
        "source_cross_angle_radius_codegree": 0,
        "one_plane_pair_distance_labels": source_per_plane,
        "one_plane_pair_energy": individual_pair_energy,
        "sum_individual_pair_energies": (
            active_planes**2 * individual_pair_energy
        ),
        "forced_global_cross_plane_energy": str(forced_global_energy),
        "critical_radius_xi_scale": source_per_plane,
    }


def exponent_ledger() -> dict[str, str]:
    """All exponents as exact fractions of log N."""

    return {
        "M": str(Fraction(1, 5)),
        "Q": str(Fraction(3, 5)),
        "source_mass_MQ": str(Fraction(4, 5)),
        "forced_rotation_codegree": str(Fraction(7, 5)),
        "radius_angle_threshold": "7/5+delta",
        "barrier_radius_angle_energy": str(Fraction(7, 5)),
        "forced_global_plane_energy": str(Fraction(13, 5)),
        "individual_pair_diagonal_upper": str(Fraction(12, 5)),
        "barrier_individual_pair_energy_sum": str(Fraction(11, 5)),
        "transfer_capacity": str(Fraction(6, 5)),
        "Xi_after_eta_transfer": "3/5+eta",
    }


def transfer_exponents(eta: Fraction) -> dict[str, Fraction]:
    """Consequence of C_plane <= N^(6/5-eta) E_radius-angle."""

    cross_plane = Fraction(13, 5)
    capacity = Fraction(6, 5) - eta
    radius_energy = cross_plane - capacity
    source_mass = Fraction(4, 5)
    maximum_radius_mass = radius_energy - source_mass
    return {
        "cross_plane": cross_plane,
        "capacity": capacity,
        "radius_energy": radius_energy,
        "maximum_radius_mass": maximum_radius_mass,
        "Xi": maximum_radius_mass,
    }


def main() -> None:
    print(
        json.dumps(
            {
                "exponents": exponent_ledger(),
                "finite_barrier": barrier_ledger(6),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
