#!/usr/bin/env python3
"""Certificates for heavy-factor synchronization and reciprocal chart."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
import math

import sympy as sp


Q = Fraction


def entropy_margin_certificate() -> dict[str, object]:
    leaf = Q(5, 9)
    log_u = Q(5, 6)
    log_c = Q(1, 18)
    ratio = log_c / log_u
    entropy = -float(ratio) * math.log2(float(ratio)) - (
        1.0 - float(ratio)
    ) * math.log2(1.0 - float(ratio))
    pattern_exponent = float(log_u) * entropy
    beta = float(leaf) - pattern_exponent
    return {
        "leaf_exponent": str(leaf),
        "log_U_exponent": str(log_u),
        "log_C_exponent": str(log_c),
        "entropy_ratio": str(ratio),
        "binary_entropy": entropy,
        "pattern_exponent": pattern_exponent,
        "synchronized_leaf_exponent": beta,
        "positive_margin": beta > 0.26,
        "pass": ratio == Q(1, 15) and 0.26108 < beta < 0.26110,
    }


def omitted_pattern_certificate(ell: int = 7, r: int = 2) -> dict[str, object]:
    occurrences = tuple(range(ell))
    patterns = [
        frozenset(pattern)
        for size in range(r + 1)
        for pattern in combinations(occurrences, size)
    ]
    binomial_tail = sum(math.comb(ell, size) for size in range(r + 1))

    # Repeat patterns nonuniformly to make a finite leaf family.
    leaf_patterns = patterns + patterns[:11] + patterns[:4]
    multiplicities = {
        pattern: leaf_patterns.count(pattern) for pattern in set(leaf_patterns)
    }
    largest_class = max(multiplicities.values())
    pigeonhole_bound = math.ceil(len(leaf_patterns) / len(patterns))

    # The selected heavy skeleton is the complement of the omitted pattern.
    chosen_pattern = max(multiplicities, key=multiplicities.get)
    common_skeleton = frozenset(occurrences) - chosen_pattern
    agreeing = [
        pattern for pattern in leaf_patterns if pattern == chosen_pattern
    ]
    return {
        "heavy_occurrences": ell,
        "maximum_omitted": r,
        "number_of_patterns": len(patterns),
        "binomial_tail": binomial_tail,
        "leaf_count": len(leaf_patterns),
        "largest_pattern_class": largest_class,
        "pigeonhole_bound": pigeonhole_bound,
        "common_skeleton_size": len(common_skeleton),
        "agreeing_leaf_count": len(agreeing),
        "pass": (
            len(patterns) == binomial_tail
            and largest_class >= pigeonhole_bound
            and len(agreeing) == largest_class
        ),
    }


def signed_quotient_firewall_certificate() -> dict[str, object]:
    x, y = sp.symbols("x y")
    quotient = x + y - x * y + x * y**2 + x**2 * y
    left = sp.Poly(sp.expand((1 + x) * quotient), x, y)
    right = sp.Poly(sp.expand((1 + y) * quotient), x, y)
    product = sp.Poly(sp.expand((1 + x) * (1 + y) * quotient), x, y)

    def is_mask(poly: sp.Poly) -> bool:
        return all(coefficient in (0, 1) for coefficient in poly.coeffs())

    quotient_poly = sp.Poly(quotient, x, y)
    has_negative = any(coefficient < 0 for coefficient in quotient_poly.coeffs())
    return {
        "quotient_has_negative_coefficient": has_negative,
        "x_product_is_mask": is_mask(left),
        "y_product_is_mask": is_mask(right),
        "double_product_is_mask": is_mask(product),
        "quotient_augmentation": int(quotient.subs({x: 1, y: 1})),
        "left_support_size": len(left.terms()),
        "right_support_size": len(right.terms()),
        "pass": is_mask(left) and is_mask(right) and is_mask(product) and has_negative,
    }


def reciprocal_chart_certificate() -> dict[str, object]:
    rho = sp.Rational(3, 2)
    tangent = sp.Rational(5, 1)
    h = sp.sqrt(5)
    source = [sp.Integer(0), sp.Integer(1), sp.sqrt(2)]
    parameters = [sp.Integer(1), 1 + sp.sqrt(2), 2 - sp.sqrt(2)]

    rows = []
    all_equal = True
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
        equality = all(sp.simplify(a - b) == 0 for a, b in zip(direct, chart))
        all_equal &= equality and sp.simplify(lam * w - h) == 0
        rows.append(
            {
                "w": str(w),
                "lambda": str(lam),
                "height": str(z),
                "cell": [str(value) for value in direct],
                "chart_identity": equality,
            }
        )
    return {
        "rho": str(rho),
        "tangent": str(tangent),
        "common_direction": str(h),
        "rows": rows,
        "all_chart_identities_hold": all_equal,
        "pass": all_equal,
    }


def main() -> int:
    result = {
        "entropy_margin": entropy_margin_certificate(),
        "omitted_patterns": omitted_pattern_certificate(),
        "signed_quotient_firewall": signed_quotient_firewall_certificate(),
        "reciprocal_chart": reciprocal_chart_certificate(),
        "all_parameter_UFD_and_entropy_proof_in_manuscript": True,
    }
    result["pass"] = all(
        result[key]["pass"]
        for key in (
            "entropy_margin",
            "omitted_patterns",
            "signed_quotient_firewall",
            "reciprocal_chart",
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
