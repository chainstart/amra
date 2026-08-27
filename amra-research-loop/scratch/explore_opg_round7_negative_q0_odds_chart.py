#!/usr/bin/env python3
"""Discovery scan for the Möbius/odds chart on a double-negative q0 page."""

from __future__ import annotations

from itertools import product
from fractions import Fraction
from pathlib import Path
import sys


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_c_zero_fibre import EDGES  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_page_direct_chambers import (  # noqa: E402
    C_EDGE,
    ROUTES,
    chart,
    digest,
)
from verify_negative_q0_no_positive_gram import build_delta  # noqa: E402


TAU = 7


def scale(poly, scalar):
    return {monomial: scalar * value for monomial, value in poly.items() if scalar}


def route_q(index, state, uniform_positive=False):
    first = variable(1 + 2 * index)
    second = variable(2 + 2 * index)
    if state == "P" and not uniform_positive:
        return add(add(multiply(first, second), first), second)
    return first


def negative_odds_data(states, uniform_positive=False):
    c = variable(0)
    q3 = route_q(1, states[1], uniform_positive)
    q4 = route_q(2, states[2], uniform_positive)
    P = multiply(multiply(c, q3), q4)
    C = add(add(multiply(c, q3), multiply(c, q4)), multiply(q3, q4))
    tau_P = multiply(variable(TAU), P)
    s0 = variable(2)
    left_numerator = scale(multiply(tau_P, s0), -1)
    left_denominator = add(C, multiply(tau_P, s0))
    right_numerator = scale(
        multiply(tau_P, add(constant(1), s0, -1)),
        -1,
    )
    right_denominator = add(C, tau_P)
    return (left_numerator, left_denominator), (right_numerator, right_denominator), P, C


def negative_nested_odds_data(states, uniform_positive=False):
    """Fill the admissible odds quantity successively on a unit square."""
    c = variable(0)
    q3 = route_q(1, states[1], uniform_positive)
    q4 = route_q(2, states[2], uniform_positive)
    P = multiply(multiply(c, q3), q4)
    C = add(add(multiply(c, q3), multiply(c, q4)), multiply(q3, q4))
    s = variable(2)
    t = variable(TAU)
    sP = multiply(s, P)
    one_minus_s = add(constant(1), s, -1)
    tau_fill = add(s, multiply(t, one_minus_s))
    left_numerator = scale(sP, -1)
    left_denominator = add(C, sP)
    right_numerator = scale(multiply(multiply(t, P), one_minus_s), -1)
    right_denominator = add(C, multiply(P, tau_fill))
    return (left_numerator, left_denominator), (right_numerator, right_denominator), P, C


def uniform_positive_chart(index, state):
    q = variable(1 + 2 * index)
    s = variable(2 + 2 * index)
    if state == "P":
        denominator = add(constant(1), multiply(q, s))
        return (
            multiply(q, s),
            multiply(q, add(constant(1), s, -1)),
            denominator,
            "R",
        )
    negative = scale(s, -1)
    positive = add(q, s)
    denominator = add(constant(1), s, -1)
    return (
        (negative, positive, denominator, "R")
        if state == "L"
        else (positive, negative, denominator, "L")
    )


def cleared_polynomial(
    delta,
    states,
    nested=False,
    denominator_degree=2,
    uniform_positive=False,
):
    data = (
        negative_nested_odds_data(states, uniform_positive)
        if nested
        else negative_odds_data(states, uniform_positive)
    )
    left, right, _, _ = data
    positive_charts = [
        (
            uniform_positive_chart(index, states[index])
            if uniform_positive
            else chart(index, states[index], 0)
        )
        for index in (1, 2)
    ]
    result = {}
    for original_monomial, coefficient in delta.items():
        term = constant(coefficient)
        term = multiply(
            term,
            power(variable(0), original_monomial[EDGES.index(C_EDGE)]),
        )
        for edge, (numerator, denominator) in zip(ROUTES[0], (left, right)):
            degree = original_monomial[EDGES.index(edge)]
            term = multiply(term, power(numerator, degree))
            assert degree <= denominator_degree
            term = multiply(term, power(denominator, denominator_degree - degree))
        for edges, data in zip(ROUTES[1:], positive_charts):
            left_num, right_num, denominator, rational_side = data
            left_degree = original_monomial[EDGES.index(edges[0])]
            right_degree = original_monomial[EDGES.index(edges[1])]
            term = multiply(term, power(left_num, left_degree))
            term = multiply(term, power(right_num, right_degree))
            if rational_side is not None:
                rational_degree = left_degree if rational_side == "L" else right_degree
                assert rational_degree <= denominator_degree
                term = multiply(
                    term,
                    power(denominator, denominator_degree - rational_degree),
                )
        result = add(result, term)
    return result


def row(poly):
    return {
        "terms": len(poly),
        "negative": sum(value < 0 for value in poly.values()),
        "minimum": str(min(poly.values())),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
        "sha256": digest(poly),
    }


def subdivide_bernstein(poly, slot, degree):
    """Split one Bernstein coordinate at 1/2 by exact de Casteljau."""
    grouped = {}
    for monomial, value in poly.items():
        key = monomial[:slot] + monomial[slot + 1 :]
        grouped.setdefault(key, [Fraction()] * (degree + 1))[monomial[slot]] = value
    halves = ({}, {})
    for key, coefficients in grouped.items():
        triangle = [coefficients]
        for _ in range(degree):
            previous = triangle[-1]
            triangle.append([
                (previous[index] + previous[index + 1]) / 2
                for index in range(len(previous) - 1)
            ])
        controls = (
            [triangle[index][0] for index in range(degree + 1)],
            [triangle[degree - index][index] for index in range(degree + 1)],
        )
        for half, values in zip(halves, controls):
            for index, value in enumerate(values):
                if not value:
                    continue
                monomial = key[:slot] + (index,) + key[slot:]
                half[monomial] = value
    return halves


def uniform_boxes(poly, slots, rounds):
    boxes = [poly]
    for _ in range(rounds):
        for slot in slots:
            degree = max(monomial[slot] for monomial in poly)
            boxes = [
                half
                for box in boxes
                for half in subdivide_bernstein(box, slot, degree)
            ]
    return boxes


def main():
    delta, _, _ = build_delta()
    for positive_states in product("PLR", repeat=2):
        state = "N" + "".join(positive_states)
        poly = cleared_polynomial(delta, state)
        bounded = [2, TAU]
        bounded.extend(
            2 + 2 * index
            for index in (1, 2)
            if state[index] != "P"
        )
        transformed = bernstein_transform(poly, bounded)
        print(state, row(poly), row(transformed), flush=True)
        if state in ("NPP", "NPL", "NPR"):
            for rounds in range(1, 4):
                boxes = uniform_boxes(transformed, bounded, rounds)
                failed = [
                    box for box in boxes
                    if any(value < 0 for value in box.values())
                ]
                print(
                    "  dyadic",
                    rounds,
                    "boxes",
                    len(boxes),
                    "failed",
                    len(failed),
                    "worst",
                    min(value for box in boxes for value in box.values()),
                    flush=True,
                )
                if not failed:
                    break
        if state in ("NPP", "NPL", "NPR", "NLP", "NRP"):
            nested = cleared_polynomial(delta, state, nested=True)
            nested_transformed = bernstein_transform(nested, bounded)
            print(
                "  nested",
                row(nested),
                row(nested_transformed),
                flush=True,
            )


if __name__ == "__main__":
    main()
