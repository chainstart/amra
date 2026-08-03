#!/usr/bin/env python3
"""Exact one-coordinate falsification search for G201's fixed-edge quantifier.

Every reported point is simultaneously connected to the positive orthant in
each marked-edge deletion component by its one-coordinate line segment.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json


def is_connected(n: int, edges: tuple[tuple[int, int], ...]) -> bool:
    if n == 0:
        return True
    seen = {0}
    changed = True
    while changed:
        changed = False
        for left, right in edges:
            if left in seen and right not in seen:
                seen.add(right); changed = True
            if right in seen and left not in seen:
                seen.add(left); changed = True
    return len(seen) == n


def is_forest(n: int, edges: tuple[tuple[int, int], ...]) -> tuple[bool, list[int]]:
    parent = list(range(n))

    def find(v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for left, right in edges:
        rl, rr = find(left), find(right)
        if rl == rr:
            return False, parent
        parent[rl] = rr
    for v in range(n):
        parent[v] = find(v)
    return True, parent


def has_bridge(n: int, edges: tuple[tuple[int, int], ...]) -> bool:
    return any(not is_connected(n, edges[:index] + edges[index + 1:])
               for index in range(len(edges)))


def coefficient_table(n: int, edges: tuple[tuple[int, int], ...]):
    """For marked e and varied f return P=A*t+B and Q=C*t+D."""
    m = len(edges)
    table = {}
    for marked in range(m):
        remaining = [index for index in range(m) if index != marked]
        data = {varied: [0, 0, 0, 0] for varied in range(m)}  # A,B,C,D
        for mask in range(1 << len(remaining)):
            chosen_indices = tuple(remaining[i] for i in range(len(remaining)) if mask >> i & 1)
            chosen_edges = tuple(edges[i] for i in chosen_indices)
            forest, parent = is_forest(n, chosen_edges)
            if not forest:
                continue
            ml, mr = edges[marked]
            connected_endpoints = parent[ml] == parent[mr]
            chosen_set = set(chosen_indices)
            for varied in range(m):
                # Complement monomial contains varied iff it was not chosen;
                # the marked edge is absent from every complement.
                exponent_one = varied != marked and varied not in chosen_set
                if exponent_one:
                    data[varied][0] += 1
                    if connected_endpoints:
                        data[varied][2] += 1
                else:
                    data[varied][1] += 1
                    if connected_endpoints:
                        data[varied][3] += 1
        for varied, values in data.items():
            table[(marked, varied)] = tuple(values)
    return table


def profiles_for_graph(n: int, edges: tuple[tuple[int, int], ...]):
    table = coefficient_table(n, edges)
    m = len(edges)
    profiles = []
    for varied in range(m):
        lower = None
        for marked in range(m):
            A, B, _, _ = table[(marked, varied)]
            if A:
                root = Fraction(-B, A)
                lower = root if lower is None else max(lower, root)
        assert lower is not None

        roots = sorted({Fraction(-D, C) for marked in range(m)
                        for _, _, C, D in [table[(marked, varied)]]
                        if C and Fraction(-D, C) > lower})
        candidates = []
        boundaries = [lower] + roots
        for left, right in zip(boundaries, roots):
            if left < right:
                candidates.append((left + right) / 2)
        candidates.extend(roots)  # exact xi=0 points are valid strict failures
        candidates.append((roots[-1] if roots else lower) + 1)

        for value in candidates:
            if value <= lower:
                continue
            p_values = []
            q_values = []
            for marked in range(m):
                A, B, C, D = table[(marked, varied)]
                p = A * value + B
                q = C * value + D
                assert p > 0
                # P is affine and positive at value and at t=1, so the whole
                # line segment is a certified path inside P>0.
                assert A + B > 0
                p_values.append(p)
                q_values.append(q)
            good = frozenset(index for index, q in enumerate(q_values) if q > 0)
            profiles.append({
                "varied": varied, "value": value, "lower": lower,
                "good": good, "P": p_values, "Q": q_values,
            })
    # One representative per exact good-edge set is enough for intersection.
    unique = {}
    for profile in profiles:
        unique.setdefault(profile["good"], profile)
    return list(unique.values()), len(profiles), table


def encode_profile(profile, edges):
    return {
        "varied_edge": list(edges[profile["varied"]]),
        "value": str(profile["value"]),
        "component_lower_bound": str(profile["lower"]),
        "good_edges": [list(edges[index]) for index in sorted(profile["good"])],
        "P_values": [str(value) for value in profile["P"]],
        "xi_values": [str(value) for value in profile["Q"]],
    }


def main() -> None:
    graph_count = 0
    profile_count = 0
    rational_point_count = 0
    graphs_with_shrunk_good_set = 0
    best = None
    exact_pair = None
    for n in range(3, 6):
        possible = tuple(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = tuple(possible[i] for i in range(len(possible)) if mask >> i & 1)
            if len(edges) < n or not is_connected(n, edges) or has_bridge(n, edges):
                continue
            graph_count += 1
            profiles, raw_points, _ = profiles_for_graph(n, edges)
            profile_count += len(profiles)
            rational_point_count += raw_points
            full = frozenset(range(len(edges)))
            if any(profile["good"] != full for profile in profiles):
                graphs_with_shrunk_good_set += 1
            for first_index, first in enumerate(profiles):
                intersection = first["good"]
                candidate = (len(intersection), n, edges, [first])
                if best is None or candidate[0] < best[0]:
                    best = candidate
                for second in profiles[first_index + 1:]:
                    common = first["good"] & second["good"]
                    candidate = (len(common), n, edges, [first, second])
                    if best is None or candidate[0] < best[0]:
                        best = candidate
                    if not common:
                        exact_pair = (n, edges, first, second)
                        break
                if exact_pair:
                    break
            if exact_pair:
                break
        if exact_pair:
            break

    result = {
        "schema": "amra.opg1757.g201-fixed-edge-falsification.v1",
        "definition": {
            "pointwise_good": "p_-e lies in distinguished component of C_(G\\e)>0 and xi_e(p)>0",
            "fixed_edge_claim": "there exists one ordinary edge e good at every point of its distinguished deletion component",
            "strict_kill": "for every edge e, exhibit a component-valid point with xi_e<=0",
            "coloop_boundary": "xi=0 for a coloop is handled by the exceptional recursion and is not used as a quantifier kill",
        },
        "search": {
            "connected_bridgeless_labelled_graphs": graph_count,
            "maximum_vertices": 5,
            "exact_one_coordinate_profiles": profile_count,
            "certified_rational_points_before_good_set_deduplication": rational_point_count,
            "graphs_with_any_shrunk_good_edge_set": graphs_with_shrunk_good_set,
            "membership": "affine P_e(t)>0 along the full segment from rational t to 1, simultaneously for every marked edge",
        },
        "exact_two_point_falsifier": None,
        "minimum_common_edge_intersection": best[0] if best else None,
        "best_finite_profile": None,
        "public_problem_changed": False,
    }
    if exact_pair:
        n, edges, first, second = exact_pair
        result["exact_two_point_falsifier"] = {
            "vertices": n,
            "edges": [list(edge) for edge in edges],
            "point_1": encode_profile(first, edges),
            "point_2": encode_profile(second, edges),
            "common_good_edges": [],
            "interpretation": "Every edge has xi<=0 at at least one point on its own certified deletion component; no globally fixed edge works."
        }
    elif best:
        _, n, edges, chosen = best
        result["best_finite_profile"] = {
            "vertices": n,
            "edges": [list(edge) for edge in edges],
            "points": [encode_profile(profile, edges) for profile in chosen],
            "common_good_edges": [list(edges[index]) for index in sorted(set.intersection(*(set(p["good"]) for p in chosen)))],
            "scope": "finite one-coordinate search only; no absence theorem on full components"
        }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
