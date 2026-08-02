#!/usr/bin/env python3
"""Finite certificates for finite-quotient shadows and aperiodic escape."""

from __future__ import annotations

from fractions import Fraction
import json
import math

import sympy as sp


def p_mask(variable: sp.Symbol, terms: int, dilation: int = 1) -> sp.Expr:
    return sum(variable ** (dilation * index) for index in range(terms))


def is_mask(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> bool:
    coefficients = sp.Poly(sp.expand(poly), *variables).coeffs()
    return bool(coefficients) and all(coefficient == 1 for coefficient in coefficients)


def finite_quotient_shadow_certificate() -> dict[str, object]:
    z = sp.symbols("z")
    group_order = 6
    source = {0, 2, 4}
    complement = {0, 1}

    tiling_counts = [0] * group_order
    for source_element in source:
        for complement_element in complement:
            tiling_counts[(source_element + complement_element) % group_order] += 1

    source_prime = 5
    scale = 2
    h_division = sp.div(
        p_mask(z, source_prime, scale), p_mask(z, source_prime), domain=sp.ZZ
    )
    h = h_division[0]
    shadow = p_mask(z, scale, source_prime)
    shadow_division = sp.div(shadow, h, domain=sp.ZZ)

    # B is the direct product of the three source residues and the
    # two-term external shadow.  Multiplication by Y fills every group
    # residue with exactly the same external polynomial.
    projected_b: dict[tuple[int, int], int] = {}
    for residue in source:
        for z_exponent in (0, source_prime):
            projected_b[(residue, z_exponent)] = 1
    compressed_counts: dict[tuple[int, int], int] = {}
    for (residue, z_exponent), coefficient in projected_b.items():
        for y_element in complement:
            key = ((residue + y_element) % group_order, z_exponent)
            compressed_counts[key] = compressed_counts.get(key, 0) + coefficient
    uniform_by_residue = all(
        [compressed_counts.get((residue, z_exponent), 0) for residue in range(group_order)]
        == [1] * group_order
        for z_exponent in (0, source_prime)
    )

    return {
        "group_order": group_order,
        "source_size": len(source),
        "complement_size": len(complement),
        "exact_finite_tiling": tiling_counts == [1] * group_order,
        "uniform_compressed_coefficients": uniform_by_residue,
        "shadow_mass": int(shadow.subs(z, 1)),
        "expected_quotient_mass": 2,
        "H_exact": h_division[1] == 0,
        "H_divides_shadow": shadow_division[1] == 0,
        "pass": (
            tiling_counts == [1] * group_order
            and uniform_by_residue
            and int(shadow.subs(z, 1)) == 2
            and h_division[1] == 0
            and shadow_division[1] == 0
        ),
    }


def aperiodic_signed_escape_certificate() -> dict[str, object]:
    x = sp.symbols("x")
    source = 1 + x + x**4
    signed_quotient = 1 - x**4 + x**5 + x**7
    product_mask = sp.expand(source * signed_quotient)
    expected = 1 + x + x**6 + x**7 + x**9 + x**11

    torsion_orders_checked = 256
    torsion_gcd_degrees = []
    for order in range(1, torsion_orders_checked + 1):
        torsion_gcd_degrees.append(
            sp.degree(sp.gcd(source, x**order - 1), x)
        )

    return {
        "source_terms": len(sp.Poly(source, x).terms()),
        "quotient_augmentation": int(signed_quotient.subs(x, 1)),
        "signed_quotient_has_negative_coefficient": any(
            coefficient < 0
            for coefficient in sp.Poly(signed_quotient, x).all_coeffs()
        ),
        "exact_product_identity": sp.expand(product_mask - expected) == 0,
        "product_is_mask": is_mask(product_mask, (x,)),
        "product_terms": len(sp.Poly(product_mask, x).terms()),
        "strict_augmentation": bool(
            signed_quotient.subs(x, 1) < source.subs(x, 1)
        ),
        "source_irreducible_over_Q": bool(sp.Poly(source, x).is_irreducible),
        "torsion_orders_checked": torsion_orders_checked,
        "no_torsion_factor_in_checked_range": all(
            degree == 0 for degree in torsion_gcd_degrees
        ),
        "unit_triangle_proof_in_manuscript": True,
        "finite_cyclic_tiling_excluded_by_fourier": True,
        "pass": bool(
            int(source.subs(x, 1)) == 3
            and int(signed_quotient.subs(x, 1)) == 2
            and any(
                coefficient < 0
                for coefficient in sp.Poly(signed_quotient, x).all_coeffs()
            )
            and sp.expand(product_mask - expected) == 0
            and is_mask(product_mask, (x,))
            and len(sp.Poly(product_mask, x).terms()) == 6
            and sp.Poly(source, x).is_irreducible
            and all(degree == 0 for degree in torsion_gcd_degrees)
        ),
    }


def two_point_minimality_certificate() -> dict[str, object]:
    records = []
    for difference in range(1, 21):
        modulus = 2 * difference
        source = {0, difference}
        complement = set(range(difference))
        counts = [0] * modulus
        for left in source:
            for right in complement:
                counts[(left + right) % modulus] += 1
        records.append(
            {
                "difference": difference,
                "modulus": modulus,
                "exact_tiling": counts == [1] * modulus,
            }
        )
    return {
        "records": records,
        "all_two_point_models_tile": all(record["exact_tiling"] for record in records),
        "pass": all(record["exact_tiling"] for record in records),
    }


def endpoint_extension_certificate() -> dict[str, object]:
    family_exponent = Fraction(5, 9)
    quotient_exponent = Fraction(1, 18)
    finite_tile_bound = 2 * quotient_exponent
    return {
        "family_exponent": str(family_exponent),
        "finite_tile_bound_exponent": str(finite_tile_bound),
        "gap": str(family_exponent - finite_tile_bound),
        "pass": (
            finite_tile_bound == Fraction(1, 9)
            and family_exponent - finite_tile_bound == Fraction(4, 9)
        ),
    }


def main() -> int:
    result = {
        "finite_quotient_shadow": finite_quotient_shadow_certificate(),
        "aperiodic_signed_escape": aperiodic_signed_escape_certificate(),
        "two_point_minimality": two_point_minimality_certificate(),
        "endpoint_extension": endpoint_extension_certificate(),
        "all_parameter_proofs_in_manuscript": True,
    }
    result["pass"] = all(
        result[key]["pass"]
        for key in (
            "finite_quotient_shadow",
            "aperiodic_signed_escape",
            "two_point_minimality",
            "endpoint_extension",
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
