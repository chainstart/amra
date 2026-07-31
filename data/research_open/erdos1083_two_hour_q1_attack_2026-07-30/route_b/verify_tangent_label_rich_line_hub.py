#!/usr/bin/env python3
"""Exact certificates for the tangent--label rich-line hub theorem.

The script checks:

1. the reverse-circle radius identity symbolically;
2. the two competing multiplicity thresholds and their crossing;
3. every equality in the endpoint exponent ledger;
4. a finite random-coordinate version of the source fibre cap;
5. a finite exact version of the planar target-fibre encoding.

It is a verifier for algebra and finite bookkeeping, not a proof of the
Szemeredi--Trotter or point--circle incidence theorems invoked in the note.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

import sympy as sp


def symbolic_radius_identity() -> None:
    c, v, d = sp.symbols("c v d", nonzero=True, real=True)
    a = c * v
    tau = (1 - c**2) / c**2
    radius_sq = d - (1 - c**2) * v**2
    assert sp.simplify(radius_sq + a**2 * tau - d) == 0


def threshold_certificate() -> dict[str, Fraction]:
    kappa = sp.symbols("kappa", real=True)
    lower = (5 - 15 * kappa) / 2
    source_fibre_upper = 1 - kappa / 2
    planar_fibre_upper = (22 - 3 * kappa) / 25
    first_root = sp.solve(sp.Eq(lower, source_fibre_upper), kappa)
    refined_root = sp.solve(sp.Eq(lower, planar_fibre_upper), kappa)
    assert first_root == [sp.Rational(3, 14)]
    assert refined_root == [sp.Rational(9, 41)]
    assert (
        sp.simplify(lower - source_fibre_upper)
        == sp.Rational(3, 2) - 7 * kappa
    )
    assert (
        sp.simplify(lower - planar_fibre_upper)
        == sp.Rational(81, 50) - sp.Rational(369, 50) * kappa
    )
    return {
        "first_crossing": Fraction(3, 14),
        "refined_crossing": Fraction(9, 41),
        "old_threshold": Fraction(1, 5),
        "strict_gain": Fraction(9, 41) - Fraction(1, 5),
    }


def endpoint_ledger_certificate() -> dict[str, Fraction]:
    kappa = Fraction(9, 41)
    a = Fraction(32, 41)
    b = Fraction(193, 41)
    m = Fraction(35, 41)
    p = Fraction(105, 41)
    c = Fraction(105, 41)

    assert a + b + m == 7 - 3 * kappa
    assert b + m == 6 - 2 * kappa
    assert a + b == Fraction(18, 11) + Fraction(9, 11) * b
    assert c == 2 * p - 3 * m
    assert c == p
    assert c + 3 + a == 7 - 3 * kappa
    assert m == (5 - 15 * kappa) / 2
    assert m == (22 - 3 * kappa) / 25

    # The second rich-line term is strictly below the required line count.
    assert p - m < c

    # The planar target fibre is active; the source fibre has slack.
    hub = 7 - 3 * kappa
    circles_per_line = b - c
    assert circles_per_line + m == 3
    assert circles_per_line + a < 3
    assert c + 3 + a == hub

    return {
        "kappa": kappa,
        "source_richness_a": a,
        "circle_count_b": b,
        "multiplicity_m": m,
        "parameter_points_p": p,
        "parameter_lines_c": c,
        "circles_per_line": circles_per_line,
        "hub_mass": hub,
    }


def finite_fibre_cap_certificate(seed: int = 1083) -> dict[str, int]:
    """Build many circles with fixed A^2,r^2 and count source incidences.

    For each source point and each of A=+sqrt(a),-sqrt(a), the circle
    equation has at most two possible centre heights.  We explicitly
    construct every such circle for an integer sample and verify that the
    total number of incidences is at most 4Q.
    """

    rng = Random(seed)
    q = 80
    points = {(rng.randint(-30, 30), rng.randint(-30, 30)) for _ in range(q)}
    points = sorted(points)
    q = len(points)
    abs_a = 7
    radius_sq = 625

    # Exact rational/integer centres are sufficient for the finite check.
    centres: set[tuple[int, int]] = set()
    for u, z in points:
        for centre_x in (abs_a, -abs_a):
            rem = radius_sq - (u - centre_x) ** 2
            root = int(sp.integer_nthroot(max(rem, 0), 2)[0])
            if rem >= 0 and root * root == rem:
                centres.add((centre_x, z + root))
                centres.add((centre_x, z - root))

    incidences = 0
    max_centres_per_point = 0
    for u, z in points:
        local = 0
        for centre_x, centre_z in centres:
            if (u - centre_x) ** 2 + (z - centre_z) ** 2 == radius_sq:
                incidences += 1
                local += 1
        max_centres_per_point = max(max_centres_per_point, local)

    assert max_centres_per_point <= 4
    assert incidences <= 4 * q
    return {
        "source_points": q,
        "circles_in_fibre": len(centres),
        "incidences": incidences,
        "cap": 4 * q,
        "max_centres_per_point": max_centres_per_point,
    }


def finite_target_fibre_certificate() -> dict[str, int]:
    """Check that one fixed-A parameter fibre gives distinct coplanar targets."""

    centre_x = 5
    radius_sq = 169
    centre_heights = (-9, -2, 4, 13)
    transverse_coordinates = (-12, -7, -1, 3, 8, 15)

    targets: set[tuple[int, int, int]] = set()
    labels: set[int] = set()
    normalized_circles: dict[int, set[tuple[int, int, int]]] = {}

    for centre_z in centre_heights:
        normalized_circles[centre_z] = set()
        for transverse_y in transverse_coordinates:
            # q=(A,y,w), tan(beta-alpha)=y/A, and
            # d=rho^2+A^2 tan^2=rho^2+y^2.
            q = (centre_x, transverse_y, centre_z)
            d = radius_sq + transverse_y**2
            targets.add(q)
            labels.add(d)

            # Normalized reverse-circle coefficients in the source xz-plane:
            # x^2+z^2-2Ax-2wz+(A^2+w^2-rho^2)=0.
            coeffs = (
                -2 * centre_x,
                -2 * centre_z,
                centre_x**2 + centre_z**2 - radius_sq,
            )
            normalized_circles[centre_z].add(coeffs)

    assert len(targets) == len(centre_heights) * len(transverse_coordinates)
    assert {point[0] for point in targets} == {centre_x}
    assert all(len(equations) == 1 for equations in normalized_circles.values())
    assert len(
        {next(iter(equations)) for equations in normalized_circles.values()}
    ) == len(centre_heights)
    assert len(labels) == len({y * y for y in transverse_coordinates})

    return {
        "circles": len(centre_heights),
        "multiplicity_per_circle": len(transverse_coordinates),
        "coplanar_target_points": len(targets),
        "selected_labels": len(labels),
    }


def main() -> None:
    symbolic_radius_identity()
    print("symbolic radius identity: PASS")
    print("threshold:", threshold_certificate())
    print("endpoint ledger:", endpoint_ledger_certificate())
    print("finite fibre cap:", finite_fibre_cap_certificate())
    print("finite target fibre:", finite_target_fibre_certificate())
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
