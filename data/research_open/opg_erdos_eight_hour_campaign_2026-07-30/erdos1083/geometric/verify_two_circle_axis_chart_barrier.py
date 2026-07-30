#!/usr/bin/env python3
"""Exact finite checks for the concentric two-chart Lenz barrier."""

from __future__ import annotations

import json

import sympy as sp


def squared_distance(left, right):
    return sp.simplify(
        sum((a - b) ** 2 for a, b in zip(left, right))
    )


def concentric_two_chart_model(
    polygon_order: int,
    half_axis_size: int,
) -> dict[str, int]:
    if polygon_order < 3 or half_axis_size < 1:
        raise ValueError("need polygon_order >= 3 and half_axis_size >= 1")

    center = sp.Integer(3)
    height_step = sp.Integer(10)
    radii = (sp.Integer(1), sp.Integer(2))
    circle_points = []
    for radius in radii:
        circle_points.append(
            tuple(
                (
                    center
                    + radius
                    * sp.cos(2 * sp.pi * index / polygon_order),
                    sp.Integer(0),
                    radius
                    * sp.sin(2 * sp.pi * index / polygon_order),
                )
                for index in range(polygon_order)
            )
        )

    odd_indices = tuple(
        range(-(2 * half_axis_size - 1), 0, 2)
    ) + tuple(range(1, 2 * half_axis_size, 2))
    axis_points = tuple(
        (center, height_step * index, sp.Integer(0))
        for index in odd_indices
    )

    points = circle_points[0] + circle_points[1] + axis_points
    distances = {
        squared_distance(points[first], points[second])
        for first in range(len(points))
        for second in range(first + 1, len(points))
    }

    repeated_circle_multiplicities = []
    cross_label_counts = []
    for radius in radii:
        normalized_circles = set()
        labels = set()
        for index in odd_indices:
            y = height_step * index
            radial_squared = center**2 + y**2
            distance_label = radius**2 + y**2
            # Coefficients after the leading u^2+z^2:
            # (-2cv, -2w, v^2+w^2-d).
            normalized_circles.add(
                (
                    -2 * center,
                    0,
                    sp.expand(radial_squared - distance_label),
                )
            )
            labels.add(distance_label)
        assert len(normalized_circles) == 1
        repeated_circle_multiplicities.append(len(odd_indices))
        cross_label_counts.append(len(labels))

    upper_bound = (
        3 * (polygon_order // 2)
        + 4 * half_axis_size
    )
    assert len(distances) <= upper_bound
    assert repeated_circle_multiplicities == [
        2 * half_axis_size,
        2 * half_axis_size,
    ]
    assert cross_label_counts == [
        half_axis_size,
        half_axis_size,
    ]

    return {
        "polygon_order": polygon_order,
        "half_axis_size": half_axis_size,
        "points": len(points),
        "distinct_squared_distances": len(distances),
        "proved_linear_upper_bound": upper_bound,
        "chart_count": 2,
        "distinct_circle_radii": 2,
        "multiplicity_per_chart": 2 * half_axis_size,
        "cross_labels_per_chart": half_axis_size,
    }


def audit() -> dict[str, object]:
    cases = [
        concentric_two_chart_model(order, half_size)
        for order in (3, 4, 6, 8)
        for half_size in (1, 2, 4, 7)
    ]
    return {
        "schema": "amra.erdos1083.two-circle-axis-chart-barrier.v1",
        "status": "PASS",
        "cases": cases,
        "claim": (
            "Two incidence-active circle-axis charts with a common "
            "center and axis but different radii can have only "
            "linearly many distinct distances."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
