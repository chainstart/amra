#!/usr/bin/env python3
"""Finite LP probe for signed low-conductor majorants on the CRT cube."""

from itertools import product
from math import prod

import numpy as np
from scipy.optimize import linprog


def main() -> None:
    primes = (11, 13, 17, 19, 23, 29, 31, 37, 41, 43)
    h_count = 5
    a = 0.2
    q_local = np.array([h_count / p for p in primes], dtype=float)
    patterns = np.array(tuple(product((0.0, 1.0), repeat=len(primes))))
    probabilities = np.prod(
        np.where(patterns == 1.0, q_local, 1.0 - q_local), axis=1
    )
    weight = np.prod(1.0 - a * patterns, axis=1)
    exact_mean = float(probabilities @ weight)
    full_modulus = prod(primes)

    ledgers = []
    for cutoff in (1, 100, 1000, 10000, 100000, full_modulus):
        supports = []
        for mask in range(1 << len(primes)):
            conductor = prod(
                p for index, p in enumerate(primes) if mask & (1 << index)
            )
            if conductor <= cutoff:
                supports.append(mask)

        design = np.empty((len(patterns), len(supports)), dtype=float)
        objective = np.empty(len(supports), dtype=float)
        for column, mask in enumerate(supports):
            indices = [
                index for index in range(len(primes)) if mask & (1 << index)
            ]
            design[:, column] = (
                np.prod(patterns[:, indices], axis=1) if indices else 1.0
            )
            objective[column] = (
                float(np.prod(q_local[indices])) if indices else 1.0
            )

        result = linprog(
            objective,
            A_ub=-design,
            b_ub=-weight,
            bounds=[(None, None)] * len(supports),
            method="highs",
        )
        assert result.success, result.message
        majorant = design @ result.x
        min_slack = float(np.min(majorant - weight))
        objective_check = float(probabilities @ majorant)
        assert min_slack > -2e-8
        assert abs(objective_check - result.fun) < 2e-8
        ledgers.append(
            (
                cutoff,
                len(supports),
                result.fun,
                result.fun / exact_mean,
                min_slack,
            )
        )

    print(
        "status=PASS "
        f"variables={len(primes)} patterns={len(patterns)} "
        f"exact_mean={exact_mean:.12f} full_modulus={full_modulus}"
    )
    for cutoff, terms, optimum, ratio, slack in ledgers:
        print(
            f"D={cutoff} terms={terms} optimum={optimum:.12f} "
            f"ratio_to_exact={ratio:.6f} min_slack={slack:.3e}"
        )


if __name__ == "__main__":
    main()
