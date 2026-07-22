#!/usr/bin/env python3
"""Finite falsification checks for the progression bound in (4).

The theorem itself is the integral comparison in HARMONIC_WEIGHTED_CLIQUES.md;
this script checks small parameters exhaustively and a deterministic random
box.  Floating point is used only to look for counterexamples with slack.
"""

from __future__ import annotations

import json
import math
import random


def progression_sum(L: int, r: int, M: int, X: int) -> float:
    return sum(
        1.0 / value
        for value in range(r, X + 1, L)
        if value >= M
    )


def check(L: int, r: int, M: int, X: int) -> float:
    error = abs(progression_sum(L, r, M, X) - math.log(X) / L)
    budget = 2.0 / r + (2.0 + math.log(2 * L)) / L
    assert error <= budget + 1e-12, (L, r, M, X, error, budget)
    return error / budget


def main() -> None:
    tested = 0
    maximum_ratio = 0.0
    for L in range(1, 21):
        for r in range(1, L + 1):
            for M in range(1, L + 1):
                for X in range(1, 4 * L + 1):
                    maximum_ratio = max(maximum_ratio, check(L, r, M, X))
                    tested += 1

    rng = random.Random(2500252026)
    random_cases = 5000
    for _ in range(random_cases):
        L = rng.randint(1, 5000)
        r = rng.randint(1, L)
        M = rng.randint(1, L)
        X = rng.randint(1, 20 * L)
        maximum_ratio = max(maximum_ratio, check(L, r, M, X))
        tested += 1

    print(json.dumps({
        "schema": "amra.erdos25.harmonic-weight.v1",
        "status": "PASS",
        "exhaustive": {"max_L": 20, "max_X_over_L": 4},
        "random_seed": 2500252026,
        "random_cases": random_cases,
        "total_cases": tested,
        "maximum_error_over_stated_budget": maximum_ratio,
        "scope_warning": "Finite floating-point falsifier; the uniform bound is proved by integral comparison.",
    }, indent=2))


if __name__ == "__main__":
    main()
