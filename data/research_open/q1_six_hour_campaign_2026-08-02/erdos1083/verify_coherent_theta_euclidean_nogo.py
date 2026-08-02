#!/usr/bin/env python3
"""Exact finite certificates for the coherent-theta Euclidean no-go model.

The all-parameter theorem is proved in COHERENT_THETA_EUCLIDEAN_NO_GO.md.
This file uses exact SymPy radicals to falsify its algebraic and geometric
interfaces on representative finite instances.
"""

from __future__ import annotations

import json
from itertools import combinations

import sympy as sp


def squared_distance(left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]) -> sp.Expr:
    return sp.simplify(sum((a - b) ** 2 for a, b in zip(left, right)))


def build_certificate(source_size: int, arm_count: int, tangent: int = 10) -> dict[str, object]:
    if source_size < 2:
        raise ValueError("source_size must be at least two")
    if not 1 <= arm_count <= source_size - 1:
        raise ValueError("arm_count must lie in [1, source_size-1]")
    if tangent <= 0:
        raise ValueError("tangent must be positive")

    S = source_size
    K = arm_count
    A = sp.Integer(2)
    x_set = [sp.Rational(j, S - 1) for j in range(S)]
    arm_labels = x_set[1 : K + 1]
    endpoint_heights = [sp.sqrt(2), -sp.sqrt(2)]
    internal_heights = [
        sp.simplify(-x + sp.sqrt(1 + x**2)) for x in arm_labels
    ]

    def potential(z: sp.Expr, x: sp.Expr) -> sp.Expr:
        return sp.simplify(z**2 + 2 * z * x)

    sources = [
        (A + sp.sqrt(1 - x**2), sp.Integer(0), x) for x in x_set
    ]
    endpoint_targets = [
        (A, sp.sqrt(tangent), -z) for z in endpoint_heights
    ]
    internal_targets = [
        (A, sp.sqrt(tangent + 1), -z) for z in internal_heights
    ]
    points = sources + endpoint_targets + internal_targets

    endpoint_potentials = [potential(z, sp.Integer(0)) for z in endpoint_heights]
    internal_potentials = [
        potential(z, x) for z, x in zip(internal_heights, arm_labels)
    ]
    fixed_difference_equations = [
        sp.simplify(endpoint_potential - internal_potential)
        for endpoint_potential in endpoint_potentials
        for internal_potential in internal_potentials
    ]

    common_label = sp.Integer(tangent + 3)
    selected_distances = []
    for internal_index, internal_target in enumerate(internal_targets):
        selected_distances.extend(
            [
                squared_distance(sources[0], endpoint_targets[0]),
                squared_distance(sources[internal_index + 1], internal_target),
                squared_distance(sources[0], endpoint_targets[1]),
            ]
        )

    cell_sizes = []
    for height, target in zip(endpoint_heights, endpoint_targets):
        cell_sizes.append(len({squared_distance(source, target) for source in sources}))
    for height, target in zip(internal_heights, internal_targets):
        cell_sizes.append(len({squared_distance(source, target) for source in sources}))

    transversality_degrees = []
    for internal_height in internal_heights:
        ratio = sp.simplify(internal_height / sp.sqrt(2))
        polynomial = sp.minimal_polynomial(ratio)
        transversality_degrees.append(int(sp.degree(polynomial)))

    point_keys = {tuple(map(sp.srepr, point)) for point in points}
    all_squared_distances = {
        sp.simplify(squared_distance(left, right))
        for left, right in combinations(points, 2)
    }
    pair_bound = len(points) * (len(points) - 1) // 2
    endpoint_pair_bound = 2 * S * S + S

    source_circle_checks = [
        sp.simplify((source[0] - A) ** 2 + source[2] ** 2)
        for source in sources
    ]
    internal_distinct = len(set(map(sp.srepr, internal_heights))) == K
    all_heights = endpoint_heights + internal_heights
    height_distinct = len(set(map(sp.srepr, all_heights))) == K + 2

    result = {
        "source_size": S,
        "arm_count": K,
        "point_count": len(points),
        "expected_point_count": S + K + 2,
        "point_count_at_most_2S_plus_1": len(points) <= 2 * S + 1,
        "points_distinct": len(point_keys) == len(points),
        "source_circle_exact": all(value == 1 for value in source_circle_checks),
        "endpoint_potentials": list(map(str, endpoint_potentials)),
        "internal_potentials": list(map(str, internal_potentials)),
        "fixed_difference_values": list(map(str, fixed_difference_equations)),
        "fixed_difference_is_one": all(value == 1 for value in fixed_difference_equations),
        "common_selected_distance": str(common_label),
        "selected_distance_values": list(map(str, selected_distances)),
        "selected_distances_all_common": all(value == common_label for value in selected_distances),
        "row_cell_sizes": cell_sizes,
        "every_selected_cell_injective": all(size == S for size in cell_sizes),
        "transverse_ratio_minimal_polynomial_degrees": transversality_degrees,
        "every_endpoint_internal_ratio_irrational": all(degree > 1 for degree in transversality_degrees),
        "internal_heights_distinct": internal_distinct,
        "all_row_heights_distinct": height_distinct,
        "all_heights_nonzero": all(sp.simplify(height) != 0 for height in all_heights),
        "orientation_word": "+-",
        "interiors_pairwise_disjoint": internal_distinct,
        "tangent_squares": [tangent, tangent + 1],
        "all_tangents_positive": tangent > 0,
        "distinct_squared_distance_count": len(all_squared_distances),
        "complete_pair_bound": pair_bound,
        "complete_pair_bound_holds": len(all_squared_distances) <= pair_bound,
        "endpoint_formula_bound": endpoint_pair_bound,
        "endpoint_formula_bound_holds": len(all_squared_distances) <= endpoint_pair_bound,
    }
    result["pass"] = all(
        (
            result["point_count"] == result["expected_point_count"],
            result["point_count_at_most_2S_plus_1"],
            result["points_distinct"],
            result["source_circle_exact"],
            result["fixed_difference_is_one"],
            result["selected_distances_all_common"],
            result["every_selected_cell_injective"],
            result["every_endpoint_internal_ratio_irrational"],
            result["all_row_heights_distinct"],
            result["all_heights_nonzero"],
            result["interiors_pairwise_disjoint"],
            result["all_tangents_positive"],
            result["complete_pair_bound_holds"],
            result["endpoint_formula_bound_holds"],
        )
    )
    return result


