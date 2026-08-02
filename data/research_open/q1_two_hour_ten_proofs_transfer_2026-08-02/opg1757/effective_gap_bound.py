#!/usr/bin/env python3
"""Compute a rigorous (very large) effective threshold for the gap theorem.

The companion note EFFECTIVE_GAP_BOUND.md proves that the integer printed as
S_gap_effective is a valid upper bound.  All arithmetic used to construct the
bound is exact integer or Fraction arithmetic.
"""

from __future__ import annotations

import math
from fractions import Fraction

import sympy as sp

from verify_complete_log_layer import (
    B,
    EXPECTED_OLD_RECURRENCE_SHA256,
    S,
    X,
    even_w_components,
    odd_w_components,
    page_recurrence_components,
    source_hash,
)


K_CUTOFF = 1000
GEOMETRY_THRESHOLD = 58_564  # 242^2


def coefficient_data(
    components: dict[int, sp.Expr],
) -> tuple[tuple[int, int, int, int, int, int], ...]:
    """Return (base, shift, degree, lc, lower_l1, total_l1)."""

    result = []
    for base, expression in components.items():
        for (shift,), coefficient in sp.Poly(expression, B).terms():
            coefficients = [
                int(value) for value in sp.Poly(coefficient, S).all_coeffs()
            ]
            leading = coefficients[0]
            lower_l1 = sum(abs(value) for value in coefficients[1:])
            result.append(
                (
                    base,
                    shift,
                    len(coefficients) - 1,
                    leading,
                    lower_l1,
                    abs(leading) + lower_l1,
                )
            )
    return tuple(result)


def shifted_nonnegative(expression: sp.Expr, start: int) -> tuple[bool, int]:
    polynomial = sp.Poly(sp.expand(expression.subs(S, X + start)), B, X)
    coefficients = polynomial.coeffs()
    return (
        all(value >= 0 for value in coefficients),
        sum(1 if value > 0 else 0 for value in coefficients),
    )


def falling(k: int, j: int) -> int:
    return math.prod(range(k - j + 1, k + 1)) if j else 1


def fixed_index_threshold(
    components: dict[int, sp.Expr],
    exponent_offset: int,
    top_height: int,
    first_index: int,
) -> dict[str, int]:
    """Cauchy-style threshold for all first_index <= k < K_CUTOFF.

    Multiplication by k! clears every factorial in the leading coefficient
    and in the error majorant, so the calculation is integer-only.
    """

    data = coefficient_data(components)
    threshold = 1
    threshold_index = first_index
    maximum_binomial_error = 0
    for k in range(first_index, K_CUTOFF):
        leading_scaled = 0
        error_scaled = 0
        for base, shift, degree, lc, lower_l1, total_l1 in data:
            if shift > k:
                continue
            residual = k - shift
            binomial_scaled = (2 * base) ** residual * falling(k, shift)
            binomial_error = residual * (
                abs(exponent_offset) + residual
            )
            maximum_binomial_error = max(
                maximum_binomial_error, binomial_error
            )
            if degree + residual == k + top_height:
                leading_scaled += lc * binomial_scaled
                error_scaled += (
                    abs(lc) * binomial_error + 2 * lower_l1
                ) * binomial_scaled
            else:
                if degree + residual > k + top_height - 1:
                    raise AssertionError(
                        (base, shift, degree, residual, k, top_height)
                    )
                error_scaled += 2 * total_l1 * binomial_scaled
        if leading_scaled <= 0:
            raise AssertionError((k, leading_scaled))
        candidate = error_scaled // leading_scaled + 1
        if candidate > threshold:
            threshold = candidate
            threshold_index = k
    return {
        "threshold": threshold,
        "attained_at_k": threshold_index,
        "maximum_binomial_error": maximum_binomial_error,
    }


def sufficient_growing_bound(
    components: dict[int, sp.Expr], p: int
) -> dict[str, object]:
    """Bound all bases a<p by the positive beta^0 term of base p."""

    terms: list[tuple[Fraction, int, Fraction]] = []
    for base, shift, degree, _lc, _lower_l1, total_l1 in coefficient_data(
        components
    ):
        if base == p:
            continue
        if degree - shift > 1:
            raise AssertionError((p, base, shift, degree))
        ratio = Fraction(base, p)
        constant = Fraction(total_l1, base**shift)
        terms.append((ratio, shift, constant))

    bound = Fraction(0)
    for ratio, power, constant in terms:
        monotonic_ratio = ratio * Fraction(K_CUTOFF + 1, K_CUTOFF) ** power
        if monotonic_ratio >= 1:
            raise AssertionError((p, ratio, power, monotonic_ratio))
        bound += constant * K_CUTOFF**power * ratio**K_CUTOFF
    if bound >= Fraction(1, 2):
        raise AssertionError((p, bound))
    return {
        "terms": len(terms),
        "bound_at_k1000": bound,
    }


