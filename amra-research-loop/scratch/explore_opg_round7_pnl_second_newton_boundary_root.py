#!/usr/bin/env python3
"""Exact low-dimensional root at the open above/A second-Newton boundary."""

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
from verify_pnl_double_corner_blowup import radial_projective_chart, row  # noqa: E402
from verify_rlp_projective_corner_reduction import reverse_slot  # noqa: E402


def main():
    centered = centered_chart("above")
    order, _ = face_record(centered)
    radial = radial_projective_chart(centered, LOCAL_SLOTS, 1, order)
    boundary = specialize(radial, 1, 1)
    remaining = tuple(slot for slot in LOCAL_SLOTS if slot != 1)
    _, _, primitive = factor_boundary(boundary, remaining)
    reduced = primitive
    for slot, value in ((0, 1), (4, 0), (6, 1), (7, 0)):
        reduced = specialize(reduced, slot, value)
    print("bivariate_zero", not reduced, flush=True)

    local = reverse_slot(primitive, 0)
    local = reverse_slot(local, 6)
    deviation_slots = (0, 4, 6, 7)
    order = min(sum(m[slot] for slot in deviation_slots) for m in local)
    face = {
        monomial: coefficient
        for monomial, coefficient in local.items()
        if sum(monomial[slot] for slot in deviation_slots) == order
    }
    print("transverse_order", order, "face", row(face), flush=True)
    R_radial = radial_projective_chart(local, deviation_slots, 0, order)
    print("R_max_radial", row(R_radial), flush=True)

    R, zeta, H, B, C, d = sp.symbols("R zeta H B C d")
    expression = 0
    for monomial, coefficient in face.items():
        expression += sp.Rational(coefficient.numerator, coefficient.denominator) * (
            R ** monomial[0]
        ) * (zeta ** monomial[2]) * (H ** monomial[4]) * (
            B ** monomial[5]
        ) * (C ** monomial[6]) * (d ** monomial[7])
    print("factor", sp.factor(expression), flush=True)


if __name__ == "__main__":
    main()
