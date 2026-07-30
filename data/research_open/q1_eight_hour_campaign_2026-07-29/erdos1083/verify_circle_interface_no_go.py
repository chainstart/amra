#!/usr/bin/env python3
"""Exact stress test for the fixed-axis circular-fibre interface.

The construction is deliberately *local*: it realizes the exact angular
quantities q_alpha and r_alpha from (4.37j), as well as every capacity used
before cross-fibre distances enter.  It is not asserted to have few global
Euclidean distances.  Its purpose is to prove that a useful next lemma must
use cross-fibre distance information.

For an integer t >= 3 set

    fibre count F = t^3,
    angular progression length S = t^2,
    active angles M = t,
    total mass N = F*S = t^5,
    critical distance parameter D = t^3.

On every circular fibre use the angular set

    A = {0, theta, ..., (S-1) theta},

where theta/pi is irrational.  At alpha_j = j theta, 1 <= j <= M,
the source plane contains one point of every fibre, while rotation through
2 alpha_j has S-2j successes on every fibre.  All counts below are integer
index counts and therefore do not use floating point.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ActiveAngle:
    index: int
    source_count: int
    rotation_success: int


@dataclass(frozen=True)
class Result:
    scale: int
    points: int
    fibre_count: int
    fibre_size: int
    active_angle_count: int
    critical_distance_parameter: int
    per_fibre_chord_labels: int
    min_source_count: int
    min_rotation_success: int
    generic_cylinder_distance_count: int
    source_incidence_sum: int
    rotation_success_sum: int
    active_joint_moment: int
    joint_over_nD: float
    min_success_over_n: float


def active_angles(t: int) -> tuple[ActiveAngle, ...]:
    if t < 3:
        raise ValueError("need scale >= 3")

    fibres = t**3
    fibre_size = t**2
    return tuple(
        ActiveAngle(
            index=j,
            source_count=fibres,
            rotation_success=fibres * (fibre_size - 2 * j),
        )
        for j in range(1, t + 1)
    )


def run(t: int) -> Result:
    angles = active_angles(t)
    fibres = t**3
    fibre_size = t**2
    n = fibres * fibre_size
    critical_D = t**3
    joint = sum(item.source_count * item.rotation_success for item in angles)
    source_sum = sum(item.source_count for item in angles)
    success_sum = sum(item.rotation_success for item in angles)
    return Result(
        scale=t,
        points=n,
        fibre_count=fibres,
        fibre_size=fibre_size,
        active_angle_count=t,
        critical_distance_parameter=critical_D,
        # Irrationality of theta/pi makes the S-1 nonzero differences give
        # distinct chord lengths on any one fixed-radius fibre.
        per_fibre_chord_labels=fibre_size - 1,
        min_source_count=min(item.source_count for item in angles),
        min_rotation_success=min(item.rotation_success for item in angles),
        # Put the fibres at heights 0,...,F-1 on a cylinder of radius
        # rho<1/2.  Squared distances are x_k+h^2.  The chord part satisfies
        # 0<=x_k<1, so different h give disjoint unit intervals, while
        # irrationality makes the S chord values distinct.
        generic_cylinder_distance_count=n - 1,
        source_incidence_sum=source_sum,
        rotation_success_sum=success_sum,
        active_joint_moment=joint,
        joint_over_nD=joint / (n * critical_D),
        min_success_over_n=min(item.rotation_success for item in angles) / n,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(asdict(run(args.scale)), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
