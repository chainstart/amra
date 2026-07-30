#!/usr/bin/env python3
"""Exact overlap-energy checks for independently varying height sets."""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import asdict, dataclass
from fractions import Fraction


@dataclass(frozen=True)
class EnergyCertificate:
    radius_count: int
    point_count: int
    line_count: int
    incidence_mass: int
    ordered_cross_correlation: int
    second_moment: int
    cauchy_lower_bound: Fraction
    elementary_incidence_lower_bound: Fraction
    maximum_pair_correlation: int
    ordered_block_pair_count: int


@dataclass(frozen=True)
class SearchCertificate:
    radius_count: int
    height_count: int
    iterations: int
    initial_line_count: int
    best_line_count: int
    ratio_over_f_three_halves: float
    best_height_sets: tuple[tuple[int, ...], ...]


def blocks_by_product(
    height_sets: tuple[tuple[int, ...], ...],
    *,
    ratio: int = 2,
    radial_scale: int = 1,
) -> dict[int, list[tuple[int, frozenset[int]]]]:
    blocks: dict[int, list[tuple[int, frozenset[int]]]] = {}
    for left, left_heights in enumerate(height_sets):
        for right in range(left, len(height_sets)):
            right_heights = height_sets[right]
            offset = radial_scale**2 * (
                ratio**left - ratio**right
            ) ** 2
            squared_differences = frozenset(
                (z - w) ** 2
                for z in left_heights
                for w in right_heights
            )
            blocks.setdefault(left + right, []).append(
                (offset, squared_differences)
            )
    return blocks


def energy_certificate(
    height_sets: tuple[tuple[int, ...], ...],
    *,
    ratio: int = 2,
    radial_scale: int = 1,
) -> EnergyCertificate:
    blocks = blocks_by_product(
        height_sets,
        ratio=ratio,
        radial_scale=radial_scale,
    )
    incidence_mass = 0
    line_count = 0
    ordered_correlation = 0
    maximum_correlation = 0
    ordered_block_pairs = 0
    second_moment = 0

    for product_blocks in blocks.values():
        shifted = [
            {offset + value for value in values}
            for offset, values in product_blocks
        ]
        incidence_mass += sum(len(values) for values in shifted)
        union = set().union(*shifted)
        line_count += len(union)
        multiplicities = {
            value: sum(value in values for values in shifted)
            for value in union
        }
        second_moment += sum(value * value for value in multiplicities.values())
        for first, first_values in enumerate(shifted):
            for second, second_values in enumerate(shifted):
                if first == second:
                    continue
                overlap = len(first_values & second_values)
                ordered_correlation += overlap
                maximum_correlation = max(maximum_correlation, overlap)
                ordered_block_pairs += 1

    point_count = sum(len(values) for values in height_sets)
    radius_count = len(height_sets)
    return EnergyCertificate(
        radius_count=radius_count,
        point_count=point_count,
        line_count=line_count,
        incidence_mass=incidence_mass,
        ordered_cross_correlation=ordered_correlation,
        second_moment=second_moment,
        cauchy_lower_bound=Fraction(
            incidence_mass * incidence_mass,
            second_moment,
        ),
        elementary_incidence_lower_bound=Fraction(
            (radius_count + 1) * point_count,
            4,
        ),
        maximum_pair_correlation=maximum_correlation,
        ordered_block_pair_count=ordered_block_pairs,
    )


def divisor_count(number: int) -> int:
    number = abs(number)
    if number == 0:
        raise ValueError("divisor bound requires a nonzero integer")
    result = 1
    prime = 2
    while prime * prime <= number:
        exponent = 0
        while number % prime == 0:
            number //= prime
            exponent += 1
        if exponent:
            result *= exponent + 1
        prime += 1
    if number > 1:
        result *= 2
    return result


def verify_divisor_bound(
    height_sets: tuple[tuple[int, ...], ...],
    *,
    ratio: int = 2,
    radial_scale: int = 1,
) -> bool:
    for product_blocks in blocks_by_product(
        height_sets,
        ratio=ratio,
        radial_scale=radial_scale,
    ).values():
        for first in range(len(product_blocks)):
            first_offset, first_values = product_blocks[first]
            first_shifted = {
                first_offset + value for value in first_values
            }
            for second in range(first + 1, len(product_blocks)):
                second_offset, second_values = product_blocks[second]
                second_shifted = {
                    second_offset + value for value in second_values
                }
                delta = second_offset - first_offset
                if len(first_shifted & second_shifted) > divisor_count(delta):
                    return False
    return True


def adversarial_search(
    radius_count: int,
    height_count: int,
    *,
    universe_size: int,
    iterations: int,
    seed: int,
) -> SearchCertificate:
    if universe_size < height_count:
        raise ValueError("universe is too small")
    rng = random.Random(seed)
    step = 3 if 3 * (height_count - 1) < universe_size else 1
    initial = tuple(
        tuple(step * index for index in range(height_count))
        for _ in range(radius_count)
    )
    current = [list(values) for values in initial]
    current_count = energy_certificate(tuple(map(tuple, current))).line_count
    initial_count = current_count
    best_count = current_count
    best = tuple(map(tuple, current))

    for _ in range(iterations):
        radius = rng.randrange(radius_count)
        position = rng.randrange(height_count)
        replacement = rng.randrange(universe_size)
        if replacement in current[radius]:
            continue
        old = current[radius][position]
        current[radius][position] = replacement
        current[radius].sort()
        candidate = energy_certificate(tuple(map(tuple, current))).line_count
        if candidate <= current_count:
            current_count = candidate
            if candidate < best_count:
                best_count = candidate
                best = tuple(map(tuple, current))
        else:
            current[radius].remove(replacement)
            current[radius].append(old)
            current[radius].sort()

    point_count = radius_count * height_count
    return SearchCertificate(
        radius_count=radius_count,
        height_count=height_count,
        iterations=iterations,
        initial_line_count=initial_count,
        best_line_count=best_count,
        ratio_over_f_three_halves=best_count / point_count**1.5,
        best_height_sets=best,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=5000)
    args = parser.parse_args()
    height_sets = (
        (0, 1, 4, 12),
        (0, 3, 9, 11),
        (2, 5, 13, 20),
        (0, 7, 8, 19),
    )
    energy = energy_certificate(height_sets)
    payload = {
        "energy_check": {
            **asdict(energy),
            "cauchy_lower_bound": str(energy.cauchy_lower_bound),
            "elementary_incidence_lower_bound": str(
                energy.elementary_incidence_lower_bound
            ),
            "second_moment_identity": (
                energy.second_moment
                == energy.incidence_mass
                + energy.ordered_cross_correlation
            ),
            "divisor_bound_verified": verify_divisor_bound(height_sets),
        },
        "adversarial_searches": [
            asdict(
                adversarial_search(
                    size,
                    size,
                    universe_size=3 * size + 8,
                    iterations=args.iterations,
                    seed=20260729 + size,
                )
            )
            for size in range(3, 8)
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
