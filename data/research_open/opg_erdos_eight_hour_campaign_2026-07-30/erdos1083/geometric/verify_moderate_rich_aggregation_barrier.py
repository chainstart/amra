#!/usr/bin/env python3
"""Exact LP certificate for the moderate-rich aggregation barrier."""

from __future__ import annotations

import json
from fractions import Fraction


def ledger(kappa: Fraction) -> dict[str, Fraction]:
    richness = 1 - kappa
    circle_count = Fraction(7 + 11 * kappa, 2)
    multiplicity = Fraction(5 - 15 * kappa, 2)
    return {
        "richness": richness,
        "circle_count": circle_count,
        "multiplicity": multiplicity,
        "triple_weight": circle_count + multiplicity,
        "weighted_mass": richness + circle_count + multiplicity,
        "unweighted_incidence": richness + circle_count,
        "point_circle_second": Fraction(18, 11)
        + Fraction(9, 11) * circle_count,
        "weighted_second": Fraction(72, 11)
        - Fraction(18, 11) * kappa
        + Fraction(2, 11) * multiplicity,
        "hub": 7 - 3 * kappa,
        "slot_per_plane": circle_count + multiplicity - 1,
        "ms_pair": Fraction(4, 3) * richness,
    }


def audit() -> dict[str, object]:
    checked = 0
    for denominator in range(3, 25):
        for numerator in range(1, denominator):
            kappa = Fraction(numerator, denominator)
            if not Fraction(1, 5) <= kappa < Fraction(1, 3):
                continue
            values = ledger(kappa)
            if values["triple_weight"] != 6 - 2 * kappa:
                raise AssertionError("triple capacity identity failed")
            if values["weighted_mass"] != values["hub"]:
                raise AssertionError("hub mass identity failed")
            if values["unweighted_incidence"] != values["point_circle_second"]:
                raise AssertionError("unweighted incidence saturation failed")
            if values["weighted_second"] != values["hub"]:
                raise AssertionError("weighted dyadic saturation failed")
            if values["slot_per_plane"] != 5 - 2 * kappa:
                raise AssertionError("target-plane slot capacity failed")
            if not 0 < values["multiplicity"] <= 1:
                raise AssertionError("multiplicity cap failed")
            if values["ms_pair"] >= 3:
                raise AssertionError("pairwise MS constraint failed")
            checked += 1

    return {
        "schema": "amra.erdos1083.moderate-rich-lp-barrier.v1",
        "status": "PASS",
        "rational_kappa_cases": checked,
        "endpoint_one_fifth": {
            key: str(value) for key, value in ledger(Fraction(1, 5)).items()
        },
        "interior_one_fourth": {
            key: str(value) for key, value in ledger(Fraction(1, 4)).items()
        },
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
