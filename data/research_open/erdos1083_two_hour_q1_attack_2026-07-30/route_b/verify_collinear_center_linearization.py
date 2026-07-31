#!/usr/bin/env python3
"""Exact certificates for the collinear-centre linearization theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def lifted_point(
    source_point: tuple[Fraction, Fraction],
    signed_center: Fraction,
) -> tuple[Fraction, Fraction]:
    """Return (Z,Y) under the fixed-A parabolic lift."""

    u, z = source_point
    return z, (u - signed_center) ** 2 + z**2


def circle_line(
    center_height: Fraction,
    radius_squared: Fraction,
) -> tuple[Fraction, Fraction]:
    """Return slope and intercept of the lifted line."""

    if radius_squared <= 0:
        raise ValueError("radius_squared must be positive")
    return (
        2 * center_height,
        radius_squared - center_height**2,
    )


def verify_finite_geometry() -> dict[str, int]:
    """Check incidence preservation, fibre size, and circle-line injection."""

    signed_center = Fraction(2)
    source_points = [
        (Fraction(u), Fraction(z))
        for u, z in product(range(-4, 9), range(-3, 4))
    ]

    fibres: dict[tuple[Fraction, Fraction], list[tuple[Fraction, Fraction]]] = {}
    for point in source_points:
        fibres.setdefault(lifted_point(point, signed_center), []).append(point)
    assert max(map(len, fibres.values())) <= 2

    circles = [
        (Fraction(w), Fraction(radius_squared))
        for w, radius_squared in product(range(-3, 4), range(1, 8))
    ]
    lines = [circle_line(w, radius_squared) for w, radius_squared in circles]
    assert len(lines) == len(set(lines))

    checked_incidences = 0
    for point in source_points:
        u, z = point
        Z, Y = lifted_point(point, signed_center)
        for w, radius_squared in circles:
            on_circle = (u - signed_center) ** 2 + (z - w) ** 2 == radius_squared
            slope, intercept = circle_line(w, radius_squared)
            on_line = Y == slope * Z + intercept
            assert on_circle == on_line
            checked_incidences += int(on_circle)

    return {
        "source_points": len(source_points),
        "lifted_points": len(fibres),
        "circles": len(circles),
        "lines": len(set(lines)),
        "checked_incidences": checked_incidences,
        "max_lift_fibre": max(map(len, fibres.values())),
    }


def endpoint_ledger() -> dict[str, Fraction]:
    """Verify the exact scalar endpoint at kappa=2/9."""

    kappa = Fraction(2, 9)
    ell = Fraction(14, 9)
    p = Fraction(23, 9)
    a = Fraction(7, 9)
    b = Fraction(85, 18)
    m = Fraction(5, 6)
    c = Fraction(47, 18)
    h = Fraction(19, 9)
    r = Fraction(19, 18)
    j = Fraction(14, 9)
    x = Fraction(53, 18)

    assert ell == 2 - 2 * kappa
    assert p == 3 - 2 * kappa
    assert a + b + m == 7 - 3 * kappa
    assert b + m == 6 - 2 * kappa
    assert 11 * a + 2 * b == 18
    assert b == c + h
    assert c == 2 * p - 3 * m
    assert r + h + m == 4
    assert x == h + m
    assert c == r + j
    assert j == ell
    assert j + h + m == ell + x
    assert 3 * a + b == 6 + r
    assert (5 - 15 * kappa) / 2 == m
    assert (1 + 3 * kappa) / 2 == m

    assert h + a < 3
    assert j + m < p
    assert x < 3

    return {
        "kappa": kappa,
        "labels_ell": ell,
        "parameter_points_p": p,
        "source_richness_a": a,
        "circles_b": b,
        "multiplicity_m": m,
        "signed_lines_c": c,
        "circles_per_signed_line_h": h,
        "signed_centers_r": r,
        "lines_per_signed_center_j": j,
        "targets_per_signed_center_x": x,
    }


def old_endpoint_linearization_gap() -> Fraction:
    """Return the source-incidence exponent gap at the old 9/41 ledger."""

    required = Fraction(225, 41)
    linearized_upper = (
        2 + Fraction(1, 3) + Fraction(2, 3) * Fraction(193, 41)
    )
    assert linearized_upper == Fraction(673, 123)
    assert required == Fraction(675, 123)
    return required - linearized_upper


def main() -> None:
    print("finite geometry:", verify_finite_geometry())
    print("endpoint ledger:", endpoint_ledger())
    print("old endpoint gap:", old_endpoint_linearization_gap())
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
