#!/usr/bin/env python3
"""Certificates for the simultaneous-positive-complement no-go model."""

from __future__ import annotations

import json

import sympy as sp


def masks(source_size: int) -> tuple[sp.Symbol, sp.Symbol, sp.Poly, sp.Poly, sp.Poly, sp.Poly]:
    x, y = sp.symbols("x y")
    px = sum(x**index for index in range(source_size))
    py = sum(y**index for index in range(source_size))
    quotient = x + y - x * y + x * y**source_size + x**source_size * y
    a0 = sp.Poly(sp.expand(py * quotient), x, y)
    a1 = sp.Poly(sp.expand(px * quotient), x, y)
    spectrum = sp.Poly(sp.expand(px * py * quotient), x, y)
    return x, y, sp.Poly(quotient, x, y), a0, a1, spectrum


def is_mask(poly: sp.Poly) -> bool:
    return all(coefficient == 1 for coefficient in poly.coeffs())


def mask_identity_certificate(start: int = 4, stop: int = 14) -> dict[str, object]:
    records = []
    passed = True
    for source_size in range(start, stop + 1):
        x, y, quotient, a0, a1, spectrum = masks(source_size)
        quotient_augmentation = int(quotient.eval({x: 1, y: 1}))
        record = {
            "source_size": source_size,
            "quotient_has_negative_coefficient": any(
                coefficient < 0 for coefficient in quotient.coeffs()
            ),
            "quotient_augmentation": quotient_augmentation,
            "complement_size_0": len(a0.terms()),
            "complement_size_1": len(a1.terms()),
            "spectrum_size": len(spectrum.terms()),
            "a0_is_mask": is_mask(a0),
            "a1_is_mask": is_mask(a1),
            "spectrum_is_mask": is_mask(spectrum),
            "strict_U_below_S_squared": 3 * source_size < source_size**2,
        }
        record["pass"] = (
            record["quotient_has_negative_coefficient"]
            and quotient_augmentation == 3
            and len(a0.terms()) == 3 * source_size
            and len(a1.terms()) == 3 * source_size
            and len(spectrum.terms()) == 3 * source_size**2
            and record["a0_is_mask"]
            and record["a1_is_mask"]
            and record["spectrum_is_mask"]
            and record["strict_U_below_S_squared"]
        )
        passed &= record["pass"]
        records.append(record)
    return {
        "parameter_range": [start, stop],
        "records": records,
        "all_parameter_identity_proved_in_manuscript": True,
        "pass": passed,
    }


def support_values(poly: sp.Poly, alpha: sp.Expr, beta: sp.Expr) -> set[sp.Expr]:
    return {
        sp.simplify(monomial[0] * alpha + monomial[1] * beta)
        for monomial, coefficient in poly.terms()
        if coefficient
    }


def euclidean_certificate(source_size: int = 4) -> dict[str, object]:
    x, y, quotient, a0_poly, a1_poly, spectrum_poly = masks(source_size)
    root2 = sp.sqrt(2)
    kappa = sp.simplify(source_size + (source_size - 1) / root2)
    step = sp.simplify(kappa / (2 * source_size**2))
    alpha = step
    beta = sp.simplify(step / root2)
    epsilon = sp.Rational(1, 4 * source_size)
    lam0 = sp.simplify(alpha / epsilon)
    lam1 = sp.simplify(beta / epsilon)
    z0 = sp.simplify(lam0 / 2)
    z1 = sp.simplify(lam1 / 2)

    source = [sp.simplify(index * epsilon) for index in range(source_size)]
    a0 = support_values(a0_poly, alpha, beta)
    a1 = support_values(a1_poly, alpha, beta)
    spectrum = support_values(spectrum_poly, alpha, beta)

    chosen_a0 = sp.simplify(source_size * alpha + source_size * beta)
    chosen_a1 = beta
    tangent_identity = sp.simplify(chosen_a0 - chosen_a1 - z0**2 + z1**2) == 0

    translation = sp.Integer(100)
    tangents0 = {sp.simplify(translation + value - 1 - z0**2) for value in a0}
    tangents1 = {sp.simplify(translation + value - 1 - z1**2) for value in a1}
    common_tangent = sp.simplify(translation + chosen_a0 - 1 - z0**2)

    row0 = {
        sp.simplify(1 + z0**2 + tangent + 2 * z0 * source_value)
        for tangent in tangents0
        for source_value in source
    }
    row1 = {
        sp.simplify(1 + z1**2 + tangent + 2 * z1 * source_value)
        for tangent in tangents1
        for source_value in source
    }
    translated_spectrum = {
        sp.simplify(translation + value) for value in spectrum
    }

    # Check the Cartesian squared-distance identity on the common tangent.
    radial_anchor = sp.Integer(3)
    distance_identities = []
    for source_value in source:
        source_point = sp.Matrix(
            [radial_anchor + sp.sqrt(1 - source_value**2), 0, source_value]
        )
        for height in (z0, z1):
            target_point = sp.Matrix(
                [radial_anchor, sp.sqrt(common_tangent), -height]
            )
            squared_distance = sp.simplify(
                sum((source_point[index] - target_point[index]) ** 2 for index in range(3))
            )
            expected = sp.simplify(
                1 + height**2 + common_tangent + 2 * height * source_value
            )
            distance_identities.append(sp.simplify(squared_distance - expected) == 0)

    return {
        "source_size": source_size,
        "source_step": str(epsilon),
        "alpha": str(alpha),
        "beta": str(beta),
        "alpha_over_beta": str(sp.simplify(alpha / beta)),
        "source_values_inside_unit_interval": all(
            0 <= float(value) < 1 for value in source
        ),
        "complement_sizes": [len(a0), len(a1)],
        "spectrum_size": len(spectrum),
        "common_tangent_identity": tangent_identity,
        "common_tangent_in_both_sets": (
            common_tangent in tangents0 and common_tangent in tangents1
        ),
        "all_tangents_positive": all(
            float(sp.N(value)) > 0 for value in tangents0 | tangents1
        ),
        "row0_equals_spectrum": row0 == translated_spectrum,
        "row1_equals_spectrum": row1 == translated_spectrum,
        "row0_injective": len(row0) == 3 * source_size**2,
        "row1_injective": len(row1) == 3 * source_size**2,
        "all_cartesian_distance_identities": all(distance_identities),
        "pass": (
            tangent_identity
            and common_tangent in tangents0
            and common_tangent in tangents1
            and all(float(sp.N(value)) > 0 for value in tangents0 | tangents1)
            and row0 == translated_spectrum
            and row1 == translated_spectrum
            and len(row0) == 3 * source_size**2
            and len(row1) == 3 * source_size**2
            and all(distance_identities)
        ),
    }


def main() -> int:
    result = {
        "mask_identities": mask_identity_certificate(),
        "euclidean_realization": euclidean_certificate(),
    }
    result["pass"] = all(result[key]["pass"] for key in result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
