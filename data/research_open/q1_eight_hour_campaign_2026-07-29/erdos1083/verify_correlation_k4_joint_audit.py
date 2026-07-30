#!/usr/bin/env python3
"""Exact exponent and finite certificates for the joint correlation--K4 audit."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction


@dataclass(frozen=True)
class ExponentLedger:
    line_exponent_in_l: Fraction
    correlation_exponent_in_l: Fraction
    dyadic_overlap_boundary_in_l: Fraction
    active_edge_exponent_at_boundary: Fraction
    height_point_count_exponent_in_l: Fraction
    uncoloured_c4_edge_threshold_in_l: Fraction
    required_representation_multiplicity_in_l: Fraction
    automatic_edge_density_at_boundary_in_l: Fraction
    maximum_edge_density_at_boundary_in_l: Fraction


@dataclass(frozen=True)
class ParityBarrier:
    part_size: int
    edge_counts: tuple[int, int, int, int]
    edge_densities: tuple[Fraction, Fraction, Fraction, Fraction]
    transversal_cycle_count: int


def exponent_ledger(eta: Fraction) -> ExponentLedger:
    line_exponent = Fraction(8, 3) + eta
    correlation_exponent = Fraction(6, 1) - line_exponent
    overlap_boundary = correlation_exponent - Fraction(5, 2)
    active_at_boundary = correlation_exponent - overlap_boundary - 1
    representation_needed = Fraction(3, 1) - (
        correlation_exponent - 1
    )
    return ExponentLedger(
        line_exponent_in_l=line_exponent,
        correlation_exponent_in_l=correlation_exponent,
        dyadic_overlap_boundary_in_l=overlap_boundary,
        active_edge_exponent_at_boundary=active_at_boundary,
        height_point_count_exponent_in_l=Fraction(2, 1),
        uncoloured_c4_edge_threshold_in_l=Fraction(3, 1),
        required_representation_multiplicity_in_l=representation_needed,
        automatic_edge_density_at_boundary_in_l=(
            overlap_boundary - 2
        ),
        maximum_edge_density_at_boundary_in_l=(
            overlap_boundary - 1
        ),
    )


def parity_barrier(part_size: int) -> ParityBarrier:
    if part_size < 2 or part_size % 2:
        raise ValueError("need a positive even part size")

    def allowed(edge: int, left: int, right: int) -> bool:
        return (
            left % 2 == right % 2
            if edge < 3
            else left % 2 != right % 2
        )

    counts = tuple(
        sum(
            allowed(edge, left, right)
            for left in range(part_size)
            for right in range(part_size)
        )
        for edge in range(4)
    )
    cycles = sum(
        all(
            allowed(edge, values[edge], values[(edge + 1) % 4])
            for edge in range(4)
        )
        for values in itertools.product(range(part_size), repeat=4)
    )
    return ParityBarrier(
        part_size=part_size,
        edge_counts=counts,
        edge_densities=tuple(
            Fraction(count, part_size * part_size)
            for count in counts
        ),
        transversal_cycle_count=cycles,
    )


def has_c4(vertex_count: int, edges: set[tuple[int, int]]) -> bool:
    neighbours = [set() for _ in range(vertex_count)]
    for first, second in edges:
        neighbours[first].add(second)
        neighbours[second].add(first)
    return any(
        len(neighbours[first] & neighbours[second]) >= 2
        for first in range(vertex_count)
        for second in range(first + 1, vertex_count)
    )


def c4_free_path_inequality(
    vertex_count: int,
    edges: set[tuple[int, int]],
) -> bool:
    if has_c4(vertex_count, edges):
        return True
    degrees = [0] * vertex_count
    for first, second in edges:
        degrees[first] += 1
        degrees[second] += 1
    return sum(math.comb(degree, 2) for degree in degrees) <= math.comb(
        vertex_count,
        2,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epsilon-numerator", type=int, default=1)
    parser.add_argument("--epsilon-denominator", type=int, default=20)
    parser.add_argument("--part-size", type=int, default=12)
    args = parser.parse_args()
    epsilon = Fraction(
        args.epsilon_numerator,
        args.epsilon_denominator,
    )
    eta = 2 * epsilon
    ledger = exponent_ledger(eta)
    barrier = parity_barrier(args.part_size)
    payload = {
        "epsilon_in_f": str(epsilon),
        "eta_in_l": str(eta),
        "exponent_ledger": {
            key: str(value)
            for key, value in asdict(ledger).items()
        },
        "parity_barrier": {
            **asdict(barrier),
            "edge_densities": [
                str(value) for value in barrier.edge_densities
            ],
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
