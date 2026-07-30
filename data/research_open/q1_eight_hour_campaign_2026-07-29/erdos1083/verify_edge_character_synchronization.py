#!/usr/bin/env python3
"""Verify the edge-character synchronization audit."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction


ORIGINAL_TO_EXTERNAL = {
    (0, 4): (1, 3),
    (4, 8): (5, 7),
    (0, 8): (2, 6),
    (8, 19): (13, 14),
    (4, 19): (11, 12),
    (0, 19): (9, 10),
}

EDGE_QUOTIENTS = {
    (0, 4): (7, 1),
    (4, 8): (14, 1),
    (8, 19): (21, 1),
    (0, 19): (28, 2),
    (0, 8): (5, 1),
    (4, 19): (9, 1),
}

CYCLE = ((0, 4), (4, 8), (8, 19), (0, 19))


def radial_offset(pair: tuple[int, int]) -> int:
    left, right = pair
    return (2**left - 2**right) ** 2


def selected_value_count(m: int, modulus: int, colour: int) -> int:
    if m % modulus:
        raise ValueError("m must be divisible by the edge modulus")
    if colour % modulus in (0, modulus - colour % modulus):
        raise ValueError("the two symmetric residues must be distinct")
    return 2 * m // modulus


def representation_count(m: int, modulus: int, colour: int) -> int:
    selected_value_count(m, modulus, colour)
    return 2 * m * m // modulus


def selected_relation(
    left: int, right: int, modulus: int, colour: int
) -> bool:
    difference = (left - right) % modulus
    return difference in {colour % modulus, (-colour) % modulus}


def transversal_cycle_count(m: int) -> int:
    adjacency = {}
    for edge in CYCLE:
        modulus, colour = EDGE_QUOTIENTS[edge]
        adjacency[edge] = {
            left: [
                right
                for right in range(m)
                if selected_relation(left, right, modulus, colour)
            ]
            for left in range(m)
        }

    count = 0
    final_modulus, final_colour = EDGE_QUOTIENTS[(0, 19)]
    for z0 in range(m):
        for z4 in adjacency[(0, 4)][z0]:
            for z8 in adjacency[(4, 8)][z4]:
                for z19 in adjacency[(8, 19)][z8]:
                    if selected_relation(
                        z0, z19, final_modulus, final_colour
                    ):
                        count += 1
    return count


def gram_identity(heights: tuple[int, int, int, int]) -> bool:
    def squared_difference(first: int, second: int) -> int:
        return (heights[first] - heights[second]) ** 2

    a01 = squared_difference(0, 1)
    a02 = squared_difference(0, 2)
    a03 = squared_difference(0, 3)
    a12 = squared_difference(1, 2)
    a13 = squared_difference(1, 3)
    a23 = squared_difference(2, 3)
    g12 = Fraction(a01 + a02 - a12, 2)
    g13 = Fraction(a01 + a03 - a13, 2)
    g23 = Fraction(a02 + a03 - a23, 2)
    return g12 * g13 * g23 == a01 * a02 * a03


def reconstruct_potentials(
    vertices: tuple[int, ...],
    edge_labels: dict[tuple[int, int], int],
    modulus: int,
    root: int,
) -> dict[int, int]:
    def label(left: int, right: int) -> int:
        if left < right:
            return edge_labels[(left, right)] % modulus
        return -edge_labels[(right, left)] % modulus

    potentials = {root: 0}
    for vertex in vertices:
        if vertex != root:
            potentials[vertex] = label(vertex, root)
    return potentials


def potential_disagreements(
    vertices: tuple[int, ...],
    edge_labels: dict[tuple[int, int], int],
    potentials: dict[int, int],
    modulus: int,
) -> int:
    return sum(
        edge_labels[(left, right)] % modulus
        != (potentials[left] - potentials[right]) % modulus
        for left, right in itertools.combinations(vertices, 2)
    )


def build_certificate(m: int) -> dict[str, object]:
    if m % 1260:
        raise ValueError("m must be divisible by 1260")

    edge_certificates = []
    for original, external in ORIGINAL_TO_EXTERNAL.items():
        modulus, colour = EDGE_QUOTIENTS[original]
        original_offset = radial_offset(original)
        external_offset = radial_offset(external)
        values = selected_value_count(m, modulus, colour)
        representations = representation_count(m, modulus, colour)
        edge_certificates.append(
            {
                "original_pair": original,
                "external_pair": external,
                "common_sum": sum(original),
                "modulus": modulus,
                "colour": colour,
                "selected_value_count": values,
                "representation_count": representations,
                "average_representation_multiplicity": Fraction(
                    representations, values
                ),
                "offset_difference": original_offset - external_offset,
            }
        )

    external_indices = list(
        itertools.chain.from_iterable(ORIGINAL_TO_EXTERNAL.values())
    )
    moduli = [modulus for modulus, _ in EDGE_QUOTIENTS.values()]
    return {
        "height_count": m,
        "edge_certificates": edge_certificates,
        "all_external_indices_distinct": len(external_indices)
        == len(set(external_indices)),
        "external_indices_disjoint_from_original": set(
            itertools.chain.from_iterable(ORIGINAL_TO_EXTERNAL)
        ).isdisjoint(external_indices),
        "moduli_gcd": math.gcd(*moduli),
        "transversal_cycle_count_mod_84": transversal_cycle_count(84),
        "gram_identity_exhaustive_on_range_0_4": all(
            gram_identity(heights)
            for heights in itertools.product(range(5), repeat=4)
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--height-count", type=int, default=1260)
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
