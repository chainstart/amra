#!/usr/bin/env python3
"""Exact nested-Gram certificate for four mixed c-negative chambers."""

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

    representative = tuple("LLR")
    assert required_denominator_degrees(A2, representative) == (2, 2, 2)
    assert required_denominator_degrees(H, representative) == (2, 3, 2)
    schur_A2 = schur_substitute(
        uniform_state_polynomial(
            A2,
            representative,
            denominator_degrees=(2, 2, 2),
        )
    )
    A2_bernstein = bernstein_transform(schur_A2, [2, 4, 6, 7])
    assert A2_bernstein
    assert all(value > 0 for value in A2_bernstein.values())

    raw_schur_H = schur_substitute(
        uniform_state_polynomial(
            H,
            representative,
            denominator_degrees=(2, 3, 2),
        )
    )
    schur_H = divide_one_minus_variable(raw_schur_H, 4)
    one_minus_t3 = add(constant(1), variable(4), -1)
    assert raw_schur_H == multiply(schur_H, one_minus_t3)
    assert max(monomial[4] for monomial in schur_H) == 2

    a0, a1, a2 = (coefficient(schur_H, 4, degree) for degree in range(3))
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
    assert common == (0, 0, 0, 3, 0, 2, 2, 0)
    determinant_residual = divide_monomial(determinant, common)
    determinant_bernstein = bernstein_transform(
        determinant_residual,
        [2, 6, 7],
    )
    assert determinant_bernstein
    assert all(value > 0 for value in determinant_bernstein.values())

    # The full boundary determinant, rather than the x01 discriminant
    # residual, is transported by the two exact graph symmetries.
    states = ("LLR", "LRL", "RRL", "RLR")
    cleared_delta = {
        state: uniform_state_polynomial(
            delta,
            tuple(state),
            denominator_degrees=(2, 2, 2),
        )
        for state in states
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
    page_swap = (0, 1, 2, 5, 6, 3, 4, 7)
    assert cleared_delta["RRL"] == cleared_delta["LLR"]
    assert cleared_delta["LRL"] == permute(cleared_delta["LLR"], page_swap)
    assert cleared_delta["RLR"] == permute(cleared_delta["RRL"], page_swap)

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-c-mixed-gram.v1",
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
        "denominator_clearing": {
            "invariant": "each declared page degree equals the polynomial degree in that page's rational-side activity",
            "A2_page_degrees": [2, 2, 2],
            "H_page_degrees": [2, 3, 2],
        },
        "H_t3_gram": {
            "cleared_factor": "raw_schur_H=(1-t3)*H_tilde",
            "formula": "H_tilde=(1-t3)^2*gamma0+2*t3*(1-t3)*gamma1+t3^2*gamma2",
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
            "raw_schur_H_sha256": digest(raw_schur_H),
            "reduced_schur_H_sha256": digest(schur_H),
            "gamma0_sha256": digest(gamma0),
            "gamma2_sha256": digest(gamma2),
            "determinant_residual_sha256": digest(determinant_residual),
        },
        "representative": "LLR",
        "symmetry_images": {
            "page_exchange": "LRL",
            "hub_exchange": "RRL",
            "both": "RLR",
            "checked_on_exact_cleared_Delta_b": True,
        },
        "certified_chambers": list(states),
        "certified_count": len(states),
        "conclusion": "Delta_b>=0 in all four listed mixed c-negative Schur chambers",
        "scope": "four additional interior c-negative chambers; together with the direct, nonshared, and all-negative Gram certificates this gives 20 of 27, while seven c-negative chambers, negative-page cases, and the global marked-host theorem remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
