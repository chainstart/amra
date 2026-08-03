#!/usr/bin/env python3
"""Bounded exact two-coordinate falsification test for G201 on K4 and W4.

For every pair of varied edges, P_e and Q_e are precomputed as biaffine
integer polynomials.  A rational endpoint is admitted only if, for every
marked edge e, all three Bernstein coefficients of P_e on the straight line
from the all-ones point are strictly positive.  No numerical approximation,
SymPy, or author checker is used.
"""

from __future__ import annotations

from itertools import combinations
from math import gcd
import json


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def is_forest(vertices: tuple[int, ...], edges: tuple[tuple[int, int], ...]) -> bool:
    parent = {vertex: vertex for vertex in vertices}

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        root_left, root_right = find(left), find(right)
        if root_left == root_right:
            return False
        parent[root_left] = root_right
    return True


def connected(
    vertices: tuple[int, ...], edges: tuple[tuple[int, int], ...], source: int, target: int
) -> bool:
    adjacency = {vertex: [] for vertex in vertices}
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    stack = [source]
    seen = {source}
    while stack:
        vertex = stack.pop()
        for nxt in adjacency[vertex]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return target in seen


def forest_complement_masks(
    vertices: tuple[int, ...], graph_edges: tuple[tuple[int, int], ...], marked_index: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    marked = graph_edges[marked_index]
    unmarked = tuple((index, item) for index, item in enumerate(graph_edges) if index != marked_index)
    full_mask = sum(1 << index for index, _ in unmarked)
    p_terms = []
    q_terms = []
    for subset_mask in range(1 << len(unmarked)):
        chosen = tuple(
            unmarked[position][1]
            for position in range(len(unmarked))
            if subset_mask >> position & 1
        )
        if not is_forest(vertices, chosen):
            continue
        chosen_mask = sum(
            1 << unmarked[position][0]
            for position in range(len(unmarked))
            if subset_mask >> position & 1
        )
        complement = full_mask ^ chosen_mask
        p_terms.append(complement)
        if connected(vertices, chosen, *marked):
            q_terms.append(complement)
    return tuple(p_terms), tuple(q_terms)


def biaffine_coefficients(terms: tuple[int, ...], first: int, second: int) -> tuple[int, int, int, int]:
    coefficients = [0, 0, 0, 0]
    for mask in terms:
        exponent_code = ((mask >> first) & 1) + 2 * ((mask >> second) & 1)
        coefficients[exponent_code] += 1
    return tuple(coefficients)


def endpoint_scaled(coefficients: tuple[int, int, int, int], x: int, y: int, denominator: int) -> int:
    c00, c10, c01, c11 = coefficients
    return c00*denominator**2 + c10*x*denominator + c01*y*denominator + c11*x*y


def bernstein_scaled(
    coefficients: tuple[int, int, int, int], x: int, y: int, denominator: int
) -> tuple[int, int, int]:
    """Return degree-two Bernstein coefficients times 2*denominator^2."""
    c00, c10, c01, c11 = coefficients
    anchor = c00 + c10 + c01 + c11
    dx, dy = x - denominator, y - denominator
    b0 = 2 * denominator**2 * anchor
    b1 = b0 + denominator * (c10*dx + c01*dy + c11*(dx + dy))
    b2 = 2 * endpoint_scaled(coefficients, x, y, denominator)
    return b0, b1, b2


def rational_string(numerator: int, denominator: int) -> str:
    divisor = gcd(abs(numerator), denominator)
    numerator //= divisor
    denominator //= divisor
    return str(numerator) if denominator == 1 else f"{numerator}/{denominator}"


def point_certificate(
    point: tuple[int, int], denominator: int, graph_edges: tuple[tuple[int, int], ...],
    p_coefficients: tuple[tuple[int, int, int, int], ...],
    q_coefficients: tuple[tuple[int, int, int, int], ...]
) -> dict[str, object]:
    x, y = point
    per_edge = {}
    good = []
    for index, marked in enumerate(graph_edges):
        bernstein = bernstein_scaled(p_coefficients[index], x, y, denominator)
        q_value = endpoint_scaled(q_coefficients[index], x, y, denominator)
        assert min(bernstein) > 0
        label = f"{marked[0]}{marked[1]}"
        per_edge[label] = {
            "P_path_bernstein_scaled_by_2D2": list(bernstein),
            "Q_endpoint_scaled_by_D2": q_value,
            "strict_good": q_value > 0
        }
        if q_value > 0:
            good.append(label)
    return {
        "coordinates": [rational_string(x, denominator), rational_string(y, denominator)],
        "strict_good_edges": good,
        "per_marked_edge": per_edge
    }


def analyze_host(name: str, vertices: tuple[int, ...], graph_edges: tuple[tuple[int, int], ...]) -> dict[str, object]:
    terms = tuple(
        forest_complement_masks(vertices, graph_edges, marked_index)
        for marked_index in range(len(graph_edges))
    )
    denominator = 8
    grid = range(-160, 81)  # exact [-20,10] in steps of 1/8
    profiles: dict[tuple[int, ...], tuple[int, int, int, int]] = {}
    certified_points = 0
    rejected_barriers = []

    for first, second in combinations(range(len(graph_edges)), 2):
        p_coefficients = tuple(
            biaffine_coefficients(terms[marked][0], first, second)
            for marked in range(len(graph_edges))
        )
        q_coefficients = tuple(
            biaffine_coefficients(terms[marked][1], first, second)
            for marked in range(len(graph_edges))
        )
        for x in grid:
            for y in grid:
                bernstein_rows = tuple(
                    bernstein_scaled(coefficients, x, y, denominator)
                    for coefficients in p_coefficients
                )
                component_valid = all(min(row) > 0 for row in bernstein_rows)
                q_values = tuple(
                    endpoint_scaled(coefficients, x, y, denominator)
                    for coefficients in q_coefficients
                )
                if not component_valid:
                    if len(rejected_barriers) < 8 and any(value <= 0 for value in q_values):
                        blocking = next(index for index, row in enumerate(bernstein_rows) if min(row) <= 0)
                        rejected_barriers.append({
                            "varied_edges": [list(graph_edges[first]), list(graph_edges[second])],
                            "coordinates": [rational_string(x, denominator), rational_string(y, denominator)],
                            "nonpositive_Q_edges": [
                                f"{graph_edges[index][0]}{graph_edges[index][1]}"
                                for index, value in enumerate(q_values) if value <= 0
                            ],
                            "blocking_P_edge": f"{graph_edges[blocking][0]}{graph_edges[blocking][1]}",
                            "blocking_bernstein_scaled": list(bernstein_rows[blocking])
                        })
                    continue
                certified_points += 1
                good_profile = tuple(index for index, value in enumerate(q_values) if value > 0)
                profiles.setdefault(good_profile, (first, second, x, y))

    profile_items = list(profiles.items())
    best = None
    empty_pair = None
    for left_index, (left_good, left_data) in enumerate(profile_items):
        for right_good, right_data in profile_items[left_index:]:
            intersection = set(left_good) & set(right_good)
            candidate = (len(intersection), left_good, left_data, right_good, right_data)
            if best is None or candidate[0] < best[0]:
                best = candidate
            if not intersection:
                empty_pair = candidate
                break
        if empty_pair is not None:
            break

    chosen = empty_pair if empty_pair is not None else best
    certificates = []
    intersection_labels = []
    if chosen is not None:
        _, left_good, left_data, right_good, right_data = chosen
        for good, data in ((left_good, left_data), (right_good, right_data)):
            first, second, x, y = data
            p_coefficients = tuple(
                biaffine_coefficients(terms[marked][0], first, second)
                for marked in range(len(graph_edges))
            )
            q_coefficients = tuple(
                biaffine_coefficients(terms[marked][1], first, second)
                for marked in range(len(graph_edges))
            )
            certificate = point_certificate((x, y), denominator, graph_edges, p_coefficients, q_coefficients)
            certificate["varied_edges"] = [list(graph_edges[first]), list(graph_edges[second])]
            assert tuple(
                index for index, marked in enumerate(graph_edges)
                if f"{marked[0]}{marked[1]}" in certificate["strict_good_edges"]
            ) == good
            certificates.append(certificate)
        intersection_labels = [
            f"{graph_edges[index][0]}{graph_edges[index][1]}"
            for index in set(left_good) & set(right_good)
        ]

    return {
        "host": name,
        "vertices": len(vertices),
        "edges": len(graph_edges),
        "varied_edge_pairs": len(graph_edges) * (len(graph_edges) - 1) // 2,
        "grid": {"denominator": denominator, "numerators": [-160, 80], "points_per_pair": len(grid) ** 2},
        "simultaneously_component_certified_points": certified_points,
        "distinct_strict_good_profiles": len(profiles),
        "empty_intersection_found": empty_pair is not None,
        "minimum_two_point_intersection_size": None if chosen is None else chosen[0],
        "minimum_intersection_edges": intersection_labels,
        "best_pair_certificates": certificates,
        "rejected_negative_barriers": rejected_barriers,
        "classification": "exact_two_coordinate_falsifier" if empty_pair is not None else "finite_exact_absence_only"
    }


def main() -> None:
    k4_vertices = tuple(range(4))
    k4_edges = tuple(edge(left, right) for left, right in combinations(k4_vertices, 2))
    w4_vertices = tuple(range(5))
    w4_edges = (
        edge(0, 1), edge(0, 2), edge(0, 3), edge(0, 4),
        edge(1, 2), edge(2, 3), edge(3, 4), edge(1, 4)
    )
    hosts = [
        analyze_host("K4", k4_vertices, k4_edges),
        analyze_host("W4", w4_vertices, w4_edges)
    ]
    killed = any(host["empty_intersection_found"] for host in hosts)
    print(json.dumps({
        "schema": "amra.opg1757.g201-multicoordinate-exact.v1",
        "method": "precomputed biaffine P_e,Q_e; exact rational grid; degree-two Bernstein-positive straight paths for every marked edge",
        "hosts": hosts,
        "G201_killed": killed,
        "mathematical_status": "refuted_on_displayed_host" if killed else "finite_exact_absence_only",
        "scope": "K4 and W4; exactly two varied edge activities; finite grid only",
        "phase_changed": False,
        "lean_used": False,
        "public_problem_changed": False
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
