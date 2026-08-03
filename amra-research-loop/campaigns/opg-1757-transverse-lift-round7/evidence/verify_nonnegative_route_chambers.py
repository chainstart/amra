#!/usr/bin/env python3
"""Exact certificates for 11 nonnegative-effective-route sign chambers."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb
import json

from verify_c_zero_fibre import (
    EDGES,
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)


B_EDGE = (0, 4)
C_EDGE = (1, 2)
ROUTES = (((0, 1), (0, 2)), ((1, 3), (2, 3)), ((1, 4), (2, 4)))
COUNT = 7
ZERO = (0,) * COUNT


def add(left, right, scale=1):
    scale = Fraction(scale)
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction()) + scale * coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def multiply(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            result[monomial] = (
                result.get(monomial, Fraction()) + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items() if scalar}


def constant(value):
    value = Fraction(value)
    return {} if not value else {ZERO: value}


def variable(slot, coefficient=1):
    monomial = [0] * COUNT
    monomial[slot] = 1
    return {tuple(monomial): Fraction(coefficient)}


def power(poly, exponent):
    result = constant(1)
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def state_polynomial(delta, states):
    """Clear a square denominator for each negative edge activity."""
    cvar = variable(0)
    route_factors = []
    for index, state in enumerate(states):
        first = variable(1 + 2 * index)
        second = variable(2 + 2 * index)
        if state == "P":
            route_factors.append((first, second, None))
            continue
        q, t = first, second
        one_minus_t = add(constant(1), t, -1)
        q_plus_t = add(q, t)
        negative = scale(t, -1)
        if state == "L":
            route_factors.append((negative, q_plus_t, one_minus_t))
        else:
            route_factors.append((q_plus_t, negative, one_minus_t))

    result = {}
    for original_monomial, original_coefficient in delta.items():
        term = constant(original_coefficient)
        term = multiply(term, power(cvar, original_monomial[EDGES.index(C_EDGE)]))
        for state, edges, factors in zip(states, ROUTES, route_factors):
            left_degree = original_monomial[EDGES.index(edges[0])]
            right_degree = original_monomial[EDGES.index(edges[1])]
            left, right, denominator = factors
            term = multiply(term, power(left, left_degree))
            term = multiply(term, power(right, right_degree))
            if state != "P":
                positive_degree = right_degree if state == "L" else left_degree
                term = multiply(term, power(denominator, 2 - positive_degree))
        result = add(result, term)
    return result


def bernstein_transform(poly, states):
    result = dict(poly)
    for index, state in enumerate(states):
        if state == "P":
            continue
        slot = 2 + 2 * index
        degree = max(monomial[slot] for monomial in result)
        grouped = {}
        for monomial, coefficient in result.items():
            key = monomial[:slot] + monomial[slot + 1 :]
            grouped.setdefault(key, {})[monomial[slot]] = coefficient
        transformed = {}
        for key, coefficients in grouped.items():
            for bernstein_index in range(degree + 1):
                value = sum(
                    coefficients.get(power_degree, 0)
                    * Fraction(comb(bernstein_index, power_degree), comb(degree, power_degree))
                    for power_degree in range(bernstein_index + 1)
                )
                if value:
                    monomial = key[:slot] + (bernstein_index,) + key[slot:]
                    transformed[monomial] = value
        result = transformed
    return result


def coefficient(poly, slot, degree):
    result = {}
    for monomial, value in poly.items():
        if monomial[slot] != degree:
            continue
        reduced = list(monomial)
        reduced[slot] = 0
        result[tuple(reduced)] = value
    return result


def divide_one_plus_variable(poly, slot):
    grouped = {}
    for monomial, value in poly.items():
        key = monomial[:slot] + monomial[slot + 1 :]
        grouped.setdefault(key, {})[monomial[slot]] = value
    quotient = {}
    for key, coefficients in grouped.items():
        degree = max(coefficients)
        previous = Fraction()
        for exponent in range(degree):
            value = coefficients.get(exponent, Fraction()) - previous
            if value:
                monomial = key[:slot] + (exponent,) + key[slot:]
                quotient[monomial] = value
            previous = value
        assert coefficients.get(degree, Fraction()) == previous
    return quotient


def divide_monomial(poly, degrees):
    result = {}
    for monomial, coefficient in poly.items():
        reduced = list(monomial)
        for slot, degree in degrees.items():
            assert reduced[slot] >= degree
            reduced[slot] -= degree
        result[tuple(reduced)] = coefficient
    return result


def permute(poly, old_to_new):
    result = {}
    for monomial, coefficient in poly.items():
        transformed = [0] * COUNT
        for old, degree in enumerate(monomial):
            transformed[old_to_new[old]] = degree
        result[tuple(transformed)] = coefficient
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

    direct_states = ("PPP", "PLL", "PRR", "LPL", "LLP", "RPR", "RRP")
    polynomials = {
        state: state_polynomial(delta, tuple(state))
        for state in direct_states
    }
    direct_records = {}
    for state, poly in polynomials.items():
        transformed = bernstein_transform(poly, tuple(state))
        assert all(coefficient > 0 for coefficient in transformed.values())
        direct_records[state] = {
            "cleared_terms": len(poly),
            "bernstein_nonzero": len(transformed),
            "minimum_bernstein_coefficient": str(min(transformed.values())),
            "sha256": digest(poly),
        }

    # One negative edge on the nonshared page 4.  Slots are
    # (c,a=x01,b=x02,r=x13,z=x23,q=q4,t).  The cleared cubic has an
    # exact (1-t) factor, leaving a quadratic in Bernstein form.
    ppl = state_polynomial(delta, tuple("PPL"))
    t_slot = 6
    cubic = [coefficient(ppl, t_slot, degree) for degree in range(4)]
    Q0 = cubic[0]
    Q1 = add(cubic[1], Q0)
    Q2 = add(cubic[2], Q1)
    assert cubic[3] == scale(Q2, -1)
    beta0 = Q0
    beta1 = add(Q0, scale(Q1, Fraction(1, 2)))
    beta2 = add(add(Q0, Q1), Q2)

    a, b, c, r, z, q = (variable(slot) for slot in (1, 2, 0, 3, 4, 5))
    beta0_residual = divide_monomial(beta0, {1: 2})
    assert len(beta0_residual) == 47
    assert all(coefficient > 0 for coefficient in beta0_residual.values())

    beta2_quotient = divide_one_plus_variable(beta2, 5)
    binomial_square = power(add(multiply(a, z), multiply(b, r), -1), 2)
    explicit_square = multiply(power(c, 2), binomial_square)
    beta2_residual = add(beta2_quotient, explicit_square, -1)
    assert len(beta2_residual) == 42
    assert all(coefficient > 0 for coefficient in beta2_residual.values())

    determinant = add(multiply(beta0, beta2), multiply(beta1, beta1), -1)
    determinant_residual = divide_monomial(determinant, {1: 2, 2: 2})
    assert len(determinant_residual) == 628
    assert all(coefficient > 0 for coefficient in determinant_residual.values())

    # Global hub exchange proves PPR; page-3/page-4 exchange proves PLP, and
    # their composition proves PRP.  Verify the relabelings on the exact
    # cleared polynomials instead of merely invoking symmetry.
    ppr = state_polynomial(delta, tuple("PPR"))
    plp = state_polynomial(delta, tuple("PLP"))
    prp = state_polynomial(delta, tuple("PRP"))
    hub_swap = (0, 2, 1, 4, 3, 5, 6)
    page_swap = (0, 1, 2, 5, 6, 3, 4)
    assert ppr == permute(ppl, hub_swap)
    assert plp == permute(ppl, page_swap)
    assert prp == permute(permute(ppl, hub_swap), page_swap)

    records = {
        "PPL_cleared": ppl,
        "PPL_beta0": beta0,
        "PPL_beta1": beta1,
        "PPL_beta2": beta2,
        "PPL_beta0_residual": beta0_residual,
        "PPL_beta2_positive_residual": beta2_residual,
        "PPL_bernstein_determinant_residual": determinant_residual,
    }
    print(json.dumps({
        "schema": "amra.opg1757.round7.nonnegative-route-chambers.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "domain": "q0,q3,q4,c>=0, positive edge floors",
        "sign_code": "P=both page activities nonnegative; L/R=the left/right activity is negative",
        "direct_bernstein": direct_records,
        "single_negative_nonshared_page": {
            "representative": "PPL",
            "symmetric_chambers": ["PPL", "PPR", "PLP", "PRP"],
            "substitution": "x14=-t, x24=(q4+t)/(1-t), 0<=t<1",
            "cleared_factorization": "(1-t)^2*Delta_b=(1-t)*[beta0*(1-t)^2+2*beta1*t*(1-t)+beta2*t^2]",
            "beta0": "a^2 times a 47-term positive-coefficient polynomial",
            "beta2": "(q4+1)*(c^2*(a*z-b*r)^2 + 42-term positive-coefficient residual)",
            "bernstein_matrix_determinant": "a^2*b^2 times a 628-term strictly positive-coefficient polynomial",
        },
        "certified_chambers": sorted(set(direct_states) | {"PPL", "PPR", "PLP", "PRP"}),
        "certified_count": 11,
        "total_nonnegative_route_sign_chambers": 27,
        "records": {
            name: {"terms": len(poly), "sha256": digest(poly)}
            for name, poly in records.items()
        },
        "scope": "exact partial sign theorem; 16 nonnegative-route sign chambers and all chambers with one negative effective route remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
