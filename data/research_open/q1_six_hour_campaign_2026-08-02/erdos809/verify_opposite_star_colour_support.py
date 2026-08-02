#!/usr/bin/env python3
"""Finite guards for leaf-independence colour-support compression."""

from __future__ import annotations

import argparse
import itertools
import json
import math


def choose2(x):
    return x * (x - 1) // 2


def ceil_div(x, y):
    return (x + y - 1) // y


def run_exhaustive(max_leaves=6):
    graphs = 0
    independent_sets_checked = 0
    aggregate_support_systems = 0
    union_rectangle_systems = 0
    for ell in range(1, max_leaves + 1):
        pairs = list(itertools.combinations(range(ell), 2))
        for mask in range(1 << len(pairs)):
            graphs += 1
            edges = {
                pair for index, pair in enumerate(pairs)
                if (mask >> index) & 1
            }
            independent = []
            for subset_mask in range(1, 1 << ell):
                subset = {
                    vertex for vertex in range(ell)
                    if (subset_mask >> vertex) & 1
                }
                if not any(set(pair) <= subset for pair in edges):
                    independent.append(subset)
                    independent_sets_checked += 1

            alpha = max(map(len, independent))
            missing_edges = choose2(ell) - len(edges)
            assert choose2(alpha) <= missing_edges
            reserve_root = (1 + math.isqrt(1 + 8 * missing_edges)) // 2
            assert alpha <= reserve_root

            ordered = sorted(independent, key=lambda item: (len(item), sorted(item)))
            for stop in range(1, len(ordered) + 1):
                supports = ordered[:stop]
                incidence_mass = sum(map(len, supports))
                colour_count = len(supports)
                assert colour_count >= ceil_div(incidence_mass, alpha)

                loads = [
                    sum(vertex in support for support in supports)
                    for vertex in range(ell)
                ]
                maximum_load = max(loads)
                union_rectangle = colour_count * maximum_load
                assert maximum_load >= ceil_div(incidence_mass, ell)
                assert union_rectangle >= (
                    ceil_div(incidence_mass, alpha) * maximum_load
                )
                assert union_rectangle >= (
                    ceil_div(incidence_mass, alpha)
                    * ceil_div(incidence_mass, ell)
                )

                # Replacing the exact independence number by the root
                # forced by an available missing-edge reserve remains valid.
                reserve_alpha_cap = (
                    1 + math.isqrt(1 + 8 * missing_edges)
                ) // 2
                assert alpha <= reserve_alpha_cap
                assert union_rectangle >= (
                    ceil_div(incidence_mass, reserve_alpha_cap)
                    * ceil_div(incidence_mass, ell)
                )
                assert incidence_mass * incidence_mass <= (
                    reserve_alpha_cap * ell * union_rectangle
                )
                aggregate_support_systems += 1
                union_rectangle_systems += 1

    return {
        "schema": "amra.erdos809.opposite-star-colour-support.v1",
        "max_leaves": max_leaves,
        "graphs": graphs,
        "independent_sets_checked": independent_sets_checked,
        "aggregate_support_systems": aggregate_support_systems,
        "union_rectangle_systems": union_rectangle_systems,
        "status": "PASS",
        "scope": (
            "finite incidence/union-rectangle guard; "
            "universal proof is in the notes"
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-leaves", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(run_exhaustive(args.max_leaves), indent=2, sort_keys=True))
