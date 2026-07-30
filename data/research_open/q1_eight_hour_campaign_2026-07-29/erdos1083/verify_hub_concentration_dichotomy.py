#!/usr/bin/env python3
"""Verify the hub concentration partial dichotomy."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction


def link_weight(
    sizes: dict[tuple[int, int], int],
    first: int,
    second: int,
    radius_count: int,
    height_count: int,
    selected_count: int,
) -> Fraction:
    total = Fraction(0)
    for third in range(radius_count):
        if third in (first, second):
            continue
        first_edge = tuple(sorted((first, third)))
        second_edge = tuple(sorted((second, third)))
        total += Fraction(1, sizes[first_edge] * sizes[second_edge])
    return height_count * selected_count**2 * total


def hub_vertices(
    sizes: dict[tuple[int, int], int],
    radius_count: int,
    large_threshold: int,
    minimum_large_degree: int,
) -> set[int]:
    return {
        vertex
        for vertex in range(radius_count)
        if sum(
            sizes[tuple(sorted((vertex, other)))] >= large_threshold
            for other in range(radius_count)
            if other != vertex
        )
        >= minimum_large_degree
    }


def finite_cover_certificate(radius_count: int = 20) -> dict[str, object]:
    height_count = radius_count
    selected_count = radius_count // 2
    hub = {0, 1, 2}
    small_size = radius_count
    large_size = radius_count**2
    sizes = {
        edge: (
            large_size
            if edge[0] in hub or edge[1] in hub
            else small_size
        )
        for edge in itertools.combinations(range(radius_count), 2)
    }
    detected_hubs = hub_vertices(
        sizes,
        radius_count,
        large_threshold=large_size,
        minimum_large_degree=radius_count // 2,
    )
    weights = {
        edge: link_weight(
            sizes,
            *edge,
            radius_count,
            height_count,
            selected_count,
        )
        for edge in sizes
    }
    maximum_hub_pair_weight = max(
        weight
        for edge, weight in weights.items()
        if edge[0] in hub and edge[1] in hub
    )
    minimum_outside_pair_weight = min(
        weight
        for edge, weight in weights.items()
        if edge[0] not in hub and edge[1] not in hub
    )
    cutoff = (
        maximum_hub_pair_weight + minimum_outside_pair_weight
    ) / 2
    low_edges = {edge for edge, weight in weights.items() if weight < cutoff}
    return {
        "radius_count": radius_count,
        "declared_hubs": sorted(hub),
        "detected_hubs": sorted(detected_hubs),
        "low_edge_count": len(low_edges),
        "all_low_edges_covered": all(
            edge[0] in detected_hubs or edge[1] in detected_hubs
            for edge in low_edges
        ),
        "maximum_hub_pair_weight": maximum_hub_pair_weight,
        "minimum_outside_pair_weight": minimum_outside_pair_weight,
        "cutoff": cutoff,
    }


def exponent_ledger(
    eta_numerator: int, eta_denominator: int
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    target_link = Fraction(1, 3) + 2 * eta
    large_threshold = Fraction(11, 6) - eta
    overlap_mass = Fraction(10, 3) - eta
    hub_upper = Fraction(5, 6) + 2 * eta
    hub_lower = Fraction(2, 3) - eta / 2
    line_alternative = hub_lower + large_threshold
    line_target = Fraction(8, 3) + eta
    return {
        "eta": eta,
        "target_link": target_link,
        "large_threshold": large_threshold,
        "link_from_two_small_blocks": (
            4 - 2 * large_threshold
        ),
        "overlap_mass": overlap_mass,
        "hub_upper": hub_upper,
        "hub_lower": hub_lower,
        "low_overlap_capacity": 2 * hub_lower + 2,
        "line_alternative": line_alternative,
        "line_target": line_target,
        "residual_gap": line_target - line_alternative,
        "required_hub_for_target": line_target - large_threshold,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    args = parser.parse_args()
    result = {
        "finite_cover": finite_cover_certificate(),
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
