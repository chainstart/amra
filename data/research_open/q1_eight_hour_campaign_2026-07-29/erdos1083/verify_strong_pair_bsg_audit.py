#!/usr/bin/env python3
"""Verify the strong-pair BSG exponent and saturation audit."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


def hyperbola_pair(
    parameter: int, delta: int | Fraction = 1
) -> tuple[Fraction, Fraction]:
    value = Fraction(parameter, 1)
    shift = Fraction(delta, 1) / value
    return (value + shift) / 2, (shift - value) / 2


def selected_representation_count(
    left: set[Fraction], right: set[Fraction], values: set[Fraction]
) -> dict[Fraction, int]:
    return {
        value: sum(
            (first - second) ** 2 == value
            for first in left
            for second in right
        )
        for value in values
    }


def pad_pair_avoiding_values(
    left: set[Fraction],
    right: set[Fraction],
    selected_values: set[Fraction],
    target_size: int,
) -> tuple[set[Fraction], set[Fraction]]:
    candidate = 1000
    while len(left) < target_size or len(right) < target_size:
        if len(left) < target_size:
            proposed = Fraction(candidate, 1)
            candidate += 1
            if proposed not in left and all(
                (proposed - second) ** 2 not in selected_values
                for second in right
            ):
                left.add(proposed)
        if len(right) < target_size:
            proposed = Fraction(-candidate, 1)
            candidate += 1
            if proposed not in right and all(
                (first - proposed) ** 2 not in selected_values
                for first in left
            ):
                right.add(proposed)
    return left, right


def rational_multiplicity_one_example(
    m: int, overlap_size: int, delta: int = 16065
) -> dict[str, object]:
    if not 1 <= overlap_size < m:
        raise ValueError("require 1 <= overlap_size < m")

    pairs = [
        hyperbola_pair(index + 2, delta) for index in range(overlap_size)
    ]
    xs = {pair[0] for pair in pairs}
    ys = {pair[1] for pair in pairs}
    x_values = {value * value for value in xs}
    y_values = {value * value for value in ys}
    assert {value + delta for value in y_values} == x_values

    first_left, first_right = pad_pair_avoiding_values(
        set(xs), {Fraction(0)}, x_values, m
    )
    second_left, second_right = pad_pair_avoiding_values(
        set(ys), {Fraction(0)}, y_values, m
    )
    first_counts = selected_representation_count(
        first_left, first_right, x_values
    )
    second_counts = selected_representation_count(
        second_left, second_right, y_values
    )
    return {
        "height_count": m,
        "overlap_size": overlap_size,
        "offset_difference": delta,
        "smaller_radial_offset": 64,
        "larger_radial_offset": 16129,
        "first_selected_counts": sorted(first_counts.values()),
        "second_selected_counts": sorted(second_counts.values()),
        "shifted_values_match": {value for value in x_values}
        == {value + delta for value in y_values},
        "actual_shifted_blocks_match": {
            Fraction(64) + value for value in x_values
        }
        == {Fraction(16129) + value for value in y_values},
    }


def zero_shift_interval_energy(m: int, overlap_size: int) -> int:
    if not 1 <= overlap_size < m:
        raise ValueError("require 1 <= overlap_size < m")
    return sum((2 * (m - difference)) ** 2 for difference in range(
        1, overlap_size + 1
    ))


def exponent_ledger(eta_numerator: int, eta_denominator: int) -> dict:
    eta = Fraction(eta_numerator, eta_denominator)
    overlap = Fraction(5, 6) - eta
    maximum_energy = 2 + overlap
    minimum_bsg_parameter = 3 - maximum_energy
    automatic_energy = overlap
    automatic_bsg_parameter = 3 - automatic_energy
    global_target = Fraction(8, 3) + eta
    local_capacity = Fraction(2, 1)
    return {
        "eta": eta,
        "overlap_exponent": overlap,
        "maximum_energy_exponent": maximum_energy,
        "minimum_bsg_parameter_exponent": minimum_bsg_parameter,
        "automatic_energy_exponent": automatic_energy,
        "automatic_bsg_parameter_exponent": automatic_bsg_parameter,
        "global_target_exponent": global_target,
        "local_capacity_exponent": local_capacity,
        "global_propagation_gap_exponent": global_target - local_capacity,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--height-count", type=int, default=12)
    parser.add_argument("--overlap-size", type=int, default=5)
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    parser.add_argument("--offset-difference", type=int, default=16065)
    args = parser.parse_args()
    result = {
        "rational_example": rational_multiplicity_one_example(
            args.height_count, args.overlap_size, args.offset_difference
        ),
        "zero_shift_interval_energy": zero_shift_interval_energy(
            args.height_count, args.overlap_size
        ),
        "exponent_ledger": exponent_ledger(
            args.eta_numerator, args.eta_denominator
        ),
    }
    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
            default=lambda value: (
                int(value)
                if isinstance(value, Fraction) and value.denominator == 1
                else str(value)
            ),
        )
    )


if __name__ == "__main__":
    main()
