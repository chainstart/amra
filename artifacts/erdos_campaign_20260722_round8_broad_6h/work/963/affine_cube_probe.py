#!/usr/bin/env python3
"""Probe an affine Boolean-cube strengthening suggested by Erdős #963.

The conjectural strengthening is: if d(P)=r, then P is contained in an
affine Boolean cube c+FS(d_1,...,d_r).  It would immediately imply
|P|<=2^r.  This program searches positive integer sets and asks exact Z3
linear real arithmetic whether such a containment exists.

SAT output is only diagnostic.  UNSAT output is a rigorous solver result but
must be replaced by an independently checkable finite certificate before it
is used in a mathematical report.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random

from z3 import Bool, If, Real, Solver, sat


def subset_sums(values: tuple[int, ...]) -> set[int]:
    sums = {0}
    for value in values:
        sums |= {s + value for s in tuple(sums)}
    return sums


def dissociated(values: tuple[int, ...]) -> bool:
    return len(subset_sums(values)) == 1 << len(values)


def rank(P: tuple[int, ...]) -> int:
    # For positive integers <= max(P), 2^r distinct subset sums lie in
    # [0,r*max(P)], so 2^r <= r*max(P)+1.  This avoids starting an
    # exponential scan at |P| for dense random samples.
    upper = 0
    for candidate in range(1, len(P) + 1):
        if (1 << candidate) <= candidate * max(P) + 1:
            upper = candidate
        else:
            break
    for r in range(upper, -1, -1):
        if any(dissociated(B) for B in itertools.combinations(P, r)):
            return r
    raise AssertionError


def affine_cube(P: tuple[int, ...], r: int, timeout_ms: int) -> dict:
    solver = Solver()
    solver.set(timeout=timeout_ms)
    c = Real("c")
    directions = [Real(f"d_{j}") for j in range(r)]
    codes = [[Bool(f"e_{i}_{j}") for j in range(r)] for i in range(len(P))]
    for i, value in enumerate(P):
        solver.add(value == c + sum(If(codes[i][j], directions[j], 0) for j in range(r)))
    outcome = solver.check()
    result = {"status": str(outcome)}
    if outcome == sat:
        model = solver.model()
        result["c"] = str(model.eval(c, model_completion=True))
        result["directions"] = [str(model.eval(d, model_completion=True)) for d in directions]
        result["codes"] = [
            [bool(model.eval(bit, model_completion=True)) for bit in row]
            for row in codes
        ]
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--M", type=int, default=12)
    parser.add_argument("--minimum-size", type=int, default=4)
    parser.add_argument("--maximum-size", type=int)
    parser.add_argument("--timeout-ms", type=int, default=10000)
    parser.add_argument("--random-trials", type=int, default=0)
    parser.add_argument("--seed", type=int, default=1963)
    args = parser.parse_args()
    checked = 0
    if args.random_trials:
        rng = random.Random(args.seed)
        for trial in range(1, args.random_trials + 1):
            maximum_size = min(args.M, args.maximum_size or args.M)
            size = rng.randint(args.minimum_size, maximum_size)
            P = tuple(sorted(rng.sample(range(1, args.M + 1), size)))
            r = rank(P)
            if len(P) <= r + 1:
                continue
            checked += 1
            result = affine_cube(P, r, args.timeout_ms)
            if result["status"] != "sat":
                print(json.dumps({
                    "candidate_counterexample": P,
                    "size": size,
                    "dissociated_rank": r,
                    "solver": result,
                    "trial": trial,
                    "seed": args.seed,
                    "checked_before": checked - 1,
                }, separators=(",", ":")))
                return
        print(json.dumps({"candidate_counterexample": None, "checked": checked,
                          "random_trials": args.random_trials, "seed": args.seed},
                         separators=(",", ":")))
        return
    for size in range(args.minimum_size, args.M + 1):
        for P in itertools.combinations(range(1, args.M + 1), size):
            r = rank(P)
            if len(P) <= r + 1:
                continue
            checked += 1
            result = affine_cube(P, r, args.timeout_ms)
            if result["status"] != "sat":
                print(json.dumps({
                    "candidate_counterexample": P,
                    "size": size,
                    "dissociated_rank": r,
                    "solver": result,
                    "checked_before": checked - 1,
                }, separators=(",", ":")))
                return
    print(json.dumps({"candidate_counterexample": None, "checked": checked}, separators=(",", ":")))


if __name__ == "__main__":
    main()
