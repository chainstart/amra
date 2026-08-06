#!/usr/bin/env python3
"""Discovery analysis of the q3:PNL tau-copositivity tangency."""

from __future__ import annotations

from pathlib import Path
from fractions import Fraction
import sys

import sympy as sp


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))
sys.path.insert(0, str(Path(__file__).parent))

from explore_opg_round7_negative_q3_odds_chart import cleared_polynomial  # noqa: E402
from verify_mixed_three_negative import divide_polynomial  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_opposite_nonshared_chambers import divide_one_minus_variable  # noqa: E402
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    coefficient,
    common_monomial,
    divide_monomial,
    gram,
    scale,
)
from verify_negative_q0_no_positive_gram import build_delta  # noqa: E402
from verify_rlp_projective_corner_reduction import reverse_slot  # noqa: E402


NAMES = ("c", "q0", "s0", "q3", "h", "q4", "s4", "tau")
SYMBOLS = sp.symbols(" ".join(NAMES))


def to_sympy(poly):
    result = 0
    for monomial, value in poly.items():
        term = sp.Rational(value.numerator, value.denominator)
        for symbol, degree in zip(SYMBOLS, monomial):
            term *= symbol**degree
        result += term
    return result


def row(poly):
    if not poly:
        return {"terms": 0}
    return {
        "terms": len(poly),
        "negative": sum(value < 0 for value in poly.values()),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
        "sha256": digest(poly),
    }


def strip_one_minus(poly, slot):
    count = 0
    while True:
        try:
            quotient = divide_one_minus_variable(poly, slot)
        except AssertionError:
            return count, poly
        count += 1
        poly = quotient


def main():
    delta, _, _ = build_delta()
    cleared = cleared_polynomial(delta, "PNL")
    cleared_common = common_monomial(cleared)
    core = divide_monomial(cleared, cleared_common)
    b0, b1, b2, determinant = gram(core, 7)
    print("raw commons", cleared_common, common_monomial(b0), common_monomial(b1), common_monomial(b2), common_monomial(determinant), flush=True)
    for label, poly in (("b1", b1), ("det", determinant)):
        stripped = poly
        factors = []
        for slot in (2, 4, 6):
            count, stripped = strip_one_minus(stripped, slot)
            factors.append(count)
        print(label, "one-minus", factors, "residual", row(stripped), flush=True)

    c, q0, s0, _, s3, _, _, _ = (variable(slot) for slot in range(8))
    one_minus_s0 = add(constant(1), s0, -1)
    one_minus_s3 = add(constant(1), s3, -1)
    j_factor = multiply(c, one_minus_s0)
    J = scale(
        divide_one_minus_variable(
            divide_monomial(b1, (1, 0, 0, 0, 0, 0, 0, 0)),
            2,
        ),
        -2,
    )
    assert b1 == scale(multiply(j_factor, J), Fraction(-1, 2))
    s4_power, J_small = strip_one_minus(J, 6)
    print("J s4 factor", s4_power, row(J_small), flush=True)

    det_factor = multiply(
        power(c, 2),
        multiply(power(one_minus_s0, 2), power(one_minus_s3, 2)),
    )
    R = divide_monomial(determinant, (2, 0, 0, 0, 0, 0, 0, 0))
    R = divide_one_minus_variable(divide_one_minus_variable(R, 2), 2)
    R = divide_one_minus_variable(divide_one_minus_variable(R, 4), 4)
    R = scale(R, 4)
    assert determinant == scale(multiply(det_factor, R), Fraction(1, 4))

    print("cleared", cleared_common, row(cleared), row(core), flush=True)
    print("b", row(b0), row(b1), row(b2), flush=True)
    print("J", row(J), flush=True)
    print("R", row(R), flush=True)

    J_h = reverse_slot(J_small, 4)
    R_h = reverse_slot(R, 4)
    for name, poly in (("J", J_h), ("R", R_h)):
        degree = max(monomial[4] for monomial in poly)
        print(name, "h-degree", degree, flush=True)
        for index in range(degree + 1):
            part = coefficient(poly, 4, index)
            print(name, "h", index, row(part), flush=True)
            if name == "J":
                print(sp.factor(to_sympy(part)), flush=True)

    # Record the exact endpoint rank-one identity in its smallest form.
    b_h = [reverse_slot(entry, 4) for entry in (b0, b1, b2)]
    endpoint = [coefficient(entry, 4, 0) for entry in b_h]
    print("endpoint b0", sp.factor(to_sympy(endpoint[0])), flush=True)
    print("endpoint b1", sp.factor(to_sympy(endpoint[1])), flush=True)
    print("endpoint b2", sp.factor(to_sympy(endpoint[2])), flush=True)


if __name__ == "__main__":
    main()
