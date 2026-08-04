#!/usr/bin/env python3
"""Exact nested-Gram certificate for the c<0 PLL and PRR chambers."""

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
from verify_mixed_three_negative import divide_polynomial
from verify_negative_c_all_negative_gram import (
    coefficient,
    divide_one_minus_variable,
    scale,
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
from verify_negative_c_schur_endpoint import (
    required_denominator_degrees,
    schur_substitute,
    uniform_state_polynomial,
)
from verify_nonnegative_route_chambers import state_polynomial
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


def divide_monomial(poly, factor):
    result = {}
    for monomial, value in poly.items():
        reduced = tuple(degree - removed for degree, removed in zip(monomial, factor))
        assert all(degree >= 0 for degree in reduced)
        result[reduced] = value
    return result


def permute(poly, old_to_new):
    result = {}
    for monomial, value in poly.items():
        transformed = [0] * len(monomial)
        for old, degree in enumerate(monomial):
            transformed[old_to_new[old]] = degree
        transformed = tuple(transformed)
        result[transformed] = result.get(transformed, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def gram(poly, slot):
    assert max(monomial[slot] for monomial in poly) == 2
    a0, a1, a2 = (coefficient(poly, slot, degree) for degree in range(3))
    gamma0 = a0
    gamma1 = add(a0, scale(a1, Fraction(1, 2)))
    gamma2 = add(add(a0, a1), a2)
    determinant = add(
        multiply(gamma0, gamma2),
        multiply(gamma1, gamma1),
        -1,
    )
    return gamma0, gamma1, gamma2, determinant


def strictly_positive_bernstein(poly, slots):
    transformed = bernstein_transform(poly, slots)
    assert transformed
    assert all(value > 0 for value in transformed.values())
    return transformed


def remove_one_minus_factors(poly, factors):
    quotient = poly
    expected = constant(1)
    for slot, count in factors:
        one_minus = add(constant(1), variable(slot), -1)
        for _ in range(count):
            quotient = divide_one_minus_variable(quotient, slot)
            expected = multiply(expected, one_minus)
    assert poly == multiply(quotient, expected)
    return quotient


def endpoint_square_certificate(endpoint):
    q0, q3, q4, t4, tau = (variable(slot) for slot in (1, 3, 5, 6, 7))
    one_minus_t4 = add(constant(1), t4, -1)
    one_minus_tau = add(constant(1), tau, -1)
    common = multiply(multiply(q0, q4), tau)
    entries = (
        multiply(multiply(q3, power(t4, 2)), tau),
        multiply(
            multiply(multiply(q3, power(q4, 2)), power(one_minus_t4, 2)),
            tau,
        ),
        multiply(
            multiply(
                multiply(multiply(q0, q3), q4),
                power(one_minus_t4, 2),
            ),
            one_minus_tau,
        ),
        multiply(
            multiply(multiply(q0, power(q4, 2)), power(one_minus_t4, 2)),
            one_minus_tau,
        ),
    )
    square_root = add(add(add(entries[0], entries[1], -1), entries[2], -1), entries[3], -1)
    square_term = multiply(common, power(square_root, 2))
    residual = add(endpoint, square_term, -1)
    endpoint_bernstein = bernstein_transform(endpoint, [6, 7])
    negative = {
        monomial: value
        for monomial, value in endpoint_bernstein.items()
        if value < 0
    }
    assert len(endpoint_bernstein) == 481
    assert len(negative) == 3
    assert sorted(negative.values()) == [Fraction(-1, 3), Fraction(-1, 9), Fraction(-1, 9)]
    residual_bernstein = strictly_positive_bernstein(residual, [6, 7])
    assert len(residual_bernstein) == 471
    return {
        "formula": (
            "eta2=q0*q4*tau*(q3*t4^2*tau"
            "-q3*q4^2*(1-t4)^2*tau"
            "-q0*q3*q4*(1-t4)^2*(1-tau)"
            "-q0*q4^2*(1-t4)^2*(1-tau))^2+R"
        ),
        "endpoint_terms": len(endpoint),
        "endpoint_bernstein_nonzero": len(endpoint_bernstein),
        "endpoint_negative_bernstein": len(negative),
        "square_terms": len(square_term),
        "residual_terms": len(residual),
        "residual_bernstein_nonzero": len(residual_bernstein),
        "residual_minimum_bernstein_coefficient": str(min(residual_bernstein.values())),
        "endpoint_sha256": digest(endpoint),
        "square_term_sha256": digest(square_term),
        "residual_sha256": digest(residual),
    }


def leading_coefficient_certificate(poly):
    raw = schur_substitute(
        uniform_state_polynomial(
            poly,
            tuple("PLL"),
            denominator_degrees=(0, 2, 2),
        )
    )
    reduced = remove_one_minus_factors(raw, ((4, 1), (6, 1)))
    assert len(raw) == 448
    assert len(reduced) == 144

    alpha0, alpha1, alpha2, determinant = gram(reduced, 4)
    alpha0_bernstein = strictly_positive_bernstein(alpha0, [2, 6, 7])
    alpha2_bernstein = strictly_positive_bernstein(alpha2, [2, 6, 7])
    common = tuple(min(monomial[slot] for monomial in determinant) for slot in range(8))
    assert common == (0, 4, 2, 3, 0, 2, 0, 0)
    determinant_residual = divide_monomial(determinant, common)

    q0, q3, q4, tau = (variable(slot) for slot in (1, 3, 5, 7))
    positive_schur_factor = add(
        multiply(
            multiply(add(constant(1), tau, -1), q0),
            add(add(multiply(q3, q4), q3), q4),
        ),
        multiply(q3, q4),
    )
    core = divide_polynomial(determinant_residual, positive_schur_factor)
    assert determinant_residual == multiply(positive_schur_factor, core)
    assert len(core) == 346

    eta0, eta1, eta2, core_determinant = gram(core, 2)
    eta0_bernstein = strictly_positive_bernstein(eta0, [6, 7])
    square_record = endpoint_square_certificate(eta2)
    core_common = tuple(
        min(monomial[slot] for monomial in core_determinant) for slot in range(8)
    )
    assert core_common == (0, 0, 0, 1, 0, 1, 2, 2)
    core_determinant_residual = divide_monomial(core_determinant, core_common)
    core_determinant_bernstein = strictly_positive_bernstein(
        core_determinant_residual,
        [6, 7],
    )

    return {
        "cleared_factor": "raw=(1-t3)*(1-t4)*tilde",
        "outer_formula": "tilde=(1-t3)^2*alpha0+2*t3*(1-t3)*alpha1+t3^2*alpha2",
        "raw_terms": len(raw),
        "reduced_terms": len(reduced),
        "alpha0_bernstein_nonzero": len(alpha0_bernstein),
        "alpha0_minimum_bernstein_coefficient": str(min(alpha0_bernstein.values())),
        "alpha2_bernstein_nonzero": len(alpha2_bernstein),
        "alpha2_minimum_bernstein_coefficient": str(min(alpha2_bernstein.values())),
        "outer_determinant_terms": len(determinant),
        "outer_determinant_common_monomial": list(common),
        "outer_determinant_factorization": (
            "common*((1-tau)*q0*(q3*q4+q3+q4)+q3*q4)*S"
        ),
        "core_terms": len(core),
        "inner_formula": "S=(1-s0)^2*eta0+2*s0*(1-s0)*eta1+s0^2*eta2",
        "eta0_bernstein_nonzero": len(eta0_bernstein),
        "eta0_minimum_bernstein_coefficient": str(min(eta0_bernstein.values())),
        "eta2_square_certificate": square_record,
        "inner_determinant_terms": len(core_determinant),
        "inner_determinant_common_monomial": list(core_common),
        "inner_determinant_bernstein_nonzero": len(core_determinant_bernstein),
        "inner_determinant_minimum_bernstein_coefficient": str(
            min(core_determinant_bernstein.values())
        ),
        "raw_sha256": digest(raw),
        "reduced_sha256": digest(reduced),
        "outer_determinant_residual_sha256": digest(determinant_residual),
        "core_sha256": digest(core),
        "inner_determinant_residual_sha256": digest(core_determinant_residual),
    }


def discriminant_residual_certificate(poly):
    raw = schur_substitute(
        uniform_state_polynomial(
            poly,
            tuple("PLL"),
            denominator_degrees=(0, 2, 2),
        )
    )
    reduced = remove_one_minus_factors(raw, ((4, 2), (6, 2)))
    assert len(raw) == 667
    assert len(reduced) == 111

    gamma0, gamma1, gamma2, determinant = gram(reduced, 4)
    gamma0_bernstein = strictly_positive_bernstein(gamma0, [2, 6, 7])
    gamma2_bernstein = strictly_positive_bernstein(gamma2, [2, 6, 7])
    common = tuple(min(monomial[slot] for monomial in determinant) for slot in range(8))
    assert common == (0, 4, 2, 3, 0, 2, 2, 0)
    determinant_residual = divide_monomial(determinant, common)
    determinant_bernstein = strictly_positive_bernstein(
        determinant_residual,
        [2, 6, 7],
    )
    return {
        "cleared_factor": "raw=(1-t3)^2*(1-t4)^2*tilde",
        "formula": "tilde=(1-t3)^2*gamma0+2*t3*(1-t3)*gamma1+t3^2*gamma2",
        "raw_terms": len(raw),
        "reduced_terms": len(reduced),
        "gamma0_bernstein_nonzero": len(gamma0_bernstein),
        "gamma0_minimum_bernstein_coefficient": str(min(gamma0_bernstein.values())),
        "gamma2_bernstein_nonzero": len(gamma2_bernstein),
        "gamma2_minimum_bernstein_coefficient": str(min(gamma2_bernstein.values())),
        "determinant_terms": len(determinant),
        "determinant_common_monomial": list(common),
        "determinant_bernstein_nonzero": len(determinant_bernstein),
        "determinant_minimum_bernstein_coefficient": str(
            min(determinant_bernstein.values())
        ),
        "raw_sha256": digest(raw),
        "reduced_sha256": digest(reduced),
        "determinant_residual_sha256": digest(determinant_residual),
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
    assert len(delta) == 178

    B2 = original_coefficient(delta, X02, 2)
    B1 = original_coefficient(delta, X02, 1)
    B0 = original_coefficient(delta, X02, 0)
    discriminant = add_original(
        multiply_original(B1, B1),
        multiply_original(B2, B0),
        -4,
    )
    divided = divide_original_monomial(
        discriminant,
        {C_EDGE: 2, X01: 2, X23: 2, X24: 2},
    )
    assert all(value % 4 == 0 for value in divided.values())
    H2 = {monomial: -value // 4 for monomial, value in divided.items()}
    assert len(H2) == 215

    representative = tuple("PLL")
    assert required_denominator_degrees(B2, representative) == (0, 2, 2)
    assert required_denominator_degrees(H2, representative) == (0, 2, 2)
    B2_record = leading_coefficient_certificate(B2)
    H2_record = discriminant_residual_certificate(H2)

    hub_swap = {
        X01: X02,
        X02: X01,
        X13: X23,
        X23: X13,
        X14: X24,
        X24: X14,
    }
    assert delta == permute_edges(delta, hub_swap)
    cleared_pll = state_polynomial(delta, tuple("PLL"))
    cleared_prr = state_polynomial(delta, tuple("PRR"))
    assert cleared_prr == permute(cleared_pll, (0, 2, 1, 3, 4, 5, 6))

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-c-positive-shared-gram.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
            "x02_discriminant_residual_H2_terms": len(H2),
        },
        "domain": "q0,q3,q4>0, c=-tau*P/B with 0<=tau<=1, positive edge floors",
        "shared_quadratic": {
            "formula": "Delta_b=B2*x02^2+B1*x02+B0",
            "discriminant": "B1^2-4*B2*B0=-4*c^2*x01^2*x23^2*x24^2*H2",
            "strategy": "prove B2>=0 and H2>=0 by exact nested Gram and Bernstein-square certificates",
        },
        "denominator_clearing": {
            "invariant": "each declared page degree equals the polynomial degree in that page's rational-side activity",
            "B2_page_degrees": [0, 2, 2],
            "H2_page_degrees": [0, 2, 2],
        },
        "B2_nested_gram": B2_record,
        "H2_gram": H2_record,
        "representative": "PLL",
        "symmetry_images": {
            "hub_exchange": "PRR",
            "checked_on_exact_cleared_Delta_b": True,
        },
        "certified_chambers": ["PLL", "PRR"],
        "certified_count": 2,
        "conclusion": "Delta_b>=0 in both positive-shared c-negative Schur chambers",
        "scope": "two additional interior c-negative chambers; together with the preceding certificates this gives 26 of 27, while PPP, negative-page cases, and the global marked-host theorem remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
