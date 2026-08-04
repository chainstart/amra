#!/usr/bin/env python3
"""Exact Gram certificates for eight same-side negative nonshared chambers."""

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
from verify_negative_page_direct_chambers import C_EDGE, ROUTES, digest
from verify_negative_q0_no_positive_gram import (
    build_delta,
    quadratic_certificate,
)


T = 7


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {
        monomial: scalar * value
        for monomial, value in poly.items()
        if scalar * value
    }


def positive_page_chart(index, state):
    assert state in "PLR"
    q = variable(1 + 2 * index)
    s = variable(2 + 2 * index)
    one = constant(1)
    if state == "P":
        left = multiply(q, s)
        right = multiply(q, add(one, s, -1))
        denominator = add(one, multiply(q, s))
        rational_side = "R"
    else:
        negative = scale(s, -1)
        positive = add(q, s)
        denominator = add(one, s, -1)
        if state == "L":
            left, right, rational_side = negative, positive, "R"
        else:
            left, right, rational_side = positive, negative, "L"
    if rational_side == "R":
        q_numerator = add(
            add(multiply(left, right), multiply(left, denominator)),
            right,
        )
    else:
        q_numerator = add(
            add(multiply(left, right), left),
            multiply(right, denominator),
        )
    assert q_numerator == multiply(q, denominator)
    return left, right, denominator, rational_side


def positive_route_data(negative_index):
    routes = [variable(0)]
    routes.extend(
        variable(1 + 2 * index)
        for index in range(3)
        if index != negative_index
    )
    assert len(routes) == 3
    product = constant(1)
    for route in routes:
        product = multiply(product, route)
    pair_sum = constant(0)
    for left in range(3):
        for right in range(left + 1, 3):
            pair_sum = add(pair_sum, multiply(routes[left], routes[right]))
    return product, pair_sum, add(product, pair_sum)


def negative_page_chart(index, state):
    assert index in (1, 2) and state in "LR"
    product, _, determinant_sum = positive_route_data(index)
    s, t = variable(2 + 2 * index), variable(T)
    t_product = multiply(t, product)
    negative = scale(
        add(
            t_product,
            multiply(add(determinant_sum, t_product, -1), s),
        ),
        -1,
    )
    positive = s
    one_minus_s = add(constant(1), s, -1)
    data = (
        ((negative, determinant_sum), (positive, one_minus_s))
        if state == "L"
        else ((positive, one_minus_s), (negative, determinant_sum))
    )
    left, right = data
    q_numerator = add(
        add(
            multiply(left[0], right[0]),
            multiply(left[0], right[1]),
        ),
        multiply(right[0], left[1]),
    )
    assert q_numerator == scale(multiply(t_product, one_minus_s), -1)
    return data


def cleared_polynomial(delta, state, negative_index):
    assert negative_index in (1, 2) and state[negative_index] in "LR"
    negative = negative_page_chart(negative_index, state[negative_index])
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
    s_negative = variable(2 + 2 * negative_index)
    other_nonshared = 2 if negative_index == 1 else 1
    s_other = variable(2 + 2 * other_nonshared)
    return multiply(
        multiply(variable(0), add(constant(1), s_negative, -1)),
        add(constant(1), s_other, -1),
    )


def permute_original_pages(poly):
    result = {}
    for monomial, value in poly.items():
        transformed = list(monomial)
        transformed[4], transformed[5] = monomial[5], monomial[4]
        transformed[6], transformed[7] = monomial[7], monomial[6]
        transformed = tuple(transformed)
        result[transformed] = result.get(transformed, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def permute_parameter_pages(poly):
    result = {}
    for monomial, value in poly.items():
        transformed = list(monomial)
        transformed[3], transformed[5] = monomial[5], monomial[3]
        transformed[4], transformed[6] = monomial[6], monomial[4]
        transformed = tuple(transformed)
        result[transformed] = result.get(transformed, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def representative_record(delta, state):
    cleared = cleared_polynomial(delta, state, 1)
    factor = manifest_factor(1)
    core = divide_polynomial(cleared, factor)
    assert cleared == multiply(factor, core)
    if state == "LLL":
        assert len(cleared) == 2230 and len(core) == 935
        certificate = quadratic_certificate(core, 6, [2, 4, T])
        assert certificate["endpoint_bernstein_nonzero"] == [477, 971]
        assert certificate["endpoint_minimum"] == ["1/12", "1/12"]
        assert certificate["determinant_terms"] == 7740
        assert certificate["determinant_common_monomial"] == [0, 0, 2, 0, 0, 1, 0, 0]
        assert certificate["determinant_residual_terms"] == 7740
        assert certificate["determinant_bernstein_nonzero"] == 13667
        assert certificate["determinant_minimum"] == "1/270"
    else:
        assert state == "RLL"
        assert len(cleared) == 2098 and len(core) == 786
        certificate = quadratic_certificate(core, 4, [2, 6, T])
        assert certificate["endpoint_bernstein_nonzero"] == [363, 796]
        assert certificate["endpoint_minimum"] == ["1/12", "1/6"]
        assert certificate["determinant_terms"] == 5802
        assert certificate["determinant_common_monomial"] == [1, 0, 2, 0, 0, 1, 0, 0]
        assert certificate["determinant_residual_terms"] == 5802
        assert certificate["determinant_bernstein_nonzero"] == 11551
        assert certificate["determinant_minimum"] == "1/270"
    return {
        "cleared_terms": len(cleared),
        "manifest_factor": "c*(1-s_negative)*(1-s_other)",
        "core": certificate,
        "cleared_sha256": digest(cleared),
        "core_sha256": digest(core),
    }, cleared


def main():
    delta, forest_count, connected_count = build_delta()
    assert permute_original_pages(delta) == delta

    records = {}
    representatives = {}
    for state in ("LLL", "RLL"):
        records[state], representatives[state] = representative_record(delta, state)

    q3_rrr = cleared_polynomial(delta, "RRR", 1)
    q3_lrr = cleared_polynomial(delta, "LRR", 1)
    assert q3_rrr == representatives["LLL"]
    assert q3_lrr == representatives["RLL"]

    for state, q3_poly in (
        ("LLL", representatives["LLL"]),
        ("RRR", q3_rrr),
        ("RLL", representatives["RLL"]),
        ("LRR", q3_lrr),
    ):
        q4_poly = cleared_polynomial(delta, state, 2)
        assert q4_poly == permute_parameter_pages(q3_poly)

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-nonshared-same-side-gram.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "domain": "q3<0 or q4<0 is the sole negative diagonal route quantity, K>0, and the listed activity word holds",
        "representatives": ["q3:LLL", "q3:RLL"],
        "symmetry_closure": {
            "q3:LLL": ["q3:LLL", "q3:RRR", "q4:LLL", "q4:RRR"],
            "q3:RLL": ["q3:RLL", "q3:LRR", "q4:RLL", "q4:LRR"],
        },
        "certified_chambers": [
            "q3:LLL", "q3:LRR", "q3:RLL", "q3:RRR",
            "q4:LLL", "q4:LRR", "q4:RLL", "q4:RRR",
        ],
        "certified_count": 8,
        "records": records,
        "conclusion": "Delta_b>=0 in all eight listed same-side negative-nonshared-page chambers",
        "scope": "adds four q3-negative and their four exact q4-negative page-swap images; 26 negative-page orientations remain open, so the generic sign and OPG-1757 are not claimed",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
