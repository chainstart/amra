#!/usr/bin/env python3
"""Fit the free bivariate Bernstein-Gram entry from exact coefficient features."""

from __future__ import annotations

from pathlib import Path
import math
import random
import sys
from itertools import product

import numpy as np
from scipy.optimize import linprog, minimize_scalar


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from verify_mixed_three_negative import divide_polynomial  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    variable,
)
from verify_negative_nonshared_same_side_gram import positive_route_data  # noqa: E402
from verify_negative_q0_no_positive_gram import build_delta, coefficient  # noqa: E402
from explore_opg_round7_negative_q3_single_uniform import cleared_polynomial  # noqa: E402
from explore_opg_round7_remaining_single_gram import manifest_factor  # noqa: E402


def evaluate(poly, values):
    return sum(
        float(coefficient_) * math.prod(
            values[index] ** degree
            for index, degree in enumerate(monomial)
            if degree
        )
        for monomial, coefficient_ in poly.items()
    )


def matrix(entries, free):
    return np.array([
        [entries[0], entries[1], entries[3], free],
        [entries[1], entries[2], 2 * entries[4] - free, entries[5]],
        [entries[3], 2 * entries[4] - free, entries[6], entries[7]],
        [free, entries[5], entries[7], entries[8]],
    ])


def minimum_eigenvalue(entries, free):
    return np.linalg.eigvalsh(matrix(entries, free))[0]


def feasible_interval(entries):
    scale = max(abs(entries))
    normalized = entries / scale
    interval = feasible_interval_normalized(normalized)
    return None if interval is None else (interval[0] * scale, interval[1] * scale)


def feasible_interval_normalized(entries):
    bound03 = math.sqrt(max(0.0, entries[0] * entries[8]))
    bound12 = math.sqrt(max(0.0, entries[2] * entries[6]))
    lower = max(-bound03, 2 * entries[4] - bound12)
    upper = min(bound03, 2 * entries[4] + bound12)
    assert lower <= upper
    result = minimize_scalar(
        lambda free: -minimum_eigenvalue(entries, free),
        bounds=(lower, upper),
        method="bounded",
        options={"xatol": 1e-14},
    )
    optimum = result.x
    if minimum_eigenvalue(entries, optimum) < -1e-9:
        return None

    def boundary(outside, inside):
        if minimum_eigenvalue(entries, outside) >= -1e-11:
            return outside
        for _ in range(70):
            middle = (outside + inside) / 2
            if minimum_eigenvalue(entries, middle) >= 0:
                inside = middle
            else:
                outside = middle
        return inside

    return boundary(lower, optimum), boundary(upper, optimum)


def main():
    delta, _, _ = build_delta()
    core = divide_polynomial(cleared_polynomial(delta, "RLP"), manifest_factor("RLP"))
    transformed = bernstein_transform(core, [4, 6])
    polynomials = [
        coefficient(coefficient(transformed, 4, i), 6, j)
        for i in range(3)
        for j in range(3)
    ]

    features = []
    lowers = []
    uppers = []
    for _ in range(1500):
        values = (
            10 ** random.uniform(-2, 2),
            10 ** random.uniform(-2, 2),
            random.random(),
            0,
            0,
            10 ** random.uniform(-2, 2),
            0,
            random.random(),
        )
        entries = np.array([evaluate(poly, values) for poly in polynomials])
        scale = max(abs(entries))
        interval = feasible_interval(entries)
        if interval is None:
            print("no_pointwise_gram", values)
            return
        lower, upper = interval
        features.append(entries / scale)
        lowers.append(lower / scale)
        uppers.append(upper / scale)
    features = np.array(features)
    lowers = np.array(lowers)
    uppers = np.array(uppers)
    constraints = np.vstack((features, -features))
    bounds = np.concatenate((uppers, -lowers))
    result = linprog(
        np.zeros(9),
        A_ub=constraints,
        b_ub=bounds,
        bounds=[(None, None)] * 9,
        method="highs",
    )
    print("linear_entries", result.success, result.message)
    if result.success:
        print(result.x)

    c, q0, s0, q4 = (variable(slot) for slot in (0, 1, 2, 5))
    _, _, determinant_sum = positive_route_data(1)
    common = multiply(
        multiply(multiply(c, q4), multiply(s0, add(constant(1), s0, -1))),
        multiply(add(q0, s0), determinant_sum),
    )

    box_features = []
    for c_degree, q0_degree, s0_degree, q4_degree, tau_degree in product(
        range(2), range(3), range(2), range(2), range(2)
    ):
        monomial = [0] * 8
        for slot, degree in zip(
            (0, 1, 2, 5, 7),
            (c_degree, q0_degree, s0_degree, q4_degree, tau_degree),
        ):
            monomial[slot] = degree
        box_features.append({tuple(monomial): 1})

    features = []
    lowers = []
    uppers = []
    for _ in range(3500):
        values = (
            10 ** random.uniform(-3, 3),
            10 ** random.uniform(-3, 3),
            random.random(),
            0,
            0,
            10 ** random.uniform(-3, 3),
            0,
            random.random(),
        )
        entries = np.array([evaluate(poly, values) for poly in polynomials])
        scale = max(abs(entries))
        lower, upper = feasible_interval(entries)
        common_value = evaluate(common, values)
        features.append([
            common_value * evaluate(feature, values) / scale
            for feature in box_features
        ])
        lowers.append(lower / scale)
        uppers.append(upper / scale)
    features = np.array(features)
    result = linprog(
        np.zeros(len(box_features)),
        A_ub=np.vstack((features, -features)),
        b_ub=np.concatenate((np.array(uppers), -np.array(lowers))),
        bounds=[(None, None)] * len(box_features),
        method="highs",
    )
    print("quotient_box", result.success, result.message)
    if result.success:
        print(result.x)

    quotient = divide_polynomial(polynomials[4], common)
    assert polynomials[4] == multiply(common, quotient)
    monomial_features = [{monomial: 1} for monomial in quotient]
    print("quotient_terms", len(quotient))

    features = []
    lowers = []
    uppers = []
    for _ in range(2500):
        values = (
            10 ** random.uniform(-3, 3),
            10 ** random.uniform(-3, 3),
            random.random(),
            0,
            0,
            10 ** random.uniform(-3, 3),
            0,
            random.random(),
        )
        entries = np.array([evaluate(poly, values) for poly in polynomials])
        scale = max(abs(entries))
        interval = feasible_interval(entries)
        if interval is None:
            print("no_pointwise_gram_monomial", values)
            return
        lower, upper = interval
        common_value = evaluate(common, values)
        features.append([
            common_value * evaluate(feature, values) / scale
            for feature in monomial_features
        ])
        lowers.append(lower / scale)
        uppers.append(upper / scale)
    features = np.array(features)
    constraints = np.vstack((features, -features))
    bounds = np.concatenate((np.array(uppers), -np.array(lowers)))
    result = linprog(
        np.zeros(len(monomial_features)),
        A_ub=constraints,
        b_ub=bounds,
        bounds=[(None, None)] * len(monomial_features),
        method="highs",
    )
    print("quotient_support", result.success, result.message)
    if result.success:
        print(result.x)


if __name__ == "__main__":
    main()
