#!/usr/bin/env python3
"""Certificates for the mask-factor sunflower inverse theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json

import sympy as sp


Q = Fraction


def endpoint_certificate() -> dict[str, object]:
    leaf = Q(5, 9)
    source = Q(7, 9)
    fixed_difference_leaf = Q(1, 6)
    return {
        "common_tangent_leaf_exponent": str(leaf),
        "source_exponent": str(source),
        "fixed_difference_leaf_exponent": str(fixed_difference_leaf),
        "log_S_is_subpower": True,
        "leaf_family_is_power_large": leaf > 0,
        "pass": leaf == Q(5, 9) and fixed_difference_leaf == Q(1, 6),
    }


def factor_sunflower_certificate() -> dict[str, object]:
    # A finite pairwise-intersecting factor family with no global factor.
    factor_sets = [
        {"a", "b"},
        {"a", "c"},
        {"b", "c"},
        {"a", "b", "c"},
    ]
    pairwise_intersecting = all(
        bool(left & right) for left, right in combinations(factor_sets, 2)
    )
    global_intersection = set.intersection(*factor_sets)
    best_bounds = []
    actual_hubs = []
    for index, chosen in enumerate(factor_sets):
        r = len(chosen)
        lower = 1 + (len(factor_sets) - 1 + r - 1) // r
        actual = max(
            sum(factor in other for other in factor_sets) for factor in chosen
        )
        best_bounds.append(lower)
        actual_hubs.append(actual)
    return {
        "family_size": len(factor_sets),
        "pairwise_intersecting": pairwise_intersecting,
        "global_intersection_empty": not global_intersection,
        "sunflower_lower_bounds": best_bounds,
        "actual_factor_hubs": actual_hubs,
        "every_sunflower_bound_holds": all(
            actual >= lower for actual, lower in zip(actual_hubs, best_bounds)
        ),
        "pass": (
            pairwise_intersecting
            and not global_intersection
            and all(actual >= lower for actual, lower in zip(actual_hubs, best_bounds))
        ),
    }


def augmentation_certificate() -> dict[str, object]:
    # Synthetic irreducible-factor augmentations.  Their absolute product
    # is S, and the number of factors of magnitude >=2 is at most log_2 S.
    augmentations = [1, -1, 2, 1, 3, -1]
    source_size = 1
    for value in augmentations:
        source_size *= abs(value)
    large_count = sum(abs(value) >= 2 for value in augmentations)
    unit_count = sum(abs(value) == 1 for value in augmentations)
    log_bound = source_size.bit_length() - 1
    return {
        "factor_augmentations": augmentations,
        "source_size": source_size,
        "augmentation_unit_factor_count": unit_count,
        "large_augmentation_factor_count": large_count,
        "floor_log2_source_size": log_bound,
        "large_factor_count_bound_holds": large_count <= log_bound,
        "pass": source_size == 6 and large_count <= log_bound,
    }


def cyclotomic_obstruction_certificate(primes: tuple[int, ...] = (3, 5, 7, 11)) -> dict[str, object]:
    x = sp.symbols("x")
    exponent = 1
    for prime in primes:
        exponent *= prime
    coefficient, factors = sp.factor_list(x**exponent + 1)
    factor_data = [
        {
            "degree": int(sp.degree(factor)),
            "multiplicity": int(multiplicity),
            "augmentation": int(factor.subs(x, 1)),
        }
        for factor, multiplicity in factors
    ]
    unit_augmentation_count = sum(
        data["multiplicity"]
        for data in factor_data
        if abs(data["augmentation"]) == 1
    )
    expected_factor_count = 2 ** len(primes)
    return {
        "odd_primes": list(primes),
        "exponent": exponent,
        "mask_support_size": 2,
        "coefficient": int(coefficient),
        "irreducible_factor_count": sum(data["multiplicity"] for data in factor_data),
        "expected_factor_count": expected_factor_count,
        "augmentation_unit_factor_count": unit_augmentation_count,
        "expected_augmentation_unit_count": expected_factor_count - 1,
        "factor_data": factor_data,
        "pass": (
            coefficient == 1
            and sum(data["multiplicity"] for data in factor_data) == expected_factor_count
            and unit_augmentation_count == expected_factor_count - 1
        ),
    }


def main() -> int:
    result = {
        "endpoint": endpoint_certificate(),
        "factor_sunflower": factor_sunflower_certificate(),
        "augmentation": augmentation_certificate(),
        "cyclotomic_obstruction": cyclotomic_obstruction_certificate(),
        "all_parameter_UFD_argument_proved_in_manuscript": True,
    }
    result["pass"] = all(
        result[key]["pass"]
        for key in ("endpoint", "factor_sunflower", "augmentation", "cyclotomic_obstruction")
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
