#!/usr/bin/env python3
"""Discovery-only continuous search in successively stronger outer cones.

SciPy is used only for routing.  Any candidate must be rationalized and
replayed by a standard-library exact verifier before it becomes evidence.
"""

from __future__ import annotations

from itertools import combinations
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

from verify_falsification_witnesses import EDGES, reconstruct_complements  # noqa: E402


def mask(complement):
    return sum(1 << EDGES.index(edge) for edge in complement)


def simple_cycles():
    cycles = set()
    vertices = range(5)
    edge_set = {tuple(sorted(edge)) for edge in EDGES}
    from itertools import permutations

    for length in range(3, 6):
        for order in permutations(vertices, length):
            if order[0] != min(order):
                continue
            if order[1] > order[-1]:
                continue
            cycle_edges = tuple(
                sorted(
                    tuple(sorted((order[index], order[(index + 1) % length])))
                    for index in range(length)
                )
            )
            if all(edge in edge_set for edge in cycle_edges):
                cycles.add(cycle_edges)
    return tuple(sorted(cycles))


def monomial_values(weights):
    values = np.ones(1 << len(EDGES))
    for subset in range(1, len(values)):
        bit = subset & -subset
        index = bit.bit_length() - 1
        values[subset] = values[subset ^ bit] * weights[index]
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cone", choices=("p", "cycles", "derivatives"), default="p")
    parser.add_argument("--target", choices=("xi", "edge_slope", "edge_delta"), default="xi")
    parser.add_argument(
        "--eliminate",
        choices=("x01", "x02", "b", "c", "x13", "x14", "x23", "x24"),
        default="b",
    )
    parser.add_argument("--maxiter", type=int, default=400)
    parser.add_argument("--seed", type=int, default=1757)
    parser.add_argument("--p-floor", type=float, default=1e-8)
    parser.add_argument("--cycle-floor", type=float, default=1e-7)
    parser.add_argument(
        "--max-derivative-order",
        type=int,
        default=None,
        help="when set, enforce P derivatives only through this order",
    )
    args = parser.parse_args()

    deletion, connectivity = reconstruct_complements()
    deletion_masks = tuple(mask(complement) for complement in deletion)
    connectivity_masks = tuple(mask(complement) for complement in connectivity)
    cycles = simple_cycles()
    cycle_indices = tuple(tuple(EDGES.index(edge) for edge in cycle) for cycle in cycles)
    derivative_residuals = tuple(
        tuple(complement ^ subset for complement in deletion_masks if complement & subset == subset)
        for subset in range(1 << len(EDGES))
    )
    constrained_derivative_indices = tuple(
        subset
        for subset in range(1 << len(EDGES))
        if args.max_derivative_order is None
        or subset.bit_count() <= args.max_derivative_order
    )

    edge_names = ("x01", "x02", "b", "c", "x13", "x14", "x23", "x24")
    eliminated_index = edge_names.index(args.eliminate)
    eliminated_bit = 1 << eliminated_index

    def evaluate(weights):
        values = monomial_values(weights)
        p_value = sum(values[index] for index in deletion_masks)
        xi_value = sum(values[index] for index in connectivity_masks)
        p_slope = sum(
            values[index ^ eliminated_bit]
            for index in deletion_masks
            if index & eliminated_bit
        )
        p_zero = sum(
            values[index] for index in deletion_masks if not index & eliminated_bit
        )
        xi_slope = sum(
            values[index ^ eliminated_bit]
            for index in connectivity_masks
            if index & eliminated_bit
        )
        xi_zero = sum(
            values[index] for index in connectivity_masks if not index & eliminated_bit
        )
        delta = p_slope * xi_zero - xi_slope * p_zero
        return values, p_value, xi_value, xi_slope, delta

    def objective(weights):
        values, p_value, xi_value, xi_slope, delta = evaluate(weights)
        if p_value <= args.p_floor:
            return 1e6 + (1 - p_value) ** 2
        if args.cone in {"cycles", "derivatives"}:
            logs = np.log1p(weights)
            smallest_cycle = min(sum(logs[index] for index in cycle) for cycle in cycle_indices)
            if smallest_cycle <= args.cycle_floor:
                return 1e5 + (1 - smallest_cycle) ** 2
        if args.cone == "derivatives":
            derivatives = np.array(
                [
                    sum(values[index] for index in derivative_residuals[subset])
                    for subset in constrained_derivative_indices
                ]
            )
            smallest = derivatives.min()
            if smallest <= 1e-8:
                return 1e4 + (1 - smallest) ** 2
        return {"xi": xi_value, "edge_slope": xi_slope, "edge_delta": delta}[args.target]

    result = differential_evolution(
        objective,
        bounds=[(-0.99, 6.0)] * len(EDGES),
        maxiter=args.maxiter,
        popsize=20,
        polish=True,
        seed=args.seed,
        workers=1,
        updating="immediate",
        tol=1e-9,
    )
    values, p_value, xi_value, xi_slope, delta = evaluate(result.x)
    derivatives = np.array(
        [sum(values[index] for index in residuals) for residuals in derivative_residuals]
    )
    logs = np.log1p(result.x)
    print({
        "cone": args.cone,
        "target": args.target,
        "eliminate": args.eliminate,
        "success": bool(result.success),
        "objective": float(result.fun),
        "weights": [float(value) for value in result.x],
        "P": float(p_value),
        "xi": float(xi_value),
        "edge_slope": float(xi_slope),
        "edge_delta": float(delta),
        "minimum_cycle_log_sum": float(
            min(sum(logs[index] for index in cycle) for cycle in cycle_indices)
        ),
        "minimum_derivative": float(derivatives.min()),
        "nonpositive_derivatives": int(np.count_nonzero(derivatives <= 0)),
        "max_derivative_order": args.max_derivative_order,
        "constrained_derivatives": len(constrained_derivative_indices),
        "cycles": len(cycles),
    })


if __name__ == "__main__":
    main()
