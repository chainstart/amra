#!/usr/bin/env python3
"""Exact Gram certificates for six shared-negative-page chambers."""

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
from verify_negative_c_direct_chambers import (
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_page_direct_chambers import (
    B_EDGE,
    chart_polynomial,
    digest,
    schur_substitute,
)


SLOTS = {"c": 0, "s0": 2, "q3": 3, "s3": 4, "q4": 5, "s4": 6}
TAU = 7


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in poly.items()
        if scalar * coefficient
    }


def coefficient(poly, slot, degree):
    result = {}
    for monomial, value in poly.items():
        if monomial[slot] != degree:
            continue
        reduced = list(monomial)
        reduced[slot] = 0
        result[tuple(reduced)] = value
    return result


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


def common_monomial(poly):
    return tuple(min(monomial[slot] for monomial in poly) for slot in range(8))


def divide_monomial(poly, factor):
    result = {}
    for monomial, value in poly.items():
        reduced = tuple(degree - removed for degree, removed in zip(monomial, factor))
        assert all(degree >= 0 for degree in reduced)
        result[reduced] = value
    return result


def positive_bernstein(poly, slots):
    transformed = bernstein_transform(poly, slots)
    assert transformed
    assert all(value > 0 for value in transformed.values())
    return transformed


def quadratic_certificate(poly, slot, other_bounded_slots):
    gamma0, _, gamma2, determinant = gram(poly, slot)
    beta0 = positive_bernstein(gamma0, other_bounded_slots)
    beta2 = positive_bernstein(gamma2, other_bounded_slots)
    common = common_monomial(determinant)
    residual = divide_monomial(determinant, common)
    determinant_bernstein = positive_bernstein(residual, other_bounded_slots)
    return {
        "terms": len(poly),
        "slot": slot,
        "endpoint_bernstein_nonzero": [len(beta0), len(beta2)],
        "endpoint_minimum": [str(min(beta0.values())), str(min(beta2.values()))],
        "determinant_terms": len(determinant),
        "determinant_common_monomial": list(common),
        "determinant_residual_terms": len(residual),
        "determinant_bernstein_nonzero": len(determinant_bernstein),
        "determinant_minimum": str(min(determinant_bernstein.values())),
        "sha256": digest(poly),
    }


def sparse(rows):
    result = {}
    for value, degrees in rows:
        monomial = [0] * 8
        for name, degree in degrees.items():
            monomial[SLOTS[name]] = degree
        monomial = tuple(monomial)
        result[monomial] = result.get(monomial, Fraction()) + Fraction(value)
    return {monomial: value for monomial, value in result.items() if value}


