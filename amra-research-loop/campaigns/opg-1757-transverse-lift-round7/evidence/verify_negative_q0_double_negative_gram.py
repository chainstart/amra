#!/usr/bin/env python3
"""Exact nested-odds Gram certificates for all five remaining q0 chambers."""

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
    common_monomial,
    divide_monomial,
    gram,
    positive_bernstein,
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


def positive_routes():
    c, q3, q4 = (variable(slot) for slot in (0, 3, 5))
    product = multiply(multiply(c, q3), q4)
    pair_sum = add(
        add(multiply(c, q3), multiply(c, q4)),
        multiply(q3, q4),
    )
    determinant_sum = add(pair_sum, product)
    return c, q3, q4, product, pair_sum, determinant_sum


def positive_page_chart(index, state):
    """Uniform q/orientation chart for a positive effective page route."""
    assert index in (1, 2) and state in "PLR"
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


def negative_page_chart():
    """Sequentially fill the admissible negative-page odds on [0,1]^2."""
    _, _, _, product, pair_sum, _ = positive_routes()
    s = variable(2)
    t = variable(T)
    one = constant(1)
    one_minus_s = add(one, s, -1)
    fill = add(s, multiply(t, one_minus_s))
    left_numerator = scale(multiply(product, s), -1)
    left_denominator = add(pair_sum, multiply(product, s))
    right_numerator = scale(
        multiply(multiply(product, t), one_minus_s),
        -1,
    )
    right_denominator = add(pair_sum, multiply(product, fill))

    q_numerator = add(
        add(
            multiply(left_numerator, right_numerator),
            multiply(left_numerator, right_denominator),
        ),
        multiply(right_numerator, left_denominator),
    )
    expected_q_numerator = scale(
        multiply(multiply(product, fill), left_denominator),
        -1,
    )
    assert q_numerator == expected_q_numerator

    # q0=-product*fill/right_denominator.  Therefore the route determinant
    # has numerator product*pair_sum*(1-s)*(1-t), exactly the square domain.
    route_determinant_numerator = add(
        multiply(product, right_denominator),
        multiply(
            multiply(product, fill),
            add(pair_sum, product),
        ),
        -1,
    )
    assert route_determinant_numerator == multiply(
        multiply(product, pair_sum),
        multiply(one_minus_s, add(one, t, -1)),
    )
    return (
        (left_numerator, left_denominator),
        (right_numerator, right_denominator),
    )


def cleared_polynomial(delta, state):
    """Apply all charts and clear every positive activity denominator squared."""
    assert state[0] == "N" and len(state) == 3
    negative = negative_page_chart()
    positive = [
        positive_page_chart(index, state[index])
        for index in (1, 2)
    ]
    result = {}
    for original_monomial, value in delta.items():
        term = constant(value)
        term = multiply(
            term,
            power(variable(0), original_monomial[EDGES.index(C_EDGE)]),
        )
        for edge, (numerator, denominator) in zip(ROUTES[0], negative):
            degree = original_monomial[EDGES.index(edge)]
            assert degree <= 2
            term = multiply(term, power(numerator, degree))
            term = multiply(term, power(denominator, 2 - degree))
        for edges, chart in zip(ROUTES[1:], positive):
            left, right, denominator, rational_side = chart
            left_degree = original_monomial[EDGES.index(edges[0])]
            right_degree = original_monomial[EDGES.index(edges[1])]
            term = multiply(term, power(left, left_degree))
            term = multiply(term, power(right, right_degree))
            rational_degree = left_degree if rational_side == "L" else right_degree
            assert rational_degree <= 2
            term = multiply(term, power(denominator, 2 - rational_degree))
        result = add(result, term)
    return result


def manifest_factor(state):
    c, q3, q4, _, _, _ = positive_routes()
    s3, s4 = variable(4), variable(6)
    q3_denominator = add(constant(1), multiply(q3, s3))
    factor = multiply(power(c, 4), power(q3, 4))
    if state == "NPP":
        q4_denominator = add(constant(1), multiply(q4, s4))
        return multiply(
            factor,
            multiply(power(q4, 4), multiply(q3_denominator, q4_denominator)),
        )
    assert state in ("NPL", "NPR")
    return multiply(
        factor,
        multiply(
            power(q4, 2),
            multiply(q3_denominator, add(constant(1), s4, -1)),
        ),
    )


def first_endpoint_kernel():
    """A manifest sum of two nonnegative square multiples."""
    _, q3, q4, _, _, determinant_sum = positive_routes()
    s0, s3 = variable(2), variable(4)
    return add(
        multiply(
            multiply(power(q3, 2), power(s3, 2)),
            multiply(
                add(variable(0), q4),
                power(add(constant(1), s0, -1), 2),
            ),
        ),
        multiply(determinant_sum, power(add(s0, s3, -1), 2)),
    )


