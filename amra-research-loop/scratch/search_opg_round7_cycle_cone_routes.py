#!/usr/bin/env python3
"""Discovery-only search for Delta_b<0 in the projected book cycle cone.

Each length-two route is parameterized by its log product and an internal log
imbalance.  Pairwise sums of the four route log products are exactly the six
simple-cycle derivative inequalities after deleting b.  The objective is
Delta divided by its absolute monomial sum, so its sign is preserved while
extreme edge-floor scales remain numerically searchable.
"""

from __future__ import annotations

from pathlib import Path
import argparse
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=float, default=8.0)
    parser.add_argument("--maxiter", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=1757)
    parser.add_argument("--slopes", choices=("none", "a", "ad"), default="none")
    parser.add_argument(
        "--nonnegative-routes",
        action="store_true",
        help="restrict all four route logs to be nonnegative",
    )
    args = parser.parse_args()

    deletion, connectivity, _, _ = reconstruct_original()
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add(multiply(a_slope, e_zero), multiply(d_slope, c_zero), -1)
    terms = tuple(delta.items())

    def evaluate_polynomial(poly, weights):
        value = 0.0
        for exponent, coefficient in poly.items():
            monomial = float(coefficient)
            for index, degree in enumerate(exponent):
                if degree:
                    monomial *= weights[index] ** degree
            value += monomial
        return value

    def weights_from(parameters):
        r0, r3, r4, rc, s0, s3, s4 = parameters
        edge_floors = {
            (0, 1): np.exp((r0 + s0) / 2),
            (0, 2): np.exp((r0 - s0) / 2),
            (1, 3): np.exp((r3 + s3) / 2),
            (2, 3): np.exp((r3 - s3) / 2),
            (1, 4): np.exp((r4 + s4) / 2),
            (2, 4): np.exp((r4 - s4) / 2),
            (1, 2): np.exp(rc),
            B_EDGE: 1.0,
        }
        return np.array([edge_floors[edge] - 1 for edge in EDGES])

    def delta_and_scale(parameters):
        weights = weights_from(parameters)
        value = 0.0
        scale = 0.0
        for exponent, coefficient in terms:
            monomial = float(coefficient)
            for index, degree in enumerate(exponent):
                if degree:
                    monomial *= weights[index] ** degree
            value += monomial
            scale += abs(monomial)
        return (
            value,
            max(scale, 1.0),
            evaluate_polynomial(a_slope, weights),
            evaluate_polynomial(d_slope, weights),
            weights,
        )

    def objective(parameters):
        route_logs = parameters[:4]
        minimum_cycle_log = min(
            route_logs[left] + route_logs[right]
            for left in range(4)
            for right in range(left + 1, 4)
        )
        if minimum_cycle_log <= 1e-8:
            return 2.0 + (1.0 - minimum_cycle_log) ** 2
        value, scale, a_value, d_value, _ = delta_and_scale(parameters)
        if args.slopes in {"a", "ad"} and a_value <= 1e-8:
            return 1.0 + (1.0 - a_value) ** 2
        if args.slopes == "ad" and d_value <= 1e-8:
            return 1.0 + (1.0 - d_value) ** 2
        return value / scale

    bounds = [
        (0.0, args.bound) if args.nonnegative_routes and index < 4 else (-args.bound, args.bound)
        for index in range(7)
    ]
    result = differential_evolution(
        objective,
        bounds=bounds,
        maxiter=args.maxiter,
        popsize=25,
        polish=True,
        seed=args.seed,
        workers=1,
        updating="immediate",
        tol=1e-10,
    )
    value, scale, a_value, d_value, weights = delta_and_scale(result.x)
    route_logs = result.x[:4]
    print({
        "success": bool(result.success),
        "objective": float(result.fun),
        "parameters": [float(item) for item in result.x],
        "weights": [float(item) for item in weights],
        "Delta_b": float(value),
        "A": float(a_value),
        "D": float(d_value),
        "absolute_monomial_scale": float(scale),
        "minimum_cycle_log_sum": float(min(
            route_logs[left] + route_logs[right]
            for left in range(4)
            for right in range(left + 1, 4)
        )),
        "bound": args.bound,
        "slopes": args.slopes,
        "nonnegative_routes": args.nonnegative_routes,
    })


if __name__ == "__main__":
    main()
