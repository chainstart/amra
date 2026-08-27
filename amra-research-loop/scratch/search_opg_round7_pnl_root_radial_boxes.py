#!/usr/bin/env python3
"""Float discovery for the projective radial charts at the PNL moving root."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from search_opg_round7_rlp_bernstein_boxes import split_axis  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    variable,
)
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    build_delta,
    common_monomial,
    divide_monomial,
    scale,
)
from verify_negative_nonshared_double_negative_gram import cleared_polynomial  # noqa: E402
from verify_opposite_nonshared_chambers import divide_one_minus_variable  # noqa: E402
from verify_pnl_double_corner_blowup import (  # noqa: E402
    activity_blowup,
    compactify_scale,
    projective_chart,
    radial_projective_chart,
    substitute_slot,
)
from verify_rlp_projective_corner_reduction import (  # noqa: E402
    polynomial_sum,
    reverse_slot,
)


RADIAL_SLOTS = (0, 1, 4, 5, 6, 7)
MAXIMUM_SLOTS = {
    "a": 0,
    "ratio1": 1,
    "H": 4,
    "ratio2": 5,
    "e": 6,
    "s": 7,
}


def root_polynomial(branch):
    delta, _, _ = build_delta()
    cleared = cleared_polynomial(delta, "PNL", 1)
    core = divide_monomial(cleared, common_monomial(cleared))
    quotient = divide_one_minus_variable(core, 6)
    local = quotient
    for slot in (2, 4, 6, 7):
        local = reverse_slot(local, slot)
    h_chart = activity_blowup(local, "h")
    boundary = compactify_scale(projective_chart(h_chart, 0))
    for slot in RADIAL_SLOTS:
        boundary = reverse_slot(boundary, slot)

    a, z, H, s = (variable(slot) for slot in (0, 2, 4, 7))
    L = polynomial_sum(H, scale(a, 3))
    denominator = add(L, s)
    if branch == "negative":
        numerator = multiply(s, add(constant(1), z, -1))
    else:
        numerator = add(s, multiply(L, z))
    result, degree = substitute_slot(boundary, 2, numerator, denominator)
    assert degree == 4
    assert min(sum(m[slot] for slot in RADIAL_SLOTS) for m in result) == 7
    return result


def control_tensor(branch, maximum_slot):
    root = root_polynomial(branch)
    radial = radial_projective_chart(root, RADIAL_SLOTS, maximum_slot, 7)
    slots = (maximum_slot, 2, *(slot for slot in RADIAL_SLOTS if slot != maximum_slot))
    controls = bernstein_transform(radial, list(slots))
    shape = tuple(max(m[slot] for m in radial) + 1 for slot in slots)
    tensor = np.zeros(shape)
    for monomial, value in controls.items():
        tensor[tuple(monomial[slot] for slot in slots)] = float(value)
    return tensor, slots, controls


def describe_negatives(tensor, slots):
    negative = np.argwhere(tensor < 0)
    print(
        "root", tensor.shape, "slots", slots, "negative", len(negative),
        "minimum", float(np.min(tensor)), "maximum", float(np.max(tensor)),
        flush=True,
    )
    if not len(negative):
        return
    for axis, slot in enumerate(slots):
        values, counts = np.unique(negative[:, axis], return_counts=True)
        histogram = ",".join(f"{int(value)}:{int(count)}" for value, count in zip(values, counts))
        print("negative_axis", axis, "slot", slot, histogram, flush=True)


def adaptive_search(root, slots, limit, max_depth):
    queue = deque([(root, (0,) * len(slots), (0.0,) * len(slots), (1.0,) * len(slots))])
    processed = closed = 0
    unresolved = []
    split_counts = [0] * len(slots)
    while queue and processed < limit:
        tensor, depths, lower, upper = queue.pop()
        processed += 1
        scale_value = max(1.0, float(np.max(np.abs(tensor))))
        tolerance = -1e-12 * scale_value
        if float(np.min(tensor)) >= tolerance:
            closed += 1
            continue
        if sum(depths) >= max_depth:
            unresolved.append((depths, lower, upper, float(np.min(tensor)) / scale_value))
            continue

        # Test each least-refined coordinate and choose the subdivision that
        # leaves the fewest negative controls.  Keep only the selected pair.
        minimum_depth = min(depths)
        eligible = [axis for axis in range(len(slots)) if depths[axis] <= minimum_depth + 1]
        best = None
        for axis in eligible:
            left, right = split_axis(tensor, axis)
            score = (
                int(np.sum(left < tolerance)) + int(np.sum(right < tolerance)),
                max(0.0, -float(np.min(left)) / scale_value)
                + max(0.0, -float(np.min(right)) / scale_value),
                depths[axis],
                axis,
            )
            if best is None or score < best[0]:
                best = (score, axis, left, right)
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
        if processed % 250 == 0:
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
    examples = [
        (depths, lower, upper, float(np.min(tensor)))
        for tensor, depths, lower, upper in list(queue)[-10:]
    ]
    print("queued_examples", examples, flush=True)
    print("unresolved_examples", unresolved[:10], flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", choices=("negative", "positive"), default="negative")
    parser.add_argument("--maximum", choices=tuple(MAXIMUM_SLOTS), default="a")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--max-depth", type=int, default=80)
    args = parser.parse_args()

    tensor, slots, controls = control_tensor(args.branch, MAXIMUM_SLOTS[args.maximum])
    describe_negatives(tensor, slots)
    print("nonzero_controls", len(controls), flush=True)
    if args.limit:
        adaptive_search(tensor, slots, args.limit, args.max_depth)


if __name__ == "__main__":
    main()
