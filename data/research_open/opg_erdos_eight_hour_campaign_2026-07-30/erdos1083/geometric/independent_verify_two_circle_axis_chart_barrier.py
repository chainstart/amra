#!/usr/bin/env python3
"""Independent checks for the concentric two-circle--axis barrier."""

from __future__ import annotations

import json
import math
from itertools import combinations


Point = tuple[float, float, float]


def _add(left: Point, right: Point) -> Point:
    return tuple(a + b for a, b in zip(left, right))


def _sub(left: Point, right: Point) -> Point:
    return tuple(a - b for a, b in zip(left, right))


def _scale(value: float, point: Point) -> Point:
    return tuple(value * coordinate for coordinate in point)


def _dot(left: Point, right: Point) -> float:
    return sum(a * b for a, b in zip(left, right))


def _norm_squared(point: Point) -> float:
    return _dot(point, point)


def _distance_key(left: Point, right: Point) -> float:
    return round(_norm_squared(_sub(left, right)), 9)


def _frame(alpha: float) -> tuple[Point, Point]:
    return (
        (math.cos(alpha), math.sin(alpha), 0.0),
        (-math.sin(alpha), math.cos(alpha), 0.0),
    )


def general_formula_residuals(
    *,
    alpha1: float,
    alpha2: float,
    A1: float,
    A2: float,
    w1: float,
    w2: float,
    r1: float,
    r2: float,
    phi: float,
    psi: float,
    y: float,
    z: float,
) -> tuple[float, float, float, float]:
    """Compare equations (3)--(6) with direct three-dimensional norms."""
    e1, f1 = _frame(alpha1)
    e2, f2 = _frame(alpha2)
    ez = (0.0, 0.0, 1.0)
    center1 = _add(_scale(A1, e1), _scale(w1, ez))
    center2 = _add(_scale(A2, e2), _scale(w2, ez))
    x1 = _add(_scale(math.cos(phi), e1), _scale(math.sin(phi), ez))
    x2 = _add(_scale(math.cos(psi), e2), _scale(math.sin(psi), ez))
    p1 = _add(center1, _scale(r1, x1))
    p2 = _add(center2, _scale(r2, x2))
    q1 = _add(center1, _scale(y, f1))
    q2 = _add(center2, _scale(z, f2))

    theta = alpha2 - alpha1
    cosine = math.cos(theta)
    sine = math.sin(theta)
    delta_w = w1 - w2
    base = A1 * A1 + A2 * A2 - 2 * cosine * A1 * A2 + delta_w**2

    formula_qq = (
        base
        + y * y
        + z * z
        - 2 * cosine * y * z
        - 2 * A2 * sine * y
        + 2 * A1 * sine * z
    )
    formula_pq = (
        base
        + r1 * r1
        + z * z
        + 2
        * r1
        * ((A1 - A2 * cosine) * math.cos(phi) + delta_w * math.sin(phi))
        + 2 * A1 * sine * z
        + 2 * r1 * sine * z * math.cos(phi)
    )
    formula_qp = (
        base
        + y * y
        + r2 * r2
        - 2 * A2 * sine * y
        - 2
        * r2
        * ((A1 * cosine - A2) * math.cos(psi) + delta_w * math.sin(psi))
        - 2 * r2 * sine * y * math.cos(psi)
    )
    formula_pp = (
        base
        + r1 * r1
        + r2 * r2
        + 2
        * r1
        * ((A1 - A2 * cosine) * math.cos(phi) + delta_w * math.sin(phi))
        - 2
        * r2
        * ((A1 * cosine - A2) * math.cos(psi) + delta_w * math.sin(psi))
        - 2
        * r1
        * r2
        * (
            cosine * math.cos(phi) * math.cos(psi)
            + math.sin(phi) * math.sin(psi)
        )
    )

    direct = (
        _norm_squared(_sub(q1, q2)),
        _norm_squared(_sub(p1, q2)),
        _norm_squared(_sub(q1, p2)),
        _norm_squared(_sub(p1, p2)),
    )
    formulas = (formula_qq, formula_pq, formula_qp, formula_pp)
    return tuple(abs(a - b) for a, b in zip(direct, formulas))


def _polygon(radius: float, order: int, center: float) -> tuple[Point, ...]:
    return tuple(
        (
            center + radius * math.cos(2 * math.pi * index / order),
            0.0,
            radius * math.sin(2 * math.pi * index / order),
        )
        for index in range(order)
    )


def _odd_indices(m: int) -> tuple[int, ...]:
    return tuple(range(-(2 * m - 1), 2 * m, 2))


