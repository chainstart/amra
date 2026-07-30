#!/usr/bin/env python3
"""Exact certificates for the affine-copy reductions and barriers."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import comb


@dataclass(frozen=True)
class BarrierResult:
    value_count: int
    affine_copy_count: int
    common_offset: int
    endpoint_union_size: int
    distinct_parameter_count: int
    all_slopes_positive: bool
    all_height_squares_nonnegative: bool


def construct(q: int, x1: Fraction = Fraction(2, 7)) -> BarrierResult:
    if q < 2:
        raise ValueError("need q >= 2")
    if x1 <= 0:
        raise ValueError("need x1 > 0")

    raw = [
        (u, v, Fraction(v - u, 1) / x1)
        for u in range(1, q + 1)
        for v in range(u + 1, q + 1)
    ]
    max_square = max((slope - 1) ** 2 for _, _, slope in raw)
    offset = (
        max_square.numerator + max_square.denominator - 1
    ) // max_square.denominator

    parameters: set[tuple[Fraction, Fraction]] = set()
    endpoints: set[Fraction] = set()
    height_squares: list[Fraction] = []
    for u, v, slope in raw:
        intercept = Fraction(offset + u, 1)
        parameters.add((intercept, slope))
        endpoints.update((intercept, intercept + slope * x1))
        height_squares.append(intercept - (slope - 1) ** 2)

    return BarrierResult(
        value_count=q,
        affine_copy_count=comb(q, 2),
        common_offset=offset,
        endpoint_union_size=len(endpoints),
        distinct_parameter_count=len(parameters),
        all_slopes_positive=all(slope > 0 for _, _, slope in raw),
        all_height_squares_nonnegative=all(value >= 0 for value in height_squares),
    )


def parameter_line_count(circles: list[tuple[int, int]]) -> int:
    """Count exact (A_ij,B_ij) pairs, including self-pairs."""

    lines = set()
    for i, (radius_i, height_i) in enumerate(circles):
        for radius_j, height_j in circles[i:]:
            lines.add(
                (
                    (radius_i - radius_j) ** 2 + (height_i - height_j) ** 2,
                    2 * radius_i * radius_j,
                )
            )
    return len(lines)


def sidon_grid_line_count(radius_count: int, height_count: int) -> int:
    if radius_count < 1 or height_count < 1:
        raise ValueError("counts must be positive")
    radii = [2 ** (3**index) for index in range(radius_count)]
    circles = [
        (radius, height)
        for radius in radii
        for height in range(height_count)
    ]
    return parameter_line_count(circles)


def geometric_grid_line_count(radius_count: int, height_count: int) -> int:
    """High multiplicative-energy radii with separated radial offsets."""

    if radius_count < 1 or height_count < 1:
        raise ValueError("counts must be positive")
    radii = [height_count * 2**index for index in range(radius_count)]
    circles = [
        (radius, height)
        for radius in radii
        for height in range(height_count)
    ]
    return parameter_line_count(circles)


def critical_exponent(beta: Fraction) -> Fraction:
    return Fraction(2, 5) + Fraction(3, 5) * beta


def all_pairs_st_exponent(line_exponent_in_f: Fraction) -> Fraction:
    return (
        Fraction(2, 5)
        + Fraction(3, 5) * line_exponent_in_f
    ) / 2


def balanced_energy_line_exponent(
    radius_energy_exponent_in_l: Fraction,
) -> Fraction:
    """F-exponent from F^4/(m^3 E_x) when F=L^2 and m=L."""

    return (Fraction(5, 1) - radius_energy_exponent_in_l) / 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--values", type=int, default=20)
    parser.add_argument("--grid-size", type=int, default=5)
    args = parser.parse_args()
    payload = asdict(construct(args.values))
    payload["sidon_balanced_grid"] = {
        "size": args.grid_size,
        "line_count": sidon_grid_line_count(args.grid_size, args.grid_size),
        "expected": args.grid_size * comb(args.grid_size + 1, 2),
    }
    payload["geometric_balanced_grid"] = {
        "size": args.grid_size,
        "line_count": geometric_grid_line_count(args.grid_size, args.grid_size),
        "expected": args.grid_size * comb(args.grid_size + 1, 2),
    }
    payload["critical_exponents"] = {
        "separate_beta_1_4": str(critical_exponent(Fraction(1, 4))),
        "threshold_beta_1_3": str(critical_exponent(Fraction(1, 3))),
        "strong_beta_1_2": str(critical_exponent(Fraction(1, 2))),
        "all_pairs_M_F_4_3": str(all_pairs_st_exponent(Fraction(4, 3))),
        "all_pairs_M_F_3_2": str(all_pairs_st_exponent(Fraction(3, 2))),
        "energy_E_L_7_3_gives_M_F": str(
            balanced_energy_line_exponent(Fraction(7, 3))
        ),
        "energy_E_L_2_gives_M_F": str(
            balanced_energy_line_exponent(Fraction(2, 1))
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
