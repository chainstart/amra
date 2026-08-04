#!/usr/bin/env python3
"""Exact certificate for all six mixed three-negative chambers (stdlib only)."""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
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
    divide_one_plus_variable,
    multiply,
    permute,
    power,
    scale,
    state_polynomial,
    variable,
)
from verify_opposite_nonshared_chambers import divide_one_minus_variable
from verify_same_side_three_negative import (
    bernstein_entries,
    digest,
    divide_monomial,
    gram_determinant,
)


def divide_polynomial(dividend, divisor):
    """Exact sparse long division by one divisor in lexicographic order."""
    remainder = dict(dividend)
    quotient = {}
    divisor_lead = max(divisor)
    divisor_value = divisor[divisor_lead]
    while remainder:
        lead = max(remainder)
        value = remainder[lead]
        assert all(left >= right for left, right in zip(lead, divisor_lead))
        monomial = tuple(left - right for left, right in zip(lead, divisor_lead))
        quotient_value = value / divisor_value
        quotient[monomial] = quotient.get(monomial, Fraction()) + quotient_value
        for factor_monomial, factor_value in divisor.items():
            target = tuple(a + b for a, b in zip(monomial, factor_monomial))
            remainder[target] = (
                remainder.get(target, Fraction()) - quotient_value * factor_value
            )
            if not remainder[target]:
                del remainder[target]
    return {monomial: value for monomial, value in quotient.items() if value}


def sqrt_fraction(value):
    assert value > 0
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    assert numerator * numerator == value.numerator
    assert denominator * denominator == value.denominator
    return Fraction(numerator, denominator)


