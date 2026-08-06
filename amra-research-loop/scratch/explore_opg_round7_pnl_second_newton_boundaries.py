#!/usr/bin/env python3
"""Exact boundary reductions for the open PNL second-Newton charts."""

from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_a_root_accumulation import (  # noqa: E402
    LOCAL_SLOTS,
    centered_chart,
    face_record,
)
from verify_negative_q0_no_positive_gram import common_monomial, divide_monomial  # noqa: E402
from verify_opposite_nonshared_chambers import divide_one_minus_variable  # noqa: E402
from verify_pnl_double_corner_blowup import radial_projective_chart, row  # noqa: E402


NAMES = {
    "r": 0,
    "zeta": 2,
    "A": 1,
    "Hbar": 4,
    "B": 5,
    "C": 6,
    "d": 7,
}


def specialize(poly, slot, value):
    value = Fraction(value)
    result = {}
    for monomial, coefficient in poly.items():
        reduced = list(monomial)
        exponent = reduced[slot]
        reduced[slot] = 0
        key = tuple(reduced)
        result[key] = result.get(key, Fraction()) + coefficient * value**exponent
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def factor_boundary(poly, slots):
    monomial = common_monomial(poly)
    reduced = divide_monomial(poly, monomial)
    one_minus = {}
    for slot in slots:
        multiplicity = 0
        while True:
            try:
                candidate = divide_one_minus_variable(reduced, slot)
            except AssertionError:
                break
            reduced = candidate
            multiplicity += 1
        if multiplicity:
            one_minus[slot] = multiplicity
    return monomial, one_minus, reduced


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", choices=("below", "above"), required=True)
    parser.add_argument("--maximum", choices=tuple(NAMES), required=True)
    args = parser.parse_args()

    centered = centered_chart(args.side)
    order, _ = face_record(centered)
    maximum_slot = NAMES[args.maximum]
    radial = radial_projective_chart(centered, LOCAL_SLOTS, maximum_slot, order)
    boundary = specialize(radial, maximum_slot, 1)
    remaining = tuple(slot for slot in LOCAL_SLOTS if slot != maximum_slot)
    monomial, one_minus, primitive = factor_boundary(boundary, remaining)
    print(
        "chart", args.side, args.maximum,
        "radial", row(radial),
        "rho_one", row(boundary),
        "monomial", monomial,
        "one_minus", one_minus,
        "primitive", row(primitive),
        flush=True,
    )
    for slot in remaining:
        for value in (0, 1):
            face = specialize(primitive, slot, value)
            print(
                "primitive_boundary", "slot", slot, "value", value,
                "row", row(face) if face else "zero",
                flush=True,
            )


if __name__ == "__main__":
    main()
