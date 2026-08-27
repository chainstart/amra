#!/usr/bin/env python3
"""Discovery-only coupled Gram scan for the three connection polynomials."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_b_rayleigh_reduction import reconstruct_terminal_states  # noqa: E402
from verify_connection_gram import (  # noqa: E402
    B_EDGE,
    EDGES,
    NAMES,
    add,
    connection_certificate,
    constant,
    multiply,
    power,
    route_a,
    scale,
    variable,
)


def substitute_cleared(poly, denominator_powers):
    q = {name: variable(f"q{name}") for name in ("0", "3", "4")}
    c = variable("c")
    left = {name: variable(f"l{name}") for name in ("0", "3", "4")}
    den = {name: add(constant(1), left[name]) for name in ("0", "3", "4")}
    right_num = {name: add(q[name], left[name], -1) for name in ("0", "3", "4")}
    edge_page = {
        (0, 1): ("0", "left"),
        (0, 2): ("0", "right"),
        (1, 3): ("3", "left"),
        (2, 3): ("3", "right"),
        (1, 4): ("4", "left"),
        (2, 4): ("4", "right"),
    }
    result = {}
    for monomial, coefficient_value in poly.items():
        assert monomial[EDGES.index(B_EDGE)] == 0
        term = constant(coefficient_value)
        term = multiply(term, power(c, monomial[EDGES.index((1, 2))]))
        for edge, (page, side) in edge_page.items():
            degree = monomial[EDGES.index(edge)]
            factor = left[page] if side == "left" else right_num[page]
            term = multiply(term, power(factor, degree))
        for page, denominator_power in denominator_powers.items():
            right_degree = monomial[EDGES.index({
                "0": (0, 2), "3": (2, 3), "4": (2, 4)
            }[page])]
            term = multiply(term, power(den[page], denominator_power - right_degree))
        result = add(result, term)
    return result


def to_sympy(poly):
    symbols = sp.symbols(" ".join(NAMES))
    expression = sum(
        sp.Integer(value)
        * sp.prod(symbol ** exponent for symbol, exponent in zip(symbols, monomial))
        for monomial, value in poly.items()
    )
    return symbols, sp.expand(expression)


def main():
    states, _ = reconstruct_terminal_states({B_EDGE})
    q = {name: variable(f"q{name}") for name in ("0", "3", "4")}
    q["c"] = variable("c")
    left = {name: variable(f"l{name}") for name in ("0", "3", "4")}
    A = route_a(q)
    p03 = connection_certificate("0", "3", "4", q, left, A)["cleared"]
    p04 = connection_certificate("0", "4", "3", q, left, A)["cleared"]
    p34 = connection_certificate("3", "4", "0", q, left, A)["cleared"]
    u = substitute_cleared(states["u"], {"0": 1, "3": 1, "4": 1})
    den0 = add(constant(1), left["0"])
    negative_channel = add(
        scale(multiply(den0, u), 2),
        multiply(power(den0, 2), p34),
        -1,
    )
    delta_cleared = add(
        multiply(p03, p04),
        multiply(A, negative_channel),
        -1,
    )
    symbols, negative_expression = to_sympy(negative_channel)
    _, delta_expression = to_sympy(delta_cleared)
    print({
        "p03_terms": len(p03),
        "p04_terms": len(p04),
        "p34_terms": len(p34),
        "u_terms": len(u),
        "negative_channel_terms": len(negative_channel),
        "delta_cleared_terms": len(delta_cleared),
    }, flush=True)
    print("negative_channel_factor", sp.factor(negative_expression), flush=True)
    l0, l3, l4 = (symbols[NAMES.index(name)] for name in ("l0", "l3", "l4"))
    reduced_negative = sp.cancel(negative_expression / (1 + l0))
    grouped = sp.Poly(reduced_negative, l0, l3, l4)
    print("negative_channel_grouped", [
        (monomial, sp.factor(coefficient_value))
        for monomial, coefficient_value in grouped.terms()
    ], flush=True)


if __name__ == "__main__":
    main()