def outer_endpoint_certificate(endpoint, state):
    first = first_endpoint_kernel()
    assert len(first) == 18
    second = divide_polynomial(endpoint, first)
    expected_terms = {"NPP": 18, "NPL": 18, "NPR": 24}[state]
    assert len(second) == expected_terms
    assert endpoint == multiply(first, second)
    second_record = quadratic_certificate(second, 2, [6])
    expected = {
        "NPP": ([6, 4], 7),
        "NPL": ([6, 21], 36),
        "NPR": ([18, 7], 36),
    }[state]
    assert second_record["endpoint_bernstein_nonzero"] == expected[0]
    assert second_record["endpoint_minimum"] == ["1", "1"]
    assert second_record["determinant_terms"] == 21
    assert second_record["determinant_common_monomial"] == [0, 0, 0, 0, 0, 2, 2, 0]
    assert second_record["determinant_residual_terms"] == 21
    assert second_record["determinant_bernstein_nonzero"] == expected[1]
    assert second_record["determinant_minimum"] == "1"
    return {
        "factorization": "K3*K4",
        "K3_terms": len(first),
        "K3_sos": "q3^2*s3^2*(c+q4)*(1-s0)^2+B*(s0-s3)^2",
        "K3_sha256": digest(first),
        "K4": second_record,
    }


def determinant_core(determinant, state):
    _, q3, q4, product, pair_sum, _ = positive_routes()
    s0, s3, s4 = variable(2), variable(4), variable(6)
    common = {
        "NPP": (0, 0, 2, 0, 0, 0, 0, 0),
        "NPL": (0, 0, 2, 0, 0, 0, 0, 0),
        "NPR": (0, 0, 2, 0, 0, 0, 2, 0),
    }[state]
    assert common_monomial(determinant) == common
    left_denominator = add(pair_sum, multiply(product, s0))
    factors = [
        add(constant(1), s0, -1),
        add(constant(1), s3, -1),
        left_denominator,
    ]
    if state == "NPP":
        factors.append(add(constant(1), s4, -1))
    elif state == "NPL":
        factors.append(add(q4, s4))
    positive_factor = constant(1)
    for factor in factors:
        positive_factor = multiply(positive_factor, power(factor, 2))
    quotient = divide_monomial(determinant, common)
    core = divide_polynomial(quotient, positive_factor)
    assert determinant == multiply(
        {common: Fraction(1)},
        multiply(positive_factor, core),
    )
    assert len(core) == {"NPP": 57, "NPL": 57, "NPR": 163}[state]
    return core, common


def last_nine_term_kernel():
    _, q3, q4, _, _, _ = positive_routes()
    s3, s4 = variable(4), variable(6)
    return add(
        add(
            multiply(
                multiply(q3, power(s3, 2)),
                power(add(constant(1), s4, -1), 2),
            ),
            multiply(
                multiply(q4, power(s4, 2)),
                power(add(constant(1), s3, -1), 2),
            ),
        ),
        power(add(s3, s4, -1), 2),
    )


def core_certificate(core, state):
    gamma0, _, gamma2, determinant = gram(core, 2)
    gamma0_bernstein = positive_bernstein(gamma0, [4, 6])
    expected_gamma0 = {"NPP": 15, "NPL": 15, "NPR": 72}[state]
    assert len(gamma0_bernstein) == expected_gamma0
    assert min(gamma0_bernstein.values()) == 1

    if state == "NPP":
        gamma2_bernstein = positive_bernstein(gamma2, [4, 6])
        assert len(gamma2_bernstein) == 18
        assert min(gamma2_bernstein.values()) == Fraction(1, 2)
        gamma2_record = {
            "kind": "direct_tensor_bernstein",
            "terms": len(gamma2),
            "bernstein_nonzero": len(gamma2_bernstein),
            "minimum": str(min(gamma2_bernstein.values())),
            "sha256": digest(gamma2),
        }
    else:
        gamma2_record = {
            "kind": "nested_s3_gram",
            **quadratic_certificate(gamma2, 4, [6]),
        }
        expected = {
            "NPL": ([7, 36], 57, 87),
            "NPR": ([36, 17], 117, 147),
        }[state]
        assert gamma2_record["endpoint_bernstein_nonzero"] == expected[0]
        assert gamma2_record["endpoint_minimum"] == ["1", "1"]
        assert gamma2_record["determinant_terms"] == expected[1]
        assert gamma2_record["determinant_common_monomial"] == [0, 0, 0, 2, 0, 2, 2, 0]
        assert gamma2_record["determinant_residual_terms"] == expected[1]
        assert gamma2_record["determinant_bernstein_nonzero"] == expected[2]
        assert gamma2_record["determinant_minimum"] == "1"

    inner_common = common_monomial(determinant)
    expected_common = {
        "NPP": (0, 0, 0, 2, 2, 2, 2, 0),
        "NPL": (0, 0, 0, 2, 2, 2, 2, 0),
        "NPR": (0, 0, 0, 2, 2, 2, 0, 0),
    }[state]
    assert inner_common == expected_common
    residual = divide_monomial(determinant, inner_common)
    if state == "NPP":
        _, _, _, _, pair_sum, determinant_sum = positive_routes()
        kernel = last_nine_term_kernel()
        assert len(kernel) == 9
        assert residual == multiply(
            multiply(kernel, determinant_sum),
            power(pair_sum, 2),
        )
        determinant_record = {
            "kind": "explicit_nonnegative_factorization",
            "terms": len(determinant),
            "common_monomial": list(inner_common),
            "residual_terms": len(residual),
            "factorization": "H9*B*C^2",
            "H9_terms": len(kernel),
            "H9_sos": "q3*s3^2*(1-s4)^2+q4*s4^2*(1-s3)^2+(s3-s4)^2",
            "H9_sha256": digest(kernel),
            "sha256": digest(determinant),
        }
    else:
        transformed = positive_bernstein(residual, [4, 6])
        expected = {
            "NPL": (188, Fraction(1, 2)),
            "NPR": (598, Fraction(1, 6)),
        }[state]
        assert len(transformed) == expected[0]
        assert min(transformed.values()) == expected[1]
        determinant_record = {
            "kind": "direct_tensor_bernstein",
            "terms": len(determinant),
            "common_monomial": list(inner_common),
            "residual_terms": len(residual),
            "bernstein_nonzero": len(transformed),
            "minimum": str(min(transformed.values())),
            "sha256": digest(determinant),
        }
    return {
        "terms": len(core),
        "s0_endpoint0": {
            "terms": len(gamma0),
            "bernstein_nonzero": len(gamma0_bernstein),
            "minimum": str(min(gamma0_bernstein.values())),
            "sha256": digest(gamma0),
        },
        "s0_endpoint1": gamma2_record,
        "s0_gram_determinant": determinant_record,
        "sha256": digest(core),
    }


