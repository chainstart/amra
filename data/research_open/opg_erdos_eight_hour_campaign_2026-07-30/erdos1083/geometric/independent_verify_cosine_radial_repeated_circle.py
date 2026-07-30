#!/usr/bin/env python3
"""Independent checks for the cosine--radial repeated-circle barrier."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction


def normal_form_certificate(
    transverse: tuple[int, ...],
    A: int = 5,
    w0: int = 2,
    C: int = 9,
) -> dict[str, int]:
    if len(set(transverse)) != len(transverse):
        raise ValueError("transverse coordinates must be distinct")
    if A == 0:
        raise ValueError("A must be nonzero")

    radius_squared = A * A - C
    if radius_squared < 0:
        raise ValueError("the common circle must be real")

    ordinary_radius_squares = {
        A * A + value * value for value in transverse
    }
    labels = {
        A * A + value * value - C for value in transverse
    }
    if ordinary_radius_squares != {
        label + C for label in labels
    }:
        raise AssertionError("radius/label translation failed")

    target_distance_squares = {
        (left - right) ** 2
        for left, right in itertools.combinations(transverse, 2)
    }
    lower = max(0, len(transverse) - 1)
    if len(target_distance_squares) < lower:
        raise AssertionError("collinear distance lower bound failed")

    # Check the complete-bipartite distance identity on rational points
    # from the circle whenever the radius permits easy axis points.
    source_points = (
        (A + math.isqrt(radius_squared), w0),
        (A - math.isqrt(radius_squared), w0),
    )
    if math.isqrt(radius_squared) ** 2 == radius_squared:
        for u, z in source_points:
            for value in transverse:
                distance = (
                    (u - A) ** 2
                    + (z - w0) ** 2
                    + value * value
                )
                label = A * A + value * value - C
                if distance != label:
                    raise AssertionError("cross-distance identity failed")

    return {
        "multiplicity": len(transverse),
        "common_circle_radius_squared": radius_squared,
        "distinct_plane_slopes": len(
            {Fraction(value, A) for value in transverse}
        ),
        "ordinary_radii": len(ordinary_radius_squares),
        "distance_labels": len(labels),
        "target_distances": len(target_distance_squares),
        "radius_label_lower_bound": (
            (len(transverse) + 1) // 2
        ),
        "collinear_lower_bound": lower,
    }


def saturation_ledger(n: int, m: int) -> dict[str, int]:
    if n < 3 or m < 1:
        raise ValueError("need n >= 3 and m >= 1")

    odd_indices = tuple(
        range(-(2 * m - 1), 2 * m, 2)
    )
    if len(odd_indices) != 2 * m:
        raise AssertionError("odd progression size failed")

    target_differences = {
        abs(left - right) // 2
        for left, right in itertools.combinations(
            odd_indices, 2
        )
    }
    cross_label_keys = {value * value for value in odd_indices}
    source_chord_steps = {
        min(step, n - step) for step in range(1, n)
    }

    if source_chord_steps != set(
        range(1, n // 2 + 1)
    ):
        raise AssertionError("regular polygon chord ledger failed")
    if target_differences != set(range(1, 2 * m)):
        raise AssertionError("target AP distance ledger failed")
    if len(cross_label_keys) != m:
        raise AssertionError("cross-label ledger failed")

    upper = n // 2 + 3 * m - 1
    return {
        "n": n,
        "m": m,
        "multiplicity": 2 * m,
        "source_source_distances": len(source_chord_steps),
        "target_target_distances": len(target_differences),
        "cross_distances": len(cross_label_keys),
        "distance_union_upper_bound": upper,
        "cross_representations": 2 * m * n,
        "target_rays": 2 * m,
        "full_configuration_rays": 2 * m + 1,
        "target_radial_overlap": 2 * m,
    }


def direct_coordinate_check(
    n: int,
    m: int,
    a: float = 5.0,
    r: float = 2.0,
    h: float = 3.0,
) -> int:
    """Numerically enumerate the full configuration as an extra audit."""

    source = tuple(
        (
            a + r * math.cos(2 * math.pi * index / n),
            0.0,
            r * math.sin(2 * math.pi * index / n),
        )
        for index in range(n)
    )
    odd = tuple(range(-(2 * m - 1), 2 * m, 2))
    target = tuple((a, h * value, 0.0) for value in odd)
    points = source + target
    distances = {
        round(
            sum(
                (left[coordinate] - right[coordinate]) ** 2
                for coordinate in range(3)
            ),
            9,
        )
        for left, right in itertools.combinations(points, 2)
    }
    bound = saturation_ledger(n, m)[
        "distance_union_upper_bound"
    ]
    if len(distances) > bound:
        raise AssertionError("direct full-distance bound failed")

    # Every source-target distance depends only on |j|.
    cross = {
        round(
            sum(
                (left[coordinate] - right[coordinate]) ** 2
                for coordinate in range(3)
            ),
            9,
        )
        for left in source
        for right in target
    }
    if len(cross) != m:
        raise AssertionError("direct cross-distance count failed")
    return len(distances)


def audit() -> dict[str, object]:
    normal_records = []
    for size in range(2, 13):
        half = size // 2
        transverse = (
            tuple(range(-half, 0)) + tuple(range(1, half + 1))
            if size % 2 == 0
            else tuple(range(-half, 0)) + tuple(range(1, half + 2))
        )
        record = normal_form_certificate(transverse)
        if record["ordinary_radii"] < (size + 1) // 2:
            raise AssertionError("radius lower bound failed")
        if record["distance_labels"] < (size + 1) // 2:
            raise AssertionError("label lower bound failed")
        normal_records.append(record)

    saturation_records = []
    coordinate_checks = 0
    for n in range(3, 16):
        for m in range(1, 7):
            record = saturation_ledger(n, m)
            actual = direct_coordinate_check(n, m)
            record["direct_distinct_distances"] = actual
            saturation_records.append(record)
            coordinate_checks += 1

    return {
        "schema": "amra.erdos1083.cosine-radial-independent.v1",
        "status": "PASS",
        "normal_form_records": normal_records,
        "saturation_records": saturation_records,
        "normal_form_checks": len(normal_records),
        "full_coordinate_checks": coordinate_checks,
        "subsystem_qualification": (
            "target rays = 2m; full configuration rays = 2m+1"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()
    print(json.dumps(audit(), indent=args.indent, sort_keys=True))


if __name__ == "__main__":
    main()