def two_chart_ledger(order: int, m: int) -> dict[str, int]:
    if order < 3 or m < 1:
        raise ValueError("need order >= 3 and m >= 1")
    center = 4.0
    radii = (1.0, 2.0)
    height_step = 10.0
    sources = tuple(_polygon(radius, order, center) for radius in radii)
    targets = tuple(
        (center, height_step * index, 0.0) for index in _odd_indices(m)
    )
    floor_half = order // 2

    within_1 = {
        _distance_key(left, right) for left, right in combinations(sources[0], 2)
    }
    within_2 = {
        _distance_key(left, right) for left, right in combinations(sources[1], 2)
    }
    between_sources = {
        _distance_key(left, right) for left in sources[0] for right in sources[1]
    }
    axis_axis = {
        _distance_key(left, right) for left, right in combinations(targets, 2)
    }
    circle_axis = tuple(
        {
            _distance_key(source, target)
            for source in source_circle
            for target in targets
        }
        for source_circle in sources
    )

    if len(within_1) != floor_half or len(within_2) != floor_half:
        raise AssertionError("within-circle chord count failed")
    if len(between_sources) != floor_half + 1:
        raise AssertionError("between-circle distance count failed")
    if len(axis_axis) != 2 * m - 1:
        raise AssertionError("axis arithmetic-progression count failed")
    if tuple(map(len, circle_axis)) != (m, m):
        raise AssertionError("circle-axis label count failed")

    all_points = sources[0] + sources[1] + targets
    all_distances = {
        _distance_key(left, right) for left, right in combinations(all_points, 2)
    }
    upper_bound = 3 * floor_half + 4 * m
    if len(all_distances) > upper_bound:
        raise AssertionError("full union exceeds category upper bound")

    for radius in radii:
        normalized_constants = {
            round(
                center * center
                + (height_step * index) ** 2
                - (radius * radius + (height_step * index) ** 2),
                9,
            )
            for index in _odd_indices(m)
        }
        if normalized_constants != {center * center - radius * radius}:
            raise AssertionError("repeated reverse-circle equation failed")

    return {
        "order": order,
        "m": m,
        "within_circle_1": len(within_1),
        "within_circle_2": len(within_2),
        "between_circles": len(between_sources),
        "axis_axis": len(axis_axis),
        "circle_1_axis": len(circle_axis[0]),
        "circle_2_axis": len(circle_axis[1]),
        "distinct_distances": len(all_distances),
        "upper_bound": upper_bound,
        "representations": 4 * m * order,
        "multiplicity_per_chart": 2 * m,
    }


def k_chart_ledger(order: int, m: int, chart_count: int) -> dict[str, int]:
    if order < 3 or m < 1 or chart_count < 1:
        raise ValueError("invalid K-chart parameters")
    center = float(chart_count + 2)
    height_step = float(10 * (chart_count + 1))
    radii = tuple(float(index + 1) for index in range(chart_count))
    sources = tuple(_polygon(radius, order, center) for radius in radii)
    targets = tuple(
        (center, height_step * index, 0.0) for index in _odd_indices(m)
    )
    floor_half = order // 2
    within_counts = tuple(
        len(
            {
                _distance_key(left, right)
                for left, right in combinations(circle, 2)
            }
        )
        for circle in sources
    )
    between_counts = tuple(
        len(
            {
                _distance_key(left, right)
                for left in sources[first]
                for right in sources[second]
            }
        )
        for first, second in combinations(range(chart_count), 2)
    )
    circle_axis_counts = tuple(
        len(
            {
                _distance_key(source, target)
                for source in circle
                for target in targets
            }
        )
        for circle in sources
    )
    axis_axis_count = len(
        {
            _distance_key(left, right)
            for left, right in combinations(targets, 2)
        }
    )
    if within_counts != (floor_half,) * chart_count:
        raise AssertionError("K-chart within-circle ledger failed")
    if between_counts != (floor_half + 1,) * math.comb(chart_count, 2):
        raise AssertionError("K-chart between-circle ledger failed")
    if circle_axis_counts != (m,) * chart_count:
        raise AssertionError("K-chart circle-axis ledger failed")
    if axis_axis_count != 2 * m - 1:
        raise AssertionError("K-chart axis ledger failed")

    all_points = tuple(point for circle in sources for point in circle) + targets
    all_distances = {
        _distance_key(left, right) for left, right in combinations(all_points, 2)
    }
    explicit_upper = (
        chart_count * floor_half
        + math.comb(chart_count, 2) * (floor_half + 1)
        + (2 * m - 1)
        + chart_count * m
    )
    if len(all_distances) > explicit_upper:
        raise AssertionError("K-chart union exceeds explicit ledger")
    return {
        "order": order,
        "m": m,
        "chart_count": chart_count,
        "distinct_distances": len(all_distances),
        "explicit_upper_bound": explicit_upper,
        "within_source_blocks": sum(within_counts),
        "between_source_blocks": sum(between_counts),
        "axis_axis": axis_axis_count,
        "circle_axis_blocks": sum(circle_axis_counts),
        "representations": 2 * chart_count * m * order,
    }


def audit() -> dict[str, object]:
    parameter_sets = (
        (0.1, 0.9, 3.2, 1.7, -0.4, 0.8, 0.7, 1.1, 0.3, -0.6, 1.2, -0.9),
        (-0.7, 1.4, 2.5, -1.3, 1.1, -0.2, 1.3, 0.4, -1.0, 0.2, -0.5, 1.7),
        (1.2, -0.4, -2.1, 3.8, 0.0, 1.3, 0.8, 1.9, 2.0, -1.4, 0.6, 0.1),
    )
    maximum_residual = 0.0
    for values in parameter_sets:
        residuals = general_formula_residuals(
            alpha1=values[0],
            alpha2=values[1],
            A1=values[2],
            A2=values[3],
            w1=values[4],
            w2=values[5],
            r1=values[6],
            r2=values[7],
            phi=values[8],
            psi=values[9],
            y=values[10],
            z=values[11],
        )
        maximum_residual = max(maximum_residual, *residuals)
        if maximum_residual > 1e-10:
            raise AssertionError("general cross formula residual is too large")

    two_chart_cases = [
        two_chart_ledger(order, m)
        for order in range(3, 15)
        for m in range(1, 6)
    ]
    k_chart_cases = [
        k_chart_ledger(order, m, chart_count)
        for order in (3, 4, 7, 10)
        for m in (1, 3)
        for chart_count in range(1, 6)
    ]
    return {
        "schema": "amra.erdos1083.two-circle-axis-independent.v1",
        "status": "PASS",
        "general_formula_cases": len(parameter_sets),
        "maximum_formula_residual": maximum_residual,
        "two_chart_cases": len(two_chart_cases),
        "k_chart_cases": len(k_chart_cases),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
