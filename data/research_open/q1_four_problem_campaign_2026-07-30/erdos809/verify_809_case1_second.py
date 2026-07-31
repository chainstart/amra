#!/usr/bin/env python3
"""Finite guards for the second fixed-s Case-1 attack.

The checks are deliberately finite:

1. for disjoint induced edge pairs, C7 compatibility is equivalent to a
   vertex-disjoint (2,3)-path linkage under one of the two endpoint pairings;
2. a non-linked distance-two orientation gives the advertised deleted
   three-vertex/no-three-path certificate;
3. a distance-three orientation has outer endpoints of codegree zero;
4. the inherited "use only the two dense interiors" estimate has the
   recorded normalized barrier.

No finite check is promoted to an asymptotic theorem.
"""

from __future__ import annotations

import itertools
import json
import random

Edge = tuple[int, int]


def edge(u: int, v: int) -> Edge:
    assert u != v
    return (u, v) if u < v else (v, u)


def neighborhoods(n: int, edges: set[Edge]) -> list[set[int]]:
    out = [set() for _ in range(n)]
    for u, v in edges:
        out[u].add(v)
        out[v].add(u)
    return out


def simple_paths(
    n: int, edges: set[Edge], start: int, end: int, length: int
) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []

    def visit(path: tuple[int, ...]) -> None:
        if len(path) == length + 1:
            if path[-1] == end:
                result.append(path)
            return
        for nxt in range(n):
            if nxt in path or edge(path[-1], nxt) not in edges:
                continue
            if nxt == end and len(path) != length:
                continue
            visit(path + (nxt,))

    visit((start,))
    return result


def has_23_linkage(
    n: int, edges: set[Edge], first: Edge, second: Edge
) -> bool:
    a, b = first
    c, d = second
    pairings = (
        ((a, c), (b, d)),
        ((a, d), (b, c)),
    )
    for (u, v), (x, y) in pairings:
        for left_length, right_length in ((2, 3), (3, 2)):
            left_paths = simple_paths(
                n, edges, u, v, left_length
            )
            right_paths = simple_paths(
                n, edges, x, y, right_length
            )
            for left in left_paths:
                for right in right_paths:
                    if set(left).isdisjoint(right):
                        return True
    return False


def cycle_compatible_pairs(
    n: int, edges: set[Edge]
) -> set[tuple[Edge, Edge]]:
    covered: set[tuple[Edge, Edge]] = set()
    for vertices in itertools.combinations(range(n), 7):
        root = vertices[0]
        for tail in itertools.permutations(vertices[1:]):
            if tail[0] > tail[-1]:
                continue
            cycle = (root,) + tail
            used = {
                edge(cycle[index], cycle[(index + 1) % 7])
                for index in range(7)
            }
            if not used <= edges:
                continue
            for pair in itertools.combinations(sorted(used), 2):
                covered.add(pair)
    return covered


def is_induced_edge_pair(edges: set[Edge], first: Edge, second: Edge) -> bool:
    if set(first) & set(second):
        return False
    return not any(
        edge(x, y) in edges for x in first for y in second
    )


def exact_linkage_guard(samples: int = 240) -> dict[str, int | bool]:
    rng = random.Random(809_20260730)
    induced_pairs = 0
    linked_pairs = 0
    unlinked_pairs = 0
    distance_two_certificates = 0
    distance_three_certificates = 0

    for sample in range(samples):
        n = 7 + sample % 3
        probability = 0.28 + 0.58 * rng.random()
        edges = {
            edge(u, v)
            for u in range(n)
            for v in range(u + 1, n)
            if rng.random() < probability
        }
        neigh = neighborhoods(n, edges)
        covered = cycle_compatible_pairs(n, edges)

        for first, second in itertools.combinations(sorted(edges), 2):
            if not is_induced_edge_pair(edges, first, second):
                continue
            induced_pairs += 1
            linked = has_23_linkage(n, edges, first, second)
            compatible = (first, second) in covered
            assert linked == compatible
            if linked:
                linked_pairs += 1
                continue
            unlinked_pairs += 1

            # Check every oriented distance-two inner path.  Its complementary
            # outer endpoints cannot have a disjoint length-three path.
            for x, y in (first, first[::-1]):
                for z, w in (second, second[::-1]):
                    for a in neigh[x] & neigh[z]:
                        forbidden = {x, a, z}
                        outer_paths = simple_paths(n, edges, y, w, 3)
                        assert not any(
                            set(path).isdisjoint(forbidden)
                            for path in outer_paths
                        )
                        distance_two_certificates += 1

                    # If this orientation has a simple inner length-three
                    # path and no shorter cross-endpoint route, the two outer
                    # endpoints have no common neighbour.
                    cross_pairs = [
                        (u, v) for u in first for v in second
                    ]
                    if (
                        all(not (neigh[u] & neigh[v]) for u, v in cross_pairs)
                        and simple_paths(n, edges, x, z, 3)
                    ):
                        assert not (neigh[y] & neigh[w])
                        distance_three_certificates += 1

    assert induced_pairs > 0
    assert linked_pairs > 0
    assert unlinked_pairs > 0
    assert distance_two_certificates > 0
    assert distance_three_certificates > 0
    return {
        "random_graphs": samples,
        "induced_edge_pairs": induced_pairs,
        "linked_pairs": linked_pairs,
        "unlinked_pairs": unlinked_pairs,
        "distance_two_certificates": distance_two_certificates,
        "distance_three_certificates": distance_three_certificates,
        "passed": True,
    }


def normalized_barrier_guard(denominator: int = 10000) -> dict[str, object]:
    """Locate the exact crossover of the two-interior lower bound.

    In the empty-intersection distance-two branch, using only the guaranteed
    internal degrees of P and Q gives

        L(s) = (1-2s)(1/2-3s)/2.

    The BCM target is

        T(s) = 1/8+s/2+s^2/2.

    Their difference is 1/8-(5/2)s+(5/2)s^2 and changes sign at
    (1-sqrt(4/5))/2.
    """
    crossover = (1 - (4 / 5) ** 0.5) / 2
    last_success = 0.0
    first_failure = None
    for index in range(denominator // 2 + 1):
        s = index / denominator
        internal = (1 - 2 * s) * (0.5 - 3 * s) / 2
        target = 0.125 + s / 2 + s * s / 2
        if internal + 1e-15 >= target:
            last_success = s
        elif first_failure is None:
            first_failure = s
    assert abs(crossover - 0.05278640450004207) < 1e-12
    return {
        "crossover": crossover,
        "last_grid_success": last_success,
        "first_grid_failure": first_failure,
        "interpretation": (
            "Even granting cross-block colour separation, the inherited "
            "two-interior estimate cannot reach the target beyond this s."
        ),
        "passed": True,
    }


def main() -> None:
    result = {
        "exact_linkage": exact_linkage_guard(),
        "normalized_barrier": normalized_barrier_guard(),
        "scope": (
            "Finite guards verify the exact C7/linkage equivalence and "
            "displayed arithmetic only; they do not prove Erdős #809."
        ),
        "passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
