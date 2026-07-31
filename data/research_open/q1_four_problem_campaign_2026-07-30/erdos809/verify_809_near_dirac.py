#!/usr/bin/env python3
"""Independent finite guards for the 2026-07-30 Erdős #809 milestone.

The program checks:

1. the exact set identities behind four-path obstruction stability;
2. the distance-two -> no-three-step C7 splice;
3. dense-clique C7 compatibility on finite adversarial samples;
4. the maximum-cut core/hub family by brute-force C7 enumeration;
5. the normalized rectangle inequality on a rational grid.

These checks guard displayed formulas.  They do not extrapolate a finite
sample to the asymptotic theorem or to Erdős #809.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
from collections import deque
from fractions import Fraction

Edge = tuple[int, int]


def edge(u: int, v: int) -> Edge:
    assert u != v
    return (u, v) if u < v else (v, u)


def neighborhoods(n: int, edges: set[Edge]) -> list[set[int]]:
    result = [set() for _ in range(n)]
    for u, v in edges:
        result[u].add(v)
        result[v].add(u)
    return result


def path_exact(
    n: int,
    edges: set[Edge],
    start: int,
    end: int,
    length: int,
    forbidden: set[int] | None = None,
) -> list[int] | None:
    """Return one simple path of exactly ``length`` edges, if it exists."""
    forbidden = set() if forbidden is None else set(forbidden)
    if start in forbidden or end in forbidden:
        return None
    allowed = set(range(n)) - forbidden

    def dfs(path: list[int]) -> list[int] | None:
        if len(path) == length + 1:
            return path if path[-1] == end else None
        current = path[-1]
        remaining_edges = length + 1 - len(path)
        for nxt in sorted(allowed):
            if nxt in path or edge(current, nxt) not in edges:
                continue
            if nxt == end and remaining_edges != 1:
                continue
            found = dfs(path + [nxt])
            if found is not None:
                return found
        return None

    return dfs([start])


def all_pairs_shortest_paths(
    n: int, edges: set[Edge]
) -> tuple[list[list[int]], list[list[int | None]]]:
    adjacency = neighborhoods(n, edges)
    distances: list[list[int]] = []
    parents: list[list[int | None]] = []
    for source in range(n):
        dist = [-1] * n
        parent: list[int | None] = [None] * n
        dist[source] = 0
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for nxt in adjacency[current]:
                if dist[nxt] < 0:
                    dist[nxt] = dist[current] + 1
                    parent[nxt] = current
                    queue.append(nxt)
        distances.append(dist)
        parents.append(parent)
    return distances, parents


def shortest_path_from_parent(
    start: int, end: int, parent: list[int | None]
) -> list[int]:
    reverse = [end]
    while reverse[-1] != start:
        previous = parent[reverse[-1]]
        assert previous is not None
        reverse.append(previous)
    return list(reversed(reverse))


def four_path_profile(
    n: int, original_edges: set[Edge], u: int, v: int
) -> dict[str, int] | None:
    """Check every exact inequality used in the obstruction lemma."""
    if path_exact(n, original_edges, u, v, 4) is not None:
        return None

    original_neigh = neighborhoods(n, original_edges)
    delta = min(map(len, original_neigh))
    edges = set(original_edges)
    edges.add(edge(u, v))
    # Adding the endpoint edge must not create an exact simple four-path.
    assert path_exact(n, edges, u, v, 4) is None

    neigh = neighborhoods(n, edges)
    common = neigh[u] & neigh[v]
    x_side = neigh[u] - common - {v}
    y_side = neigh[v] - common - {u}
    z_side = set(range(n)) - common - x_side - y_side - {u, v}

    property_pairs = 0
    for x in common | x_side:
        for y in common | y_side:
            if x == y:
                continue
            assert (neigh[x] & neigh[y]) <= {u, v}
            property_pairs += 1

    if 3 * delta > n + 6:
        assert len(common) <= 2
        assert len(x_side) >= delta - 3
        assert len(y_side) >= delta - 3
        assert len(z_side) <= n - 2 * delta + 2

    complement_bounds = 0
    for x in x_side:
        for y in y_side:
            assert len(neigh[x] & neigh[y]) <= 2
            complement_y = set(range(n)) - neigh[y]
            assert len(neigh[x] ^ complement_y) <= n - 2 * delta + 4
            complement_bounds += 1

    product_bounds = 0
    if x_side and y_side:
        x0 = min(x_side)
        y0 = min(y_side)
        universe = set(range(n))
        u_side = set(neigh[x0])
        w_side = universe - u_side
        theta = n - 2 * delta + 4
        assert delta <= len(u_side) <= n - delta + 2
        for x in x_side:
            assert len(neigh[x] ^ u_side) <= 2 * theta
        for y in y_side:
            assert len(neigh[y] ^ w_side) <= theta

        xu, xw = x_side & u_side, x_side & w_side
        yu, yw = y_side & u_side, y_side & w_side
        assert len(xu) * len(xw) <= 2 * theta * len(x_side)
        assert len(yu) * len(yw) <= theta * len(y_side)
        product_bounds = 2

    return {
        "property_pairs": property_pairs,
        "complement_bounds": complement_bounds,
        "product_bounds": product_bounds,
        "delta": delta,
    }


def exhaustive_four_path_guard(max_n: int = 6) -> dict[str, object]:
    graph_count = 0
    obstruction_count = 0
    property_pairs = 0
    complement_bounds = 0
    product_bounds = 0
    by_n: dict[str, dict[str, int]] = {}

    for n in range(3, max_n + 1):
        complete = [edge(u, v) for u in range(n) for v in range(u + 1, n)]
        local_graphs = 0
        local_obstructions = 0
        for mask in range(1 << len(complete)):
            edges = {
                complete[index]
                for index in range(len(complete))
                if mask & (1 << index)
            }
            graph_count += 1
            local_graphs += 1
            for u, v in itertools.combinations(range(n), 2):
                result = four_path_profile(n, edges, u, v)
                if result is None:
                    continue
                obstruction_count += 1
                local_obstructions += 1
                property_pairs += result["property_pairs"]
                complement_bounds += result["complement_bounds"]
                product_bounds += result["product_bounds"]
        by_n[str(n)] = {
            "labelled_graphs": local_graphs,
            "obstructed_pairs": local_obstructions,
        }

    # Two exact asymptotic models exercise the two orientations at a size
    # beyond the exhaustive range.
    model_profiles = []
    for model in ("two_cliques", "complete_bipartite"):
        n = 20
        left = set(range(n // 2))
        right = set(range(n // 2, n))
        if model == "two_cliques":
            edges = {
                edge(u, v)
                for side in (left, right)
                for u, v in itertools.combinations(side, 2)
            }
            endpoints = (0, n // 2)
        else:
            edges = {edge(u, v) for u in left for v in right}
            endpoints = (0, n // 2)
        profile = four_path_profile(n, edges, *endpoints)
        assert profile is not None
        model_profiles.append({"model": model, **profile})

    return {
        "labelled_graphs": graph_count,
        "obstructed_pairs": obstruction_count,
        "property_pairs_checked": property_pairs,
        "complement_bounds_checked": complement_bounds,
        "product_bounds_checked": product_bounds,
        "by_n": by_n,
        "model_profiles": model_profiles,
        "passed": True,
    }


def distance_two_splice_guard(
    seeds: int = 500,
) -> dict[str, int | bool]:
    checked_distance_two_pairs = 0
    checked_splices = 0
    rng = random.Random(8090730)

    for seed in range(seeds):
        n = 7 + seed % 3
        probability = 0.35 + 0.3 * rng.random()
        edges = {
            edge(u, v)
            for u in range(n)
            for v in range(u + 1, n)
            if rng.random() < probability
        }
        distances, parents = all_pairs_shortest_paths(n, edges)
        edge_list = sorted(edges)
        for first, second in itertools.combinations(edge_list, 2):
            endpoints_first = first
            endpoints_second = second
            candidates = [
                (distances[x][z], x, z)
                for x in endpoints_first
                for z in endpoints_second
                if distances[x][z] >= 0
            ]
            if not candidates:
                continue
            distance, x, z = min(candidates)
            if distance != 2:
                continue
            checked_distance_two_pairs += 1
            path_xz = shortest_path_from_parent(x, z, parents[x])
            assert len(path_xz) == 3
            a = path_xz[1]
            y = first[1] if first[0] == x else first[0]
            w = second[1] if second[0] == z else second[0]
            # The theorem only invokes the splice after distances 0/1 have
            # been excluded.  Verify this boundary explicitly.
            if len({x, a, z, y, w}) < 5 or edge(y, w) in edges:
                continue
            outer = path_exact(
                n, edges, y, w, 3, forbidden={x, a, z}
            )
            if outer is None:
                continue
            cycle = [y, x, a, z, w, outer[2], outer[1]]
            assert len(cycle) == len(set(cycle)) == 7
            cycle_edges = {
                edge(cycle[index], cycle[(index + 1) % 7])
                for index in range(7)
            }
            assert cycle_edges <= edges
            assert first in cycle_edges and second in cycle_edges
            checked_splices += 1

    assert checked_splices > 0
    return {
        "random_graphs": seeds,
        "distance_two_edge_pairs_checked": checked_distance_two_pairs,
        "actual_three_path_splices_checked": checked_splices,
        "passed": True,
    }


def cycle_covered_pairs(
    n: int, edges: set[Edge], family: list[Edge]
) -> tuple[int, int]:
    """Brute-force all C7s and return covered/total family-edge pairs."""
    index = {item: position for position, item in enumerate(family)}
    outstanding = set(itertools.combinations(range(len(family)), 2))
    cycles = 0
    for vertices in itertools.combinations(range(n), 7):
        first = vertices[0]
        for tail in itertools.permutations(vertices[1:]):
            if tail[0] > tail[-1]:
                continue
            cycle = (first,) + tail
            used = {
                edge(cycle[i], cycle[(i + 1) % 7])
                for i in range(7)
            }
            if not used <= edges:
                continue
            cycles += 1
            hits = sorted(index[item] for item in used if item in index)
            for pair in itertools.combinations(hits, 2):
                outstanding.discard(pair)
        if not outstanding:
            break
    total = len(family) * (len(family) - 1) // 2
    return total - len(outstanding), total


def dense_clique_guard() -> dict[str, object]:
    instances = []
    for m, deleted in (
        (9, {edge(0, 1), edge(2, 3), edge(4, 5)}),
        (10, {edge(i, (i + 1) % 10) for i in range(10)}),
    ):
        edges = {
            edge(u, v)
            for u in range(m)
            for v in range(u + 1, m)
        } - deleted
        family = sorted(edges)
        covered, total = cycle_covered_pairs(m, edges, family)
        assert covered == total
        instances.append(
            {
                "vertices": m,
                "edges": len(edges),
                "family_pairs": total,
                "all_covered": True,
            }
        )
    return {"instances": instances, "passed": True}


def core_hub_bruteforce_guard() -> dict[str, object]:
    """Test the union family without assuming either side is independent."""
    a_side = set(range(8))
    b_side = set(range(8, 14))
    p, q = 0, 1
    p_rows = {2, 3}
    q_rows = {4, 5}
    core_rows = {6, 7}
    p_anchor, q_anchor = 8, 9

    edges = {edge(a, b) for a in a_side for b in b_side}
    edges |= {edge(p, q)}
    edges |= {edge(p, row) for row in p_rows}
    edges |= {edge(q, row) for row in q_rows}
    # Extra internal B-edges ensure the finite model does not accidentally
    # rely on B being independent.
    edges |= {edge(8, 10), edge(9, 11), edge(12, 13)}

    family_set = set()
    for row in p_rows | q_rows:
        forbidden = set()
        if row in p_rows:
            forbidden.add(p_anchor)
        if row in q_rows:
            forbidden.add(q_anchor)
        for column in b_side - forbidden:
            family_set.add(edge(row, column))
    for row in core_rows:
        for column in b_side:
            family_set.add(edge(row, column))
    family = sorted(family_set)
    covered, total = cycle_covered_pairs(14, edges, family)
    assert covered == total
    return {
        "vertices": 14,
        "graph_edges": len(edges),
        "family_edges": len(family),
        "family_pairs": total,
        "covered_pairs": covered,
        "hub_rows": len(p_rows | q_rows),
        "core_rows": len(core_rows),
        "independent_side_deliberately_violated": True,
        "passed": True,
    }


def rectangle_optimization_guard(denominator: int = 400) -> dict[str, object]:
    checked = 0
    minimum = Fraction(1)
    minimizers: list[tuple[Fraction, Fraction]] = []
    for x_num in range(denominator + 1):
        x = Fraction(x_num, denominator)
        for y_num in range(x_num + 1):
            y = Fraction(y_num, denominator)
            k = max(Fraction(0), 1 - x - y)
            value = x + (1 - x) * k
            assert value >= Fraction(1, 2)
            checked += 1
            if value < minimum:
                minimum = value
                minimizers = [(x, y)]
            elif value == minimum:
                minimizers.append((x, y))
    return {
        "rational_profiles": checked,
        "denominator": denominator,
        "minimum": str(minimum),
        "sample_minimizers": [
            [str(x), str(y)] for x, y in minimizers[:5]
        ],
        "passed": minimum == Fraction(1, 2),
    }


def run_all(fast: bool = False) -> dict[str, object]:
    return {
        "four_path_obstruction": exhaustive_four_path_guard(5 if fast else 6),
        "distance_two_splice": distance_two_splice_guard(120 if fast else 500),
        "dense_clique": dense_clique_guard(),
        "maximum_cut_core_hub": core_hub_bruteforce_guard(),
        "rectangle_optimization": rectangle_optimization_guard(
            120 if fast else 400
        ),
        "scope_guard": (
            "Finite checks guard exact identities and C7 templates only; "
            "they do not prove an asymptotic statement or Erdős #809."
        ),
        "passed": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run_all(fast=args.fast), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
