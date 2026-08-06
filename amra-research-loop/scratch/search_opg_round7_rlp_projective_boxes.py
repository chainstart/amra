#!/usr/bin/env python3
"""Projective Bernstein discovery for the RLP outer-Gram factor H1884.

The separate compactification of c, q0, and q4 creates an artificial corner
where all three variables approach infinity at unrelated rates.  Instead write

    (c, q0, q4) = r * (direction),

cover the positive direction space by the three charts in which c, q0, or q4
is maximal, and compactify only r.  H1884 has total route degree 7 through 14,
so r**7 divides every chart and the remaining scale polynomial has degree 7.
"""

from __future__ import annotations

from collections import deque
from math import comb
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
from explore_opg_round7_rlp_tau import build  # noqa: E402
from search_opg_round7_rlp_bernstein_boxes import split_axis  # noqa: E402


ROUTES = (0, 1, 5)
SLOTS = (0, 1, 2, 5, 6, 7)
ROUTE_DEGREE_MIN = 7
ROUTE_DEGREE_MAX = 14


def compactify_scale(poly):
    """Substitute r=u/(1-u) after r**7 has been removed."""
    u = variable(0)
    one_minus_u = add(constant(1), u, -1)
    result = {}
    for monomial, value in poly.items():
        exponent = monomial[0]
        reduced = list(monomial)
        reduced[0] = 0
        term = {tuple(reduced): value}
        term = multiply(term, power(u, exponent))
        term = multiply(term, power(one_minus_u, 7 - exponent))
        result = add(result, term)
    return result


def reverse_slot(poly, slot):
    """Substitute x_slot=1-x_slot using a sparse binomial expansion."""
    result = {}
    for monomial, value in poly.items():
        exponent = monomial[slot]
        for degree in range(exponent + 1):
            reversed_monomial = list(monomial)
            reversed_monomial[slot] = degree
            key = tuple(reversed_monomial)
            result[key] = result.get(key, 0) + (
                value * (-1 if degree % 2 else 1) * comb(exponent, degree)
            )
    return {monomial: value for monomial, value in result.items() if value}


def local_corner(poly, maximum_slot):
    """Use distances from the unique unresolved projective corner."""
    result = compactify_scale(projective_chart(poly, maximum_slot))
    for slot in (0, 1, 2, 5, 7):
        result = reverse_slot(result, slot)
    return result


def projective_chart(poly, maximum_slot):
    """Return H1884/r**7 in a chart where ``maximum_slot`` equals r.

    The two remaining route ratios are stored in slots one and five.  Slot zero
    stores the scale r; the non-route variables retain their original slots.
    """
    assert maximum_slot in ROUTES
    ratio_routes = tuple(slot for slot in ROUTES if slot != maximum_slot)
    result = {}
    for monomial, value in poly.items():
        assert monomial[3] == monomial[4] == 0
        route_degree = sum(monomial[slot] for slot in ROUTES)
        assert ROUTE_DEGREE_MIN <= route_degree <= ROUTE_DEGREE_MAX
        projected = [0] * 8
        projected[0] = route_degree - ROUTE_DEGREE_MIN
        projected[1] = monomial[ratio_routes[0]]
        projected[5] = monomial[ratio_routes[1]]
        projected[2] = monomial[2]
        projected[6] = monomial[6]
        projected[7] = monomial[7]
        key = tuple(projected)
        result[key] = result.get(key, 0) + value
    return {monomial: value for monomial, value in result.items() if value}


def control_tensor(poly, maximum_slot):
    chart = projective_chart(poly, maximum_slot)
    compact = compactify_scale(chart)
    transformed = bernstein_transform(compact, list(SLOTS))
    shape = tuple(
        max(monomial[slot] for monomial in transformed) + 1 for slot in SLOTS
    )
    tensor = np.zeros(shape)
    for monomial, value in transformed.items():
        tensor[tuple(monomial[slot] for slot in SLOTS)] = float(value)
    return chart, compact, transformed, tensor


def in_local_corner(lower, upper):
    """Return whether a box lies in the analytically certified corner."""
    epsilon = 1e-12
    return all(
        (
            upper[axis] >= 1 - epsilon
            if side else lower[axis] <= epsilon
        )
        and upper[axis] - lower[axis] <= width + epsilon
        for axis, (width, side) in enumerate(zip(LOCAL_WIDTHS, LOCAL_SIDES))
    )


LOCAL_WIDTHS = (1 / 2, 1 / 128, 1 / 16, 1 / 2, 1 / 128, 1 / 32)
LOCAL_SIDES = (1, 1, 1, 1, 0, 1)


