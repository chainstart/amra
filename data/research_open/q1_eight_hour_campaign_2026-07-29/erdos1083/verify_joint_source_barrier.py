#!/usr/bin/env python3
"""Stress-test a tempting joint source/rotation inequality for #1083.

The coplanar-axis branch of the inherited reflection argument naturally
suggests bounding

    sum_alpha q_alpha r_alpha,

where q_alpha counts points on a mirror plane through a fixed axis and
r_alpha counts pairs carried by the corresponding axial rotation.

The dihedral product model used here is not a counterexample to the original
distinct-distance conjecture.  It is a falsification test for any proposed
bound that ignores the distance-set size: the joint moment is quadratic in
the number of points, so a useful theorem has to spend global distance
information, not only mirror and rotation incidences.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Result:
    polygon_size: int
    layers: int
    points: int
    mirror_count: int
    min_fixed_points: int
    max_fixed_points: int
    rotation_success: int
    joint_moment: int
    numerical_distance_count: int
    joint_over_n_squared: float
    joint_over_nD: float


def distance_count(m: int, c: int) -> int:
    """Count squared-distance values in a unit m-gon times c integer layers.

    Values are evaluated at high ordinary floating precision and rounded.
    The output is only a stress-test diagnostic, not a formal algebraic
    distinctness certificate.
    """

    horizontal = [2.0 - 2.0 * math.cos(2.0 * math.pi * k / m) for k in range(m // 2 + 1)]
    vertical = [float(k * k) for k in range(c)]
    return len({round(x + y, 12) for x in horizontal for y in vertical} - {0.0})


def run(m: int, c: int) -> Result:
    if m < 3 or c < 1:
        raise ValueError("need polygon_size >= 3 and layers >= 1")

    # The full dihedral group has m reflection axes.  For odd m every axis
    # fixes one vertex per layer; for even m, half fix two and half fix none.
    fixed_counts = []
    for j in range(m):
        if m % 2:
            fixed_counts.append(c)
        else:
            fixed_counts.append(2 * c if j % 2 == 0 else 0)

    n = m * c
    # Every associated dihedral rotation preserves the full product set.
    r = n
    joint = sum(q * r for q in fixed_counts)
    D = distance_count(m, c)
    return Result(
        polygon_size=m,
        layers=c,
        points=n,
        mirror_count=m,
        min_fixed_points=min(fixed_counts),
        max_fixed_points=max(fixed_counts),
        rotation_success=r,
        joint_moment=joint,
        numerical_distance_count=D,
        joint_over_n_squared=joint / (n * n),
        joint_over_nD=joint / (n * D),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--polygon-size", type=int, default=31)
    parser.add_argument("--layers", type=int, default=47)
    args = parser.parse_args()
    print(json.dumps(asdict(run(args.polygon_size, args.layers)), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
