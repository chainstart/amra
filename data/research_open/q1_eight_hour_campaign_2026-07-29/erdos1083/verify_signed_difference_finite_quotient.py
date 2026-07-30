#!/usr/bin/env python3
"""Verify the mod-seven signed-difference obstruction and network repair."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction


CYCLE_PAIRS = ((0, 7), (7, 1), (1, 16), (16, 0))
EXTERNAL_PAIRS = ((3, 4), (2, 6), (8, 9), (5, 11))
EDGE_COLOURS = (1, 1, 1, 2)


def selected_values(m: int, colour: int, modulus: int = 7) -> set[int]:
    residues = {colour % modulus, (-colour) % modulus}
    return {
        difference * difference
        for difference in range(1, m)
        if difference % modulus in residues
    }


def representation_edges(
    m: int, colour: int, modulus: int = 7
) -> set[tuple[int, int]]:
    values = selected_values(m, colour, modulus)
    return {
        (left, right)
        for left in range(m)
        for right in range(m)
        if (left - right) ** 2 in values
    }


def transversal_cycle_count(m: int) -> int:
    relations = [
        representation_edges(m, colour) for colour in EDGE_COLOURS
    ]
    count = 0
    for z0, z1, z2, z3 in itertools.product(range(m), repeat=4):
        if (
            (z0, z1) in relations[0]
            and (z1, z2) in relations[1]
            and (z2, z3) in relations[2]
            and (z3, z0) in relations[3]
        ):
            count += 1
    return count


def signed_zero_possible(
    colours: tuple[int, ...], modulus: int = 7
) -> bool:
    return any(
        sum(sign * colour for sign, colour in zip(signs, colours))
        % modulus
        == 0
        for signs in itertools.product((-1, 1), repeat=len(colours))
    )


def bad_colour_multisets() -> set[tuple[int, ...]]:
    return {
        tuple(sorted(colours))
        for colours in itertools.product((1, 2, 3), repeat=4)
        if not signed_zero_possible(colours)
    }


def all_k23_colourings_repair() -> bool:
    for labels in itertools.product((1, 2, 3), repeat=6):
        top = labels[:3]
        bottom = labels[3:]
        cycle_lifts = []
        for first, second in itertools.combinations(range(3), 2):
            colours = (
                top[first],
                top[second],
                bottom[first],
                bottom[second],
            )
            cycle_lifts.append(signed_zero_possible(colours))
        if not any(cycle_lifts):
            return False
    return True


def radial_offset(pair: tuple[int, int]) -> int:
    first, second = pair
    return (2**first - 2**second) ** 2


def build_certificate(m: int) -> dict[str, object]:
    if m < 7 or m % 7:
        raise ValueError("height count must be a positive multiple of seven")

    edges = []
    for cycle_pair, external_pair, colour in zip(
        CYCLE_PAIRS, EXTERNAL_PAIRS, EDGE_COLOURS
    ):
        values = selected_values(m, colour)
        representations = representation_edges(m, colour)
        cycle_offset = radial_offset(cycle_pair)
        external_offset = radial_offset(external_pair)
        difference = cycle_offset - external_offset
        target_values = {difference + value for value in values}
        edges.append(
            {
                "cycle_pair": cycle_pair,
                "external_pair": external_pair,
                "common_sum": sum(cycle_pair),
                "selected_value_count": len(values),
                "representation_count": len(representations),
                "average_representation_multiplicity": Fraction(
                    len(representations), len(values)
                ),
                "cycle_offset": cycle_offset,
                "external_offset": external_offset,
                "offset_difference": difference,
                "offset_positive": difference > 0,
                "target_count": len(target_values),
            }
        )

    cycle_indices = set(itertools.chain.from_iterable(CYCLE_PAIRS))
    external_indices = list(itertools.chain.from_iterable(EXTERNAL_PAIRS))
    return {
        "height_count": m,
        "edge_certificates": edges,
        "transversal_point_cycle_count": transversal_cycle_count(m),
        "bad_colour_multisets": sorted(bad_colour_multisets()),
        "all_k23_colourings_repair": all_k23_colourings_repair(),
        "all_external_indices_distinct": len(set(external_indices))
        == len(external_indices),
        "external_indices_disjoint_from_cycle": cycle_indices.isdisjoint(
            external_indices
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--height-count", type=int, default=14)
    args = parser.parse_args()
    certificate = build_certificate(args.height_count)
    print(
        json.dumps(
            certificate,
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
