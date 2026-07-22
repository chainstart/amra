#!/usr/bin/env python3
"""Exact finite audits for the round-9 #1083 defect/pencil lemmas.

This is not a proof of an asymptotic statement.  It independently enumerates
integer point sets, their generated perpendicular-bisector planes, the
reflection matchings, isosceles flags, and every axis line determined by two
input points.  All arithmetic is integral after canonical normalization.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import gcd
import json


Point = tuple[int, int, int]
Plane = tuple[int, int, int, int]  # ax+by+cz=d, primitive and signed
Line = tuple[int, int, int, int, int, int]  # Pluecker (direction, moment)


def gcd_many(values: tuple[int, ...]) -> int:
    out = 0
    for value in values:
        out = gcd(out, abs(value))
    return out


def canonical_signed(values: tuple[int, ...]) -> tuple[int, ...]:
    divisor = gcd_many(values)
    assert divisor
    values = tuple(value // divisor for value in values)
    for value in values:
        if value:
            return values if value > 0 else tuple(-x for x in values)
    raise AssertionError("zero tuple")


def bisector(a: Point, b: Point) -> Plane:
    normal = tuple(2 * (b[i] - a[i]) for i in range(3))
    rhs = sum(x * x for x in b) - sum(x * x for x in a)
    return canonical_signed((*normal, rhs))  # type: ignore[return-value]


def on_plane(point: Point, plane: Plane) -> bool:
    return sum(plane[i] * point[i] for i in range(3)) == plane[3]


def cross(a: Point, b: Point) -> Point:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def subtract(a: Point, b: Point) -> Point:
    return tuple(a[i] - b[i] for i in range(3))  # type: ignore[return-value]


def primitive_direction(a: Point, b: Point) -> Point:
    d = subtract(b, a)
    divisor = gcd_many(d)
    d = tuple(value // divisor for value in d)
    for value in d:
        if value:
            return d if value > 0 else tuple(-x for x in d)  # type: ignore[return-value]
    raise AssertionError("equal points")


def canonical_line_coordinates(direction: Point, moment: Point) -> Line:
    return canonical_signed((*direction, *moment))  # type: ignore[return-value]


def canonical_line(a: Point, b: Point) -> Line:
    # Pluecker-style affine encoding: direction d and moment a x d.
    d = primitive_direction(a, b)
    return canonical_line_coordinates(d, cross(a, d))


def intersection_line(first: Plane, second: Plane) -> Line | None:
    n1 = first[:3]
    n2 = second[:3]
    direction = cross(n1, n2)  # type: ignore[arg-type]
    if direction == (0, 0, 0):
        return None
    # For p on both planes, p x (n1 x n2)=n1(p.n2)-n2(p.n1).
    moment = tuple(
        second[3] * n1[i] - first[3] * n2[i] for i in range(3)
    )
    return canonical_line_coordinates(direction, moment)  # type: ignore[arg-type]


def on_line(point: Point, line: Line) -> bool:
    d = line[:3]
    moment = line[3:]
    return cross(point, d) == moment  # type: ignore[arg-type]


def line_in_plane(line: Line, plane: Plane) -> bool:
    d = line[:3]
    moment = line[3:]
    normal = plane[:3]
    if sum(normal[i] * d[i] for i in range(3)) != 0:
        return False
    # d x (p x d)=|d|^2 p modulo the direction d; normal.d=0.
    projected_numerator = cross(d, moment)  # type: ignore[arg-type]
    norm_squared = sum(value * value for value in d)
    return sum(
        normal[i] * projected_numerator[i] for i in range(3)
    ) == plane[3] * norm_squared


def squared_distance(a: Point, b: Point) -> int:
    return sum((a[i] - b[i]) ** 2 for i in range(3))


def analyse(points: list[Point]) -> dict[str, object]:
    assert len(points) == len(set(points))
    n = len(points)
    distance_values = {
        squared_distance(a, b) for a, b in combinations(points, 2)
    }
    D = len(distance_values)

    generators: dict[Plane, list[tuple[Point, Point]]] = defaultdict(list)
    for a, b in combinations(points, 2):
        generators[bisector(a, b)].append((a, b))

    q: dict[Plane, int] = {
        plane: sum(on_plane(x, plane) for x in points)
        for plane in generators
    }
    g = {plane: len(edges) for plane, edges in generators.items()}
    e = {plane: n - q[plane] - 2 * g[plane] for plane in generators}
    assert all(value >= 0 for value in e.values())
    assert sum(g.values()) == n * (n - 1) // 2

    grouped_isosceles = sum(g[plane] * q[plane] for plane in generators)
    direct_isosceles = 0
    for vertex in points:
        multiplicities: dict[int, int] = defaultdict(int)
        for other in points:
            if other != vertex:
                multiplicities[squared_distance(vertex, other)] += 1
        direct_isosceles += sum(m * (m - 1) // 2 for m in multiplicities.values())
    assert grouped_isosceles == direct_isosceles

    reflection_maps: dict[Plane, dict[Point, Point]] = {}
    for plane, edges in generators.items():
        mapping = {x: x for x in points if on_plane(x, plane)}
        for a, b in edges:
            mapping[a] = b
            mapping[b] = a
        assert len(mapping) == q[plane] + 2 * g[plane]
        reflection_maps[plane] = mapping

    # The one-step domain of s_pi s_sigma has exactly the size of the
    # intersection of the two individual reflection domains.
    composition_pairs_checked = 0
    maximum_composition_domain = 0
    overlap_sum = 0
    for first, second in combinations(generators, 2):
        direct_domain = sum(
            point in reflection_maps[second]
            and reflection_maps[second][point] in reflection_maps[first]
            for point in points
        )
        intersection_domain = len(
            reflection_maps[first].keys() & reflection_maps[second].keys()
        )
        assert direct_domain == intersection_domain
        composition_pairs_checked += 1
        overlap_sum += intersection_domain
        maximum_composition_domain = max(
            maximum_composition_domain, direct_domain
        )
    domain_degrees = {
        point: sum(point in mapping for mapping in reflection_maps.values())
        for point in points
    }
    assert overlap_sum == sum(
        degree * (degree - 1) // 2 for degree in domain_degrees.values()
    )

    # For every q-rich subfamily, a parallel class has at most n/q planes.
    # Canonicalizing the normal separately identifies its projective direction.
    for threshold in sorted(set(q.values())):
        if threshold == 0:
            continue
        direction_classes: dict[tuple[int, int, int], int] = defaultdict(int)
        family_size = 0
        for plane in generators:
            if q[plane] < threshold:
                continue
            normal = canonical_signed(plane[:3])
            direction_classes[normal] += 1  # type: ignore[index]
            family_size += 1
        assert all(size * threshold <= n for size in direction_classes.values())
        parallel_pairs = sum(
            size * (size - 1) // 2 for size in direction_classes.values()
        )
        assert 2 * threshold * parallel_pairs <= n * family_size

    # Point-determined lines test axes rich in P.  Pairwise intersections of
    # generated planes additionally test the important axes containing no P
    # points (for example central axes of cubes and regular polygons).
    lines = {canonical_line(a, b) for a, b in combinations(points, 2)}
    for first, second in combinations(generators, 2):
        line = intersection_line(first, second)
        if line is not None:
            lines.add(line)
    maximum_pencil_generator_sum = 0
    maximum_pencil_flag_sum = 0
    pencil_count = 0
    for line in lines:
        line_points = [x for x in points if on_line(x, line)]
        ell = len(line_points)
        pencil = [plane for plane in generators if line_in_plane(line, plane)]
        if not pencil:
            continue
        pencil_count += 1
        generator_sum = sum(g[plane] for plane in pencil)
        flag_sum = sum(g[plane] * q[plane] for plane in pencil)
        assert generator_sum <= D * n
        assert flag_sum <= (
            ell * D * n + Fraction((n - ell) * (n - ell - 1), 2)
        )
        maximum_pencil_generator_sum = max(
            maximum_pencil_generator_sum, generator_sum
        )
        maximum_pencil_flag_sum = max(maximum_pencil_flag_sum, flag_sum)

    return {
        "n": n,
        "distinct_distances": D,
        "generated_planes": len(generators),
        "isosceles_flags": grouped_isosceles,
        "maximum_defect": max(e.values(), default=0),
        "minimum_defect": min(e.values(), default=0),
        "axis_lines_checked": pencil_count,
        "composition_pairs_checked": composition_pairs_checked,
        "maximum_composition_domain": maximum_composition_domain,
        "maximum_pencil_generator_sum": maximum_pencil_generator_sum,
        "maximum_pencil_flag_sum": maximum_pencil_flag_sum,
    }


def main() -> None:
    samples: dict[str, list[Point]] = {
        "cube_2": list(product(range(2), repeat=3)),
        "grid_2x2x3": list(product(range(2), range(2), range(3))),
        "octahedron": [
            (1, 0, 0), (-1, 0, 0), (0, 1, 0),
            (0, -1, 0), (0, 0, 1), (0, 0, -1),
        ],
        "asymmetric_7": [
            (0, 0, 0), (1, 2, 0), (3, 1, 1), (2, 5, 1),
            (7, 0, 2), (1, 1, 4), (4, 3, 6),
        ],
    }
    results = {name: analyse(points) for name, points in samples.items()}
    print(json.dumps({
        "schema": "amra.erdos1083.round9.defect_pencil_audit.v1",
        "arithmetic": "exact integers and rational comparison",
        "samples": results,
        "identities_checked": [
            "sum_pi g_pi = binom(n,2)",
            "sum_pi g_pi q_pi = direct unordered isosceles count",
            "e_pi = n-q_pi-2g_pi >= 0",
            "sum_{pi contains L} g_pi <= D n",
            "sum_{pi contains L} g_pi q_pi <= ell D n +(n-ell)(n-ell-1)/2",
            "|Dom(s_pi s_sigma)| = |S_pi intersect S_sigma|",
            "sum pairwise domain overlaps = sum_x binom(domain_degree_x,2)",
            "every q-rich parallel class has at most n/q planes",
        ],
        "warning": "finite audit only; universal proofs are in REPORT.md",
        "result": "PASS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
