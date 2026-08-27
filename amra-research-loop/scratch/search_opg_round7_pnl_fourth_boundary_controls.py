#!/usr/bin/env python3
"""Bernstein scans for endpoint restrictions of the fourth PNL q-chart."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_second_newton_boundaries import (  # noqa: E402
    factor_boundary,
    specialize,
)
from explore_opg_round7_pnl_third_newton_root import ROOT_SLOTS, parameterized  # noqa: E402
from search_opg_round7_pnl_second_newton_controls import float_bernstein_tensor  # noqa: E402
from verify_negative_c_direct_chambers import bernstein_transform  # noqa: E402
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_pnl_double_corner_blowup import radial_projective_chart, row  # noqa: E402


ACTIVE_SLOTS = (0, 2, 4, 5, 6, 7)
NAMES = {"q": 0, "y": 2, "Hbar": 4, "b": 5, "v": 6, "d": 7}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variable", choices=tuple(NAMES), required=True)
    parser.add_argument("--value", type=int, choices=(0, 1), required=True)
    parser.add_argument("--exact", action="store_true")
    args = parser.parse_args()

    below = parameterized("below")
    third_v = radial_projective_chart(below, ROOT_SLOTS, 6, 1)
    fourth_q = radial_projective_chart(third_v, ROOT_SLOTS, 0, 1)
    fixed_slot = NAMES[args.variable]
    boundary = specialize(fourth_q, fixed_slot, args.value)
    slots = tuple(slot for slot in ACTIVE_SLOTS if slot != fixed_slot)
    monomial, one_minus, primitive = factor_boundary(boundary, slots)
    print(
        "boundary", args.variable, args.value, "row", row(boundary),
        "monomial", monomial, "one_minus", one_minus,
        "primitive", row(primitive), "slots", slots,
        flush=True,
    )
    if args.exact:
        controls = bernstein_transform(primitive, list(slots))
        degrees = row(primitive)["degrees"]
        total = 1
        for slot in slots:
            total *= degrees[slot] + 1
        print(
            "exact", "total", total, "nonzero", len(controls),
            "negative", sum(value < 0 for value in controls.values()),
            "minimum", min(controls.values()), "maximum", max(controls.values()),
            "sha256", digest(controls), flush=True,
        )
        return
    controls = float_bernstein_tensor(primitive, slots)
    scale = max(1.0, float(np.max(np.abs(controls))))
    negative = np.argwhere(controls < -1e-12 * scale)
    print(
        "float", "shape", controls.shape, "scale", scale,
        "negative", len(negative), "minimum_scaled", float(np.min(controls)) / scale,
        flush=True,
    )
    for axis, slot in enumerate(slots):
        if not len(negative):
            break
        values, counts = np.unique(negative[:, axis], return_counts=True)
        print(
            "negative_axis", axis, slot,
            ",".join(f"{int(value)}:{int(count)}" for value, count in zip(values, counts)),
            flush=True,
        )


if __name__ == "__main__":
    main()