def page_growing_bound(
    components: dict[int, sp.Expr], p: int
) -> dict[str, object]:
    """Bound bases a<p-1 by a positive beta^3 term of base p-1."""

    q = p - 1
    shift_offset = 2 * p - 4
    terms: list[tuple[Fraction, int, Fraction]] = []
    for base, shift, degree, _lc, _lower_l1, total_l1 in coefficient_data(
        components
    ):
        if base >= q:
            continue
        if shift < 2:
            raise AssertionError((p, base, shift))
        height_deficit = shift - degree - 1
        if height_deficit < 0:
            raise AssertionError((p, base, shift, degree))
        effective_ratio = (
            Fraction(base, q)
            * Fraction(241, 242) ** height_deficit
        )
        constant = (
            Fraction(total_l1 * q**3, (p - 2) * base**shift)
            * Fraction(242, 241) ** (height_deficit * shift_offset)
        )
        if shift == 2:
            constant *= 2
            power = -1
        else:
            power = shift - 3
        terms.append((effective_ratio, power, constant))

    bound = Fraction(0)
    for ratio, power, constant in terms:
        if power >= 0:
            monotonic_ratio = (
                ratio * Fraction(K_CUTOFF + 1, K_CUTOFF) ** power
            )
            value = constant * K_CUTOFF**power * ratio**K_CUTOFF
        else:
            monotonic_ratio = ratio * Fraction(K_CUTOFF, K_CUTOFF + 1)
            value = constant * ratio**K_CUTOFF / (K_CUTOFF - 2)
        if monotonic_ratio >= 1:
            raise AssertionError((p, ratio, power, monotonic_ratio))
        bound += value
    if bound >= Fraction(1, 2):
        raise AssertionError((p, bound))
    return {
        "terms": len(terms),
        "bound_at_k1000": bound,
    }


def certify() -> dict[str, object]:
    actual_source_hash = source_hash()
    if actual_source_hash != EXPECTED_OLD_RECURRENCE_SHA256:
        raise AssertionError(
            (actual_source_hash, EXPECTED_OLD_RECURRENCE_SHA256)
        )
    odd_sufficient = odd_w_components()
    even_sufficient = even_w_components()
    odd_page = page_recurrence_components(6)
    even_page = page_recurrence_components(7)

    for expression in (odd_sufficient[6], even_sufficient[7]):
        beta_zero = sp.Poly(expression, B).coeff_monomial(B**0)
        if sp.expand(beta_zero - 2 * (S - 2)) != 0:
            raise AssertionError(beta_zero)

    fixed = {
        "odd_sufficient": fixed_index_threshold(
            odd_sufficient, -15, 1, 8
        ),
        "even_sufficient": fixed_index_threshold(
            even_sufficient, -17, 1, 10
        ),
        "odd_page": fixed_index_threshold(odd_page, -14, -1, 8),
        "even_page": fixed_index_threshold(even_page, -16, -1, 10),
    }

    dominant_nonnegative = {}
    for name, expression, start in (
        ("odd_sufficient_p", odd_sufficient[6], 8),
        ("even_sufficient_p", even_sufficient[7], 9),
        ("odd_page_q", odd_page[5], 50),
        ("odd_page_p", odd_page[6], 8),
        ("even_page_q", even_page[6], 100),
        ("even_page_p", even_page[7], 9),
    ):
        ok, count = shifted_nonnegative(expression, start)
        if not ok:
            raise AssertionError((name, start))
        dominant_nonnegative[name] = {
            "start": start,
            "positive_shifted_monomials": count,
        }

    odd_q3 = sp.factor(sp.Poly(odd_page[5], B).coeff_monomial(B**3))
    even_q3 = sp.factor(sp.Poly(even_page[6], B).coeff_monomial(B**3))
    if sp.expand(odd_q3 - 8 * (S**2 + 35 * S - 1074)) != 0:
        raise AssertionError(odd_q3)
    if sp.expand(even_q3 - 10 * (S**2 + 49 * S - 2178)) != 0:
        raise AssertionError(even_q3)
    for expression, lower in ((odd_q3, 4 * S**2), (even_q3, 5 * S**2)):
        difference = sp.Poly(sp.expand((expression - lower).subs(S, X + 100)), X)
        if any(value < 0 for value in difference.all_coeffs()):
            raise AssertionError((expression, lower))

    growing = {
        "odd_sufficient": sufficient_growing_bound(odd_sufficient, 6),
        "even_sufficient": sufficient_growing_bound(even_sufficient, 7),
        "odd_page": page_growing_bound(odd_page, 6),
        "even_page": page_growing_bound(even_page, 7),
    }

    effective = max(
        GEOMETRY_THRESHOLD,
        100,
        *(item["maximum_binomial_error"] for item in fixed.values()),
        *(item["threshold"] for item in fixed.values()),
    )
    return {
        "source_sha256": actual_source_hash,
        "k_cutoff": K_CUTOFF,
        "geometry_threshold": GEOMETRY_THRESHOLD,
        "fixed": fixed,
        "dominant_nonnegative": dominant_nonnegative,
        "growing": growing,
        "S_gap_effective": effective,
    }


def fraction_summary(value: Fraction) -> str:
    if value.numerator.bit_length() < 1024:
        return f"{value} (~{float(value):.6g})"
    log10_value = (
        math.log(value.numerator) - math.log(value.denominator)
    ) / math.log(10)
    return (
        f"exact Fraction with {value.numerator.bit_length()} numerator bits, "
        f"{value.denominator.bit_length()} denominator bits "
        f"(~10^{log10_value:.3f})"
    )


def main() -> None:
    result = certify()
    print("OPG COMPLETE LOG-LAYER EFFECTIVE BOUND: PASS")
    print("source_sha256:", result["source_sha256"])
    print("k_cutoff:", result["k_cutoff"])
    print("geometry_threshold:", result["geometry_threshold"])
    for name, data in result["fixed"].items():
        print(name, data)
    for name, data in result["dominant_nonnegative"].items():
        print(name, data)
    for name, data in result["growing"].items():
        print(
            name,
            {
                "terms": data["terms"],
                "bound_at_k1000": fraction_summary(
                    data["bound_at_k1000"]
                ),
            },
        )
    print("S_gap_effective:", result["S_gap_effective"])
    print("S_gap_effective_digits:", len(str(result["S_gap_effective"])))
    print("status_original_opg1757: OPEN")


if __name__ == "__main__":
    main()
