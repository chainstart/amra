#!/usr/bin/env python3
"""Independent cross-audit guard for the frozen Erdős #809 transfer.

No author verifier is imported.  The scalar ledger is rebuilt with integer
arithmetic and the sharp graphs are reconstructed directly from their cyclic
interval definition.
"""

from __future__ import annotations

from collections import deque
import json


def choose2(value: int) -> int:
    return value * (value - 1) // 2


def scalar_audit() -> dict[str, int]:
    profiles = 0
    feasible_profiles = 0
    near_band_profiles = 0
    boundary_rows = 0

    for parity in (0, 1):
        for g in range(4, 81):
            base_a = 2 if parity == 0 else 1
            shift_threshold = 8 if parity == 0 else 6
            min_h_cost = None
            min_shift_cost = None
            for a in range(base_a, 2 * g - 2, 2):
                kappa = 2 * g - a
                if kappa < 3:
                    continue
                assert a % 2 == parity
                for h in range(0, kappa - 2):
                    assert 0 <= h <= kappa - 3 == 2 * g - a - 3
                    h_cost = h * (2 * g - h - 1)
                    a_cost = (
                        (a - 2) * (a + 4) // 2
                        if parity == 0
                        else (a - 1) * (a + 3) // 2
                    )
                    if h >= 1:
                        min_h_cost = h_cost if min_h_cost is None else min(min_h_cost, h_cost)
                    if a != base_a:
                        min_shift_cost = a_cost if min_shift_cost is None else min(min_shift_cost, a_cost)
                    for u in range(0, h + 1):
                        profiles += 1
                        energy = a_cost + h_cost + 2 * u * (h - u)
                        for delta in (3, g + 2, g * g + 5):
                            kappa = 2 * g - a
                            n = 2 * delta + kappa
                            d = kappa - h - 1
                            p = delta + u
                            maximum_degree = delta + g
                            assert 2 <= d <= kappa - 1
                            assert delta <= p <= delta + h
                            assert n - d - 1 == 2 * delta + h

                            missing = choose2(n) - (n * n // 4 + 1)
                            relaxed = (
                                p * (n - d - 1 - p)
                                + n
                                - 1
                                + (d - 1) * (n - 2 - maximum_degree)
                                - choose2(d - 1)
                            )
                            endpoint = (
                                delta * (n - d - 1 - delta)
                                + n
                                - 1
                                + (d - 1) * (n - 2 - maximum_degree)
                                - choose2(d - 1)
                            )
                            assert relaxed - endpoint == u * (h - u)

                            if parity == 0:
                                remainder = a * a - 4 + 2 * h * (2 * g - h - 1)
                                assert remainder % 4 == 0
                                expected_difference = (
                                    delta - g * g + 2 * g + 2
                                    + remainder // 4 + u * (h - u)
                                )
                                delta_star = g * g - 2 * g - 2
                                n_star = 2 * g * g - 2 * g - 6
                            else:
                                remainder = a * a - 1 + 2 * h * (2 * g - h - 1)
                                assert remainder % 4 == 0
                                expected_difference = (
                                    delta - g * g + 2 * g + 1
                                    + remainder // 4 + u * (h - u)
                                )
                                delta_star = g * g - 2 * g - 1
                                n_star = 2 * g * g - 2 * g - 3

                            difference = relaxed - missing
                            assert difference == expected_difference
                            vertex_deficit = n_star - n
                            assert vertex_deficit == 2 * (delta_star - delta) + (a - base_a)
                            assert vertex_deficit % 2 == 0
                            assert vertex_deficit - energy == -2 * difference
                            assert (relaxed <= missing) == (vertex_deficit >= energy)

                            if relaxed <= missing:
                                feasible_profiles += 1
                                assert (a + 1) ** 2 <= (
                                    2 * vertex_deficit + (9 if parity == 0 else 4)
                                )
                                if h > 0:
                                    assert min(u, h - u) * h <= vertex_deficit

                        near_threshold = min(shift_threshold, 2 * g - 2)
                        if energy < near_threshold:
                            near_band_profiles += 1
                            assert a == base_a and h == 0 and u == 0

            assert min_shift_cost == shift_threshold
            assert min_h_cost == 2 * g - 2
            boundary_rows += 2

    # Hostile sign check: at an interior centre the concavity remainder is
    # positive, so replacing +u(h-u) by a minus sign is false.
    g, a, h, u, delta = 5, 2, 2, 1, 7
    kappa = 2 * g - a
    n = 2 * delta + kappa
    d = kappa - h - 1
    p = delta + u
    common = (d - 1) * (n - 2 - (delta + g)) - choose2(d - 1)
    centre = p * (n - d - 1 - p) + n - 1 + common
    endpoint = delta * (n - d - 1 - delta) + n - 1 + common
    assert centre - endpoint == 1

    return {
        "scalar_profiles": profiles,
        "feasible_profile_instances": feasible_profiles,
        "near_band_profiles": near_band_profiles,
        "boundary_checks": boundary_rows,
    }


def add_edge(adjacency: list[set[int]], left: int, right: int) -> None:
    assert left != right
    adjacency[left].add(right)
    adjacency[right].add(left)


def distance(adjacency: list[set[int]], source: int, target: int) -> int:
    queue = deque([(source, 0)])
    seen = {source}
    while queue:
        vertex, depth = queue.popleft()
        if vertex == target:
            return depth
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append((neighbour, depth + 1))
    raise AssertionError("sharp graph unexpectedly disconnected")


def build_sharp_graph(g: int, parity: int):
    delta = g * g - 2 * g - (2 if parity == 0 else 1)
    kappa = 2 * g - (2 if parity == 0 else 1)
    maximum_degree = delta + g
    P = list(range(delta))
    U = list(range(delta, 2 * delta))
    b = 2 * delta
    c = b + 1
    W = list(range(c + 1, c + 1 + kappa - 2))
    n = len(P) + len(U) + 2 + len(W)
    adjacency = [set() for _ in range(n)]

    for block, hub in ((P, b), (U, c)):
        for i, left in enumerate(block):
            add_edge(adjacency, hub, left)
            for right in block[i + 1 :]:
                add_edge(adjacency, left, right)

    cyclic = P + U
    for index, w in enumerate(W):
        start = index * maximum_degree
        for offset in range(maximum_degree):
            add_edge(adjacency, w, cyclic[(start + offset) % (2 * delta)])

    return adjacency, P, U, b, c, W, delta, kappa, maximum_degree


def graph_audit() -> dict[str, int]:
    graph_rows = 0
    repeated_classes = 0
    reserve_pairs_checked = 0
    g4_boundary_rows = 0
    l4_eligible_rows = 0

    for parity in (0, 1):
        for g in range(4, 13):
            adjacency, P, U, b, c, W, delta, kappa, maximum_degree = build_sharp_graph(g, parity)
            n = len(adjacency)
            edge_count = sum(map(len, adjacency)) // 2
            assert edge_count == n * n // 4 + 1
            degrees = [len(row) for row in adjacency]
            assert min(degrees) == delta
            assert max(degrees) == maximum_degree
            assert all(len(adjacency[w] & set(P)) >= g for w in W)
            assert all(len(adjacency[w] & set(U)) >= g for w in W)
            assert not (set(P) & set(U))
            assert all(u not in adjacency[p] for p in P for u in U)
            assert adjacency[b] == set(P)
            assert adjacency[c] == set(U)

            if g == 4:
                g4_boundary_rows += 1
            else:
                l4_eligible_rows += 1

            v = W[0]
            A = set(adjacency[v]) | {v}
            B = set(range(n)) - A
            assert b in B and c in B
            xs = sorted(A & set(P))[:g]
            ys = sorted(A & set(U))[:g]
            assert len(xs) == len(ys) == g

            # Deleting the two repeated edges from a C7 leaves one of two
            # endpoint pairings whose path lengths sum to five.  Both
            # pairings below require at least six edges.
            for left, right in zip(xs, ys):
                assert distance(adjacency, b, c) >= 4
                assert distance(adjacency, left, right) >= 2
                assert distance(adjacency, b, right) >= 3
                assert distance(adjacency, left, c) >= 3
                assert distance(adjacency, b, c) + distance(adjacency, left, right) >= 6
                assert distance(adjacency, b, right) + distance(adjacency, left, c) >= 6
                repeated_classes += 1

            missing_star = set()
            for hub in (b, c):
                for other in B - {hub}:
                    if other not in adjacency[hub]:
                        missing_star.add(tuple(sorted((hub, other))))
            expected_reserve = delta + 2 * kappa - g - 5
            assert len(missing_star) == expected_reserve
            assert expected_reserve == (g * g + g - (11 if parity == 0 else 8))
            assert len(missing_star) >= g
            reserve_pairs_checked += len(missing_star)
            graph_rows += 1

    assert g4_boundary_rows == 2
    assert l4_eligible_rows == 16
    return {
        "sharp_graph_rows": graph_rows,
        "repeated_classes": repeated_classes,
        "reserve_pairs_checked": reserve_pairs_checked,
        "g4_graph_only_rows": g4_boundary_rows,
        "g_ge_5_l4_eligible_rows": l4_eligible_rows,
    }


def main() -> None:
    result = {
        "schema": "amra.erdos809.cross-audit-by-erdos1083.v1",
        "pass": True,
        **scalar_audit(),
        **graph_audit(),
        "author_verifier_imported": False,
        "original_problem_proved": False,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