def intersects_local_corner(lower, upper):
    epsilon = 1e-12
    return all(
        upper[axis] > 1 - width + epsilon
        if side else lower[axis] < width - epsilon
        for axis, (width, side) in enumerate(zip(LOCAL_WIDTHS, LOCAL_SIDES))
    )


def unmet_local_axes(lower, upper):
    epsilon = 1e-12
    return [
        axis
        for axis, (width, side) in enumerate(zip(LOCAL_WIDTHS, LOCAL_SIDES))
        if (
            upper[axis] < 1 - epsilon
            or upper[axis] - lower[axis] > width + epsilon
            if side else (
                lower[axis] > epsilon
                or upper[axis] - lower[axis] > width + epsilon
            )
        )
    ]


def scan(root, limit=1000000, max_total_depth=84):
    queue = deque([(
        root,
        (0,) * len(SLOTS),
        (0.0,) * len(SLOTS),
        (1.0,) * len(SLOTS),
    )])
    closed = 0
    local_closed = 0
    unresolved = []
    processed = 0
    worst = (0.0, None)
    while queue and processed < limit:
        tensor, depths, lower, upper = queue.pop()
        processed += 1
        if in_local_corner(lower, upper):
            local_closed += 1
            continue
        scale = max(1.0, float(np.max(np.abs(tensor))))
        relative_minimum = float(np.min(tensor)) / scale
        if relative_minimum >= -1e-12:
            closed += 1
            continue
        if relative_minimum < worst[0]:
            worst = (relative_minimum, (depths, lower, upper))
        if sum(depths) >= max_total_depth:
            unresolved.append((depths, lower, upper, relative_minimum))
            continue
        # Balance refinements while preferring tau, shape variables, scale,
        # and finally the two projective direction ratios.
        priorities = (5, 2, 4, 0, 1, 3)
        axis = min(
            priorities,
            key=lambda candidate: (
                depths[candidate], priorities.index(candidate)
            ),
        )
        left, right = split_axis(tensor, axis)
        next_depths = list(depths)
        next_depths[axis] += 1
        middle = (lower[axis] + upper[axis]) / 2
        left_upper = list(upper)
        left_upper[axis] = middle
        right_lower = list(lower)
        right_lower[axis] = middle
        left_node = (left, tuple(next_depths), lower, tuple(left_upper))
        right_node = (right, tuple(next_depths), tuple(right_lower), upper)
        if intersects_local_corner(lower, upper) and LOCAL_SIDES[axis] == 0:
            queue.append(right_node)
            queue.append(left_node)
        else:
            queue.append(left_node)
            queue.append(right_node)
    return {
        "processed": processed,
        "closed": closed,
        "local_closed": local_closed,
        "queued": len(queue),
        "unresolved": unresolved,
        "worst": worst,
    }


