#!/usr/bin/env python3
"""Exact shared-coordinate Gram certificates for four more c<0 chambers."""

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
    digest,
    multiply,
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


def coefficient(poly, slot, degree):
    result = {}
    for monomial, value in poly.items():
        if monomial[slot] != degree:
            continue
        reduced = list(monomial)
        reduced[slot] = 0
        result[tuple(reduced)] = value
    return result


def divide_monomial(poly, factor):
    result = {}
    for monomial, value in poly.items():
        reduced = tuple(degree - removed for degree, removed in zip(monomial, factor))
        assert all(degree >= 0 for degree in reduced)
        result[reduced] = value
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

    # The hub exchange preserves Delta and swaps L/R in every page.  It will
    # transfer PPR -> PPL and PRP -> PLP after the two representatives below.
    hub_swap = {
        X01: X02,
        X02: X01,
        X13: X23,
        X23: X13,
        X14: X24,
        X24: X14,
    }
    assert delta == permute_edges(delta, hub_swap)

    expected_gcd = {
        "PPR": (0, 4, 0, 7, 0, 3, 2, 2),
        "PRP": (0, 4, 0, 3, 2, 7, 0, 2),
    }
    H_denominator_degrees = {
        "PPR": (2, 3, 2),
        "PRP": (2, 2, 3),
    }
    records = {}
    for state in ("PPR", "PRP"):
        states = tuple(state)
        assert required_denominator_degrees(A2, states) == (2, 2, 2)
        assert required_denominator_degrees(H, states) == H_denominator_degrees[state]
        schur_A2 = schur_substitute(
            uniform_state_polynomial(
                A2,
                states,
                denominator_degrees=(2, 2, 2),
            )
        )
        A2_bernstein = bernstein_transform(schur_A2, [2, 4, 6, 7])
        assert A2_bernstein
        assert all(value > 0 for value in A2_bernstein.values())

        schur_H = schur_substitute(
            uniform_state_polynomial(
                H,
                states,
                denominator_degrees=H_denominator_degrees[state],
            )
        )
        assert max(monomial[2] for monomial in schur_H) == 2
        a0, a1, a2 = (coefficient(schur_H, 2, degree) for degree in range(3))
        beta0 = a0
        beta1 = add(a0, {monomial: value / 2 for monomial, value in a1.items()})
        beta2 = add(add(a0, a1), a2)
        beta0_bernstein = bernstein_transform(beta0, [4, 6, 7])
        beta2_bernstein = bernstein_transform(beta2, [4, 6, 7])
        assert all(value > 0 for value in beta0_bernstein.values())
        assert all(value > 0 for value in beta2_bernstein.values())

        determinant = add(
            multiply(beta0, beta2),
            multiply(beta1, beta1),
            -1,
        )
        common = tuple(min(monomial[slot] for monomial in determinant) for slot in range(8))
        assert common == expected_gcd[state]
        determinant_residual = divide_monomial(determinant, common)
        determinant_bernstein = bernstein_transform(determinant_residual, [4, 6, 7])
        assert determinant_bernstein
        assert all(value > 0 for value in determinant_bernstein.values())

        records[state] = {
            "A2_bernstein_nonzero": len(A2_bernstein),
            "A2_minimum_bernstein_coefficient": str(min(A2_bernstein.values())),
            "H_beta0_bernstein_nonzero": len(beta0_bernstein),
            "H_beta0_minimum_bernstein_coefficient": str(min(beta0_bernstein.values())),
            "H_beta2_bernstein_nonzero": len(beta2_bernstein),
            "H_beta2_minimum_bernstein_coefficient": str(min(beta2_bernstein.values())),
            "H_gram_determinant_terms": len(determinant_residual),
            "H_gram_determinant_bernstein_nonzero": len(determinant_bernstein),
            "H_gram_determinant_minimum_bernstein_coefficient": str(
                min(determinant_bernstein.values())
            ),
            "H_gram_determinant_common_monomial": list(common),
            "schur_A2_sha256": digest(schur_A2),
            "schur_H_sha256": digest(schur_H),
            "H_gram_determinant_residual_sha256": digest(determinant_residual),
        }

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-c-nonshared-gram.v1",
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
            "strategy": "prove A2>=0 and H>=0 after the exact Schur and uniform-page substitutions",
        },
        "H_s0_gram": {
            "formula": "H=(1-s0)^2*beta0+2*s0*(1-s0)*beta1+s0^2*beta2",
            "certificate": "beta0,beta2 and beta0*beta2-beta1^2 have strictly positive tensor Bernstein coefficients in the other page orientations and tau",
        },
        "denominator_clearing": {
            "invariant": "each declared page degree is at least the polynomial degree in that page's rational-side activity",
            "A2_page_degrees": [2, 2, 2],
            "H_page_degrees": {
                state: list(H_denominator_degrees[state])
                for state in ("PPR", "PRP")
            },
        },
        "representatives": ["PPR", "PRP"],
        "hub_images": {"PPR": "PPL", "PRP": "PLP"},
        "certified_chambers": ["PLP", "PPL", "PPR", "PRP"],
        "certified_count": 4,
        "records": records,
        "conclusion": "Delta_b>=0 in all four listed c-negative Schur chambers",
        "scope": "four additional interior c-negative chambers; together with NEGATIVE_C_DIRECT_CHAMBERS.md this gives 14 of 27, while thirteen c-negative chambers, negative-page cases, and the global marked-host theorem remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
