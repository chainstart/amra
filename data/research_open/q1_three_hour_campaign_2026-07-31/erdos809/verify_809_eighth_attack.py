#!/usr/bin/env python3
"""Finite guards for the eighth 2026-07-31 Erdős #809 attack.

The graph is a three-clique chain.  It separates failure of the
high/low absorption certificate from small opposite residual moment.
"""

from __future__ import annotations

import itertools
import json
import math


Vertex = tuple[str, int]
Edge = frozenset[Vertex]


def edge(left: Vertex, right: Vertex) -> Edge:
    return frozenset((left, right))


def build_linear_residual_graph(
    k: int = 6, hub_size: int = 16
) -> dict[str, object]:
    """Build four k-sets and a hub clique of size hub_size."""
    assert k >= 5
    assert hub_size >= 5
    sizes = {
        "U": k,
        "X": k,
        "W": k,
        "Y": k,
        "H": hub_size,
    }
    groups = {
        name: [(name, index) for index in range(size)]
        for name, size in sizes.items()
    }
    vertices = sum(groups.values(), [])
    graph_edges: set[Edge] = set()
    for clique in (
        groups["U"] + groups["X"],
        groups["W"] + groups["Y"],
        groups["H"],
    ):
        graph_edges.update(
            edge(left, right)
            for left, right in itertools.combinations(clique, 2)
        )
    for hub in groups["H"]:
        graph_edges.update(
            edge(hub, item) for item in groups["X"] + groups["Y"]
        )
    adjacency = {
        item: {
            other
            for other in vertices
            if other != item and edge(item, other) in graph_edges
        }
        for item in vertices
    }
    return {
        "k": k,
        "hub_size": hub_size,
        "groups": groups,
        "vertices": vertices,
        "edges": graph_edges,
        "adjacency": adjacency,
    }


def exact_four_internal_sets(
    first: Vertex,
    second: Vertex,
    adjacency: dict[Vertex, set[Vertex]],
) -> set[frozenset[Vertex]]:
    """Return internal vertex sets of all simple exact-four paths."""
    paths: set[frozenset[Vertex]] = set()
    for one in adjacency[first] - {second}:
        for two in adjacency[one] - {first, second}:
            for three in (adjacency[two] & adjacency[second]) - {
                first,
                one,
                two,
            }:
                paths.add(frozenset((one, two, three)))
    return paths


def has_transversal_at_most_two(
    path_sets: set[frozenset[Vertex]],
    eligible: list[Vertex],
) -> bool:
    """Test whether one or two eligible vertices hit every path set."""
    common = set.intersection(*(set(item) for item in path_sets))
    if common:
        return True
    for first in eligible:
        avoiding_first = [
            set(item) for item in path_sets if first not in item
        ]
        if not avoiding_first:
            return True
        if set.intersection(*avoiding_first):
            return True
    return False


def l4_two_guard(graph: dict[str, object]) -> dict[str, int | bool]:
    """Check L4(2) via the exact-four path transversal criterion."""
    vertices = graph["vertices"]
    adjacency = graph["adjacency"]
    assert isinstance(vertices, list)
    assert isinstance(adjacency, dict)
    minimum_path_sets: int | None = None
    checked_pairs = 0
    for first, second in itertools.combinations(vertices, 2):
        path_sets = exact_four_internal_sets(first, second, adjacency)
        assert path_sets
        eligible = [
            item for item in vertices if item not in {first, second}
        ]
        assert not has_transversal_at_most_two(path_sets, eligible)
        minimum_path_sets = (
            len(path_sets)
            if minimum_path_sets is None
            else min(minimum_path_sets, len(path_sets))
        )
        checked_pairs += 1
    n = len(vertices)
    deletion_checks = checked_pairs * (
        1 + (n - 2) + math.comb(n - 2, 2)
    )
    return {
        "vertex_pairs": checked_pairs,
        "equivalent_deletion_checks": deletion_checks,
        "minimum_exact_four_internal_sets": minimum_path_sets or 0,
        "passed": True,
    }


def has_length_three(
    first: Vertex,
    second: Vertex,
    adjacency: dict[Vertex, set[Vertex]],
) -> bool:
    """Check for a simple exact-three path between two endpoints."""
    for one in adjacency[first] - {second}:
        for two in (adjacency[one] & adjacency[second]) - {
            first,
            one,
        }:
            return True
    return False


def linked_two_three(
    first_edge: Edge,
    second_edge: Edge,
    adjacency: dict[Vertex, set[Vertex]],
) -> bool:
    """Test whether two induced independent edges lie on one C7."""
    first = tuple(first_edge)
    second = tuple(second_edge)
    for pairing in (
        ((first[0], second[0]), (first[1], second[1])),
        ((first[0], second[1]), (first[1], second[0])),
    ):
        for short_index in range(2):
            short = pairing[short_index]
            long = pairing[1 - short_index]
            for middle in (
                adjacency[short[0]] & adjacency[short[1]]
            ) - set(first + second):
                short_vertices = {short[0], middle, short[1]}
                for one in adjacency[long[0]] - short_vertices - {
                    long[1]
                }:
                    for two in (
                        adjacency[one] & adjacency[long[1]]
                    ) - short_vertices - {long[0], one}:
                        if two != one:
                            return True
    return False


