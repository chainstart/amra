#!/usr/bin/env python3
"""Exact conditional-copositive certificate for the c<0 PPP chamber."""

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
from verify_negative_c_all_negative_gram import coefficient, scale
from verify_negative_c_direct_chambers import (
    add,
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


B_EDGE = (0, 4)


def product(*factors):
    result = constant(1)
    for factor in factors:
        result = multiply(result, factor)
    return result


def square(poly):
    return multiply(poly, poly)


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

    states = tuple("PPP")
    assert required_denominator_degrees(delta, states) == (2, 2, 2)
    cleared = uniform_state_polynomial(
        delta,
        states,
        denominator_degrees=(2, 2, 2),
    )
    schur = schur_substitute(cleared)
    assert len(cleared) == 628
    assert len(schur) == 1395
    a0, a1, a2 = (coefficient(schur, 7, degree) for degree in range(3))
    beta0 = a0
    beta1 = add(a0, scale(a1, Fraction(1, 2)))
    beta2 = add(add(a0, a1), a2)
    two_beta1 = scale(beta1, 2)

    q0, s0, q3, s3, q4, s4 = (variable(slot) for slot in range(1, 7))
    one = constant(1)
    u = add(one, s0, -1)
    v3 = add(one, s3, -1)
    v4 = add(one, s4, -1)
    d3 = add(s0, s3, -1)
    d4 = add(s0, s4, -1)
    d34 = add(s3, s4, -1)
    B = add(
        product(q0, q3, q4),
        add(add(multiply(q0, q3), multiply(q0, q4)), multiply(q3, q4)),
    )

    A3 = add(product(q0, square(s0), square(v3)), square(d3))
    A4 = add(product(q0, square(s0), square(v4)), square(d4))
    H3 = add(A3, product(q3, square(s3), square(u)))
    H4 = add(A4, product(q4, square(s4), square(u)))
    E3 = multiply(add(one, multiply(q3, square(s3))), H3)
    E4 = multiply(add(one, multiply(q4, square(s4))), H4)
    J3 = add(product(q0, s0, square(v3)), scale(d3, 2))
    J4 = add(product(q0, s0, square(v4)), scale(d4, 2))
    L = add(
        product(q0, square(s0), v3, v4),
        multiply(d3, d4),
    )

    K = add(
        add(
            scale(L, 2),
            product(u, q0, s0, square(d34)),
            -1,
        ),
        add(
            add(
                scale(product(q3, u, square(s3), J4), -1),
                scale(product(q4, u, square(s4), J3), -1),
            ),
            scale(product(q3, q4, square(u), square(s3), square(s4)), 2),
        ),
    )
    assert len(K) == 35

    positive_middle_factor = product(
        power(q0, 4),
        power(q3, 3),
        power(q4, 3),
        s0,
        u,
        add(one, multiply(q3, s3)),
        add(one, multiply(q4, s4)),
        B,
    )
    expected_beta0 = product(
        power(q0, 4),
        power(q3, 2),
        power(q4, 2),
        square(s0),
        square(u),
        add(one, multiply(q3, s3)),
        add(one, product(q3, square(s3))),
        add(one, multiply(q4, s4)),
        add(one, product(q4, square(s4))),
        square(B),
    )
    expected_beta2 = product(
        power(q0, 4),
        power(q3, 4),
        power(q4, 4),
        add(one, multiply(q3, s3)),
        add(one, multiply(q4, s4)),
        H3,
        H4,
    )
    assert beta0 == expected_beta0
    assert two_beta1 == scale(multiply(positive_middle_factor, K), -1)
    assert beta2 == expected_beta2

    determinant = add(multiply(beta0, beta2), square(beta1), -1)
    conditional_residual = add(
        scale(multiply(E3, E4), 4),
        square(K),
        -1,
    )
    assert scale(determinant, 4) == multiply(
        square(positive_middle_factor),
        conditional_residual,
    )

    # Exact polynomial identities behind the analytic upper bound K/2 <=
    # sqrt(E3*E4).  Only Cauchy--Schwarz and the scalar AM--GM inequality
    # remain after these identities are checked.
    cauchy_residual = add(multiply(A3, A4), square(L), -1)
    assert cauchy_residual == product(
        q0,
        square(s0),
        square(u),
        square(d34),
    )
    scalar_records = {}
    for name, q, s, v, A, H, E, J in (
        ("3", q3, s3, v3, A3, H3, E3, J3),
        ("4", q4, s4, v4, A4, H4, E4, J4),
    ):
        j_residual = add(scale(A, 4), square(J), -1)
        expected_j_residual = product(
            q0,
            s0,
            square(v),
            add(scale(s, 4), product(q0, s0, square(v)), -1),
        )
        assert j_residual == expected_j_residual
        expected_E = add(
            add(A, product(q, square(s), add(A, square(u)))),
            product(square(q), power(s, 4), square(u)),
        )
        assert E == expected_E
        assert H == add(A, product(q, square(s), square(u)))
        scalar_records[name] = {
            "A_terms": len(A),
            "H_terms": len(H),
            "E_terms": len(E),
            "J_terms": len(J),
            "j_residual_sha256": digest(j_residual),
        }

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-c-all-positive-copositive.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
            "cleared_PPP_terms": len(cleared),
            "schur_PPP_terms": len(schur),
        },
        "domain": "q0,q3,q4>0, c=-tau*P/B with 0<=tau<=1, and 0<=s0,s3,s4<=1",
        "tau_quadratic": {
            "formula": "F=(1-tau)^2*beta0+2*tau*(1-tau)*beta1+tau^2*beta2",
            "beta0_terms": len(beta0),
            "two_beta1_terms": len(two_beta1),
            "beta2_terms": len(beta2),
            "middle_sign": "2*beta1=-M*K with M>=0",
            "endpoint_certificate": "beta0 and beta2 are displayed products of nonnegative factors; H3 and H4 are sums of three weighted squares",
        },
        "conditional_gram": {
            "K_terms": len(K),
            "determinant_terms": len(determinant),
            "residual_terms": len(conditional_residual),
            "identity": "4*(beta0*beta2-beta1^2)=M^2*(4*E3*E4-K^2)",
            "case_K_nonpositive": "beta1>=0, so all three tau Bernstein coefficients are nonnegative",
            "case_K_positive": "K/2<=sqrt(E3*E4), so the Gram determinant is nonnegative",
        },
        "upper_bound_ledger": {
            "definitions": {
                "Aj": "q0*s0^2*(1-sj)^2+(s0-sj)^2",
                "Hj": "Aj+qj*sj^2*(1-s0)^2",
                "Ej": "(1+qj*sj^2)*Hj",
                "Jj": "q0*s0*(1-sj)^2+2*(s0-sj)",
                "L": "q0*s0^2*(1-s3)*(1-s4)+(s0-s3)*(s0-s4)",
            },
            "K_decomposition": "K/2=L-(1-s0)*q0*s0*(s3-s4)^2/2-q3*(1-s0)*s3^2*J4/2-q4*(1-s0)*s4^2*J3/2+q3*q4*(1-s0)^2*s3^2*s4^2",
            "cauchy_identity": "A3*A4-L^2=q0*s0^2*(1-s0)^2*(s3-s4)^2",
            "scalar_identity": "4*Aj-Jj^2=q0*s0*(1-sj)^2*(4*sj-q0*s0*(1-sj)^2)",
            "endpoint_bound": "-Jj/2<=sqrt(Aj); if Jj<0 the scalar identity has nonnegative right side",
            "energy_bound": "sqrt(Ej)>=sqrt(Aj)+qj*(1-s0)*sj^2 by scalar AM-GM",
            "records": scalar_records,
        },
        "representative": "PPP",
        "certified_chambers": ["PPP"],
        "certified_count": 1,
        "conclusion": "Delta_b>=0 in the all-positive-activity c-negative Schur chamber",
        "combined_conclusion": "all 27 activity chambers are now certified when c is the sole negative diagonal route quantity",
        "records": {
            "cleared_sha256": digest(cleared),
            "schur_sha256": digest(schur),
            "beta0_sha256": digest(beta0),
            "two_beta1_sha256": digest(two_beta1),
            "beta2_sha256": digest(beta2),
            "K_sha256": digest(K),
            "conditional_residual_sha256": digest(conditional_residual),
        },
        "scope": "completes the 27 sole-negative-c interior activity chambers; the three negative-page cases, generic contact classification, global marked-host theorem, and OPG-1757 remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
