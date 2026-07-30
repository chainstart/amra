#!/usr/bin/env python3
"""Exact verifier for the Xi/parameter-energy attack."""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from math import comb


def xi_lower(incidences: int, columns: int, overlap: int) -> Fraction:
    """The exact sparse Xi lower bound."""

    if incidences < 1 or columns < 1 or overlap < 0:
        raise ValueError("need I,J >= 1 and lambda >= 0")
    return Fraction(
        incidences * incidences,
        2 * incidences + overlap * columns * columns,
    )


def xi_inverse_lower(
    incidences: int, columns: int, target: Fraction
) -> Fraction:
    """Lambda forced by the strict inequality Xi < target."""

    if incidences < 1 or columns < 1 or target <= 0:
        raise ValueError("need positive inputs")
    return (
        Fraction(incidences * incidences, 1) / target - 2 * incidences
    ) / (columns * columns)


def square_offset_overlap(height_count: int) -> int:
    """Exact max_{h != 0} |A intersect (A+h)| for A={0^2,...,(m-1)^2}."""

    if height_count < 2:
        return 0
    differences: Counter[int] = Counter()
    squares = [value * value for value in range(height_count)]
    for right in range(1, height_count):
        for left in range(right):
            differences[squares[right] - squares[left]] += 1
    return max(differences.values())


def interval_square_union_count(height_count: int, columns: int) -> int:
    """Count {d^2+k: 0<=d<m, 0<=k<J} exactly."""

    if height_count < 1 or columns < 1:
        raise ValueError("counts must be positive")
    return len(
        {
            difference * difference + chord
            for difference in range(height_count)
            for chord in range(columns)
        }
    )


def grid_circles(t: int, ratio: int = 2) -> tuple[tuple[int, int], ...]:
    """Critical grid: L=t radii and m=t^2 heights."""

    if t < 2 or ratio < 2:
        raise ValueError("need t,ratio >= 2")
    height_count = t * t
    return tuple(
        (height_count * ratio**radius_index, height)
        for radius_index in range(t)
        for height in range(height_count)
    )


def parameter_multiplicities(t: int, ratio: int = 2) -> Counter[tuple[int, int]]:
    """Enumerate all unordered critical-grid circle-pair parameters."""

    circles = grid_circles(t, ratio)
    multiplicities: Counter[tuple[int, int]] = Counter()
    for index, (radius, height) in enumerate(circles):
        for other_radius, other_height in circles[index:]:
            parameter = (
                (radius - other_radius) ** 2 + (height - other_height) ** 2,
                2 * radius * other_radius,
            )
            multiplicities[parameter] += 1
    return multiplicities


def critical_parameter_formula(t: int) -> dict[str, int]:
    """Closed forms from the critical anisotropic-grid theorem."""

    if t < 2:
        raise ValueError("need t >= 2")
    radius_count = t
    height_count = t * t
    circle_count = radius_count * height_count
    square_sum = (
        (height_count - 1) * height_count * (2 * height_count - 1) // 6
    )
    diagonal_energy = height_count * height_count + square_sum
    cross_energy = height_count * height_count + 4 * square_sum
    return {
        "circle_count": circle_count,
        "raw_pairs": circle_count * (circle_count + 1) // 2,
        "parameter_lines": height_count * comb(radius_count + 1, 2),
        "parameter_energy": (
            radius_count * diagonal_energy
            + comb(radius_count, 2) * cross_energy
        ),
    }


def xi_exponent(i: Fraction, j: Fraction, ell: Fraction) -> Fraction:
    """Exponent min(i,2i-ell-2j)."""

    return min(i, 2 * i - ell - 2 * j)


def parameter_exponents(
    raw_pair_exponent: Fraction,
    energy_exponent: Fraction,
    column_exponent: Fraction,
) -> tuple[Fraction, Fraction]:
    """Return (M exponent, ST distance exponent)."""

    line_exponent = 2 * raw_pair_exponent - energy_exponent
    distance_exponent = min(
        line_exponent, (column_exponent + line_exponent) / 2
    )
    return line_exponent, distance_exponent


def energy_threshold_exponent(
    raw_pair_exponent: Fraction,
    column_exponent: Fraction,
    target_exponent: Fraction,
) -> Fraction:
    """Largest energy exponent allowed by both parameter inequalities."""

    return min(
        2 * raw_pair_exponent - target_exponent,
        2 * raw_pair_exponent + column_exponent - 2 * target_exponent,
    )


def exponent_ledger() -> dict[str, str]:
    """The exact sparse/full critical exponent ledger."""

    p = Fraction(6, 5)
    e = Fraction(8, 5)
    sparse_j = Fraction(1, 5)
    full_j = Fraction(2, 5)
    sparse_i = Fraction(3, 5)
    full_i = Fraction(4, 5)
    ell = Fraction(0)
    sparse_m, sparse_parameter = parameter_exponents(p, e, sparse_j)
    full_m, full_parameter = parameter_exponents(p, e, full_j)
    return {
        "raw_pair_p": str(p),
        "parameter_energy_e": str(e),
        "parameter_line_m": str(sparse_m),
        "sparse_J": str(sparse_j),
        "sparse_I": str(sparse_i),
        "sparse_Xi": str(xi_exponent(sparse_i, sparse_j, ell)),
        "sparse_parameter_distance": str(sparse_parameter),
        "sparse_combined": str(
            max(xi_exponent(sparse_i, sparse_j, ell), sparse_parameter)
        ),
        "full_J": str(full_j),
        "full_I": str(full_i),
        "full_Xi": str(xi_exponent(full_i, full_j, ell)),
        "full_parameter_distance": str(full_parameter),
        "full_combined": str(
            max(xi_exponent(full_i, full_j, ell), full_parameter)
        ),
        "sparse_energy_threshold_at_epsilon_zero": str(
            energy_threshold_exponent(p, sparse_j, Fraction(3, 5))
        ),
        "full_energy_threshold_at_epsilon_zero": str(
            energy_threshold_exponent(p, full_j, Fraction(3, 5))
        ),
    }


def critical_metrics(t: int) -> dict[str, int | str]:
    """Finite exact values for both angular-column regimes."""

    if t < 2:
        raise ValueError("need t >= 2")
    height_count = t * t
    sparse_columns = t
    full_columns = height_count
    overlap = square_offset_overlap(height_count)
    sparse_incidences = height_count * sparse_columns
    full_incidences = height_count * full_columns
    formula = critical_parameter_formula(t)
    return {
        "t": t,
        "N": t**5,
        "F": t**3,
        "height_count_m": height_count,
        "overlap_lambda": overlap,
        "parameter_lines_M": formula["parameter_lines"],
        "parameter_energy": formula["parameter_energy"],
        "sparse_columns_J": sparse_columns,
        "sparse_incidences_I": sparse_incidences,
        "sparse_Xi": str(
            xi_lower(sparse_incidences, sparse_columns, overlap)
        ),
        "sparse_actual_interval_union": interval_square_union_count(
            height_count, sparse_columns
        ),
        "full_columns_J": full_columns,
        "full_incidences_I": full_incidences,
        "full_Xi": str(xi_lower(full_incidences, full_columns, overlap)),
        "full_actual_interval_union": interval_square_union_count(
            height_count, full_columns
        ),
        "diagnosis": (
            "sparse J=t has I=t^3=N^(3/5): column-starvation equality; "
            "full J=t^2 makes Xi exponent 4/5"
        ),
    }


def main() -> None:
    report = {
        "exponent_ledger": exponent_ledger(),
        "finite_critical_grid": critical_metrics(6),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
