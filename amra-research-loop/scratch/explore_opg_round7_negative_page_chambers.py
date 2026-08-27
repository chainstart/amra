#!/usr/bin/env python3
"""Discovery-only Bernstein scan for the two negative-page orbits.

The exact route chamber ``diag(q0,q3,q4,c)+11^T > 0`` has at most one
negative diagonal quantity.  When a page quantity is the negative one, put

    q_negative = -a,
    a = tau*P/B,

where P is the product of the other three positive route quantities and B
is their diagonal-plus-ones determinant.  The negative page has three
activity charts: N (both activities negative), L, and R.  The other two
pages use the familiar P/L/R charts.  This script clears every positive
denominator and reports exact tensor-Bernstein signs in the bounded chart
variables and tau.

This is scratch discovery code.  Any chamber promoted into campaign
evidence must be reconstructed and asserted by a stdlib verifier.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
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
TAU = 7


def scale(poly, scalar):
    return {monomial: scalar * value for monomial, value in poly.items() if scalar}


def chart(index, state, negative_index):
    """Return left numerator, right numerator, denominator, rational side."""
    first = variable(1 + 2 * index)
    second = variable(2 + 2 * index)
    one = constant(1)
    if index == negative_index:
        assert state in "NLR"
        a, s = first, second
        if state == "N":
            # xL=-a*s, xR=-a*(1-s)/(1-a*s), 0<=s<=1.
            denominator = add(one, multiply(a, s), -1)
            return (
                scale(multiply(a, s), -1),
                scale(multiply(a, add(one, s, -1)), -1),
                denominator,
                "R",
            )
        # If q=-a and precisely one activity is nonnegative, write the
        # negative activity as -[a+(1-a)s] and the positive one as s/(1-s).
        negative = scale(add(a, multiply(add(one, a, -1), s)), -1)
        positive = s
        denominator = add(one, s, -1)
        if state == "L":
            return negative, positive, denominator, "R"
        return positive, negative, denominator, "L"

    assert state in "PLR"
    if state == "P":
        # Both activities themselves are unbounded nonnegative variables.
        return first, second, one, None
    q, s = first, second
    negative = scale(s, -1)
    positive = add(q, s)
    denominator = add(one, s, -1)
    if state == "L":
        return negative, positive, denominator, "R"
    return positive, negative, denominator, "L"


def route_q(index, state, negative_index):
    """Effective q for a positive page; the negative page is omitted."""
    assert index != negative_index
    first = variable(1 + 2 * index)
    second = variable(2 + 2 * index)
    if state == "P":
        return add(add(multiply(first, second), first), second)
    return first


def chart_polynomial(poly, states, negative_index):
    """Clear a square denominator on each rational page side."""
    charts = [chart(index, state, negative_index) for index, state in enumerate(states)]
    result = {}
    for original_monomial, coefficient in poly.items():
        term = constant(coefficient)
        term = multiply(term, power(variable(0), original_monomial[EDGES.index(C_EDGE)]))
        for edges, data in zip(ROUTES, charts):
            left, right, denominator, rational_side = data
            left_degree = original_monomial[EDGES.index(edges[0])]
            right_degree = original_monomial[EDGES.index(edges[1])]
            term = multiply(term, power(left, left_degree))
            term = multiply(term, power(right, right_degree))
            if rational_side is not None:
                rational_degree = left_degree if rational_side == "L" else right_degree
                term = multiply(term, power(denominator, 2 - rational_degree))
        result = add(result, term)
    return result


def schur_substitute_negative_page(poly, states, negative_index):
    """Substitute a=tau*P/B and clear the exact power of B."""
    positive_routes = [variable(0)]
    positive_routes.extend(
        route_q(index, state, negative_index)
        for index, state in enumerate(states)
        if index != negative_index
    )
    assert len(positive_routes) == 3
    P = constant(1)
    for route in positive_routes:
        P = multiply(P, route)
    B = P
    for left in range(3):
        for right in range(left + 1, 3):
            B = add(B, multiply(positive_routes[left], positive_routes[right]))

    a_slot = 1 + 2 * negative_index
    a_degree = max(monomial[a_slot] for monomial in poly)
    tau_P = multiply(variable(TAU), P)
    result = {}
    for monomial, coefficient in poly.items():
        degree = monomial[a_slot]
        reduced = list(monomial)
        reduced[a_slot] = 0
        term = {tuple(reduced): coefficient}
        term = multiply(term, power(tau_P, degree))
        term = multiply(term, power(B, a_degree - degree))
        result = add(result, term)
    return result, a_degree


def sign_row(poly):
    values = tuple(poly.values())
    return {
        "terms": len(poly),
        "positive": sum(value > 0 for value in values),
        "negative": sum(value < 0 for value in values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
    }


def main():
    deletion, connectivity, forest_count, connected_count = reconstruct_original()
    assert (forest_count, connected_count) == (128, 58)
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(
        multiply_original(a_slope, e_zero),
        multiply_original(d_slope, c_zero),
        -1,
    )

    for negative_index, orbit in ((0, "q0"), (1, "q3")):
        positive_indices = tuple(index for index in range(3) if index != negative_index)
        for negative_state in "NLR":
            for positive_states in product("PLR", repeat=2):
                states = [None] * 3
                states[negative_index] = negative_state
                for index, state in zip(positive_indices, positive_states):
                    states[index] = state
                state = "".join(states)
                cleared = chart_polynomial(delta, states, negative_index)
                schur, a_degree = schur_substitute_negative_page(
                    cleared, states, negative_index
                )
                bounded_slots = [2 + 2 * negative_index, TAU]
                bounded_slots.extend(
                    2 + 2 * index
                    for index in positive_indices
                    if states[index] != "P"
                )
                bernstein = bernstein_transform(schur, sorted(bounded_slots))
                print(
                    {
                        "orbit": orbit,
                        "state": state,
                        "a_degree": a_degree,
                        "schur": sign_row(schur),
                        "bernstein": sign_row(bernstein),
                    },
                    flush=True,
                )


if __name__ == "__main__":
    main()