def polynomial_square_root(poly):
    """Recover and verify the exact lex-positive square root of a square."""
    lead = max(poly)
    assert all(degree % 2 == 0 for degree in lead)
    root_lead = tuple(degree // 2 for degree in lead)
    root = {root_lead: sqrt_fraction(poly[lead])}
    remainder = add(poly, multiply(root, root), -1)
    while remainder:
        monomial = max(remainder)
        value = remainder[monomial]
        assert all(left >= right for left, right in zip(monomial, root_lead))
        next_monomial = tuple(
            left - right for left, right in zip(monomial, root_lead)
        )
        next_value = value / (2 * root[root_lead])
        next_term = {next_monomial: next_value}
        old_root = dict(root)
        root = add(root, next_term)
        remainder = add(remainder, multiply(old_root, next_term), -2)
        remainder = add(remainder, multiply(next_term, next_term), -1)
    assert multiply(root, root) == poly
    return root


def substitute_slot(poly, slot, replacement):
    result = {}
    for monomial, value in poly.items():
        term = constant(value)
        for index, degree in enumerate(monomial):
            term = multiply(
                term,
                power(replacement if index == slot else variable(index), degree),
            )
        result = add(result, term)
    return result


def restrict_slot_zero(poly, slot):
    return {
        monomial: value
        for monomial, value in poly.items()
        if monomial[slot] == 0
    }


def positive_square_residual(poly, monomial_factor, one_plus_slots, square):
    quotient = divide_monomial(poly, monomial_factor)
    for slot in one_plus_slots:
        quotient = divide_one_plus_variable(quotient, slot)
    residual = add(quotient, square, -1)
    assert all(value > 0 for value in residual.values())
    return quotient, residual


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

    # Slots are (c,q0,t0,q3,t3,q4,t4).  Representatives LLR and LRR share
    # the same core outer Gram determinant.
    cleared = {
        state: state_polynomial(delta, tuple(state))
        for state in ("LLR", "LRR")
    }
    quotients = {}
    for state, poly in cleared.items():
        quotient = divide_one_minus_variable(
            divide_one_minus_variable(poly, 4), 6
        )
        rebuilt = multiply(
            multiply(quotient, add(constant(1), variable(4), -1)),
            add(constant(1), variable(6), -1),
        )
        assert rebuilt == poly
        assert [max(m[slot] for m in quotient) for slot in (2, 4, 6)] == [4, 2, 2]
        quotients[state] = quotient

    # LLR endpoint entries: two nested t4 quadratic Gram certificates.  Two
    # mixed endpoint polynomials are an explicit square plus a
    # positive-coefficient residual.
    llr_t3_entries = bernstein_entries(quotients["LLR"], 4, 2)
    llr_endpoint_certificates = []
    endpoint_square_records = {}
    for label, endpoint, expected_counts, expected_determinant_terms in (
        ("f0", llr_t3_entries[0], (27, 33, 42), 224),
        ("f2", llr_t3_entries[2], (42, 53, 67), 543),
    ):
        entries = bernstein_entries(endpoint, 6, 2)
        endpoint_determinant = gram_determinant(entries)
        assert tuple(len(poly) for poly in entries) == expected_counts
        assert all(value > 0 for value in entries[0].values())
        assert len(endpoint_determinant) == expected_determinant_terms
        assert all(value > 0 for value in endpoint_determinant.values())
        if label == "f0":
            square = multiply(
                multiply(power(variable(0), 2), power(variable(3), 2)),
                power(add(constant(1), variable(2), -1), 2),
            )
            quotient, residual = positive_square_residual(
                entries[2], {2: 2}, (5,), square
            )
            assert (len(quotient), len(residual)) == (24, 21)
        else:
            square = multiply(
                multiply(
                    multiply(power(variable(0), 2), variable(3)),
                    power(variable(2), 2),
                ),
                power(add(constant(1), variable(2), -1), 2),
            )
            quotient, residual = positive_square_residual(
                entries[2], {}, (5, 3), square
            )
            assert (len(quotient), len(residual)) == (21, 18)
        endpoint_square_records[f"LLR_{label}_t4_beta2_quotient"] = quotient
        endpoint_square_records[f"LLR_{label}_t4_beta2_positive_residual"] = residual
        llr_endpoint_certificates.append((entries, endpoint_determinant))

    # The outer determinants for LLR and LRR are exactly identical.
    outer_determinants = {
        state: gram_determinant(bernstein_entries(quotient, 4, 2))
        for state, quotient in quotients.items()
    }
    assert outer_determinants["LLR"] == outer_determinants["LRR"]
    outer_residual = divide_monomial(outer_determinants["LLR"], {2: 2})
    q0_plus_t0 = add(variable(1), variable(2))
    H = divide_polynomial(
        divide_polynomial(outer_residual, q0_plus_t0), q0_plus_t0
    )
    assert len(H) == 729

    # H is quadratic in q0.  Its discriminant is minus a manifestly
    # nonnegative product times the square of a 28-term polynomial.
    H_q0_entries = tuple(coefficient(H, 1, degree) for degree in range(3))
    H_q0_discriminant = add(
        multiply(H_q0_entries[1], H_q0_entries[1]),
        multiply(H_q0_entries[0], H_q0_entries[2]),
        -4,
    )
    square_residual = scale(H_q0_discriminant, Fraction(-1, 4))
    square_residual = divide_monomial(square_residual, {0: 2, 6: 2})
    q4_plus_t4 = add(variable(5), variable(6))
    square_residual = divide_polynomial(square_residual, q4_plus_t4)
    square_residual = divide_polynomial(square_residual, q4_plus_t4)
    square_residual = divide_one_minus_variable(square_residual, 2)
    square_residual = divide_one_minus_variable(square_residual, 2)
    square_residual = divide_one_plus_variable(square_residual, 3)
    route_minor = add(
        add(
            multiply(multiply(variable(0), variable(3)), variable(5)),
            multiply(variable(0), variable(3)),
        ),
        add(multiply(variable(0), variable(5)), multiply(variable(3), variable(5))),
    )
    square_residual = divide_polynomial(square_residual, route_minor)
    square_root = polynomial_square_root(square_residual)
    assert (len(square_residual), len(square_root)) == (229, 28)
    assert sum(value < 0 for value in square_root.values()) == 8

    # To determine the sign of H, evaluate it at the convenient real point
    # q0=-t0.  The result is c^2*t4^2*(1-t0)^2*J.
    H_at_minus_t0 = substitute_slot(H, 1, scale(variable(2), -1))
    J = divide_monomial(H_at_minus_t0, {0: 2, 6: 2})
    J = divide_one_minus_variable(divide_one_minus_variable(J, 2), 2)
    assert len(J) == 73

    # J=C2*c^2+C1*c+C0.  C0 is coefficientwise positive and C2 is a
    # positive route sum times an exact square.
    J_c_entries = tuple(coefficient(J, 0, degree) for degree in range(3))
    assert tuple(len(poly) for poly in J_c_entries) == (7, 23, 43)
    assert all(value > 0 for value in J_c_entries[0].values())
    q3, q4, t0, t4 = (variable(slot) for slot in (3, 5, 2, 6))
    route_sum = add(add(multiply(q3, q4), q3), q4)
    signed_linear = add(
        add(
            add(multiply(multiply(q3, q4), t0), multiply(q3, q4), -1),
            multiply(q3, t4),
            -1,
        ),
        add(add(multiply(q3, t0), multiply(q4, t0)), multiply(t4, t0)),
    )
    assert J_c_entries[2] == multiply(route_sum, power(signed_linear, 2))

    # If C1<0, an exact implication certificate forces the c-discriminant
    # to be negative.  Write C1=q3*t0*L and disc_c as a positive factor R.
    J_c_discriminant = add(
        multiply(J_c_entries[1], J_c_entries[1]),
        multiply(J_c_entries[0], J_c_entries[2]),
        -4,
    )
    L = divide_monomial(J_c_entries[1], {2: 1, 3: 1})
    R = divide_monomial(J_c_discriminant, {2: 2, 3: 4, 6: 2})
    R = divide_one_plus_variable(divide_one_plus_variable(R, 5), 5)
    R = divide_one_plus_variable(R, 3)
    assert (len(L), len(R)) == (23, 16)

    route_total = add(add(multiply(q3, q4), q3), add(q4, t4))
    B = add(multiply(t0, route_total), multiply(q3, add(q4, t4)), -1)
    A = add(B, multiply(q3, add(q4, t4)), -1)
    implication_identity = add(
        add(multiply(t0, L), multiply(q3, R), -1),
        multiply(multiply(q4, A), B),
        -2,
    )
    assert not implication_identity

    # Introduce z in the otherwise unused t3 slot.  If A*B<0 then
    # 0<B<q3*(q4+t4), so z=B is positive.  The following 28-term identity
    # makes route_total*L strictly positive, contradicting L<0.
    z = variable(4)
    L0, L1 = coefficient(L, 2, 0), coefficient(L, 2, 1)
    positive_implication_poly = add(
        multiply(route_total, L0),
        multiply(add(z, multiply(q3, add(q4, t4))), L1),
    )
    assert len(positive_implication_poly) == 28
    assert all(value > 0 for value in positive_implication_poly.values())
    assert substitute_slot(positive_implication_poly, 4, B) == multiply(route_total, L)

    # For LRR, the t3=0 endpoint is exactly the x23=0 specialization of the
    # already certified LPR chamber after its (1-t4) factor is removed.
    lrr_t3_entries = bernstein_entries(quotients["LRR"], 4, 2)
    lpr_cleared = state_polynomial(delta, tuple("LPR"))
    lpr_x23_zero = restrict_slot_zero(lpr_cleared, 4)
    lpr_boundary_quotient = divide_one_minus_variable(lpr_x23_zero, 6)
    assert lrr_t3_entries[0] == lpr_boundary_quotient

    # Exact graph symmetries transport the representatives to all six mixed
    # three-negative chambers.
    all_cleared = {
        state: state_polynomial(delta, tuple(state))
        for state in ("LLR", "LRL", "RRL", "RLR", "LRR", "RLL")
    }
    page_swap = (0, 1, 2, 5, 6, 3, 4)
    assert all_cleared["LRL"] == permute(all_cleared["LLR"], page_swap)
    assert all_cleared["RRL"] == all_cleared["LLR"]
    assert all_cleared["RLR"] == permute(all_cleared["RRL"], page_swap)
    assert all_cleared["RLL"] == all_cleared["LRR"]

    records = {
        "LLR_cleared": cleared["LLR"],
        "LRR_cleared": cleared["LRR"],
        "LLR_quotient": quotients["LLR"],
        "LRR_quotient": quotients["LRR"],
        "common_outer_gram_determinant": outer_determinants["LLR"],
        "common_outer_gram_residual_H": H,
        "H_q0_discriminant": H_q0_discriminant,
        "H_q0_discriminant_square": square_residual,
        "H_q0_discriminant_square_root": square_root,
        "H_at_q0_minus_t0_residual_J": J,
        "J_c_discriminant_factor_R": R,
        "J_c_linear_factor_L": L,
        "positive_implication_polynomial": positive_implication_poly,
        **endpoint_square_records,
    }
    print(json.dumps({
        "schema": "amra.opg1757.round7.mixed-three-negative.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "representatives": {
            "LLR": {
                "Q_terms": len(quotients["LLR"]),
                "endpoint_t4_bernstein_term_counts": [
                    [len(poly) for poly in certificate[0]]
                    for certificate in llr_endpoint_certificates
                ],
                "endpoint_t4_gram_determinant_terms": [
                    len(certificate[1]) for certificate in llr_endpoint_certificates
                ],
                "mixed_endpoint_positive_residual_terms": [21, 18],
            },
            "LRR": {
                "Q_terms": len(quotients["LRR"]),
                "certified_t3_zero_dependency": "exact x23=0 specialization of the LPR theorem in NESTED_SHARED_DISCRIMINANT.md",
            },
        },
        "common_outer_determinant": {
            "exactly_identical_for_LLR_and_LRR": True,
            "factorization": "t0^2*(q0+t0)^2*H",
            "H_terms": len(H),
            "H_q0_quadratic_term_counts": [len(poly) for poly in H_q0_entries],
            "H_q0_discriminant": "-4*c^2*t4^2*(q4+t4)^2*(1-t0)^2*(q3+1)*(c*q3*q4+c*q3+c*q4+q3*q4)*K^2",
            "K_terms": len(square_root),
            "H_test_value": "H(-t0)=c^2*t4^2*(1-t0)^2*J",
            "J_terms": len(J),
            "J_c_quadratic_term_counts": [len(poly) for poly in J_c_entries],
            "J_c_leading_coefficient": "(q3*q4+q3+q4)*signed_linear^2",
            "J_c_discriminant_factor_terms": len(R),
            "sign_implication": "C1<0 implies R<0 via t0*L-q3*R=2*q4*A*B and a 28-term positive substitution identity",
        },
        "certified_chambers_added": ["LLR", "LRL", "LRR", "RLL", "RLR", "RRL"],
        "combined_nonnegative_route_coverage": "27 of 27 chambers",
        "symmetry_checks": {
            "page_exchange": ["LLR -> LRL", "RRL -> RLR"],
            "hub_exchange": ["LLR -> RRL", "LRR -> RLL"],
            "checked_on_exact_cleared_polynomials": True,
        },
        "records": {
            name: {"terms": len(poly), "sha256": digest(poly)}
            for name, poly in records.items()
        },
        "scope": "complete nonnegative-effective-route sign theorem; four negative-effective-route matrix chambers, generic contact classification, the full marked-host theorem, and OPG-1757 remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
