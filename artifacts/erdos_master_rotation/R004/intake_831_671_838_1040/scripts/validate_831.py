#!/usr/bin/env python3
"""Exact certificates for the two local obstructions found for Erdős #831."""

from fractions import Fraction as Q
from itertools import combinations
from sympy import expand, symbols


Point = tuple[Q, Q]


def det2(a: Point, b: Point, c: Point) -> Q:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def dist2(a: Point, b: Point) -> Q:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def circumradius2(a: Point, b: Point, c: Point) -> Q:
    # R^2 = |AB|^2 |AC|^2 |BC|^2 / (4 det(AB,AC)^2).
    d = det2(a, b, c)
    assert d != 0
    return dist2(a, b) * dist2(a, c) * dist2(b, c) / (4 * d * d)


def concyclicity_det(a: Point, b: Point, c: Point, d: Point) -> Q:
    """The 4x4 determinant of rows (x,y,x^2+y^2,1), by elimination."""
    rows = [[p[0], p[1], p[0] * p[0] + p[1] * p[1], Q(1)] for p in (a, b, c, d)]
    total = Q(0)
    for perm in __import__("itertools").permutations(range(4)):
        inv = sum(perm[i] > perm[j] for i in range(4) for j in range(i + 1, 4))
        term = Q(-1 if inv % 2 else 1)
        for i in range(4):
            term *= rows[i][perm[i]]
        total += term
    return total


def check_orthocentric_k4() -> None:
    # H is the orthocentre of ABC.
    points: list[Point] = [
        (Q(0), Q(0)),
        (Q(4), Q(0)),
        (Q(1), Q(2)),
        (Q(1), Q(3, 2)),
    ]
    radii = {
        triple: circumradius2(*(points[i] for i in triple))
        for triple in combinations(range(4), 3)
    }
    assert set(radii.values()) == {Q(65, 16)}
    assert all(det2(*(points[i] for i in triple)) != 0 for triple in combinations(range(4), 3))
    assert concyclicity_det(*points) != 0

    pair_codegrees = {
        pair: sum(set(pair) <= set(triple) for triple in radii)
        for pair in combinations(range(4), 2)
    }
    assert set(pair_codegrees.values()) == {2}
    assert len(radii) == 2 * len(pair_codegrees) // 3 == 4
    print("ORTHOCENTRIC_K4_OK")
    print("common_R_squared=65/16")
    print(f"four_point_concyclicity_determinant={concyclicity_det(*points)}")
    print("all_six_pair_codegrees=2")


SATURATED_DESIGNS = {
    6: [
        (0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5), (0, 4, 5),
        (1, 2, 5), (1, 3, 4), (1, 4, 5), (2, 3, 4), (2, 3, 5),
    ],
    7: [
        (0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5), (0, 4, 6),
        (0, 5, 6), (1, 2, 5), (1, 3, 6), (1, 4, 5), (1, 4, 6),
        (2, 3, 4), (2, 3, 6), (2, 5, 6), (3, 4, 5),
    ],
}


def check_combinatorial_saturation() -> None:
    for n, edges in SATURATED_DESIGNS.items():
        edge_set = set(edges)
        assert len(edge_set) == 2 * __import__("math").comb(n, 2) // 3
        for pair in combinations(range(n), 2):
            assert sum(set(pair) <= set(edge) for edge in edge_set) == 2
        k4_count = sum(
            all(tuple(sorted(t)) in edge_set for t in combinations(vertices, 3))
            for vertices in combinations(range(n), 4)
        )
        assert k4_count == 0
        # The link at every vertex is a connected 2-regular graph, hence the
        # single cycle C_(n-1).  This is the exact local normal form that a
        # hypothetical congruent-circle realization would have to respect.
        link_cycle_lengths = []
        for vertex in range(n):
            link_vertices = set(range(n)) - {vertex}
            link_edges = {
                tuple(sorted(set(edge) - {vertex}))
                for edge in edge_set
                if vertex in edge
            }
            degrees = {
                x: sum(x in link_edge for link_edge in link_edges)
                for x in link_vertices
            }
            assert set(degrees.values()) == {2}
            seen = set()
            stack = [next(iter(link_vertices))]
            while stack:
                x = stack.pop()
                if x in seen:
                    continue
                seen.add(x)
                stack.extend(
                    y
                    for link_edge in link_edges
                    if x in link_edge
                    for y in link_edge
                    if y != x
                )
            assert seen == link_vertices
            link_cycle_lengths.append(len(seen))
        assert set(link_cycle_lengths) == {n - 1}
        print(
            f"TWO_DESIGN_{n}_OK edges={len(edge_set)} K4_3={k4_count} "
            f"all_links=C{n - 1}"
        )


def check_six_vertex_symbolic_obstruction() -> None:
    # In the notation of REPORT_831, the two remaining-circle conditions are
    # |X+e|^2=1 and |-X+e|^2=1, while |e|^2=1.  Their sum is exactly
    # 2|X|^2, forcing X=0 over R.  The following is an exact polynomial
    # identity, not a floating-point check.
    x, y, u, v = symbols("x y u v", real=True)
    q_plus = (x + u) ** 2 + (y + v) ** 2 - 1
    q_minus = (-x + u) ** 2 + (-y + v) ** 2 - 1
    unit = u**2 + v**2 - 1
    assert expand(q_plus + q_minus - 2 * (x**2 + y**2) - 2 * unit) == 0
    print("SIX_VERTEX_REALIZABILITY_OBSTRUCTION_OK")
    print("|X+e|=|-X+e|=|e|=1 implies X=0, hence p2=p5")


if __name__ == "__main__":
    check_orthocentric_k4()
    check_combinatorial_saturation()
    check_six_vertex_symbolic_obstruction()
