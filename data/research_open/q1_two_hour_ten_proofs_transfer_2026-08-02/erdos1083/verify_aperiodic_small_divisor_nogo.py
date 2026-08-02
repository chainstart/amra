#!/usr/bin/env python3
"""Finite certificates for the aperiodic small-divisor no-go."""

from __future__ import annotations

import cmath
import json
import math

import sympy as sp


x, y = sp.symbols("x y")
P = x**6 + x**5 + x**3 + x + 1
F = y**3 + y**2 - 3 * y - 1


def modular_power_remainder(exponent: int) -> sp.Poly:
    modulus_poly = sp.Poly(P, x, modulus=3)
    result = sp.Poly(1, x, modulus=3)
    base = sp.Poly(x, x, modulus=3)
    while exponent:
        if exponent & 1:
            result = (result * base).rem(modulus_poly)
        base = (base * base).rem(modulus_poly)
        exponent //= 2
    return (result - sp.Poly(x, x, modulus=3)).rem(modulus_poly)


def rabin_certificate() -> dict[str, object]:
    modulus_poly = sp.Poly(P, x, modulus=3)
    remainder_two = modular_power_remainder(3**2)
    remainder_three = modular_power_remainder(3**3)
    remainder_six = modular_power_remainder(3**6)
    gcd_two = sp.gcd(modulus_poly, remainder_two)
    gcd_three = sp.gcd(modulus_poly, remainder_three)
    return {
        "remainder_k2": str(remainder_two.as_expr()),
        "remainder_k3": str(remainder_three.as_expr()),
        "remainder_k6": str(remainder_six.as_expr()),
        "gcd_k2": str(gcd_two.as_expr()),
        "gcd_k3": str(gcd_three.as_expr()),
        "irreducible_mod_3": bool(sp.Poly(P, x, modulus=3).is_irreducible),
        "irreducible_over_Q": bool(sp.Poly(P, x).is_irreducible),
        "pass": (
            remainder_two.as_expr() == x**4 - x**3 - 1
            and remainder_three.as_expr() == -x**5 - x**4 - x**2 - x - 1
            and remainder_six.is_zero
            and gcd_two.degree() == gcd_three.degree() == 0
            and sp.Poly(P, x, modulus=3).is_irreducible
            and sp.Poly(P, x).is_irreducible
        ),
    }


def root_geometry_certificate() -> dict[str, object]:
    reciprocal_substitution = sp.expand(
        (y**3 - 3 * y) + (y**2 - 2) + 1 - F
    )
    roots = [complex(root) for root in sp.nroots(P, n=40, maxsteps=200)]
    unit_roots = [root for root in roots if abs(abs(root) - 1) < 1e-12]
    off_circle_roots = [root for root in roots if abs(abs(root) - 1) > 1e-6]
    signs = {
        "f(-3)": int(F.subs(y, -3)),
        "f(-2)": int(F.subs(y, -2)),
        "8f(-1/2)": int(8 * F.subs(y, sp.Rational(-1, 2))),
        "f(0)": int(F.subs(y, 0)),
        "f(1)": int(F.subs(y, 1)),
        "f(2)": int(F.subs(y, 2)),
    }
    return {
        "reciprocal_substitution_exact": reciprocal_substitution == 0,
        "signs": signs,
        "unit_root_count_numeric": len(unit_roots),
        "off_circle_root_count_numeric": len(off_circle_roots),
        "maximum_unit_modulus_error": max(abs(abs(root) - 1) for root in unit_roots),
        "pass": (
            reciprocal_substitution == 0
            and signs["f(-3)"] < 0 < signs["f(-2)"]
            and signs["8f(-1/2)"] > 0 > signs["f(0)"]
            and signs["f(1)"] < 0 < signs["f(2)"]
            and len(unit_roots) == 4
            and len(off_circle_roots) == 2
        ),
    }


def small_divisor_certificate() -> dict[str, object]:
    roots = [complex(root) for root in sp.nroots(P, n=50, maxsteps=200)]
    unit_root = next(root for root in roots if root.imag > 0 and abs(abs(root) - 1) < 1e-14)
    theta = cmath.phase(unit_root)
    prime_sample = list(sp.primerange(7, 300))
    records = []
    for prime in prime_sample:
        nearest = round(prime * theta / (2 * math.pi)) % prime
        root_of_unity = cmath.exp(2j * math.pi * nearest / prime)
        value = sum(root_of_unity**exponent for exponent in (0, 1, 3, 5, 6))
        all_values = [
            abs(sum(cmath.exp(2j * math.pi * frequency * exponent / prime)
                    for exponent in (0, 1, 3, 5, 6)))
            for frequency in range(prime)
        ]
        sigma = min(all_values)
        records.append(
            {
                "prime": prime,
                "nearest_frequency": nearest,
                "nearest_value": abs(value),
                "sigma": sigma,
                "upper_bound": 15 * math.pi / prime,
                "bound_holds": 0 < sigma <= abs(value) + 1e-12 <= 15 * math.pi / prime + 1e-12,
            }
        )

    torsion_orders = 256
    torsion_gcd_degrees = [
        sp.degree(sp.gcd(P, x**order - 1), x)
        for order in range(1, torsion_orders + 1)
    ]
    return {
        "unit_root": [unit_root.real, unit_root.imag],
        "prime_records": records,
        "torsion_orders_checked": torsion_orders,
        "no_torsion_factor_checked": all(degree == 0 for degree in torsion_gcd_degrees),
        "all_prime_sample_bounds": all(record["bound_holds"] for record in records),
        "all_n_proof_in_manuscript": True,
        "pass": (
            all(degree == 0 for degree in torsion_gcd_degrees)
            and all(record["bound_holds"] for record in records)
        ),
    }


