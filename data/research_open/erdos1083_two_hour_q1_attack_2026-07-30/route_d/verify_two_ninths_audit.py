#!/usr/bin/env python3
"""Independent exact certificates for the Route B 2/9 argument."""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def lift(
    point: tuple[Fraction, Fraction],
    signed_center: Fraction,
) -> tuple[Fraction, Fraction]:
    u, z = point
    return z, (u - signed_center) ** 2 + z**2


def lifted_line(
    center_height: Fraction,
    radius_squared: Fraction,
) -> tuple[Fraction, Fraction]:
    if radius_squared <= 0:
        raise ValueError("positive radius required")
    return 2 * center_height, radius_squared - center_height**2


def independent_geometry_check() -> dict[str, int]:
    """Verify two-to-one lifting and exact circle/line equivalence."""

    signed_center = Fraction(2)
    points = [
        (Fraction(u), Fraction(z))
        for u, z in product(range(-7, 12), range(-8, 9))
    ]
    circles = [
        (Fraction(w), Fraction(radius_squared))
        for w, radius_squared in product(range(-6, 7), range(1, 26))
    ]

    fibres: dict[tuple[Fraction, Fraction], int] = {}
    for point in points:
        image = lift(point, signed_center)
        fibres[image] = fibres.get(image, 0) + 1
    assert max(fibres.values()) <= 2

    lines = [lifted_line(w, radius_squared) for w, radius_squared in circles]
    assert len(lines) == len(set(lines))

    incidences = 0
    for u, z in points:
        Z, Y = lift((u, z), signed_center)
        for w, radius_squared in circles:
            circle_incidence = (
                (u - signed_center) ** 2 + (z - w) ** 2
                == radius_squared
            )
            slope, intercept = lifted_line(w, radius_squared)
            line_incidence = Y == slope * Z + intercept
            assert circle_incidence == line_incidence
            incidences += int(circle_incidence)

    return {
        "points": len(points),
        "image_points": len(fibres),
        "maximum_fibre": max(fibres.values()),
        "circles": len(circles),
        "lines": len(set(lines)),
        "incidences": incidences,
    }


def exponent_certificate(kappa: Fraction) -> dict[str, Fraction]:
    """Return the exact branch bounds used in the audit."""

    old_m_lower = (5 - 15 * kappa) / 2
    q_branch_m_upper = (24 * kappa - 5) / 16
    main_branch_m_upper = (1 + 3 * kappa) / 2
    rich_line_term_gap_at_m_one = 1 - 2 * kappa

    return {
        "kappa": kappa,
        "old_m_lower": old_m_lower,
        "q_branch_m_upper": q_branch_m_upper,
        "q_branch_gap": old_m_lower - q_branch_m_upper,
        "main_branch_m_upper": main_branch_m_upper,
        "main_branch_gap": old_m_lower - main_branch_m_upper,
        "rich_line_term_gap_at_m_one": rich_line_term_gap_at_m_one,
    }


def threshold_from_fixed_a_saving(delta: Fraction) -> Fraction:
    """Threshold if the fixed-A ST main term gains a factor t^-delta."""

    if delta < 0:
        raise ValueError("delta must be nonnegative")
    return Fraction(2, 9) + delta / 6


def threshold_from_ledger_saving(delta: Fraction) -> Fraction:
    """Threshold if rich-line or target capacity gains t^-delta."""

    if delta < 0:
        raise ValueError("delta must be nonnegative")
    return Fraction(2, 9) + delta / 18


def cross_energy_certificate() -> dict[str, Fraction]:
    """Return the exact collision exponents at the 2/9 endpoint."""

    r = Fraction(19, 18)
    s = Fraction(7, 9)
    u = Fraction(5, 6)
    h = Fraction(19, 9)
    d = Fraction(3)

    one_fibre_domain = s + u + h
    one_fibre_required = 2 * one_fibre_domain - d
    one_fibre_benchmark = 2 * s + u + h

    all_a_domain = r + s + u + h
    all_a_required = 2 * all_a_domain - d
    all_a_benchmark = 2 * r + 2 * s + u + h

    assert one_fibre_required == Fraction(40, 9)
    assert one_fibre_benchmark == Fraction(9, 2)
    assert one_fibre_benchmark - one_fibre_required == Fraction(1, 18)
    assert all_a_required == Fraction(59, 9)
    assert all_a_benchmark == Fraction(119, 18)
    assert all_a_benchmark - all_a_required == Fraction(1, 18)

    return {
        "one_fibre_domain": one_fibre_domain,
        "one_fibre_required": one_fibre_required,
        "one_fibre_benchmark": one_fibre_benchmark,
        "one_fibre_saving_needed": one_fibre_benchmark - one_fibre_required,
        "all_a_domain": all_a_domain,
        "all_a_required": all_a_required,
        "all_a_benchmark": all_a_benchmark,
        "all_a_saving_needed": all_a_benchmark - all_a_required,
    }


def endpoint_certificate() -> dict[str, Fraction]:
    """Verify the complete scalar endpoint ledger independently."""

    kappa = Fraction(2, 9)
    a = Fraction(7, 9)
    b = Fraction(85, 18)
    m = Fraction(5, 6)
    c = Fraction(47, 18)
    h = Fraction(19, 9)
    r = Fraction(19, 18)

    assert a + b + m == 7 - 3 * kappa
    assert b + m == 6 - 2 * kappa
    assert 11 * a + 2 * b == 18
    assert b == c + h
    assert c == 6 - 4 * kappa - 3 * m
    assert r + h + m == 4
    assert r == 10 - 4 * kappa - b - 4 * m
    assert 3 * a + b == 6 + r
    assert a + 2 * m == 2 + 2 * kappa
    assert a == 1 - kappa
    assert m == (5 - 15 * kappa) / 2
    assert m == (1 + 3 * kappa) / 2

    branch = exponent_certificate(kappa)
    assert branch["main_branch_gap"] == 0
    assert branch["q_branch_gap"] == Fraction(13, 16)
    assert branch["rich_line_term_gap_at_m_one"] == Fraction(5, 9)

    return {
        "kappa": kappa,
        "a": a,
        "b": b,
        "m": m,
        "c": c,
        "h": h,
        "r": r,
        **branch,
    }


def main() -> None:
    print("geometry:", independent_geometry_check())
    print("endpoint:", endpoint_certificate())
    for kappa in (Fraction(1, 5), Fraction(9, 41), Fraction(2, 9)):
        print(f"branches at {kappa}:", exponent_certificate(kappa))
    print("cross energy:", cross_energy_certificate())
    print(
        "threshold from fixed-A delta=1/100:",
        threshold_from_fixed_a_saving(Fraction(1, 100)),
    )
    print("ALL INDEPENDENT CHECKS PASSED")


if __name__ == "__main__":
    main()
