#!/usr/bin/env python3
"""Finite guards for the R004 near-complete-split lemma for Erdős #809.

This checks the explicit C7 templates on dense finite samples and the elementary
optimization used in the asymptotic count.  It is not a finite proof of the
asymptotic statement or of Erdős #809.
"""

from __future__ import annotations

import itertools
import json
import random
from fractions import Fraction


def edge(u: str, v: str) -> frozenset[str]:
    return frozenset((u, v))


def cycle_edges(cycle: list[str]) -> set[frozenset[str]]:
    return {
        edge(cycle[i], cycle[(i + 1) % len(cycle)])
        for i in range(len(cycle))
    }


def first(items, predicate):
    for item in items:
        if predicate(item):
            return item
    raise LookupError("selector pool was unexpectedly empty")


def verify_instance(
    seed: int,
    a_size: int = 18,
    b_size: int = 18,
    p_extra_internal: int = 9,
    q_extra_internal: int = 9,
    hub_threshold: int = 4,
):
    rng = random.Random(seed)
    c_vertices = tuple(f"c{i}" for i in range(a_size))
    r_vertices = tuple(f"r{i}" for i in range(b_size))
    p, q = c_vertices[:2]

    graph = set()
    for c in c_vertices:
        for r in r_vertices:
            if rng.random() < 0.94:
                graph.add(edge(c, r))

    # The proof uses two kinds of density.  Every R-column is uniformly dense,
    # while the selected ordinary C-rows are dense.  Force transparent finite
    # analogues (at most two missing cross edges).
    for r in r_vertices:
        missing = [c for c in c_vertices if edge(c, r) not in graph]
        for c in missing[2:]:
            graph.add(edge(c, r))
    for c in c_vertices[2:]:
        missing = [r for r in r_vertices if edge(c, r) not in graph]
        for r in missing[2:]:
            graph.add(edge(c, r))

    # Give p,q a sizeable common cross-neighborhood.  The extra internal
    # degrees are parameters so that the same verifier also attacks the
    # h=0,1,2 boundary cases hidden by the original dense random tests.
    for r in r_vertices[:7]:
        graph.add(edge(p, r))
        graph.add(edge(q, r))
    graph.add(edge(p, q))
    for c in c_vertices[2:2 + p_extra_internal]:
        graph.add(edge(p, c))
    q_start = max(2, a_size - 2 - q_extra_internal)
    for c in c_vertices[q_start:q_start + q_extra_internal]:
        graph.add(edge(q, c))

    p_internal = {
        c for c in c_vertices[2:] if edge(p, c) in graph
    }
    q_internal = {
        c for c in c_vertices[2:] if edge(q, c) in graph
    }
    p_anchor = first(r_vertices, lambda r: edge(p, r) in graph)
    q_anchor = first(r_vertices, lambda r: edge(q, r) in graph)
    p_rows_raw = {
        c for c in p_internal if edge(c, p_anchor) in graph
    }
    q_rows_raw = {
        c for c in q_internal if edge(c, q_anchor) in graph
    }
    # Finite analogue of the asymptotic tau_n threshold.  A hub with fewer
    # than tau_n n rows is discarded in the proof; its whole rectangle costs
    # at most tau_n n^2=o(n^2).  Keeping this branch explicit prevents the
    # finite tests from silently assuming a spare hub row.
    p_rows = (
        p_rows_raw
        if len(p_internal) >= hub_threshold
        else set()
    )
    q_rows = (
        q_rows_raw
        if len(q_internal) >= hub_threshold
        else set()
    )
    union_rows = p_rows | q_rows
    common_columns_raw = {
        r
        for r in r_vertices
        if edge(p, r) in graph and edge(q, r) in graph
    }
    # The equal-row/equal-column core templates need finitely many spare
    # common columns.  If the common kernel is subthreshold, the asymptotic
    # proof discards that core rectangle at o(n^2) cost.
    common_columns = (
        common_columns_raw
        if len(common_columns_raw) >= hub_threshold
        else set()
    )
    ordinary_rows = set(c_vertices[2:])

    # The one fixed anchor used by a hub template is removed from that hub's
    # edge set.  This costs only O(n) edges asymptotically and prevents a
    # repeated vertex in the displayed seven-cycle.
    family = []
    for c in union_rows:
        forbidden = set()
        if c in p_rows:
            forbidden.add(p_anchor)
        if c in q_rows:
            forbidden.add(q_anchor)
        for r in r_vertices:
            if r not in forbidden and edge(c, r) in graph:
                family.append((c, r, "hub"))
    for c in ordinary_rows - union_rows:
        for r in common_columns:
            if edge(c, r) in graph:
                family.append((c, r, "core"))

    def check(cycle, first_edge, second_edge):
        assert len(cycle) == len(set(cycle)) == 7
        used = cycle_edges(cycle)
        assert used <= graph
        assert edge(*first_edge[:2]) in used
        assert edge(*second_edge[:2]) in used

    def hub_witness(first_edge, second_edge, center, rows, anchor):
        x1, y1, _ = first_edge
        x2, y2, _ = second_edge
        assert y1 != anchor and y2 != anchor
        if x1 == x2:
            spare_row = first(
                rows,
                lambda c: c not in {center, x1}
                and edge(c, y1) in graph,
            )
            selector = first(
                c_vertices,
                lambda c: c not in {center, spare_row, x1}
                and edge(c, y2) in graph
                and edge(c, anchor) in graph,
            )
            return [
                center,
                spare_row,
                y1,
                x1,
                y2,
                selector,
                anchor,
            ]
        if y1 == y2:
            spare_column = first(
                r_vertices,
                lambda r: r not in {y1, anchor}
                and edge(x2, r) in graph,
            )
            selector = first(
                c_vertices,
                lambda c: c not in {center, x1, x2}
                and edge(c, spare_column) in graph
                and edge(c, anchor) in graph,
            )
            return [
                center,
                x1,
                y1,
                x2,
                spare_column,
                selector,
                anchor,
            ]
        selector = first(
            c_vertices,
            lambda c: c not in {center, x1, x2}
            and edge(c, y1) in graph
            and edge(c, y2) in graph,
        )
        return [center, x1, y1, selector, y2, x2, anchor]

    def core_witness(first_edge, second_edge):
        a1, z1, _ = first_edge
        a2, z2, _ = second_edge
        if a1 == a2:
            spare_column = first(
                common_columns, lambda r: r not in {z1, z2}
            )
            selector = first(
                c_vertices,
                lambda c: c not in {p, q, a1}
                and edge(c, z2) in graph
                and edge(c, spare_column) in graph,
            )
            return [p, q, z1, a1, z2, selector, spare_column]
        if z1 == z2:
            x = first(
                common_columns,
                lambda r: r != z1 and edge(a1, r) in graph,
            )
            y = first(
                common_columns,
                lambda r: r not in {z1, x}
                and edge(a2, r) in graph,
            )
            return [p, q, x, a1, z1, a2, y]
        selector = first(
            r_vertices,
            lambda r: r not in {z1, z2}
            and edge(a1, r) in graph
            and edge(a2, r) in graph,
        )
        return [p, q, z1, a1, selector, a2, z2]

    def cross_hub_witness(p_edge, q_edge):
        x, y, _ = p_edge
        t, z, _ = q_edge
        assert x in p_rows and t in q_rows
        if x == t:
            # Both specified edges also belong to the p-hub family.
            return hub_witness(p_edge, q_edge, p, p_rows, p_anchor)
        if y == z:
            # Boundary-safe same-column template.  It needs no auxiliary
            # internal neighbour of either centre: r is selected from the
            # good row x, and c is a common neighbour of the dense columns
            # r and q_anchor.
            spare_column = first(
                r_vertices,
                lambda r: r not in {y, q_anchor}
                and edge(x, r) in graph,
            )
            selector = first(
                c_vertices,
                lambda c: c not in {p, q, x, t}
                and edge(c, spare_column) in graph
                and edge(c, q_anchor) in graph,
            )
            return [
                q,
                t,
                y,
                x,
                spare_column,
                selector,
                q_anchor,
            ]
        selector = first(
            c_vertices,
            lambda c: c not in {p, q, x, t}
            and edge(c, y) in graph
            and edge(c, z) in graph,
        )
        return [p, x, y, selector, z, t, q]

    def mixed_witness(core_edge, hub_edge, center):
        a, z, _ = core_edge
        x, y, _ = hub_edge
        assert a != x
        if z == y:
            spare_anchor = first(
                common_columns, lambda r: r != z
            )
            t = first(
                r_vertices,
                lambda r: r not in {z, spare_anchor}
                and edge(a, r) in graph,
            )
            selector = first(
                c_vertices,
                lambda c: c not in {center, x, a}
                and edge(c, t) in graph
                and edge(c, spare_anchor) in graph,
            )
            return [center, x, z, a, t, selector, spare_anchor]
        t = first(
            r_vertices,
            lambda r: r not in {y, z} and edge(a, r) in graph,
        )
        selector = first(
            c_vertices,
            lambda c: c not in {center, x, a}
            and edge(c, y) in graph
            and edge(c, t) in graph,
        )
        return [center, x, y, selector, t, a, z]

    case_counts = {
        "core_core": 0,
        "hub_hub_same_center": 0,
        "hub_hub_cross_centers": 0,
        "core_hub": 0,
    }
    detailed_case_counts = {
        "core_core_disjoint": 0,
        "core_core_same_row": 0,
        "core_core_same_column": 0,
        "same_hub_disjoint": 0,
        "same_hub_same_row": 0,
        "same_hub_same_column": 0,
        "cross_hub_different_columns": 0,
        "cross_hub_same_column": 0,
        "core_hub_different_columns": 0,
        "core_hub_same_column": 0,
    }
    for first_edge, second_edge in itertools.combinations(family, 2):
        if first_edge[2] == second_edge[2] == "core":
            cycle = core_witness(first_edge, second_edge)
            case_counts["core_core"] += 1
            if first_edge[0] == second_edge[0]:
                detailed_case_counts["core_core_same_row"] += 1
            elif first_edge[1] == second_edge[1]:
                detailed_case_counts["core_core_same_column"] += 1
            else:
                detailed_case_counts["core_core_disjoint"] += 1
        elif "core" in {first_edge[2], second_edge[2]}:
            core_edge, hub_edge = (
                (first_edge, second_edge)
                if first_edge[2] == "core"
                else (second_edge, first_edge)
            )
            if hub_edge[0] in p_rows:
                cycle = mixed_witness(core_edge, hub_edge, p)
            else:
                cycle = mixed_witness(core_edge, hub_edge, q)
            case_counts["core_hub"] += 1
            if core_edge[1] == hub_edge[1]:
                detailed_case_counts["core_hub_same_column"] += 1
            else:
                detailed_case_counts[
                    "core_hub_different_columns"
                ] += 1
        else:
            x1, x2 = first_edge[0], second_edge[0]
            if x1 in p_rows and x2 in p_rows:
                cycle = hub_witness(
                    first_edge, second_edge, p, p_rows, p_anchor
                )
                case_counts["hub_hub_same_center"] += 1
                if first_edge[0] == second_edge[0]:
                    detailed_case_counts["same_hub_same_row"] += 1
                elif first_edge[1] == second_edge[1]:
                    detailed_case_counts["same_hub_same_column"] += 1
                else:
                    detailed_case_counts["same_hub_disjoint"] += 1
            elif x1 in q_rows and x2 in q_rows:
                cycle = hub_witness(
                    first_edge, second_edge, q, q_rows, q_anchor
                )
                case_counts["hub_hub_same_center"] += 1
                if first_edge[0] == second_edge[0]:
                    detailed_case_counts["same_hub_same_row"] += 1
                elif first_edge[1] == second_edge[1]:
                    detailed_case_counts["same_hub_same_column"] += 1
                else:
                    detailed_case_counts["same_hub_disjoint"] += 1
            elif x1 in p_rows and x2 in q_rows:
                cycle = cross_hub_witness(first_edge, second_edge)
                case_counts["hub_hub_cross_centers"] += 1
                if first_edge[1] == second_edge[1]:
                    detailed_case_counts["cross_hub_same_column"] += 1
                else:
                    detailed_case_counts[
                        "cross_hub_different_columns"
                    ] += 1
            elif x2 in p_rows and x1 in q_rows:
                cycle = cross_hub_witness(second_edge, first_edge)
                case_counts["hub_hub_cross_centers"] += 1
                if first_edge[1] == second_edge[1]:
                    detailed_case_counts["cross_hub_same_column"] += 1
                else:
                    detailed_case_counts[
                        "cross_hub_different_columns"
                    ] += 1
            else:
                raise AssertionError("unclassified hub pair")
        check(cycle, first_edge, second_edge)

    return {
        "seed": seed,
        "C_size": a_size,
        "R_size": b_size,
        "p_hub_rows": len(p_rows),
        "q_hub_rows": len(q_rows),
        "p_raw_internal_rows": len(p_internal),
        "q_raw_internal_rows": len(q_internal),
        "p_hub_discarded_by_threshold":
            bool(p_internal) and not bool(p_rows),
        "q_hub_discarded_by_threshold":
            bool(q_internal) and not bool(q_rows),
        "hub_union_rows": len(union_rows),
        "common_columns": len(common_columns),
        "common_columns_raw": len(common_columns_raw),
        "family_edges": len(family),
        "edge_pairs_checked": len(family) * (len(family) - 1) // 2,
        "template_case_counts": case_counts,
        "detailed_template_case_counts": detailed_case_counts,
        "passed": True,
    }


