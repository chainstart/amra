#!/usr/bin/env python3
"""Verify the dual service cochain and a translated Latin SAT core."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from itertools import product

import sympy as sp


def radial_offset(first: int, second: int, ratio: int) -> int:
    return (ratio**first - ratio**second) ** 2


def alternating_sum(values: tuple[sp.Expr, ...]) -> sp.Expr:
    return sp.simplify(
        sum(
            value if index % 2 == 0 else -value
            for index, value in enumerate(values)
        )
    )


def forced_partner_shift(
    radial_gap: sp.Expr,
    first_cross_shift: sp.Expr,
    second_cross_shift: sp.Expr,
) -> sp.Expr:
    """Use radial_gap=C_xy-C_uv."""
    return sp.simplify(
        (
            radial_gap
            - first_cross_shift**2
            + second_cross_shift**2
        )
        / (2 * (first_cross_shift + second_cross_shift))
    )


def equal_shift_cycle_radial_identity(
    radial_gaps: tuple[sp.Expr, ...],
    first_cross_shift: sp.Expr,
    second_cross_shift: sp.Expr,
) -> dict[str, sp.Expr | bool]:
    if len(radial_gaps) not in (4, 6):
        raise ValueError("the audit checks four- and six-cycles")
    partner_shifts = tuple(
        forced_partner_shift(
            gap,
            first_cross_shift,
            second_cross_shift,
        )
        for gap in radial_gaps
    )
    partner_cycle_sum = alternating_sum(partner_shifts)
    radial_cycle_sum = alternating_sum(radial_gaps)
    denominator = 2 * (
        first_cross_shift + second_cross_shift
    )
    return {
        "cycle_length": len(radial_gaps),
        "partner_cycle_sum": partner_cycle_sum,
        "radial_cycle_sum": radial_cycle_sum,
        "scaled_identity_holds": (
            sp.simplify(
                denominator * partner_cycle_sum
                - radial_cycle_sum
            )
            == 0
        ),
    }


def _component_cycle_rank(
    vertices: set[tuple[str, int, int]],
    edges: list[
        tuple[tuple[str, int, int], tuple[str, int, int], sp.Expr]
    ],
) -> int:
    parent = {vertex: vertex for vertex in vertices}

    def find(vertex: tuple[str, int, int]) -> tuple[str, int, int]:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(
        first: tuple[str, int, int],
        second: tuple[str, int, int],
    ) -> None:
        root_first = find(first)
        root_second = find(second)
        if root_first != root_second:
            parent[root_second] = root_first

    for first, second, _ in edges:
        union(first, second)
    component_count = len({find(vertex) for vertex in vertices})
    return len(edges) - len(vertices) + component_count


def translated_latin_sat_core() -> dict[str, object]:
    """An exact q=3,U=2 service design on the maximal pairable core."""
    field_order = 3
    hub_group_count = 2
    partner_radius_offset = 5
    ratio = 2
    radical_a = sp.sqrt(49149)
    radical_b = sp.sqrt(12285)
    hub_translations = (sp.Integer(0), (-1 + radical_a) / 2)
    partner_translations = (
        (-1 + radical_a - radical_b) / 2,
        sp.Rational(-1, 2),
        sp.Rational(1, 2),
    )
    strip_permutations = (
        (2, 0, 1),
        (1, 2, 0),
    )

    services = []
    used_cross_edges = set()
    cross_cells = set()
    partner_arcs = []
    hub_arcs = []
    local_boundary_sums = []
    for slope, permutation in enumerate(strip_permutations):
        hub_first = 0
        hub_second = 1
        partner_second_group = slope
        partner_first_group = slope + 1
        partner_second_radius = (
            partner_radius_offset + partner_second_group
        )
        partner_first_radius = (
            partner_radius_offset + partner_first_group
        )
        for intercept, paired_intercept in enumerate(permutation):
            first_residue = intercept
            second_residue = (
                partner_first_group + paired_intercept
            ) % field_order
            height_first = (
                hub_translations[hub_first] + first_residue
            )
            height_second = (
                partner_translations[partner_second_group]
                + intercept
            )
            height_hub_second = (
                hub_translations[hub_second] + second_residue
            )
            height_partner_first = (
                partner_translations[partner_first_group]
                + paired_intercept
            )
            first_cross_shift = sp.simplify(
                height_first - height_second
            )
            second_cross_shift = sp.simplify(
                height_hub_second - height_partner_first
            )
            partner_shift = sp.simplify(
                height_second - height_partner_first
            )
            hub_shift = sp.simplify(
                height_hub_second - height_first
            )
            original_first = sp.simplify(
                radial_offset(
                    hub_first,
                    partner_first_radius,
                    ratio,
                )
                + (height_first - height_partner_first) ** 2
            )
            original_second = sp.simplify(
                radial_offset(
                    hub_second,
                    partner_second_radius,
                    ratio,
                )
                + (height_hub_second - height_second) ** 2
            )
            boundary_sum = sp.simplify(
                hub_shift
                - second_cross_shift
                + partner_shift
                + first_cross_shift
            )
            local_boundary_sums.append(boundary_sum)
            first_edge = (
                hub_first,
                first_residue,
                partner_second_group,
                intercept,
            )
            second_edge = (
                hub_second,
                second_residue,
                partner_first_group,
                paired_intercept,
            )
            used_cross_edges.update((first_edge, second_edge))
            first_cell = (
                hub_first + partner_second_radius,
                sp.simplify(
                    radial_offset(
                        hub_first,
                        partner_second_radius,
                        ratio,
                    )
                    + first_cross_shift**2
                ),
            )
            second_cell = (
                hub_second + partner_first_radius,
                sp.simplify(
                    radial_offset(
                        hub_second,
                        partner_first_radius,
                        ratio,
                    )
                    + second_cross_shift**2
                ),
            )
            cross_cells.update((first_cell, second_cell))
            partner_start = (
                "n",
                partner_first_group,
                paired_intercept,
            )
            partner_end = (
                "n",
                partner_second_group,
                intercept,
            )
            hub_start = ("h", hub_first, first_residue)
            hub_end = ("h", hub_second, second_residue)
            partner_arcs.append(
                (partner_start, partner_end, partner_shift)
            )
            hub_arcs.append((hub_start, hub_end, hub_shift))
            services.append(
                {
                    "strip": slope,
                    "intercept": intercept,
                    "paired_intercept": paired_intercept,
                    "original_values_equal": (
                        sp.simplify(
                            original_first - original_second
                        )
                        == 0
                    ),
                    "local_four_cycle_sum": boundary_sum,
                    "partner_shift": partner_shift,
                    "hub_shift": hub_shift,
                    "first_cross_shift": first_cross_shift,
                    "second_cross_shift": second_cross_shift,
                }
            )

    partner_vertices = {
        endpoint
        for first, second, _ in partner_arcs
        for endpoint in (first, second)
    }
    hub_vertices = {
        endpoint
        for first, second, _ in hub_arcs
        for endpoint in (first, second)
    }
    parallel_hub_labels: defaultdict[
        tuple[tuple[str, int, int], tuple[str, int, int]],
        list[sp.Expr],
    ] = defaultdict(list)
    for first, second, label in hub_arcs:
        parallel_hub_labels[(first, second)].append(label)
    parallel_hub_differences = tuple(
        sp.simplify(labels[0] - labels[1])
        for labels in parallel_hub_labels.values()
        if len(labels) == 2
    )
    return {
        "field_order": field_order,
        "hub_group_count": hub_group_count,
        "permutation_pair_search_space": 6**2,
        "strip_permutations": strip_permutations,
        "hub_translation_polynomial_holds": (
            sp.simplify(
                hub_translations[1] ** 2
                + hub_translations[1]
                - 12287
            )
            == 0
        ),
        "translation_gap_polynomial_holds": (
            sp.simplify(
                (
                    hub_translations[1]
                    - partner_translations[0]
                )
                ** 2
                - sp.Rational(12285, 4)
            )
            == 0
        ),
        "service_count": len(services),
        "all_original_gram_equalities_hold": all(
            service["original_values_equal"] for service in services
        ),
        "all_local_four_cycle_sums_zero": all(
            value == 0 for value in local_boundary_sums
        ),
        "used_cross_edge_count": len(used_cross_edges),
        "pairable_core_cross_edge_count": (
            len(strip_permutations)
            * 2
            * field_order
        ),
        "all_pairable_core_edges_used_once": (
            len(used_cross_edges)
            == len(strip_permutations)
            * 2
            * field_order
        ),
        "unpairable_boundary_block_count": 2,
        "distinct_cross_cell_count": len(cross_cells),
        "cross_cell_block_bound": (
            2 * len(strip_permutations) * 2
        ),
        "partner_projection_cycle_rank": _component_cycle_rank(
            partner_vertices,
            partner_arcs,
        ),
        "hub_projection_cycle_rank": _component_cycle_rank(
            hub_vertices,
            hub_arcs,
        ),
        "parallel_hub_two_cycle_count": len(
            parallel_hub_differences
        ),
        "all_parallel_hub_two_cycles_close": all(
            difference == 0
            for difference in parallel_hub_differences
        ),
    }


def exponent_ledger() -> dict[str, sp.Rational]:
    service_mass = sp.Rational(33, 10)
    cross_edges = sp.Rational(29, 10)
    return {
        "service_mass_exponent": service_mass,
        "cross_edge_exponent": cross_edges,
        "required_compatibility_degree_exponent": (
            service_mass - cross_edges
        ),
        "finite_sat_core_power_surplus": sp.Rational(0),
    }


def _json_ready(value: object) -> object:
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    output = {
        "translated_latin_sat_core": translated_latin_sat_core(),
        "four_cycle_identity": equal_shift_cycle_radial_identity(
            (sp.Integer(3), 5, 8, 6),
            sp.Integer(2),
            sp.Integer(3),
        ),
        "six_cycle_identity": equal_shift_cycle_radial_identity(
            (sp.Integer(3), 5, 8, 6, 4, 4),
            sp.Integer(2),
            sp.Integer(3),
        ),
        "ledger": exponent_ledger(),
    }
    print(json.dumps(_json_ready(output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
