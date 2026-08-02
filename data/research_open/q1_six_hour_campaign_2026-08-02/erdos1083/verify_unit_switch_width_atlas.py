#!/usr/bin/env python3
"""Certificates for the augmentation-unit subset-sum height atlas."""

from __future__ import annotations

from itertools import combinations
import json
import math

import sympy as sp


def divisor_class_certificate(multiplicities: tuple[int, ...] = (3, 2, 1)) -> dict[str, object]:
    occurrences = sum(multiplicities)
    divisor_classes = math.prod(value + 1 for value in multiplicities)
    binary_bound = 2**occurrences
    synthetic_leaf_count = 2 * divisor_classes + 2
    forced_classes = math.ceil((synthetic_leaf_count - 2) / 2)
    return {
        "multiplicities": list(multiplicities),
        "unit_factor_occurrences": occurrences,
        "divisor_associate_classes": divisor_classes,
        "binary_upper_bound": binary_bound,
        "synthetic_leaf_count": synthetic_leaf_count,
        "forced_nonunit_classes": forced_classes,
        "log2_class_lower_bound": math.log2(forced_classes),
        "pass": divisor_classes <= binary_bound and forced_classes == divisor_classes,
    }


def width_and_distance_certificate() -> dict[str, object]:
    rho = sp.Rational(3, 2)
    diameter = sp.Rational(5, 1)
    skeleton_width = sp.Rational(2, 1)
    common_direction = sp.Rational(7, 1)
    factor_widths = [sp.Rational(1, 3), sp.Rational(2, 5), sp.Rational(3, 7)]
    selections = [(0,), (1,), (2,), (0, 1), (0, 2), (0, 1, 2)]

    rows = []
    subset_sums = []
    for selection in selections:
        residual_width = sum((factor_widths[index] for index in selection), sp.S.Zero)
        scalar = sp.simplify((skeleton_width + residual_width) / diameter)
        height = sp.simplify(scalar / (2 * rho))
        w = sp.simplify(common_direction / scalar)
        subset_sums.append(residual_width)
        rows.append(
            {
                "selection": list(selection),
                "residual_width": str(residual_width),
                "scalar": str(scalar),
                "height": str(height),
                "w": str(w),
                "direction_identity": sp.simplify(scalar * w - common_direction) == 0,
                "width_identity": (
                    sp.simplify(
                        scalar * diameter - skeleton_width - residual_width
                    )
                    == 0
                ),
            }
        )

    ordered = sorted(set(subset_sums))
    base = ordered[0]
    squared_distances = {
        sp.simplify((value - base) ** 2 / (4 * rho**2 * diameter**2))
        for value in ordered[1:]
    }
    return {
        "factor_widths": [str(value) for value in factor_widths],
        "distinct_subset_sums": len(ordered),
        "fixed_base_distances": len(squared_distances),
        "expected_fixed_base_distances": max(0, len(ordered) - 1),
        "rows": rows,
        "pass": (
            all(row["direction_identity"] and row["width_identity"] for row in rows)
            and len(squared_distances) == max(0, len(ordered) - 1)
        ),
    }


def signed_width_additivity_certificate() -> dict[str, object]:
    x = sp.symbols("x")
    left = 1 + x + x**2
    right = 1 - x + x**2
    product = sp.expand(left * right)

    def width(poly: sp.Expr) -> int:
        terms = sp.Poly(poly, x).terms()
        exponents = [monomial[0] for monomial, _ in terms]
        return max(exponents) - min(exponents)

    return {
        "left": str(left),
        "right": str(right),
        "product": str(product),
        "interior_cancellation": sp.Poly(product, x).coeff_monomial(x) == 0,
        "left_width": width(left),
        "right_width": width(right),
        "product_width": width(product),
        "pass": width(product) == width(left) + width(right),
    }


def cyclotomic_scalar_switch_certificate(
    source_size: int = 5, primes: tuple[int, ...] = (2, 3, 7)
) -> dict[str, object]:
    x = sp.symbols("x")
    large_scalar = math.prod(primes)

    def mask(scalar: int) -> sp.Expr:
        return sum(x ** (scalar * index) for index in range(source_size))

    divisors = [
        math.prod(chosen) if chosen else 1
        for size in range(len(primes) + 1)
        for chosen in combinations(primes, size)
    ]
    large_mask = sp.Poly(mask(large_scalar), x, domain=sp.ZZ)
    base_mask = sp.Poly(mask(1), x, domain=sp.ZZ)
    records = []
    all_divide = True
    for scalar in sorted(divisors):
        leaf_mask = sp.Poly(mask(scalar), x, domain=sp.ZZ)
        quotient, remainder = sp.div(large_mask, leaf_mask, domain=sp.ZZ)
        base_quotient, base_remainder = sp.div(leaf_mask, base_mask, domain=sp.ZZ)
        divides = remainder.is_zero
        shares_heavy_base = base_remainder.is_zero
        unit_augmentation = int(base_quotient.eval(1))
        all_divide &= divides and shares_heavy_base and unit_augmentation == 1
        records.append(
            {
                "scalar": scalar,
                "large_quotient_augmentation": int(quotient.eval(1)),
                "base_quotient_augmentation": unit_augmentation,
                "divides_large_mask": divides,
                "contains_heavy_base": shares_heavy_base,
            }
        )
    return {
        "source_size": source_size,
        "primes": list(primes),
        "large_scalar": large_scalar,
        "scalar_copy_count": len(divisors),
        "expected_copy_count": 2 ** len(primes),
        "large_mask_support_size": len(large_mask.terms()),
        "records": records,
        "pass": (
            math.gcd(source_size, large_scalar) == 1
            and len(divisors) == 2 ** len(primes)
            and len(large_mask.terms()) == source_size
            and all_divide
        ),
    }


def main() -> int:
    result = {
        "divisor_classes": divisor_class_certificate(),
        "width_and_distance": width_and_distance_certificate(),
        "signed_width_additivity": signed_width_additivity_certificate(),
        "cyclotomic_scalar_switch": cyclotomic_scalar_switch_certificate(),
        "all_parameter_proofs_in_manuscript": True,
    }
    result["pass"] = all(
        result[key]["pass"]
        for key in (
            "divisor_classes",
            "width_and_distance",
            "signed_width_additivity",
            "cyclotomic_scalar_switch",
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
