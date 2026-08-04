#!/usr/bin/env python3
"""Exact direct certificates for ten K-positive c-negative chambers."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from math import comb
import json

from verify_c_zero_fibre import (
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_nonnegative_route_chambers import state_polynomial


B_EDGE = (0, 4)
COUNT = 8
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


def constant(value):
    value = Fraction(value)
    return {} if not value else {ZERO: value}


def variable(slot):
    monomial = [0] * COUNT
    monomial[slot] = 1
    return {tuple(monomial): Fraction(1)}


def power(poly, exponent):
    assert exponent >= 0, f"polynomial power must be nonnegative, got {exponent}"
    result = constant(1)
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def route_q(state, index):
    first = variable(1 + 2 * index)
    second = variable(2 + 2 * index)
    if state == "P":
        return add(add(multiply(first, second), first), second)
    return first


def schur_substitute(poly, states):
    """Return B^2*poly at c=-tau*P/B, with tau in slot seven."""
    q0, q3, q4 = (route_q(state, index) for index, state in enumerate(states))
    P = multiply(multiply(q0, q3), q4)
    B = add(
        P,
        add(add(multiply(q0, q3), multiply(q0, q4)), multiply(q3, q4)),
    )
    tau_P = multiply(variable(7), P)
    result = {}
    for old_monomial, old_coefficient in poly.items():
        c_degree = old_monomial[0]
        assert c_degree <= 2
        monomial = list(old_monomial) + [0]
        monomial[0] = 0
        term = {
            tuple(monomial): Fraction(old_coefficient)
            * (-1 if c_degree % 2 else 1)
        }
        term = multiply(term, power(tau_P, c_degree))
        term = multiply(term, power(B, 2 - c_degree))
        result = add(result, term)
    return result


def bernstein_transform(poly, slots):
    result = dict(poly)
    for slot in slots:
        degree = max(monomial[slot] for monomial in result)
        grouped = {}
        for monomial, coefficient in result.items():
            key = monomial[:slot] + monomial[slot + 1 :]
            grouped.setdefault(key, {})[monomial[slot]] = coefficient
        transformed = {}
        for key, coefficients in grouped.items():
            for index in range(degree + 1):
                value = sum(
                    coefficients.get(power_degree, Fraction())
                    * Fraction(
                        comb(index, power_degree),
                        comb(degree, power_degree),
                    )
                    for power_degree in range(index + 1)
                )
                if value:
                    monomial = key[:slot] + (index,) + key[slot:]
                    transformed[monomial] = value
        result = transformed
    return result


def canonical(poly):
    return json.dumps(
        [
            [list(monomial), coefficient.numerator, coefficient.denominator]
            for monomial, coefficient in sorted(poly.items())
        ],
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
    assert len(delta) == 178

    certified = (
        "PLR", "PRL",
        "LPP", "RPP",
        "LPR", "LRP", "RPL", "RLP",
        "LRR", "RLL",
    )
    records = {}
    for state in certified:
        states = tuple(state)
        cleared = state_polynomial(delta, states)
        schur = schur_substitute(cleared, states)
        bounded_slots = [
            2 + 2 * index
            for index, sign in enumerate(states)
            if sign != "P"
        ] + [7]
        bernstein = bernstein_transform(schur, bounded_slots)
        assert bernstein
        assert all(coefficient > 0 for coefficient in bernstein.values())
        records[state] = {
            "schur_terms": len(schur),
            "bernstein_nonzero": len(bernstein),
            "minimum_bernstein_coefficient": str(min(bernstein.values())),
            "schur_sha256": digest(schur),
        }

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-c-direct-chambers.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "domain": "q0,q3,q4>0, c<0, positive edge floors, K=diag(q0,q3,q4,c)+11^T positive definite",
        "schur_parameterization": {
            "P": "q0*q3*q4",
            "B": "q0*q3*q4+q0*q3+q0*q4+q3*q4",
            "c": "-tau*P/B",
            "tau": "0<tau<1",
            "det_K": "P*(1-tau)",
        },
        "sign_code": "P=both page activities nonnegative; L/R=the left/right activity is negative",
        "certificate": "after clearing positive page denominators and B^2, every nonzero tensor Bernstein coefficient in the negative-activity parameters and tau is strictly positive, with ordinary monomials in all unbounded nonnegative variables",
        "certified_chambers": sorted(certified),
        "certified_count": len(certified),
        "records": records,
        "conclusion": "Delta_b>=0 in the ten listed c-negative Schur chambers",
        "scope": "ten of the 27 activity-sign chambers in the sole-negative-c part of K>0; the other 17 c-negative chambers, the three negative-page cases, and the global marked-host theorem remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