def full_contract_countermodel_guard() -> dict[str, int | float | bool]:
    """Audit the finite graph, colouring, budgets, and residual moment."""
    graph = build_linear_residual_graph()
    groups = graph["groups"]
    vertices = graph["vertices"]
    graph_edges = graph["edges"]
    adjacency = graph["adjacency"]
    k = graph["k"]
    hub_size = graph["hub_size"]
    assert isinstance(groups, dict)
    assert isinstance(vertices, list)
    assert isinstance(graph_edges, set)
    assert isinstance(adjacency, dict)
    assert isinstance(k, int)
    assert isinstance(hub_size, int)

    n = len(vertices)
    e_count = len(graph_edges)
    degrees = {item: len(adjacency[item]) for item in vertices}
    delta = min(degrees.values())
    maximum_degree = max(degrees.values())
    center = groups["H"][0]
    a_side = set(groups["H"] + groups["X"] + groups["Y"])
    b_side = set(groups["U"] + groups["W"])
    assert a_side == {center, *adjacency[center]}
    assert b_side == set(vertices) - a_side
    assert delta == 2 * k - 1
    assert maximum_degree == 2 * k + hub_size - 1
    assert len(a_side) == maximum_degree + 1
    assert e_count > n * n / 4
    bcm_threshold = n / 2 + math.sqrt(
        e_count - n * n / 4 + n / 2
    )
    assert math.isclose(bcm_threshold, len(a_side))

    repeated_pairs: list[tuple[Edge, Edge]] = []
    for index in range(k):
        for coordinate in range(k):
            repeated_pairs.append(
                (
                    edge(groups["U"][index], groups["X"][coordinate]),
                    edge(groups["W"][index], groups["Y"][coordinate]),
                )
            )
    assert len(repeated_pairs) == k * k
    for first_edge, second_edge in repeated_pairs:
        endpoints = set(first_edge) | set(second_edge)
        induced_edges = {
            item for item in graph_edges if item <= endpoints
        }
        assert induced_edges == {first_edge, second_edge}
        assert not linked_two_three(first_edge, second_edge, adjacency)

    zero_pairs: list[Edge] = []
    residuals: list[int] = []
    for index in range(k):
        first = groups["U"][index]
        second = groups["W"][index]
        zero_pair = edge(first, second)
        assert zero_pair not in graph_edges
        assert not has_length_three(first, second, adjacency)
        assert not (adjacency[first] & adjacency[second])
        zero_pairs.append(zero_pair)
        residuals.append(n - degrees[first] - degrees[second])
    assert set(residuals) == {hub_size + 2}

    missing_a = sum(
        edge(left, right) not in graph_edges
        for left, right in itertools.combinations(a_side, 2)
    )
    missing_b = sum(
        edge(left, right) not in graph_edges
        for left, right in itertools.combinations(b_side, 2)
    )
    assert missing_a == k * k
    assert missing_b == k * k
    q_a = sum(
        len(adjacency[left] & b_side)
        * len(adjacency[right] & b_side)
        for left, right in itertools.combinations(a_side, 2)
        if edge(left, right) not in graph_edges
    )
    assert q_a == k**4

    phi = e_count / 2 + n / 2 * math.sqrt(
        e_count - n * n / 4
    )
    size_slack = e_count - math.comb(len(b_side), 2) - phi
    defect_a = len(repeated_pairs)
    colour_count = e_count - defect_a
    defect_b = defect_a
    residual_a = defect_a - defect_b
    assert residual_a == 0
    assert defect_a == missing_b
    assert defect_a <= missing_b + size_slack
    assert colour_count >= phi

    zero_excess = len(zero_pairs) * (k - 1)
    opposite_excess = zero_excess
    opposite_residual_moment = sum(
        (k - 1) * residual for residual in residuals
    )
    normalized_residual = (
        opposite_residual_moment / (n * opposite_excess)
    )
    assert residual_a + zero_excess > size_slack

    high_low_values = {
        threshold: (
            (threshold - 1) * missing_b
            + 2 * q_a / threshold
        )
        for threshold in range(2, 2 * k * k + 2)
    }
    best_threshold = min(high_low_values, key=high_low_values.get)
    best_bound = high_low_values[best_threshold]
    assert residual_a + best_bound > size_slack
    return {
        "n": n,
        "edges": e_count,
        "density_quarter_square": n * n / 4,
        "minimum_degree": delta,
        "maximum_degree": maximum_degree,
        "maximum_witness_size": len(a_side),
        "BCM_size_threshold": bcm_threshold,
        "repeated_good_defect_DA": defect_a,
        "total_colours": colour_count,
        "BCM_colour_target_Phi": phi,
        "B_oriented_defect_DB": defect_b,
        "outer_A_residual_RA": residual_a,
        "missing_A_edges": missing_a,
        "missing_B_edges": missing_b,
        "Q_A": q_a,
        "size_slack_Sm": size_slack,
        "zero_shore_excess_E0": zero_excess,
        "opposite_excess_E0opp": opposite_excess,
        "opposite_residual_rho": residuals[0],
        "opposite_residual_moment": opposite_residual_moment,
        "Ropp_over_nE0opp": normalized_residual,
        "best_high_low_H": best_threshold,
        "best_high_low_bound": best_bound,
        "specific_absorption_fails": True,
        "actual_budget_closes": True,
        "repeated_pairs_C7_incompatible": True,
        "passed": True,
    }


