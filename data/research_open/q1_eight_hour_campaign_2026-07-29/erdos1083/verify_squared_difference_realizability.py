#!/usr/bin/env python3
"""Exact and symbolic certificates for squared-difference realizability."""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import asdict, dataclass

import sympy


@dataclass(frozen=True)
class HadamardRealizationCertificate:
    product_exponent: int
    radius_pairs: tuple[tuple[int, int], ...]
    radial_offsets: tuple[int, ...]
    shifted_blocks: tuple[tuple[int, int], ...]
    pair_intersections: tuple[int, ...]
    pair_symmetric_differences: tuple[int, ...]
    union_size: int
    all_two_point_realizations_exact: bool


@dataclass(frozen=True)
class TriangleCertificate:
    sizes: tuple[int, int, int]
    compatible_value_triples: int
    point_triples: int
    minimum_max_representation: int
    support_lower_bound_numerator: int
    support_lower_bound_denominator: int
    all_values_satisfy_polynomial: bool


def two_point_realization(
    first_square: int,
    second_square: int,
) -> tuple[tuple[sympy.Expr, ...], tuple[sympy.Expr, ...]]:
    if not 0 < first_square < second_square:
        raise ValueError("need 0 < first_square < second_square")
    first = sympy.sqrt(first_square)
    second = sympy.sqrt(second_square)
    alpha = (second + first) / 2
    beta = (second - first) / 2
    return (-alpha, alpha), (-beta, beta)


def symbolic_squared_differences(
    left: tuple[sympy.Expr, ...],
    right: tuple[sympy.Expr, ...],
) -> set[sympy.Expr]:
    return {
        sympy.simplify((first - second) ** 2)
        for first in left
        for second in right
    }


def hadamard_realization() -> HadamardRealizationCertificate:
    pairs = ((0, 5), (1, 4), (2, 3))
    offsets = tuple((2**left - 2**right) ** 2 for left, right in pairs)
    private_values = (1001, 1002, 1003)
    shifted_blocks = tuple(
        (1000, private)
        for private in private_values
    )
    exact = True
    for offset, shifted in zip(offsets, shifted_blocks):
        desired = {sympy.Integer(value - offset) for value in shifted}
        ordered = sorted(int(value) for value in desired)
        left, right = two_point_realization(ordered[0], ordered[1])
        exact = exact and symbolic_squared_differences(left, right) == desired

    intersections = tuple(
        len(set(shifted_blocks[first]) & set(shifted_blocks[second]))
        for first in range(3)
        for second in range(first + 1, 3)
    )
    symmetric_differences = tuple(
        len(set(shifted_blocks[first]) ^ set(shifted_blocks[second]))
        for first in range(3)
        for second in range(first + 1, 3)
    )
    return HadamardRealizationCertificate(
        product_exponent=5,
        radius_pairs=pairs,
        radial_offsets=offsets,
        shifted_blocks=shifted_blocks,
        pair_intersections=intersections,
        pair_symmetric_differences=symmetric_differences,
        union_size=len(set().union(*(set(block) for block in shifted_blocks))),
        all_two_point_realizations_exact=exact,
    )


def representation_counts(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> dict[int, int]:
    counts: dict[int, int] = {}
    for first in left:
        for second in right:
            value = (first - second) ** 2
            counts[value] = counts.get(value, 0) + 1
    return counts


def triangle_certificate(
    first: tuple[int, ...],
    second: tuple[int, ...],
    third: tuple[int, ...],
) -> TriangleCertificate:
    value_triples = {
        ((x - y) ** 2, (y - z) ** 2, (x - z) ** 2)
        for x in first
        for y in second
        for z in third
    }
    all_valid = all(
        (third_value - first_value - second_value) ** 2
        == 4 * first_value * second_value
        for first_value, second_value, third_value in value_triples
    )
    maximum_representations = (
        max(representation_counts(first, second).values()),
        max(representation_counts(second, third).values()),
        max(representation_counts(first, third).values()),
    )
    minimum_max = min(maximum_representations)
    numerator = len(first) * len(second) * len(third)
    denominator = 2 * minimum_max
    return TriangleCertificate(
        sizes=(len(first), len(second), len(third)),
        compatible_value_triples=len(value_triples),
        point_triples=numerator,
        minimum_max_representation=minimum_max,
        support_lower_bound_numerator=numerator,
        support_lower_bound_denominator=denominator,
        all_values_satisfy_polynomial=all_valid,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    examples = (
        ((0, 1, 4, 10), (0, 2, 7, 11), (1, 3, 8, 20)),
        ((0, 3, 6, 9),) * 3,
    )
    payload = {
        "hadamard_realization": asdict(hadamard_realization()),
        "triangle_examples": [
            asdict(triangle_certificate(*example))
            for example in examples
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
