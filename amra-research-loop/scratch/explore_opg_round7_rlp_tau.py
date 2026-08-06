#!/usr/bin/env python3
"""Exact factor diagnostics for the RLP outer-Gram tau cubic."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from verify_mixed_three_negative import divide_polynomial  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_nonshared_same_side_gram import positive_route_data  # noqa: E402
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    build_delta,
    coefficient,
    common_monomial,
    divide_monomial,
    gram,
    scale,
)
from explore_opg_round7_m88 import row, sympy_poly  # noqa: E402
from explore_opg_round7_negative_q3_single_uniform import cleared_polynomial  # noqa: E402
from explore_opg_round7_remaining_single_gram import manifest_factor  # noqa: E402


def build():
    delta, _, _ = build_delta()
    core = divide_polynomial(cleared_polynomial(delta, "RLP"), manifest_factor("RLP"))
    determinant = gram(core, 4)[3]
    residual = divide_monomial(determinant, common_monomial(determinant))
    q0, s0 = variable(1), variable(2)
    _, _, determinant_sum = positive_route_data(1)
    factor = multiply(power(add(q0, s0), 2), determinant_sum)
    h1884 = divide_polynomial(residual, factor)
    assert residual == multiply(factor, h1884)
    betas = [
        coefficient(bernstein_transform(h1884, [7]), 7, index)
        for index in range(4)
    ]

    c, q4, s4 = variable(0), variable(5), variable(6)
    one_minus_s4 = add(constant(1), s4, -1)
    j8 = add(
        power(add(multiply(q0, one_minus_s4), s0), 2),
        multiply(
            power(s0, 2),
            multiply(
                power(s4, 2),
                add(add(multiply(q0, q4), q0), q4),
            ),
        ),
    )
    assert betas[3] == multiply(
        multiply(multiply(power(c, 3), power(q4, 3)), add(c, q4)),
        power(j8, 2),
    )
    k30 = divide_polynomial(betas[0], power(determinant_sum, 3))
    n = scale(
        divide_polynomial(
            divide_polynomial(
                divide_polynomial(betas[1], c),
                q4,
            ),
            power(determinant_sum, 2),
        ),
        3,
    )
    h21 = scale(
        divide_polynomial(
            betas[2],
            multiply(
                multiply(multiply(power(c, 2), power(q4, 2)), determinant_sum),
                j8,
            ),
        ),
        3,
    )
    return h1884, betas, k30, n, j8, h21


def main():
    import sympy as sp

    h1884, betas, k30, n, j8, h21 = build()
    print("H1884", row(h1884))
    for index, beta in enumerate(betas):
        print("beta", index, row(beta))
    for name, poly in (("K30", k30), ("N", n), ("J8", j8), ("H21", h21)):
        print(name, row(poly))
        _, converted = sympy_poly(poly)
        print(name, "factor", sp.factor(converted.as_expr()))
        if name in ("N", "H21"):
            for c_degree in range(2):
                part = coefficient(poly, 0, c_degree)
                print(name, "c", c_degree, row(part), sp.factor(sympy_poly(part)[1].as_expr()))


if __name__ == "__main__":
    main()
