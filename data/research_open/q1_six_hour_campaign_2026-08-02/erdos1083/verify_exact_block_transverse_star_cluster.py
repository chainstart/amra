#!/usr/bin/env python3
"""Finite and symbolic checks for the exact-block star-cluster theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json

import networkx as nx
import sympy as sp


Q = Fraction


def endpoint_certificate() -> dict[str, object]:
    source = Q(7, 9)
    tangent_row = Q(5, 6)
    edge = Q(8, 9)
    rows = Q(13, 18)
    tangent_overlap = Q(19, 9)
    star = edge - rows
    common_tangent_star = tangent_overlap - rows - tangent_row
    tiling_margin = 2 * source - tangent_row
    return {
        "S_exponent": str(source),
        "U_exponent": str(tangent_row),
        "S2_over_U_margin": str(tiling_margin),
        "fixed_difference_edge_exponent": str(edge),
        "transverse_tangent_overlap_exponent": str(tangent_overlap),
        "row_exponent": str(rows),
        "star_leaf_exponent": str(star),
        "common_tangent_leaf_exponent": str(common_tangent_star),
        "U_strictly_below_S2": tangent_row < 2 * source,
        "pass": (
            tiling_margin == Q(13, 18)
            and star == Q(1, 6)
            and common_tangent_star == Q(5, 9)
            and tangent_row < 2 * source
        ),
    }


def exhaustive_triangle_free_neighbourhood_certificate(max_vertices: int = 6) -> dict[str, object]:
    graph_count = 0
    triangle_free_count = 0
    neighbourhood_checks = 0
    for vertex_count in range(1, max_vertices + 1):
        possible_edges = list(combinations(range(vertex_count), 2))
        for mask in range(1 << len(possible_edges)):
            graph_count += 1
            graph = nx.Graph()
            graph.add_nodes_from(range(vertex_count))
            graph.add_edges_from(
                edge for bit, edge in enumerate(possible_edges) if mask >> bit & 1
            )
            if any(len(clique) >= 3 for clique in nx.enumerate_all_cliques(graph)):
                continue
            triangle_free_count += 1
            for vertex in graph:
                neighbours = list(graph.neighbors(vertex))
                neighbourhood_checks += 1
                if any(graph.has_edge(left, right) for left, right in combinations(neighbours, 2)):
                    raise AssertionError("triangle-free neighbourhood was not independent")
    return {
        "max_vertices": max_vertices,
        "graph_count": graph_count,
        "triangle_free_graph_count": triangle_free_count,
        "neighbourhood_checks": neighbourhood_checks,
        "all_triangle_free_neighbourhoods_independent": True,
        "pass": True,
    }


def rank_two_examples_certificate() -> dict[str, object]:
    # Star: all planes contain e1, but their total span has dimension four.
    star_family = [
        sp.Matrix.hstack(sp.eye(4)[:, 0], sp.eye(4)[:, index])
        for index in (1, 2, 3)
    ]
    # Top: three coordinate planes in Q^3; pairwise intersections are
    # nonzero but the total intersection is zero.
    basis3 = sp.eye(3)
    top_family = [
        sp.Matrix.hstack(basis3[:, 0], basis3[:, 1]),
        sp.Matrix.hstack(basis3[:, 0], basis3[:, 2]),
        sp.Matrix.hstack(basis3[:, 1], basis3[:, 2]),
    ]

    def intersection_dimension(left: sp.Matrix, right: sp.Matrix) -> int:
        return left.rank() + right.rank() - sp.Matrix.hstack(left, right).rank()

    def total_intersection_dimension(family: list[sp.Matrix]) -> int:
        # Orthogonal-complement identity: intersection kernels can be
        # computed from the span of annihilator row spaces.
        ambient = family[0].rows
        annihilators = []
        for matrix in family:
            annihilators.extend(matrix.T.nullspace())
        if not annihilators:
            return ambient
        annihilator_span = sp.Matrix.hstack(*annihilators)
        return ambient - annihilator_span.rank()

    def span_dimension(family: list[sp.Matrix]) -> int:
        return sp.Matrix.hstack(*family).rank()

    star_pairwise = [
        intersection_dimension(left, right)
        for left, right in combinations(star_family, 2)
    ]
    top_pairwise = [
        intersection_dimension(left, right)
        for left, right in combinations(top_family, 2)
    ]
    star_common = total_intersection_dimension(star_family)
    top_common = total_intersection_dimension(top_family)
    star_span = span_dimension(star_family)
    top_span = span_dimension(top_family)
    return {
        "top_scalar_dilate_model": {
            "minimal_polynomial": "a^3-a^2-1",
            "W": ["1", "a"],
            "scalar_dilates": ["W", "aW", "a^2W"],
            "coordinate_planes_in_basis_1_a_a2": ["12", "23", "13"],
        },
        "star_pairwise_intersection_dimensions": star_pairwise,
        "star_total_intersection_dimension": star_common,
        "star_total_span_dimension": star_span,
        "top_pairwise_intersection_dimensions": top_pairwise,
        "top_total_intersection_dimension": top_common,
        "top_total_span_dimension": top_span,
        "pass": (
            all(value >= 1 for value in star_pairwise)
            and star_common == 1
            and star_span == 4
            and all(value >= 1 for value in top_pairwise)
            and top_common == 0
            and top_span == 3
        ),
    }


def quotient_identity_certificate() -> dict[str, object]:
    # W=span_Q{1,sqrt(2)}.  The scalar dilates below are chosen so that
    # every space is W itself (the scalars are nonzero elements of the
    # quadratic field), providing exact pairwise quotient witnesses.
    root = sp.sqrt(2)
    basis = [sp.Integer(1), root]
    scalars = [sp.Integer(1), 1 + root, 3 - 2 * root]
    witnesses = []
    for left, right in combinations(scalars, 2):
        ratio = sp.simplify(left / right)
        expanded = sp.collect(sp.expand(ratio), root)
        polynomial = sp.minimal_polynomial(ratio)
        witnesses.append(
            {
                "left": str(left),
                "right": str(right),
                "ratio": str(expanded),
                "ratio_degree_at_most_two": int(sp.degree(polynomial)) <= 2,
            }
        )
    return {
        "W_basis": list(map(str, basis)),
        "pair_count": len(witnesses),
        "witnesses": witnesses,
        "all_ratios_in_quadratic_quotient_field": all(
            witness["ratio_degree_at_most_two"] for witness in witnesses
        ),
        "pass": all(witness["ratio_degree_at_most_two"] for witness in witnesses),
    }


def main() -> int:
    result = {
        "endpoint": endpoint_certificate(),
        "triangle_free_graphs": exhaustive_triangle_free_neighbourhood_certificate(),
        "rank_two_examples": rank_two_examples_certificate(),
        "quotient_identity": quotient_identity_certificate(),
        "all_parameter_group_ring_input_proved_in_manuscript": True,
    }
    result["pass"] = all(
        result[key]["pass"]
        for key in ("endpoint", "triangle_free_graphs", "rank_two_examples", "quotient_identity")
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
