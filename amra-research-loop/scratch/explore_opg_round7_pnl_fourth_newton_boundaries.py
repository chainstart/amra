#!/usr/bin/env python3
"""Exact endpoint inventory for the difficult fourth PNL Newton charts."""

from __future__ import annotations

import argparse
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
from explore_opg_round7_pnl_third_newton_root import (  # noqa: E402
    ROOT_SLOTS,
    parameterized,
)
from verify_pnl_double_corner_blowup import radial_projective_chart, row  # noqa: E402


ACTIVE_SLOTS = (0, 2, 4, 5, 6, 7)
NAMES = {0: "q", 2: "y", 4: "Hbar", 5: "b", 6: "v", 7: "d"}
MAXIMA = {"q": 0, "v": 6}


def sympy_expression(poly):
    symbols = sp.symbols("q unused_y y unused_h Hbar b v d")
    expression = 0
    for monomial, coefficient in poly.items():
        term = sp.Rational(coefficient.numerator, coefficient.denominator)
        for slot, exponent in enumerate(monomial):
            term *= symbols[slot] ** exponent
        expression += term
    return expression


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum", choices=tuple(MAXIMA), required=True)
    parser.add_argument(
        "--factor-boundary",
        choices=tuple(f"{NAMES[slot]}{value}" for slot in ACTIVE_SLOTS for value in (0, 1)),
    )
    args = parser.parse_args()

    below = parameterized("below")
    third_v = radial_projective_chart(below, ROOT_SLOTS, 6, 1)
    fourth_order = min(sum(m[slot] for slot in ROOT_SLOTS) for m in third_v)
    assert fourth_order == 1
    maximum_slot = MAXIMA[args.maximum]
    fourth = radial_projective_chart(
        third_v, ROOT_SLOTS, maximum_slot, fourth_order
    )
    slots = (maximum_slot, *(slot for slot in ACTIVE_SLOTS if slot != maximum_slot))
    print("chart", args.maximum, "slots", slots, "row", row(fourth), flush=True)
    for slot in slots:
        for value in (0, 1):
            boundary = specialize(fourth, slot, value)
            remaining = tuple(item for item in slots if item != slot)
            monomial, one_minus, primitive = factor_boundary(boundary, remaining)
            print(
                "boundary", NAMES[slot], value,
                "row", row(boundary) if boundary else "zero",
                "monomial", monomial,
                "one_minus", one_minus,
                "primitive", row(primitive) if primitive else "zero",
                flush=True,
            )
            if args.factor_boundary == f"{NAMES[slot]}{value}":
                print("factor", sp.factor(sympy_expression(primitive)), flush=True)


if __name__ == "__main__":
    main()
