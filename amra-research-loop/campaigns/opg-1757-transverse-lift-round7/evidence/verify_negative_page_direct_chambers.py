#!/usr/bin/env python3
"""Exact direct certificates for thirty negative-page activity chambers."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json

from verify_c_zero_fibre import (
    EDGES,
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_negative_c_direct_chambers import (
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
    scalar = Fraction(scalar)
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in poly.items()
        if scalar * coefficient
    }


def digest(poly):
    canonical = json.dumps(
        [
            [list(monomial), coefficient.numerator, coefficient.denominator]
            for monomial, coefficient in sorted(poly.items())
        ],
        separators=(",", ":"),
    )
    return sha256(canonical.encode()).hexdigest()


def chart(index, state, negative_index):
    """Return left numerator, right numerator, denominator, rational side."""
    first = variable(1 + 2 * index)
    second = variable(2 + 2 * index)
    one = constant(1)
    if index == negative_index:
        assert state in "NLR"
        a, s = first, second
        if state == "N":
            denominator = add(one, multiply(a, s), -1)
            data = (
                scale(multiply(a, s), -1),
                scale(multiply(a, add(one, s, -1)), -1),
                denominator,
                "R",
            )
        else:
            negative = scale(add(a, multiply(add(one, a, -1), s)), -1)
            positive = s
            denominator = add(one, s, -1)
            data = (
                (negative, positive, denominator, "R")
                if state == "L"
                else (positive, negative, denominator, "L")
            )
        expected_q = scale(a, -1)
    else:
        assert state in "PLR"
        if state == "P":
            data = (first, second, one, None)
            expected_q = add(add(multiply(first, second), first), second)
        else:
            q, s = first, second
            negative = scale(s, -1)
            positive = add(q, s)
            denominator = add(one, s, -1)
            data = (
                (negative, positive, denominator, "R")
                if state == "L"
                else (positive, negative, denominator, "L")
            )
            expected_q = q

    left, right, denominator, rational_side = data
    if rational_side == "R":
        q_numerator = add(
            add(multiply(left, right), multiply(left, denominator)),
            right,
        )
        assert q_numerator == multiply(expected_q, denominator)
    elif rational_side == "L":
        q_numerator = add(
            add(multiply(left, right), left),
            multiply(right, denominator),
        )
        assert q_numerator == multiply(expected_q, denominator)
    else:
        assert add(add(multiply(left, right), left), right) == expected_q
    return data


def route_q(index, state, negative_index):
    assert index != negative_index
    first = variable(1 + 2 * index)
    second = variable(2 + 2 * index)
    if state == "P":
        return add(add(multiply(first, second), first), second)
    return first


def chart_polynomial(poly, states, negative_index):
    """Substitute every page chart and clear its positive square denominator."""
    charts = [
        chart(index, state, negative_index)
        for index, state in enumerate(states)
    ]
    result = {}
    for original_monomial, coefficient in poly.items():
        term = constant(coefficient)
        term = multiply(
            term,
            power(variable(0), original_monomial[EDGES.index(C_EDGE)]),
        )
        for edges, data in zip(ROUTES, charts):
            left, right, denominator, rational_side = data
            left_degree = original_monomial[EDGES.index(edges[0])]
            right_degree = original_monomial[EDGES.index(edges[1])]
            term = multiply(term, power(left, left_degree))
            term = multiply(term, power(right, right_degree))
            if rational_side is not None:
                rational_degree = (
                    left_degree if rational_side == "L" else right_degree
                )
                assert rational_degree <= 2
                term = multiply(term, power(denominator, 2 - rational_degree))
        result = add(result, term)
    return result


def positive_route_data(states, negative_index):
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
    return positive_routes, P, B


def schur_substitute(poly, states, negative_index):
    """Substitute a=tau*P/B and clear the exact power of positive B."""
    _, P, B = positive_route_data(states, negative_index)
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


def verify_schur_identity(states, negative_index):
    """Check det(diag(q)+11^T)=P-a*B and its tau substitution."""
    positive_routes, P, B = positive_route_data(states, negative_index)
    a = variable(1 + 2 * negative_index)
    route_values = []
    positive_iterator = iter(positive_routes[1:])
    for index in range(3):
        route_values.append(scale(a, -1) if index == negative_index else next(positive_iterator))
    route_values.append(positive_routes[0])
    determinant = constant(0)
    for omitted in range(4):
        triple = constant(1)
        for index, route in enumerate(route_values):
            if index != omitted:
                triple = multiply(triple, route)
        determinant = add(determinant, triple)
    product_all = constant(1)
    for route in route_values:
        product_all = multiply(product_all, route)
    determinant = add(determinant, product_all)
    assert determinant == add(P, multiply(a, B), -1)
    cleared, degree = schur_substitute(determinant, states, negative_index)
    assert degree == 1
    expected = multiply(
        multiply(P, B),
        add(constant(1), variable(TAU), -1),
    )
    assert cleared == expected


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
    assert len(delta) == 178

    certified = {
        "q0": ("NLL", "NLR", "NRL", "NRR", "LPL", "LLP", "LLL", "RPR", "RRP", "RRR"),
        "q3": ("LNP", "LNR", "RNP", "RNL", "PLL", "LLP", "LLR", "PRR", "RRP", "RRL"),
        "q4": ("LPN", "LRN", "RPN", "RLN", "PLL", "LPL", "LRL", "PRR", "RPR", "RLR"),
    }
    route_index = {"q0": 0, "q3": 1, "q4": 2}
    records = {}
    for route_name, states_for_route in certified.items():
        negative_index = route_index[route_name]
        route_records = {}
        for state in sorted(states_for_route):
            states = tuple(state)
            assert states[negative_index] in "NLR"
            assert all(
                states[index] in "PLR"
                for index in range(3)
                if index != negative_index
            )
            verify_schur_identity(states, negative_index)
            cleared = chart_polynomial(delta, states, negative_index)
            schur, a_degree = schur_substitute(cleared, states, negative_index)
            bounded_slots = [2 + 2 * negative_index, TAU]
            bounded_slots.extend(
                2 + 2 * index
                for index in range(3)
                if index != negative_index and states[index] != "P"
            )
            bernstein = bernstein_transform(schur, sorted(bounded_slots))
            assert bernstein
            assert all(coefficient > 0 for coefficient in bernstein.values())
            route_records[state] = {
                "a_degree": a_degree,
                "schur_terms": len(schur),
                "bernstein_nonzero": len(bernstein),
                "minimum_bernstein_coefficient": str(min(bernstein.values())),
                "schur_sha256": digest(schur),
            }
        assert len(route_records) == 10
        records[route_name] = route_records

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-page-direct-chambers.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "domain": "positive edge floors, K=diag(q0,q3,q4,c)+11^T positive definite, and exactly one page quantity negative",
        "schur_parameterization": {
            "positive_routes": "the direct route c and the two positive page quantities",
            "P": "product of the three positive route quantities",
            "B": "P plus their three pairwise products",
            "negative_page_quantity": "-a=-tau*P/B",
            "tau": "0<tau<1",
            "det_K": "P*(1-tau)",
        },
        "negative_page_charts": {
            "N": "xL=-a*s, xR=-a*(1-s)/(1-a*s), 0<=s<=1",
            "L": "xL=-(a+(1-a)*s), xR=s/(1-s), 0<=s<1",
            "R": "xR=-(a+(1-a)*s), xL=s/(1-s), 0<=s<1",
        },
        "positive_page_charts": {
            "P": "xL,xR>=0",
            "L": "xL=-s, xR=(q+s)/(1-s), 0<=s<1",
            "R": "xR=-s, xL=(q+s)/(1-s), 0<=s<1",
        },
        "certificate": "after clearing positive page denominators and the exact power of B, every nonzero tensor Bernstein coefficient in tau and all bounded page parameters is strictly positive, with ordinary monomials in all unbounded nonnegative variables",
        "certified_chambers": {
            route: sorted(states) for route, states in certified.items()
        },
        "certified_per_negative_route": 10,
        "certified_total": sum(len(states) for states in certified.values()),
        "total_negative_page_activity_chambers": 81,
        "records": records,
        "conclusion": "Delta_b>=0 in the thirty listed negative-page activity chambers",
        "scope": "direct certificates for 30 of 81 negative-page activity chambers; all three negative-page route cases retain unresolved orientations, so the generic sign and OPG-1757 remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
