#!/usr/bin/env python3
"""Exact certificates for the Route E joint endpoint theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def endpoint_certificate() -> dict[str, Fraction]:
    """Verify the full 2/9 ledger and the joint ST/service equality."""

    kappa = Fraction(2, 9)
    a = Fraction(7, 9)
    b = Fraction(85, 18)
    m = Fraction(5, 6)
    c = Fraction(47, 18)
    h = Fraction(19, 9)
    r = Fraction(19, 18)
    p = Fraction(23, 9)

    assert a + b + m == 7 - 3 * kappa
    assert b + m == 6 - 2 * kappa
    assert 11 * a + 2 * b == 18
    assert b == c + h
    assert c == 2 * p - 3 * m
    assert r + h + m == 4
    assert 3 * a + b == 6 + r
    assert a == 1 - kappa
    assert m == (5 - 15 * kappa) / 2
    assert m == (1 + 3 * kappa) / 2

    joint_left = r + b + 4 * m
    joint_right = 4 + 2 * p
    assert joint_left == joint_right == Fraction(82, 9)

    return {
        "kappa": kappa,
        "a": a,
        "b": b,
        "m": m,
        "c": c,
        "h": h,
        "r": r,
        "parameter_point_exponent": p,
        "joint_left": joint_left,
        "joint_right": joint_right,
    }


def conditional_threshold(delta: Fraction) -> dict[str, Fraction]:
    """Return the exact threshold and all branch-separation margins."""

    if delta <= 0:
        raise ValueError("delta must be positive")
    if delta >= Fraction(16, 5):
        raise ValueError("the audited theorem requires delta < 16/5")

    threshold = (4 + delta) / 18
    improvement = delta / 18
    q_branch_threshold = (5 + delta) / 16
    q_branch_separation = q_branch_threshold - threshold

    assert threshold == Fraction(2, 9) + improvement
    assert threshold < Fraction(2, 5)
    assert q_branch_separation == (13 + delta) / 144
    assert q_branch_separation > 0

    return {
        "delta": delta,
        "threshold": threshold,
        "improvement": improvement,
        "q_branch_threshold": q_branch_threshold,
        "q_branch_separation": q_branch_separation,
        "point_circle_range_limit": Fraction(2, 5),
    }


def branch_certificate(
    kappa: Fraction,
    delta: Fraction,
) -> dict[str, Fraction]:
    """Audit the exact lower and upper multiplicity bounds."""

    if delta < 0:
        raise ValueError("delta must be nonnegative")

    m_lower = (5 - 15 * kappa) / 2
    main_m_upper = (1 + 3 * kappa - delta) / 2
    q_branch_m_upper = (24 * kappa - 5 - 9 * delta) / 16
    main_gap = m_lower - main_m_upper
    q_branch_gap = m_lower - q_branch_m_upper

    assert main_gap == 2 - 9 * kappa + delta / 2
    assert q_branch_gap == 9 * (5 - 16 * kappa + delta) / 16

    return {
        "kappa": kappa,
        "delta": delta,
        "m_lower": m_lower,
        "main_m_upper": main_m_upper,
        "q_branch_m_upper": q_branch_m_upper,
        "main_gap": main_gap,
        "q_branch_gap": q_branch_gap,
    }


def service_saturation_model(
    radius_count: int = 5,
    height_count: int = 7,
    tangent_count: int = 3,
) -> dict[str, object]:
    """Build the exact interval model saturating target service.

    Set A=1.  A target (w, tau) carrying label d=b+tau produces the
    positive-radius circle with centre (1,w) and squared radius b.
    Square roots are unnecessary for the exact parameter audit.
    """

    if min(radius_count, height_count, tangent_count) < 1:
        raise ValueError("all counts must be positive")

    radii_squared = tuple(range(1, radius_count + 1))
    heights = tuple(range(1, height_count + 1))
    tangent_squares = tuple(range(1, tangent_count + 1))
    labels = {
        b + tau
        for b, tau in product(radii_squared, tangent_squares)
    }
    circles = set(product(radii_squared, heights))
    targets = set(product(heights, tangent_squares))
    producers = {
        (b, w, tau, b + tau)
        for b, w, tau in product(
            radii_squared,
            heights,
            tangent_squares,
        )
    }

    for b, w, tau, label in producers:
        assert b > 0
        assert tau > 0
        assert label == b + tau
        assert (b, w) in circles
        assert (w, tau) in targets
        assert label in labels

    circle_multiplicities = {
        circle: sum(
            1
            for b, w, _tau, _label in producers
            if (b, w) == circle
        )
        for circle in circles
    }
    target_service_degrees = {
        target: sum(
            1
            for b, w, tau, _label in producers
            if (w, tau) == target
        )
        for target in targets
    }

    assert set(circle_multiplicities.values()) == {tangent_count}
    assert set(target_service_degrees.values()) == {radius_count}
    assert len(labels) == radius_count + tangent_count - 1

    total_service = len(producers)
    service_cap = min(len(labels), radius_count) * len(targets)
    assert total_service == radius_count * height_count * tangent_count
    assert total_service == service_cap

    return {
        "radius_count": radius_count,
        "height_count": height_count,
        "tangent_count": tangent_count,
        "circle_count": len(circles),
        "target_count": len(targets),
        "label_count": len(labels),
        "producer_count": len(producers),
        "service_cap": service_cap,
        "circle_multiplicities": circle_multiplicities,
        "target_service_degrees": target_service_degrees,
        "labels": labels,
    }


def main() -> None:
    endpoint = endpoint_certificate()
    print("2/9 endpoint")
    for key, value in endpoint.items():
        print(f"  {key}: {value}")

    for delta in (Fraction(1, 18), Fraction(1, 2), Fraction(1)):
        threshold = conditional_threshold(delta)
        at_crossing = branch_certificate(threshold["threshold"], delta)
        assert at_crossing["main_gap"] == 0
        print(f"conditional threshold for delta={delta}")
        for key, value in threshold.items():
            print(f"  {key}: {value}")

    model = service_saturation_model()
    print("exact service-saturation model")
    for key in (
        "radius_count",
        "height_count",
        "tangent_count",
        "circle_count",
        "target_count",
        "label_count",
        "producer_count",
        "service_cap",
    ):
        print(f"  {key}: {model[key]}")

    print("ALL EXACT CHECKS PASSED")


if __name__ == "__main__":
    main()
