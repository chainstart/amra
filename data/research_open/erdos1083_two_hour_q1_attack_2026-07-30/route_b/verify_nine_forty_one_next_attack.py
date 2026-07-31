#!/usr/bin/env python3
"""Certificates for the signed-slope aggregation barrier at 9/41."""

from __future__ import annotations

from fractions import Fraction


def threshold_from_aggregate_saving(delta: Fraction) -> Fraction:
    """Return the conditional threshold forced by a t^{-delta} saving."""

    if delta < 0:
        raise ValueError("delta must be nonnegative")
    if delta >= Fraction(37, 125):
        raise ValueError("certificate is restricted to thresholds below 2/5")

    threshold = (9 + 25 * delta) / 41
    lower_m = (5 - 15 * threshold + 9 * delta) / 2
    upper_m = (22 - 3 * threshold) / 25
    assert lower_m == upper_m
    return threshold


def endpoint_aggregate_ledger() -> dict[str, Fraction]:
    kappa = Fraction(9, 41)
    ell = Fraction(64, 41)
    a = Fraction(32, 41)
    b = Fraction(193, 41)
    m = Fraction(35, 41)
    p = Fraction(105, 41)
    c = Fraction(105, 41)
    r = Fraction(41, 41)
    j = Fraction(64, 41)
    h = Fraction(88, 41)
    x = Fraction(123, 41)

    hub = 7 - 3 * kappa
    triple_capacity = 6 - 2 * kappa

    # Original Route B endpoint.
    assert ell == 2 - 2 * kappa
    assert a + b + m == hub
    assert b + m == triple_capacity
    assert a + b == Fraction(18, 11) + Fraction(9, 11) * b
    assert c == 2 * p - 3 * m
    assert c == p

    # Signed-slope enrichment.
    assert c == r + j
    assert b == r + j + h
    assert x == h + m
    assert x == 3
    assert r + x == 4
    assert j == ell
    assert r + ell + x + a == hub
    assert r + j + h + m == triple_capacity

    # Capacity slacks.
    assert j + m < p  # parallel lines use disjoint parameter points
    assert h + a < 3  # old source fibre cap

    # Each target is used by all L labels at exponent scale.
    assert j + h + m == ell + x

    return {
        "kappa": kappa,
        "labels_ell": ell,
        "source_richness_a": a,
        "circles_b": b,
        "circle_multiplicity_m": m,
        "parameter_points_p": p,
        "parameter_lines_c": c,
        "signed_slopes_r": r,
        "lines_per_slope_j": j,
        "circles_per_line_h": h,
        "target_points_per_slope_x": x,
        "hub": hub,
        "triple_capacity": triple_capacity,
    }


def finite_interval_service_model(
    line_count: int = 31,
    tangent_count: int = 7,
    height_count: int = 11,
) -> dict[str, int]:
    """Construct only the one-slope label-service model from Section 6.

    This certificate has no source-point set and does not claim a full
    Euclidean endpoint realization.
    """

    if min(line_count, tangent_count, height_count) <= 0:
        raise ValueError("all sizes must be positive")

    tangent_squares = tuple(range(1, tangent_count + 1))
    intercepts = tuple(range(1, line_count + 1))
    heights = tuple(range(height_count))
    labels = {
        intercept + tangent
        for intercept in intercepts
        for tangent in tangent_squares
    }

    line_parameter_points: dict[int, set[tuple[int, int]]] = {}
    circle_targets: dict[tuple[int, int], set[tuple[int, int]]] = {}
    target_lines: dict[tuple[int, int], set[int]] = {}

    for intercept in intercepts:
        line_parameter_points[intercept] = {
            (tangent, intercept + tangent)
            for tangent in tangent_squares
        }
        for height in heights:
            circle = (intercept, height)
            circle_targets[circle] = set()
            for tangent in tangent_squares:
                target = (tangent, height)
                circle_targets[circle].add(target)
                target_lines.setdefault(target, set()).add(intercept)

    assert len(labels) == line_count + tangent_count - 1
    assert all(
        len(points) == tangent_count
        for points in line_parameter_points.values()
    )
    assert all(
        len(targets) == tangent_count
        for targets in circle_targets.values()
    )
    assert all(len(lines) == line_count for lines in target_lines.values())

    target_count = tangent_count * height_count
    circle_count = line_count * height_count
    triple_count = line_count * tangent_count * height_count

    assert len(target_lines) == target_count
    assert len(circle_targets) == circle_count
    assert sum(map(len, circle_targets.values())) == triple_count
    assert sum(map(len, target_lines.values())) == triple_count

    return {
        "parameter_lines": line_count,
        "tangent_squares": tangent_count,
        "heights": height_count,
        "labels": len(labels),
        "target_points": target_count,
        "circle_classes": circle_count,
        "triples": triple_count,
        "multiplicity_per_circle": tangent_count,
        "lines_per_target": line_count,
    }


def main() -> None:
    print("aggregate endpoint:", endpoint_aggregate_ledger())
    print("finite interval service:", finite_interval_service_model())
    print(
        "threshold with delta=1/100:",
        threshold_from_aggregate_saving(Fraction(1, 100)),
    )
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
