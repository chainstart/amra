#!/usr/bin/env python3
"""Discovery-only search for Delta_b<0 on the exact route PD chamber.

The projected book polynomial is det(diag(q0,q3,q4,c)+J).  This script
parameterizes the positive-definite component exactly: either every diagonal
q is positive, or one q_i=-a is negative with

    0 < a < 1 / (1 + sum_{j != i} 1/q_j).

SciPy is used only for routing.  Candidates still require exact replay.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import differential_evolution


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_c_zero_fibre import (  # noqa: E402
    EDGES,
    add,
    derivative,
    multiply,
    reconstruct_original,
    restrict_original_zero,
)


B_EDGE = (0, 4)
ROUTE_EDGES = (
    ((0, 1), (0, 2)),
    ((1, 3), (2, 3)),
    ((1, 4), (2, 4)),
)
ROUTE_NAMES = ("q0", "q3", "q4", "c")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--small",
        choices=("none",) + ROUTE_NAMES,
        default="none",
        help="the unique negative effective route, if any",
    )
    parser.add_argument("--bound", type=float, default=10.0)
    parser.add_argument("--maxiter", type=int, default=1200)
    parser.add_argument("--seed", type=int, default=1757)
    args = parser.parse_args()

    deletion, connectivity, _, _ = reconstruct_original()
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add(multiply(a_slope, e_zero), multiply(d_slope, c_zero), -1)
    terms = tuple(delta.items())

    small_index = None if args.small == "none" else ROUTE_NAMES.index(args.small)

    def decode(parameters):
        positive = np.exp(parameters[:4])
        q = positive.copy()
        if small_index is not None:
            reciprocal_sum = sum(
                1.0 / positive[index]
                for index in range(4)
                if index != small_index
            )
            maximum = 1.0 / (1.0 + reciprocal_sum)
            fraction = 1.0 / (1.0 + np.exp(-parameters[small_index]))
            q[small_index] = -maximum * fraction

        route_products = 1.0 + q[:3]
        imbalances = parameters[4:]
        floors = {}
        for product, imbalance, edges in zip(route_products, imbalances, ROUTE_EDGES):
            root = np.sqrt(product)
            floors[edges[0]] = root * np.exp(imbalance / 2.0)
            floors[edges[1]] = root * np.exp(-imbalance / 2.0)
        floors[(1, 2)] = 1.0 + q[3]
        floors[B_EDGE] = 1.0
        weights = np.array([floors[edge] - 1.0 for edge in EDGES])
        return q, weights

    def evaluate(parameters):
        q, weights = decode(parameters)
        value = 0.0
        scale = 0.0
        for exponent, coefficient in terms:
            monomial = float(coefficient)
            for index, degree in enumerate(exponent):
                if degree:
                    monomial *= weights[index] ** degree
            value += monomial
            scale += abs(monomial)
        return value, max(scale, 1.0), q, weights

    def objective(parameters):
        value, scale, _, _ = evaluate(parameters)
        return value / scale

    result = differential_evolution(
        objective,
        bounds=[(-args.bound, args.bound)] * 7,
        maxiter=args.maxiter,
        popsize=25,
        polish=True,
        seed=args.seed,
        workers=1,
        updating="immediate",
        tol=1e-10,
    )
    value, scale, q, weights = evaluate(result.x)
    matrix = np.diag(q) + np.ones((4, 4))
    print({
        "small": args.small,
        "success": bool(result.success),
        "objective": float(result.fun),
        "parameters": [float(item) for item in result.x],
        "effective_activities": [float(item) for item in q],
        "minimum_matrix_eigenvalue": float(np.linalg.eigvalsh(matrix).min()),
        "weights": [float(item) for item in weights],
        "Delta_b": float(value),
        "absolute_monomial_scale": float(scale),
    })


if __name__ == "__main__":
    main()