def signed_escape_certificate() -> dict[str, object]:
    quotient = 1 - x**5 + x**8 + x**10 - x**13 + x**18
    expected = (
        1 + x + x**3 + x**9 + x**11 + x**13
        + x**15 + x**21 + x**23 + x**24
    )
    product = sp.expand(P * quotient)
    quotient_coefficients = [
        int(coefficient) for coefficient in sp.Poly(quotient, x).all_coeffs()
    ]
    product_coefficients = [
        int(coefficient) for coefficient in sp.Poly(product, x).coeffs()
    ]
    augmentation = int(quotient.subs(x, 1))
    norm_squared = sum(coefficient * coefficient for coefficient in quotient_coefficients)
    delta = (norm_squared - augmentation) // 2
    heavy_factor = 1 + x**8
    unit_factor_one = 1 - x + x**2
    unit_factor_two = x**8 + x**7 - x**5 - x**4 - x**3 + x + 1
    exact_factorization = sp.expand(
        heavy_factor * unit_factor_one * unit_factor_two
    ) == quotient
    ratio_records = []
    for prime in (29, 31, 37, 43, 47):
        ratios = []
        for frequency in range(prime):
            root = cmath.exp(2j * math.pi * frequency / prime)
            centre_value = sum(root**exponent for exponent in (0, 1, 3, 5, 6))
            quotient_value = sum(
                coefficient * root**exponent
                for exponent, coefficient in ((0, 1), (5, -1), (8, 1),
                                                (10, 1), (13, -1), (18, 1))
            )
            product_value = centre_value * quotient_value
            ratios.append(abs(product_value) ** 2 / abs(centre_value) ** 2)
        ratio_records.append(
            {
                "prime": prime,
                "ratio_average": sum(ratios) / prime,
                "ratio_maximum": max(ratios),
                "parseval_six": abs(sum(ratios) / prime - 6) < 1e-9,
                "pointwise_bound_36": max(ratios) <= 36 + 1e-9,
            }
        )
    return {
        "quotient": str(quotient),
        "quotient_augmentation": augmentation,
        "strict_augmentation": augmentation < int(P.subs(x, 1)),
        "negative_coefficients": sum(
            coefficient < 0 for coefficient in quotient_coefficients
        ),
        "product": str(product),
        "exact_product": product == expected,
        "product_is_mask": all(coefficient == 1 for coefficient in product_coefficients),
        "product_terms": len(sp.Poly(product, x).terms()),
        "factorial_energy": delta,
        "exact_factorization": exact_factorization,
        "factor_augmentations": [
            int(heavy_factor.subs(x, 1)),
            int(unit_factor_one.subs(x, 1)),
            int(unit_factor_two.subs(x, 1)),
        ],
        "co_vanishing_ratio_records": ratio_records,
        "pass": (
            augmentation == 2
            and augmentation < 5
            and sum(coefficient < 0 for coefficient in quotient_coefficients) == 2
            and product == expected
            and all(coefficient == 1 for coefficient in product_coefficients)
            and len(sp.Poly(product, x).terms()) == 10
            and delta == 2
            and exact_factorization
            and [
                int(heavy_factor.subs(x, 1)),
                int(unit_factor_one.subs(x, 1)),
                int(unit_factor_two.subs(x, 1)),
            ] == [2, 1, 1]
            and all(record["parseval_six"] for record in ratio_records)
            and all(record["pointwise_bound_36"] for record in ratio_records)
        ),
    }


def run_all() -> dict[str, object]:
    result = {
        "rabin": rabin_certificate(),
        "root_geometry": root_geometry_certificate(),
        "small_divisor": small_divisor_certificate(),
        "signed_escape": signed_escape_certificate(),
        "signed_positive_quotient_constructed": True,
        "power_large_family_constructed": False,
        "original_problem_proved": False,
    }
    result["pass"] = all(
        result[key]["pass"]
        for key in ("rabin", "root_geometry", "small_divisor", "signed_escape")
    )
    return result


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
