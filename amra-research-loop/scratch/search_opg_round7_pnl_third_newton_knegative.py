#!/usr/bin/env python3
"""Bernstein discovery on the K<=0 part of the above/A transverse R chart."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_third_newton_root import R_max_polynomial  # noqa: E402
from search_opg_round7_pnl_second_newton_controls import float_bernstein_tensor  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    variable,
)
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_negative_q0_no_positive_gram import scale  # noqa: E402
from verify_pnl_double_corner_blowup import row, substitute_slot  # noqa: E402
from verify_rlp_projective_corner_reduction import polynomial_sum  # noqa: E402


ACTIVE_SLOTS = (0, 2, 4, 5, 6, 7)


def parameterized(patch):
    poly = R_max_polynomial()
    b, y = (variable(slot) for slot in (5, 2))
    if patch == "high_B":
        # B=(1+6*b)/7 gives K<=0 for every zeta=y.
        poly, degree = substitute_slot(
            poly, 5, polynomial_sum(constant(1), scale(b, 6)), constant(7)
        )
        assert degree == 5
    else:
        # B=b/7 and zeta=[7*(1-b)+11*b*y]/(7+4*b) cover the part
        # above the moving-root threshold; K=-11*b*y/7.
        poly, degree = substitute_slot(poly, 5, b, constant(7))
        assert degree == 5
        numerator = polynomial_sum(
            scale(add(constant(1), b, -1), 7),
            scale(multiply(b, y), 11),
        )
        denominator = polynomial_sum(constant(7), scale(b, 4))
        poly, degree = substitute_slot(poly, 2, numerator, denominator)
        assert degree == 4
    return poly


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch", choices=("high_B", "low_B_high_zeta"), required=True)
    parser.add_argument("--exact", action="store_true")
    args = parser.parse_args()

    poly = parameterized(args.patch)
    if args.exact:
        controls = bernstein_transform(poly, list(ACTIVE_SLOTS))
        print(
            "exact", "patch", args.patch, "polynomial", row(poly),
            "nonzero", len(controls),
            "negative", sum(value < 0 for value in controls.values()),
            "minimum_nonzero", min(controls.values()),
            "maximum", max(controls.values()),
            "sha256", digest(controls),
            flush=True,
        )
        return
    controls = float_bernstein_tensor(poly, ACTIVE_SLOTS)
    scale_value = max(1.0, float(np.max(np.abs(controls))))
    tolerance = -1e-12 * scale_value
    negative = np.argwhere(controls < tolerance)
    print(
        "patch", args.patch, "polynomial", row(poly), "shape", controls.shape,
        "negative", len(negative), "minimum_scaled", float(np.min(controls)) / scale_value,
        flush=True,
    )
    for axis, slot in enumerate(ACTIVE_SLOTS):
        if not len(negative):
            break
        values, counts = np.unique(negative[:, axis], return_counts=True)
        histogram = ",".join(f"{int(v)}:{int(c)}" for v, c in zip(values, counts))
        print("negative_axis", axis, "slot", slot, histogram, flush=True)


if __name__ == "__main__":
    main()
