#!/usr/bin/env python3
"""Exact nested Gram/SOS certificate for four opposite-side chambers."""

from __future__ import annotations

from fractions import Fraction
import json

from verify_mixed_three_negative import divide_polynomial
from verify_negative_c_direct_chambers import (
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_nonshared_same_side_gram import (
    cleared_polynomial,
    manifest_factor,
    permute_parameter_pages,
    positive_route_data,
)
from verify_negative_page_direct_chambers import digest
from verify_negative_q0_no_positive_gram import (
    build_delta,
    coefficient,
    common_monomial,
    divide_monomial,
    gram,
    positive_bernstein,
    quadratic_certificate,
    scale,
)


T = 7


def sum_polynomials(*polynomials):
    result = constant(0)
    for polynomial in polynomials:
        result = add(result, polynomial)
    return result


def square(polynomial):
    return multiply(polynomial, polynomial)


def weighted_square(weight, left, right, scalar=1):
    return scale(multiply(weight, square(add(left, right, -1))), scalar)


def positive_residual_record(polynomial):
    assert polynomial
    assert all(value > 0 for value in polynomial.values())
    return {
        "terms": len(polynomial),
        "minimum": str(min(polynomial.values())),
        "sha256": digest(polynomial),
    }


def row(polynomial):
    return {
        "terms": len(polynomial),
        "negative_coefficients": sum(value < 0 for value in polynomial.values()),
        "degrees": [
            max(monomial[slot] for monomial in polynomial)
            for slot in range(8)
        ],
        "sha256": digest(polynomial),
    }


def bounded_union(s0, s4):
    """s0+s4-s0*s4 = s0+s4*(1-s0) is nonnegative on the unit square."""
    one_minus_s0 = add(constant(1), s0, -1)
    return add(s0, multiply(s4, one_minus_s0))


def j9_kernel(q0, s0, q4, s4):
    difference = add(multiply(q0, s4), multiply(q4, s0), -1)
    result = sum_polynomials(
        square(difference),
        multiply(power(q0, 2), multiply(q4, power(s4, 2))),
        multiply(q0, multiply(power(q4, 2), power(s0, 2))),
        scale(multiply(multiply(q0, q4), multiply(power(s0, 2), s4)), 2),
        scale(multiply(multiply(q0, q4), multiply(s0, power(s4, 2))), 2),
        multiply(add(q0, q4), multiply(power(s0, 2), power(s4, 2))),
    )
    assert len(result) == 9
    assert digest(result) == "1faf37bc7ee7887ae3f82da800a22775b1e3ddcb81b8efcfe4dcd3d9e51f7723"
    return result


def m0_certificate(m0, q0, s0, q4, s4):
    quotient = divide_polynomial(m0, q4)
    assert m0 == multiply(q4, quotient)
    assert len(quotient) == 36

    atoms = (
        weighted_square(
            multiply(power(q0, 3), power(s4, 2)),
            multiply(s0, q4),
            s4,
        ),
        weighted_square(
            multiply(power(q0, 3), power(s4, 2)),
            multiply(s0, s4),
            q4,
        ),
        weighted_square(
            multiply(multiply(q0, s0), q4),
            multiply(q0, s4),
            multiply(s0, q4),
            2,
        ),
        weighted_square(
            multiply(multiply(q0, q4), power(s4, 3)),
            q0,
            power(s0, 2),
            2,
        ),
        weighted_square(
            multiply(power(s0, 2), q4),
            multiply(q0, s4),
            multiply(s0, q4),
            2,
        ),
        weighted_square(
            multiply(power(s0, 2), power(s4, 2)),
            multiply(q0, s4),
            multiply(s0, q4),
            2,
        ),
    )
    residual = quotient
    for atom in atoms:
        residual = add(residual, atom, -1)
    assert len(residual) == 23
    record = positive_residual_record(residual)
    assert record["minimum"] == "1"
    return {
        "factor": "q4",
        "quotient_terms": len(quotient),
        "weighted_binomial_squares": len(atoms),
        "positive_residual": record,
        "sha256": digest(m0),
    }


def m1_certificate(m1, q0, s0, q4, s4):
    union = bounded_union(s0, s4)
    difference = add(multiply(q0, s4), multiply(q4, s0), -1)
    first_factor = sum_polynomials(
        multiply(multiply(q0, q4), union),
        multiply(q0, power(s4, 2)),
        multiply(q4, power(s0, 2)),
        multiply(power(s0, 2), power(s4, 2)),
    )
    second_factor = divide_polynomial(m1, first_factor)
    assert m1 == multiply(first_factor, second_factor)
    assert len(first_factor) == 6 and len(second_factor) == 13

    residual = add(
        add(second_factor, scale(square(difference), 2), -1),
        multiply(multiply(q0, power(q4, 2)), union),
        -1,
    )
    assert len(residual) == 8
    record = positive_residual_record(residual)
    assert record["minimum"] == "1"
    return {
        "factorization": "M1=A*K",
        "A_terms": len(first_factor),
        "A_nonnegative_pieces": 4,
        "K_terms": len(second_factor),
        "K_square_pieces": 1,
        "K_bounded_union_pieces": 1,
        "K_positive_residual": record,
        "A_sha256": digest(first_factor),
        "K_sha256": digest(second_factor),
        "sha256": digest(m1),
    }


def h23_certificate(h23, q0, s0, q4, s4):
    c = variable(0)
    h0 = coefficient(h23, 0, 0)
    h1 = coefficient(h23, 0, 1)
    assert h23 == add(h0, multiply(c, h1))
    difference = add(multiply(q0, s4), multiply(q4, s0), -1)

    h0_residual = add(h0, multiply(q4, square(difference)), -1)
    assert len(h0_residual) == 8
    h0_record = positive_residual_record(h0_residual)

    s_difference = add(s0, s4, -1)
    two_minus_s4 = add(constant(2), s4, -1)
    h1_pieces = (
        square(difference),
        multiply(multiply(q0, power(q4, 2)), square(s_difference)),
        multiply(
            multiply(multiply(q0, power(q4, 2)), s4),
            two_minus_s4,
        ),
    )
    h1_residual = h1
    for piece in h1_pieces:
        h1_residual = add(h1_residual, piece, -1)
    assert len(h1_residual) == 8
    h1_record = positive_residual_record(h1_residual)
    assert h0_record["minimum"] == h1_record["minimum"] == "1"
    return {
        "split": "H23=H0+c*H1",
        "H0_terms": len(h0),
        "H0_square_pieces": 1,
        "H0_positive_residual": h0_record,
        "H1_terms": len(h1),
        "H1_square_pieces": 2,
        "H1_bounded_pieces": 1,
        "H1_positive_residual": h1_record,
        "H0_sha256": digest(h0),
        "H1_sha256": digest(h1),
        "sha256": digest(h23),
    }


def tau_certificate(h1971):
    c, q0, s0, q4, s4 = (
        variable(slot) for slot in (0, 1, 2, 5, 6)
    )
    _, _, determinant_sum = positive_route_data(1)
    transformed = bernstein_transform(h1971, [T])
    betas = [coefficient(transformed, T, index) for index in range(4)]

    k30 = divide_polynomial(betas[0], power(determinant_sum, 3))
    assert betas[0] == multiply(power(determinant_sum, 3), k30)
    k30_bernstein = positive_bernstein(k30, [2, 6])
    assert len(k30) == 30 and len(k30_bernstein) == 130
    assert min(k30_bernstein.values()) == Fraction(1, 18)

    m88 = scale(
        divide_polynomial(
            divide_polynomial(betas[1], c),
            power(determinant_sum, 2),
        ),
        3,
    )
    assert betas[1] == scale(
        multiply(multiply(c, power(determinant_sum, 2)), m88),
        Fraction(1, 3),
    )
    m0 = coefficient(m88, 0, 0)
    m1 = coefficient(m88, 0, 1)
    assert m88 == add(m0, multiply(c, m1))
    assert len(m88) == 88 and len(m0) == 36 and len(m1) == 52

    j9 = j9_kernel(q0, s0, q4, s4)
    beta2_divisor = multiply(multiply(power(c, 2), determinant_sum), j9)
    h23 = scale(divide_polynomial(betas[2], beta2_divisor), 3)
    assert betas[2] == scale(multiply(beta2_divisor, h23), Fraction(1, 3))
    assert len(h23) == 23

    beta3_expected = multiply(
        multiply(multiply(q4, add(c, q4)), power(c, 3)),
        power(j9, 2),
    )
    assert betas[3] == beta3_expected
    return {
        "degree": 3,
        "bernstein_rows": [row(beta) for beta in betas],
        "beta0": {
            "factorization": "B^3*K30",
            "K30_terms": len(k30),
            "K30_bernstein_nonzero": len(k30_bernstein),
            "K30_bernstein_minimum": str(min(k30_bernstein.values())),
            "K30_sha256": digest(k30),
        },
        "beta1": {
            "factorization": "c*B^2*(M0+c*M1)/3",
            "M88_terms": len(m88),
            "M0": m0_certificate(m0, q0, s0, q4, s4),
            "M1": m1_certificate(m1, q0, s0, q4, s4),
            "M88_sha256": digest(m88),
        },
        "beta2": {
            "factorization": "c^2*B*J9*H23/3",
            "J9_terms": len(j9),
            "J9_nonnegative_pieces": 6,
            "J9_sha256": digest(j9),
            "H23": h23_certificate(h23, q0, s0, q4, s4),
        },
        "beta3": {
            "factorization": "q4*(c+q4)*c^3*J9^2",
            "sha256": digest(betas[3]),
        },
        "sha256": digest(h1971),
    }


def representative_record(delta):
    cleared = cleared_polynomial(delta, "RLR", 1)
    factor = manifest_factor(1)
    core = divide_polynomial(cleared, factor)
    assert cleared == multiply(factor, core)
    assert len(cleared) == 2020 and len(core) == 766
    assert digest(cleared) == "af1e9287ee722808482ef7b3b7bbd0c6ef4a8d9e96b5408d8ae3c6add1ffe136"
    assert digest(core) == "a8e145fc062073f4adb21bd9da5112458ed329cc71547ef23537c879a203e035"

    gamma0, _, gamma2, determinant = gram(core, 4)
    gamma0_certificate = quadratic_certificate(gamma0, 6, [2, T])
    gamma2_certificate = quadratic_certificate(gamma2, 6, [2, T])
    assert gamma0_certificate["endpoint_bernstein_nonzero"] == [68, 145]
    assert gamma0_certificate["endpoint_minimum"] == ["1/6", "1/12"]
    assert gamma0_certificate["determinant_terms"] == 743
    assert gamma0_certificate["determinant_common_monomial"] == [2, 0, 4, 0, 0, 3, 0, 0]
    assert gamma0_certificate["determinant_bernstein_nonzero"] == 933
    assert gamma0_certificate["determinant_minimum"] == "1/8"
    assert gamma2_certificate["endpoint_bernstein_nonzero"] == [127, 299]
    assert gamma2_certificate["endpoint_minimum"] == ["1/6", "1/6"]
    assert gamma2_certificate["determinant_terms"] == 1607
    assert gamma2_certificate["determinant_common_monomial"] == [0, 0, 2, 0, 0, 1, 0, 0]
    assert gamma2_certificate["determinant_bernstein_nonzero"] == 2397
    assert gamma2_certificate["determinant_minimum"] == "1/30"

    common = common_monomial(determinant)
    assert common == (1, 0, 2, 0, 0, 1, 0, 0)
    determinant_residual = divide_monomial(determinant, common)
    q0, s0 = variable(1), variable(2)
    _, _, determinant_sum = positive_route_data(1)
    positive_factor = multiply(power(add(q0, s0), 2), determinant_sum)
    h1971 = divide_polynomial(determinant_residual, positive_factor)
    assert determinant_residual == multiply(positive_factor, h1971)
    assert len(determinant) == 5939 and len(h1971) == 1971
    assert digest(h1971) == "24a5d325d1719eb7f5492a18bf2151ceb68edf09a1211dbcfbab7409aa630300"
    return {
        "cleared_terms": len(cleared),
        "manifest_factor": "c*(1-s3)*(1-s4)",
        "core_terms": len(core),
        "outer_variable": "s3",
        "outer_endpoint_s4_grams": [gamma0_certificate, gamma2_certificate],
        "outer_determinant_terms": len(determinant),
        "outer_determinant_common_monomial": list(common),
        "outer_determinant_positive_factor": "(q0+s0)^2*B",
        "outer_determinant_core_terms": len(h1971),
        "tau_certificate": tau_certificate(h1971),
        "cleared_sha256": digest(cleared),
        "core_sha256": digest(core),
        "outer_determinant_sha256": digest(determinant),
    }, cleared


def main():
    delta, forest_count, connected_count = build_delta()
    record, q3_rlr = representative_record(delta)

    q3_lrl = cleared_polynomial(delta, "LRL", 1)
    assert q3_lrl == q3_rlr
    q4_rrl = cleared_polynomial(delta, "RRL", 2)
    q4_llr = cleared_polynomial(delta, "LLR", 2)
    assert q4_rrl == permute_parameter_pages(q3_rlr)
    assert q4_llr == permute_parameter_pages(q3_lrl)

    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-nonshared-opposite-side-gram.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "domain": "q3<0 or q4<0 is the sole negative diagonal route quantity, K>0, the negative page has one negative activity, and the two nonshared negative activities lie on opposite hub sides",
        "representative": "q3:RLR",
        "symmetry_closure": {
            "q3:RLR": ["q3:RLR", "q3:LRL", "q4:RRL", "q4:LLR"],
        },
        "certified_chambers": ["q3:LRL", "q3:RLR", "q4:LLR", "q4:RRL"],
        "certified_count": 4,
        "record": record,
        "conclusion": "Delta_b>=0 in all four listed opposite-side negative-nonshared-page chambers",
        "scope": "adds two q3-negative chambers and their two exact q4 page-swap images; 18 negative-page orientations remain open, so the generic sign and OPG-1757 are not claimed",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
