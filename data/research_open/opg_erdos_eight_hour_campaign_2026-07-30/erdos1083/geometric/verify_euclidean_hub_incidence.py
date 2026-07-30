#!/usr/bin/env python3
"""Exponent and coordinate checks for Euclidean hub incidence."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction


def hub_exponent_ledger(kappa: Fraction) -> dict[str, Fraction]:
    kappa = Fraction(kappa)
    if kappa <= 0 or kappa >= 1:
        raise ValueError("kappa must lie in (0,1)")

    labels = Fraction(2) - 2 * kappa
    hub_mass = Fraction(5) - kappa
    lower_total = labels + hub_mass
    incidence_terms = {
        "two_thirds": Fraction(19, 3) - Fraction(4, 3) * kappa,
        "six_eleven": (
            Fraction(74, 11) - Fraction(18, 11) * kappa
        ),
        "points": Fraction(4),
        "circles": Fraction(6) - 2 * kappa,
    }
    upper = max(incidence_terms.values())
    return {
        "kappa": kappa,
        "labels": labels,
        "hub_mass_required": hub_mass,
        "lower_total": lower_total,
        **incidence_terms,
        "upper_total": upper,
        "total_saving": lower_total - upper,
        "per_label_upper": upper - labels,
        "per_label_saving": hub_mass - (upper - labels),
    }


def conditional_kappa_threshold(saving: Fraction) -> Fraction:
    saving = Fraction(saving)
    if saving < 0:
        raise ValueError("saving must be nonnegative")
    return (Fraction(3) + 11 * saving) / 15


def forced_repeat_exponent(kappa: Fraction) -> Fraction:
    """Cross-plane circle multiplicity forced by a surviving hub."""

    kappa = Fraction(kappa)
    return (Fraction(5) - 15 * kappa) / 11


def normalized_circle(
    cosine: Fraction,
    radial: int,
    height: int,
    distance: int,
) -> tuple[Fraction, Fraction, Fraction]:
    """Coefficients (-2cv,-2w,v^2+w^2-d) after u^2+z^2."""

    cosine = Fraction(cosine)
    return (
        -2 * cosine * radial,
        Fraction(-2 * height),
        Fraction(radial * radial + height * height - distance),
    )


def finite_circle_injectivity_check() -> dict[str, int]:
    cosine = Fraction(2, 3)
    radials = (-3, -2, -1, 1, 2, 3)
    heights = tuple(range(-2, 3))
    distances = tuple(range(1, 8))
    triples = tuple(
        itertools.product(radials, heights, distances)
    )
    circles = {
        normalized_circle(cosine, radial, height, distance)
        for radial, height, distance in triples
    }
    if len(circles) != len(triples):
        raise AssertionError("nonperpendicular reverse circles collided")

    # At cosine zero, opposite signed radials with the same height and
    # distance do collide, certifying why that plane is deleted.
    perpendicular = normalized_circle(Fraction(0), 2, 1, 5)
    opposite = normalized_circle(Fraction(0), -2, 1, 5)
    if perpendicular != opposite:
        raise AssertionError("perpendicular exception was not detected")

    # A genuine cross-plane collision with two different nonzero
    # cosines: cv=2, w=1, and v^2-d=1 in both cases.
    cross_first = normalized_circle(Fraction(1, 2), 4, 1, 15)
    cross_second = normalized_circle(Fraction(2, 3), 3, 1, 8)
    if cross_first != cross_second:
        raise AssertionError("cosine-radial collision identity failed")

    return {
        "nonperpendicular_parameter_triples": len(triples),
        "distinct_nonperpendicular_circles": len(circles),
        "perpendicular_opposite_collision": 1,
        "cross_plane_cosine_radial_collision": 1,
    }


def audit() -> dict[str, object]:
    ledgers = {}
    for kappa in (
        Fraction(1, 10),
        Fraction(1, 5),
        Fraction(1, 2),
    ):
        ledger = hub_exponent_ledger(kappa)
        ledgers[str(kappa)] = {
            key: str(value) for key, value in ledger.items()
        }

    if hub_exponent_ledger(Fraction(1, 10))[
        "total_saving"
    ] <= 0:
        raise AssertionError("subcritical hub should be excluded")
    if hub_exponent_ledger(Fraction(1, 5))[
        "total_saving"
    ] != 0:
        raise AssertionError("one-fifth threshold failed")
    balanced = hub_exponent_ledger(Fraction(1, 2))
    if balanced["total_saving"] != Fraction(-9, 22):
        raise AssertionError("balanced incidence deficit failed")
    if balanced["per_label_upper"] != Fraction(54, 11):
        raise AssertionError("balanced per-label capacity failed")
    if conditional_kappa_threshold(Fraction(9, 22)) != Fraction(1, 2):
        raise AssertionError("conditional threshold failed")
    if forced_repeat_exponent(Fraction(1, 4)) != Fraction(5, 44):
        raise AssertionError("forced repeat exponent failed")
    if forced_repeat_exponent(Fraction(1, 3)) != 0:
        raise AssertionError("one-third repeat threshold failed")

    return {
        "schema": "amra.erdos1083.euclidean-hub-incidence.v1",
        "status": "PASS",
        "hub_ledgers": ledgers,
        "coordinate_injectivity": finite_circle_injectivity_check(),
        "unconditional_hub_exclusion": "0 < kappa < 1/5",
        "forced_repeat_range": "1/5 <= kappa < 1/3",
        "balanced_required_saving": "strictly greater than 9/22",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()
    print(json.dumps(audit(), indent=args.indent, sort_keys=True))


if __name__ == "__main__":
    main()