def verify_optimization():
    """Check the normalized exact inequality on a fine rational grid.

    If x=max(h_p,h_q), y=min(h_p,h_q), u>=x and
    k>=max(0,1-x-y), then u+(1-u)k >= 1/2.  Monotonicity reduces this
    to u=x and the displayed lower bound for k.
    """

    checked = 0
    minimum = Fraction(1)
    minimizers = []
    denominator = 400
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
        "rational_pairs_checked": checked,
        "minimum": str(minimum),
        "sample_minimizers": [
            [str(x), str(y)] for x, y in minimizers[:5]
        ],
        "passed": minimum == Fraction(1, 2),
    }


def main():
    dense_instances = [verify_instance(seed) for seed in range(16)]
    sparse_profiles = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),
        (0, 9), (1, 9), (2, 9),
        (9, 0), (9, 1), (9, 2),
    ]
    sparse_instances = [
        verify_instance(
            1000 + index,
            p_extra_internal=p_degree,
            q_extra_internal=q_degree,
        )
        for index, (p_degree, q_degree) in enumerate(sparse_profiles)
    ]
    instances = dense_instances + sparse_instances
    output = {
        "claim": (
            "The displayed core/hub union templates produce simple C7s in "
            "finite dense and sparse-hub adversarial instances, subthreshold "
            "hub/core rectangles are explicitly discarded, and the "
            "normalized rectangle count is at least 1/2."
        ),
        "dense_instances": dense_instances,
        "sparse_hub_instances": sparse_instances,
        "sparse_hub_profiles": [
            {
                "p_extra_internal": p_degree,
                "q_extra_internal": q_degree,
            }
            for p_degree, q_degree in sparse_profiles
        ],
        "optimization": verify_optimization(),
        "scope_guard": (
            "This guards explicit templates and arithmetic only.  The "
            "asymptotic cleaning argument and the reduction into the split "
            "branch are proved in REPORT.md, not by finite enumeration."
        ),
        "passed": all(item["passed"] for item in instances),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
