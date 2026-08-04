#!/usr/bin/env python3
"""Exact LLL/RRR three-negative chamber certificate (stdlib only)."""

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
    constant,
    multiply,
    power,
    scale,
    state_polynomial,
    variable,
)
from verify_opposite_nonshared_chambers import divide_one_minus_variable


def bernstein_entries(poly, slot, degree):
    power_entries = [coefficient(poly, slot, index) for index in range(degree + 1)]
    return tuple(
        sum_polynomials(
            scale(
                power_entries[power_degree],
                Fraction(comb(index, power_degree), comb(degree, power_degree)),
            )
            for power_degree in range(index + 1)
        )
        for index in range(degree + 1)
    )


def sum_polynomials(polynomials):
    result = {}
    for poly in polynomials:
        result = add(result, poly)
    return result


def gram_determinant(entries):
    assert len(entries) == 3
    return add(multiply(entries[0], entries[2]), multiply(entries[1], entries[1]), -1)


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

    # Slots are (c,q0,t0,q3,t3,q4,t4).  Every page uses its left-negative
    # route chart.  The two nonshared square denominators each lose one exact
    # factor; the shared page does not.
    lll_cleared = state_polynomial(delta, tuple("LLL"))
    quotient = divide_one_minus_variable(
        divide_one_minus_variable(lll_cleared, 4), 6
    )
    rebuilt = multiply(
        multiply(quotient, add(constant(1), variable(4), -1)),
        add(constant(1), variable(6), -1),
    )
    assert rebuilt == lll_cleared
    assert [max(m[slot] for m in quotient) for slot in (2, 4, 6)] == [4, 2, 2]

    # Regard the quotient as a quadratic in t3.  Its endpoint entries are
    # quadratics in t4 and admit exact 2x2 Bernstein Gram certificates.
    t3_entries = bernstein_entries(quotient, 4, 2)
    endpoint_certificates = []
    for endpoint, expected_counts, expected_determinant_terms in (
        (t3_entries[0], (33, 39, 51), 224),
        (t3_entries[2], (51, 62, 76), 543),
    ):
        t4_entries = bernstein_entries(endpoint, 6, 2)
        endpoint_determinant = gram_determinant(t4_entries)
        assert tuple(len(poly) for poly in t4_entries) == expected_counts
        assert all(value > 0 for value in t4_entries[0].values())
        assert all(value > 0 for value in t4_entries[2].values())
        assert len(endpoint_determinant) == expected_determinant_terms
        assert all(value > 0 for value in endpoint_determinant.values())
        endpoint_certificates.append((t4_entries, endpoint_determinant))

    # The remaining t3 Gram determinant has an exact t0^2 factor.  Its
    # residual is quartic in t4, and all five Bernstein coefficient
    # polynomials are coefficientwise strictly positive.
    t3_determinant = gram_determinant(t3_entries)
    determinant_residual = divide_monomial(t3_determinant, {2: 2})
    t4_quartic_entries = bernstein_entries(determinant_residual, 6, 4)
    assert tuple(len(poly) for poly in t4_quartic_entries) == (224, 321, 481, 514, 543)
    assert all(
        value > 0
        for entry in t4_quartic_entries
        for value in entry.values()
    )

    # With no positive raw-activity page, global hub exchange preserves the
    # (q,t) slots and makes the RRR cleared polynomial literally identical.
    rrr_cleared = state_polynomial(delta, tuple("RRR"))
    assert rrr_cleared == lll_cleared

    records = {
        "LLL_cleared": lll_cleared,
        "LLL_quotient": quotient,
        "t3_beta0": t3_entries[0],
        "t3_beta1": t3_entries[1],
        "t3_beta2": t3_entries[2],
        "t3_gram_determinant": t3_determinant,
        "t3_gram_determinant_residual": determinant_residual,
        "t3_beta0_t4_gram_determinant": endpoint_certificates[0][1],
        "t3_beta2_t4_gram_determinant": endpoint_certificates[1][1],
    }
    records.update({
        f"t3_gram_residual_t4_beta{index}": poly
        for index, poly in enumerate(t4_quartic_entries)
    })
    print(json.dumps({
        "schema": "amra.opg1757.round7.same-side-three-negative.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "representative": {
            "sign_chamber": "LLL",
            "substitution": "x_iL=-t_i, x_iR=(q_i+t_i)/(1-t_i), 0<=t_i<1 for i=0,3,4",
            "cleared_identity": "product_i(1-t_i)^2*Delta_b=(1-t3)*(1-t4)*Q",
            "Q_degrees_in_t0_t3_t4": [4, 2, 2],
            "Q_terms": len(quotient),
        },
        "nested_certificate": {
            "outer_variable": "t3",
            "endpoint_t4_bernstein_term_counts": [
                [len(poly) for poly in certificate[0]]
                for certificate in endpoint_certificates
            ],
            "endpoint_t4_gram_determinant_terms": [
                len(certificate[1]) for certificate in endpoint_certificates
            ],
            "outer_gram_determinant_factor": "t0^2",
            "outer_gram_residual_t4_degree": 4,
            "outer_gram_residual_t4_bernstein_term_counts": [
                len(poly) for poly in t4_quartic_entries
            ],
            "all_required_endpoint_determinant_and_quartic_coefficients_strictly_positive": True,
        },
        "certified_chambers_added": ["LLL", "RRR"],
        "combined_nonnegative_route_coverage": "21 of 27 chambers",
        "symmetry_check": "RRR cleared polynomial is exactly identical to LLL under global hub exchange",
        "records": {
            name: {"terms": len(poly), "sha256": digest(poly)}
            for name, poly in records.items()
        },
        "scope": "exact same-hub-side three-negative theorem; six mixed three-negative chambers and all negative-effective-route cases remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
