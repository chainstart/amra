#!/usr/bin/env python3
"""Finite guards for the opposite-star common-host theorem.

The exhaustive search is evidence for implementation and boundary sanity,
not a substitute for the all-parameter proof in the companion note.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math


def pairs(vertices):
    return list(itertools.combinations(vertices, 2))


def choose2(x):
    return x * (x - 1) // 2


def ceil_div(x, y):
    return (x + y - 1) // y


def graph_from_mask(n, mask):
    edge_list = pairs(range(n))
    edges = {edge for i, edge in enumerate(edge_list) if (mask >> i) & 1}
    neighbours = [set() for _ in range(n)]
    for x, y in edges:
        neighbours[x].add(y)
        neighbours[y].add(x)
    return edges, neighbours


def edge_present(edges, x, y):
    return (min(x, y), max(x, y)) in edges


def missing_inside(edges, vertices):
    return sum(not edge_present(edges, x, y) for x, y in pairs(sorted(vertices)))


def crossing_edges(edges, left, right):
    return sum(edge_present(edges, x, y) for x in left for y in right)


def opposite_zero_leaf(edges, neighbours, b, c):
    if c == b or edge_present(edges, b, c):
        return False
    p = neighbours[b]
    q = neighbours[c]
    if p & q:
        return False
    return not any(edge_present(edges, x, y) for x in p for y in q)


def audit_system(n, edges, neighbours, b, leaves):
    vertices = set(range(n))
    pset = set(neighbours[b])
    cset = vertices - pset
    qsets = [set(neighbours[c]) for c in leaves]
    union = set().union(*qsets)
    residual = cset - union
    delta = min(map(len, neighbours))
    kappa = n - 2 * delta

    assert union <= cset
    assert not any(edge_present(edges, x, y) for x in pset for y in union)

    cross_pc = crossing_edges(edges, pset, cset)
    cross_pr = crossing_edges(edges, pset, residual)
    assert cross_pc == cross_pr
    assert cross_pc <= len(pset) * len(residual)

    psi = choose2(len(pset)) + choose2(len(cset)) - len(edges)
    energy = missing_inside(edges, pset) + missing_inside(edges, cset)
    assert energy == psi + cross_pc
    assert energy <= psi + len(pset) * len(residual)

    assert 0 <= len(residual) <= kappa
    deficits = []
    for leaf, qset in zip(leaves, qsets):
        rho = n - len(pset) - len(neighbours[leaf])
        deficit = len(union - qset)
        assert deficit == rho - len(residual)
        assert 0 <= deficit <= kappa - len(residual)
        deficits.append(deficit)

    for i, j in pairs(range(len(qsets))):
        symdiff = len(qsets[i] ^ qsets[j])
        assert symdiff <= deficits[i] + deficits[j]
        assert symdiff <= 2 * (kappa - len(residual))

    common = set.intersection(*qsets)
    assert len(common) >= len(union) - sum(deficits)

    residual_leaves = set(leaves) & residual
    nonisolated_leaf_count = len(leaves) - len(residual_leaves)
    leaf_set = set(leaves)
    external_union = union - leaf_set
    leaf_edges = choose2(len(leaves)) - missing_inside(edges, leaf_set)
    external_defect = sum(
        len(external_union - qset) for qset in qsets
    )
    assert sum(deficits) == (
        len(leaves) * nonisolated_leaf_count
        - 2 * leaf_edges
        + external_defect
    )
    assert sum(deficits) >= (
        nonisolated_leaf_count
        * (len(leaves) - nonisolated_leaf_count + 1)
    )
    deficit_root = math.isqrt(sum(deficits))
    isolated_leaf_count = len(residual_leaves)
    assert (
        nonisolated_leaf_count <= deficit_root
        or isolated_leaf_count <= deficit_root - 1
    )
    if nonisolated_leaf_count <= deficit_root:
        assert missing_inside(edges, leaf_set) >= (
            choose2(len(leaves)) - choose2(deficit_root)
        )
    if nonisolated_leaf_count > deficit_root:
        assert 2 * leaf_edges >= (
            len(leaves) * (len(leaves) - deficit_root + 1)
            - sum(deficits)
        )
    if sum(deficits) < len(leaves):
        assert leaf_edges == 0
    if sum(deficits) == len(leaves) and leaf_edges > 0:
        assert nonisolated_leaf_count == len(leaves)
        assert leaf_edges == choose2(len(leaves))
        assert external_defect == 0
        for leaf, qset in zip(leaves, qsets):
            assert qset == union - {leaf}
    assert nonisolated_leaf_count <= sum(deficits)
    assert not any(
        edge_present(edges, x, y)
        for x in residual_leaves
        for y in leaves
        if x != y
    )

    leaf_missing = missing_inside(edges, leaf_set)
    forced_by_residual = (
        choose2(len(leaves)) - choose2(nonisolated_leaf_count)
    )
    clipped_deficit = min(len(leaves), sum(deficits))
    assert leaf_missing >= forced_by_residual
    assert forced_by_residual >= (
        choose2(len(leaves)) - choose2(clipped_deficit)
    )

    for degree_cap in range(len(leaves) + 1):
        missing_degrees = {
            leaf: sum(
                not edge_present(edges, leaf, other)
                for other in leaves
                if other != leaf
            )
            for leaf in leaves
        }
        retained = {
            leaf for leaf in leaves
            if missing_degrees[leaf] <= degree_cap
        }
        lower_order = (
            len(leaves)
            - (2 * leaf_missing) // (degree_cap + 1)
        )
        assert len(retained) >= lower_order
        retained_missing = missing_inside(edges, retained)
        assert retained_missing <= leaf_missing
        for leaf in retained:
            retained_degree = sum(
                edge_present(edges, leaf, other)
                for other in retained
                if other != leaf
            )
            assert retained_degree >= len(retained) - 1 - degree_cap

    # Guard the new maximum-witness union rectangle for every possible
    # maximum-degree choice whose outside block contains this star.
    union_rectangle_witnesses = 0
    maximum_degree = max(map(len, neighbours))
    for witness in range(n):
        if len(neighbours[witness]) != maximum_degree:
            continue
        aset = {witness} | set(neighbours[witness])
        bset = vertices - aset
        if b not in bset or not set(leaves) <= bset:
            continue
        maximum_basepoints = {b, witness} | residual_leaves
        assert maximum_basepoints <= residual
        assert len(residual) >= len(residual_leaves) + 2
        for leaf in leaves:
            rho = n - len(pset) - len(neighbours[leaf])
            assert rho >= 3
        xset = pset & aset
        yset = union & aset
        assert not xset & yset
        assert not any(
            edge_present(edges, x, y) for x in xset for y in yset
        )
        assert missing_inside(edges, aset) >= len(xset) * len(yset)
        assert len(yset) >= max(len(qset & aset) for qset in qsets)

        z_b = (union & bset) - leaf_set
        e_a = sum(len(yset - qset) for qset in qsets)
        e_b = sum(len(z_b - qset) for qset in qsets)
        leaf_missing = missing_inside(edges, leaf_set)
        isolated_count = len(residual_leaves)
        total_deficit = sum(deficits)
        assert (
            total_deficit + len(leaves) * (isolated_count - 1)
            == 2 * leaf_missing + e_a + e_b
        )

        # All missing B-pairs incident with an active leaf form a
        # conservative proxy for the actual global reserve.
        reserve_proxy = sum(
            not edge_present(edges, x, y)
            and (x in leaf_set or y in leaf_set)
            for x, y in pairs(sorted(bset))
        )
        assert reserve_proxy >= leaf_missing + e_b
        paid_cap = reserve_proxy + min(
            reserve_proxy, choose2(len(leaves))
        )
        unpaid = max(
            0,
            total_deficit
            + len(leaves) * (isolated_count - 1)
            - paid_cap,
        )
        assert e_a >= unpaid
        degree_mass_a = sum(len(qset & aset) for qset in qsets)
        assert len(leaves) * len(yset) == degree_mass_a + e_a
        assert len(yset) >= ceil_div(degree_mass_a + unpaid, len(leaves))

        # Guard the disjoint degree-cap missing-pair budget (4b) and
        # its p/ell-free relaxation (17) on actual finite graphs.
        ell = len(leaves)
        isolated = len(residual_leaves)
        common_residual = len(residual) - isolated
        assert common_residual >= 2
        residual_mass = sum(
            n - len(pset) - len(neighbours[leaf]) for leaf in leaves
        )
        assert residual_mass >= (common_residual + 1) * ell
        assert len(pset) <= n - delta - common_residual - 1

        residual_vertices = common_residual - 1
        forced_per_residual = max(
            0, n - ell - 2 - maximum_degree
        )
        degree_cap_extra = max(
            0,
            residual_vertices * forced_per_residual
            - choose2(residual_vertices),
        )
        degree_cap_lower = (
            len(pset) * (n - len(pset) - common_residual)
            + n
            - len(pset)
            - 1
            + residual_vertices * ell
            + degree_cap_extra
        )
        total_missing = choose2(n) - len(edges)
        assert total_missing >= degree_cap_lower

        relaxed_lower = (
            delta * (n - common_residual - 1 - delta)
            + n
            - 1
            + residual_vertices * (n - 2 - maximum_degree)
            - choose2(residual_vertices)
        )
        assert degree_cap_lower >= relaxed_lower
        union_rectangle_witnesses += 1

    return union_rectangle_witnesses


def run_exhaustive(max_n=6):
    parameter_cases = 0
    for leaf_count in range(1, 31):
        for colour_mass in range(leaf_count, 301):
            average = ceil_div(colour_mass, leaf_count)
            assert choose2(leaf_count) + average * average >= colour_mass
            critical_rectangle = colour_mass * average
            assert critical_rectangle * leaf_count >= colour_mass ** 2
            assert colour_mass <= math.isqrt(
                leaf_count * critical_rectangle
            )
            for total_deficit in range(61):
                common_coordinate = max(
                    0,
                    ceil_div(colour_mass + total_deficit, leaf_count)
                    - total_deficit,
                )
                clipped_deficit = min(leaf_count, total_deficit)
                two_budget_lower = (
                    choose2(leaf_count)
                    - choose2(clipped_deficit)
                    + average * common_coordinate
                )
                stable_lower = (
                    colour_mass
                    - total_deficit * average
                    - choose2(total_deficit)
                )
                assert two_budget_lower >= stable_lower
                if total_deficit < leaf_count:
                    minimum_budget = stable_lower
                    cap = (
                        leaf_count
                        * (minimum_budget + choose2(total_deficit))
                        + total_deficit * (leaf_count - 1)
                    ) // (leaf_count - total_deficit)
                    assert colour_mass <= cap
                parameter_cases += 1

    graphs = 0
    centers = 0
    systems = 0
    union_rectangle_witnesses = 0
    for n in range(2, max_n + 1):
        edge_count = choose2(n)
        for mask in range(1 << edge_count):
            graphs += 1
            edges, neighbours = graph_from_mask(n, mask)
            for b in range(n):
                eligible = [
                    c for c in range(n)
                    if opposite_zero_leaf(edges, neighbours, b, c)
                ]
                if not eligible:
                    continue
                centers += 1
                for size in range(1, len(eligible) + 1):
                    for leaves in itertools.combinations(eligible, size):
                        union_rectangle_witnesses += audit_system(
                            n, edges, neighbours, b, leaves
                        )
                        systems += 1
    return {
        "schema": "amra.erdos809.opposite-star-common-host.v1",
        "max_n": max_n,
        "graphs": graphs,
        "eligible_centers": centers,
        "star_systems": systems,
        "union_rectangle_witnesses": union_rectangle_witnesses,
        "two_budget_parameter_cases": parameter_cases,
        "status": "PASS",
        "scope": "finite guards only; theorem proof is in the companion note",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(run_exhaustive(args.max_n), indent=2, sort_keys=True))
