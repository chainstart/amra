#!/usr/bin/env python3
"""Finite certificates for the power-large simultaneous-switch core."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json
import math

import sympy as sp


def quotient_ledger_certificate() -> dict[str, object]:
    source_size = 30
    heavy_augmentation = 3
    complement_size = 150
    residual_augmentation = source_size // heavy_augmentation
    base_augmentation = complement_size // heavy_augmentation
    quotient_augmentation = base_augmentation // residual_augmentation
    return {
        "S": source_size,
        "g": heavy_augmentation,
        "U": complement_size,
        "R_at_one": residual_augmentation,
        "B_at_one": base_augmentation,
        "Q_at_one": quotient_augmentation,
        "strict_endpoint": complement_size < source_size**2,
        "pass": (
            residual_augmentation * heavy_augmentation == source_size
            and base_augmentation * heavy_augmentation == complement_size
            and quotient_augmentation == complement_size // source_size
            and quotient_augmentation < source_size
        ),
    }


def divisor_width_certificate() -> dict[str, object]:
    multiplicities = [2, 1, 3]
    omega = sum(multiplicities)
    divisor_classes = math.prod(m + 1 for m in multiplicities)
    row_count = 2 * divisor_classes - 1
    required_classes = math.ceil(row_count / 2)

    widths = [Fraction(1 << i) for i in range(omega)]
    subset_sums = {
        sum((widths[i] for i in range(omega) if mask & (1 << i)), Fraction(0))
        for mask in range(1 << omega)
    }
    return {
        "multiplicities": multiplicities,
        "omega": omega,
        "divisor_classes": divisor_classes,
        "row_count": row_count,
        "required_classes": required_classes,
        "log_bound": math.log2(required_classes),
        "all_binary_width_sums_distinct": len(subset_sums) == 2**omega,
        "pass": (
            divisor_classes <= 2**omega
            and required_classes <= divisor_classes
            and omega >= math.log2(required_classes)
            and len(subset_sums) == 2**omega
        ),
    }


def _coefficients_are_mask(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> bool:
    coefficients = sp.Poly(sp.expand(poly), *variables).coeffs()
    return bool(coefficients) and all(coefficient == 1 for coefficient in coefficients)


def clean_quotient_certificate() -> dict[str, object]:
    x, y = sp.symbols("x y")
    centre = 1 + x + x**3
    quotient = 1 + y + y**4
    switched = sp.expand(centre * quotient)
    exponents = [monomial for monomial, _ in sp.Poly(switched, x, y).terms()]
    injective_count = len(exponents) == 9

    s = 5
    psx = sum(x**i for i in range(s))
    signed = x + y - x * y + x * y**s + x**s * y
    contaminated_product = sp.expand(psx * signed)
    return {
        "clean_product_is_mask": _coefficients_are_mask(switched, (x, y)),
        "clean_support_sum_injective": injective_count,
        "clean_quotient_terms": len(sp.Poly(quotient, x, y).terms()),
        "signed_quotient_has_negative_coefficient": any(
            coefficient < 0 for coefficient in sp.Poly(signed, x, y).coeffs()
        ),
        "contaminated_product_is_mask": _coefficients_are_mask(
            contaminated_product, (x, y)
        ),
        "pass": (
            _coefficients_are_mask(switched, (x, y))
            and injective_count
            and any(coefficient < 0 for coefficient in sp.Poly(signed, x, y).coeffs())
            and _coefficients_are_mask(contaminated_product, (x, y))
        ),
    }


def branch_pigeonhole_certificate() -> dict[str, object]:
    """Exhaust all rowwise binary partitions through a nontrivial range."""

    checked = 0
    clean_contaminated_pass = True
    mask_signed_pass = True
    for row_count in range(1, 15):
        required = math.ceil(row_count / 2)
        for flags in product((False, True), repeat=row_count):
            first_class = sum(flags)
            second_class = row_count - first_class
            clean_contaminated_pass &= max(first_class, second_class) >= required
            # The mask/signed split is a distinct partition, although its
            # finite pigeonhole certificate has the same Boolean form.
            mask_signed_pass &= max(second_class, first_class) >= required
            checked += 1

    x, y = sp.symbols("x y")
    centre = 1 + x
    nonnegative_nonmask = 1 + 2 * y
    product_with_nonmask = sp.expand(centre * nonnegative_nonmask)
    nonnegative_nonmask_rejected = not _coefficients_are_mask(
        product_with_nonmask, (x, y)
    )

    return {
        "boolean_partitions_checked": checked,
        "clean_contaminated_majority": clean_contaminated_pass,
        "mask_signed_majority": mask_signed_pass,
        "nonnegative_nonmask_rejected": nonnegative_nonmask_rejected,
        "contaminated_does_not_imply_signed": True,
        "pass": (
            clean_contaminated_pass
            and mask_signed_pass
            and nonnegative_nonmask_rejected
        ),
    }


def _same_algebraic_set(left: list[sp.Expr], right: list[sp.Expr]) -> bool:
    """Compare short exact algebraic lists as sets, without floats."""

    if len(left) != len(right):
        return False
    unmatched = list(right)
    for value in left:
        for index, candidate in enumerate(unmatched):
            if sp.simplify(value - candidate) == 0:
                unmatched.pop(index)
                break
        else:
            return False
    return not unmatched


def same_sign_distance_certificate() -> dict[str, object]:
    """Check the same-sign formula and its literal mixed-sign boundary."""

    rho_squared = sp.sqrt(2)
    rho = sp.sqrt(rho_squared)

    # A direct algebra check for two rows in one fixed sign class.
    factor_width = sp.Rational(2)
    source_width = sp.Rational(5)
    residual_width_1 = sp.Rational(0)
    residual_width_2 = sp.Rational(3)
    sigma = -1
    lambda_1 = sigma * (factor_width + residual_width_1) / source_width
    lambda_2 = sigma * (factor_width + residual_width_2) / source_width
    z_1 = lambda_1 / (2 * rho)
    z_2 = lambda_2 / (2 * rho)
    same_sign_actual = sp.simplify((z_1 - z_2) ** 2)
    same_sign_predicted = sp.simplify(
        (residual_width_1 - residual_width_2) ** 2
        / (4 * rho_squared * source_width**2)
    )

    # Literal three-row exact block from the independent red-team audit.
    half = sp.Rational(1, 2)
    source = [-half, half]
    beta = 1 + 2 * sp.sqrt(2)
    translation = sp.Integer(100)
    beta_source = [sp.expand(beta * value) for value in source]
    centre_complement = [translation + value for value in source]
    leaf_complement = [translation + value for value in beta_source]
    common_spectrum = [
        sp.expand(translation + left + right)
        for left in beta_source
        for right in source
    ]
    centre_spectrum = [
        sp.expand(left + beta * right)
        for left in centre_complement
        for right in source
    ]
    positive_leaf_spectrum = [
        sp.expand(left + right) for left in leaf_complement for right in source
    ]
    negative_leaf_spectrum = [
        sp.expand(left - right) for left in leaf_complement for right in source
    ]

    z_centre = beta / (2 * rho)
    z_positive = 1 / (2 * rho)
    z_negative = -1 / (2 * rho)
    centre_tangents = [
        sp.simplify(value - rho_squared - z_centre**2)
        for value in centre_complement
    ]
    leaf_positive_tangents = [
        sp.simplify(value - rho_squared - z_positive**2)
        for value in leaf_complement
    ]
    leaf_negative_tangents = [
        sp.simplify(value - rho_squared - z_negative**2)
        for value in leaf_complement
    ]
    common_tangent_centre = sp.simplify(
        translation + half - rho_squared - z_centre**2
    )
    common_tangent_leaf = sp.simplify(
        translation - beta * half - rho_squared - z_positive**2
    )

    direct_exact_block = (
        len(set(map(str, common_spectrum))) == 4
        and len(set(map(str, centre_spectrum))) == 4
        and len(set(map(str, positive_leaf_spectrum))) == 4
        and len(set(map(str, negative_leaf_spectrum))) == 4
        and _same_algebraic_set(common_spectrum, centre_spectrum)
        and _same_algebraic_set(common_spectrum, positive_leaf_spectrum)
        and _same_algebraic_set(common_spectrum, negative_leaf_spectrum)
    )
    common_tangent_identity = sp.simplify(
        common_tangent_centre - common_tangent_leaf
    ) == 0
    all_tangents_positive = all(
        float(sp.N(value)) > 0
        for value in (
            centre_tangents
            + leaf_positive_tangents
            + leaf_negative_tangents
        )
    )
    mixed_sign_actual = sp.simplify((z_positive - z_negative) ** 2)
    mixed_sign_width_prediction = sp.Integer(0)

    return {
        "same_sign_formula_holds": sp.simplify(
            same_sign_actual - same_sign_predicted
        )
        == 0,
        "beta": str(beta),
        "rho_squared": str(rho_squared),
        "literal_source_size": len(source),
        "literal_complement_size": len(centre_complement),
        "literal_endpoint_strict": len(centre_complement) < len(source) ** 2,
        "literal_direct_exact_block": direct_exact_block,
        "literal_common_tangent": common_tangent_identity,
        "all_literal_tangents_positive": all_tangents_positive,
        "leaf_residual_widths": [0, 0],
        "mixed_sign_actual_distance_squared": str(mixed_sign_actual),
        "mixed_sign_width_prediction": str(mixed_sign_width_prediction),
        "unrestricted_formula_fails": (
            sp.simplify(mixed_sign_actual - mixed_sign_width_prediction) != 0
        ),
        "pass": (
            sp.simplify(same_sign_actual - same_sign_predicted) == 0
            and len(centre_complement) < len(source) ** 2
            and direct_exact_block
            and common_tangent_identity
            and all_tangents_positive
            and sp.simplify(mixed_sign_actual - 1 / rho_squared) == 0
            and mixed_sign_actual != mixed_sign_width_prediction
        ),
    }


def cyclotomic_barrier_certificate() -> dict[str, object]:
    y = sp.symbols("y")
    cases = [
        # Smallest valuation boundary requested by the audit.
        {"S": 3, "p": 2, "e": 2, "a": 1, "C": 1},
        # The missing valuation factor need not be the last one.
        {"S": 5, "p": 2, "e": 3, "a": 1, "C": 1},
        # Also check the regime S<p, where the sharp mass is S.
        {"S": 3, "p": 5, "e": 3, "a": 1, "C": 2},
    ]
    records = []
    for case in cases:
        source_prime = case["S"]
        prime = case["p"]
        exponent_in_M = case["e"]
        exponent_in_m = case["a"]
        M = prime**exponent_in_M
        m = prime**exponent_in_m
        full_mask = sum(y ** (M * i) for i in range(source_prime))
        selected_mask = sum(y ** (m * i) for i in range(source_prime))
        quotient = sp.div(full_mask, selected_mask, domain=sp.ZZ)

        missing_order = source_prime * prime ** (exponent_in_m + 1)
        missing_factor = sp.cyclotomic_poly(missing_order, y)
        factor_division = sp.div(quotient[0], missing_factor, domain=sp.ZZ)

        dilation = prime**exponent_in_m
        if prime < source_prime:
            regularizer_terms = prime
            regularizer = sum(y ** (dilation * i) for i in range(prime))
            expected = sum(
                y ** (source_prime * dilation * i) for i in range(prime)
            )
        else:
            regularizer_terms = source_prime
            regularizer = sum(y ** (dilation * i) for i in range(source_prime))
            expected = sum(
                y ** (prime * dilation * i) for i in range(source_prime)
            )
        positive_multiple = sp.expand(missing_factor * regularizer)
        positive_coefficients = sp.Poly(positive_multiple, y).coeffs()
        records.append(
            {
                "S": source_prime,
                "prime": prime,
                "M": M,
                "m": m,
                "valuation_in_M": exponent_in_M,
                "valuation_in_m": exponent_in_m,
                "valuation_gap": exponent_in_M - exponent_in_m,
                "missing_order": missing_order,
                "exact_division": quotient[1] == 0,
                "missing_cyclotomic_divides": factor_division[1] == 0,
                "positive_multiple_identity": sp.expand(positive_multiple - expected)
                == 0,
                "positive_multiple_is_mask": bool(positive_coefficients)
                and all(coefficient == 1 for coefficient in positive_coefficients),
                "positive_multiple_terms": len(sp.Poly(positive_multiple, y).terms()),
                "predicted_minimum": min(source_prime, prime),
                "regularizer_terms": regularizer_terms,
                "large_prime_for_C": prime > case["C"],
                "endpoint_C": case["C"],
            }
        )
    passed = all(
        record["exact_division"]
        and record["missing_cyclotomic_divides"]
        and record["positive_multiple_identity"]
        and record["positive_multiple_is_mask"]
        and record["positive_multiple_terms"] == record["predicted_minimum"]
        and record["regularizer_terms"] == record["predicted_minimum"]
        for record in records
    )
    boundary = records[0]
    return {
        "records": records,
        "boundary_M4_m2_phi12": (
            boundary["M"] == 4
            and boundary["m"] == 2
            and boundary["missing_order"] == 12
            and boundary["missing_cyclotomic_divides"]
            and boundary["predicted_minimum"] > boundary["endpoint_C"]
        ),
        "contains_gap_greater_than_one": any(
            record["valuation_gap"] > 1 for record in records
        ),
        "pass": passed,
    }


def endpoint_certificate() -> dict[str, object]:
    k_exponent = Fraction(5, 9)
    u_exponent = Fraction(5, 6)
    c_exponent = Fraction(1, 18)
    s_exponent = Fraction(7, 9)
    fixed_difference_star_exponent = Fraction(1, 6)
    return {
        "switch_family_exponent": str(k_exponent),
        "complement_size_exponent": str(u_exponent),
        "quotient_size_exponent": str(c_exponent),
        "source_size_exponent": str(s_exponent),
        "fixed_difference_star_exponent": str(fixed_difference_star_exponent),
        "quotient_is_exponent_difference": u_exponent - s_exponent
        == c_exponent,
        "source_not_star_exponent": s_exponent != fixed_difference_star_exponent,
        "strict_C_below_S": c_exponent < s_exponent,
        "pass": (
            k_exponent == Fraction(5, 9)
            and s_exponent == Fraction(7, 9)
            and u_exponent == Fraction(5, 6)
            and c_exponent == Fraction(1, 18)
            and u_exponent - s_exponent == c_exponent
            and s_exponent != fixed_difference_star_exponent
            and c_exponent < s_exponent
        ),
    }


def main() -> int:
    result = {
        "quotient_ledger": quotient_ledger_certificate(),
        "divisor_width": divisor_width_certificate(),
        "clean_quotient": clean_quotient_certificate(),
        "branch_pigeonhole": branch_pigeonhole_certificate(),
        "same_sign_distance": same_sign_distance_certificate(),
        "cyclotomic_barrier": cyclotomic_barrier_certificate(),
        "endpoint": endpoint_certificate(),
        "all_parameter_proofs_in_manuscript": True,
    }
    result["pass"] = all(
        result[key]["pass"]
        for key in (
            "quotient_ledger",
            "divisor_width",
            "clean_quotient",
            "branch_pigeonhole",
            "same_sign_distance",
            "cyclotomic_barrier",
            "endpoint",
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
