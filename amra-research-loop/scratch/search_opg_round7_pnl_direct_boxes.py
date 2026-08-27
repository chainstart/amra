#!/usr/bin/env python3
"""Float discovery for a coefficientwise adaptive PNL Bernstein tree."""

from __future__ import annotations

from collections import deque
from pathlib import Path
import argparse
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_negative_q3_odds_chart import cleared_polynomial  # noqa: E402
from search_opg_round7_pnl_conditional_boxes import split_axis  # noqa: E402
from verify_negative_c_direct_chambers import bernstein_transform  # noqa: E402
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    build_delta,
    common_monomial,
    divide_monomial,
)
from verify_opposite_nonshared_chambers import divide_one_minus_variable  # noqa: E402
from verify_rlp_projective_corner_reduction import reverse_slot  # noqa: E402


ROUTE_SLOTS = (0, 1, 5)
BOX_SLOTS = (2, 4, 6, 7)


def blow_up(poly, chart):
    result = {}
    for monomial, value in poly.items():
        x_degree, h_degree = monomial[2], monomial[4]
        assert x_degree + h_degree >= 2
        transformed = list(monomial)
        if chart == "x":
            transformed[2] = x_degree + h_degree - 2
            transformed[4] = h_degree
        else:
            assert chart == "h"
            transformed[4] = x_degree + h_degree - 2
            transformed[2] = x_degree
        transformed = tuple(transformed)
        result[transformed] = result.get(transformed, 0) + value
    return {monomial: value for monomial, value in result.items() if value}


def root_tensor(chart):
    delta, _, _ = build_delta()
    cleared = cleared_polynomial(delta, "PNL")
    core = divide_monomial(cleared, common_monomial(cleared))
    core = divide_one_minus_variable(core, 6)
    if chart != "original":
        for slot in BOX_SLOTS:
            core = reverse_slot(core, slot)
        core = blow_up(core, chart)
    transformed = bernstein_transform(core, list(BOX_SLOTS))
    route_shape = tuple(
        max(monomial[slot] for monomial in transformed) + 1
        for slot in ROUTE_SLOTS
    )
    box_shape = tuple(
        max(monomial[slot] for monomial in transformed) + 1
        for slot in BOX_SLOTS
    )
    tensor = np.zeros((int(np.prod(route_shape)),) + box_shape)
    for monomial, value in transformed.items():
        route_index = np.ravel_multi_index(
            tuple(monomial[slot] for slot in ROUTE_SLOTS), route_shape
        )
        tensor[(route_index,) + tuple(monomial[slot] for slot in BOX_SLOTS)] = float(value)
    return tensor, route_shape


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=500_000)
    parser.add_argument("--max-depth", type=int, default=80)
    parser.add_argument("--chart", choices=("original", "x", "h"), default="original")
    args = parser.parse_args()
    root, route_shape = root_tensor(args.chart)
    print("root", root.shape, route_shape, "negative", int(np.sum(root < 0)), flush=True)
    queue = deque([(
        root,
        (0,) * len(BOX_SLOTS),
        (0.0,) * len(BOX_SLOTS),
        (1.0,) * len(BOX_SLOTS),
    )])
    processed = closed = 0
    unresolved = []
    axis_counts = [0] * len(BOX_SLOTS)
    maximum_seen_depth = 0
    while queue and processed < args.limit:
        tensor, depths, lower, upper = queue.pop()
        processed += 1
        maximum_seen_depth = max(maximum_seen_depth, sum(depths))
        scale = max(1.0, float(np.max(np.abs(tensor))))
        if float(np.min(tensor)) >= -1e-12 * scale:
            closed += 1
            continue
        if sum(depths) >= args.max_depth:
            unresolved.append((
                depths, lower, upper, float(np.min(tensor)) / scale
            ))
            continue
        priorities = (3, 1, 0, 2)
        minimum_depth = min(depths)
        eligible = [
            axis for axis in priorities if depths[axis] <= minimum_depth + 2
        ]
        choices = []
        for axis in eligible:
            left, right = split_axis(tensor, axis)
            score = []
            for child in (left, right):
                child_scale = max(1.0, float(np.max(np.abs(child))))
                tolerance = -1e-12 * child_scale
                score.append((
                    float(np.min(child)) < tolerance,
                    int(np.sum(child < tolerance)),
                    max(0.0, -float(np.min(child)) / child_scale),
                ))
            choices.append((
                (sum(row[0] for row in score), sum(row[1] for row in score),
                 sum(row[2] for row in score), depths[axis], priorities.index(axis)),
                axis, left, right,
            ))
        _, axis, left, right = min(choices, key=lambda item: item[0])
        axis_counts[axis] += 1
        next_depths = list(depths)
        next_depths[axis] += 1
        middle = (lower[axis] + upper[axis]) / 2
        left_upper = list(upper)
        left_upper[axis] = middle
        right_lower = list(lower)
        right_lower[axis] = middle
        queue.append((left, tuple(next_depths), lower, tuple(left_upper)))
        queue.append((right, tuple(next_depths), tuple(right_lower), upper))
        if processed % 50_000 == 0:
            print(
                "progress", processed, "queue", len(queue), "closed", closed,
                "unresolved", len(unresolved), "axes", axis_counts, flush=True,
            )
    print(
        "done", processed, "queue", len(queue), "closed", closed,
        "unresolved", len(unresolved), "axes", axis_counts,
        "maximum_seen_depth", maximum_seen_depth, flush=True,
    )
    print("examples", unresolved[:20], flush=True)
    print("queued_examples", [
        (depths, lower, upper, float(np.min(tensor)))
        for tensor, depths, lower, upper in list(queue)[-20:]
    ], flush=True)


if __name__ == "__main__":
    main()
