#!/usr/bin/env python3
"""Exact discovery diagnostics for the final RLR outer-Gram core."""

from __future__ import annotations

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

from verify_mixed_three_negative import divide_polynomial  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_nonshared_same_side_gram import (  # noqa: E402
    manifest_factor,
    positive_route_data,
)
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    build_delta,
    coefficient,
    common_monomial,
    divide_monomial,
    gram,
    scale,
)
from explore_opg_round7_negative_q3_single_uniform import (  # noqa: E402
    cleared_polynomial,
)


def row(poly):
    return {
        "terms": len(poly),
        "negative": sum(value < 0 for value in poly.values()),
        "minimum": str(min(poly.values())),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
        "sha256": digest(poly),
    }


def build_m88():
    delta, _, _ = build_delta()
    cleared = cleared_polynomial(delta, "RLR")
    factor = manifest_factor(1)
    core = divide_polynomial(cleared, factor)
    assert cleared == multiply(factor, core)
    assert len(core) == 766

    _, _, _, determinant = gram(core, 4)
    common = common_monomial(determinant)
    assert common == (1, 0, 2, 0, 0, 1, 0, 0)
    residual = divide_monomial(determinant, common)

    q0, s0 = variable(1), variable(2)
    _, _, B = positive_route_data(1)
    positive_factor = multiply(power(add(q0, s0), 2), B)
    h1971 = divide_polynomial(residual, positive_factor)
    assert residual == multiply(positive_factor, h1971)
    assert len(h1971) == 1971

    tau_bernstein = bernstein_transform(h1971, [7])
    beta1 = coefficient(tau_bernstein, 7, 1)
    c = variable(0)
    m88 = scale(divide_polynomial(divide_polynomial(beta1, c), power(B, 2)), 3)
    assert beta1 == scale(multiply(multiply(c, power(B, 2)), m88), Fraction(1, 3))
    assert len(m88) == 88
    m0 = coefficient(m88, 0, 0)
    m1 = coefficient(m88, 0, 1)
    assert m88 == add(m0, multiply(c, m1))
    return core, h1971, m88, m0, m1


def sympy_poly(poly):
    import sympy as sp

    names = "c q0 s0 q3 s3 q4 s4 tau".split()
    symbols = sp.symbols(" ".join(names))
    expression = sum(
        sp.Rational(value.numerator, value.denominator)
        * sp.prod(symbol**degree for symbol, degree in zip(symbols, monomial))
        for monomial, value in poly.items()
    )
    return symbols, sp.Poly(expression, *symbols)


def substitute_slot(poly, slot, replacement):
    result = {}
    for monomial, value in poly.items():
        term = constant(value)
        for index, degree in enumerate(monomial):
            term = multiply(
                term,
                power(replacement if index == slot else variable(index), degree),
            )
        result = add(result, term)
    return result


def local_bernstein(poly, x_bounds, y_bounds):
    x0, x1 = map(Fraction, x_bounds)
    y0, y1 = map(Fraction, y_bounds)
    localized = substitute_slot(
        poly,
        2,
        add(constant(x0), scale(variable(2), x1 - x0)),
    )
    localized = substitute_slot(
        localized,
        6,
        add(constant(y0), scale(variable(6), y1 - y0)),
    )
    return bernstein_transform(localized, [2, 6])


def subdivision_scan(poly, max_depth=6):
    pending = [(Fraction(0), Fraction(1), Fraction(0), Fraction(1), 0)]
    closed = []
    unresolved = []
    while pending:
        x0, x1, y0, y1, depth = pending.pop()
        beta = local_bernstein(poly, (x0, x1), (y0, y1))
        if all(value >= 0 for value in beta.values()):
            closed.append((x0, x1, y0, y1, depth, min(beta.values())))
            continue
        if depth == max_depth:
            unresolved.append((x0, x1, y0, y1, depth, min(beta.values())))
            continue
        xm = (x0 + x1) / 2
        ym = (y0 + y1) / 2
        pending.extend([
            (x0, xm, y0, ym, depth + 1),
            (xm, x1, y0, ym, depth + 1),
            (x0, xm, ym, y1, depth + 1),
            (xm, x1, ym, y1, depth + 1),
        ])
    return closed, unresolved


def main():
    _, h1971, m88, m0, m1 = build_m88()
    for name, poly in (
        ("H1971", h1971),
        ("M88", m88),
        ("M0", m0),
        ("M1", m1),
    ):
        print(name, row(poly))
    symbols, _ = sympy_poly(m88)
    for name, poly in (("M0", m0), ("M1", m1)):
        _, converted = sympy_poly(poly)
        expression = converted.as_expr()
        print(f"{name}_factor", __import__("sympy").factor(expression))
        print(f"{name}_s0_coefficients")
        for degree in range(5):
            value = __import__("sympy").expand(expression).coeff(symbols[2], degree)
            print(degree, __import__("sympy").factor(value))
    closed, unresolved = subdivision_scan(m0, 7)
    print("M0_subdivision", len(closed), len(unresolved))
    for row_ in unresolved[:20]:
        print("open", row_)


if __name__ == "__main__":
    main()
