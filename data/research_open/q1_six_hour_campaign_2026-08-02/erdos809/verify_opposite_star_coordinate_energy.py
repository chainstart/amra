#!/usr/bin/env python3
"""Finite graph guard for the common-coordinate missing-energy theorem."""

from __future__ import annotations

import argparse
import itertools
import json

from verify_opposite_star_common_host import (
    choose2,
    crossing_edges,
    graph_from_mask,
    missing_inside,
    opposite_zero_leaf,
)


def ceil_div(x, y):
    return (x + y - 1) // y


def audit_coordinate_system(edges, neighbours, aset, b, leaves):
    vertices = set(range(len(neighbours)))
    bset = vertices - aset
    pset = set(neighbours[b])
    qsets = [set(neighbours[c]) for c in leaves]
    union = set().union(*qsets)
    deficits = [len(union - qset) for qset in qsets]
    total_deficit = sum(deficits)

    common_a = set(aset).intersection(*qsets)
    degrees_a = [len(neighbours[c] & aset) for c in leaves]
    direct_lower = max(
        [0]
        + [
            degree + deficit - total_deficit
            for degree, deficit in zip(degrees_a, deficits)
        ]
    )
    average_lower = max(
        0,
        ceil_div(sum(degrees_a) + total_deficit, len(leaves))
        - total_deficit,
    )
    assert len(common_a) >= direct_lower
    assert direct_lower >= average_lower

    center_a = pset & aset
    assert center_a.isdisjoint(common_a)
    assert not any(
        tuple(sorted((x, y))) in edges for x in center_a for y in common_a
    )
    missing_a = missing_inside(edges, aset)
    assert missing_a >= len(center_a) * len(common_a)
    assert missing_a >= len(center_a) * average_lower

    delta = min(map(len, neighbours))
    spread = len(aset) - delta - 1
    assert spread >= 0
    cross_ab = crossing_edges(edges, aset, bset)
    missing_b = missing_inside(edges, bset)
    ledger_slack = (
        choose2(len(aset)) + choose2(len(bset)) - len(edges)
    )
    assert cross_ab == missing_a + missing_b - ledger_slack

    xsize = len(center_a)
    ysize = len(common_a)
    forced_cross = (
        xsize * max(0, ysize - spread)
        + ysize * max(0, xsize - spread)
    )
    assert cross_ab >= forced_cross
    assert missing_b >= forced_cross - missing_a + ledger_slack
    if xsize >= spread and ysize >= spread:
        outside_rectangle = missing_a - xsize * ysize
        assert outside_rectangle >= 0
        assert missing_b >= (
            xsize * ysize
            - spread * (xsize + ysize)
            - outside_rectangle
            + ledger_slack
        )


def run_exhaustive(max_n=5):
    graphs = 0
    witness_partitions = 0
    star_systems = 0
    for n in range(2, max_n + 1):
        for mask in range(1 << choose2(n)):
            graphs += 1
            edges, neighbours = graph_from_mask(n, mask)
            max_degree = max(map(len, neighbours))
            for v in range(n):
                if len(neighbours[v]) != max_degree:
                    continue
                aset = set(neighbours[v]) | {v}
                bset = set(range(n)) - aset
                if not bset:
                    continue
                witness_partitions += 1
                for b in bset:
                    eligible = [
                        c
                        for c in bset
                        if opposite_zero_leaf(edges, neighbours, b, c)
                    ]
                    for size in range(1, len(eligible) + 1):
                        for leaves in itertools.combinations(eligible, size):
                            audit_coordinate_system(
                                edges, neighbours, aset, b, leaves
                            )
                            star_systems += 1
    return {
        "schema": "amra.erdos809.opposite-star-coordinate-energy.v1",
        "max_n": max_n,
        "graphs": graphs,
        "maximum_degree_partitions": witness_partitions,
        "star_systems": star_systems,
        "status": "PASS",
        "scope": "finite graph guard only; universal proof is in the note",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(run_exhaustive(args.max_n), indent=2, sort_keys=True))
