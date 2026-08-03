#!/usr/bin/env python3
"""Exact all-base q-fibre and resultant ledger (standard library only)."""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations
import json
from math import prod

from verify_transverse_expansion import reconstruct


ZERO = (0,) * 7


def add(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
    return {monomial: value for monomial, value in result.items() if value}


def multiply(left, right):
    result = {}
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            monomial = tuple(
                left_degree + right_degree
                for left_degree, right_degree in zip(left_monomial, right_monomial)
            )
            result[monomial] = result.get(monomial, 0) + left_value * right_value
    return {monomial: value for monomial, value in result.items() if value}


def scale(poly, scalar):
    return {monomial: scalar * value for monomial, value in poly.items() if scalar * value}


def q_coefficients(poly):
    coefficients = [{}, {}, {}]
    for monomial, value in poly.items():
        q_degree = monomial[7]
        assert q_degree <= 2
        base_monomial = monomial[:7]
        coefficients[q_degree][base_monomial] = (
            coefficients[q_degree].get(base_monomial, 0) + value
        )
    return [
        {monomial: value for monomial, value in coefficient.items() if value}
        for coefficient in coefficients
    ]


def restrict_zero(poly, variable_index):
    return {
        monomial: value
        for monomial, value in poly.items()
        if monomial[variable_index] == 0
    }


def monomial(**degrees):
    names = "abcdeuv"
    exponent = [0] * len(names)
    for name, degree in degrees.items():
        exponent[names.index(name)] = degree
    return tuple(exponent)


def canonical(poly):
    return json.dumps(
        [[list(monomial), coefficient] for monomial, coefficient in sorted(poly.items())],
        separators=(",", ":"),
    )


def digest(poly):
    return sha256(canonical(poly).encode()).hexdigest()


def evaluate(poly, values):
    return sum(
        coefficient
        * prod(value ** degree for value, degree in zip(values, monomial))
        for monomial, coefficient in poly.items()
    )


def determinant(matrix):
    size = len(matrix)
    result = {}
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        term = {ZERO: -1 if inversions % 2 else 1}
        for row, column in enumerate(permutation):
            term = multiply(term, matrix[row][column])
        result = add(result, term)
    return result


def main():
    deletion, connectivity, forest_count, connected_count = reconstruct()
    assert (forest_count, connected_count) == (128, 58)
    p0, p1, p2 = q_coefficients(deletion)
    x0, x1, x2 = q_coefficients(connectivity)

    expected_p1 = {
        monomial(c=1, u=1, v=2): 2,
        monomial(c=1, d=1, u=1): -4,
        monomial(c=1, d=2, u=1): -2,
    }
    expected_x1 = {
        monomial(a=2, c=1, v=1): 2,
        monomial(c=1, d=1, u=1): -4,
        monomial(c=1, u=2, v=1): -2,
    }
    assert p1 == expected_p1
    assert x1 == expected_x1

    one_plus_b = {ZERO: 1, monomial(b=1): 1}
    x2_inner = {
        monomial(a=1, c=1, d=1): 1,
        monomial(a=1, c=1): 1,
        monomial(a=1, d=1): 2,
        monomial(c=1, d=1): 1,
        monomial(c=1, u=1, v=1): 1,
    }
    assert x2 == scale(multiply(one_plus_b, x2_inner), -2)

    # P2 also has an exact -(b+1) factor.  Extract its 24-term quotient by
    # comparing the b^0 and b^1 slices; no symbolic factorizer is trusted.
    p2_b0, p2_b1 = {}, {}
    for exponent, value in p2.items():
        reduced = exponent[:1] + (0,) + exponent[2:]
        if exponent[1] == 0:
            p2_b0[reduced] = value
        elif exponent[1] == 1:
            p2_b1[reduced] = value
        else:
            raise AssertionError("P2 has unexpected b degree")
    assert p2_b0 == p2_b1
    p2_inner = scale(p2_b0, -1)
    assert p2 == scale(multiply(one_plus_b, p2_inner), -1)
    assert evaluate(p2, (1, 1, 1, 1, 1, 0, 0)) == -48

    # For P=p2*q^2+p1*q+p0 and X=x2*q^2+x1*q+x0, the quadratic
    # resultant admits the compact Bezout form D0^2-D1*D2.  Verify it
    # independently against the 4-by-4 Sylvester determinant.
    d0 = add(multiply(p2, x0), multiply(x2, p0), -1)
    d1 = add(multiply(p2, x1), multiply(x2, p1), -1)
    d2 = add(multiply(p1, x0), multiply(x1, p0), -1)
    resultant = add(multiply(d0, d0), multiply(d1, d2), -1)
    empty = {}
    sylvester = [
        [p2, p1, p0, empty],
        [empty, p2, p1, p0],
        [x2, x1, x0, empty],
        [empty, x2, x1, x0],
    ]
    assert determinant(sylvester) == resultant

    # On c=0 both linear q coefficients vanish, so the resultant is D0^2.
    # The remaining common-wall factor collapses to an 18-term product.
    a2_minus_u2 = {
        monomial(a=2): 1,
        monomial(u=2): -1,
    }
    v_wall = {
        monomial(v=2): 1,
        monomial(d=2): -1,
        monomial(d=1): -2,
    }
    expected_c_wall_d0 = scale(
        multiply(
            multiply(
                {monomial(d=1, e=1): 1},
                multiply(a2_minus_u2, a2_minus_u2),
            ),
            multiply(one_plus_b, v_wall),
        ),
        4,
    )
    c_wall_d0 = restrict_zero(d0, 2)
    assert c_wall_d0 == expected_c_wall_d0

    records = {
        "P0": p0,
        "P1": p1,
        "P2": p2,
        "xi0": x0,
        "xi1": x1,
        "xi2": x2,
        "P2_inner": p2_inner,
        "D0": d0,
        "D1": d1,
        "D2": d2,
        "D0_at_c_zero": c_wall_d0,
        "resultant": resultant,
    }
    print(json.dumps({
        "schema": "amra.opg1757.round7.q-fibre-ledger.v1",
        "q_linear_factors": {
            "P1": "2*c*u*(v^2-d^2-2*d)",
            "xi1": "2*c*(v*(a^2-u^2)-2*d*u)",
        },
        "q_quadratic_factors": {
            "P2": "-(b+1)*H_P2, with H_P2 recorded by hash",
            "xi2": "-2*(b+1)*(a*c*d+a*c+2*a*d+c*d+c*u*v)",
            "partial_14_partial_24_P_at_anchor": 48,
        },
        "records": {
            name: {
                "terms": len(poly),
                "total_degree": max(map(sum, poly)) if poly else -1,
                "sha256": digest(poly),
            }
            for name, poly in records.items()
        },
        "resultant_identity": "Res_q(P,xi)=D0^2-D1*D2",
        "c_zero_wall": "D0=4*d*e*(a^2-u^2)^2*(b+1)*(v^2-d^2-2*d)",
        "scope": "exact coefficient and wall-contact ledger only; no projected-component sign classification",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
