#!/usr/bin/env python3
"""Float Bernstein scan of the two charts at the third PNL Newton root."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_third_newton_root import (  # noqa: E402
    ROOT_SLOTS,
    parameterized,
)
from search_opg_round7_pnl_second_newton_controls import float_bernstein_tensor  # noqa: E402
from search_opg_round7_rlp_bernstein_boxes import split_axis  # noqa: E402
from verify_negative_c_direct_chambers import bernstein_transform  # noqa: E402
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_pnl_double_corner_blowup import radial_projective_chart  # noqa: E402


ACTIVE_SLOTS = (0, 2, 4, 5, 6, 7)
MAXIMA = {"R": 0, "v": 6}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", choices=("below", "above"), required=True)
    parser.add_argument("--maximum", choices=tuple(MAXIMA), required=True)
    parser.add_argument("--exact", action="store_true")
    parser.add_argument("--chain-axis", type=int)
    parser.add_argument("--chain-direction", choices=("left", "right"), default="left")
    parser.add_argument("--chain-depth", type=int, default=12)
    args = parser.parse_args()

    poly = parameterized(args.side)
    order = min(sum(m[slot] for slot in ROOT_SLOTS) for m in poly)
    assert order == 1
    maximum_slot = MAXIMA[args.maximum]
    radial = radial_projective_chart(poly, ROOT_SLOTS, maximum_slot, order)
    slots = (maximum_slot, *(slot for slot in ACTIVE_SLOTS if slot != maximum_slot))
    if args.exact:
        controls = bernstein_transform(radial, list(slots))
        print(
            "exact", "side", args.side, "maximum", args.maximum,
            "slots", slots, "nonzero", len(controls),
            "negative", sum(value < 0 for value in controls.values()),
            "minimum_nonzero", min(controls.values()),
            "maximum_value", max(controls.values()),
            "sha256", digest(controls),
            flush=True,
        )
        return
    controls = float_bernstein_tensor(radial, slots)
    scale = max(1.0, float(np.max(np.abs(controls))))
    tolerance = -1e-12 * scale
    negative = np.argwhere(controls < tolerance)
    print(
        "side", args.side, "maximum", args.maximum, "slots", slots,
        "shape", controls.shape, "scale", scale,
        "negative", len(negative), "minimum_scaled", float(np.min(controls)) / scale,
        flush=True,
    )
    for axis, slot in enumerate(slots):
        if not len(negative):
            break
        values, counts = np.unique(negative[:, axis], return_counts=True)
        histogram = ",".join(f"{int(v)}:{int(c)}" for v, c in zip(values, counts))
        print("negative_axis", axis, "slot", slot, histogram, flush=True)
    if args.chain_axis is not None:
        tensor = controls
        for depth in range(1, args.chain_depth + 1):
            left, right = split_axis(tensor, args.chain_axis)
            rows = []
            for child in (left, right):
                child_scale = max(1.0, float(np.max(np.abs(child))))
                rows.append((
                    int(np.sum(child < -1e-12 * child_scale)),
                    float(np.min(child)) / child_scale,
                ))
            print("chain", depth, "left", rows[0], "right", rows[1], flush=True)
            tensor = left if args.chain_direction == "left" else right


if __name__ == "__main__":
    main()
