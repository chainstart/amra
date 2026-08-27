#!/usr/bin/env python3
"""Locate Bernstein obstructions on dyadic q-annuli of the fourth PNL chart."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_third_newton_root import ROOT_SLOTS, parameterized  # noqa: E402
from search_opg_round7_pnl_second_newton_controls import float_bernstein_tensor  # noqa: E402
from search_opg_round7_rlp_bernstein_boxes import split_axis  # noqa: E402
from verify_pnl_double_corner_blowup import radial_projective_chart  # noqa: E402


ACTIVE_SLOTS = (0, 2, 4, 5, 6, 7)


def summary(tensor):
    scale = max(1.0, float(np.max(np.abs(tensor))))
    return (
        int(np.sum(tensor < -1e-12 * scale)),
        float(np.min(tensor)) / scale,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--annulus-depth", type=int, default=2)
    parser.add_argument(
        "--path",
        default="",
        help="comma-separated axis/direction refinements after the q annulus, e.g. 1L,3R",
    )
    args = parser.parse_args()
    assert args.annulus_depth >= 1

    below = parameterized("below")
    third_v = radial_projective_chart(below, ROOT_SLOTS, 6, 1)
    fourth_q = radial_projective_chart(third_v, ROOT_SLOTS, 0, 1)
    tensor = float_bernstein_tensor(fourth_q, ACTIVE_SLOTS)
    for depth in range(1, args.annulus_depth + 1):
        left, right = split_axis(tensor, 0)
        if depth == args.annulus_depth:
            tensor = right
        else:
            tensor = left
    for item in filter(None, args.path.split(",")):
        axis = int(item[:-1])
        direction = item[-1].upper()
        assert direction in ("L", "R")
        left, right = split_axis(tensor, axis)
        tensor = left if direction == "L" else right
    print(
        "annulus", f"[{2**-args.annulus_depth},{2**-(args.annulus_depth-1)}]",
        "path", args.path or "root", "summary", summary(tensor), flush=True,
    )
    for axis, slot in enumerate(ACTIVE_SLOTS):
        left, right = split_axis(tensor, axis)
        print(
            "split_axis", axis, "slot", slot,
            "left", summary(left), "right", summary(right), flush=True,
        )


if __name__ == "__main__":
    main()
