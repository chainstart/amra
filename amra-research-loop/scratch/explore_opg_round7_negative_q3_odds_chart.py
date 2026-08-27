#!/usr/bin/env python3
"""Discovery scan for nested odds on the q3-negative page."""

from __future__ import annotations

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
from verify_negative_page_direct_chambers import C_EDGE, ROUTES, digest  # noqa: E402
from verify_negative_q0_double_negative_gram import scale  # noqa: E402
from verify_negative_q0_no_positive_gram import build_delta  # noqa: E402


T = 7
NEGATIVE_INDEX = 1


def positive_routes():
    c, q0, q4 = (variable(slot) for slot in (0, 1, 5))
    P = multiply(multiply(c, q0), q4)
    C = add(add(multiply(c, q0), multiply(c, q4)), multiply(q0, q4))
    return P, C


def positive_page_chart(index, state):
    assert index in (0, 2) and state in "PLR"
    q = variable(1 + 2 * index)
    s = variable(2 + 2 * index)
    if state == "P":
        return (
            multiply(q, s),
            multiply(q, add(constant(1), s, -1)),
            add(constant(1), multiply(q, s)),
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


def negative_page_chart():
    P, C = positive_routes()
    s, t = variable(4), variable(T)
    one_minus_s = add(constant(1), s, -1)
    fill = add(s, multiply(t, one_minus_s))
    return (
        (scale(multiply(P, s), -1), add(C, multiply(P, s))),
        (
            scale(multiply(multiply(P, t), one_minus_s), -1),
            add(C, multiply(P, fill)),
        ),
    )


def cleared_polynomial(delta, state):
    assert len(state) == 3 and state[NEGATIVE_INDEX] == "N"
    negative = negative_page_chart()
    pages = {
        index: positive_page_chart(index, state[index])
        for index in (0, 2)
    }
    result = {}
    for original_monomial, value in delta.items():
        term = constant(value)
        term = multiply(
            term,
            power(variable(0), original_monomial[EDGES.index(C_EDGE)]),
        )
        for index, edges in enumerate(ROUTES):
            if index == NEGATIVE_INDEX:
                for edge, (numerator, denominator) in zip(edges, negative):
                    degree = original_monomial[EDGES.index(edge)]
                    term = multiply(term, power(numerator, degree))
                    term = multiply(term, power(denominator, 2 - degree))
                continue
            left, right, denominator, rational_side = pages[index]
            left_degree = original_monomial[EDGES.index(edges[0])]
            right_degree = original_monomial[EDGES.index(edges[1])]
            term = multiply(term, power(left, left_degree))
            term = multiply(term, power(right, right_degree))
            rational_degree = left_degree if rational_side == "L" else right_degree
            term = multiply(term, power(denominator, 2 - rational_degree))
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


def main():
    delta, _, _ = build_delta()
    for state in ("PNP", "PNL", "PNR", "LNL", "RNR"):
        poly = cleared_polynomial(delta, state)
        transformed = bernstein_transform(poly, [2, 4, 6, T])
        print(state, row(poly), row(transformed), flush=True)


if __name__ == "__main__":
    main()
