#!/usr/bin/env python3
"""Float adaptive projective-box discovery for the two PNL blow-up charts."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_negative_q3_odds_chart import cleared_polynomial  # noqa: E402
from search_opg_round7_pnl_direct_boxes import blow_up  # noqa: E402
from search_opg_round7_rlp_bernstein_boxes import split_axis  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    build_delta,
    common_monomial,
    divide_monomial,
)
from verify_opposite_nonshared_chambers import divide_one_minus_variable  # noqa: E402
from verify_rlp_projective_corner_reduction import reverse_slot  # noqa: E402


ROUTES = (0, 1, 5)
SLOTS = (0, 1, 2, 4, 5, 6, 7)
ROUTE_MIN = 7
ROUTE_MAX = 12


def projective_chart(poly, maximum_slot):
    ratio_slots = tuple(slot for slot in ROUTES if slot != maximum_slot)
    result = {}
    for monomial, value in poly.items():
        route_degree = sum(monomial[slot] for slot in ROUTES)
        assert ROUTE_MIN <= route_degree <= ROUTE_MAX
        projected = [0] * 8
        projected[0] = route_degree - ROUTE_MIN
        projected[1] = monomial[ratio_slots[0]]
        projected[5] = monomial[ratio_slots[1]]
        for slot in (2, 4, 6, 7):
            projected[slot] = monomial[slot]
        key = tuple(projected)
        result[key] = result.get(key, 0) + value
    return {monomial: value for monomial, value in result.items() if value}


def compactify_scale(poly):
    u = variable(0)
    one_minus_u = add(constant(1), u, -1)
    result = {}
    for monomial, value in poly.items():
        exponent = monomial[0]
        reduced = list(monomial)
        reduced[0] = 0
        term = {tuple(reduced): value}
        term = multiply(term, power(u, exponent))
        term = multiply(term, power(one_minus_u, ROUTE_MAX - ROUTE_MIN - exponent))
        result = add(result, term)
    return result


def control_tensor(activity_chart, maximum_slot):
    delta, _, _ = build_delta()
    cleared = cleared_polynomial(delta, "PNL")
    core = divide_monomial(cleared, common_monomial(cleared))
    core = divide_one_minus_variable(core, 6)
    for slot in (2, 4, 6, 7):
        core = reverse_slot(core, slot)
    core = blow_up(core, activity_chart)
    compact = compactify_scale(projective_chart(core, maximum_slot))
    transformed = bernstein_transform(compact, list(SLOTS))
    shape = tuple(
        max(monomial[slot] for monomial in transformed) + 1 for slot in SLOTS
    )
    tensor = np.zeros(shape)
    for monomial, value in transformed.items():
        tensor[tuple(monomial[slot] for slot in SLOTS)] = float(value)
    return tensor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--activity", choices=("x", "h"), required=True)
    parser.add_argument("--maximum", choices=("c", "q0", "q4"), required=True)
    parser.add_argument("--limit", type=int, default=100_000)
    parser.add_argument("--max-depth", type=int, default=120)
    args = parser.parse_args()
    maximum_slot = {"c": 0, "q0": 1, "q4": 5}[args.maximum]
    root = control_tensor(args.activity, maximum_slot)
    print("root", root.shape, "negative", int(np.sum(root < 0)), flush=True)

    queue = deque([(
        root,
        (0,) * len(SLOTS),
        (0.0,) * len(SLOTS),
        (1.0,) * len(SLOTS),
    )])
    processed = closed = 0
    unresolved = []
    axes = [0] * len(SLOTS)
    maximum_seen_depth = 0
    while queue and processed < args.limit:
        tensor, depths, lower, upper = queue.pop()
        processed += 1
        maximum_seen_depth = max(maximum_seen_depth, sum(depths))
        scale = max(1.0, float(np.max(np.abs(tensor))))
        tolerance = -1e-12 * scale
        if float(np.min(tensor)) >= tolerance:
            closed += 1
            continue
        if sum(depths) >= args.max_depth:
            unresolved.append((
                depths, lower, upper, float(np.min(tensor)) / scale
            ))
            continue
        minimum_depth = min(depths)
        priorities = (6, 3, 2, 5, 0, 1, 4)
        eligible = [
            axis for axis in priorities if depths[axis] <= minimum_depth + 2
        ]
        choices = []
        for axis in eligible:
            left, right = split_axis(tensor, axis)
            scores = []
            for child in (left, right):
                child_scale = max(1.0, float(np.max(np.abs(child))))
                child_tolerance = -1e-12 * child_scale
                child_minimum = float(np.min(child))
                scores.append((
                    child_minimum < child_tolerance,
                    int(np.sum(child < child_tolerance)),
                    max(0.0, -child_minimum / child_scale),
                ))
            choices.append((
                (sum(item[0] for item in scores),
                 sum(item[1] for item in scores),
                 sum(item[2] for item in scores),
                 depths[axis], priorities.index(axis)),
                axis, left, right,
            ))
        _, axis, left, right = min(choices, key=lambda item: item[0])
        axes[axis] += 1
        next_depths = list(depths)
        next_depths[axis] += 1
        middle = (lower[axis] + upper[axis]) / 2
        left_upper = list(upper)
        left_upper[axis] = middle
        right_lower = list(lower)
        right_lower[axis] = middle
        queue.append((left, tuple(next_depths), lower, tuple(left_upper)))
        queue.append((right, tuple(next_depths), tuple(right_lower), upper))
        if processed % 10_000 == 0:
            print(
                "progress", processed, "queue", len(queue), "closed", closed,
                "unresolved", len(unresolved), "axes", axes, flush=True,
            )
    print(
        "done", processed, "queue", len(queue), "closed", closed,
        "unresolved", len(unresolved), "axes", axes,
        "maximum_seen_depth", maximum_seen_depth, flush=True,
    )
    print("unresolved_examples", unresolved[:10], flush=True)
    print("queued_examples", [
        (depths, lower, upper, float(np.min(tensor)))
        for tensor, depths, lower, upper in list(queue)[-10:]
    ], flush=True)


if __name__ == "__main__":
    main()
