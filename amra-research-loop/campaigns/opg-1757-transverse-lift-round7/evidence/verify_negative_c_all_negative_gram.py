#!/usr/bin/env python3
"""Exact nested-Gram certificate for the RRR/LLL c-negative chambers."""

from __future__ import annotations

from fractions import Fraction
import json

from verify_c_zero_fibre import (
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_negative_c_direct_chambers import (
    add,
    bernstein_transform,
    constant,
    digest,
    multiply,
    power,
    variable,
)
from verify_negative_c_schur_endpoint import schur_substitute, uniform_state_polynomial
from verify_shared_page_discriminant import (
    C_EDGE,
    X01,
    X02,
    X13,
    X14,
    X23,
    X24,
    coefficient as original_coefficient,
    divide_monomial as divide_original_monomial,
    permute_edges,
)


B_EDGE = (0, 4)


def coefficient(poly, slot, degree):
    result = {}
    for monomial, value in poly.items():
        if monomial[slot] != degree:
            continue
        reduced = list(monomial)
        reduced[slot] = 0
        result[tuple(reduced)] = value
    return result


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {monomial: scalar * value for monomial, value in poly.items() if value}


def square(poly):
    return multiply(poly, poly)


def divide_one_minus_variable(poly, slot):
    """Exact division by 1-x_slot, asserting a zero remainder."""
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


def divide_monomial(poly, factor):
    result = {}
    for monomial, value in poly.items():
        reduced = tuple(degree - removed for degree, removed in zip(monomial, factor))
        assert all(degree >= 0 for degree in reduced)
        result[reduced] = value
    return result


def product(*factors):
    result = constant(1)
    for factor in factors:
        result = multiply(result, factor)
    return result


def total(*summands):
    result = {}
    for summand in summands:
        result = add(result, summand)
    return result


def main():
    deletion, connectivity, forest_count, connected_count = reconstruct_original()
    assert (forest_count, connected_count) == (128, 58)
    A = derivative(deletion, (B_EDGE,))
    C = restrict_original_zero(deletion, B_EDGE)
    D = derivative(connectivity, (B_EDGE,))
    E = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(multiply_original(A, E), multiply_original(D, C), -1)
    assert len(delta) == 178

    A2 = original_coefficient(delta, X01, 2)
    A1 = original_coefficient(delta, X01, 1)
    A0 = original_coefficient(delta, X01, 0)
    discriminant = add_original(
        multiply_original(A1, A1),
        multiply_original(A2, A0),
        -4,
    )
    divided = divide_original_monomial(
        discriminant,
        {C_EDGE: 2, X02: 2, X13: 2, X14: 2},
    )
    assert all(value % 4 == 0 for value in divided.values())
    H = {monomial: -value // 4 for monomial, value in divided.items()}
    assert len(H) == 215

    hub_swap = {
        X01: X02,
        X02: X01,
        X13: X23,
        X23: X13,
        X14: X24,
        X24: X14,
    }
    assert delta == permute_edges(delta, hub_swap)

    states = tuple("RRR")
    schur_A2 = schur_substitute(uniform_state_polynomial(A2, states))
    A2_bernstein = bernstein_transform(schur_A2, [2, 4, 6, 7])
    assert A2_bernstein
    assert all(value > 0 for value in A2_bernstein.values())

    raw_schur_H = schur_substitute(uniform_state_polynomial(H, states))
    schur_H = divide_one_minus_variable(
        divide_one_minus_variable(raw_schur_H, 2),
        2,
    )
    assert raw_schur_H == multiply(schur_H, power(add(constant(1), variable(2), -1), 2))
    s0_degree = max(monomial[2] for monomial in schur_H)
    assert s0_degree == 2, (s0_degree, len(schur_H))
    a0, a1, a2 = (coefficient(schur_H, 2, degree) for degree in range(3))
    beta0 = a0
    beta1 = add(a0, scale(a1, Fraction(1, 2)))
    beta2 = add(add(a0, a1), a2)
    beta0_bernstein = bernstein_transform(beta0, [4, 6, 7])
    beta1_bernstein = bernstein_transform(beta1, [4, 6, 7])
    assert beta0_bernstein
    assert all(value > 0 for value in beta0_bernstein.values())
    assert beta1_bernstein

    one = constant(1)
    q0, q3, t3, q4, t4, tau = (
        variable(1),
        variable(3),
        variable(4),
        variable(5),
        variable(6),
        variable(7),
    )
    one_minus_t3 = add(one, t3, -1)
    one_minus_t4 = add(one, t4, -1)
    one_minus_tau = add(one, tau, -1)
    q0q3 = multiply(q0, q3)
    q0q4 = multiply(q0, q4)
    q3q4 = multiply(q3, q4)
    q0q3q4 = multiply(q0q3, q4)
    B_schur = total(q0q3q4, q0q3, q0q4, q3q4)
    D_schur = total(
        multiply(one_minus_tau, total(q0q3q4, q0q3, q0q4)),
        q3q4,
    )
    difference = add(multiply(q3, t4), multiply(q4, t3), -1)

    # The normalized beta2 is quadratic in tau.  Its three Bernstein
    # coefficients below are sums of nonnegative products on the unit box.
    beta2_tau_zero = multiply(
        square(B_schur),
        total(
            multiply(q3, square(t4)),
            multiply(q4, square(t3)),
            multiply(square(t3), square(t4)),
        ),
    )
    beta2_tau_one_kernel = total(
        multiply(q0, square(difference)),
        product(square(q0), q3, q4, square(t3), square(t4)),
        product(square(q0), q3, square(t3), square(t4)),
        product(square(q0), q4, square(t3), square(t4)),
        product(q0, square(q3), q4, square(t4)),
        product(q0, q3, square(q4), square(t3)),
        scale(product(q0, q3, q4, square(t3), square(t4)), 2),
        product(q0, q3, square(t3), square(t4)),
        product(q0, q4, square(t3), square(t4)),
        product(square(q3), q4, square(t4)),
        product(q3, square(q4), square(t3)),
        product(q3, q4, square(t3), square(t4)),
    )
    beta2_tau_one = multiply(q3q4, beta2_tau_one_kernel)
    beta2_tau_mid_kernel = total(
        multiply(q0, square(difference)),
        product(q0, square(q3), q4, square(t4)),
        product(q0, q3, square(q4), square(t3)),
        scale(product(q0, q3, q4, square(t3), square(t4)), 2),
        product(q0, q3, square(t3), square(t4)),
        product(q0, q4, square(t3), square(t4)),
        scale(product(square(q3), q4, square(t4)), 2),
        scale(product(q3, square(q4), square(t3)), 2),
        scale(product(q3, q4, square(t3), square(t4)), 2),
    )
    beta2_tau_mid = scale(multiply(B_schur, beta2_tau_mid_kernel), Fraction(1, 2))
    normalized_beta2 = total(
        product(square(one_minus_tau), beta2_tau_zero),
        scale(product(tau, one_minus_tau, beta2_tau_mid), 2),
        product(square(tau), beta2_tau_one),
    )
    expected_beta2 = product(
        q3,
        q4,
        square(one_minus_t3),
        square(one_minus_t4),
        normalized_beta2,
    )
    assert beta2 == expected_beta2

    determinant = add(multiply(beta0, beta2), multiply(beta1, beta1), -1)
    common = (0, 2, 0, 3, 2, 3, 2, 2)
    calculated_common = tuple(
        min(monomial[slot] for monomial in determinant) for slot in range(8)
    )
    assert calculated_common == common
    common_factor = product(
        power(q0, 2),
        power(q3, 3),
        power(t3, 2),
        power(q4, 3),
        power(t4, 2),
        power(tau, 2),
    )
    determinant_residual = divide_monomial(determinant, common)
    determinant_core = determinant_residual
    for _ in range(4):
        determinant_core = divide_one_minus_variable(determinant_core, 4)
        determinant_core = divide_one_minus_variable(determinant_core, 6)
    determinant_kernel = total(
        square(difference),
        product(square(q3), q4, square(t4)),
        product(q3, square(q4), square(t3)),
        scale(product(q3, q4, square(t3), t4), 2),
        scale(product(q3, q4, t3, square(t4)), 2),
        product(q3, square(t3), square(t4)),
        product(q4, square(t3), square(t4)),
    )
    expected_determinant_core = product(B_schur, D_schur, determinant_kernel)
    assert determinant_core == expected_determinant_core
    expected_determinant = product(
        common_factor,
        power(one_minus_t3, 4),
        power(one_minus_t4, 4),
        expected_determinant_core,
    )
    assert determinant == expected_determinant

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-c-all-negative-gram.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
            "shared_discriminant_residual_H_terms": len(H),
        },
        "domain": "q0,q3,q4>0, c=-tau*P/B with 0<=tau<=1, positive edge floors",
        "shared_quadratic": {
            "formula": "Delta_b=A2*x01^2+A1*x01+A0",
            "discriminant": "A1^2-4*A2*A0=-4*c^2*x02^2*x13^2*x14^2*H",
            "A2_bernstein_nonzero": len(A2_bernstein),
            "A2_minimum_bernstein_coefficient": str(min(A2_bernstein.values())),
            "schur_A2_sha256": digest(schur_A2),
        },
        "H_s0_gram": {
            "formula": "H=(1-s0)^2*beta0+2*s0*(1-s0)*beta1+s0^2*beta2",
            "beta0_bernstein_nonzero": len(beta0_bernstein),
            "beta0_minimum_bernstein_coefficient": str(min(beta0_bernstein.values())),
            "beta1_bernstein_nonzero": len(beta1_bernstein),
            "beta1_maximum_bernstein_coefficient": str(max(beta1_bernstein.values())),
            "beta2_factor": "q3*q4*(1-t3)^2*(1-t4)^2 times a quadratic with three explicitly nonnegative tau-Bernstein coefficients",
            "beta2_tau_bernstein": {
                "zero_sha256": digest(beta2_tau_zero),
                "middle_sha256": digest(beta2_tau_mid),
                "one_sha256": digest(beta2_tau_one),
            },
            "determinant_factor": "M*(1-t3)^4*(1-t4)^4*B*D*Q",
            "determinant_kernel_Q": "(q3*t4-q4*t3)^2 plus six nonnegative monomials",
            "determinant_common_monomial": list(common),
            "determinant_residual_terms": len(determinant_residual),
            "determinant_core_terms": len(determinant_core),
            "raw_schur_H_sha256": digest(raw_schur_H),
            "reduced_schur_H_sha256": digest(schur_H),
            "beta2_sha256": digest(beta2),
            "determinant_sha256": digest(determinant),
            "determinant_kernel_Q_sha256": digest(determinant_kernel),
        },
        "representative": "RRR",
        "hub_image": "LLL",
        "certified_chambers": ["LLL", "RRR"],
        "certified_count": 2,
        "conclusion": "Delta_b>=0 in both all-negative-activity c-negative Schur chambers",
        "scope": "two additional interior c-negative chambers; together with the direct and nonshared Gram certificates this gives 16 of 27, while eleven c-negative chambers, negative-page cases, and the global marked-host theorem remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
