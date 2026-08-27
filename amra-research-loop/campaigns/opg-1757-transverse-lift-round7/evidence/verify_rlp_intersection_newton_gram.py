#!/usr/bin/env python3
"""Exact Newton-Gram face at the second q0-chart RLP intersection corner."""

from __future__ import annotations

from fractions import Fraction
import json

from verify_mixed_three_negative import divide_polynomial
from verify_negative_c_direct_chambers import (
    add,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_page_direct_chambers import digest
from verify_negative_q0_no_positive_gram import coefficient
from verify_rlp_projective_corner_reduction import (
    polynomial_sum,
    product,
    reconstruct_h1884,
    reverse_slot,
    scale,
    small_direction_faces,
    square,
)


def substitute_one(poly, slot):
    result = {}
    for monomial, value in poly.items():
        transformed = list(monomial)
        transformed[slot] = 0
        key = tuple(transformed)
        result[key] = result.get(key, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def row(poly):
    return {
        "terms": len(poly),
        "sha256": digest(poly),
        "negative_power_coefficients": sum(value < 0 for value in poly.values()),
    }


def build_record():
    normalized = small_direction_faces(reconstruct_h1884()[0])[1]
    # y=1 is the common boundary x=B*v*t between the root chart and its
    # complementary affine-fill chart.  Reverse a=1-A so slot one stores A.
    intersection = substitute_one(normalized, 0)
    corner = reverse_slot(intersection, 1)
    route_degrees = [monomial[1] + monomial[5] for monomial in corner]
    assert (min(route_degrees), max(route_degrees)) == (4, 9)
    face = {
        monomial: value
        for monomial, value in corner.items()
        if monomial[1] + monomial[5] == 4
    }

    one = constant(1)
    A, B, v, t = (variable(slot) for slot in (1, 5, 6, 7))
    L = polynomial_sum(A, product(A, t, v), product(B, t, v))
    H = divide_polynomial(face, L)
    assert face == multiply(L, H)
    assert max(monomial[2] for monomial in H) == 2
    h0, h1, h2 = (coefficient(H, 2, degree) for degree in range(3))

    S = polynomial_sum(
        A,
        scale(multiply(A, v), -1),
        product(A, v, v),
        scale(product(A, t, v), 2),
        product(A, t, t, v),
        product(B, t, t, v),
        product(B, t, v, v),
    )
    expected_h0 = product(add(A, B), square(S))
    assert h0 == expected_h0

    determinant = add(
        multiply(h0, h2),
        multiply(h1, h1),
        Fraction(-1, 4),
    )
    expected_determinant = product(
        A,
        B,
        power(add(one, v, -1), 2),
        polynomial_sum(A, multiply(A, v), multiply(B, v)),
        L,
        square(S),
    )
    assert determinant == expected_determinant

    assert (len(intersection), len(corner), len(face), len(L), len(H)) == (
        3618, 1743, 201, 3, 114,
    )
    assert digest(face) == (
        "0ad452d374428b4c5459c6c2bc57f8a5a1d5cab087b432b66da9a79a874d3f14"
    )
    assert digest(H) == (
        "58b699ccc0771b5753205d03bb33a4c46dd435c27c11c88498c6066bed0569a5"
    )
    assert [len(h0), len(h1), len(h2)] == [40, 38, 36]
    assert [digest(h0), digest(h1), digest(h2)] == [
        "f38c32211bda9d68f3c39da3367eff182542014184f4dff9bd63c51dbe127806",
        "8cf496ad26d1af1fc369ec818bb2b6acf7e43b882819529065bea032482cee14",
        "8cd0c3062fe0c0ac1def9e7cfd630cf8393529ce22a18ed8cf9366a9cd097c15",
    ]
    assert len(determinant) == 133
    assert digest(determinant) == (
        "52f300e7b61f833d7e08b29c78fb68d54ea07b47fdda1d71b92c64b948abbb19"
    )

    return {
        "schema": "amra.opg1757.round7.rlp-intersection-newton-gram.v1",
        "domain": "the q0-maximal small-direction normalized form on y=1 (x=B*v*t), with 0<=A,B,z,v,t<=1",
        "coordinates": "A=1-a; the second corner is A=B=0",
        "intersection": row(intersection),
        "corner": {
            "terms": len(corner),
            "sha256": digest(corner),
            "AB_total_degree_range": [4, 9],
        },
        "degree_four_face": {
            **row(face),
            "factorization": "L*H(z)",
            "L": "A*(1+t*v)+B*t*v",
            "L_sha256": digest(L),
            "H": row(H),
        },
        "quadratic_gram": {
            "H": "h0+h1*z+h2*z^2",
            "rows": [row(h0), row(h1), row(h2)],
            "S": "A*(1-v+v^2+2*t*v+t^2*v)+B*t*v*(t+v)",
            "S_sha256": digest(S),
            "h0": "(A+B)*S^2",
            "determinant": "A*B*(1-v)^2*(A*(1+v)+B*v)*L*S^2",
            "determinant_record": row(determinant),
            "sign": "the 2x2 monomial Gram of H is positive semidefinite on the closed box, by the displayed h0 and determinant identities plus continuity on h0=0",
        },
        "conclusion": "the common degree-four Newton face at A=B=0 is nonnegative for every real z",
        "coverage_change": 0,
        "remaining_negative_page_chambers": 18,
        "scope": "this certifies the Newton principal only; higher AB-degree terms, the full q3:RLP chamber, the generic Delta_b sign, and OPG-1757 remain open",
    }


def main():
    print(json.dumps(build_record(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
