#!/usr/bin/env python3
"""Exact certificates for the network inverse barrier."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class HadamardCertificate:
    dimension: int
    universe_size: int
    block_size: int
    block_count: int
    union_size: int
    minimum_intersection: int
    maximum_intersection: int
    minimum_symmetric_difference: int
    maximum_symmetric_difference: int
    correlation_edge_count: int
    four_cycle_count: int
    lacunary_union_additive_energy: int
    minimum_possible_energy_formula: int


def parity(number: int) -> int:
    return number.bit_count() & 1


def hadamard_blocks(dimension: int) -> tuple[frozenset[int], ...]:
    if dimension < 2:
        raise ValueError("need dimension >= 2")
    universe_size = 1 << dimension
    return tuple(
        frozenset(
            value
            for value in range(universe_size)
            if parity(mask & value) == 0
        )
        for mask in range(1, universe_size)
    )


def four_cycle_count_complete_graph(vertex_count: int) -> int:
    # Every four vertices support three distinct undirected 4-cycles.
    return 3 * math.comb(vertex_count, 4)


def additive_energy(values: set[int]) -> int:
    multiplicities: dict[int, int] = {}
    for left in values:
        for right in values:
            total = left + right
            multiplicities[total] = multiplicities.get(total, 0) + 1
    return sum(count * count for count in multiplicities.values())


def hadamard_certificate(dimension: int) -> HadamardCertificate:
    blocks = hadamard_blocks(dimension)
    intersections = []
    symmetric_differences = []
    for first in range(len(blocks)):
        for second in range(first + 1, len(blocks)):
            intersections.append(len(blocks[first] & blocks[second]))
            symmetric_differences.append(
                len(blocks[first] ^ blocks[second])
            )
    return HadamardCertificate(
        dimension=dimension,
        universe_size=1 << dimension,
        block_size=len(blocks[0]),
        block_count=len(blocks),
        union_size=len(set().union(*blocks)),
        minimum_intersection=min(intersections),
        maximum_intersection=max(intersections),
        minimum_symmetric_difference=min(symmetric_differences),
        maximum_symmetric_difference=max(symmetric_differences),
        correlation_edge_count=math.comb(len(blocks), 2),
        four_cycle_count=four_cycle_count_complete_graph(len(blocks)),
        lacunary_union_additive_energy=additive_energy(
            {3**index for index in range(1 << dimension)}
        ),
        minimum_possible_energy_formula=(
            2 * (1 << dimension) ** 2 - (1 << dimension)
        ),
    )


def dyadic_extraction(weights: list[int]) -> tuple[int, int, int]:
    """Return threshold, qualifying edge count, and weighted mass."""

    if not weights or min(weights) < 0:
        raise ValueError("need a nonempty list of nonnegative weights")
    maximum = max(weights)
    if maximum == 0:
        return 1, 0, 0
    best_threshold = 1
    best_count = 0
    best_product = 0
    threshold = 1
    while threshold <= maximum:
        count = sum(weight >= threshold for weight in weights)
        product = threshold * count
        if product > best_product:
            best_threshold = threshold
            best_count = count
            best_product = product
        threshold *= 2
    return best_threshold, best_count, best_product


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, default=5)
    args = parser.parse_args()
    certificate = hadamard_certificate(args.dimension)
    weight = certificate.block_size // 2
    weights = [weight] * certificate.correlation_edge_count
    threshold, edge_count, product = dyadic_extraction(weights)
    payload = {
        "hadamard": asdict(certificate),
        "dyadic_extraction": {
            "total_weight": sum(weights),
            "threshold": threshold,
            "edge_count": edge_count,
            "threshold_times_edges": product,
            "scale_count": 1 + math.ceil(math.log2(max(weights))),
            "inequality_verified": (
                product * (1 + math.ceil(math.log2(max(weights))))
                >= sum(weights)
            ),
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
