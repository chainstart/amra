#!/usr/bin/env python3
"""Compress and test the b=1 boundary of the fourth PNL q-chart."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_second_newton_boundaries import (  # noqa: E402
    factor_boundary,
    specialize,
)
from explore_opg_round7_pnl_third_newton_root import ROOT_SLOTS, parameterized  # noqa: E402
from verify_mixed_three_negative import divide_polynomial  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    variable,
)
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_negative_q0_no_positive_gram import scale  # noqa: E402
from verify_pnl_double_corner_blowup import radial_projective_chart, row  # noqa: E402
from verify_rlp_projective_corner_reduction import (  # noqa: E402
    polynomial_sum,
    product,
    square,
)


def sympy_expression(poly):
    q, y, Hbar, b, v, d = sp.symbols("q y Hbar b v d")
    slot_symbols = {0: q, 2: y, 4: Hbar, 5: b, 6: v, 7: d}
    expression = 0
    for monomial, coefficient in poly.items():
        term = sp.Rational(coefficient.numerator, coefficient.denominator)
        for slot, symbol in slot_symbols.items():
            term *= symbol ** monomial[slot]
        expression += term
    return expression, (q, y, Hbar, b, v, d)


def as_sparse_factor(expression, variables):
    result = {}
    for powers, coefficient in sp.Poly(expression, *variables).terms():
        monomial = [0] * 8
        for slot, exponent in zip((0, 4, 7), powers):
            monomial[slot] = exponent
        result[tuple(monomial)] = Fraction(int(coefficient.p), int(coefficient.q))
    return result


def compress_q2v(poly):
    result = {}
    for monomial, coefficient in poly.items():
        assert monomial[0] == 2 * monomial[6]
        compressed = list(monomial)
        compressed[0] = monomial[6]
        compressed[6] = 0
        key = tuple(compressed)
        result[key] = result.get(key, Fraction()) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def manifest_factor():
    z, Hbar, d = (variable(slot) for slot in (0, 4, 7))
    z2 = multiply(z, z)
    z3 = multiply(z2, z)
    positive_cubic = polynomial_sum(
        scale(multiply(Hbar, z3), 6),
        multiply(Hbar, z2),
        scale(z, 12),
        constant(9),
    )
    square_base = polynomial_sum(
        product(Hbar, d, z3),
        scale(product(Hbar, d, z2), -1),
        scale(multiply(Hbar, z2), 2),
        scale(multiply(Hbar, z), -5),
        constant(-9),
    )
    return product(
        constant(1771561),
        add(constant(1), z, -1),
        polynomial_sum(scale(z, 6), constant(1)),
        square(polynomial_sum(multiply(d, z), constant(2))),
        positive_cubic,
        square(square_base),
    )


def main():
    below = parameterized("below")
    third_v = radial_projective_chart(below, ROOT_SLOTS, 6, 1)
    fourth_q = radial_projective_chart(third_v, ROOT_SLOTS, 0, 1)
    boundary = specialize(fourth_q, 5, 1)
    monomial, one_minus, primitive = factor_boundary(boundary, (0, 2, 4, 6, 7))
    assert monomial == (2, 0, 0, 0, 0, 0, 1, 0)
    assert not one_minus
    expression, (q, _, Hbar, _, v, d) = sympy_expression(primitive)
    compressed_sparse = compress_q2v(primitive)
    manifest = manifest_factor()
    exact_residual = divide_polynomial(compressed_sparse, manifest)
    z = sp.symbols("z")
    compressed = 0
    for powers, coefficient in sp.Poly(expression, q, Hbar, v, d).terms():
        q_degree, H_degree, v_degree, d_degree = powers
        assert q_degree == 2 * v_degree
        compressed += coefficient * z**v_degree * Hbar**H_degree * d**d_degree
    coefficient, factors = sp.factor_list(compressed)
    print(
        "boundary", row(boundary), "primitive", row(primitive),
        "factor_coefficient", coefficient,
        "factor_degrees", [(sp.Poly(factor, z, Hbar, d).total_degree(), exponent) for factor, exponent in factors],
        flush=True,
    )
    residual = max((factor for factor, _ in factors), key=lambda item: len(sp.Poly(item, z, Hbar, d).terms()))
    residual_sparse = as_sparse_factor(-residual, (z, Hbar, d))
    assert exact_residual == residual_sparse
    controls = bernstein_transform(residual_sparse, [0, 4, 7])
    print(
        "negative_residual", row(residual_sparse),
        "compressed", row(compressed_sparse),
        "manifest", row(manifest),
        "controls", len(controls),
        "negative", sum(value < 0 for value in controls.values()),
        "zero", sum(value == 0 for value in controls.values()),
        "minimum", min(controls.values()),
        "maximum", max(controls.values()),
        "sha256", digest(controls),
        flush=True,
    )
    print("factorization", sp.factor(compressed), flush=True)


if __name__ == "__main__":
    main()
