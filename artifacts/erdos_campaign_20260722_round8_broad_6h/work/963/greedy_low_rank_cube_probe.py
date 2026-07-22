#!/usr/bin/env python3
"""Generate diverse low-dissociation-rank integer sets and test cube cover.

This is a falsification aid for the affine Boolean-cube route.  It greedily
builds sets with no dissociated (r+1)-subset under random orderings, then uses
the exact LRA/Boolean model from affine_cube_probe to test containment in an
r-dimensional affine Boolean cube.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random

from affine_cube_probe import affine_cube, dissociated, rank


def can_add(P: list[int], value: int, r: int) -> bool:
    if len(P) < r:
        return True
    return not any(dissociated(tuple((*base, value)))
                   for base in itertools.combinations(P, r))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--M", type=int, default=80)
    parser.add_argument("--rank", type=int, default=4)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=2963)
    parser.add_argument("--timeout-ms", type=int, default=30000)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    size_histogram: dict[int, int] = {}
    cube_checks = 0
    for trial in range(1, args.trials + 1):
        order = list(range(1, args.M + 1))
        rng.shuffle(order)
        P: list[int] = []
        for value in order:
            if can_add(P, value, args.rank):
                P.append(value)
        P.sort()
        actual_rank = rank(tuple(P))
        assert actual_rank <= args.rank
        size_histogram[len(P)] = size_histogram.get(len(P), 0) + 1
        if len(P) <= actual_rank + 1:
            continue
        cube_checks += 1
        result = affine_cube(tuple(P), actual_rank, args.timeout_ms)
        if result["status"] != "sat":
            print(json.dumps({
                "candidate_counterexample": P,
                "dissociated_rank": actual_rank,
                "trial": trial,
                "seed": args.seed,
                "solver": result,
                "size_histogram_so_far": size_histogram,
            }, separators=(",", ":")))
            return
    print(json.dumps({
        "candidate_counterexample": None,
        "trials": args.trials,
        "seed": args.seed,
        "cube_checks": cube_checks,
        "size_histogram": size_histogram,
    }, separators=(",", ":")))


if __name__ == "__main__":
    main()
