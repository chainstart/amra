#!/usr/bin/env python3
"""Reconstruct the compact q0-chart root and weighted Newton blow-up."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import random
import sys


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_mixed_three_negative import (  # noqa: E402
    divide_polynomial,
    polynomial_square_root,
)
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    coefficient,
    common_monomial,
    divide_monomial,
    scale,
)
from verify_rlp_projective_corner_reduction import (  # noqa: E402
    compactify_scale,
    polynomial_sum,
    product,
    projective_chart,
    reconstruct_h1884,
    square,
)


def cleared_substitute(poly, slot, numerator, denominator, degree):
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
        "sha256": digest(poly),
    }


def main():
    compact = compactify_scale(projective_chart(reconstruct_h1884()[0], 1))
    one = constant(1)
    u, A, w, B, v, tau = (variable(slot) for slot in (0, 1, 2, 5, 6, 7))
    one_minus_u = add(one, u, -1)
    one_minus_v = add(one, v, -1)
    one_minus_tau = add(one, tau, -1)
    D = multiply(one_minus_tau, one_minus_u)
    E = product(B, u, add(tau, v, -1), one_minus_v)

    face = {
        monomial: value
        for monomial, value in compact.items()
        if (monomial[5], monomial[2]) in ((0, 2), (1, 1), (2, 0))
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
    print("compact", row(compact), "face", row(face), flush=True)
    print("root", row(root), "rows", [len(entry) for entry in rows], flush=True)
    print("row common", [common_monomial(entry) for entry in rows], flush=True)

    C = polynomial_sum(
        product(A, B, add(one, multiply(tau, u), -1)),
        product(add(A, B), one_minus_tau, one_minus_u),
    )
    r4_factor = product(add(A, B), C, power(one_minus_u, 2))
    F = polynomial_square_root(divide_polynomial(rows[4], r4_factor))
    H = divide_polynomial(
        scale(rows[3], Fraction(-1, 2)),
        product(C, power(one_minus_u, 2), F),
    )
    assert rows[4] == product(r4_factor, square(F))
    assert rows[3] == scale(
        product(C, power(one_minus_u, 2), F, H), -2
    )
    print("C", row(C), "F", row(F), "H", row(H), flush=True)

    K = add(
        multiply(add(A, B), rows[2]),
        product(C, power(one_minus_u, 2), square(H)),
        -1,
    )
    K_common = common_monomial(K)
    Kbar = divide_monomial(K, K_common)
    print("K", row(K), K_common, "Kbar", row(Kbar), flush=True)

    blowup = weighted_blowup(root)
    principal = coefficient(blowup, 5, 0)
    expected_principal = product(
        power(A, 3),
        power(u, 2),
        power(one_minus_tau, 5),
        power(one_minus_u, 7),
        polynomial_sum(
            product(power(u, 2), power(v, 2), one_minus_tau, power(one_minus_v, 2)),
            multiply(A, square(w)),
        ),
    )
    assert principal == expected_principal
    print("blowup", row(blowup), "principal", row(principal), flush=True)

    # Find a small exact witness that the sufficient tridiagonal Gram is not
    # globally PSD.  This is not a witness against the quartic on its interval.
    rng = random.Random(1757)
    witness = None
    for _ in range(2000):
        values = [Fraction(rng.randrange(1, 16), 16) for _ in range(8)]
        values[2] = values[3] = values[4] = Fraction()
        entries = [evaluate(row_poly, values) for row_poly in rows]
        lower_minor = 4 * entries[2] * entries[4] - entries[3] ** 2
        determinant = (
            entries[0] * entries[2] * entries[4]
            - entries[0] * entries[3] ** 2 / 4
            - entries[1] ** 2 * entries[4] / 4
        )
        if lower_minor < 0 or determinant < 0:
            witness = (values, entries, lower_minor, determinant)
            break
    print("Gram negative witness", witness, flush=True)


if __name__ == "__main__":
    main()