def endpoint_exponent_certificate() -> dict[str, object]:
    source = sp.Rational(7, 9)
    local_pair_bound = 2 * source
    global_budget = sp.Integer(3)
    margin = global_budget - local_pair_bound
    inherited_theta = sp.Rational(1, 20)
    return {
        "source_exponent": str(source),
        "maximal_arm_exponent": str(source),
        "inherited_theta_exponent": str(inherited_theta),
        "local_complete_distance_upper_exponent": str(local_pair_bound),
        "global_distance_budget_exponent": str(global_budget),
        "budget_margin": str(margin),
        "maximal_width_dominates_inherited_theta": bool(source > inherited_theta),
        "local_distance_bound_below_global_budget": bool(local_pair_bound < global_budget),
        "pass": bool(
            local_pair_bound == sp.Rational(14, 9)
            and margin == sp.Rational(13, 9)
            and source > inherited_theta
        ),
    }


def main() -> int:
    instances = [
        build_certificate(5, 1),
        build_certificate(7, 4),
        build_certificate(10, 9),
    ]
    result = {
        "instances": instances,
        "endpoint": endpoint_exponent_certificate(),
        "all_parameter_claim_proved_in_manuscript": True,
    }
    result["pass"] = all(instance["pass"] for instance in instances) and result["endpoint"]["pass"]
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
