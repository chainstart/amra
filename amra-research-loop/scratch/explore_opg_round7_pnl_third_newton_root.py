#!/usr/bin/env python3
"""Exact rational parameterization of the above/A boundary moving root."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_a_root_accumulation import (  # noqa: E402
    LOCAL_SLOTS,
    centered_chart,
    face_record,
)
from explore_opg_round7_pnl_second_newton_boundaries import (  # noqa: E402
    factor_boundary,
    specialize,
)
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    constant,
    multiply,
    variable,
)
from verify_negative_q0_no_positive_gram import scale  # noqa: E402
from verify_pnl_double_corner_blowup import (  # noqa: E402
    radial_projective_chart,
    row,
    substitute_slot,
)
from verify_rlp_projective_corner_reduction import (  # noqa: E402
    polynomial_sum,
    reverse_slot,
)


TRANSVERSE_SLOTS = (0, 4, 6, 7)
ROOT_SLOTS = (0, 6)


def R_max_polynomial():
    centered = centered_chart("above")
    order, _ = face_record(centered)
    second_A = radial_projective_chart(centered, LOCAL_SLOTS, 1, order)
    boundary = specialize(second_A, 1, 1)
    remaining = tuple(slot for slot in LOCAL_SLOTS if slot != 1)
    _, _, primitive = factor_boundary(boundary, remaining)
    local = reverse_slot(primitive, 0)
    local = reverse_slot(local, 6)
    transverse_order = min(
        sum(m[slot] for slot in TRANSVERSE_SLOTS) for m in local
    )
    assert transverse_order == 2
    return radial_projective_chart(local, TRANSVERSE_SLOTS, 0, transverse_order)


def parameterized(side):
    poly = R_max_polynomial()
    b, y, u = (variable(slot) for slot in (5, 2, 6))
    one = constant(1)
    one_minus_b = add(one, b, -1)
    one_minus_y = add(one, y, -1)

    # B=b/7 and zeta=7*(1-b)*y/(7+4*b) parameterize
    # K=1-7*B-(4*B+1)*zeta=(1-b)*(1-y)>=0.
    poly, B_degree = substitute_slot(poly, 5, b, constant(7))
    assert B_degree == 5
    poly, zeta_degree = substitute_slot(
        poly,
        2,
        scale(multiply(one_minus_b, y), 7),
        polynomial_sum(constant(7), scale(b, 4)),
    )
    assert zeta_degree == 4
    K = multiply(one_minus_b, one_minus_y)
    if side == "below":
        numerator = multiply(K, u)
    else:
        numerator = polynomial_sum(K, multiply(add(constant(11), K, -1), u))
    poly, C_degree = substitute_slot(poly, 6, numerator, constant(11))
    assert C_degree == 2
    if side == "below":
        poly = reverse_slot(poly, 6)
    return poly


def main():
    symbols = sp.symbols("R y H b v d")
    symbol_slots = tuple(zip(symbols, (0, 2, 4, 5, 6, 7)))
    for side in ("below", "above"):
        poly = parameterized(side)
        order = min(sum(m[slot] for slot in ROOT_SLOTS) for m in poly)
        face = {
            monomial: coefficient
            for monomial, coefficient in poly.items()
            if sum(monomial[slot] for slot in ROOT_SLOTS) == order
        }
        print(side, "polynomial", row(poly), "root_order", order, "face", row(face), flush=True)
        expression = 0
        for monomial, coefficient in face.items():
            term = sp.Rational(coefficient.numerator, coefficient.denominator)
            for symbol, slot in symbol_slots:
                term *= symbol ** monomial[slot]
            expression += term
        print(side, "factor", sp.factor(expression), flush=True)


if __name__ == "__main__":
    main()
