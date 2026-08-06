#!/usr/bin/env python3
"""Float discovery for a coefficientwise conditional PNL box certificate."""

from __future__ import annotations

from collections import deque
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_negative_q3_odds_chart import cleared_polynomial  # noqa: E402
from verify_negative_c_direct_chambers import bernstein_transform  # noqa: E402
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    build_delta,
    common_monomial,
    divide_monomial,
    gram,
    scale,
)
from verify_opposite_nonshared_chambers import divide_one_minus_variable  # noqa: E402


ROUTE_SLOTS = (0, 1, 5)
BOX_SLOTS = (2, 4, 6)


def normalized_pair():
    delta, _, _ = build_delta()
    cleared = cleared_polynomial(delta, "PNL")
    core = divide_monomial(cleared, common_monomial(cleared))
    _, b1, _, determinant = gram(core, 7)

    J = divide_monomial(b1, (1, 0, 0, 0, 0, 0, 0, 0))
    J = divide_one_minus_variable(J, 2)
    J = divide_one_minus_variable(J, 6)
    J = scale(J, -2)

    R = divide_monomial(determinant, (2, 0, 0, 0, 0, 0, 0, 0))
    for slot in (2, 2, 4, 4, 6, 6):
        R = divide_one_minus_variable(R, slot)
    R = scale(R, 4)
    return J, R


def grouped_tensor(poly):
    transformed = bernstein_transform(poly, list(BOX_SLOTS))
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
            tuple(monomial[slot] for slot in ROUTE_SLOTS),
            route_shape,
        )
        tensor[(route_index,) + tuple(monomial[slot] for slot in BOX_SLOTS)] = float(value)
    return tensor, route_shape


def split_axis(tensor, axis):
    # Axis zero indexes route monomials and is never split.
    work = np.moveaxis(tensor, axis + 1, 0)
    degree = work.shape[0] - 1
    levels = [work]
    for _ in range(degree):
        levels.append((levels[-1][:-1] + levels[-1][1:]) / 2)
    left = np.stack([levels[index][0] for index in range(degree + 1)])
    right = np.stack([levels[degree - index][index] for index in range(degree + 1)])
    return np.moveaxis(left, 0, axis + 1), np.moveaxis(right, 0, axis + 1)


def main():
    J, R = normalized_pair()
    J_root, J_route_shape = grouped_tensor(J)
    R_root, R_route_shape = grouped_tensor(R)
    print(
        "root",
        "J", J_root.shape, J_route_shape, float(np.max(J_root)),
        "R", R_root.shape, R_route_shape, float(np.min(R_root)),
        flush=True,
    )

    queue = deque([(
        J_root,
        R_root,
        (0, 0, 0),
        (0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0),
    )])
    processed = 0
    j_closed = 0
    r_closed = 0
    unresolved = []
    max_boxes = 200_000
    while queue and processed < max_boxes:
        J_box, R_box, depths, lower, upper = queue.pop()
        processed += 1
        J_scale = max(1.0, float(np.max(np.abs(J_box))))
        R_scale = max(1.0, float(np.max(np.abs(R_box))))
        if float(np.max(J_box)) <= 1e-12 * J_scale:
            j_closed += 1
            continue
        if float(np.min(R_box)) >= -1e-12 * R_scale:
            r_closed += 1
            continue
        if sum(depths) >= 60:
            unresolved.append((
                depths,
                lower,
                upper,
                float(np.max(J_box)) / J_scale,
                float(np.min(R_box)) / R_scale,
            ))
            continue

        # Prefer s3, then s0, then s4 among the least-refined coordinates.
        priorities = (1, 0, 2)
        axis = min(
            priorities,
            key=lambda candidate: (depths[candidate], priorities.index(candidate)),
        )
        J_halves = split_axis(J_box, axis)
        R_halves = split_axis(R_box, axis)
        next_depths = list(depths)
        next_depths[axis] += 1
        middle = (lower[axis] + upper[axis]) / 2
        left_upper = list(upper)
        left_upper[axis] = middle
        right_lower = list(lower)
        right_lower[axis] = middle
        queue.append((
            J_halves[0], R_halves[0], tuple(next_depths), lower, tuple(left_upper)
        ))
        queue.append((
            J_halves[1], R_halves[1], tuple(next_depths), tuple(right_lower), upper
        ))
        if processed % 10_000 == 0:
            print(
                "progress", processed, "queued", len(queue),
                "j", j_closed, "r", r_closed, "unresolved", len(unresolved),
                flush=True,
            )

    print(
        "done", processed, "queued", len(queue),
        "j", j_closed, "r", r_closed, "unresolved", len(unresolved),
        flush=True,
    )
    print("examples", unresolved[:20], flush=True)


if __name__ == "__main__":
    main()
