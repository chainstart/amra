#!/usr/bin/env python3
"""Float discovery for an exact adaptive Bernstein box certificate of H1884."""

from __future__ import annotations

from collections import deque
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from explore_opg_round7_m88 import substitute_slot  # noqa: E402
from explore_opg_round7_rlp_tau import build  # noqa: E402


SLOTS = (0, 1, 2, 5, 6, 7)


def compactify(poly, slot):
    degree = max(monomial[slot] for monomial in poly)
    coordinate = variable(slot)
    complement = add(constant(1), coordinate, -1)
    result = {}
    for monomial, value in poly.items():
        exponent = monomial[slot]
        reduced = list(monomial)
        reduced[slot] = 0
        term = {tuple(reduced): value}
        term = multiply(term, power(coordinate, exponent))
        term = multiply(term, power(complement, degree - exponent))
        result = add(result, term)
    return result


def control_tensor():
    poly = build()[0]
    for slot in (0, 1, 5):
        poly = compactify(poly, slot)
    transformed = bernstein_transform(poly, list(SLOTS))
    shape = tuple(max(monomial[slot] for monomial in transformed) + 1 for slot in SLOTS)
    tensor = np.zeros(shape)
    for monomial, value in transformed.items():
        tensor[tuple(monomial[slot] for slot in SLOTS)] = float(value)
    return tensor


def split_axis(tensor, axis):
    work = np.moveaxis(tensor, axis, 0)
    degree = work.shape[0] - 1
    levels = [work]
    for _ in range(degree):
        levels.append((levels[-1][:-1] + levels[-1][1:]) / 2)
    left = np.stack([levels[index][0] for index in range(degree + 1)])
    right = np.stack([levels[degree - index][index] for index in range(degree + 1)])
    return np.moveaxis(left, 0, axis), np.moveaxis(right, 0, axis)


def main():
    root = control_tensor()
    queue = deque([(
        root,
        (0,) * len(SLOTS),
        (0.0,) * len(SLOTS),
        (1.0,) * len(SLOTS),
    )])
    closed = 0
    unresolved = []
    processed = 0
    while queue and processed < 200000:
        tensor, depths, lower, upper = queue.pop()
        processed += 1
        scale = max(1.0, float(np.max(np.abs(tensor))))
        if np.min(tensor) >= -1e-12 * scale:
            closed += 1
            continue
        if sum(depths) >= 48:
            unresolved.append((depths, lower, upper, float(np.min(tensor)) / scale))
            continue
        # Split a least-refined variable; ties prefer tau, then the activities.
        priorities = (5, 2, 4, 0, 1, 3)
        axis = min(priorities, key=lambda candidate: (depths[candidate], priorities.index(candidate)))
        left, right = split_axis(tensor, axis)
        next_depths = list(depths)
        next_depths[axis] += 1
        middle = (lower[axis] + upper[axis]) / 2
        left_upper = list(upper)
        left_upper[axis] = middle
        right_lower = list(lower)
        right_lower[axis] = middle
        queue.append((left, tuple(next_depths), lower, tuple(left_upper)))
        queue.append((right, tuple(next_depths), tuple(right_lower), upper))
    print(
        "processed", processed,
        "closed", closed,
        "queued", len(queue),
        "unresolved", len(unresolved),
    )
    print("examples", unresolved[:20])


if __name__ == "__main__":
    main()
