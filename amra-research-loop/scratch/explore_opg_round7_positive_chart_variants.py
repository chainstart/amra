#!/usr/bin/env python3
"""Scan both rational-side choices for positive-activity page charts."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from verify_c_zero_fibre import EDGES  # noqa: E402
from verify_mixed_three_negative import divide_polynomial  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_page_direct_chambers import C_EDGE, ROUTES  # noqa: E402
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    build_delta,
    common_monomial,
    divide_monomial,
    gram,
)
from explore_opg_round7_m88 import row  # noqa: E402
from explore_opg_round7_negative_q3_single_uniform import negative_page_chart  # noqa: E402
from explore_opg_round7_negative_q3_odds_chart import positive_page_chart  # noqa: E402
from explore_opg_round7_remaining_single_gram import manifest_factor  # noqa: E402


def positive_variant(index, state, rational_side):
    if state != "P" or rational_side == "R":
        return positive_page_chart(index, state)
    assert rational_side == "L"
    q, s = variable(1 + 2 * index), variable(2 + 2 * index)
    return (
        multiply(q, add(constant(1), s, -1)),
        multiply(q, s),
        add(constant(1), multiply(q, s)),
        "L",
    )


def cleared_polynomial(delta, state, choices):
    negative = negative_page_chart(state[1])
    pages = {
        index: positive_variant(index, state[index], choices.get(index, "R"))
        for index in (0, 2)
    }
    result = {}
    for original_monomial, value in delta.items():
        term = constant(value)
        term = multiply(term, power(variable(0), original_monomial[EDGES.index(C_EDGE)]))
        for index, edges in enumerate(ROUTES):
            if index == 1:
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


def main():
    delta, _, _ = build_delta()
    variants = {
        "PLP": ({0: left, 2: right} for left in "LR" for right in "LR"),
        "PLR": ({0: left} for left in "LR"),
        "RLP": ({2: right} for right in "LR"),
    }
    for state, choices_set in variants.items():
        for choices in choices_set:
            cleared = cleared_polynomial(delta, state, choices)
            core = divide_polynomial(cleared, manifest_factor(state))
            label = "".join(f"p{index}{side}" for index, side in sorted(choices.items()))
            direct = bernstein_transform(core, [2, 4, 6, 7])
            print("\n", state, label, "core", row(core), "direct", row(direct))
            for outer in (4, 6):
                g0, _, g2, determinant = gram(core, outer)
                other = [slot for slot in (2, 4, 6, 7) if slot != outer]
                residual = divide_monomial(determinant, common_monomial(determinant))
                print(
                    "outer", outer,
                    "g0", row(bernstein_transform(g0, other)),
                    "g2", row(bernstein_transform(g2, other)),
                    "det", row(bernstein_transform(residual, other)),
                    flush=True,
                )


if __name__ == "__main__":
    main()
