#!/usr/bin/env python3
"""Verify weighted labelled-C4 fibres and sharp obstruction models."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import prod


Edge = tuple[int, int]
Shift = tuple[int, int, int, int]


def difference_counts(values: tuple[int, ...]) -> Counter[int]:
    return Counter(first - second for first in values for second in values)


def additive_energy(values: tuple[int, ...]) -> int:
    counts = difference_counts(values)
    return sum(count**2 for count in counts.values())


def edge_shift_counts(edges: set[Edge]) -> Counter[int]:
    return Counter(first - second for first, second in edges)


def marginal_cocycle_energy(
    first: Counter[int],
    second: Counter[int],
    third: Counter[int],
    fourth: Counter[int],
) -> int:
    """Count compatible independent edge choices after endpoint forgetting."""
    energy = 0
    for shift_first, count_first in first.items():
        for shift_second, count_second in second.items():
            for shift_third, count_third in third.items():
                shift_fourth = (
                    shift_first - shift_second + shift_third
                )
                energy += (
                    count_first
                    * count_second
                    * count_third
                    * fourth[shift_fourth]
                )
    return energy


def weighted_cycle_statistics(
    height_sets: tuple[tuple[int, ...], ...],
    edge_sets: tuple[set[Edge], ...],
) -> dict[str, object]:
    """Partition actual C4s by their four signed edge differences."""
    if len(height_sets) != 4 or len(edge_sets) != 4:
        raise ValueError("exactly four height and edge sets are required")
    first_hubs, first_partners, second_hubs, second_partners = (
        height_sets
    )
    edge_01, edge_21, edge_23, edge_03 = edge_sets
    fibres: Counter[Shift] = Counter()
    for hub_first, hub_second, partner_first, partner_second in product(
        first_hubs,
        second_hubs,
        first_partners,
        second_partners,
    ):
        if (
            (hub_first, partner_first) not in edge_01
            or (hub_second, partner_first) not in edge_21
            or (hub_second, partner_second) not in edge_23
            or (hub_first, partner_second) not in edge_03
        ):
            continue
        shift = (
            hub_first - partner_first,
            hub_second - partner_first,
            hub_second - partner_second,
            hub_first - partner_second,
        )
        if shift[0] - shift[1] + shift[2] - shift[3] != 0:
            raise AssertionError("an actual rectangle violated the cocycle")
        fibres[shift] += 1

    cycle_count = sum(fibres.values())
    fibre_second_moment = sum(count**2 for count in fibres.values())
    occupied_fibres = len(fibres)
    maximum_fibre = max(fibres.values(), default=0)
    maximum_height_capacity = max(map(len, height_sets), default=0)

    difference_counters = tuple(
        difference_counts(values) for values in height_sets
    )
    common_nonzero_difference_energy = sum(
        prod(
            difference_counter[shift]
            for difference_counter in difference_counters
        )
        for shift in set.intersection(
            *(set(counter) for counter in difference_counters)
        )
        if shift != 0
    )
    additive_energies = tuple(
        sum(count**2 for count in counter.values())
        for counter in difference_counters
    )
    maximum_additive_energy = max(additive_energies, default=0)
    excess_fibre_moment = fibre_second_moment - cycle_count
    energy_upper_bound = (
        maximum_height_capacity**2 * maximum_additive_energy
    )

    marginal_counts = tuple(
        edge_shift_counts(edges) for edges in edge_sets
    )
    marginal_energy = marginal_cocycle_energy(*marginal_counts)
    return {
        "cycle_count": cycle_count,
        "occupied_signed_fibres": occupied_fibres,
        "maximum_signed_fibre": maximum_fibre,
        "fibre_second_moment": fibre_second_moment,
        "excess_fibre_moment": excess_fibre_moment,
        "cauchy_fibre_lower_bound": (
            Fraction(cycle_count**2, occupied_fibres)
            if occupied_fibres
            else Fraction(0)
        ),
        "common_nonzero_difference_energy": (
            common_nonzero_difference_energy
        ),
        "additive_energies": additive_energies,
        "maximum_additive_energy": maximum_additive_energy,
        "maximum_height_capacity": maximum_height_capacity,
        "energy_upper_bound": energy_upper_bound,
        "fibre_collision_injection_holds": (
            excess_fibre_moment
            <= common_nonzero_difference_energy
        ),
        "additive_energy_bound_holds": (
            common_nonzero_difference_energy <= energy_upper_bound
        ),
        "marginal_cocycle_energy": marginal_energy,
        "actual_cycles_bounded_by_marginal_energy": (
            cycle_count <= marginal_energy
        ),
    }


def complete_ap_model(length: int) -> dict[str, object]:
    values = tuple(range(length))
    complete = {(first, second) for first in values for second in values}
    return weighted_cycle_statistics(
        (values, values, values, values),
        (complete, complete, complete, complete),
    )


def translation_fan_model(length: int) -> dict[str, object]:
    """Make one large label fibre over a minimum-energy height set."""
    base = tuple(2**index for index in range(length))
    offsets = (0, 10**6, 3 * 10**6, 7 * 10**6)
    sets = tuple(
        tuple(value + offset for value in base)
        for offset in offsets
    )
    first_hubs, first_partners, second_hubs, second_partners = sets
    edge_sets = (
        set(zip(first_hubs, first_partners, strict=True)),
        set(zip(second_hubs, first_partners, strict=True)),
        set(zip(second_hubs, second_partners, strict=True)),
        set(zip(first_hubs, second_partners, strict=True)),
    )
    statistics = weighted_cycle_statistics(sets, edge_sets)
    statistics["base_additive_energy"] = additive_energy(base)
    statistics["minimum_energy_formula"] = 2 * length**2 - length
    return statistics


def latin_transversal_model(
    field_order: int,
    hub_group_count: int,
) -> dict[str, object]:
    """Build the affine-plane C4-free graph with real cell labels."""
    if field_order <= 1:
        raise ValueError("the field order must exceed one")
    if any(
        field_order % divisor == 0
        for divisor in range(2, int(field_order**0.5) + 1)
    ):
        raise ValueError("this verifier implements prime fields only")
    if not 1 <= hub_group_count <= field_order:
        raise ValueError("hub_group_count must lie in [1, field_order]")
    hubs = tuple(
        (group, height)
        for group in range(hub_group_count)
        for height in range(field_order)
    )
    partners = tuple(
        (slope, intercept)
        for slope in range(field_order)
        for intercept in range(field_order)
    )
    neighbours: dict[tuple[int, int], set[tuple[int, int]]] = {
        partner: set() for partner in partners
    }
    edges = set()
    cell_counts: Counter[tuple[int, int]] = Counter()
    partner_radius_offset = field_order + 2
    geometric_ratio = 10 * field_order
    for slope, intercept in partners:
        partner_index = partner_radius_offset + slope
        partner_radius = geometric_ratio**partner_index
        for group in range(hub_group_count):
            height = (slope * group + intercept) % field_order
            hub = (group, height)
            partner = (slope, intercept)
            edges.add((hub, partner))
            neighbours[partner].add(hub)
            radial_offset = (
                geometric_ratio**group - partner_radius
            ) ** 2
            vertical_difference = height - intercept
            cell = (
                group + partner_index,
                radial_offset + vertical_difference**2,
            )
            cell_counts[cell] += 1

    codegrees: Counter[tuple[tuple[int, int], tuple[int, int]]] = Counter()
    for hub_neighbours in neighbours.values():
        for first, second in combinations(sorted(hub_neighbours), 2):
            codegrees[(first, second)] += 1
    c4_count = sum(
        count * (count - 1) // 2 for count in codegrees.values()
    )
    hub_count = len(hubs)
    partner_count = len(partners)
    edge_count = len(edges)
    pair_count = hub_count * (hub_count - 1) // 2
    covered_pairs = len(codegrees)
    uncovered_pairs = pair_count - covered_pairs
    mean_degree = Fraction(edge_count, partner_count)
    degree_variance = sum(
        (Fraction(len(neighbourhood)) - mean_degree) ** 2
        for neighbourhood in neighbours.values()
    )
    stability_rhs = (
        hub_count * (hub_count - 1)
        - Fraction(edge_count**2, partner_count)
        + edge_count
    )
    return {
        "field_order": field_order,
        "hub_group_count": hub_group_count,
        "hub_vertex_count": hub_count,
        "partner_vertex_count": partner_count,
        "edge_count": edge_count,
        "kst_scale": hub_count * field_order,
        "c4_count": c4_count,
        "is_c4_free": c4_count == 0,
        "partner_degree": hub_group_count,
        "degree_variance": degree_variance,
        "covered_hub_pairs": covered_pairs,
        "uncovered_hub_pairs": uncovered_pairs,
        "expected_uncovered_within_groups": (
            hub_group_count * field_order * (field_order - 1) // 2
        ),
        "stability_identity_lhs": (
            degree_variance + 2 * uncovered_pairs
        ),
        "stability_identity_rhs": stability_rhs,
        "distinct_real_cells": len(cell_counts),
        "real_cell_upper_bound": 2 * hub_group_count * field_order,
        "maximum_cell_representation": max(cell_counts.values()),
        "height_set_additive_energy": (
            2 * field_order**3 + field_order
        ) // 3,
    }


def exponent_ledger(
    eta_numerator: int,
    eta_denominator: int,
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    height = Fraction(1)
    hub_groups = Fraction(5, 6) + 2 * eta
    hub_vertices = height + hub_groups
    partner_vertices = Fraction(2)
    threshold_edges = hub_vertices + partner_vertices / 2
    forced_edges = Fraction(3) - 3 * eta
    cell_universe = Fraction(8, 3) + eta
    endpoint_reuse_target = Fraction(1, 3) - 4 * eta
    hypothetical_cycle_count = 2 * hub_vertices
    endpoint_fibre_palette_threshold = (
        hypothetical_cycle_count - endpoint_reuse_target
    )
    maximal_energy_palette_threshold = (
        2 * hypothetical_cycle_count - 5 * height
    )
    return {
        "eta": eta,
        "height_capacity_exponent": height,
        "hub_group_exponent": hub_groups,
        "hub_vertex_exponent": hub_vertices,
        "partner_vertex_exponent": partner_vertices,
        "forced_edge_exponent": forced_edges,
        "kst_edge_threshold_exponent": threshold_edges,
        "edge_surplus_exponent": forced_edges - threshold_edges,
        "cell_universe_exponent": cell_universe,
        "signed_triple_palette_bound_from_M": 3 * cell_universe,
        "signed_triple_palette_bound_per_four_blocks": 6 * height,
        "radius_quartet_count_exponent": (
            2 * hub_groups + 2 * height
        ),
        "hypothetical_constant_surplus_c4_exponent": (
            hypothetical_cycle_count
        ),
        "endpoint_reuse_target_exponent": endpoint_reuse_target,
        "palette_needed_for_endpoint_reuse_exponent": (
            endpoint_fibre_palette_threshold
        ),
        "palette_needed_for_maximal_additive_energy_exponent": (
            maximal_energy_palette_threshold
        ),
        "global_palette_gap_for_endpoint_reuse_exponent": (
            3 * cell_universe - endpoint_fibre_palette_threshold
        ),
        "block_palette_gap_for_endpoint_reuse_exponent": (
            6 * height - endpoint_fibre_palette_threshold
        ),
    }


def _json_ready(value: object) -> object:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=7)
    parser.add_argument("--hub-groups", type=int, default=4)
    args = parser.parse_args()
    output = {
        "complete_ap": complete_ap_model(args.length),
        "translation_fan": translation_fan_model(args.length),
        "latin_transversal": latin_transversal_model(
            args.length,
            args.hub_groups,
        ),
        "eta_ledger": exponent_ledger(1, 30),
    }
    print(json.dumps(_json_ready(output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
