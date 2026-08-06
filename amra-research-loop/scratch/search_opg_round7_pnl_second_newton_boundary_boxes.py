#!/usr/bin/env python3
"""Adaptive Bernstein discovery on open second-Newton rho=1 boundaries."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_a_root_accumulation import (  # noqa: E402
    LOCAL_SLOTS,
    centered_chart,
    face_record,
)
from explore_opg_round7_pnl_second_newton_boundaries import (  # noqa: E402
    NAMES,
    factor_boundary,
    specialize,
)
from search_opg_round7_pnl_second_newton_controls import float_bernstein_tensor  # noqa: E402
from search_opg_round7_rlp_bernstein_boxes import split_axis  # noqa: E402
from verify_pnl_double_corner_blowup import radial_projective_chart  # noqa: E402


def boundary_tensor(side, maximum):
    centered = centered_chart(side)
    order, _ = face_record(centered)
    maximum_slot = NAMES[maximum]
    radial = radial_projective_chart(centered, LOCAL_SLOTS, maximum_slot, order)
    boundary = specialize(radial, maximum_slot, 1)
    slots = tuple(slot for slot in LOCAL_SLOTS if slot != maximum_slot)
    monomial, one_minus, primitive = factor_boundary(boundary, slots)
    return float_bernstein_tensor(primitive, slots), slots, monomial, one_minus


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", choices=("below", "above"), required=True)
    parser.add_argument("--maximum", choices=tuple(NAMES), required=True)
    parser.add_argument("--limit", type=int, default=10000)
    parser.add_argument("--max-depth", type=int, default=100)
    args = parser.parse_args()

    root, slots, monomial, one_minus = boundary_tensor(args.side, args.maximum)
    print(
        "root", root.shape, "slots", slots, "monomial", monomial,
        "one_minus", one_minus, "negative", int(np.sum(root < 0)),
        "minimum", float(np.min(root)), flush=True,
    )
    queue = deque([(root, (0,) * len(slots), (0.0,) * len(slots), (1.0,) * len(slots))])
    processed = closed = 0
    unresolved = []
    split_counts = [0] * len(slots)
    while queue and processed < args.limit:
        tensor, depths, lower, upper = queue.pop()
        processed += 1
        scale = max(1.0, float(np.max(np.abs(tensor))))
        tolerance = -1e-12 * scale
        if float(np.min(tensor)) >= tolerance:
            closed += 1
            continue
        if sum(depths) >= args.max_depth:
            unresolved.append((depths, lower, upper, float(np.min(tensor)) / scale))
            continue

        minimum_depth = min(depths)
        eligible = [axis for axis in range(len(slots)) if depths[axis] <= minimum_depth + 2]
        best = None
        for axis in eligible:
            left, right = split_axis(tensor, axis)
            score = []
            for child in (left, right):
                child_scale = max(1.0, float(np.max(np.abs(child))))
                child_tolerance = -1e-12 * child_scale
                score.append((
                    int(np.sum(child < child_tolerance)),
                    max(0.0, -float(np.min(child)) / child_scale),
                ))
            candidate = (
                sum(item[0] for item in score),
                sum(item[1] for item in score),
                depths[axis],
                axis,
            )
            if best is None or candidate < best[0]:
                best = (candidate, axis, left, right)
        _, axis, left, right = best
        split_counts[axis] += 1
        next_depths = list(depths)
        next_depths[axis] += 1
        middle = (lower[axis] + upper[axis]) / 2
        left_upper = list(upper)
        left_upper[axis] = middle
        right_lower = list(lower)
        right_lower[axis] = middle
        queue.append((left, tuple(next_depths), lower, tuple(left_upper)))
        queue.append((right, tuple(next_depths), tuple(right_lower), upper))
        if processed % 1000 == 0:
            print(
                "progress", processed, "queue", len(queue), "closed", closed,
                "unresolved", len(unresolved), "splits", split_counts,
                flush=True,
            )
    print(
        "done", processed, "queue", len(queue), "closed", closed,
        "unresolved", len(unresolved), "splits", split_counts,
        flush=True,
    )
    print("unresolved_examples", unresolved[:10], flush=True)
    print("queued_examples", [
        (depths, lower, upper, float(np.min(tensor)))
        for tensor, depths, lower, upper in list(queue)[-10:]
    ], flush=True)


if __name__ == "__main__":
    main()
