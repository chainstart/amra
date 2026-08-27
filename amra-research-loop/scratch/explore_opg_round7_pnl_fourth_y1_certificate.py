#!/usr/bin/env python3
"""Compress and test the y=1 boundary of the fourth PNL q-chart."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


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
    z, Hbar, b, d = (variable(slot) for slot in (0, 4, 5, 7))
    one_minus_z = add(constant(1), z, -1)
    z2 = multiply(z, z)
    z3 = multiply(z2, z)
    first_positive = polynomial_sum(multiply(b, one_minus_z), scale(z, 7))
    second_positive = polynomial_sum(
        product(Hbar, b, z2, one_minus_z),
        scale(multiply(Hbar, z3), 7),
        scale(multiply(b, one_minus_z), 2),
        scale(z, 14),
        constant(7),
    )
    square_base = polynomial_sum(
        scale(product(Hbar, b, d, z3), 11),
        scale(product(Hbar, b, d, z2), -11),
        scale(product(Hbar, b, z2), 22),
        scale(product(Hbar, b, z), -34),
        scale(multiply(Hbar, z), -21),
        scale(product(b, d, z), 7),
        scale(b, -22),
        scale(multiply(d, z), -7),
        constant(-77),
    )
    return product(
        constant(121),
        square(polynomial_sum(multiply(d, z), constant(2))),
        first_positive,
        second_positive,
        square(square_base),
    )


def main():
    below = parameterized("below")
    third_v = radial_projective_chart(below, ROOT_SLOTS, 6, 1)
    fourth_q = radial_projective_chart(third_v, ROOT_SLOTS, 0, 1)
    boundary = specialize(fourth_q, 2, 1)
    monomial, one_minus, primitive = factor_boundary(boundary, (0, 4, 5, 6, 7))
    assert monomial == (2, 0, 0, 0, 0, 0, 1, 0)
    assert not one_minus
    compressed = compress_q2v(primitive)
    manifest = manifest_factor()
    residual = divide_polynomial(compressed, manifest)
    assert multiply(manifest, residual) == compressed
    controls = bernstein_transform(residual, [0, 4, 5, 7])
    total = 1
    residual_row = row(residual)
    for slot in (0, 4, 5, 7):
        total *= residual_row["degrees"][slot] + 1
    print(
        "boundary", row(boundary),
        "primitive", row(primitive),
        "compressed", row(compressed),
        "manifest", row(manifest),
        "residual", residual_row,
        "controls_total", total,
        "controls_nonzero", len(controls),
        "controls_negative", sum(value < 0 for value in controls.values()),
        "minimum", min(controls.values()),
        "maximum", max(controls.values()),
        "sha256", digest(controls),
        flush=True,
    )


if __name__ == "__main__":
    main()