def permute_pages(poly):
    result = {}
    for monomial, value in poly.items():
        transformed = list(monomial)
        transformed[3], transformed[5] = monomial[5], monomial[3]
        transformed[4], transformed[6] = monomial[6], monomial[4]
        transformed = tuple(transformed)
        result[transformed] = result.get(transformed, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def main():
    delta, forest_count, connected_count = build_delta()
    representatives = {
        state: cleared_polynomial(delta, state)
        for state in ("NPP", "NPL", "NPR")
    }
    all_states = {
        state: cleared_polynomial(delta, state)
        for state in ("NPP", "NPL", "NPR", "NLP", "NRP")
    }
    assert permute_pages(representatives["NPL"]) == all_states["NLP"]
    assert permute_pages(representatives["NPR"]) == all_states["NRP"]

    records = {}
    for state, cleared in representatives.items():
        factor = manifest_factor(state)
        reduced = divide_polynomial(cleared, factor)
        assert cleared == multiply(factor, reduced)
        assert len(reduced) == {"NPP": 501, "NPL": 501, "NPR": 474}[state]
        beta0, _, beta2, determinant = gram(reduced, T)
        beta0_bernstein = positive_bernstein(beta0, [2, 4, 6])
        expected_beta0 = {"NPP": 25, "NPL": 129, "NPR": 43}[state]
        assert len(beta0_bernstein) == expected_beta0
        assert min(beta0_bernstein.values()) == Fraction(1, 6)
        core, common = determinant_core(determinant, state)
        records[state] = {
            "cleared_terms": len(cleared),
            "reduced_terms": len(reduced),
            "manifest_factor_sha256": digest(factor),
            "t_endpoint0": {
                "terms": len(beta0),
                "bernstein_nonzero": len(beta0_bernstein),
                "minimum": str(min(beta0_bernstein.values())),
                "sha256": digest(beta0),
            },
            "t_endpoint1": outer_endpoint_certificate(beta2, state),
            "t_gram_terms": len(determinant),
            "t_gram_common_monomial": list(common),
            "t_gram_core": core_certificate(core, state),
            "cleared_sha256": digest(cleared),
            "reduced_sha256": digest(reduced),
        }

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-q0-double-negative-gram.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "domain": "q0<0, q3>0, q4>0, c>0, K>0; both activities on the q0 page are negative",
        "nested_odds_chart": {
            "Rmax": "c*q3*q4/(c*q3+c*q4+q3*q4)",
            "fill": "s0+t*(1-s0)",
            "x0L": "-s0*P/(C+s0*P)",
            "x0R": "-t*(1-s0)*P/(C+P*(s0+t-s0*t))",
            "det_K_numerator": "P*C*(1-s0)*(1-t)",
        },
        "representatives": ["NPP", "NPL", "NPR"],
        "symmetry_closure": {
            "NPP": ["NPP"],
            "NPL": ["NPL", "NLP"],
            "NPR": ["NPR", "NRP"],
        },
        "certified_chambers": ["NLP", "NPL", "NPP", "NPR", "NRP"],
        "certified_count": 5,
        "records": records,
        "conclusion": "Delta_b>=0 in all five remaining q0-negative double-negative-page chambers",
        "scope": "completes all 27 q0-negative activity chambers; 34 q3/q4-negative orientations remain open, so the generic sign and OPG-1757 are not claimed",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
