#!/usr/bin/env python3
"""Exact all-chamber certificate on the negative-c Schur endpoint."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json

from verify_c_zero_fibre import EDGES, reconstruct_original, restrict_original_zero
from verify_negative_c_direct_chambers import (
    add,
    bernstein_transform,
    constant,
    digest,
    multiply,
    power,
    variable,
)


B_EDGE = (0, 4)
C_EDGE = (1, 2)
ROUTES = (((0, 1), (0, 2)), ((1, 3), (2, 3)), ((1, 4), (2, 4)))


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {monomial: scalar * value for monomial, value in poly.items() if value}


def required_denominator_degrees(poly, states):
    """Return the exact rational-side degree needed on each page."""
    assert poly
    assert len(states) == len(ROUTES)
    required = []
    for state, edges in zip(states, ROUTES):
        assert state in "PLR"
        rational_edge = edges[0] if state == "R" else edges[1]
        slot = EDGES.index(rational_edge)
        required.append(max(monomial[slot] for monomial in poly))
    return tuple(required)


def uniform_state_polynomial(poly, states, denominator_degrees=None):
    """Use q plus one unit-interval orientation coordinate on every page.

    ``denominator_degrees`` gives the common clearing degree on each page.
    It may exceed the polynomial's degree in the rational-side activity,
    which only introduces a positive chart factor.  It must never be smaller.
    """
    required_degrees = required_denominator_degrees(poly, states)
    if denominator_degrees is None:
        denominator_degrees = required_degrees
    denominator_degrees = tuple(denominator_degrees)
    assert len(states) == len(ROUTES) == len(denominator_degrees)
    assert all(degree >= 0 for degree in denominator_degrees)
    assert all(
        supplied >= required
        for supplied, required in zip(denominator_degrees, required_degrees)
    ), (states, denominator_degrees, required_degrees)
    c = variable(0)
    page_factors = []
    for index, state in enumerate(states):
        q = variable(1 + 2 * index)
        orientation = variable(2 + 2 * index)
        if state == "P":
            denominator = add(constant(1), multiply(q, orientation))
            left = multiply(q, orientation)
            right = multiply(q, add(constant(1), orientation, -1))
            page_factors.append((left, right, denominator, "R"))
        else:
            denominator = add(constant(1), orientation, -1)
            negative = scale(orientation, -1)
            positive = add(q, orientation)
            if state == "L":
                page_factors.append((negative, positive, denominator, "R"))
            else:
                page_factors.append((positive, negative, denominator, "L"))

    result = {}
    for original_monomial, original_coefficient in poly.items():
        term = constant(original_coefficient)
        term = multiply(term, power(c, original_monomial[EDGES.index(C_EDGE)]))
        for edges, factors, denominator_degree in zip(
            ROUTES, page_factors, denominator_degrees
        ):
            left_degree = original_monomial[EDGES.index(edges[0])]
            right_degree = original_monomial[EDGES.index(edges[1])]
            left, right, denominator, rational_side = factors
            term = multiply(term, power(left, left_degree))
            term = multiply(term, power(right, right_degree))
            rational_degree = left_degree if rational_side == "L" else right_degree
            assert rational_degree <= denominator_degree, (
                states,
                edges,
                rational_side,
                rational_degree,
                denominator_degree,
            )
            term = multiply(
                term,
                power(denominator, denominator_degree - rational_degree),
            )
        result = add(result, term)
    return result


def schur_substitute(poly):
    """Return B^2*poly(c=-tau*P/B)."""
    q0, q3, q4 = (variable(slot) for slot in (1, 3, 5))
    P = multiply(multiply(q0, q3), q4)
    B = add(P, add(add(multiply(q0, q3), multiply(q0, q4)), multiply(q3, q4)))
    tau_P = multiply(variable(7), P)
    result = {}
    for monomial, coefficient in poly.items():
        c_degree = monomial[0]
        assert c_degree <= 2
        reduced = list(monomial)
        reduced[0] = 0
        term = {tuple(reduced): coefficient * (-1 if c_degree % 2 else 1)}
        term = multiply(term, power(tau_P, c_degree))
        term = multiply(term, power(B, 2 - c_degree))
        result = add(result, term)
    return result


def substitute_tau_one(poly):
    result = {}
    for monomial, coefficient in poly.items():
        reduced = list(monomial)
        reduced[7] = 0
        reduced = tuple(reduced)
        result[reduced] = result.get(reduced, Fraction()) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def square(poly):
    return multiply(poly, poly)


def hard_factor_data():
    q0, s0, q3, s3, q4, s4 = (variable(slot) for slot in range(1, 7))
    one = constant(1)
    one_minus_s0 = add(one, s0, -1)
    one_minus_s3 = add(one, s3, -1)
    one_minus_s4 = add(one, s4, -1)
    one_plus_q0s0 = add(one, multiply(q0, s0))
    one_plus_q3s3 = add(one, multiply(q3, s3))
    one_plus_q4s4 = add(one, multiply(q4, s4))
    B = add(
        multiply(multiply(q0, q3), q4),
        add(add(multiply(q0, q3), multiply(q0, q4)), multiply(q3, q4)),
    )

    H_A = add(
        add(
            multiply(multiply(q0, square(s0)), square(one_minus_s4)),
            multiply(multiply(q4, square(s4)), square(one_minus_s0)),
        ),
        square(add(s0, s4, -1)),
    )
    H_B = add(
        add(
            multiply(multiply(q0, square(s0)), square(add(q4, s4))),
            multiply(square(q4), square(s0)),
        ),
        add(
            add(
                multiply(multiply(q4, square(s4)), square(one_minus_s0)),
                scale(multiply(multiply(q4, s0), s4), 2),
            ),
            square(s4),
        ),
    )
    H_C = add(
        add(
            multiply(multiply(multiply(q0, square(s0)), square(s4)), add(q4, one)),
            multiply(square(q4), square(one_minus_s0)),
        ),
        add(
            multiply(
                multiply(q4, s4),
                add(multiply(square(s0), s4), scale(one_minus_s0, 2)),
            ),
            square(s4),
        ),
    )
    H_D = add(
        square(add(multiply(q0, s4), multiply(q4, s0), -1)),
        add(
            add(
                multiply(multiply(square(q0), q4), square(s4)),
                multiply(multiply(q0, square(q4)), square(s0)),
            ),
            add(
                add(
                    scale(multiply(multiply(multiply(q0, q4), square(s0)), s4), 2),
                    scale(multiply(multiply(multiply(q0, q4), s0), square(s4)), 2),
                ),
                add(
                    multiply(multiply(q0, square(s0)), square(s4)),
                    multiply(multiply(q4, square(s0)), square(s4)),
                ),
            ),
        ),
    )

    q0q3q4_square = multiply(multiply(square(q0), square(q3)), square(q4))
    q0q3_square = multiply(square(q0), square(q3))
    q3_square = square(q3)
    common_P = multiply(multiply(q0q3q4_square, B), one_plus_q0s0)
    common_nonshared = multiply(multiply(q0q3_square, B), one_plus_q0s0)

    expected = {
        "PPP": multiply(
            multiply(multiply(common_P, one_plus_q4s4), square(one_plus_q3s3)),
            H_A,
        ),
        "PLP": multiply(
            multiply(multiply(common_P, one_plus_q4s4), square(one_minus_s3)),
            H_A,
        ),
        "PRP": multiply(
            multiply(multiply(common_P, one_plus_q4s4), square(one_minus_s3)),
            H_A,
        ),
        "PPL": multiply(
            multiply(multiply(common_nonshared, one_minus_s4), square(one_plus_q3s3)),
            H_B,
        ),
        "PPR": multiply(
            multiply(multiply(common_nonshared, one_minus_s4), square(one_plus_q3s3)),
            H_C,
        ),
    }
    common_D = multiply(q3_square, B)
    for state in ("LLL", "RRR", "LRL", "RLR"):
        expected[state] = multiply(
            multiply(
                multiply(common_D, multiply(one_minus_s0, one_minus_s4)),
                square(one_minus_s3),
            ),
            H_D,
        )
    for state in ("LPL", "RPR"):
        expected[state] = multiply(
            multiply(
                multiply(common_D, multiply(one_minus_s0, one_minus_s4)),
                square(one_plus_q3s3),
            ),
            H_D,
        )
    return expected, {"H_A": H_A, "H_B": H_B, "H_C": H_C, "H_D": H_D}


def main():
    deletion, _, forest_count, connected_count = reconstruct_original()
    assert (forest_count, connected_count) == (128, 58)
    C = restrict_original_zero(deletion, B_EDGE)
    assert len(C) == 47

    hard_expected, kernels = hard_factor_data()
    hard_states = set(hard_expected)
    hard_families = {
        **{state: "H_A" for state in ("PPP", "PLP", "PRP")},
        "PPL": "H_B",
        "PPR": "H_C",
        **{
            state: "H_D"
            for state in ("LLL", "RRR", "LRL", "RLR", "LPL", "RPR")
        },
    }
    assert set(hard_families) == hard_states
    all_states = {"".join(states) for states in product("PLR", repeat=3)}
    direct_states = all_states - hard_states
    assert len(hard_states) == 11 and len(direct_states) == 16

    hard_records = {}
    direct_records = {}
    for state in sorted(all_states):
        cleared = uniform_state_polynomial(
            C,
            tuple(state),
            denominator_degrees=(2, 2, 2),
        )
        endpoint = scale(substitute_tau_one(schur_substitute(cleared)), -1)
        if state in hard_states:
            assert endpoint == hard_expected[state]
            hard_records[state] = {
                "factor_family": hard_families[state],
                "endpoint_terms": len(endpoint),
                "endpoint_sha256": digest(endpoint),
            }
        else:
            transformed = bernstein_transform(endpoint, [2, 4, 6])
            assert transformed
            assert all(coefficient > 0 for coefficient in transformed.values())
            direct_records[state] = {
                "endpoint_terms": len(endpoint),
                "bernstein_nonzero": len(transformed),
                "minimum_bernstein_coefficient": str(min(transformed.values())),
                "endpoint_sha256": digest(endpoint),
            }

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-c-schur-endpoint.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "C_terms": len(C),
        },
        "domain": "q0,q3,q4>0, c=-P/B, positive edge floors; equivalently the c-negative det(K)=0 Schur endpoint",
        "uniform_page_coordinates": {
            "P": "xL=q*s, xR=q*(1-s)/(1+q*s), 0<=s<=1",
            "L": "xL=-s, xR=(q+s)/(1-s), 0<=s<1",
            "R": "xR=-s, xL=(q+s)/(1-s), 0<=s<1",
        },
        "schur": {
            "P": "q0*q3*q4",
            "B": "q0*q3*q4+q0*q3+q0*q4+q3*q4",
            "c": "-P/B",
            "det_K": "0",
        },
        "identity": "Delta_b=-D*C when det(K)=A=0; D>=0 by closure of the connection Gram certificate",
        "certificate": {
            "direct_bernstein_states": sorted(direct_states),
            "direct_count": len(direct_states),
            "factored_states": sorted(hard_states),
            "factored_count": len(hard_states),
            "kernel_decompositions": {
                "H_A": "q0*s0^2*(1-s4)^2+q4*s4^2*(1-s0)^2+(s0-s4)^2",
                "H_B": "q0*s0^2*(q4+s4)^2+q4^2*s0^2+q4*s4^2*(1-s0)^2+2*q4*s0*s4+s4^2",
                "H_C": "q0*s0^2*s4^2*(q4+1)+q4^2*(1-s0)^2+q4*s4*(s0^2*s4+2*(1-s0))+s4^2",
                "H_D": "(q0*s4-q4*s0)^2 plus six nonnegative monomials",
            },
        },
        "direct_records": direct_records,
        "hard_records": hard_records,
        "certified_chambers": sorted(all_states),
        "certified_count": len(all_states),
        "conclusion": "-C>=0 and hence Delta_b>=0 on every one of the 27 c-negative Schur endpoint activity chambers",
        "records": {
            name: {"terms": len(poly), "sha256": digest(poly)}
            for name, poly in kernels.items()
        },
        "scope": "complete det(K)=0 contact endpoint for the sole-negative-c chamber; the open interior 0<tau<1, negative-page cases, and global marked-host theorem remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
