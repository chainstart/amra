#!/usr/bin/env python3
"""Exact PLR/PRL chamber certificate (Python standard library only)."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from math import comb
import json

from verify_c_zero_fibre import (
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_nonnegative_route_chambers import (
    B_EDGE,
    add,
    coefficient,
    multiply,
    permute,
    scale,
    state_polynomial,
)


def divide_one_minus_variable(poly, slot):
    """Divide a sparse polynomial exactly by 1-x_slot."""
    grouped = {}
    for monomial, value in poly.items():
        key = monomial[:slot] + monomial[slot + 1 :]
        grouped.setdefault(key, {})[monomial[slot]] = value
    quotient = {}
    for key, coefficients in grouped.items():
        degree = max(coefficients)
        previous = Fraction()
        for exponent in range(degree):
            value = coefficients.get(exponent, Fraction()) + previous
            if value:
                monomial = key[:slot] + (exponent,) + key[slot:]
                quotient[monomial] = value
            previous = value
        assert coefficients.get(degree, Fraction()) == -previous
    return quotient


def quadratic_bernstein_entries(poly, slot):
    power_entries = [coefficient(poly, slot, degree) for degree in range(3)]
    beta0 = power_entries[0]
    beta1 = add(power_entries[0], scale(power_entries[1], Fraction(1, 2)))
    beta2 = add(add(power_entries[0], power_entries[1]), power_entries[2])
    return beta0, beta1, beta2


def determinant(entries):
    beta0, beta1, beta2 = entries
    return add(multiply(beta0, beta2), multiply(beta1, beta1), -1)


def divide_monomial(poly, degrees):
    result = {}
    for monomial, value in poly.items():
        reduced = list(monomial)
        for slot, degree in degrees.items():
            assert reduced[slot] >= degree
            reduced[slot] -= degree
        result[tuple(reduced)] = value
    return result


def canonical(poly):
    return json.dumps(
        [[list(m), c.numerator, c.denominator] for m, c in sorted(poly.items())],
        separators=(",", ":"),
    )


def digest(poly):
    return sha256(canonical(poly).encode()).hexdigest()


def main():
    deletion, connectivity, forest_count, connected_count = reconstruct_original()
    assert (forest_count, connected_count) == (128, 58)
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(
        multiply_original(a_slope, e_zero),
        multiply_original(d_slope, c_zero),
        -1,
    )

    # Slots are (c,a=x01,b=x02,q=q3,u,r=q4,s).  In PLR,
    # x13=-u, x23=(q+u)/(1-u), x14=(r+s)/(1-s), x24=-s.
    plr_cleared = state_polynomial(delta, tuple("PLR"))
    quotient = divide_one_minus_variable(
        divide_one_minus_variable(plr_cleared, 4), 6
    )
    assert max(monomial[4] for monomial in quotient) == 2
    assert max(monomial[6] for monomial in quotient) == 2

    # First Bernstein--Gram layer: regard the bidegree-(2,2) quotient as a
    # quadratic in u.  Its two endpoint entries must themselves be
    # nonnegative quadratics in s.
    u_entries = quadratic_bernstein_entries(quotient, 4)
    f0_s_entries = quadratic_bernstein_entries(u_entries[0], 6)
    f2_s_entries = quadratic_bernstein_entries(u_entries[2], 6)
    f0_s_determinant = determinant(f0_s_entries)
    f2_s_determinant = determinant(f2_s_entries)
    assert tuple(len(poly) for poly in f0_s_entries) == (9, 11, 14)
    assert tuple(len(poly) for poly in f2_s_entries) == (14, 20, 28)
    for endpoint_entries in (f0_s_entries, f2_s_entries):
        assert all(value > 0 for value in endpoint_entries[0].values())
        assert all(value > 0 for value in endpoint_entries[2].values())
    assert len(f0_s_determinant) == 53
    assert len(f2_s_determinant) == 175
    assert all(value > 0 for value in f0_s_determinant.values())
    assert all(value > 0 for value in f2_s_determinant.values())

    # Second layer: D=f0*f2-f1^2.  Remove the exact a^2*b^2 factor and
    # regard the residual R as a quadratic in b.  Its constant coefficient
    # is positive, while its discriminant is coefficientwise strictly
    # negative.  This certifies D>=0 without a quartic-in-s SOS ansatz.
    u_determinant = determinant(u_entries)
    residual = divide_monomial(u_determinant, {1: 2, 2: 2})
    b_entries = tuple(coefficient(residual, 2, degree) for degree in range(3))
    b_discriminant = add(
        multiply(b_entries[1], b_entries[1]),
        multiply(b_entries[0], b_entries[2]),
        -4,
    )
    assert tuple(len(poly) for poly in b_entries) == (73, 151, 241)
    assert all(value > 0 for value in b_entries[0].values())
    assert len(b_discriminant) == 1247
    assert all(value < 0 for value in b_discriminant.values())

    # Global hub exchange changes PLR into PRL.  Check the exact cleared
    # identity; only the two raw activities of the positive page are swapped.
    prl_cleared = state_polynomial(delta, tuple("PRL"))
    assert prl_cleared == permute(plr_cleared, (0, 2, 1, 3, 4, 5, 6))

    records = {
        "PLR_cleared": plr_cleared,
        "PLR_bidegree_quotient": quotient,
        "u_beta0": u_entries[0],
        "u_beta1": u_entries[1],
        "u_beta2": u_entries[2],
        "u_gram_determinant": u_determinant,
        "u_gram_determinant_residual": residual,
        "f0_s_gram_determinant": f0_s_determinant,
        "f2_s_gram_determinant": f2_s_determinant,
        "residual_b_constant": b_entries[0],
        "residual_b_linear": b_entries[1],
        "residual_b_quadratic": b_entries[2],
        "residual_b_discriminant": b_discriminant,
    }
    print(json.dumps({
        "schema": "amra.opg1757.round7.opposite-nonshared-chambers.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "representative": {
            "sign_chamber": "PLR",
            "substitution": "x13=-u, x23=(q3+u)/(1-u), x14=(q4+s)/(1-s), x24=-s, 0<=u,s<1",
            "cleared_identity": "(1-u)^2*(1-s)^2*Delta_b=(1-u)*(1-s)*Q(u,s)",
            "Q_bidegree": [2, 2],
            "Q_terms": len(quotient),
        },
        "nested_certificate": {
            "u_bernstein_endpoint_term_counts": [len(u_entries[0]), len(u_entries[2])],
            "f0_s_bernstein_term_counts": [len(poly) for poly in f0_s_entries],
            "f2_s_bernstein_term_counts": [len(poly) for poly in f2_s_entries],
            "f0_s_gram_determinant_terms": len(f0_s_determinant),
            "f2_s_gram_determinant_terms": len(f2_s_determinant),
            "endpoint_and_gram_coefficients_strictly_positive": True,
            "u_gram_determinant_factor": "a^2*b^2*R",
            "R_as_quadratic_in_b_term_counts": [len(poly) for poly in b_entries],
            "R_b_constant_coefficients_strictly_positive": True,
            "R_b_discriminant_terms": len(b_discriminant),
            "R_b_discriminant_coefficients_strictly_negative": True,
        },
        "certified_chambers_added": ["PLR", "PRL"],
        "combined_nonnegative_route_coverage": "19 of 27 chambers; only the eight three-negative chambers remain",
        "symmetry_check": "PRL is the exact hub-exchange image of PLR",
        "records": {
            name: {"terms": len(poly), "sha256": digest(poly)}
            for name, poly in records.items()
        },
        "scope": "exact opposite-nonshared chamber theorem; the eight three-negative chambers and all negative-effective-route cases remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
