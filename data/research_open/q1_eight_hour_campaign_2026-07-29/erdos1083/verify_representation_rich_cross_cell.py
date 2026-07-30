#!/usr/bin/env python3
"""Verify one-cell translation rulings and the global capacity ledger."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


def exponent_ledger(
    eta_numerator: int, eta_denominator: int
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    rich_cell = Fraction(1, 3) - 4 * eta
    minimum_hub = Fraction(2, 3) - eta / 2
    maximum_hub = Fraction(5, 6) + 2 * eta
    union = Fraction(8, 3) + eta
    representation_edges = union + rich_cell
    service = Fraction(10, 3) - eta
    point_moment_target = Fraction(11, 3) + eta
    forced_edges = 2 * service - point_moment_target
    forced_hub = forced_edges - 2
    return {
        "eta": eta,
        "rich_cell_exponent": rich_cell,
        "minimum_hub_exponent": minimum_hub,
        "maximum_hub_exponent": maximum_hub,
        "rich_cell_to_hub_ratio_exponent": rich_cell - minimum_hub,
        "union_exponent": union,
        "all_rich_representation_edge_exponent": representation_edges,
        "coordinate_vertex_exponent": Fraction(2),
        "c4_edge_threshold_exponent": Fraction(3),
        "c4_threshold_deficit_exponent": (
            Fraction(3) - representation_edges
        ),
        "forced_edge_exponent_if_point_moment_fails": forced_edges,
        "forced_hub_exponent_in_c4_free_branch": forced_hub,
        "forced_hub_surplus_over_upper_bound": (
            forced_hub - maximum_hub
        ),
        "required_labelled_cycle_gain_exponent": (
            Fraction(1, 3) + 2 * eta
        ),
    }


def bipartite_c4_certificate(
    hub_vertex_count: int,
    partner_vertex_count: int,
    edges: tuple[tuple[int, int], ...],
) -> dict[str, int | bool]:
    neighbours = {
        partner: set() for partner in range(partner_vertex_count)
    }
    for hub, partner in set(edges):
        if not 0 <= hub < hub_vertex_count:
            raise ValueError("hub endpoint is outside the vertex set")
        if not 0 <= partner < partner_vertex_count:
            raise ValueError("partner endpoint is outside the vertex set")
        neighbours[partner].add(hub)
    common_partner_counts: dict[tuple[int, int], int] = {}
    for hub_neighbours in neighbours.values():
        ordered = sorted(hub_neighbours)
        for first_index, first in enumerate(ordered):
            for second in ordered[first_index + 1 :]:
                pair = (first, second)
                common_partner_counts[pair] = (
                    common_partner_counts.get(pair, 0) + 1
                )
    c4_count = sum(
        count * (count - 1) // 2
        for count in common_partner_counts.values()
    )
    edge_count = len(set(edges))
    excess = max(edge_count - partner_vertex_count, 0)
    return {
        "hub_vertex_count": hub_vertex_count,
        "partner_vertex_count": partner_vertex_count,
        "edge_count": edge_count,
        "c4_count": c4_count,
        "is_c4_free": c4_count == 0,
        "c4_free_kst_squared_holds": (
            c4_count > 0
            or excess**2
            <= hub_vertex_count**2 * partner_vertex_count
        ),
    }


def fan_profile(
    signed_counts: tuple[tuple[int, int], ...]
) -> dict[str, Fraction | int | bool]:
    flat_counts = [
        count
        for pair in signed_counts
        for count in pair
        if count > 0
    ]
    active_block_count = sum(
        first + second > 0 for first, second in signed_counts
    )
    representation_count = sum(flat_counts)
    fan_energy = sum(count**2 for count in flat_counts)
    maximum_ruling = max(flat_counts, default=0)
    channel_count = len(flat_counts)
    return {
        "active_block_count": active_block_count,
        "signed_channel_count": channel_count,
        "representation_count": representation_count,
        "fan_energy": fan_energy,
        "maximum_ruling": maximum_ruling,
        "energy_lower_bound": (
            Fraction(representation_count**2, 2 * active_block_count)
            if active_block_count
            else Fraction(0)
        ),
        "maximum_lower_bound": (
            Fraction(representation_count, 2 * active_block_count)
            if active_block_count
            else Fraction(0)
        ),
        "energy_bound_holds": (
            not active_block_count
            or fan_energy * 2 * active_block_count
            >= representation_count**2
        ),
        "maximum_bound_holds": (
            not active_block_count
            or maximum_ruling * 2 * active_block_count
            >= representation_count
        ),
    }


def radial_offset(first: int, second: int, ratio: int = 2) -> int:
    return (ratio**first - ratio**second) ** 2


def one_cell_certificate(
    product_index: int,
    signed_counts: tuple[tuple[int, int], ...],
    height_capacity: int,
    ratio: int = 2,
) -> dict[str, object]:
    block_count = len(signed_counts)
    pairs = tuple(
        (index, product_index - index)
        for index in range(block_count)
    )
    all_indices = [
        index for pair in pairs for index in pair
    ]
    if len(set(all_indices)) != len(all_indices):
        raise ValueError("the selected radius blocks must be a matching")
    if any(sum(counts) > height_capacity for counts in signed_counts):
        raise ValueError("one block exceeds its height capacity")

    offsets = tuple(
        radial_offset(first, second, ratio)
        for first, second in pairs
    )
    target_value = max(offsets) + 101
    channels = []
    for pair, offset, counts in zip(
        pairs, offsets, signed_counts, strict=True
    ):
        shift_squared = target_value - offset
        for sign, count in zip((1, -1), counts, strict=True):
            channels.append(
                {
                    "radius_pair": pair,
                    "sign": sign,
                    "count": count,
                    "shift_squared": shift_squared,
                    "verified_cell_value": offset + shift_squared,
                }
            )

    semialgebraic_checks = []
    radial_product = ratio**product_index
    for (first, second), offset in zip(pairs, offsets, strict=True):
        first_radius = Fraction(ratio**first)
        second_radius = Fraction(ratio**second)
        midpoint_radius = (first_radius + second_radius) / 2
        half_radial_difference = (
            first_radius - second_radius
        ) / 2
        vertical_difference_squared = target_value - offset
        semialgebraic_checks.append(
            (
                midpoint_radius**2 - half_radial_difference**2
                == radial_product
            )
            and (
                4 * half_radial_difference**2
                + vertical_difference_squared
                == target_value
            )
        )

    profile = fan_profile(signed_counts)
    return {
        "product_index": product_index,
        "block_count": block_count,
        "radius_pairs": pairs,
        "radius_blocks_form_matching": (
            len(set(all_indices)) == len(all_indices)
        ),
        "common_radial_product": radial_product,
        "target_cell_value": target_value,
        "representation_count": profile["representation_count"],
        "maximum_height_usage": max(
            map(sum, signed_counts), default=0
        ),
        "height_capacity": height_capacity,
        "all_channels_hit_target_cell": all(
            channel["verified_cell_value"] == target_value
            for channel in channels
        ),
        "all_shift_squares_positive": all(
            channel["shift_squared"] > 0 for channel in channels
        ),
        "all_semialgebraic_identities": all(semialgebraic_checks),
        "fan_profile": profile,
    }


def cycle_cocycle(
    oriented_shifts: tuple[Fraction, ...]
) -> dict[str, Fraction | bool]:
    total = sum(oriented_shifts, Fraction(0))
    return {
        "oriented_sum": total,
        "cycle_closes": total == 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    args = parser.parse_args()
    profile = ((3, 2), (1, 4), (2, 2), (5, 0), (0, 3))
    result = {
        "exponents": exponent_ledger(
            args.eta_numerator, args.eta_denominator
        ),
        "fan_profile": fan_profile(profile),
        "one_cell": one_cell_certificate(
            product_index=9,
            signed_counts=profile,
            height_capacity=6,
        ),
        "closing_cycle": cycle_cocycle(
            (
                Fraction(7, 3),
                Fraction(-5, 2),
                Fraction(11, 6),
                Fraction(-5, 3),
            )
        ),
        "frustrated_cycle": cycle_cocycle(
            (
                Fraction(7, 3),
                Fraction(-5, 2),
                Fraction(11, 6),
                Fraction(-4, 3),
            )
        ),
        "c4_free_graph": bipartite_c4_certificate(
            3,
            3,
            ((0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (0, 2)),
        ),
        "rectangle_graph": bipartite_c4_certificate(
            2,
            2,
            ((0, 0), (0, 1), (1, 0), (1, 1)),
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
