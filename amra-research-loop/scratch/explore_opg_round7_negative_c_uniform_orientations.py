#!/usr/bin/env python3
"""Discovery scan for c<0 using q plus one bounded coordinate per page."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from pathlib import Path
import sys


EVIDENCE = Path(__file__).parents[1] / "campaigns/opg-1757-transverse-lift-round7/evidence"
sys.path.insert(0, str(EVIDENCE))

from verify_c_zero_fibre import (  # noqa: E402
    EDGES,
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)


B_EDGE = (0, 4)
C_EDGE = (1, 2)
ROUTES = (((0, 1), (0, 2)), ((1, 3), (2, 3)), ((1, 4), (2, 4)))


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {monomial: scalar * value for monomial, value in poly.items() if value}


def uniform_state_polynomial(delta, states):
    """Clear one square denominator for each q-orientation page."""
    c = variable(0)
    page_factors = []
    for index, state in enumerate(states):
        q = variable(1 + 2 * index)
        orientation = variable(2 + 2 * index)
        if state == "P":
            denominator = add(constant(1), multiply(q, orientation))
            left = multiply(q, orientation)
            right = multiply(q, add(constant(1), orientation, -1))
            page_factors.append((left, right, denominator, "R"))
        else:
            denominator = add(constant(1), orientation, -1)
            negative = scale(orientation, -1)
            positive = add(q, orientation)
            if state == "L":
                page_factors.append((negative, positive, denominator, "R"))
            else:
                page_factors.append((positive, negative, denominator, "L"))

    result = {}
    for original_monomial, original_coefficient in delta.items():
        term = constant(original_coefficient)
        c_degree = original_monomial[EDGES.index(C_EDGE)]
        term = multiply(term, power(c, c_degree))
        for edges, factors in zip(ROUTES, page_factors):
            left_degree = original_monomial[EDGES.index(edges[0])]
            right_degree = original_monomial[EDGES.index(edges[1])]
            left, right, denominator, rational_side = factors
            term = multiply(term, power(left, left_degree))
            term = multiply(term, power(right, right_degree))
            rational_degree = left_degree if rational_side == "L" else right_degree
            term = multiply(term, power(denominator, 2 - rational_degree))
        result = add(result, term)
    return result


def schur_substitute(poly):
    q0, q3, q4 = (variable(slot) for slot in (1, 3, 5))
    P = multiply(multiply(q0, q3), q4)
    B = add(P, add(add(multiply(q0, q3), multiply(q0, q4)), multiply(q3, q4)))
    tau_P = multiply(variable(7), P)
    result = {}
    for monomial, coefficient in poly.items():
        c_degree = monomial[0]
        assert c_degree <= 2
        base = list(monomial)
        base[0] = 0
        term = {tuple(base): coefficient * (-1 if c_degree % 2 else 1)}
        term = multiply(term, power(tau_P, c_degree))
        term = multiply(term, power(B, 2 - c_degree))
        result = add(result, term)
    return result


def coefficient(poly, slot, degree):
    result = {}
    for monomial, value in poly.items():
        if monomial[slot] != degree:
            continue
        reduced = list(monomial)
        reduced[slot] = 0
        result[tuple(reduced)] = value
    return result


def row(poly):
    values = tuple(poly.values())
    return {
        "terms": len(poly),
        "negative": sum(value < 0 for value in values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
    }


def main():
    deletion, connectivity, _, _ = reconstruct_original()
    A = derivative(deletion, (B_EDGE,))
    C = restrict_original_zero(deletion, B_EDGE)
    D = derivative(connectivity, (B_EDGE,))
    E = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(multiply_original(A, E), multiply_original(D, C), -1)

    for states in product("PLR", repeat=3):
        state = "".join(states)
        cleared = uniform_state_polynomial(delta, states)
        schur = schur_substitute(cleared)
        transformed = bernstein_transform(schur, [2, 4, 6, 7])
        a0, a1, a2 = (coefficient(schur, 7, degree) for degree in range(3))
        endpoint = add(add(a0, a1), a2)
        endpoint = bernstein_transform(endpoint, [2, 4, 6])
        print({
            "state": state,
            "cleared_terms": len(cleared),
            "schur_terms": len(schur),
            "full_bernstein": row(transformed),
            "tau_one_endpoint": row(endpoint),
        }, flush=True)


if __name__ == "__main__":
    main()
