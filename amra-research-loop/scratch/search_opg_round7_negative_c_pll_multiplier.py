#!/usr/bin/env python3
"""Discovery LP for a conditional Bernstein certificate in the PLL chamber.

Seek a tensor-Bernstein-positive Q such that

    G = P + d1*q0^4*s0^2*q3*q4*Q,

with P tensor-Bernstein-positive.  Here G=-disc_tau/4 and d1=F'(1).
Then d1>=0 implies G>=0.  Floating LP output is only a search hint; any
successful support must later be rationalized and checked by stdlib exact
arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


EVIDENCE = Path(__file__).parents[1] / "campaigns/opg-1757-transverse-lift-round7/evidence"
SCRATCH = Path(__file__).parent
sys.path[:0] = [str(EVIDENCE), str(SCRATCH)]

from verify_c_zero_fibre import (  # noqa: E402
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_negative_c_direct_chambers import add, multiply  # noqa: E402
from explore_opg_round7_negative_c_uniform_orientations import (  # noqa: E402
    schur_substitute,
    uniform_state_polynomial,
)


B_EDGE = (0, 4)
Q_SLOTS = (1, 3, 5)
O_SLOTS = (2, 4, 6)


def coefficient(poly, slot, degree):
    result = {}
    for monomial, value in poly.items():
        if monomial[slot] != degree:
            continue
        reduced = list(monomial)
        reduced[slot] = 0
        result[tuple(reduced)] = value
    return result


def divide_monomial(poly, factor):
    return {
        tuple(degree - removed for degree, removed in zip(monomial, factor)): value
        for monomial, value in poly.items()
    }


def bernstein(poly, degrees):
    result = dict(poly)
    for slot, degree in zip(O_SLOTS, degrees):
        transformed = {}
        for monomial, value in result.items():
            power_degree = monomial[slot]
            for index in range(power_degree, degree + 1):
                target = list(monomial)
                target[slot] = index
                target = tuple(target)
                transformed[target] = transformed.get(target, Fraction()) + value * Fraction(
                    comb(index, power_degree), comb(degree, power_degree)
                )
        result = {monomial: value for monomial, value in transformed.items() if value}
    return result


def key(monomial):
    return tuple(monomial[slot] for slot in Q_SLOTS + O_SLOTS)


def main():
    deletion, connectivity, _, _ = reconstruct_original()
    A = derivative(deletion, (B_EDGE,))
    C = restrict_original_zero(deletion, B_EDGE)
    D = derivative(connectivity, (B_EDGE,))
    E = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(multiply_original(A, E), multiply_original(D, C), -1)
    F = schur_substitute(uniform_state_polynomial(delta, tuple("PLL")))
    a0, a1, a2 = (coefficient(F, 7, degree) for degree in range(3))
    d1 = add(a1, {monomial: 2 * value for monomial, value in a2.items()})
    G = add(multiply(a0, a2), multiply(a1, a1), -Fraction(1, 4))

    d1_factor = (0, 4, 0, 1, 0, 1, 0, 0)
    G_factor = (0, 8, 2, 2, 0, 2, 0, 0)
    d1_normalized = divide_monomial(d1, d1_factor)
    G_normalized = divide_monomial(G, G_factor)

    d_degrees = tuple(max(monomial[slot] for monomial in d1_normalized) for slot in O_SLOTS)
    target_degrees = tuple(max(monomial[slot] for monomial in G_normalized) for slot in O_SLOTS)
    q_degrees_d = tuple(max(monomial[slot] for monomial in d1_normalized) for slot in Q_SLOTS)
    q_degrees_G = tuple(max(monomial[slot] for monomial in G_normalized) for slot in Q_SLOTS)
    multiplier_o_degrees = tuple(target - source for target, source in zip(target_degrees, d_degrees))
    multiplier_q_degrees = tuple(target - source for target, source in zip(q_degrees_G, q_degrees_d))
    assert all(degree >= 0 for degree in multiplier_o_degrees + multiplier_q_degrees)

    d_bernstein = {key(monomial): value for monomial, value in bernstein(d1_normalized, d_degrees).items()}
    G_bernstein = {key(monomial): value for monomial, value in bernstein(G_normalized, target_degrees).items()}

    variables = tuple(product(
        *(range(degree + 1) for degree in multiplier_q_degrees),
        *(range(degree + 1) for degree in multiplier_o_degrees),
    ))
    variable_index = {entry: index for index, entry in enumerate(variables)}

    entries = {}
    for d_key, d_value in d_bernstein.items():
        d_q, d_o = d_key[:3], d_key[3:]
        for variable_entry in variables:
            q_shift, o_index = variable_entry[:3], variable_entry[3:]
            target_key = tuple(a + b for a, b in zip(d_q, q_shift)) + tuple(
                a + b for a, b in zip(d_o, o_index)
            )
            product_weight = Fraction(1)
            for n, m, i, j in zip(d_degrees, multiplier_o_degrees, d_o, o_index):
                product_weight *= Fraction(comb(n, i) * comb(m, j), comb(n + m, i + j))
            value = d_value * product_weight
            if value:
                entries.setdefault(target_key, []).append((variable_index[variable_entry], value))

    row_keys = sorted(set(G_bernstein) | set(entries))
    rows = []
    columns = []
    values = []
    rhs = []
    for row, row_key in enumerate(row_keys):
        row_entries = entries.get(row_key, ())
        scale = max(
            [abs(float(G_bernstein.get(row_key, 0)))]
            + [abs(float(value)) for _, value in row_entries]
            + [1e-12]
        )
        rhs.append(float(G_bernstein.get(row_key, 0)) / scale)
        for column, value in row_entries:
            rows.append(row)
            columns.append(column)
            values.append(float(value) / scale)

    matrix = coo_matrix(
        (np.asarray(values), (np.asarray(rows), np.asarray(columns))),
        shape=(len(row_keys), len(variables)),
    ).tocsr()
    print({
        "d_degrees": d_degrees,
        "target_degrees": target_degrees,
        "multiplier_o_degrees": multiplier_o_degrees,
        "multiplier_q_degrees": multiplier_q_degrees,
        "variables": len(variables),
        "constraints": len(row_keys),
        "nonzeros": matrix.nnz,
    }, flush=True)
    result = linprog(
        np.zeros(len(variables)),
        A_ub=matrix,
        b_ub=np.asarray(rhs),
        bounds=(0, None),
        method="highs",
        options={"time_limit": 120.0, "presolve": True},
    )
    print({
        "success": result.success,
        "status": result.status,
        "message": result.message,
    }, flush=True)
    if result.x is not None:
        support = [
            (variables[index], value)
            for index, value in enumerate(result.x)
            if value > 1e-8
        ]
        residual = np.asarray(rhs) - matrix @ result.x
        print({
            "support": len(support),
            "minimum_residual": float(residual.min()),
            "maximum_coefficient": float(result.x.max()),
            "largest": sorted(support, key=lambda item: -item[1])[:40],
        }, flush=True)


if __name__ == "__main__":
    main()