def scan_greedy(root, limit=200000, max_total_depth=120):
    """Choose the split that leaves the fewest negative child controls."""
    queue = deque([(
        root,
        (0,) * len(SLOTS),
        (0.0,) * len(SLOTS),
        (1.0,) * len(SLOTS),
    )])
    closed = 0
    local_closed = 0
    unresolved = []
    processed = 0
    axis_counts = [0] * len(SLOTS)
    while queue and processed < limit:
        tensor, depths, lower, upper = queue.pop()
        processed += 1
        if in_local_corner(lower, upper):
            local_closed += 1
            continue
        scale = max(1.0, float(np.max(np.abs(tensor))))
        tolerance = -1e-12 * scale
        if np.min(tensor) >= tolerance:
            closed += 1
            continue
        if sum(depths) >= max_total_depth:
            unresolved.append((depths, lower, upper, float(np.min(tensor)) / scale))
            continue
        choices = []
        minimum_depth = min(depths)
        eligible_axes = [
            axis for axis in range(len(SLOTS))
            if depths[axis] <= minimum_depth + 2
            and (lower[axis] + upper[axis]) / 2 not in (lower[axis], upper[axis])
        ]
        for axis in eligible_axes:
            left, right = split_axis(tensor, axis)
            children = (left, right)
            open_children = 0
            negative_controls = 0
            severity = 0.0
            for child in children:
                child_scale = max(1.0, float(np.max(np.abs(child))))
                child_tolerance = -1e-12 * child_scale
                child_minimum = float(np.min(child))
                if child_minimum < child_tolerance:
                    open_children += 1
                    negative_controls += int(np.sum(child < child_tolerance))
                    severity += -child_minimum / child_scale
            choices.append((
                (open_children, negative_controls, severity, depths[axis], axis),
                axis,
                left,
                right,
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
        left_node = (left, tuple(next_depths), lower, tuple(left_upper))
        right_node = (right, tuple(next_depths), tuple(right_lower), upper)
        if intersects_local_corner(lower, upper) and LOCAL_SIDES[axis] == 0:
            queue.append(right_node)
            queue.append(left_node)
        else:
            queue.append(left_node)
            queue.append(right_node)
    return {
        "processed": processed,
        "closed": closed,
        "local_closed": local_closed,
        "queued": len(queue),
        "queued_examples": [
            (depths, lower, upper, float(np.min(tensor)))
            for tensor, depths, lower, upper in list(queue)[-10:]
        ],
        "unresolved": unresolved,
        "axis_counts": axis_counts,
    }


def scan_targeted(root, limit=500000, max_total_depth=120):
    """Drive the singular branch into the anisotropic analytic corner."""
    queue = deque([(
        root,
        (0,) * len(SLOTS),
        (0.0,) * len(SLOTS),
        (1.0,) * len(SLOTS),
    )])
    closed = local_closed = processed = 0
    unresolved = []
    axis_counts = [0] * len(SLOTS)
    while queue and processed < limit:
        tensor, depths, lower, upper = queue.pop()
        processed += 1
        if in_local_corner(lower, upper):
            local_closed += 1
            continue
        scale = max(1.0, float(np.max(np.abs(tensor))))
        tolerance = -1e-12 * scale
        if np.min(tensor) >= tolerance:
            closed += 1
            continue
        if sum(depths) >= max_total_depth:
            unresolved.append((depths, lower, upper, float(np.min(tensor)) / scale))
            continue
        if intersects_local_corner(lower, upper):
            eligible_axes = unmet_local_axes(lower, upper)
        else:
            priorities = (5, 2, 4, 0, 1, 3)
            minimum_depth = min(depths)
            eligible_axes = [
                axis for axis in priorities if depths[axis] <= minimum_depth + 2
            ]
        choices = []
        for axis in eligible_axes:
            left, right = split_axis(tensor, axis)
            score = []
            for child in (left, right):
                child_scale = max(1.0, float(np.max(np.abs(child))))
                child_tolerance = -1e-12 * child_scale
                child_minimum = float(np.min(child))
                score.append((
                    child_minimum < child_tolerance,
                    int(np.sum(child < child_tolerance)),
                    max(0.0, -child_minimum / child_scale),
                ))
            choices.append((
                (sum(item[0] for item in score), sum(item[1] for item in score),
                 sum(item[2] for item in score), depths[axis], axis),
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
        left_node = (left, tuple(next_depths), lower, tuple(left_upper))
        right_node = (right, tuple(next_depths), tuple(right_lower), upper)
        if intersects_local_corner(lower, upper) and LOCAL_SIDES[axis] == 0:
            queue.append(right_node)
            queue.append(left_node)
        else:
            queue.append(left_node)
            queue.append(right_node)
    return {
        "processed": processed,
        "closed": closed,
        "local_closed": local_closed,
        "queued": len(queue),
        "queued_examples": [
            (depths, lower, upper, float(np.min(tensor)))
            for tensor, depths, lower, upper in list(queue)[-10:]
        ],
        "unresolved": unresolved,
        "axis_counts": axis_counts,
    }


def main():
    poly = build()[0]
    route_degrees = [sum(monomial[slot] for slot in ROUTES) for monomial in poly]
    assert min(route_degrees) == ROUTE_DEGREE_MIN
    assert max(route_degrees) == ROUTE_DEGREE_MAX
    for maximum_slot, name in ((0, "c"), (1, "q0"), (5, "q4")):
        chart, compact, transformed, tensor = control_tensor(poly, maximum_slot)
        exact_minimum = min(transformed.values())
        negative = sum(value < 0 for value in transformed.values())
        print(
            name,
            "chart_terms", len(chart),
            "compact_terms", len(compact),
            "bernstein_terms", len(transformed),
            "shape", tensor.shape,
            "negative", negative,
            "minimum", exact_minimum,
        )
        result = scan(tensor)
        print(
            name,
            "processed", result["processed"],
            "closed", result["closed"],
            "local_closed", result["local_closed"],
            "queued", result["queued"],
            "unresolved", len(result["unresolved"]),
            "worst", result["worst"],
        )
        print(name, "examples", result["unresolved"][:10])


if __name__ == "__main__":
    main()
