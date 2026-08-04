#!/usr/bin/env python3
"""Exact double-Gram certificate for four positive-nonshared c<0 chambers."""

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


def t3_gram_certificate(poly, states, denominator_degrees, expected_common):
    raw = schur_substitute(
        uniform_state_polynomial(
            poly,
            states,
            denominator_degrees=denominator_degrees,
        )
    )
    reduced = divide_one_minus_variable(raw, 4)
    one_minus_t3 = add(constant(1), variable(4), -1)
    assert raw == multiply(reduced, one_minus_t3)
    assert max(monomial[4] for monomial in reduced) == 2

    a0, a1, a2 = (coefficient(reduced, 4, degree) for degree in range(3))
    gamma0 = a0
    gamma1 = add(a0, scale(a1, Fraction(1, 2)))
    gamma2 = add(add(a0, a1), a2)
    gamma0_bernstein = bernstein_transform(gamma0, [2, 6, 7])
    gamma2_bernstein = bernstein_transform(gamma2, [2, 6, 7])
    assert gamma0_bernstein and gamma2_bernstein
    assert all(value > 0 for value in gamma0_bernstein.values())
    assert all(value > 0 for value in gamma2_bernstein.values())

    determinant = add(
        multiply(gamma0, gamma2),
        multiply(gamma1, gamma1),
        -1,
    )
    common = tuple(
        min(monomial[slot] for monomial in determinant) for slot in range(8)
    )
    assert common == expected_common
    determinant_residual = divide_monomial(determinant, common)
    determinant_bernstein = bernstein_transform(
        determinant_residual,
        [2, 6, 7],
    )
    assert determinant_bernstein
    assert all(value > 0 for value in determinant_bernstein.values())

    return {
        "cleared_factor": "raw=(1-t3)*tilde",
        "formula": "tilde=(1-t3)^2*gamma0+2*t3*(1-t3)*gamma1+t3^2*gamma2",
        "gamma0_bernstein_nonzero": len(gamma0_bernstein),
        "gamma0_minimum_bernstein_coefficient": str(
            min(gamma0_bernstein.values())
        ),
        "gamma2_bernstein_nonzero": len(gamma2_bernstein),
        "gamma2_minimum_bernstein_coefficient": str(
            min(gamma2_bernstein.values())
        ),
        "determinant_common_monomial": list(common),
        "determinant_terms": len(determinant),
        "determinant_bernstein_nonzero": len(determinant_bernstein),
        "determinant_minimum_bernstein_coefficient": str(
            min(determinant_bernstein.values())
        ),
        "raw_sha256": digest(raw),
        "reduced_sha256": digest(reduced),
        "gamma0_sha256": digest(gamma0),
        "gamma2_sha256": digest(gamma2),
        "determinant_residual_sha256": digest(determinant_residual),
    }


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

    representative = tuple("LLP")
    assert required_denominator_degrees(A2, representative) == (2, 2, 2)
    assert required_denominator_degrees(H, representative) == (2, 3, 3)
    A2_record = t3_gram_certificate(
        A2,
        representative,
        (2, 2, 2),
        (0, 0, 0, 3, 0, 4, 0, 0),
    )
    H_record = t3_gram_certificate(
        H,
        representative,
        (2, 3, 3),
        (0, 0, 0, 3, 0, 5, 0, 0),
    )

    states = ("LLP", "LPL", "RRP", "RPR")
    cleared_delta = {
        state: state_polynomial(delta, tuple(state)) for state in states
    }
    hub_swap = {
        X01: X02,
        X02: X01,
        X13: X23,
        X23: X13,
        X14: X24,
        X24: X14,
    }
    assert delta == permute_edges(delta, hub_swap)
    hub_positive_page_swap = (0, 1, 2, 3, 4, 6, 5)
    page_swap = (0, 1, 2, 5, 6, 3, 4)
    assert cleared_delta["RRP"] == permute(
        cleared_delta["LLP"],
        hub_positive_page_swap,
    )
    assert cleared_delta["LPL"] == permute(cleared_delta["LLP"], page_swap)
    assert cleared_delta["RPR"] == permute(cleared_delta["RRP"], page_swap)

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-c-positive-nonshared-gram.v1",
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
            "strategy": "prove A2>=0 and H>=0 by separate exact t3 Gram certificates",
        },
        "denominator_clearing": {
            "invariant": "each declared page degree equals the polynomial degree in that page's rational-side activity",
            "A2_page_degrees": [2, 2, 2],
            "H_page_degrees": [2, 3, 3],
        },
        "A2_t3_gram": A2_record,
        "H_t3_gram": H_record,
        "representative": "LLP",
        "symmetry_images": {
            "page_exchange": "LPL",
            "hub_exchange": "RRP",
            "both": "RPR",
            "checked_on_exact_cleared_Delta_b": True,
        },
        "certified_chambers": list(states),
        "certified_count": len(states),
        "conclusion": "Delta_b>=0 in all four listed positive-nonshared c-negative Schur chambers",
        "scope": "four additional interior c-negative chambers; together with the preceding certificates this gives 24 of 27, while PPP, PLL, PRR, negative-page cases, and the global marked-host theorem remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
