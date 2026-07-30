#!/usr/bin/env python3
"""Verify Gram-service pairing constraints and the Latin lift obstruction."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations


CrossEdge = tuple[int, int, int, int]


def radial_offset(first: int, second: int, ratio: int) -> int:
    return (ratio**first - ratio**second) ** 2


def same_product_radial_gap(
    hub_index: int,
    partner_index: int,
    delta: int,
    ratio: int,
) -> dict[str, int | bool]:
    direct = (
        radial_offset(
            hub_index,
            partner_index + delta,
            ratio,
        )
        - radial_offset(
            hub_index + delta,
            partner_index,
            ratio,
        )
    )
    factored = (
        (ratio ** (2 * delta) - 1)
        * (
            ratio ** (2 * partner_index)
            - ratio ** (2 * hub_index)
        )
    )
    return {
        "direct_gap": direct,
        "factored_gap": factored,
        "factorization_holds": direct == factored,
    }


def required_partner_shift(
    first_cross_shift: Fraction,
    second_cross_shift: Fraction,
    first_original_offset: int,
    second_original_offset: int,
) -> Fraction | None:
    denominator = 2 * (
        first_cross_shift + second_cross_shift
    )
    if denominator == 0:
        return None
    return Fraction(
        second_original_offset
        - first_original_offset
        - first_cross_shift**2
        + second_cross_shift**2,
        denominator,
    )


def service_pair_certificate(
    first_cross_edge: CrossEdge,
    second_cross_edge: CrossEdge,
    ratio: int,
) -> dict[str, object]:
    """Check whether two cross edges are the opposite sides of a service."""
    hub_first, height_first, partner_second, height_second = (
        first_cross_edge
    )
    hub_second, height_hub_second, partner_first, height_partner_first = (
        second_cross_edge
    )
    radius_diagonal_first = hub_first - partner_second
    radius_diagonal_second = hub_second - partner_first
    same_radius_diagonal = (
        radius_diagonal_first == radius_diagonal_second
    )
    first_cross_shift = Fraction(height_first - height_second)
    second_cross_shift = Fraction(
        height_hub_second - height_partner_first
    )
    partner_shift = Fraction(height_second - height_partner_first)
    first_original_offset = radial_offset(
        hub_first,
        partner_first,
        ratio,
    )
    second_original_offset = radial_offset(
        hub_second,
        partner_second,
        ratio,
    )
    first_original_value = (
        first_original_offset
        + (first_cross_shift + partner_shift) ** 2
    )
    second_original_value = (
        second_original_offset
        + (second_cross_shift - partner_shift) ** 2
    )
    required_shift = required_partner_shift(
        first_cross_shift,
        second_cross_shift,
        first_original_offset,
        second_original_offset,
    )
    degenerate_shift_sum = (
        first_cross_shift + second_cross_shift == 0
    )
    return {
        "same_radius_diagonal": same_radius_diagonal,
        "first_cross_product": hub_first + partner_second,
        "second_cross_product": hub_second + partner_first,
        "cross_products_have_same_parity": (
            (hub_first + partner_second - hub_second - partner_first)
            % 2
            == 0
        ),
        "original_product_first": hub_first + partner_first,
        "original_product_second": hub_second + partner_second,
        "first_cross_shift": first_cross_shift,
        "second_cross_shift": second_cross_shift,
        "partner_shift": partner_shift,
        "required_partner_shift": required_shift,
        "degenerate_shift_sum": degenerate_shift_sum,
        "diagonal_offsets_equal": (
            first_original_offset == second_original_offset
        ),
        "original_distance_first": first_original_value,
        "original_distance_second": second_original_value,
        "is_service": (
            same_radius_diagonal
            and first_original_value == second_original_value
        ),
    }


def paired_service_fan(
    length: int,
    ratio: int = 2,
) -> dict[str, object]:
    """Realize the sharp m-service fibre for two paired cross cells."""
    hub_first, partner_second = 0, 5
    hub_second, partner_first = 1, 6
    first_cross_shift = Fraction(1)
    second_cross_shift = Fraction(2)
    first_original_offset = radial_offset(
        hub_first,
        partner_first,
        ratio,
    )
    second_original_offset = radial_offset(
        hub_second,
        partner_second,
        ratio,
    )
    partner_shift = required_partner_shift(
        first_cross_shift,
        second_cross_shift,
        first_original_offset,
        second_original_offset,
    )
    if partner_shift is None:
        raise AssertionError("the chosen fan must be nondegenerate")

    services = []
    cross_cells = Counter()
    for index in range(length):
        partner_first_height = Fraction(10 * index)
        partner_second_height = (
            partner_first_height + partner_shift
        )
        hub_first_height = (
            partner_second_height + first_cross_shift
        )
        hub_second_height = (
            partner_first_height + second_cross_shift
        )
        first_edge = (
            hub_first,
            hub_first_height,
            partner_second,
            partner_second_height,
        )
        second_edge = (
            hub_second,
            hub_second_height,
            partner_first,
            partner_first_height,
        )
        certificate = service_pair_certificate(
            first_edge,
            second_edge,
            ratio,
        )
        services.append(certificate)
        first_cell = (
            hub_first + partner_second,
            radial_offset(
                hub_first,
                partner_second,
                ratio,
            )
            + first_cross_shift**2,
        )
        second_cell = (
            hub_second + partner_first,
            radial_offset(
                hub_second,
                partner_first,
                ratio,
            )
            + second_cross_shift**2,
        )
        cross_cells[first_cell] += 1
        cross_cells[second_cell] += 1

    return {
        "length": length,
        "partner_shift": partner_shift,
        "service_count": len(services),
        "all_services_valid": all(
            certificate["is_service"] for certificate in services
        ),
        "distinct_cross_cells": len(cross_cells),
        "cross_cell_multiplicities": tuple(
            sorted(cross_cells.values())
        ),
        "height_capacity_per_class": length,
        "paired_type_multiplicity_bound_is_sharp": (
            len(services) == length
        ),
    }


def latin_edges(
    field_order: int,
    hub_group_count: int,
    ratio: int,
) -> tuple[tuple[CrossEdge, ...], int]:
    if any(
        field_order % divisor == 0
        for divisor in range(2, int(field_order**0.5) + 1)
    ):
        raise ValueError("this verifier implements prime fields only")
    partner_radius_offset = field_order + 2
    edges = []
    for slope in range(field_order):
        partner_radius = partner_radius_offset + slope
        for intercept in range(field_order):
            for hub_radius in range(hub_group_count):
                hub_height = (
                    slope * hub_radius + intercept
                ) % field_order
                edges.append(
                    (
                        hub_radius,
                        hub_height,
                        partner_radius,
                        intercept,
                    )
                )
    return tuple(edges), partner_radius_offset


def latin_service_lift_audit(
    field_order: int,
    hub_group_count: int,
    ratio: int | None = None,
) -> dict[str, object]:
    """Show that the unshifted real Latin model has no nontrivial service."""
    if ratio is None:
        ratio = 10 * field_order
    edges, partner_radius_offset = latin_edges(
        field_order,
        hub_group_count,
        ratio,
    )
    diagonal_buckets: dict[int, list[CrossEdge]] = {}
    for edge in edges:
        diagonal_buckets.setdefault(edge[0] - edge[2], []).append(edge)

    candidate_edge_pairs = 0
    compatible_nontrivial_services = 0
    minimum_radial_gap: int | None = None
    minimum_gap_data: tuple[int, int, int] | None = None
    block_pairs: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for bucket in diagonal_buckets.values():
        for first_edge, second_edge in combinations(bucket, 2):
            first_block = (first_edge[0], first_edge[2])
            second_block = (second_edge[0], second_edge[2])
            if first_block == second_block:
                continue
            ordered_blocks = tuple(sorted((first_block, second_block)))
            block_pairs.add(ordered_blocks)
            candidate_edge_pairs += 1
            certificate = service_pair_certificate(
                first_edge,
                second_edge,
                ratio,
            )
            compatible_nontrivial_services += certificate["is_service"]

    for first_block, second_block in block_pairs:
        hub_first, partner_second = first_block
        hub_second, partner_first = second_block
        first_offset = radial_offset(
            hub_first,
            partner_first,
            ratio,
        )
        second_offset = radial_offset(
            hub_second,
            partner_second,
            ratio,
        )
        gap = abs(first_offset - second_offset)
        if minimum_radial_gap is None or gap < minimum_radial_gap:
            minimum_radial_gap = gap
            minimum_gap_data = (
                abs(hub_second - hub_first),
                min(partner_first, partner_second),
                min(hub_first, hub_second),
            )

    height_diameter = field_order - 1
    return {
        "field_order": field_order,
        "hub_group_count": hub_group_count,
        "ratio": ratio,
        "edge_count": len(edges),
        "radius_diagonal_count": len(diagonal_buckets),
        "distinct_nontrivial_block_pairs": len(block_pairs),
        "candidate_edge_pairs": candidate_edge_pairs,
        "compatible_nontrivial_services": (
            compatible_nontrivial_services
        ),
        "unshifted_latin_cannot_lift": (
            compatible_nontrivial_services == 0
        ),
        "height_diameter": height_diameter,
        "height_square_range": height_diameter**2,
        "minimum_radial_gap": minimum_radial_gap,
        "minimum_gap_exceeds_height_square_range": (
            minimum_radial_gap is not None
            and minimum_radial_gap > height_diameter**2
        ),
        "minimum_gap_data": minimum_gap_data,
        "partner_radius_offset": partner_radius_offset,
    }


def exponent_ledger(
    eta_numerator: int,
    eta_denominator: int,
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    height_capacity = Fraction(1)
    hub_classes = Fraction(5, 6) + 2 * eta
    service_mass = Fraction(10, 3) - eta
    distinct_cross_edges = Fraction(3) - 3 * eta
    target_point_moment = Fraction(11, 3) + eta
    paired_type_minimum = service_mass - height_capacity
    available_diagonal_block_pairs = 1 + 2 * hub_classes
    return {
        "eta": eta,
        "height_capacity_exponent": height_capacity,
        "hub_class_exponent": hub_classes,
        "service_mass_exponent": service_mass,
        "distinct_cross_edge_exponent": distinct_cross_edges,
        "average_service_occurrences_per_cross_edge_exponent": (
            service_mass - distinct_cross_edges
        ),
        "point_moment_from_exact_edge_saturation_exponent": (
            2 * service_mass - distinct_cross_edges
        ),
        "target_point_moment_exponent": target_point_moment,
        "minimum_paired_signed_type_exponent": paired_type_minimum,
        "available_same_diagonal_block_pair_exponent": (
            available_diagonal_block_pairs
        ),
        "block_pair_capacity_slack_exponent": (
            available_diagonal_block_pairs - paired_type_minimum
        ),
        "partner_projection_average_degree_exponent": (
            service_mass - 2
        ),
        "hub_projection_average_degree_exponent": (
            service_mass - (1 + hub_classes)
        ),
    }


def _json_ready(value: object) -> object:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--field-order", type=int, default=7)
    parser.add_argument("--hub-groups", type=int, default=4)
    args = parser.parse_args()
    output = {
        "paired_service_fan": paired_service_fan(args.field_order),
        "latin_lift_audit": latin_service_lift_audit(
            args.field_order,
            args.hub_groups,
        ),
        "eta_ledger": exponent_ledger(1, 30),
    }
    print(json.dumps(_json_ready(output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
