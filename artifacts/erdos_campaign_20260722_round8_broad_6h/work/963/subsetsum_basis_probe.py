#!/usr/bin/env python3
"""Falsify the proposed subset-sum-basis strengthening for Erdős #963.

For a finite positive integer set P, let d(P) be the largest cardinality of a
dissociated subset.  The proposed strengthening says that some maximum
dissociated B subset P satisfies P subset FS(B), where FS(B) denotes ordinary
0/1 subset sums.  This would imply |P| <= 2^d(P)-1, hence the original
conjecture, so a small counterexample is the first thing to seek.

The exhaustive mode checks all P subset [1,M].  The random mode samples sets
from [1,M].  Every reported counterexample is independently rechecked from
integer subset sums before it is printed.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random


def subset_sums(values: tuple[int, ...]) -> set[int]:
    sums = {0}
    for value in values:
        sums |= {s + value for s in tuple(sums)}
    return sums


def dissociated(values: tuple[int, ...]) -> bool:
    return len(subset_sums(values)) == 1 << len(values)


def maximum_bases(P: tuple[int, ...]) -> tuple[int, list[tuple[int, ...]]]:
    for r in range(len(P), -1, -1):
        bases = [B for B in itertools.combinations(P, r) if dissociated(B)]
        if bases:
            return r, bases
    raise AssertionError("empty set is always dissociated")


def check(P: tuple[int, ...]) -> dict | None:
    rank, bases = maximum_bases(P)
    good = [B for B in bases if set(P) <= subset_sums(B)]
    if good:
        return None
    # Independent replay of every relevant finite predicate.
    assert all(dissociated(B) for B in bases)
    assert all(not any(dissociated(C) for C in itertools.combinations(P, rank + 1))
               for _ in [0])
    witnesses = []
    for B in bases:
        missing = sorted(set(P) - subset_sums(B))
        assert missing
        witnesses.append({"basis": B, "missing": missing})
    return {
        "P": P,
        "size": len(P),
        "dissociated_rank": rank,
        "maximum_basis_count": len(bases),
        "basis_failures": witnesses,
    }


def exhaustive(M: int, minimum_size: int) -> dict | None:
    universe = tuple(range(1, M + 1))
    for size in range(minimum_size, M + 1):
        for P in itertools.combinations(universe, size):
            result = check(P)
            if result is not None:
                result.update({"mode": "exhaustive", "M": M})
                return result
    return None


def random_search(M: int, trials: int, seed: int, minimum_size: int) -> dict | None:
    rng = random.Random(seed)
    universe = tuple(range(1, M + 1))
    for trial in range(1, trials + 1):
        size = rng.randint(minimum_size, M)
        P = tuple(sorted(rng.sample(universe, size)))
        result = check(P)
        if result is not None:
            result.update({"mode": "random", "M": M, "trial": trial, "seed": seed})
            return result
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--M", type=int, default=14)
    parser.add_argument("--minimum-size", type=int, default=3)
    parser.add_argument("--random-trials", type=int, default=0)
    parser.add_argument("--seed", type=int, default=963)
    args = parser.parse_args()
    if args.random_trials:
        result = random_search(args.M, args.random_trials, args.seed, args.minimum_size)
    else:
        result = exhaustive(args.M, args.minimum_size)
    print(json.dumps({"counterexample": result}, separators=(",", ":")))


if __name__ == "__main__":
    main()
