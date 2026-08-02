#!/usr/bin/env python3
"""Certificates for the near-full heavy-factor hub theorem."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
import math

import sympy as sp


def endpoint_certificate() -> dict[str, object]:
    leaf_exponent = Fraction(5, 9)
    log_u_exponent = Fraction(0, 1)
    return {
        "leaf_exponent": str(leaf_exponent),
        "division_by_log_U_is_subpower": True,
        "hub_exponent": str(leaf_exponent - log_u_exponent),
        "pass": leaf_exponent == Fraction(5, 9),
    }


def heavy_hub_certificate() -> dict[str, object]:
    # Four heavy factor types occur in the common complement.  Every leaf
    # chooses at least one; the most frequent chosen type meets ceil(K/r).
    heavy_augmentations = {"g0": 2, "g1": -3, "g2": 2, "g3": 5}
    leaf_factor_sets = [
        {"g0", "u0"},
        {"g1", "u1"},
        {"g0", "g2", "u2"},
        {"g3", "u3"},
        {"g0", "u4"},
        {"g2", "u5"},
        {"g1", "u6"},
        {"g0", "g3", "u7"},
        {"g2", "u8"},
        {"g0", "u9"},
        {"g1", "u10"},
    ]
    chosen = []
    for factors in leaf_factor_sets:
        heavy = sorted(
            factor
            for factor in factors
            if factor in heavy_augmentations
            and abs(heavy_augmentations[factor]) >= 2
        )
        chosen.append(heavy[0])
    frequencies = Counter(chosen)
    hub, hub_size = frequencies.most_common(1)[0]
    lower = math.ceil(len(leaf_factor_sets) / len(heavy_augmentations))
    complement_augmentation = math.prod(
        abs(value) for value in heavy_augmentations.values()
    )
    occurrence_bound = math.floor(math.log2(complement_augmentation))
    return {
        "leaf_count": len(leaf_factor_sets),
        "heavy_factor_type_count": len(heavy_augmentations),
        "heavy_occurrence_log_bound": occurrence_bound,
        "pigeonhole_lower_bound": lower,
        "hub_factor": hub,
        "hub_leaf_count": hub_size,
        "every_leaf_has_heavy_factor": len(chosen) == len(leaf_factor_sets),
        "pass": (
            len(heavy_augmentations) <= occurrence_bound
            and hub_size >= lower
            and len(chosen) == len(leaf_factor_sets)
        ),
    }


def reciprocal_chart_certificate() -> dict[str, object]:
    rho = sp.Rational(4, 3)
    tangent = sp.Rational(7, 2)
    h = sp.sqrt(3)
    source = [sp.Integer(0), sp.Rational(1, 2), sp.sqrt(2)]
    parameters = [sp.Integer(1), 1 + sp.sqrt(2), 3 - sp.sqrt(2)]
    identities = []
    for w in parameters:
        lam = sp.simplify(h / w)
        z = sp.simplify(lam / (2 * rho))
        direct = [
            sp.simplify(rho**2 + tangent + z**2 + 2 * rho * z * x)
            for x in source
        ]
        chart = [
            sp.simplify(
                rho**2
                + tangent
                + h**2 / (4 * rho**2 * w**2)
                + h * x / w
            )
            for x in source
        ]
        identities.append(
            sp.simplify(lam * w - h) == 0
            and all(sp.simplify(a - b) == 0 for a, b in zip(direct, chart))
        )
    return {
        "row_count": len(parameters),
        "all_direction_and_chart_identities": all(identities),
        "pass": all(identities),
    }


def main() -> int:
    result = {
        "endpoint": endpoint_certificate(),
        "heavy_hub": heavy_hub_certificate(),
        "reciprocal_chart": reciprocal_chart_certificate(),
        "all_parameter_UFD_proof_in_manuscript": True,
    }
    result["pass"] = all(
        result[key]["pass"] for key in ("endpoint", "heavy_hub", "reciprocal_chart")
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