def asymptotic_formula_guard() -> dict[str, list[float] | bool]:
    """Check the scaled k=6t, r=16t family numerically."""
    residual_ratios: list[float] = []
    e0_densities: list[float] = []
    slack_densities: list[float] = []
    for scale in (1, 2, 4, 8):
        k = 6 * scale
        hub_size = 16 * scale
        n = 4 * k + hub_size
        e_count = (
            2 * math.comb(2 * k, 2)
            + math.comb(hub_size, 2)
            + 2 * k * hub_size
        )
        assert math.isclose(
            e_count - n * n / 4 + n / 2,
            hub_size * hub_size / 4,
        )
        bcm_threshold = n / 2 + math.sqrt(
            e_count - n * n / 4 + n / 2
        )
        assert math.isclose(bcm_threshold, 2 * k + hub_size)
        phi = e_count / 2 + n / 2 * math.sqrt(
            e_count - n * n / 4
        )
        size_slack = e_count - math.comb(2 * k, 2) - phi
        e0 = k * (k - 1)
        residual_ratios.append((hub_size + 2) / n)
        e0_densities.append(e0 / (n * n))
        slack_densities.append(size_slack / (n * n))
    assert residual_ratios[-1] > 0.4
    assert residual_ratios[-1] < residual_ratios[0]
    assert e0_densities[-1] > 0.02
    assert slack_densities[-1] < slack_densities[0]
    return {
        "Ropp_over_nE0opp": residual_ratios,
        "E0opp_over_n2": e0_densities,
        "Sm_over_n2": slack_densities,
        "limiting_residual_ratio": 0.4,
        "passed": True,
    }


def degree_support_guard() -> dict[str, int | float | bool]:
    """Check the exact endpoint identity and low-support inequality."""
    graph = build_linear_residual_graph()
    groups = graph["groups"]
    vertices = graph["vertices"]
    adjacency = graph["adjacency"]
    k = graph["k"]
    assert isinstance(groups, dict)
    assert isinstance(vertices, list)
    assert isinstance(adjacency, dict)
    assert isinstance(k, int)
    n = len(vertices)
    degrees = {item: len(adjacency[item]) for item in vertices}
    endpoint_weight = {item: 0 for item in vertices}
    pairs: list[tuple[Vertex, Vertex, int]] = []
    for index in range(k):
        first = groups["U"][index]
        second = groups["W"][index]
        weight = k - 1
        pairs.append((first, second, weight))
        endpoint_weight[first] += weight
        endpoint_weight[second] += weight
    opposite_excess = sum(weight for _, _, weight in pairs)
    residual_moment = sum(
        weight * (n - degrees[first] - degrees[second])
        for first, second, weight in pairs
    )
    degree_form = n * opposite_excess - sum(
        endpoint_weight[item] * degrees[item] for item in vertices
    )
    centered_form = sum(
        endpoint_weight[item] * (n / 2 - degrees[item])
        for item in vertices
    )
    assert residual_moment == degree_form
    assert math.isclose(residual_moment, centered_form)

    epsilon = 0.25
    low_vertices = {
        item
        for item in vertices
        if degrees[item] < (0.5 - epsilon) * n
    }
    low_incidence = sum(endpoint_weight[item] for item in low_vertices)
    delta = min(degrees.values())
    kappa = n - 2 * delta
    support_bound = (
        2 * epsilon * n * opposite_excess
        + kappa * low_incidence
    )
    assert residual_moment <= support_bound
    return {
        "opposite_excess_E0opp": opposite_excess,
        "residual_moment": residual_moment,
        "degree_deficit_form": degree_form,
        "epsilon": epsilon,
        "low_degree_endpoint_incidence": low_incidence,
        "degree_support_bound": support_bound,
        "passed": True,
    }


def main() -> None:
    graph = build_linear_residual_graph()
    result = {
        "full_contract_countermodel": full_contract_countermodel_guard(),
        "L4_2": l4_two_guard(graph),
        "asymptotic_formula": asymptotic_formula_guard(),
        "degree_support": degree_support_guard(),
        "scope": (
            "The model refutes an implication from failure of the "
            "high/low or E0 absorption tests to a little-o opposite "
            "residual moment.  Its exact defect still fits M_B, so it "
            "does not refute the canonical budget or Erdős #809."
        ),
        "passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
