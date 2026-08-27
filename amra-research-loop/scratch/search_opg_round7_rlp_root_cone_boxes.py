#!/usr/bin/env python3
"""Float adaptive q0-projective boxes using the exact RLP root cone.

The companion exact certificate closes

    1-u <= B*v*(1-tau), 1-A<=1/128, v<=1/128, 1-tau<=1/32.

This discovery scan asks whether ordinary Bernstein subdivision closes the
complement.  It is deliberately float-only; any finite tree found here must
later be replayed with exact rational controls.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from search_opg_round7_rlp_projective_boxes import (  # noqa: E402
    build,
    control_tensor,
    split_axis,
)


AXES = ("u", "A", "s0", "B", "v", "tau")


def root_closed(lower, upper, epsilon=1e-15):
    x_max = 1.0 - lower[0]
    product_min = lower[3] * lower[4] * (1.0 - upper[5])
    return (
        lower[1] >= 1.0 - 1.0 / 128.0 - epsilon
        and upper[4] <= 1.0 / 128.0 + epsilon
        and lower[5] >= 1.0 - 1.0 / 32.0 - epsilon
        and x_max <= product_min + epsilon
    )


def root_intersects(lower, upper, epsilon=1e-15):
    x_min = 1.0 - upper[0]
    product_max = upper[3] * min(upper[4], 1.0 / 128.0) * min(
        1.0 - lower[5], 1.0 / 32.0
    )
    return (
        upper[1] >= 1.0 - 1.0 / 128.0 - epsilon
        and lower[4] <= 1.0 / 128.0 + epsilon
        and upper[5] >= 1.0 - 1.0 / 32.0 - epsilon
        and x_min <= product_max + epsilon
    )


def split_node(tensor, depths, lower, upper, axis):
    left, right = split_axis(tensor, axis)
    next_depths = list(depths)
    next_depths[axis] += 1
    middle = (lower[axis] + upper[axis]) / 2.0
    left_upper = list(upper)
    left_upper[axis] = middle
    right_lower = list(lower)
    right_lower[axis] = middle
    return (
        (left, tuple(next_depths), lower, tuple(left_upper)),
        (right, tuple(next_depths), tuple(right_lower), upper),
    )


def child_score(node):
    tensor, _, lower, upper = node
    if root_closed(lower, upper):
        return (0, 0, 0.0)
    scale = max(1.0, float(np.max(np.abs(tensor))))
    minimum = float(np.min(tensor))
    tolerance = -2e-12 * scale
    if minimum >= tolerance:
        return (0, 0, 0.0)
    return (
        1,
        int(np.sum(tensor < tolerance)),
        -minimum / scale,
    )


def choose_axis(tensor, depths, lower, upper):
    candidates = []
    intersects = root_intersects(lower, upper)
    minimum_depth = min(depths)
    for axis in range(len(AXES)):
        middle = (lower[axis] + upper[axis]) / 2.0
        if middle in (lower[axis], upper[axis]):
            continue
        children = split_node(tensor, depths, lower, upper, axis)
        scores = [child_score(child) for child in children]
        open_children = sum(score[0] for score in scores)
        negatives = sum(score[1] for score in scores)
        severity = sum(score[2] for score in scores)

        # Near the root cone, permit anisotropic refinement and prefer axes
        # that improve membership in the exact product inequality.  Elsewhere
        # keep depths roughly balanced to avoid pathological skinny boxes.
        depth_penalty = 0 if intersects else max(0, depths[axis] - minimum_depth - 2)
        cone_priority = (0, 1, 4, 5, 3, 2).index(axis) if intersects else axis
        candidates.append((
            (open_children, negatives, severity, depth_penalty,
             depths[axis], cone_priority),
            axis,
            children,
        ))
    _, axis, children = min(candidates, key=lambda item: item[0])
    return axis, children


def scan(root, limit=200_000, max_total_depth=220):
    queue = deque([(
        root,
        (0,) * len(AXES),
        (0.0,) * len(AXES),
        (1.0,) * len(AXES),
    )])
    processed = direct_closed = root_cone_closed = 0
    axis_counts = [0] * len(AXES)
    unresolved = []
    worst = (0.0, None)
    while queue and processed < limit:
        tensor, depths, lower, upper = queue.pop()
        processed += 1
        if root_closed(lower, upper):
            root_cone_closed += 1
            continue
        scale = max(1.0, float(np.max(np.abs(tensor))))
        minimum = float(np.min(tensor))
        relative = minimum / scale
        if relative >= -2e-12:
            direct_closed += 1
            continue
        if relative < worst[0]:
            worst = (relative, (depths, lower, upper))
        if sum(depths) >= max_total_depth:
            unresolved.append((depths, lower, upper, relative))
            continue
        axis, children = choose_axis(tensor, depths, lower, upper)
        axis_counts[axis] += 1
        # Push the child closer to the root corner last so it is processed
        # first under LIFO order.
        ordered = sorted(
            children,
            key=lambda node: root_intersects(node[2], node[3]),
        )
        queue.extend(ordered)
        if processed % 50_000 == 0:
            print(
                "progress", processed, "queue", len(queue),
                "direct", direct_closed, "root", root_cone_closed,
                "unresolved", len(unresolved),
                flush=True,
            )
    return {
        "processed": processed,
        "direct_closed": direct_closed,
        "root_cone_closed": root_cone_closed,
        "queued": len(queue),
        "unresolved": unresolved,
        "axis_counts": dict(zip(AXES, axis_counts)),
        "worst": worst,
        "queued_examples": [
            (depths, lower, upper, float(np.min(tensor)))
            for tensor, depths, lower, upper in list(queue)[-10:]
        ],
    }


def main():
    polynomial = build()[0]
    _, _, _, tensor = control_tensor(polynomial, 1)
    print("root", tensor.shape, "negative", int(np.sum(tensor < 0)), flush=True)
    result = scan(tensor)
    for key, value in result.items():
        if key not in ("unresolved", "queued_examples"):
            print(key, value, flush=True)
    print("unresolved_examples", result["unresolved"][:10], flush=True)
    print("queued_examples", result["queued_examples"], flush=True)


if __name__ == "__main__":
    main()
