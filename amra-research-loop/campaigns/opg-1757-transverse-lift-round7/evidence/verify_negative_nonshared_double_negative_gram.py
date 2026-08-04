#!/usr/bin/env python3
"""Exact Gram certificates for four double-negative nonshared chambers."""

from __future__ import annotations

from fractions import Fraction
import json

from verify_c_zero_fibre import EDGES
from verify_mixed_three_negative import divide_polynomial
from verify_negative_c_direct_chambers import (
    add,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_nonshared_same_side_gram import (
    permute_original_pages,
    permute_parameter_pages,
    positive_page_chart,
    positive_route_data,
    scale,
)
from verify_negative_page_direct_chambers import C_EDGE, ROUTES, digest
from verify_negative_q0_no_positive_gram import build_delta, quadratic_certificate


T = 7


def negative_page_chart(index):
    product, pair_sum, _ = positive_route_data(index)
    s, t = variable(2 + 2 * index), variable(T)
    one_minus_s = add(constant(1), s, -1)
    fill = add(s, multiply(t, one_minus_s))
    left = (
        scale(multiply(product, s), -1),
        add(pair_sum, multiply(product, s)),
    )
    right = (
        scale(multiply(multiply(product, t), one_minus_s), -1),
        add(pair_sum, multiply(product, fill)),
    )
    q_numerator = add(
        add(multiply(left[0], right[0]), multiply(left[0], right[1])),
        multiply(right[0], left[1]),
    )
    assert q_numerator == scale(
        multiply(multiply(product, fill), left[1]),
        -1,
    )
    route_numerator = add(
        multiply(product, right[1]),
        multiply(multiply(product, fill), add(pair_sum, product)),
        -1,
    )
    assert route_numerator == multiply(
        multiply(product, pair_sum),
        multiply(one_minus_s, add(constant(1), t, -1)),
    )
    return left, right


def cleared_polynomial(delta, state, negative_index):
    assert state[negative_index] == "N"
    negative = negative_page_chart(negative_index)
    positive = {
        index: positive_page_chart(index, state[index])
        for index in range(3)
        if index != negative_index
    }
    result = {}
    for original_monomial, value in delta.items():
        term = constant(value)
        term = multiply(
            term,
            power(variable(0), original_monomial[EDGES.index(C_EDGE)]),
        )
        for index, edges in enumerate(ROUTES):
            if index == negative_index:
                for edge, (numerator, denominator) in zip(edges, negative):
                    degree = original_monomial[EDGES.index(edge)]
                    assert degree <= 2
                    term = multiply(term, power(numerator, degree))
                    term = multiply(term, power(denominator, 2 - degree))
                continue
            left, right, denominator, rational_side = positive[index]
            left_degree = original_monomial[EDGES.index(edges[0])]
            right_degree = original_monomial[EDGES.index(edges[1])]
            term = multiply(term, power(left, left_degree))
            term = multiply(term, power(right, right_degree))
            rational_degree = left_degree if rational_side == "L" else right_degree
            assert rational_degree <= 2
            term = multiply(term, power(denominator, 2 - rational_degree))
        result = add(result, term)
    return result


def manifest_factor(negative_index):
    product, pair_sum, _ = positive_route_data(negative_index)
    s_negative = variable(2 + 2 * negative_index)
    left_denominator = add(pair_sum, multiply(product, s_negative))
    other_nonshared = 2 if negative_index == 1 else 1
    q_other = variable(1 + 2 * other_nonshared)
    s_other = variable(2 + 2 * other_nonshared)
    return multiply(
        power(variable(0), 2),
        multiply(
            left_denominator,
            multiply(q_other, add(constant(1), s_other, -1)),
        ),
    )


def representative_record(delta, state):
    cleared = cleared_polynomial(delta, state, 1)
    factor = manifest_factor(1)
    core = divide_polynomial(cleared, factor)
    assert cleared == multiply(factor, core)
    if state == "LNL":
        assert len(cleared) == 4115 and len(core) == 1234
        certificate = quadratic_certificate(core, 6, [2, 4, T])
        assert certificate["endpoint_bernstein_nonzero"] == [485, 1206]
        assert certificate["endpoint_minimum"] == ["1/36", "1/36"]
        assert certificate["determinant_terms"] == 10539
        assert certificate["determinant_common_monomial"] == [0, 0, 2, 0, 0, 1, 0, 0]
        assert certificate["determinant_residual_terms"] == 10539
        assert certificate["determinant_bernstein_nonzero"] == 15900
        assert certificate["determinant_minimum"] == "1/1200"
    else:
        assert state == "RNR"
        assert len(cleared) == 4125 and len(core) == 1239
        certificate = quadratic_certificate(core, 6, [2, 4, T])
        assert certificate["endpoint_bernstein_nonzero"] == [410, 1053]
        assert certificate["endpoint_minimum"] == ["1/18", "1/36"]
        assert certificate["determinant_terms"] == 10374
        assert certificate["determinant_common_monomial"] == [0, 0, 2, 0, 0, 1, 0, 0]
        assert certificate["determinant_residual_terms"] == 10374
        assert certificate["determinant_bernstein_nonzero"] == 13562
        assert certificate["determinant_minimum"] == "1/1350"
    return {
        "cleared_terms": len(cleared),
        "manifest_factor": "c^2*q_other*(1-s_other)*(C+s_negative*P)",
        "core": certificate,
        "cleared_sha256": digest(cleared),
        "core_sha256": digest(core),
    }, cleared


def main():
    delta, forest_count, connected_count = build_delta()
    assert permute_original_pages(delta) == delta
    records = {}
    q3_polynomials = {}
    for state in ("LNL", "RNR"):
        records[state], q3_polynomials[state] = representative_record(delta, state)

    for q3_state, q4_state in (("LNL", "LLN"), ("RNR", "RRN")):
        q4_poly = cleared_polynomial(delta, q4_state, 2)
        assert q4_poly == permute_parameter_pages(q3_polynomials[q3_state])

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-nonshared-double-negative-gram.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "domain": "q3<0 or q4<0 is the sole negative diagonal route quantity, K>0, and both activities on that negative page are negative",
        "representatives": ["q3:LNL", "q3:RNR"],
        "symmetry_closure": {
            "q3:LNL": ["q3:LNL", "q4:LLN"],
            "q3:RNR": ["q3:RNR", "q4:RRN"],
        },
        "certified_chambers": ["q3:LNL", "q3:RNR", "q4:LLN", "q4:RRN"],
        "certified_count": 4,
        "records": records,
        "conclusion": "Delta_b>=0 in all four listed double-negative nonshared-page chambers",
        "scope": "adds two q3-negative chambers and their exact q4 page-swap images; 22 negative-page orientations remain open, so the generic sign and OPG-1757 are not claimed",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