def negative_right_endpoint_core():
    """The 22-term endpoint factor for a right-negative q4 page."""
    c, s0, q3, q4, s4 = (variable(SLOTS[name]) for name in ("c", "s0", "q3", "q4", "s4"))
    one_minus_s0 = add(constant(1), s0, -1)
    g0 = sparse([
        (1, {"c": 2, "q3": 2, "q4": 1, "s4": 2}),
        (1, {"c": 2, "q3": 2, "s4": 2}),
    ])
    g1 = sparse([
        (1, {"c": 2, "q3": 2, "q4": 1, "s4": 2}),
        (-1, {"c": 2, "q3": 2, "q4": 1, "s4": 1}),
        (1, {"c": 2, "q3": 2, "s4": 2}),
        (-1, {"c": 2, "q3": 2, "s4": 1}),
        (1, {"c": 2, "q3": 1, "q4": 1, "s4": 2}),
        (-1, {"c": 2, "q3": 1, "q4": 1, "s4": 1}),
        (1, {"c": 1, "q3": 2, "q4": 1, "s4": 2}),
        (-1, {"c": 1, "q3": 2, "q4": 1, "s4": 1}),
    ])
    g2 = sparse([
        (1, {"c": 2, "q3": 2, "q4": 1, "s4": 2}),
        (-2, {"c": 2, "q3": 2, "q4": 1, "s4": 1}),
        (1, {"c": 2, "q3": 2, "q4": 1}),
        (1, {"c": 2, "q3": 2, "s4": 2}),
        (-2, {"c": 2, "q3": 2, "s4": 1}),
        (1, {"c": 2, "q3": 2}),
        (1, {"c": 2, "q3": 1, "q4": 2}),
        (2, {"c": 2, "q3": 1, "q4": 1, "s4": 2}),
        (-2, {"c": 2, "q3": 1, "q4": 1, "s4": 1}),
        (2, {"c": 2, "q3": 1, "q4": 1}),
        (1, {"c": 2, "q3": 1, "s4": 2}),
        (1, {"c": 2, "q4": 2}),
        (1, {"c": 2, "q4": 1, "s4": 2}),
        (1, {"c": 1, "q3": 2, "q4": 2}),
        (2, {"c": 1, "q3": 2, "q4": 1, "s4": 2}),
        (-2, {"c": 1, "q3": 2, "q4": 1, "s4": 1}),
        (2, {"c": 1, "q3": 2, "q4": 1}),
        (1, {"c": 1, "q3": 2, "s4": 2}),
        (2, {"c": 1, "q3": 1, "q4": 2}),
        (2, {"c": 1, "q3": 1, "q4": 1, "s4": 2}),
        (1, {"q3": 2, "q4": 2}),
        (1, {"q3": 2, "q4": 1, "s4": 2}),
    ])
    return add(
        add(
            multiply(power(one_minus_s0, 2), g0),
            scale(multiply(multiply(s0, one_minus_s0), g1), 2),
        ),
        multiply(power(s0, 2), g2),
    )


