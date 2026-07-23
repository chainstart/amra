#!/usr/bin/env python3
"""Exact certificate for the two-vertex extension obstruction in #757.

The only external mathematical input is Ma--Tang Lemma 2.4:
an n-point weak Sidon set has at most n-2 three-term APs.
All finite claims about the 14-point base hypergraph are checked here.
"""

from itertools import combinations


BASE = (0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056)


def is_45_set(points):
    for four in combinations(points, 4):
        distances = {abs(a - b) for a, b in combinations(four, 2)}
        if len(distances) < 5:
            return False
    return True


def ap_edges(points):
    result = []
    for i, j, k in combinations(range(len(points)), 3):
        if points[i] + points[k] == 2 * points[j]:
            result.append(frozenset((i, j, k)))
    return tuple(result)


def is_independent(vertices, edges):
    vertices = frozenset(vertices)
    return all(not edge <= vertices for edge in edges)


assert is_45_set(BASE)
old_edges = ap_edges(BASE)
assert len(old_edges) == 12

independent_eights = tuple(
    frozenset(vertices)
    for vertices in combinations(range(14), 8)
    if is_independent(vertices, old_edges)
)
assert len(independent_eights) == 143

# Exhaustive confirmation that alpha(H(BASE))=8.
assert independent_eights
assert not any(
    is_independent(vertices, old_edges) for vertices in combinations(range(14), 9)
)

# Add two abstract vertices u=14 and v=15.  Every possible new 3-edge
# contains at least one of them.
new_edges = tuple(
    frozenset(edge)
    for edge in combinations(range(16), 3)
    if 14 in edge or 15 in edge
)
assert len(new_edges) == 196


def old_maximum_set_survives(candidate_edges, added_vertices):
    """Some old maximum independent set remains independent with all new vertices."""
    for old_set in independent_eights:
        proposed = old_set | frozenset(added_vertices)
        if all(not edge <= proposed for edge in candidate_edges):
            return True
    return False


# One added point: at most one new AP edge.  Test every abstract possibility.
one_vertex_edges = tuple(edge for edge in new_edges if 15 not in edge)
for edge in one_vertex_edges:
    assert old_maximum_set_survives((edge,), (14,))

# Two added points: at most two new AP edges.  Empty and singleton choices are
# immediate; enumerate every pair of distinct possible edges.
assert old_maximum_set_survives((), (14, 15))
for edge in new_edges:
    assert old_maximum_set_survives((edge,), (14, 15))
for edge_a, edge_b in combinations(new_edges, 2):
    assert old_maximum_set_survives((edge_a, edge_b), (14, 15))

print(
    {
        "status": "PASS",
        "base_size": len(BASE),
        "base_ap_edges": len(old_edges),
        "base_independence_number": 8,
        "base_maximum_independent_sets": len(independent_eights),
        "abstract_new_edges_tested": len(new_edges),
        "new_edge_pairs_tested": len(tuple(combinations(new_edges, 2))),
        "conclusion": (
            "any weak-Sidon one-point extension has alpha>=9; "
            "any weak-Sidon two-point extension has alpha>=10"
        ),
        "scope": "finite hypergraph obstruction; no improvement of 9/17 or 4/7",
    }
)

