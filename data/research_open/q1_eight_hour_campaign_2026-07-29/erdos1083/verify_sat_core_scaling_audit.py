#!/usr/bin/env python3
"""Verify scaling ledgers for the translated-Latin SAT core."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


def same_skeleton_translation_replication(
    copy_count: int,
) -> dict[str, int | bool | Fraction]:
    if copy_count <= 0:
        raise ValueError("copy_count must be positive")
    radius_class_count = 5
    base_points_per_class = 3
    base_services = 6
    base_cross_edges = 12
    base_cross_cells = 6
    height_capacity = base_points_per_class * copy_count
    service_count = base_services * copy_count
    cross_edge_count = base_cross_edges * copy_count
    # A fixed pair of base residues and a translation difference determine
    # every vertical difference on the five-class skeleton.
    full_cell_upper_bound = (
        radius_class_count**2
        * base_points_per_class**2
        * (2 * copy_count - 1)
    )
    return {
        "copy_count": copy_count,
        "radius_class_count": radius_class_count,
        "height_capacity": height_capacity,
        "service_count": service_count,
        "cross_edge_count": cross_edge_count,
        "average_cross_edge_service_occurrence": Fraction(
            2 * service_count,
            cross_edge_count,
        ),
        "distinct_visited_cross_cells": base_cross_cells,
        "maximum_visited_cell_representation": copy_count,
        "full_cell_upper_bound_on_fixed_skeleton": (
            full_cell_upper_bound
        ),
        "compatibility_degree_grows": False,
    }


def full_cross_copy_translation_replication(
    copy_count: int,
) -> dict[str, int | bool | Fraction]:
    """Use every ordered pair of translation copies on each cross edge."""
    if copy_count <= 0:
        raise ValueError("copy_count must be positive")
    height_capacity = 3 * copy_count
    service_count = 6 * copy_count**2
    cross_edge_count = 12 * copy_count**2
    visited_cross_cell_upper_bound = 12 * (2 * copy_count - 1)
    full_cell_upper_bound = 25 * 9 * (2 * copy_count - 1)
    return {
        "copy_count": copy_count,
        "height_capacity": height_capacity,
        "service_count": service_count,
        "cross_edge_count": cross_edge_count,
        "average_cross_edge_service_occurrence": Fraction(
            2 * service_count,
            cross_edge_count,
        ),
        "visited_cross_cell_upper_bound": (
            visited_cross_cell_upper_bound
        ),
        "maximum_visited_cell_representation": copy_count,
        "full_cell_upper_bound_on_fixed_skeleton": (
            full_cell_upper_bound
        ),
        "generic_translation_has_no_extra_compatibilities": True,
    }


def transcendental_translation_differences(
    difference_radius: int,
    first_base_difference: int,
    second_base_difference: int,
) -> tuple[tuple[int, int], ...]:
    """Solve the two coefficients forced by a transcendental step."""
    if difference_radius < 0:
        raise ValueError("difference_radius must be nonnegative")
    return tuple(
        (first, second)
        for first in range(
            -difference_radius,
            difference_radius + 1,
        )
        for second in range(
            -difference_radius,
            difference_radius + 1,
        )
        if (
            first**2 == second**2
            and first_base_difference * first
            == second_base_difference * second
        )
    )


def separated_layering(
    layer_count: int,
    translation_count: int,
) -> dict[str, int | Fraction]:
    if layer_count <= 0 or translation_count <= 0:
        raise ValueError("both layer parameters must be positive")
    radius_class_count = 5 * layer_count
    height_capacity = 3 * translation_count
    service_count = 6 * layer_count * translation_count**2
    cross_edge_count = 12 * layer_count * translation_count**2
    separated_full_cell_lower_bound = (
        radius_class_count
        * (radius_class_count - 1)
        // 2
        * translation_count
    )
    return {
        "layer_count": layer_count,
        "translation_count": translation_count,
        "radius_class_count": radius_class_count,
        "height_capacity": height_capacity,
        "service_count": service_count,
        "cross_edge_count": cross_edge_count,
        "average_cross_edge_service_occurrence": Fraction(
            2 * service_count,
            cross_edge_count,
        ),
        "separated_full_cell_lower_bound": (
            separated_full_cell_lower_bound
        ),
    }


def synchronized_cycle_capacity_ledger() -> dict[str, Fraction]:
    service_edges = Fraction(33, 10)
    partner_vertices = Fraction(2)
    hub_vertices = Fraction(19, 10)

    def thresholds(vertex_exponent: Fraction) -> tuple[
        Fraction,
        Fraction,
        Fraction,
    ]:
        any_cycle = service_edges - vertex_exponent
        four_cycle = service_edges - 3 * vertex_exponent / 2
        four_or_six = service_edges - 4 * vertex_exponent / 3
        return any_cycle, four_cycle, four_or_six

    partner = thresholds(partner_vertices)
    hub = thresholds(hub_vertices)
    return {
        "service_edge_exponent": service_edges,
        "partner_vertex_exponent": partner_vertices,
        "hub_vertex_exponent": hub_vertices,
        "target_compatibility_degree_exponent": Fraction(2, 5),
        "partner_palette_threshold_for_any_cycle": partner[0],
        "partner_palette_threshold_for_c4": partner[1],
        "partner_palette_threshold_for_c4_or_c6": partner[2],
        "hub_palette_threshold_for_any_cycle": hub[0],
        "hub_palette_threshold_for_c4": hub[1],
        "hub_palette_threshold_for_c4_or_c6": hub[2],
        "diagonal_copy_service_exponent": Fraction(1),
        "full_cross_copy_service_exponent": Fraction(2),
        "layered_balanced_service_exponent": Fraction(3),
        "required_service_exponent": service_edges,
        "layered_separated_cell_exponent": Fraction(3),
        "allowed_cell_exponent": Fraction(27, 10),
        "layered_cell_excess_exponent": Fraction(3, 10),
        "layered_service_deficit_exponent": Fraction(3, 10),
    }


def monochromatic_c4_capacity(
    coordinate_vertex_count: int,
    shift_pair_palette_size: int,
) -> dict[str, int]:
    """Elementary per-colour C4-free capacity, up to constants."""
    if coordinate_vertex_count <= 0 or shift_pair_palette_size <= 0:
        raise ValueError("capacity parameters must be positive")
    per_colour = (
        coordinate_vertex_count
        * int(coordinate_vertex_count**0.5)
        + coordinate_vertex_count
    )
    return {
        "coordinate_vertex_count": coordinate_vertex_count,
        "shift_pair_palette_size": shift_pair_palette_size,
        "per_colour_c4_free_capacity": per_colour,
        "total_c4_free_coloured_capacity": (
            shift_pair_palette_size * per_colour
        ),
    }


def _fraction_strings(
    values: dict[str, Fraction],
) -> dict[str, str]:
    return {key: str(value) for key, value in values.items()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--copies", type=int, default=7)
    parser.add_argument("--layers", type=int, default=5)
    args = parser.parse_args()
    output = {
        "same_skeleton": same_skeleton_translation_replication(
            args.copies
        ),
        "full_cross_copy_skeleton": (
            full_cross_copy_translation_replication(args.copies)
        ),
        "separated_layers": separated_layering(
            args.layers,
            args.copies,
        ),
        "cycle_ledger": _fraction_strings(
            synchronized_cycle_capacity_ledger()
        ),
        "finite_c4_capacity": monochromatic_c4_capacity(
            49,
            3,
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
