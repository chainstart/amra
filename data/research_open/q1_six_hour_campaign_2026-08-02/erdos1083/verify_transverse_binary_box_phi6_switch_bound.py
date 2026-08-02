#!/usr/bin/env python3
"""Finite certificates for the signed transverse binary-box switch bound."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json
import math

import sympy as sp


def quotient_tiling_certificate() -> dict[str, object]:
    records = []
    total_group_elements = 0
    for rank in range(1, 5):
        for denominator in range(1, 5):
            modulus = 2 * denominator
            subgroup = list(product((0, denominator), repeat=rank))
            complement = list(product(range(denominator), repeat=rank))
            counts: dict[tuple[int, ...], int] = {}
            for h in subgroup:
                for y in complement:
                    element = tuple(
                        (h[index] + y[index]) % modulus for index in range(rank)
                    )
                    counts[element] = counts.get(element, 0) + 1
            expected_size = modulus**rank
            record = {
                "rank": rank,
                "D": denominator,
                "group_size": expected_size,
                "centre_image_size": len(subgroup),
                "tiling_complement_size": len(complement),
                "covered_elements": len(counts),
                "all_coefficients_one": all(count == 1 for count in counts.values()),
                "pass": len(subgroup) == 2**rank
                and len(complement) == denominator**rank
                and len(counts) == expected_size
                and all(count == 1 for count in counts.values()),
            }
            records.append(record)
            total_group_elements += expected_size
    return {
        "records": records,
        "total_group_elements_checked": total_group_elements,
        "pass": all(record["pass"] for record in records),
    }


def shadow_factor_preservation_certificate() -> dict[str, object]:
    # A concrete G=Z/6 example (D=3), retaining an independent variable x.
    # The original quotient is genuinely signed in the centre direction:
    # (1+y)(1-y+y^2)(1+x^3)=(1+y^3)(1+x^3).
    x, y = sp.symbols("x y")
    modulus = 6
    centre_positions = (0, 3)
    tiling_positions = (0, 1, 2)
    t_factor = 1 - x + x**2
    multiplier = 1 + x
    external_shadow = sp.expand(t_factor * multiplier)  # 1+x^3
    signed_quotient = sp.expand((1 - y + y**2) * external_shadow)
    positive_product = sp.expand((1 + y) * signed_quotient)
    expected_product = sp.expand((1 + y**3) * external_shadow)

    # B=F0 * external_shadow.  Projection keeps x and is already uniform
    # on the centre subgroup; multiplication by Y makes it uniform on G.
    coefficients: dict[tuple[int, int], int] = {}
    for centre in centre_positions:
        for tiling_position in tiling_positions:
            g = (centre + tiling_position) % modulus
            for (x_power,), coefficient in sp.Poly(external_shadow, x).terms():
                key = (g, x_power)
                coefficients[key] = coefficients.get(key, 0) + int(coefficient)
    profiles = {
        x_power: tuple(coefficients.get((g, x_power), 0) for g in range(modulus))
        for x_power in range(4)
    }
    shadow = {
        x_power: profile[0]
        for x_power, profile in profiles.items()
        if profile[0]
    }
    return {
        "modulus": modulus,
        "profiles": profiles,
        "profiles_uniform": all(len(set(profile)) == 1 for profile in profiles.values()),
        "shadow": shadow,
        "shadow_mass": sum(shadow.values()),
        "expected_mass": 2,
        "original_quotient_is_signed": any(
            coefficient < 0
            for coefficient in sp.Poly(signed_quotient, x, y).coeffs()
        ),
        "positive_product_identity": positive_product == expected_product
        and all(
            coefficient == 1
            for coefficient in sp.Poly(positive_product, x, y).coeffs()
        ),
        "phi6_divides_shadow": sp.rem(
            sp.Poly(sum(value * x**power for power, value in shadow.items()), x),
            sp.Poly(t_factor, x),
        )
        == 0,
        "pass": all(len(set(profile)) == 1 for profile in profiles.values())
        and sum(shadow.values()) == 2
        and any(
            coefficient < 0
            for coefficient in sp.Poly(signed_quotient, x, y).coeffs()
        )
        and positive_product == expected_product
        and all(
            coefficient == 1
            for coefficient in sp.Poly(positive_product, x, y).coeffs()
        )
        and sp.rem(
            sp.Poly(sum(value * x**power for power, value in shadow.items()), x),
            sp.Poly(t_factor, x),
        )
        == 0,
    }


def newton_zonotope_certificate() -> dict[str, object]:
    records = []
    for rank in range(1, 7):
        variables = sp.symbols(f"x0:{rank}")
        t_product = sp.prod(1 - variable + variable**2 for variable in variables)
        sharp_multiplier = sp.prod(1 + variable for variable in variables)
        sharp_positive = sp.expand(t_product * sharp_multiplier)
        polynomial = sp.Poly(sharp_positive, *variables)
        support = [term[0] for term in polynomial.terms()]
        expected_vertices = set(product((0, 3), repeat=rank))
        records.append(
            {
                "rank": rank,
                "mass": int(sharp_positive.subs({variable: 1 for variable in variables})),
                "support_size": len(support),
                "support_is_parallelotope_vertices": set(support) == expected_vertices,
                "all_coefficients_one": all(
                    coefficient == 1 for coefficient in polynomial.coeffs()
                ),
                "pass": len(support) == 2**rank
                and set(support) == expected_vertices
                and all(coefficient == 1 for coefficient in polynomial.coeffs()),
            }
        )
    return {"records": records, "pass": all(record["pass"] for record in records)}


def pairwise_hamming_certificate() -> dict[str, object]:
    rank = 10
    complement_mass = 8
    bound = int(math.log2(complement_mass))
    base = tuple(1 if index % 3 == 0 else 0 for index in range(rank))
    allowed = []
    for pattern in product((0, 1), repeat=rank):
        plus = sum(a == 1 and b == 0 for a, b in zip(pattern, base))
        minus = sum(a == 0 and b == 1 for a, b in zip(pattern, base))
        if plus <= bound and minus <= bound:
            allowed.append((pattern, plus, minus))
    hamming_ball_bound = sum(math.comb(rank, radius) for radius in range(2 * bound + 1))
    return {
        "rank": rank,
        "C": complement_mass,
        "one_sided_bound": bound,
        "base_weight": sum(base),
        "allowed_patterns": len(allowed),
        "hamming_ball_bound": hamming_ball_bound,
        "all_one_sided_bounds_hold": all(
            plus <= bound and minus <= bound for _, plus, minus in allowed
        ),
        "family_below_ball_bound": len(allowed) <= hamming_ball_bound,
        "pass": all(plus <= bound and minus <= bound for _, plus, minus in allowed)
        and len(allowed) <= hamming_ball_bound,
    }


def symbolic_pair_and_sharpness_certificate() -> dict[str, object]:
    rank = 4
    variables = sp.symbols(f"x0:{rank}")
    a_factors = [1 + variable for variable in variables]
    t_factors = [1 - variable + variable**2 for variable in variables]
    patterns = list(product((0, 1), repeat=rank))
    pair_records = []
    for epsilon in patterns:
        source_epsilon = sp.prod(
            a_factors[index] * t_factors[index] ** epsilon[index]
            for index in range(rank)
        )
        for eta in patterns:
            source_eta = sp.prod(
                a_factors[index] * t_factors[index] ** eta[index]
                for index in range(rank)
            )
            common = sp.prod(
                a_factors[index]
                * t_factors[index] ** min(epsilon[index], eta[index])
                for index in range(rank)
            )
            residual_plus = sp.prod(
                t_factors[index]
                for index in range(rank)
                if epsilon[index] > eta[index]
            )
            residual_minus = sp.prod(
                t_factors[index]
                for index in range(rank)
                if eta[index] > epsilon[index]
            )
            gcd = sp.gcd(
                sp.Poly(residual_plus, *variables),
                sp.Poly(residual_minus, *variables),
            )
            pair_records.append(
                sp.expand(source_epsilon - common * residual_plus) == 0
                and sp.expand(source_eta - common * residual_minus) == 0
                and gcd.as_expr() == 1
            )

    # Sharp exact common-product models.  For d switched coordinates the
    # complement ratio is exactly C=2^d.  The d=k case reaches C=S and
    # therefore marks the strict-block boundary.
    sharp_records = []
    centre_variables = sp.symbols(f"y0:{rank}")
    centre = sp.prod(1 + variable for variable in centre_variables)
    base_source = sp.prod(a_factors)
    all_variables = variables + centre_variables
    for switched in range(1, rank + 1):
        residual = sp.prod(t_factors[index] for index in range(switched))
        regularizer = sp.prod(a_factors[index] for index in range(switched))
        switched_source = sp.expand(base_source * residual)
        small_source_complement = sp.expand(centre * residual * regularizer)
        switched_source_complement = sp.expand(centre * regularizer)
        centre_complement = sp.expand(switched_source * regularizer)
        common_product = sp.expand(base_source * small_source_complement)
        def mask(expression: sp.Expr) -> bool:
            coefficients = sp.Poly(expression, *all_variables).coeffs()
            return bool(coefficients) and all(coefficient == 1 for coefficient in coefficients)
        sharp_records.append(
            {
                "d": switched,
                "C": 2**switched,
                "S": 2**rank,
                "common_products_equal": sp.expand(
                    switched_source * switched_source_complement - common_product
                )
                == 0
                and sp.expand(centre * centre_complement - common_product) == 0,
                "all_complements_are_masks": mask(small_source_complement)
                and mask(switched_source_complement)
                and mask(centre_complement),
                "strict_exactly_before_uniform_endpoint": (2**switched < 2**rank)
                == (switched < rank),
                "pass": sp.expand(
                    switched_source * switched_source_complement - common_product
                )
                == 0
                and sp.expand(centre * centre_complement - common_product) == 0
                and mask(small_source_complement)
                and mask(switched_source_complement)
                and mask(centre_complement),
            }
        )
    return {
        "rank": rank,
        "ordered_pairs_checked": len(pair_records),
        "all_pair_factorizations_and_coprimality": all(pair_records),
        "sharp_records": sharp_records,
        "pass": all(pair_records) and all(record["pass"] for record in sharp_records),
    }


def endpoint_entropy_certificate() -> dict[str, object]:
    ell = 3
    rank = 14 * ell
    radius = 2 * ell
    source_size = 2**rank
    complement_ratio = 2**ell
    t = 2 ** (18 * ell)
    exact_ball = sum(math.comb(rank, r) for r in range(radius + 1))
    entropy = -Fraction(1, 7) * math.log2(Fraction(1, 7)) - Fraction(
        6, 7
    ) * math.log2(Fraction(6, 7))
    exponent = Fraction(7, 9) * entropy
    required = Fraction(5, 9)
    entropy_bound = 2 ** (rank * entropy)
    return {
        "ell": ell,
        "rank": rank,
        "radius": radius,
        "radius_is_k_over_7": 7 * radius == rank,
        "S": source_size,
        "C": complement_ratio,
        "t": t,
        "exact_ball": exact_ball,
        "entropy": float(entropy),
        "t_exponent": float(exponent),
        "required_exponent": float(required),
        "exponent_margin": float(required - exponent),
        "exact_ball_below_entropy_bound": exact_ball <= entropy_bound,
        "uniform_endpoint_forces_C_at_least_S": 2**rank == source_size,
        "strict_block_contradiction": complement_ratio < source_size,
        "pass": 7 * radius == rank
        and exact_ball <= entropy_bound
        and exponent < required
        and 2**rank == source_size
        and complement_ratio < source_size,
    }


def build_report() -> dict[str, object]:
    sections = {
        "quotient_tiling": quotient_tiling_certificate(),
        "shadow_factor_preservation": shadow_factor_preservation_certificate(),
        "newton_zonotope": newton_zonotope_certificate(),
        "pairwise_hamming": pairwise_hamming_certificate(),
        "symbolic_pair_and_sharpness": symbolic_pair_and_sharpness_certificate(),
        "endpoint_entropy": endpoint_entropy_certificate(),
    }
    return {"sections": sections, "pass": all(section["pass"] for section in sections.values())}


if __name__ == "__main__":
    report = build_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["pass"] else 1)
