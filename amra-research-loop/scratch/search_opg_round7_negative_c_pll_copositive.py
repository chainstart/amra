#!/usr/bin/env python3
"""Discovery LP for a conditional copositive certificate in the PLL chamber.

For the tau-Bernstein matrix entries (b0,b1,b2), seek a nonnegative Q with

    b0*b2-b1^2 + b1*R = P,

where P and R are tensor-Bernstein-positive.  On b1<=0 this would imply the
Gram determinant is nonnegative; on b1>=0 the tau quadratic is trivially
copositive.  Floating LP output is only a search hint.
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


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_c_zero_fibre import (  # noqa: E402
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_negative_c_all_negative_gram import coefficient, scale  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    multiply,
    schur_substitute,
    variable,
)
from verify_nonnegative_route_chambers import state_polynomial  # noqa: E402


B_EDGE = (0, 4)
Q_SLOTS = (1, 2, 3, 5)
O_SLOTS = (4, 6)


def divide_monomial(poly, factor):
    result = {}
    for monomial, value in poly.items():
        reduced = tuple(degree - removed for degree, removed in zip(monomial, factor))
        assert all(degree >= 0 for degree in reduced)
        result[reduced] = value
    return result


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
    F = schur_substitute(state_polynomial(delta, tuple("PLL")), tuple("PLL"))
    a0, a1, a2 = (coefficient(F, 7, degree) for degree in range(3))
    b0 = a0
    b1 = add(a0, scale(a1, Fraction(1, 2)))
    b2 = add(add(a0, a1), a2)
    G = add(multiply(b0, b2), multiply(b1, b1), -1)

    b1_factor = (0, 1, 1, 1, 0, 1, 0, 0)
    G_factor = tuple(2 * degree for degree in b1_factor)
    b1_normalized = divide_monomial(b1, b1_factor)
    G_normalized = divide_monomial(G, G_factor)
    positive_weight = {}
    for slot in Q_SLOTS:
        positive_weight = add(positive_weight, variable(slot))
    G_normalized = multiply(G_normalized, positive_weight)

    b_degrees = tuple(max(monomial[slot] for monomial in b1_normalized) for slot in O_SLOTS)
    target_degrees = tuple(max(monomial[slot] for monomial in G_normalized) for slot in O_SLOTS)
    q_degrees_b = tuple(max(monomial[slot] for monomial in b1_normalized) for slot in Q_SLOTS)
    q_degrees_G = tuple(max(monomial[slot] for monomial in G_normalized) for slot in Q_SLOTS)
    multiplier_o_degrees = tuple(target - source for target, source in zip(target_degrees, b_degrees))
    multiplier_q_degrees = tuple(target - source for target, source in zip(q_degrees_G, q_degrees_b))
    assert all(degree >= 0 for degree in multiplier_o_degrees + multiplier_q_degrees)

    b_bernstein = {
        key(monomial): value
        for monomial, value in bernstein(b1_normalized, b_degrees).items()
    }
    G_bernstein = {
        key(monomial): value
        for monomial, value in bernstein(G_normalized, target_degrees).items()
    }
    variables = tuple(product(
        *(range(degree + 1) for degree in multiplier_q_degrees),
        *(range(degree + 1) for degree in multiplier_o_degrees),
    ))
    variable_index = {entry: index for index, entry in enumerate(variables)}

    entries = {}
    for b_key, b_value in b_bernstein.items():
        b_q, b_o = b_key[: len(Q_SLOTS)], b_key[len(Q_SLOTS) :]
        for variable_entry in variables:
            q_shift = variable_entry[: len(Q_SLOTS)]
            o_index = variable_entry[len(Q_SLOTS) :]
            target_key = tuple(a + b for a, b in zip(b_q, q_shift)) + tuple(
                a + b for a, b in zip(b_o, o_index)
            )
            product_weight = Fraction(1)
            for n, m, i, j in zip(b_degrees, multiplier_o_degrees, b_o, o_index):
                product_weight *= Fraction(comb(n, i) * comb(m, j), comb(n + m, i + j))
            value = b_value * product_weight
            if value:
                entries.setdefault(target_key, []).append((variable_index[variable_entry], value))

    row_keys = sorted(set(G_bernstein) | set(entries))
    rows = []
    columns = []
    values = []
    rhs = []
    for row, row_key in enumerate(row_keys):
        row_entries = entries.get(row_key, ())
        row_scale = max(
            [abs(float(G_bernstein.get(row_key, 0)))]
            + [abs(float(value)) for _, value in row_entries]
            + [1e-12]
        )
        rhs.append(float(G_bernstein.get(row_key, 0)) / row_scale)
        for column, value in row_entries:
            rows.append(row)
            columns.append(column)
            values.append(-float(value) / row_scale)

    matrix = coo_matrix(
        (np.asarray(values), (np.asarray(rows), np.asarray(columns))),
        shape=(len(row_keys), len(variables)),
    ).tocsr()
    print({
        "b_degrees": b_degrees,
        "target_degrees": target_degrees,
        "multiplier_o_degrees": multiplier_o_degrees,
        "multiplier_q_degrees": multiplier_q_degrees,
        "variables": len(variables),
        "constraints": len(row_keys),
        "nonzeros": matrix.nnz,
        "positive_weight": "x01+x02+q3+q4",
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
            "largest": sorted(support, key=lambda item: -item[1])[:80],
        }, flush=True)


if __name__ == "__main__":
    main()
