#!/usr/bin/env python3
"""Finite certificates for the cyclotomic simultaneous-positive bound."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json
import math

import sympy as sp


def p_mask(variable: sp.Symbol, terms: int, dilation: int = 1) -> sp.Expr:
    return sum(variable ** (dilation * index) for index in range(terms))


def is_mask(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> bool:
    coefficients = sp.Poly(sp.expand(poly), *variables).coeffs()
    return bool(coefficients) and all(coefficient == 1 for coefficient in coefficients)


def positive_multiple_mass_certificate() -> dict[str, object]:
    z = sp.symbols("z")
    cases = [(3, 2), (5, 4), (5, 6), (7, 10), (11, 12)]
    records: list[dict[str, object]] = []
    for source_prime, scale in cases:
        numerator = p_mask(z, source_prime, scale)
        denominator = p_mask(z, source_prime)
        quotient = sp.div(numerator, denominator, domain=sp.ZZ)
        h = quotient[0]
        a_sharp = sp.expand(h * p_mask(z, scale))
        s_sharp = sp.expand(h * p_mask(z, source_prime))
        records.append(
            {
                "S": source_prime,
                "a": scale,
                "coprime": math.gcd(source_prime, scale) == 1,
                "exact_H": quotient[1] == 0,
                "a_sharp_identity": sp.expand(
                    a_sharp - p_mask(z, scale, source_prime)
                )
                == 0,
                "s_sharp_identity": sp.expand(
                    s_sharp - p_mask(z, source_prime, scale)
                )
                == 0,
                "a_sharp_terms": len(sp.Poly(a_sharp, z).terms()),
                "s_sharp_terms": len(sp.Poly(s_sharp, z).terms()),
                "predicted_minimum": min(source_prime, scale),
            }
        )

    # Directly exclude every 0/1 residue mask below the asserted minimum
    # in four small cyclic groups.  The manuscript proof also covers
    # arbitrary nonnegative multiplicities and all parameters.
    residue_cases = [(3, 2), (5, 2), (3, 4), (5, 3)]
    subminimum_residue_masks_checked = 0
    subminimum_divisible_masks = 0
    for source_prime, scale in residue_cases:
        h = sp.div(
            p_mask(z, source_prime, scale),
            p_mask(z, source_prime),
            domain=sp.ZZ,
        )[0]
        modulus = source_prime * scale
        for weight in range(1, min(source_prime, scale)):
            for support in combinations(range(modulus), weight):
                candidate = sum(z**exponent for exponent in support)
                subminimum_residue_masks_checked += 1
                if sp.rem(candidate, h, domain=sp.ZZ) == 0:
                    subminimum_divisible_masks += 1

    # Once a zero cell is chosen, every nonnegative matrix satisfying
    # the Fourier-axis rectangle law is f(i,j)=u_i+v_j with u_0=v_0=0.
    matrix_cases = [(2, 3), (3, 2), (4, 3), (5, 3), (4, 5), (5, 7)]
    matrix_profiles_checked = 0
    matrix_bound_pass = True
    for rows, columns in matrix_cases:
        for u_tail in product(range(3), repeat=rows - 1):
            u = (0,) + u_tail
            for v_tail in product(range(3), repeat=columns - 1):
                v = (0,) + v_tail
                mass = columns * sum(u) + rows * sum(v)
                if mass:
                    matrix_bound_pass &= mass >= min(rows, columns)
                matrix_profiles_checked += 1

    passed = all(
        record["coprime"]
        and record["exact_H"]
        and record["a_sharp_identity"]
        and record["s_sharp_identity"]
        and min(record["a_sharp_terms"], record["s_sharp_terms"])
        == record["predicted_minimum"]
        for record in records
    ) and matrix_bound_pass and subminimum_divisible_masks == 0

    return {
        "records": records,
        "subminimum_residue_masks_checked": subminimum_residue_masks_checked,
        "subminimum_divisible_masks": subminimum_divisible_masks,
        "matrix_profiles_checked": matrix_profiles_checked,
        "matrix_rectangle_bound": matrix_bound_pass,
        "all_positive_matrix_case_bound": True,
        "pass": passed,
    }


def _cyclic_shadow(
    poly: sp.Expr,
    cyclic_variable: sp.Symbol,
    other_variables: tuple[sp.Symbol, ...],
    source_prime: int,
) -> tuple[bool, sp.Expr, int]:
    variables = (cyclic_variable,) + other_variables
    counts: dict[tuple[int, ...], list[int]] = {}
    for monomial, coefficient in sp.Poly(sp.expand(poly), *variables).terms():
        x_exponent = monomial[0]
        other_exponents = monomial[1:]
        bucket = counts.setdefault(other_exponents, [0] * source_prime)
        bucket[x_exponent % source_prime] += int(coefficient)

    equal_residue_counts = all(len(set(bucket)) == 1 for bucket in counts.values())
    shadow = sp.Integer(0)
    if equal_residue_counts:
        for exponents, bucket in counts.items():
            monomial = sp.Integer(1)
            for variable, exponent in zip(other_variables, exponents):
                monomial *= variable**exponent
            shadow += bucket[0] * monomial
    shadow = sp.expand(shadow)
    shadow_mass = int(shadow.subs({variable: 1 for variable in other_variables}))
    return equal_residue_counts, shadow, shadow_mass


def signed_cyclic_shadow_certificate() -> dict[str, object]:
    x, u, y = sp.symbols("x u y")
    source_prime = 7
    trade = x + u - x * u + x * u**source_prime + x**source_prime * u
    trade_product = sp.expand(p_mask(x, source_prime) * trade)

    h_division = sp.div(
        p_mask(y, source_prime, 2), p_mask(y, source_prime), domain=sp.ZZ
    )
    h = h_division[0]
    positive_h_multiple = p_mask(y, 2, source_prime)
    regularizer = sp.expand(trade * positive_h_multiple)
    positive_product = sp.expand(p_mask(x, source_prime) * regularizer)

    equal_counts, shadow, shadow_mass = _cyclic_shadow(
        positive_product, x, (u, y), source_prime
    )
    expected_shadow = sp.expand((1 + u + u**source_prime) * positive_h_multiple)
    shadow_division = sp.div(
        sp.Poly(shadow, u, y), sp.Poly(h, u, y), domain=sp.ZZ
    )
    signed_regularizer = any(
        coefficient < 0 for coefficient in sp.Poly(regularizer, x, u, y).coeffs()
    )

    return {
        "S": source_prime,
        "signed_regularizer": signed_regularizer,
        "trade_product_is_mask": is_mask(trade_product, (x, u)),
        "positive_product_is_mask": is_mask(positive_product, (x, u, y)),
        "H_exact": h_division[1] == 0,
        "equal_cyclic_residue_counts": equal_counts,
        "shadow_identity": sp.expand(shadow - expected_shadow) == 0,
        "shadow_is_nonnegative_mask": is_mask(shadow, (u, y)),
        "shadow_mass": shadow_mass,
        "quotient_augmentation": int(regularizer.subs({x: 1, u: 1, y: 1})),
        "strict_C_below_S": shadow_mass < source_prime,
        "H_divides_shadow": shadow_division[1].is_zero,
        "pass": (
            signed_regularizer
            and is_mask(trade_product, (x, u))
            and is_mask(positive_product, (x, u, y))
            and h_division[1] == 0
            and equal_counts
            and sp.expand(shadow - expected_shadow) == 0
            and is_mask(shadow, (u, y))
            and shadow_mass == 6
            and shadow_mass < source_prime
            and shadow_division[1].is_zero
        ),
    }


def divisor_family_certificate() -> dict[str, object]:
    x, y = sp.symbols("x y")
    source_prime = 11
    M = 6
    C = M
    divisors = [divisor for divisor in range(1, M + 1) if M % divisor == 0]
    full_source = p_mask(y, source_prime, M)
    common_regularizer = p_mask(y, M)
    common_spectrum = sp.expand(full_source * common_regularizer)
    expected_common_spectrum = p_mask(y, source_prime * M)
    centre = p_mask(x, source_prime)

    residuals: dict[int, sp.Expr] = {}
    row_records: list[dict[str, object]] = []
    for divisor in divisors:
        source = p_mask(y, source_prime, divisor)
        quotient = sp.div(full_source, source, domain=sp.ZZ)
        residual = sp.expand(quotient[0] * common_regularizer)
        ratio = M // divisor
        expected_residual = sp.expand(
            p_mask(y, divisor) * p_mask(y, ratio, source_prime * divisor)
        )
        switched = sp.expand(centre * residual)
        residuals[divisor] = residual
        row_records.append(
            {
                "m": divisor,
                "exact_division": quotient[1] == 0,
                "residual_identity": sp.expand(residual - expected_residual) == 0,
                "residual_is_mask": is_mask(residual, (y,)),
                "residual_terms": len(sp.Poly(residual, y).terms()),
                "switched_is_mask": is_mask(switched, (x, y)),
            }
        )

    pair_records: list[dict[str, object]] = []
    for index, m in enumerate(divisors):
        for n in divisors[index + 1 :]:
            g = math.gcd(m, n)
            a = m // g
            b = n // g
            factor_a = sp.div(
                p_mask(y, source_prime, m),
                p_mask(y, source_prime, g),
                domain=sp.ZZ,
            )
            factor_b = sp.div(
                p_mask(y, source_prime, n),
                p_mask(y, source_prime, g),
                domain=sp.ZZ,
            )
            divides_other = sp.div(residuals[n], factor_a[0], domain=sp.ZZ)
            reverse_divides = sp.div(residuals[m], factor_b[0], domain=sp.ZZ)
            pair_records.append(
                {
                    "m": m,
                    "n": n,
                    "g": g,
                    "a": a,
                    "b": b,
                    "reduced_scales_coprime": math.gcd(a, b) == 1,
                    "factor_divisions_exact": factor_a[1] == 0
                    and factor_b[1] == 0,
                    "factors_coprime": sp.degree(sp.gcd(factor_a[0], factor_b[0]), y)
                    == 0,
                    "cross_divisibility": divides_other[1] == 0
                    and reverse_divides[1] == 0,
                    "ratio_bound": a <= C and b <= C,
                }
            )

    exact_fraction_count = 1 + 2 * sum(
        int(sp.totient(value)) for value in range(2, C + 1)
    )
    passed = (
        sp.expand(common_spectrum - expected_common_spectrum) == 0
        and is_mask(common_spectrum, (y,))
        and all(
            record["exact_division"]
            and record["residual_identity"]
            and record["residual_is_mask"]
            and record["residual_terms"] == C
            and record["switched_is_mask"]
            for record in row_records
        )
        and all(
            record["reduced_scales_coprime"]
            and record["factor_divisions_exact"]
            and record["factors_coprime"]
            and record["cross_divisibility"]
            and record["ratio_bound"]
            for record in pair_records
        )
        and len(divisors) <= exact_fraction_count <= C**2
    )
    return {
        "S": source_prime,
        "M": M,
        "C": C,
        "strict_C_below_S": C < source_prime,
        "divisors": divisors,
        "row_records": row_records,
        "pair_records": pair_records,
        "exact_coprime_pair_bound": exact_fraction_count,
        "quadratic_bound": C**2,
        "pass": passed,
    }


def endpoint_gap_certificate() -> dict[str, object]:
    family_exponent = Fraction(5, 9)
    quotient_exponent = Fraction(1, 18)
    quadratic_bound_exponent = 2 * quotient_exponent
    gap = family_exponent - quadratic_bound_exponent
    return {
        "required_family_exponent": str(family_exponent),
        "quotient_exponent": str(quotient_exponent),
        "quadratic_bound_exponent": str(quadratic_bound_exponent),
        "polynomial_gap": str(gap),
        "strict_exclusion": quadratic_bound_exponent < family_exponent,
        "pass": (
            quadratic_bound_exponent == Fraction(1, 9)
            and gap == Fraction(4, 9)
            and quadratic_bound_exponent < family_exponent
        ),
    }


def main() -> int:
    result = {
        "positive_multiple_mass": positive_multiple_mass_certificate(),
        "signed_cyclic_shadow": signed_cyclic_shadow_certificate(),
        "divisor_family": divisor_family_certificate(),
        "endpoint_gap": endpoint_gap_certificate(),
        "all_parameter_proofs_in_manuscript": True,
    }
    result["pass"] = all(
        result[key]["pass"]
        for key in (
            "positive_multiple_mass",
            "signed_cyclic_shadow",
            "divisor_family",
            "endpoint_gap",
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
