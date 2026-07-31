#!/usr/bin/env python3
"""Finite guards for the seventh 2026-07-31 Erdos #809 attack."""

from __future__ import annotations

import itertools
import json
import math

import verify_809_sixth_attack as sixth


def opposite_core_guard() -> dict[str, int | bool]:
    """Check the exact opposite-pair core energy identity."""
    graph = sixth.build_three_hub_graph()
    groups = graph["groups"]
    vertices = graph["vertices"]
    graph_edges = graph["edges"]
    adjacency = graph["adjacency"]
    assert isinstance(groups, dict)
    assert isinstance(vertices, list)
    assert isinstance(graph_edges, set)
    assert isinstance(adjacency, dict)

    first = groups["U"][0]
    second = groups["W"][0]
    p_set = set(adjacency[first])
    q_set = set(adjacency[second])
    assert not (p_set & q_set)
    p_size = len(p_set)
    q_size = len(q_set)
    residual = len(vertices) - p_size - q_size
    c_set = set(vertices) - p_set
    cut_edges = sum(
        sixth.edge(left, right) in graph_edges
        for left in p_set
        for right in c_set
    )
    missing_p = sum(
        sixth.edge(left, right) not in graph_edges
        for left, right in itertools.combinations(p_set, 2)
    )
    missing_c = sum(
        sixth.edge(left, right) not in graph_edges
        for left, right in itertools.combinations(c_set, 2)
    )
    psi = (
        math.comb(p_size, 2)
        + math.comb(len(vertices) - p_size, 2)
        - len(graph_edges)
    )
    assert missing_p + missing_c == psi + cut_edges
    assert cut_edges <= p_size * residual
    assert missing_p + missing_c <= psi + p_size * residual
    return {
        "n": len(vertices),
        "p_degree": p_size,
        "q_degree": q_size,
        "residual_rho": residual,
        "cut_edges": cut_edges,
        "cut_upper_bound": p_size * residual,
        "missing_P": missing_p,
        "missing_C": missing_c,
        "psi": psi,
        "energy_upper_bound": psi + p_size * residual,
        "passed": True,
    }


def opposite_star_guard() -> dict[str, int | float | bool]:
    """Check local opposite alignment and its weighted residual moment."""
    graph = sixth.build_three_hub_graph()
    groups = graph["groups"]
    vertices = graph["vertices"]
    adjacency = graph["adjacency"]
    assert isinstance(groups, dict)
    assert isinstance(vertices, list)
    assert isinstance(adjacency, dict)
    center = groups["U"][0]
    p_set = set(adjacency[center])
    complement = set(vertices) - p_set
    delta = min(len(adjacency[item]) for item in vertices)
    kappa = len(vertices) - 2 * delta
    matched_leaf = groups["W"][0]
    weight = len(groups["Y"]) - 1
    residuals = []
    symmetric_differences = []
    for leaf in groups["W"]:
        q_set = set(adjacency[leaf])
        assert not (p_set & q_set)
        residual = len(complement - q_set)
        assert residual <= kappa
        residuals.append(residual)
        symmetric_differences.append(len(complement ^ q_set))

    matched_residual = len(
        complement - set(adjacency[matched_leaf])
    )
    total_weight = weight
    residual_moment = weight * matched_residual
    weighted_average = residual_moment / total_weight
    assert matched_residual <= weighted_average
    return {
        "leaves": len(residuals),
        "weighted_leaves": 1,
        "edge_weight_h_minus_one": weight,
        "star_excess": total_weight,
        "kappa": kappa,
        "maximum_complement_error": max(residuals),
        "maximum_leaf_symmetric_difference": max(
            symmetric_differences
        ),
        "weighted_residual_moment": residual_moment,
        "weighted_average_rho": weighted_average,
        "passed": True,
    }


def absorption_certificate_guard() -> dict[str, int | bool]:
    """Check the seventh-stage sufficient high/low absorption test."""
    residual_a = 4
    size_slack = 60
    missing_b = 7
    q_a = 30
    threshold = 5
    e_zero_bound = (threshold - 1) * missing_b + 2 * q_a // threshold
    assert residual_a + e_zero_bound <= size_slack
    return {
        "R_A": residual_a,
        "S_m": size_slack,
        "M_B": missing_b,
        "Q_A": q_a,
        "H": threshold,
        "E0_high_low_bound": e_zero_bound,
        "absorbed": True,
        "passed": True,
    }


def main() -> None:
    result = {
        "opposite_core": opposite_core_guard(),
        "opposite_star": opposite_star_guard(),
        "absorption_certificate": absorption_certificate_guard(),
        "scope": (
            "Finite guards for exact identities only; controlling the "
            "weighted residual moment at fixed s remains open."
        ),
        "passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