def permute_pages(poly):
    result = {}
    for monomial, value in poly.items():
        transformed = list(monomial)
        transformed[3], transformed[5] = monomial[5], monomial[3]
        transformed[4], transformed[6] = monomial[6], monomial[4]
        transformed = tuple(transformed)
        result[transformed] = result.get(transformed, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def positive_route_determinant():
    c, q3, q4 = (variable(SLOTS[name]) for name in ("c", "q3", "q4"))
    return add(
        add(multiply(multiply(c, q3), q4), multiply(c, q3)),
        add(multiply(c, q4), multiply(q3, q4)),
    )


def build_delta():
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
    return delta, forest_count, connected_count


def state_schur(delta, state):
    states = tuple(state)
    cleared = chart_polynomial(delta, states, 0)
    schur, a_degree = schur_substitute(cleared, states, 0)
    assert a_degree == 2
    return schur


def endpoint_certificates(beta0, beta2, state):
    s0, s3, s4 = (variable(SLOTS[name]) for name in ("s0", "s3", "s4"))
    one_minus_s3 = add(constant(1), s3, -1)
    one_minus_s4 = add(constant(1), s4, -1)
    B = positive_route_determinant()

    beta0_common = (0, 0, 2, 0, 0, 0, 0, 0)
    beta0_quotient = divide_monomial(beta0, beta0_common)
    beta0_factor = multiply(
        multiply(one_minus_s3, one_minus_s4),
        power(B, 2),
    )
    beta0_core = divide_polynomial(beta0_quotient, beta0_factor)
    assert beta0 == multiply(
        {beta0_common: Fraction(1)},
        multiply(beta0_factor, beta0_core),
    )
    if state == "LLR":
        assert len(beta0_core) == 66
        beta0_record = quadratic_certificate(beta0_core, 6, [2, 4])
    else:
        assert state == "LRR" and len(beta0_core) == 57
        beta0_record = quadratic_certificate(beta0_core, 2, [4, 6])

    beta2_factor = multiply(one_minus_s3, one_minus_s4)
    beta2_quotient = divide_polynomial(beta2, beta2_factor)
    right_q4 = negative_right_endpoint_core()
    assert len(right_q4) == 22
    right_q4_record = quadratic_certificate(right_q4, 2, [6])
    other_core = divide_polynomial(beta2_quotient, right_q4)
    assert beta2 == multiply(beta2_factor, multiply(other_core, right_q4))
    if state == "LLR":
        assert len(other_core) == 28
        other_bernstein = positive_bernstein(other_core, [2, 4])
        other_record = {
            "terms": len(other_core),
            "bernstein_nonzero": len(other_bernstein),
            "minimum": str(min(other_bernstein.values())),
            "sha256": digest(other_core),
        }
    else:
        assert state == "LRR" and len(other_core) == 22
        assert other_core == permute_pages(right_q4)
        other_record = quadratic_certificate(other_core, 2, [4])
    return {
        "beta0_terms": len(beta0),
        "beta0_core": beta0_record,
        "beta2_terms": len(beta2),
        "beta2_other_core": other_record,
        "beta2_right_q4_core": right_q4_record,
    }


def outer_determinant_core(determinant, state):
    s0, q3, s3, q4, s4 = (
        variable(SLOTS[name]) for name in ("s0", "q3", "s3", "q4", "s4")
    )
    one_minus_s0 = add(constant(1), s0, -1)
    one_minus_s3 = add(constant(1), s3, -1)
    one_minus_s4 = add(constant(1), s4, -1)
    B = positive_route_determinant()
    if state == "LLR":
        common = (4, 0, 2, 2, 2, 2, 0, 0)
        factors = (
            one_minus_s0,
            one_minus_s3,
            add(q4, s4),
            one_minus_s4,
            B,
        )
    else:
        assert state == "LRR"
        common = (4, 0, 2, 2, 0, 2, 0, 0)
        factors = (
            one_minus_s0,
            add(q3, s3),
            one_minus_s3,
            add(q4, s4),
            one_minus_s4,
            B,
        )
    quotient = divide_monomial(determinant, common)
    positive_factor = constant(1)
    for factor in factors:
        positive_factor = multiply(positive_factor, power(factor, 2))
    core = divide_polynomial(quotient, positive_factor)
    assert determinant == multiply(
        {common: Fraction(1)},
        multiply(positive_factor, core),
    )
    return core, common


def conditional_core_certificate(core):
    c, s0, q3, s3, q4, s4 = (
        variable(SLOTS[name])
        for name in ("c", "s0", "q3", "s3", "q4", "s4")
    )
    one = constant(1)
    one_minus_s0 = add(one, s0, -1)
    Q = add(add(multiply(q3, q4), q3), q4)
    L = add(multiply(s0, add(s3, s4)), multiply(s3, s4), -1)
    T = add(
        add(multiply(q3, power(s4, 2)), multiply(q4, power(s3, 2))),
        multiply(power(s3, 2), power(s4, 2)),
    )
    W = add(add(s3, s4), multiply(s3, s4), -1)
    q3q4 = multiply(q3, q4)
    F9_square = power(add(multiply(q3, s4), multiply(q4, s3), -1), 2)
    F9_residual = add(
        add(
            multiply(multiply(power(q3, 2), q4), power(s4, 2)),
            multiply(multiply(q3, power(q4, 2)), power(s3, 2)),
        ),
        add(
            add(
                scale(multiply(multiply(q3q4, power(s3, 2)), s4), 2),
                scale(multiply(multiply(q3q4, s3), power(s4, 2)), 2),
            ),
            multiply(add(q3, q4), multiply(power(s3, 2), power(s4, 2))),
        ),
    )
    assert all(value > 0 for value in F9_residual.values())
    F9_sos = add(F9_square, F9_residual)
    F9_compact = add(multiply(Q, T), multiply(q3q4, power(W, 2)), -1)
    assert F9_sos == F9_compact
    F9 = F9_sos
    middle = add(
        multiply(power(s0, 2), F9),
        scale(multiply(multiply(multiply(q3q4, s0), W), L), 2),
    )
    F13 = add(
        multiply(power(s0, 2), F9),
        scale(
            multiply(
                multiply(multiply(multiply(q3q4, s3), s4), one_minus_s0),
                L,
            ),
            4,
        ),
    )
    leading = multiply(Q, power(L, 2))
    trailing = multiply(
        multiply(multiply(q3q4, power(s0, 2)), T),
        constant(1),
    )
    expected = add(
        add(multiply(leading, power(c, 2)), multiply(middle, c)),
        trailing,
    )
    assert core == expected
    discriminant = add(
        multiply(middle, middle),
        scale(multiply(leading, trailing), -4),
    )
    assert discriminant == multiply(
        multiply(power(s0, 2), F13),
        F9,
    )
    bracket = add(
        scale(multiply(s0, W), -1),
        scale(multiply(multiply(s3, s4), one_minus_s0), 2),
    )
    assert bracket == add(
        multiply(multiply(s3, s4), one_minus_s0),
        L,
        -1,
    )
    return {
        "terms": len(core),
        "formula": "H=Q*L^2*c^2+(s0^2*F9+2*q3*q4*s0*W*L)*c+q3*q4*s0^2*T",
        "F9_terms": len(F9),
        "F9_sos": "(q3*s4-q4*s3)^2 plus five nonnegative monomials",
        "discriminant": "middle^2-4*leading*trailing=s0^2*F13*F9",
        "F13": "s0^2*F9+4*q3*q4*s3*s4*(1-s0)*L",
        "conditional_step": "middle<0 forces L<0; then s0*W=s3*s4*(1-s0)+L makes F13<0",
        "sha256": digest(core),
    }


def main():
    delta, forest_count, connected_count = build_delta()
    representatives = {state: state_schur(delta, state) for state in ("LLR", "LRR")}
    all_states = {state: state_schur(delta, state) for state in ("LLR", "LRL", "LRR", "RLL", "RLR", "RRL")}
    assert all_states["RRL"] == representatives["LLR"]
    assert all_states["RLL"] == representatives["LRR"]
    assert all_states["LRL"] == permute_pages(representatives["LLR"])
    assert all_states["RLR"] == all_states["LRL"]

    records = {}
    for state, schur in representatives.items():
        beta0, _, beta2, determinant = gram(schur, TAU)
        endpoints = endpoint_certificates(beta0, beta2, state)
        core, common = outer_determinant_core(determinant, state)
        if state == "LLR":
            assert len(core) == 94
            core_record = {
                "kind": "nested_unit_interval_gram",
                **quadratic_certificate(core, 6, [2, 4]),
            }
        else:
            assert len(core) == 33
            core_record = {
                "kind": "conditional_nonnegative_c_quadratic",
                **conditional_core_certificate(core),
            }
        records[state] = {
            "schur_terms": len(schur),
            "outer_gram_terms": len(determinant),
            "outer_common_monomial": list(common),
            "endpoints": endpoints,
            "outer_core": core_record,
            "schur_sha256": digest(schur),
        }

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-q0-no-positive-gram.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "domain": "q0<0, q3>0, q4>0, c>0, K>0; the q0 page has one negative activity and neither other page is in its nonnegative-activity P chart",
        "representatives": ["LLR", "LRR"],
        "symmetry_closure": {
            "LLR": ["LLR", "LRL", "RLR", "RRL"],
            "LRR": ["LRR", "RLL"],
        },
        "certified_chambers": ["LLR", "LRL", "LRR", "RLL", "RLR", "RRL"],
        "certified_count": 6,
        "records": records,
        "conclusion": "Delta_b>=0 in all six listed shared-negative-page chambers",
        "scope": "six additional q0-negative activity chambers; eleven q0-negative and all unresolved q3/q4-negative orientations remain open, so the generic sign and OPG-1757 are not claimed",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
