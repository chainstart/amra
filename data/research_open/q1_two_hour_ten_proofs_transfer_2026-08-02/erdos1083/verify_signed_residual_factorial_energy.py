#!/usr/bin/env python3
"""Finite verification for the signed-residual factorial-energy theorem."""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import cmath
import json
import math


Polynomial = dict[int, int]
Polynomial2 = dict[tuple[int, int], int]


def clean(poly: Counter[int] | Polynomial) -> Polynomial:
    return {exponent: int(coefficient) for exponent, coefficient in poly.items() if coefficient}


def mask(exponents: set[int] | tuple[int, ...] | list[int]) -> Polynomial:
    return {exponent: 1 for exponent in exponents}


def convolve(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Counter[int] = Counter()
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            result[left_exponent + right_exponent] += left_coefficient * right_coefficient
    return clean(result)


def is_mask(poly: Polynomial) -> bool:
    return bool(poly) and all(coefficient == 1 for coefficient in poly.values())


def augmentation(poly: Polynomial) -> int:
    return sum(poly.values())


def norm_squared(poly: Polynomial) -> int:
    return sum(coefficient * coefficient for coefficient in poly.values())


def factorial_energy(poly: Polynomial) -> int:
    numerator = sum(coefficient * (coefficient - 1) for coefficient in poly.values())
    assert numerator % 2 == 0
    return numerator // 2


def negative_mass(poly: Polynomial) -> int:
    return sum(-coefficient for coefficient in poly.values() if coefficient < 0)


def positive_excess(poly: Polynomial) -> int:
    return sum(coefficient - 1 for coefficient in poly.values() if coefficient > 0)


def correlation(poly: Polynomial, difference: int) -> int:
    return sum(
        coefficient * poly.get(exponent - difference, 0)
        for exponent, coefficient in poly.items()
    )


def ordered_correlation_debt(source: set[int], quotient: Polynomial) -> int:
    return sum(
        correlation(quotient, right - left)
        for left in source
        for right in source
        if left != right
    )


def difference_multiplicities(source: set[int]) -> Counter[int]:
    return Counter(
        right - left
        for left in source
        for right in source
        if left != right
    )


def popular_difference_certificate(source: set[int], quotient: Polynomial) -> dict[str, object]:
    positive = {exponent: coefficient for exponent, coefficient in quotient.items() if coefficient > 0}
    negative = {exponent: -coefficient for exponent, coefficient in quotient.items() if coefficient < 0}
    source_differences = difference_multiplicities(source)
    weights: Counter[int] = Counter()
    for positive_exponent, positive_coefficient in positive.items():
        for negative_exponent, negative_coefficient in negative.items():
            weights[positive_exponent - negative_exponent] += (
                positive_coefficient * negative_coefficient
            )
    weighted_overlap = sum(
        weight * source_differences[difference]
        for difference, weight in weights.items()
    )
    negative_total = sum(negative.values())
    positive_total = sum(positive.values())
    source_size = len(source)
    mu = max(source_differences.values(), default=0)
    best_difference, best_overlap = max(
        ((difference, source_differences[difference]) for difference in weights),
        key=lambda item: item[1],
    )
    lower_cost = max(1, math.ceil(source_size / mu) - augmentation(quotient))
    return {
        "negative_mass": negative_total,
        "positive_mass": positive_total,
        "weighted_overlap": weighted_overlap,
        "required_overlap_mass": source_size * negative_total,
        "total_pair_weight": positive_total * negative_total,
        "best_quotient_difference": best_difference,
        "best_source_overlap": best_overlap,
        "popular_overlap_threshold": source_size / positive_total,
        "mu": mu,
        "factorial_energy": factorial_energy(quotient),
        "lower_cost": lower_cost,
        "pass": (
            negative_total > 0
            and weighted_overlap >= source_size * negative_total
            and best_overlap + 1e-12 >= source_size / positive_total
            and factorial_energy(quotient) >= negative_total >= lower_cost
        ),
    }


def closest_mask_certificate(poly: Polynomial) -> dict[str, object]:
    target_mass = augmentation(poly)
    positive_support = sorted(exponent for exponent, coefficient in poly.items() if coefficient > 0)
    if len(positive_support) >= target_mass:
        target = set(positive_support[:target_mass])
    else:
        target = set(positive_support)
        candidate = (max(poly) + 1) if poly else 0
        while len(target) < target_mass:
            if candidate not in poly:
                target.add(candidate)
            candidate += 1
    target_poly = mask(target)
    union = set(poly) | set(target_poly)
    distance = sum(abs(poly.get(exponent, 0) - target_poly.get(exponent, 0)) for exponent in union)
    return {
        "target": sorted(target),
        "target_is_mask": is_mask(target_poly),
        "target_mass": augmentation(target_poly),
        "l1_distance": distance,
        "twice_factorial_energy": 2 * factorial_energy(poly),
        "bound_holds": distance <= 2 * factorial_energy(poly),
    }


def dft(poly: Polynomial, modulus: int) -> list[complex]:
    return [
        sum(
            coefficient * cmath.exp(-2j * math.pi * frequency * (exponent % modulus) / modulus)
            for exponent, coefficient in poly.items()
        )
        for frequency in range(modulus)
    ]


def exact_identity_certificate(
    source: set[int], quotient: Polynomial, expected_product: set[int]
) -> dict[str, object]:
    source_poly = mask(source)
    product = convolve(source_poly, quotient)
    source_size = len(source)
    delta = factorial_energy(quotient)
    debt = ordered_correlation_debt(source, quotient)
    return {
        "source": sorted(source),
        "quotient": sorted(quotient.items()),
        "product": sorted(product),
        "product_is_expected_mask": product == mask(expected_product),
        "augmentation": augmentation(quotient),
        "norm_defect": norm_squared(quotient) - augmentation(quotient),
        "twice_factorial_energy": 2 * delta,
        "negative_mass": negative_mass(quotient),
        "positive_excess": positive_excess(quotient),
        "factorial_lower_bound": delta >= negative_mass(quotient) + positive_excess(quotient),
        "correlation_debt": debt,
        "expected_correlation_debt": -2 * source_size * delta,
        "edit_certificate": closest_mask_certificate(quotient),
        "popular_difference_certificate": popular_difference_certificate(source, quotient),
        "pass": (
            product == mask(expected_product)
            and norm_squared(quotient) - augmentation(quotient) == 2 * delta
            and delta >= negative_mass(quotient) + positive_excess(quotient)
            and debt == -2 * source_size * delta
            and closest_mask_certificate(quotient)["bound_holds"]
            and popular_difference_certificate(source, quotient)["pass"]
        ),
    }


def prime_nonvanishing_certificate() -> dict[str, object]:
    modulus = 7
    tolerance = 1e-9
    records = []
    for source_size in range(1, modulus):
        minimum = float("inf")
        checked = 0
        for source_tuple in combinations(range(modulus), source_size):
            values = dft(mask(set(source_tuple)), modulus)
            minimum = min(minimum, *(abs(value) for value in values))
            checked += 1
        records.append(
            {
                "source_size": source_size,
                "subsets_checked": checked,
                "minimum_fourier_magnitude": minimum,
                "nonvanishing": minimum > tolerance,
            }
        )
    return {
        "prime_modulus": modulus,
        "records": records,
        "all_subsets_below_prime_nonvanishing": all(record["nonvanishing"] for record in records),
        "pass": all(record["nonvanishing"] for record in records),
    }


def common_x_reciprocal_frame_certificate() -> dict[str, object]:
    # X={0,1,2}; F_0=P_X and F_1=P_{2X}.  The common mask is F_1.
    # F_0(1-x+x^2)=F_1 and F_1*1=F_1.
    source_zero = {0, 1, 2}
    sources = [source_zero, {0, 2, 4}]
    quotients = [{0: 1, 1: -1, 2: 1}, {0: 1}]
    common_mask = mask({0, 2, 4})
    modulus = 11
    source_size = 3
    quotient_mass = 1
    tolerance = 2e-8

    common_fourier = dft(common_mask, modulus)
    source_zero_fourier = dft(mask(source_zero), modulus)
    rows = []
    aggregate_reciprocal = 0.0
    for source, quotient in zip(sources, quotients, strict=True):
        source_fourier = dft(mask(source), modulus)
        minimum_denominator = min(abs(value) for value in source_fourier)
        reciprocal_norm = sum(
            abs(common_value) ** 2 / abs(source_value) ** 2
            for common_value, source_value in zip(common_fourier, source_fourier, strict=True)
        ) / modulus
        weighted_debt = sum(
            (source_size - abs(zero_value) ** 2)
            * abs(common_value) ** 2
            / abs(source_value) ** 2
            for zero_value, common_value, source_value in zip(
                source_zero_fourier, common_fourier, source_fourier, strict=True
            )
        ) / modulus
        delta = factorial_energy(quotient)
        second_product = convolve(mask(source_zero), quotient)
        row = {
            "source": sorted(source),
            "quotient": sorted(quotient.items()),
            "common_product_identity": convolve(mask(source), quotient) == common_mask,
            "second_product_is_mask": is_mask(second_product),
            "minimum_fourier_denominator": minimum_denominator,
            "reciprocal_norm": reciprocal_norm,
            "expected_reciprocal_norm": quotient_mass + 2 * delta,
            "reciprocal_excess": reciprocal_norm - quotient_mass,
            "expected_reciprocal_excess": 2 * delta,
            "weighted_debt": weighted_debt,
            "expected_weighted_debt": 2 * source_size * delta,
            "factorial_energy": delta,
        }
        row["pass"] = (
            row["common_product_identity"]
            and row["second_product_is_mask"]
            and minimum_denominator > tolerance
            and abs(reciprocal_norm - (quotient_mass + 2 * delta)) < tolerance
            and abs(weighted_debt - 2 * source_size * delta) < tolerance
        )
        rows.append(row)
        aggregate_reciprocal += reciprocal_norm

    aggregate_excess = aggregate_reciprocal - len(rows) * quotient_mass
    signed_rows = sum(any(coefficient < 0 for coefficient in quotient.values()) for quotient in quotients)
    gcd_failure_identity = convolve(mask(source_zero), quotients[0]) == common_mask
    return {
        "modulus": modulus,
        "source_size": source_size,
        "quotient_mass": quotient_mass,
        "rows": rows,
        "aggregate_reciprocal_excess": aggregate_excess,
        "expected_aggregate_excess": 2 * sum(factorial_energy(quotient) for quotient in quotients),
        "signed_rows": signed_rows,
        "signed_row_bound": aggregate_excess / 2,
        "common_X_scalar_copies": True,
        "transversality_fails": gcd_failure_identity,
        "power_large_family": False,
        "pass": (
            all(row["pass"] for row in rows)
            and abs(
                aggregate_excess
                - 2 * sum(factorial_energy(quotient) for quotient in quotients)
            )
            < tolerance
            and signed_rows <= aggregate_excess / 2 + tolerance
            and gcd_failure_identity
        ),
    }


def two_multiplier_debt_certificate() -> dict[str, object]:
    quotient = {0: 1, 3: 1, 4: -1, 6: 1}
    source_zero = {0, 1, 2}
    source_double = {0, 2, 4}
    zero_product = convolve(mask(source_zero), quotient)
    double_product = convolve(mask(source_double), quotient)
    delta = factorial_energy(quotient)
    zero_debt = ordered_correlation_debt(source_zero, quotient)
    double_debt = ordered_correlation_debt(source_double, quotient)
    positive_support = {exponent for exponent, coefficient in quotient.items() if coefficient > 0}
    negative_support = {exponent for exponent, coefficient in quotient.items() if coefficient < 0}
    negative_point = next(iter(negative_support))
    zero_cover = {
        source + negative_point for source in source_zero
    }.issubset({source + positive for source in source_zero for positive in positive_support})
    double_cover = {
        source + negative_point for source in source_double
    }.issubset({source + positive for source in source_double for positive in positive_support})
    return {
        "quotient": sorted(quotient.items()),
        "factorial_energy": delta,
        "zero_product": sorted(zero_product),
        "double_product": sorted(double_product),
        "both_products_are_masks": is_mask(zero_product) and is_mask(double_product),
        "zero_debt": zero_debt,
        "double_debt": double_debt,
        "expected_debt": -2 * len(source_zero) * delta,
        "minimum_debt_normal_form": (
            delta == 1
            and len(negative_support) == 1
            and len(positive_support) == augmentation(quotient) + 1
        ),
        "common_cancellation_alphabet": sorted(
            positive - negative_point for positive in positive_support
        ),
        "zero_source_cover": zero_cover,
        "double_source_cover": double_cover,
        "pass": (
            is_mask(zero_product)
            and is_mask(double_product)
            and delta == 1
            and zero_debt == double_debt == -2 * len(source_zero) * delta
            and zero_cover
            and double_cover
        ),
    }


def aperiodic_escape_debt_certificate() -> dict[str, object]:
    source = {0, 1, 4}
    quotient = {0: 1, 4: -1, 5: 1, 7: 1}
    expected = {0, 1, 6, 7, 9, 11}
    return exact_identity_certificate(source, quotient, expected)


def stable_collision_ledger_certificate() -> dict[str, object]:
    examples = [
        ({0, 1}, {0: 1, 1: 1}),
        ({0, 2, 5}, {0: 2, 1: -1, 4: 1}),
        ({0, 1, 4}, {0: 1, 4: -1, 5: 1, 7: 1}),
    ]
    records = []
    for source, quotient in examples:
        product = convolve(mask(source), quotient)
        off_diagonal = ordered_correlation_debt(source, quotient)
        right_side = 2 * factorial_energy(product) - 2 * len(source) * factorial_energy(quotient)
        records.append(
            {
                "source": sorted(source),
                "quotient": sorted(quotient.items()),
                "product": sorted(product.items()),
                "product_factorial_energy": factorial_energy(product),
                "quotient_factorial_energy": factorial_energy(quotient),
                "off_diagonal": off_diagonal,
                "right_side": right_side,
                "identity": off_diagonal == right_side,
            }
        )

    shared_quotient = {0: 1, 3: 1, 4: -1, 6: 1}
    source_zero = {0, 1, 2}
    source_double = {0, 2, 4}
    output_zero = convolve(mask(source_zero), shared_quotient)
    output_double = convolve(mask(source_double), shared_quotient)
    debt_difference = (
        ordered_correlation_debt(source_zero, shared_quotient)
        - ordered_correlation_debt(source_double, shared_quotient)
    )
    defect_difference = 2 * (
        factorial_energy(output_zero) - factorial_energy(output_double)
    )
    collision_source = {0, 1}
    collision_quotient = {0: 1, 1: -1, 2: 1, 3: 1}
    collision_product = convolve(mask(collision_source), collision_quotient)
    collision_popular = popular_difference_certificate(
        collision_source, collision_quotient
    )
    return {
        "records": records,
        "two_multiplier_debt_difference": debt_difference,
        "two_multiplier_twice_output_defect_difference": defect_difference,
        "nonnegative_collision_product": sorted(collision_product.items()),
        "nonnegative_collision_is_not_mask": (
            all(coefficient >= 0 for coefficient in collision_product.values())
            and not is_mask(collision_product)
        ),
        "nonnegative_collision_popular_difference": collision_popular,
        "outer_geometric_extraction_proved": False,
        "pass": (
            all(record["identity"] for record in records)
            and debt_difference == defect_difference
            and all(coefficient >= 0 for coefficient in collision_product.values())
            and not is_mask(collision_product)
            and collision_popular["pass"]
        ),
    }


def convolve2(left: Polynomial2, right: Polynomial2) -> Polynomial2:
    result: Counter[tuple[int, int]] = Counter()
    for (left_x, left_y), left_coefficient in left.items():
        for (right_x, right_y), right_coefficient in right.items():
            result[(left_x + right_x, left_y + right_y)] += (
                left_coefficient * right_coefficient
            )
    return {exponent: int(coefficient) for exponent, coefficient in result.items() if coefficient}


def correlation2(poly: Polynomial2, difference: tuple[int, int]) -> int:
    dx, dy = difference
    return sum(
        coefficient * poly.get((x - dx, y - dy), 0)
        for (x, y), coefficient in poly.items()
    )


def full_transverse_minimum_debt_certificate() -> dict[str, object]:
    records = []
    for source_size in range(4, 13):
        source_x = {(index, 0): 1 for index in range(source_size)}
        source_y = {(0, index): 1 for index in range(source_size)}
        quotient: Polynomial2 = {
            (1, 0): 1,
            (0, 1): 1,
            (1, 1): -1,
            (1, source_size): 1,
            (source_size, 1): 1,
        }
        product_x = convolve2(source_x, quotient)
        product_y = convolve2(source_y, quotient)
        delta_numerator = sum(
            coefficient * (coefficient - 1) for coefficient in quotient.values()
        )
        delta = delta_numerator // 2
        debt_x = sum(
            correlation2(quotient, (right - left, 0))
            for left in range(source_size)
            for right in range(source_size)
            if left != right
        )
        debt_y = sum(
            correlation2(quotient, (0, right - left))
            for left in range(source_size)
            for right in range(source_size)
            if left != right
        )
        record = {
            "source_size": source_size,
            "quotient_augmentation": sum(quotient.values()),
            "strict_augmentation": sum(quotient.values()) < source_size,
            "factorial_energy": delta,
            "x_product_is_mask": is_mask(product_x),
            "y_product_is_mask": is_mask(product_y),
            "x_product_terms": len(product_x),
            "y_product_terms": len(product_y),
            "x_debt": debt_x,
            "y_debt": debt_y,
            "expected_debt": -2 * source_size * delta,
        }
        record["pass"] = (
            record["strict_augmentation"]
            and delta == 1
            and record["x_product_is_mask"]
            and record["y_product_is_mask"]
            and len(product_x) == len(product_y) == 3 * source_size
            and debt_x == debt_y == -2 * source_size
        )
        records.append(record)
    return {
        "source_sizes_checked": [record["source_size"] for record in records],
        "records": records,
        "geometric_transversality_and_euclidean_realization_proved_in_prior_manuscript": True,
        "power_large_family": False,
        "pass": all(record["pass"] for record in records),
    }


def run_all() -> dict[str, object]:
    result = {
        "prime_nonvanishing": prime_nonvanishing_certificate(),
        "common_x_reciprocal_frame": common_x_reciprocal_frame_certificate(),
        "two_multiplier_debt": two_multiplier_debt_certificate(),
        "aperiodic_escape_debt": aperiodic_escape_debt_certificate(),
        "full_transverse_minimum_debt": full_transverse_minimum_debt_certificate(),
        "stable_collision_ledger": stable_collision_ledger_certificate(),
        "all_parameter_proofs_in_manuscript": True,
        "original_problem_proved": False,
    }
    result["pass"] = all(
        result[key]["pass"]
        for key in (
            "prime_nonvanishing",
            "common_x_reciprocal_frame",
            "two_multiplier_debt",
            "aperiodic_escape_debt",
            "full_transverse_minimum_debt",
            "stable_collision_ledger",
        )
    )
    return result


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
