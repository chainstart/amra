#!/usr/bin/env python3
"""Verify the global hyperbola-network reuse lemma and tensor model."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from fractions import Fraction


Vector = tuple[int, ...]
CoreSymbol = tuple[int, Vector, int]


def add_scaled(
    point: Vector, direction: Vector, scalar: int, modulus: int
) -> Vector:
    return tuple(
        (coordinate + scalar * step) % modulus
        for coordinate, step in zip(point, direction)
    )


def canonical_line(
    point: Vector, direction: Vector, modulus: int
) -> Vector:
    return min(
        add_scaled(point, direction, scalar, modulus)
        for scalar in range(modulus)
    )


def affine_tensor(
    modulus: int = 2, dimension: int = 4
) -> dict[str, object]:
    if dimension % 2:
        raise ValueError("the finite verifier uses an even dimension")
    vertices = tuple(itertools.product(range(modulus), repeat=dimension))
    line_size = modulus
    direction_count = modulus ** (dimension // 2 - 1)
    directions = tuple(
        tuple(
            1 if coordinate == index else 0
            for coordinate in range(dimension)
        )
        for index in range(direction_count)
    )
    core_size = modulus ** (dimension // 2 + 1)

    blocks: dict[Vector, set[CoreSymbol]] = {}
    for vertex in vertices:
        symbols: set[CoreSymbol] = set()
        for direction_index, direction in enumerate(directions):
            line = canonical_line(vertex, direction, modulus)
            symbols.update(
                (direction_index, line, symbol)
                for symbol in range(core_size)
            )
        blocks[vertex] = symbols

    multiplicities = Counter(
        symbol for block in blocks.values() for symbol in block
    )
    overlaps = {
        (first, second): len(blocks[first] & blocks[second])
        for first, second in itertools.combinations(vertices, 2)
    }
    strong_edges = {
        edge: overlap for edge, overlap in overlaps.items() if overlap
    }
    total_incidence = sum(map(len, blocks.values()))
    union_size = len(multiplicities)
    correlation = sum(
        multiplicity * (multiplicity - 1) // 2
        for multiplicity in multiplicities.values()
    )
    degrees = Counter()
    for first, second in strong_edges:
        degrees[first] += 1
        degrees[second] += 1

    maximum_multiplicity = max(multiplicities.values())
    weighted_overlap = sum(strong_edges.values())
    return {
        "modulus": modulus,
        "dimension": dimension,
        "block_count": len(vertices),
        "line_size": line_size,
        "direction_count": direction_count,
        "core_size": core_size,
        "block_sizes": sorted(set(map(len, blocks.values()))),
        "union_size": union_size,
        "total_incidence": total_incidence,
        "strong_edge_count": len(strong_edges),
        "strong_overlap_sizes": sorted(set(strong_edges.values())),
        "strong_degrees": sorted(set(degrees.values())),
        "symbol_multiplicities": sorted(set(multiplicities.values())),
        "correlation": correlation,
        "weighted_overlap": weighted_overlap,
        "maximum_multiplicity": maximum_multiplicity,
        "reuse_lower_bound": Fraction(
            2 * weighted_overlap, total_incidence
        )
        + 1,
    }


def exponent_ledger(dimension: int) -> dict[str, Fraction]:
    d = Fraction(dimension, 1)
    eta = Fraction(1, 3) - 1 / d
    h = 1 / d
    g = Fraction(1, 2) - 1 / d
    overlap = Fraction(1, 2) + 1 / d
    return {
        "eta": eta,
        "common_multiplicity": h,
        "directions": g,
        "strong_overlap": overlap,
        "block_size": g + overlap,
        "strong_degree": g + h,
        "block_count": Fraction(2),
        "total_incidence": Fraction(3),
        "union": Fraction(3) - h,
        "target_union": Fraction(8, 3) + eta,
        "correlation": Fraction(3) + h,
        "forced_correlation": Fraction(10, 3) - eta,
        "strong_edges": Fraction(2) + g + h,
        "propagation_target": Fraction(2, 3) + eta,
        "reuse_gap": Fraction(1, 3) + 2 * eta,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modulus", type=int, default=2)
    parser.add_argument("--dimension", type=int, default=4)
    args = parser.parse_args()
    result = {
        "finite_tensor": affine_tensor(args.modulus, args.dimension),
        "exponent_ledger": exponent_ledger(args.dimension),
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
