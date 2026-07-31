#!/usr/bin/env python3
"""Finite guards for the third 2026-07-31 Erdős #809 attack.

The script checks:

1. exact complement-energy identities for closed maximum neighbourhoods;
2. the deterministic excess-degree cleaning certificate;
3. a rotated two-clique family in which a maximum-degree BCM witness is
   not aligned with the dense larger core, while L4(2) and a natural
   rainbow-C7 colouring survive.

The computations guard formulas and explicit constructions only.  They
do not prove the canonical-witness defect charge or Erdős #809.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from collections import deque

Edge = tuple[int, int]


def edge(u: int, v: int) -> Edge:
    if u == v:
        raise ValueError((u, v))
    return (u, v) if u < v else (v, u)


def neighborhoods(n: int, edges: set[Edge]) -> list[set[int]]:
    out = [set() for _ in range(n)]
    for u, v in edges:
        out[u].add(v)
        out[v].add(u)
    return out


def complement_energy(
    n: int, edges: set[Edge], center: int
) -> dict[str, int | bool]:
    neigh = neighborhoods(n, edges)
    degrees = [len(item) for item in neigh]
    if degrees[center] != max(degrees):
        raise ValueError("center is not maximum degree")
    witness = {center} | neigh[center]
    outside = set(range(n)) - witness
    m = len(witness)
    r = len(outside)
    inside_edges = {
        item for item in edges if item[0] in witness and item[1] in witness
    }
    outside_edges = {
        item for item in edges if item[0] in outside and item[1] in outside
    }
    crossing_edges = edges - inside_edges - outside_edges
    missing_inside = math.comb(m, 2) - len(inside_edges)
    missing_outside = math.comb(r, 2) - len(outside_edges)
    union_baseline = math.comb(m, 2) + math.comb(r, 2)
    assert len(crossing_edges) == (
        missing_inside
        + missing_outside
        + len(edges)
        - union_baseline
    )
    assert len(crossing_edges) <= 2 * missing_inside
    return {
        "vertices": n,
        "witness_size": m,
        "outside_size": r,
        "missing_inside": missing_inside,
        "missing_outside": missing_outside,
        "crossing_edges": len(crossing_edges),
        "maximum_degree_inequality": True,
        "energy_identity": True,
        "passed": True,
    }


def random_energy_guard(
    trials: int = 200, vertices: int = 18, seed: int = 80903
) -> dict[str, int | bool]:
    rng = random.Random(seed)
    nontrivial = 0
    for _ in range(trials):
        probability = rng.uniform(0.2, 0.8)
        edges = {
            edge(u, v)
            for u, v in itertools.combinations(range(vertices), 2)
            if rng.random() < probability
        }
        neigh = neighborhoods(vertices, edges)
        center = max(range(vertices), key=lambda item: len(neigh[item]))
        result = complement_energy(vertices, edges, center)
        if result["crossing_edges"]:
            nontrivial += 1
    return {
        "trials": trials,
        "vertices": vertices,
        "nontrivial_crossing_profiles": nontrivial,
        "passed": True,
    }


def cleaning_certificate(
    order: int,
    target_order: int,
    missing_edges: set[Edge],
) -> dict[str, int | float | bool]:
    """Apply the deterministic cleaning rule from Theorem 5.1."""
    if not 8 <= target_order < order:
        raise ValueError((order, target_order))
    excess = order - target_order
    bound = excess * (target_order - 7) / 16
    if len(missing_edges) > bound:
        raise ValueError((len(missing_edges), bound))

    missing_neigh = [set() for _ in range(order)]
    for u, v in missing_edges:
        missing_neigh[u].add(v)
        missing_neigh[v].add(u)
    threshold = (target_order - 7) / 4
    removed = {
        vertex
        for vertex in range(order)
        if len(missing_neigh[vertex]) > threshold
    }
    retained = set(range(order)) - removed
    retained_edges = {
        edge(u, v)
        for u, v in itertools.combinations(sorted(retained), 2)
        if edge(u, v) not in missing_edges
    }
    retained_neigh = neighborhoods(order, retained_edges)
    retained_min_degree = min(
        len(retained_neigh[vertex]) for vertex in retained
    )
    retained_order = len(retained)
    assert len(removed) < excess / 2
    assert 2 * retained_min_degree - retained_order >= 5
    assert len(retained_edges) >= math.comb(target_order, 2)
    return {
        "order": order,
        "target_order": target_order,
        "excess": excess,
        "missing_edges": len(missing_edges),
        "allowed_missing_edges": bound,
        "removed_vertices": len(removed),
        "retained_order": retained_order,
        "retained_edges": len(retained_edges),
        "compatibility_threshold": (
            2 * retained_min_degree - retained_order
        ),
        "passed": True,
    }


def cleaning_guard() -> dict[str, object]:
    # A concentrated missing star exercises the removal step.
    concentrated = {edge(0, vertex) for vertex in range(1, 11)}
    result_one = cleaning_certificate(36, 20, concentrated)

    # A dispersed matching exercises the no-removal branch.
    dispersed = {edge(2 * index, 2 * index + 1) for index in range(6)}
    result_two = cleaning_certificate(28, 20, dispersed)
    return {
        "concentrated_profile": result_one,
        "dispersed_profile": result_two,
        "passed": True,
    }


def has_exact_path(
    neigh: list[set[int]],
    start: int,
    end: int,
    length: int,
    forbidden: set[int],
) -> bool:
    if start in forbidden or end in forbidden:
        return False

    def extend(path: tuple[int, ...]) -> bool:
        if len(path) == length + 1:
            return path[-1] == end
        for nxt in neigh[path[-1]]:
            if nxt in forbidden or nxt in path:
                continue
            if nxt == end and len(path) != length:
                continue
            if extend(path + (nxt,)):
                return True
        return False

    return extend((start,))


def exact_paths(
    neigh: list[set[int]], start: int, end: int, length: int
) -> list[tuple[int, ...]]:
    found: list[tuple[int, ...]] = []

    def extend(path: tuple[int, ...]) -> None:
        if len(path) == length + 1:
            if path[-1] == end:
                found.append(path)
            return
        for nxt in neigh[path[-1]]:
            if nxt in path:
                continue
            if nxt == end and len(path) != length:
                continue
            extend(path + (nxt,))

    extend((start,))
    return found


def two_edges_share_c7(
    neigh: list[set[int]], left: Edge, right: Edge
) -> bool:
    """Use the exact vertex-disjoint (2,3)-linkage characterization."""
    if set(left) & set(right):
        # The rotated guard only calls this on disjoint paired edges.
        raise ValueError((left, right))
    x, y = left
    z, w = right
    for first_end, second_end, other_first, other_second in (
        (x, z, y, w),
        (x, w, y, z),
    ):
        for short_length, long_length in ((2, 3), (3, 2)):
            short_paths = exact_paths(
                neigh, first_end, second_end, short_length
            )
            long_paths = exact_paths(
                neigh, other_first, other_second, long_length
            )
            for short in short_paths:
                for long in long_paths:
                    if set(short).isdisjoint(set(long)):
                        return True
    return False


def rotated_graph(
    large_order: int = 13, small_order: int = 7
) -> tuple[
    int,
    set[Edge],
    int,
    set[int],
    set[int],
    set[int],
    list[Edge],
]:
    """Build the finite rotated-core red-team graph.

    P=U union B is the almost-clique larger core.  W is the smaller
    clique, v lies in W, and N[v]=U union W is a rotated maximum-degree
    witness.  Four matching bridges preserve robust connectivity.
    """
    u_order = large_order - small_order
    if u_order < 2 or (u_order + 4) % 2:
        raise ValueError((large_order, small_order))
    n = large_order + small_order
    u_set = set(range(u_order))
    b_set = set(range(u_order, large_order))
    w_set = set(range(large_order, n))
    center = large_order
    bridge_b = sorted(b_set)[:4]
    bridge_w = list(range(large_order + 1, large_order + 5))

    edges = {
        edge(x, y)
        for block in (range(large_order), range(large_order, n))
        for x, y in itertools.combinations(block, 2)
    }
    bridges = [
        edge(left, right) for left, right in zip(bridge_b, bridge_w)
    ]
    edges.update(bridges)
    edges.update(edge(center, vertex) for vertex in u_set)

    # Cover exactly the vertices whose added cross edge would otherwise
    # raise their degree above large_order-1.
    targeted = sorted(u_set) + bridge_b
    deleted_matching = [
        edge(targeted[index], targeted[index + 1])
        for index in range(0, len(targeted), 2)
    ]
    edges.difference_update(deleted_matching)
    return (
        n,
        edges,
        center,
        u_set,
        b_set,
        w_set,
        deleted_matching,
    )


def rotated_witness_guard() -> dict[str, int | bool]:
    (
        n,
        edges,
        center,
        u_set,
        b_set,
        w_set,
        deleted_matching,
    ) = rotated_graph()
    neigh = neighborhoods(n, edges)
    degrees = [len(item) for item in neigh]
    witness = {center} | neigh[center]
    large_core = u_set | b_set
    assert degrees[center] == max(degrees) == len(large_core) - 1
    assert witness == u_set | w_set
    assert len(witness & large_core) == len(u_set)
    assert len(deleted_matching) == 5
    assert len(edges) > n * n / 4

    # Full L4(2) finite guard.
    deletion_sets = [set()]
    deletion_sets.extend({vertex} for vertex in range(n))
    deletion_sets.extend(
        set(pair) for pair in itertools.combinations(range(n), 2)
    )
    path_checks = 0
    for deleted in deletion_sets:
        remaining = set(range(n)) - deleted
        for start, end in itertools.combinations(sorted(remaining), 2):
            assert has_exact_path(neigh, start, end, 4, deleted)
            path_checks += 1

    # Pair the one W-generic edge with a B-generic edge.  The paired
    # B-edge is outside E_good(N[v]).
    bridge_b = sorted(b_set)[:4]
    bridge_w = list(range(center + 1, center + 5))
    generic_b = sorted(b_set - set(bridge_b))
    generic_w = sorted(w_set - {center} - set(bridge_w))
    paired_b = edge(generic_b[0], generic_b[1])
    paired_w = edge(generic_w[0], generic_w[1])
    assert not two_edges_share_c7(neigh, paired_b, paired_w)

    colours: dict[Edge, int] = {paired_b: 0, paired_w: 0}
    next_colour = 1
    for item in sorted(edges):
        if item not in colours:
            colours[item] = next_colour
            next_colour += 1
    good_edges = {
        item
        for item in edges
        if item[0] in witness or item[1] in witness
    }
    good_colours = {colours[item] for item in good_edges}
    assert paired_w in good_edges and paired_b not in good_edges
    assert len(good_edges) == len(good_colours)

    energy = complement_energy(n, edges, center)
    assert energy["missing_inside"] > n
    assert energy["missing_outside"] == 2
    return {
        "vertices": n,
        "edges": len(edges),
        "minimum_degree": min(degrees),
        "maximum_degree": max(degrees),
        "witness_size": len(witness),
        "dense_core_size": len(large_core),
        "witness_core_intersection": len(witness & large_core),
        "witness_missing_edges": energy["missing_inside"],
        "outside_missing_edges": energy["missing_outside"],
        "L4_deletion_sets": len(deletion_sets),
        "L4_endpoint_pairs": path_checks,
        "paired_edges_share_C7": False,
        "good_edge_defect": 0,
        "passed": True,
    }


def rich_outer_guard(threshold: int = 4) -> dict[str, int | bool]:
    """Guard the rich-outer compatibility lemma on the rotated graph."""
    (
        n,
        edges,
        center,
        _u_set,
        b_set,
        _w_set,
        _deleted_matching,
    ) = rotated_graph()
    neigh = neighborhoods(n, edges)
    witness = {center} | neigh[center]
    missing_outside = math.comb(len(b_set), 2) - sum(
        1 for item in edges if item[0] in b_set and item[1] in b_set
    )
    assert missing_outside < math.comb(threshold - 1, 2)

    def orientations(item: Edge) -> list[tuple[int, int]]:
        found: list[tuple[int, int]] = []
        left, right = item
        if left in witness and len(neigh[right] & b_set) >= threshold:
            found.append((left, right))
        if right in witness and len(neigh[left] & b_set) >= threshold:
            found.append((right, left))
        return found

    rich_edges = [item for item in sorted(edges) if orientations(item)]
    induced_pairs = 0
    distance_at_most_one_pairs = 0
    for left, right in itertools.combinations(rich_edges, 2):
        endpoints_left = set(left)
        endpoints_right = set(right)
        if endpoints_left & endpoints_right or any(
            edge(x, z) in edges
            for x in endpoints_left
            for z in endpoints_right
        ):
            distance_at_most_one_pairs += 1
            continue

        certified = False
        for inner_left, outer_left in orientations(left):
            for inner_right, outer_right in orientations(right):
                first = (neigh[outer_left] & b_set) - {outer_right}
                second = (neigh[outer_right] & b_set) - {outer_left}
                for first_internal in first:
                    for second_internal in second:
                        if first_internal == second_internal:
                            continue
                        if edge(first_internal, second_internal) in edges:
                            path = (
                                outer_left,
                                first_internal,
                                second_internal,
                                outer_right,
                            )
                            assert set(path).isdisjoint(
                                {inner_left, center, inner_right}
                            )
                            certified = True
                            break
                    if certified:
                        break
                if certified:
                    break
            if certified:
                break
        assert certified
        induced_pairs += 1

    # A separate sharp local profile exercises the centered rectangle:
    # B is K_7 minus the outer pair y-w.
    local_center, local_x, local_z, local_y, local_w = range(5)
    local_b = set(range(3, 10))
    local_edges = {
        edge(left, right)
        for left, right in itertools.combinations(sorted(local_b), 2)
    }
    local_edges.discard(edge(local_y, local_w))
    local_edges.update(
        {
            edge(local_center, local_x),
            edge(local_center, local_z),
            edge(local_x, local_y),
            edge(local_z, local_w),
        }
    )
    local_neigh = neighborhoods(10, local_edges)
    local_p = (local_neigh[local_y] & local_b) - {local_w}
    local_q = (local_neigh[local_w] & local_b) - {local_y}
    local_path_found = any(
        first != second and edge(first, second) in local_edges
        for first in local_p
        for second in local_q
    )
    assert local_path_found
    assert math.comb(len(local_b), 2) - sum(
        1
        for item in local_edges
        if item[0] in local_b and item[1] in local_b
    ) == 1

    return {
        "threshold": threshold,
        "outside_missing_edges": missing_outside,
        "rich_edges": len(rich_edges),
        "distance_at_most_one_pairs": distance_at_most_one_pairs,
        "centered_rectangle_pairs": induced_pairs,
        "local_centered_rectangle": local_path_found,
        "passed": True,
    }


def main() -> None:
    result = {
        "random_energy_identities": random_energy_guard(),
        "excess_degree_cleaning": cleaning_guard(),
        "rotated_maximum_witness": rotated_witness_guard(),
        "rich_outer_compatibility": rich_outer_guard(),
        "scope": (
            "Finite guards verify exact identities, cleaning arithmetic, "
            "and one rotated construction only; the canonical defect "
            "charge and Erdos #809 remain open."
        ),
        "passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
