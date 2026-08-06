#!/usr/bin/env python3
"""Exact Gram diagnostics for the remaining q3 single-negative chambers."""

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

from verify_mixed_three_negative import divide_polynomial  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    build_delta,
    common_monomial,
    divide_monomial,
    gram,
)
from explore_opg_round7_negative_q3_single_uniform import (  # noqa: E402
    cleared_polynomial,
)


T = 7


def scale(poly, scalar):
    return {monomial: scalar * value for monomial, value in poly.items() if scalar * value}


def row(poly):
    return {
        "terms": len(poly),
        "negative": sum(value < 0 for value in poly.values()),
        "minimum": str(min(poly.values())),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
        "sha256": digest(poly),
    }


def manifest_factor(state):
    c, q0, s3, q4, s4 = (variable(slot) for slot in (0, 1, 4, 5, 6))
    factor = multiply(c, add(constant(1), s3, -1))
    if state[0] == "P":
        factor = multiply(factor, power(q0, 2))
    if state[2] == "P":
        factor = multiply(
            factor,
            multiply(q4, add(constant(1), multiply(q4, s4))),
        )
    else:
        factor = multiply(factor, add(constant(1), s4, -1))
    return factor


def beta_row(poly, slots):
    beta = bernstein_transform(poly, slots)
    return row(beta)


def main():
    delta, _, _ = build_delta()
    for state in ("PLP", "PLR", "RLP"):
        cleared = cleared_polynomial(delta, state)
        factor = manifest_factor(state)
        core = divide_polynomial(cleared, factor)
        assert cleared == multiply(factor, core)
        print("\nSTATE", state, "cleared", row(cleared), "core", row(core))
        for outer in (4, 6, 2):
            degree = max(monomial[outer] for monomial in core)
            if degree != 2:
                print("outer", outer, "degree", degree)
                continue
            g0, _, g2, determinant = gram(core, outer)
            other = [slot for slot in (2, 4, 6, T) if slot != outer]
            common = common_monomial(determinant)
            residual = divide_monomial(determinant, common)
            print(
                "outer", outer,
                "g0", row(g0), "g0b", beta_row(g0, other),
                "g2", row(g2), "g2b", beta_row(g2, other),
                "det", row(determinant), "common", common,
                "detb", beta_row(residual, other),
                flush=True,
            )


if __name__ == "__main__":
    main()
