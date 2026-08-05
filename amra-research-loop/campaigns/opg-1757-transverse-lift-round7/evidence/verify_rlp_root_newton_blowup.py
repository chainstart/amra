#!/usr/bin/env python3
"""Exact root coordinate and weighted Newton face in the compact RLP chart."""

from __future__ import annotations

from fractions import Fraction
import json

from verify_mixed_three_negative import divide_polynomial, polynomial_square_root
from verify_negative_c_direct_chambers import (
    add,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_page_direct_chambers import digest
from verify_negative_q0_no_positive_gram import (
    coefficient,
    common_monomial,
    divide_monomial,
    scale,
)
from verify_rlp_projective_corner_reduction import (
    compactify_scale,
    polynomial_sum,
    product,
    projective_chart,
    reconstruct_h1884,
    square,
)


def cleared_substitute(poly, slot, numerator, denominator, degree):
    """Substitute numerator/denominator and clear denominator**degree."""
    result = {}
    for monomial, value in poly.items():
        exponent = monomial[slot]
        reduced = list(monomial)
        reduced[slot] = 0
        term = {tuple(reduced): value}
        term = multiply(term, power(numerator, exponent))
        term = multiply(term, power(denominator, degree - exponent))
        result = add(result, term)
    return result


def weighted_blowup(poly):
    """Apply B=b**2, w=b**3*y and remove the common b**6."""
    result = {}
    for monomial, value in poly.items():
        weighted_degree = 2 * monomial[5] + 3 * monomial[2]
        assert weighted_degree >= 6
        transformed = list(monomial)
        transformed[5] = weighted_degree - 6
        key = tuple(transformed)
        result[key] = result.get(key, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def evaluate(poly, values):
    result = Fraction()
    for monomial, coefficient_value in poly.items():
        term = coefficient_value
        for value, exponent in zip(values, monomial):
            term *= value**exponent
        result += term
    return result


def row(poly):
    return {
        "terms": len(poly),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
        "negative_power_coefficients": sum(value < 0 for value in poly.values()),
        "sha256": digest(poly),
    }


def build_record():
    h1884, reconstruction = reconstruct_h1884()
    compact = compactify_scale(projective_chart(h1884, 1))

    one = constant(1)
    u, A, w, B, v, tau = (variable(slot) for slot in (0, 1, 2, 5, 6, 7))
    one_minus_u = add(one, u, -1)
    one_minus_v = add(one, v, -1)
    one_minus_tau = add(one, tau, -1)
    D = multiply(one_minus_tau, one_minus_u)
    E = product(B, u, add(tau, v, -1), one_minus_v)

    support = {(monomial[5], monomial[2]) for monomial in compact}
    pareto = {
        pair
        for pair in support
        if not any(
            other != pair
            and other[0] <= pair[0]
            and other[1] <= pair[1]
            for other in support
        )
    }
    assert pareto == {(0, 2), (1, 1), (2, 0)}
    face = {
        monomial: value
        for monomial, value in compact.items()
        if (monomial[5], monomial[2]) in pareto
    }
    expected_face = product(
        power(A, 4),
        power(u, 2),
        one_minus_tau,
        power(one_minus_u, 3),
        square(add(multiply(D, w), E)),
    )
    assert face == expected_face

    root = cleared_substitute(compact, 2, add(w, E, -1), D, 4)
    rows = [coefficient(root, 2, degree) for degree in range(5)]
    assert len(root) == 30669
    assert digest(root) == (
        "8e782abd4b9d1572aca1b88c8c333f72389fe35efb859b99086ac1c22eb17429"
    )
    assert [len(entry) for entry in rows] == [12128, 8858, 5725, 3034, 924]
    assert [digest(entry) for entry in rows] == [
        "11900e848284dacb5e4908cc66a0c4c4bdc6470343a2a83dc440d0d53178bb17",
        "f5bc6fd6ddb1716adde4909fe262bb4e7a9bf51243c4609941fb5f169e605edb",
        "120fbfc181cdd243fff460cdfc1abf61b01a65011facef6b06596bd85fee8d66",
        "39a576e47c32c634890770222f5f13acb689bee1dac34d2649e07685633f27d5",
        "0adf3137cce4304e02578ae1d4f016e363cbb60ce4f9d0082dd46282060af240",
    ]
    row_common = [common_monomial(entry) for entry in rows]
    assert row_common == [
        (4, 0, 0, 0, 0, 3, 0, 0),
        (3, 0, 0, 0, 0, 2, 0, 0),
        (2, 0, 0, 0, 0, 0, 0, 0),
        (1, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0),
    ]

    C = polynomial_sum(
        product(A, B, add(one, multiply(tau, u), -1)),
        product(add(A, B), one_minus_tau, one_minus_u),
    )
    r4_factor = product(add(A, B), C, power(one_minus_u, 2))
    F23 = polynomial_square_root(divide_polynomial(rows[4], r4_factor))
    H156 = divide_polynomial(
        scale(rows[3], Fraction(-1, 2)),
        product(C, power(one_minus_u, 2), F23),
    )
    assert rows[4] == product(r4_factor, square(F23))
    assert rows[3] == scale(
        product(C, power(one_minus_u, 2), F23, H156), -2
    )
    assert (len(F23), len(H156)) == (23, 156)
    assert digest(F23) == (
        "f1f64d0a358a31d10eef25d04a87ce82520295a83d9fef59670e8dac11120b76"
    )
    assert digest(H156) == (
        "1a9d5ae91ffb250b5c42989c1f9e3be4890c1deda203b69d61136ec158d8e0a0"
    )

    K = add(
        multiply(add(A, B), rows[2]),
        product(C, power(one_minus_u, 2), square(H156)),
        -1,
    )
    assert common_monomial(K) == (2, 0, 0, 0, 0, 2, 0, 0)
    assert len(K) == 6633
    assert digest(K) == (
        "178a6bc7254d330169f4793b381d36fb6948216122dc935f4f78dcaf07daac22"
    )

    weighted = weighted_blowup(root)
    weighted_pairs = {
        (monomial[5], monomial[2])
        for monomial in root
        if 2 * monomial[5] + 3 * monomial[2] == 6
    }
    assert weighted_pairs == {(3, 0), (0, 2)}
    principal = coefficient(weighted, 5, 0)
    expected_principal = product(
        power(A, 3),
        power(u, 2),
        power(one_minus_tau, 5),
        power(one_minus_u, 7),
        polynomial_sum(
            product(
                power(u, 2),
                power(v, 2),
                one_minus_tau,
                power(one_minus_v, 2),
            ),
            multiply(A, square(w)),
        ),
    )
    assert principal == expected_principal
    assert len(weighted) == 30669
    assert digest(weighted) == (
        "6e2ec0548499c6dbd73b41228e755013d4a026564ca97c9aedf837c01afbc872"
    )

    witness_values = [
        Fraction(11, 16),
        Fraction(7, 8),
        Fraction(),
        Fraction(),
        Fraction(),
        Fraction(7, 8),
        Fraction(7, 16),
        Fraction(1, 16),
    ]
    entries = [evaluate(entry, witness_values) for entry in rows]
    lower_minor = 4 * entries[2] * entries[4] - entries[3] ** 2
    gram_determinant = (
        entries[0] * entries[2] * entries[4]
        - entries[0] * entries[3] ** 2 / 4
        - entries[1] ** 2 * entries[4] / 4
    )
    assert lower_minor > 0 and gram_determinant < 0

    return {
        "schema": "amra.opg1757.round7.rlp-root-newton-blowup.v1",
        "domain": "q3:RLP, q0-maximal projective compact chart; 0<=u,A,s0,B,v,tau<=1",
        "coordinates": {
            "D": "(1-tau)*(1-u)",
            "E": "B*u*(tau-v)*(1-v)",
            "root": "w=D*s0+E",
            "weighted_blowup": "B=b^2, w=b^3*y, followed by division by b^6",
        },
        "reconstruction": reconstruction,
        "compact_chart": row(compact),
        "first_newton_face": {
            **row(face),
            "pareto_B_s0": [[0, 2], [1, 1], [2, 0]],
            "identity": "A^4*u^2*(1-tau)*(1-u)^3*((1-tau)*(1-u)*s0+B*u*(tau-v)*(1-v))^2",
        },
        "root_quartic": {
            **row(root),
            "row_terms": [len(entry) for entry in rows],
            "row_common_monomials": [list(entry) for entry in row_common],
            "C": "A*B*(1-tau*u)+(A+B)*(1-tau)*(1-u)",
            "C_record": row(C),
            "r4": "(A+B)*C*(1-u)^2*F23^2",
            "r3": "-2*C*(1-u)^2*F23*H156",
            "F23": row(F23),
            "H156": row(H156),
            "lower_minor_core": row(K),
        },
        "weighted_newton_face": {
            **row(principal),
            "weighted_support": [[3, 0], [0, 2]],
            "identity": "A^3*u^2*(1-tau)^5*(1-u)^7*(u^2*v^2*(1-tau)*(1-v)^2+A*y^2)",
            "blown_up_polynomial": row(weighted),
        },
        "gram_kill_test": {
            "parameters_u_A_B_v_tau": ["11/16", "7/8", "7/8", "7/16", "1/16"],
            "lower_2x2_minor_positive": True,
            "full_tridiagonal_determinant_negative": True,
            "interpretation": "the displayed tridiagonal Gram is not globally PSD; this rejects that sufficient certificate only and is not a negative value of the quartic on its admissible w interval",
        },
        "conclusion": "the internal B=s0 root curve and its B^3-versus-w^2 intersection have exact manifestly nonnegative Newton principals",
        "coverage_change": 0,
        "remaining_negative_page_chambers": 18,
        "scope": "the higher weighted orders are not certified; q3:RLP, the generic Delta_b sign, the marked-host theorem, and OPG-1757 remain open",
    }


def main():
    print(json.dumps(build_record(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
