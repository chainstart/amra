#!/usr/bin/env python3
"""Exact y-split certificates on q in [1/4,1/2] in the fourth PNL chart."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_third_newton_root import ROOT_SLOTS, parameterized  # noqa: E402
from verify_negative_c_direct_chambers import bernstein_transform, constant, variable  # noqa: E402
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_pnl_double_corner_blowup import (  # noqa: E402
    radial_projective_chart,
    row,
    substitute_slot,
)
from verify_rlp_projective_corner_reduction import polynomial_sum  # noqa: E402


ACTIVE_SLOTS = (0, 2, 4, 5, 6, 7)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--y-half", choices=("lower", "upper"), required=True)
    args = parser.parse_args()

    below = parameterized("below")
    third_v = radial_projective_chart(below, ROOT_SLOTS, 6, 1)
    fourth_q = radial_projective_chart(third_v, ROOT_SLOTS, 0, 1)
    q, y = (variable(slot) for slot in (0, 2))
    annulus, degree = substitute_slot(
        fourth_q, 0, polynomial_sum(constant(1), q), constant(4)
    )
    assert degree == 56
    numerator = y if args.y_half == "lower" else polynomial_sum(constant(1), y)
    box, degree = substitute_slot(annulus, 2, numerator, constant(2))
    assert degree == 6
    box_row = row(box)
    print("box", args.y_half, "polynomial", box_row, flush=True)
    controls = bernstein_transform(box, list(ACTIVE_SLOTS))
    total = 1
    for slot in ACTIVE_SLOTS:
        total *= box_row["degrees"][slot] + 1
    print(
        "total", total,
        "nonzero", len(controls),
        "negative", sum(value < 0 for value in controls.values()),
        "minimum", min(controls.values()),
        "maximum", max(controls.values()),
        "sha256", digest(controls),
        flush=True,
    )


if __name__ == "__main__":
    main()
