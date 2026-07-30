#!/usr/bin/env python3
"""Independent exact checks for the Euclidean hub incidence theorem.

This verifies coordinate identities, the ordered/unordered conversion,
and all affine exponent comparisons.  The planar incidence theorem
itself is an external mathematical input and is audited in the
accompanying independent review.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


AffineExponent = tuple[Fraction, Fraction]


def add(*terms: AffineExponent) -> AffineExponent:
    return (
        sum((term[0] for term in terms), Fraction()),
        sum((term[1] for term in terms), Fraction()),
    )


def scale(
    multiplier: Fraction, term: AffineExponent
) -> AffineExponent:
    return multiplier * term[0], multiplier * term[1]


def subtract(
    left: AffineExponent, right: AffineExponent
) -> AffineExponent:
    return left[0] - right[0], left[1] - right[1]


def evaluate(term: AffineExponent, kappa: Fraction) -> Fraction:
    return term[0] + term[1] * kappa


def reverse_circle(
    cosine: Fraction,
    radial: Fraction,
    height: Fraction,
    distance: Fraction,
) -> tuple[Fraction, Fraction, Fraction]:
    """Coefficients after the normalized u^2+z^2 terms."""

    return (
        -2 * cosine * radial,
        -2 * height,
        radial * radial + height * height - distance,
    )


def squared_radius(
    cosine: Fraction,
    radial: Fraction,
    distance: Fraction,
) -> Fraction:
    return distance - (1 - cosine * cosine) * radial * radial


def audit_reverse_circles() -> dict[str, object]:
    radials = tuple(Fraction(value) for value in range(-4, 5))
    heights = tuple(Fraction(value) for value in range(-2, 3))
    distances = tuple(Fraction(value) for value in range(-2, 8))

    parameter_count = len(radials) * len(heights) * len(distances)
    for cosine in (Fraction(-1), Fraction(-2, 3), Fraction(2, 3), Fraction(1)):
        circles = {
            reverse_circle(cosine, radial, height, distance)
            for radial, height, distance in itertools.product(
                radials, heights, distances
            )
        }
        if len(circles) != parameter_count:
            raise AssertionError(
                "nonperpendicular (q,d) map is not injective"
            )

    # The perpendicular exception is genuine.
    if reverse_circle(0, 3, 1, 7) != reverse_circle(0, -3, 1, 7):
        raise AssertionError("opposite radial points should collide at c=0")

    # Completing squares gives centre (cv,w) and the stated radius.
    cosine = Fraction(3, 5)
    radial = Fraction(7, 3)
    height = Fraction(-4, 3)
    distance = Fraction(13, 2)
    linear_u, linear_z, constant = reverse_circle(
        cosine, radial, height, distance
    )
    center_u = -linear_u / 2
    center_z = -linear_z / 2
    completed_radius = center_u**2 + center_z**2 - constant
    if completed_radius != squared_radius(cosine, radial, distance):
        raise AssertionError("completed-square radius identity failed")

    # One explicit real, zero, and imaginary member.
    radius_classes = {
        "real": squared_radius(Fraction(3, 5), 1, 1),
        "zero": squared_radius(Fraction(3, 5), 5, 16),
        "imaginary": squared_radius(Fraction(3, 5), 2, 1),
    }
    if not (
        radius_classes["real"] > 0
        and radius_classes["zero"] == 0
        and radius_classes["imaginary"] < 0
    ):
        raise AssertionError("radius classification failed")

    return {
        "nonperpendicular_cosines_checked": 4,
        "parameter_tuples_per_cosine": parameter_count,
        "perpendicular_collision_checked": True,
        "radius_classes": {
            key: str(value) for key, value in radius_classes.items()
        },
    }


def audit_ordered_unordered_conversion() -> dict[str, object]:
    """Check the exact factor ledger for symmetric ordered cells."""

    # Three unordered cells and three labels, with deliberately
    # nonuniform exact weights.
    weights = (
        (2, 0, 5),
        (1, 3, 4),
        (0, 7, 2),
    )
    unordered_total_square = sum(
        sum(row[label] for row in weights) ** 2
        for label in range(3)
    )
    unordered_diagonal = sum(
        value * value for row in weights for value in row
    )
    unordered_codegree = (
        unordered_total_square - unordered_diagonal
    )

    # Each unordered pair has the two orientations, and distance
    # symmetry makes their R-values equal.
    directed_rows = tuple(
        row for row in weights for _orientation in range(2)
    )
    directed_total_square = sum(
        sum(row[label] for row in directed_rows) ** 2
        for label in range(3)
    )
    directed_diagonal = sum(
        value * value for row in directed_rows for value in row
    )
    directed_codegree = directed_total_square - directed_diagonal

    if directed_total_square != 4 * unordered_total_square:
        raise AssertionError("ordered total-energy factor failed")
    if directed_diagonal != 2 * unordered_diagonal:
        raise AssertionError("ordered diagonal-energy factor failed")
    if directed_codegree != (
        4 * unordered_codegree + 2 * unordered_diagonal
    ):
        raise AssertionError("ordered codegree conversion failed")

    return {
        "unordered_codegree": unordered_codegree,
        "directed_codegree": directed_codegree,
        "identity": (
            "C_directed = 4*C_unordered + 2*Ediag_unordered"
        ),
        "interpretation": (
            "Eall_directed>=t^(13-o(1)) and "
            "Ediag_directed<=t^(12+o(1)) imply "
            "C_unordered>=t^(13-o(1))"
        ),
    }


def audit_exponents() -> dict[str, object]:
    plane_count = (Fraction(1), Fraction(0))
    points = (Fraction(3), Fraction(0))
    labels = (Fraction(2), Fraction(-2))
    hub = (Fraction(5), Fraction(-1))
    circle_count = add(points, labels)

    lower = add(labels, hub)
    upper = {
        "two_thirds": add(
            plane_count,
            scale(Fraction(2, 3), points),
            scale(Fraction(2, 3), circle_count),
        ),
        "six_eleven": add(
            plane_count,
            scale(Fraction(6, 11), points),
            scale(Fraction(9, 11), circle_count),
        ),
        "points": add(plane_count, points),
        "circles": add(plane_count, circle_count),
    }
    expected = {
        "two_thirds": (Fraction(19, 3), Fraction(-4, 3)),
        "six_eleven": (Fraction(74, 11), Fraction(-18, 11)),
        "points": (Fraction(4), Fraction(0)),
        "circles": (Fraction(6), Fraction(-2)),
    }
    if upper != expected:
        raise AssertionError("incidence exponent substitution failed")

    gaps = {
        name: subtract(lower, exponent)
        for name, exponent in upper.items()
    }
    expected_gaps = {
        "two_thirds": (Fraction(2, 3), Fraction(-5, 3)),
        "six_eleven": (Fraction(3, 11), Fraction(-15, 11)),
        "points": (Fraction(3), Fraction(-3)),
        "circles": (Fraction(1), Fraction(-1)),
    }
    if gaps != expected_gaps:
        raise AssertionError("lower-minus-upper ledger failed")

    for kappa in (
        Fraction(1, 100),
        Fraction(1, 10),
        Fraction(199, 1000),
    ):
        if not all(
            evaluate(gap, kappa) > 0 for gap in gaps.values()
        ):
            raise AssertionError("sub-one-fifth exclusion failed")
    if evaluate(gaps["six_eleven"], Fraction(1, 5)) != 0:
        raise AssertionError("one-fifth endpoint failed")

    # The 6/11,9/11 term is the largest upper term on 0<kappa<1.
    dominance_gaps = {
        name: subtract(upper["six_eleven"], exponent)
        for name, exponent in upper.items()
        if name != "six_eleven"
    }
    for kappa in (Fraction(1, 100), Fraction(1, 2), Fraction(99, 100)):
        if not all(
            evaluate(gap, kappa) > 0
            for gap in dominance_gaps.values()
        ):
            raise AssertionError("dominant incidence term failed")

    # Choosing kappa=1/5-epsilon proves the matching exponent.
    epsilon = Fraction(1, 100)
    matching_kappa = Fraction(1, 5) - epsilon
    if matching_kappa <= 0:
        raise AssertionError("invalid matching parameter")
    if evaluate(
        gaps["six_eleven"], matching_kappa
    ) != Fraction(15, 11) * epsilon:
        raise AssertionError("matching corollary slack failed")

    return {
        "lower": tuple(str(value) for value in lower),
        "upper": {
            key: tuple(str(value) for value in value)
            for key, value in upper.items()
        },
        "gaps": {
            key: tuple(str(value) for value in value)
            for key, value in gaps.items()
        },
        "threshold": "kappa < 1/5",
        "matching_parameter": "kappa = 1/5 - epsilon",
    }


def audit_repeated_circle_refinement() -> dict[str, object]:
    """Check the weighted cross-plane union and its threshold."""

    plane_count = (Fraction(1), Fraction(0))
    points = (Fraction(3), Fraction(0))
    labels = (Fraction(2), Fraction(-2))
    hub = (Fraction(5), Fraction(-1))
    all_circles = add(plane_count, points, labels)
    lower = add(labels, hub)

    upper = {
        "two_thirds": add(
            scale(Fraction(2, 3), points),
            scale(Fraction(2, 3), all_circles),
        ),
        "six_eleven": add(
            scale(Fraction(6, 11), points),
            scale(Fraction(9, 11), all_circles),
        ),
        "points": points,
        "circles": all_circles,
    }
    expected = {
        "two_thirds": (Fraction(6), Fraction(-4, 3)),
        "six_eleven": (Fraction(72, 11), Fraction(-18, 11)),
        "points": (Fraction(3), Fraction(0)),
        "circles": (Fraction(6), Fraction(-2)),
    }
    if upper != expected:
        raise AssertionError("weighted-union exponent ledger failed")

    repeat_gap = subtract(lower, upper["six_eleven"])
    if repeat_gap != (Fraction(5, 11), Fraction(-15, 11)):
        raise AssertionError("forced multiplicity exponent failed")
    if evaluate(repeat_gap, Fraction(1, 3)) != 0:
        raise AssertionError("one-third multiplicity threshold failed")

    for kappa in (Fraction(1, 100), Fraction(1, 4), Fraction(99, 100)):
        dominant = evaluate(upper["six_eleven"], kappa)
        if not all(
            dominant > evaluate(value, kappa)
            for name, value in upper.items()
            if name != "six_eleven"
        ):
            raise AssertionError(
                "weighted-union dominant term failed"
            )

    # An exact collision across different nonzero cosines.
    first = reverse_circle(Fraction(1, 2), 4, 1, 15)
    second = reverse_circle(Fraction(2, 3), 3, 1, 8)
    if first != second:
        raise AssertionError("cross-plane collision identity failed")

    return {
        "distinct_circle_cap": "n <= M*Q*L",
        "upper": {
            key: tuple(str(value) for value in exponent)
            for key, exponent in upper.items()
        },
        "forced_mu_exponent": tuple(
            str(value) for value in repeat_gap
        ),
        "positive_range": "kappa < 1/3",
        "cross_plane_collision_checked": True,
        "preprocessing": (
            "discard empty/imaginary circles; charge active "
            "zero-radius triples by MQL; merge positive-radius circles"
        ),
    }


def audit() -> dict[str, object]:
    return {
        "schema": (
            "amra.erdos1083.euclidean-hub-incidence."
            "independent-audit.v1"
        ),
        "status": "PASS",
        "reverse_circles": audit_reverse_circles(),
        "ordered_unordered": audit_ordered_unordered_conversion(),
        "exponents": audit_exponents(),
        "repeated_circle_refinement": (
            audit_repeated_circle_refinement()
        ),
        "scope": (
            "Exact coordinate and exponent checks; the external "
            "planar point-circle theorem is audited in the markdown."
        ),
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
