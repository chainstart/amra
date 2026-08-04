#!/usr/bin/env python3
"""Exact nested shared/nonshared discriminant certificate (stdlib only)."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json

from verify_c_zero_fibre import (
    EDGES,
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_nonnegative_route_chambers import permute, state_polynomial
from verify_shared_page_discriminant import coefficient as original_coefficient
from verify_shared_page_discriminant import divide_monomial as original_divide_monomial


B_EDGE = (0, 4)
X01 = (0, 1)
X02 = (0, 2)
C_EDGE = (1, 2)
X13 = (1, 3)
X23 = (2, 3)
X14 = (1, 4)
X24 = (2, 4)

# Local slots are (c,b=x02,r=x13,z=x23,q=q4,t).
COUNT = 6
ZERO = (0,) * COUNT


def add(left, right, scale=1):
    scale = Fraction(scale)
    result = dict(left)
    for monomial, value in right.items():
        result[monomial] = result.get(monomial, Fraction()) + scale * value
    return {monomial: value for monomial, value in result.items() if value}


def multiply(left, right):
    result = {}
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            result[monomial] = result.get(monomial, Fraction()) + left_value * right_value
    return {monomial: value for monomial, value in result.items() if value}


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {monomial: scalar * value for monomial, value in poly.items() if scalar * value}


def constant(value):
    value = Fraction(value)
    return {} if not value else {ZERO: value}


def variable(slot, scalar=1):
    monomial = [0] * COUNT
    monomial[slot] = 1
    return {tuple(monomial): Fraction(scalar)}


def power(poly, exponent):
    result = constant(1)
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def cleared_nonshared_right_substitution(poly):
    """Substitute x24=-t, x14=(q+t)/(1-t), and clear (1-t)^2."""
    c, b, r, z, q, t = (variable(slot) for slot in range(COUNT))
    one_minus_t = add(constant(1), t, -1)
    q_plus_t = add(q, t)
    substitutions = {
        C_EDGE: c,
        X02: b,
        X13: r,
        X23: z,
        X14: q_plus_t,
        X24: scale(t, -1),
    }
    result = {}
    for monomial, value in poly.items():
        assert monomial[EDGES.index(B_EDGE)] == 0
        assert monomial[EDGES.index(X01)] == 0
        x14_degree = monomial[EDGES.index(X14)]
        assert x14_degree <= 2
        term = constant(value)
        for edge, replacement in substitutions.items():
            term = multiply(term, power(replacement, monomial[EDGES.index(edge)]))
        term = multiply(term, power(one_minus_t, 2 - x14_degree))
        result = add(result, term)
    return result


def divide_one_minus_variable(poly, slot):
    """Divide exactly by 1-x_slot using coefficient recurrence."""
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


def coefficient(poly, slot, degree):
    result = {}
    for monomial, value in poly.items():
        if monomial[slot] != degree:
            continue
        reduced = list(monomial)
        reduced[slot] = 0
        result[tuple(reduced)] = value
    return result


def canonical(poly):
    return json.dumps(
        [[list(m), c.numerator, c.denominator] for m, c in sorted(poly.items())],
        separators=(",", ":"),
    )


def digest(poly):
    return sha256(canonical(poly).encode()).hexdigest()


def quadratic_bernstein_certificate(poly, factor_power, expected_counts):
    cleared = cleared_nonshared_right_substitution(poly)
    quotient = cleared
    for _ in range(factor_power):
        quotient = divide_one_minus_variable(quotient, 5)
    rebuilt = multiply(quotient, power(add(constant(1), variable(5), -1), factor_power))
    assert rebuilt == cleared
    assert max(monomial[5] for monomial in quotient) == 2

    q0 = coefficient(quotient, 5, 0)
    q1 = coefficient(quotient, 5, 1)
    q2 = coefficient(quotient, 5, 2)
    beta0 = q0
    beta1 = add(q0, scale(q1, Fraction(1, 2)))
    beta2 = add(add(q0, q1), q2)
    determinant = add(multiply(beta0, beta2), multiply(beta1, beta1), -1)

    counts = tuple(len(poly) for poly in (beta0, beta1, beta2, determinant))
    assert counts == expected_counts
    assert all(value > 0 for value in beta0.values())
    assert all(value > 0 for value in beta2.values())
    assert all(value > 0 for value in determinant.values())
    return {
        "cleared": cleared,
        "quotient": quotient,
        "beta0": beta0,
        "beta1": beta1,
        "beta2": beta2,
        "determinant": determinant,
        "counts": counts,
        "beta1_negative_terms": sum(value < 0 for value in beta1.values()),
    }


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

    a2 = original_coefficient(delta, X01, 2)
    a1 = original_coefficient(delta, X01, 1)
    a0 = original_coefficient(delta, X01, 0)
    discriminant = add_original(
        multiply_original(a1, a1), multiply_original(a2, a0), -4
    )
    divided = original_divide_monomial(
        discriminant,
        {C_EDGE: 2, X02: 2, X13: 2, X14: 2},
    )
    assert all(value % 4 == 0 for value in divided.values())
    H = {monomial: -value // 4 for monomial, value in divided.items()}
    assert len(H) == 215 and all(value > 0 for value in H.values())

    a2_certificate = quadratic_bernstein_certificate(
        a2, factor_power=1, expected_counts=(35, 41, 50, 367)
    )
    h_certificate = quadratic_bernstein_certificate(
        H, factor_power=2, expected_counts=(17, 28, 57, 237)
    )
    assert a2_certificate["beta1_negative_terms"] == 10
    assert h_certificate["beta1_negative_terms"] == 19

    # Exact graph relabelings transport LPR to the other three chambers.
    lpr = state_polynomial(delta, tuple("LPR"))
    rpl = state_polynomial(delta, tuple("RPL"))
    lrp = state_polynomial(delta, tuple("LRP"))
    rlp = state_polynomial(delta, tuple("RLP"))
    hub_swap_for_lpr = (0, 1, 2, 4, 3, 5, 6)
    page_swap = (0, 1, 2, 5, 6, 3, 4)
    assert rpl == permute(lpr, hub_swap_for_lpr)
    assert lrp == permute(lpr, page_swap)
    assert rlp == permute(permute(lpr, hub_swap_for_lpr), page_swap)

    records = {}
    for prefix, certificate in (("A2", a2_certificate), ("H", h_certificate)):
        for name in ("cleared", "quotient", "beta0", "beta1", "beta2", "determinant"):
            records[f"{prefix}_{name}"] = certificate[name]
    print(json.dumps({
        "schema": "amra.opg1757.round7.nested-shared-discriminant.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
            "shared_discriminant_residual_terms": len(H),
        },
        "representative": {
            "sign_chamber": "LPR",
            "substitution": "x24=-t, x14=(q4+t)/(1-t), 0<=t<1; x02,x13,x23,c,q4>=0; x01 arbitrary real",
            "A2_cleared_factor": "(1-t)",
            "H_cleared_factor": "(1-t)^2",
            "A2_bernstein_term_counts": list(a2_certificate["counts"]),
            "H_bernstein_term_counts": list(h_certificate["counts"]),
            "A2_beta1_negative_terms": a2_certificate["beta1_negative_terms"],
            "H_beta1_negative_terms": h_certificate["beta1_negative_terms"],
            "endpoint_and_determinant_coefficients_strictly_positive": True,
        },
        "consequence": "A2>=0 and H>=0 on the parameterized nonshared-right route, so the x01 quadratic Delta_b has nonpositive discriminant and is nonnegative for every real x01",
        "certified_chambers_added": ["LPR", "LRP", "RLP", "RPL"],
        "combined_nonnegative_route_coverage": "17 of 27 chambers together with NONNEGATIVE_ROUTE_CHAMBERS.md and SHARED_PAGE_DISCRIMINANT.md",
        "symmetry_checks": {
            "hub_exchange": "LPR -> RPL",
            "nonshared_page_exchange": "LPR -> LRP",
            "composition": "LPR -> RLP",
            "checked_on_exact_cleared_polynomials": True,
        },
        "records": {
            name: {"terms": len(poly), "sha256": digest(poly)}
            for name, poly in records.items()
        },
        "scope": "exact nested coordinate-discriminant theorem; PLR/PRL, all-eight-three-negative chambers, and negative effective routes remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
