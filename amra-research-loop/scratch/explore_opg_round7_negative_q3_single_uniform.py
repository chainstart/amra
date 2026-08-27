#!/usr/bin/env python3
"""Discovery scan for q3-negative L/R pages in uniform positive charts."""

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
from explore_opg_round7_negative_q3_odds_chart import (  # noqa: E402
    positive_page_chart,
    positive_routes,
)


T = 7
NEGATIVE_INDEX = 1


def negative_page_chart(state):
    assert state in "LR"
    P, C = positive_routes()
    B = add(P, C)
    s, t = variable(4), variable(T)
    tP = multiply(t, P)
    negative_numerator = scale(
        add(tP, multiply(add(B, tP, -1), s)),
        -1,
    )
    positive_numerator = s
    one_minus_s = add(constant(1), s, -1)
    return (
        (
            (negative_numerator, B),
            (positive_numerator, one_minus_s),
        )
        if state == "L"
        else (
            (positive_numerator, one_minus_s),
            (negative_numerator, B),
        )
    )


def cleared_polynomial(delta, state):
    assert len(state) == 3 and state[NEGATIVE_INDEX] in "LR"
    negative = negative_page_chart(state[NEGATIVE_INDEX])
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
    states = (
        "PLP", "PLR", "LLL", "RLP", "RLL", "RLR",
        "PRP", "PRL", "LRP", "LRL", "LRR", "RRR",
    )
    for state in states:
        poly = cleared_polynomial(delta, state)
        transformed = bernstein_transform(poly, [2, 4, 6, T])
        print(state, row(poly), row(transformed), flush=True)


if __name__ == "__main__":
    main()
