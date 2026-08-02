#!/usr/bin/env python3
"""Independent finite scratch guard for a second scalar copy of P.

This file deliberately imports none of the author verifiers.  It uses exact
polynomial arithmetic in SymPy and reports only finite searches plus the exact
factor classification of the one fixed common mask M.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product
import json
from math import gcd

import sympy as sp


x = sp.symbols("x")
P = 1 + x + x**3 + x**5 + x**6
Q = 1 - x**5 + x**8 + x**10 - x**13 + x**18
M = sp.expand(P * Q)


def is_mask(poly: sp.Expr) -> bool:
    coefficients = sp.Poly(poly, x, domain=sp.ZZ).as_dict().values()
    return all(value == 1 for value in coefficients)


def scaled_p(scale: int) -> sp.Poly:
    return sp.Poly(P.subs(x, x**scale), x, domain=sp.QQ)


def same_q_product(r: int, s: int) -> dict[int, int]:
    p_support = (0, 1, 3, 5, 6)
    q_terms = ((0, 1), (5, -1), (8, 1), (10, 1), (13, -1), (18, 1))
    answer: defaultdict[int, int] = defaultdict(int)
    for a in p_support:
        for b, coefficient in q_terms:
            answer[r * a + s * b] += coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def main() -> None:
    expected_factors = (
        P,
        x**8 + 1,
        x**2 - x + 1,
        x**8 + x**7 - x**5 - x**4 - x**3 + x + 1,
    )
    assert sp.expand(sp.prod(expected_factors)) == M
    assert all(sp.Poly(f, x, domain=sp.QQ).is_irreducible for f in expected_factors)
    assert len({sp.Poly(f, x).monic().as_expr() for f in expected_factors}) == 4
    assert [int(f.subs(x, 1)) for f in expected_factors] == [5, 2, 1, 1]

    augmentation_five_divisors: list[tuple[tuple[int, ...], sp.Expr, bool]] = []
    for bits in product((0, 1), repeat=4):
        divisor = sp.expand(sp.prod(f for bit, f in zip(bits, expected_factors) if bit))
        if divisor.subs(x, 1) == 5:
            augmentation_five_divisors.append((bits, divisor, is_mask(divisor)))
    assert len(augmentation_five_divisors) == 4
    mask_divisors = [divisor for _, divisor, mask in augmentation_five_divisors if mask]
    assert mask_divisors == [P]

    primitive_unordered = []
    nonconstant_gcds = []
    for r in range(1, 101):
        for s in range(r + 1, 101):
            if gcd(r, s) != 1:
                continue
            primitive_unordered.append((r, s))
            common = sp.gcd(scaled_p(r), scaled_p(s))
            if common.degree() > 0:
                nonconstant_gcds.append((r, s, common.as_expr()))
    assert len(primitive_unordered) == 3043
    assert nonconstant_gcds == []

    # If two such coprime five-term factors divide an integral common mask,
    # their product divides it.  Evaluation at one would force 25 | 5C.
    augmentation_obstructions = {C: (5 * C) % 25 for C in range(1, 5)}
    assert all(remainder != 0 for remainder in augmentation_obstructions.values())

    direct_pairs = []
    direct_hits = []
    for r in range(1, 25):
        for s in range(1, 25):
            if r == s or gcd(r, s) != 1:
                continue
            direct_pairs.append((r, s))
            numerator = sp.Poly(M.subs(x, x**s), x, domain=sp.QQ)
            denominator = scaled_p(r)
            quotient, remainder = sp.div(numerator, denominator, domain=sp.QQ)
            if remainder.is_zero:
                direct_hits.append((r, s, quotient.as_expr()))
    assert len(direct_pairs) == 358
    assert direct_hits == []

    same_q_pairs = 0
    same_q_hits = []
    for r in range(1, 201):
        for s in range(1, 201):
            if gcd(r, s) != 1:
                continue
            same_q_pairs += 1
            coefficients = same_q_product(r, s).values()
            if all(value == 1 for value in coefficients):
                same_q_hits.append((r, s))
    assert same_q_pairs == 24463
    assert same_q_hits == [(1, 1)]

    # P is reciprocal, so changing only the sign of a scalar gives an
    # associate rather than an independent divisor.
    assert sp.expand(x**6 * P.subs(x, x**-1)) == P

    print(
        json.dumps(
            {
                "schema": "amra.erdos1083.second-scalar-scratch.v1",
                "pass": True,
                "fixed_M_augmentation_five_divisors": 4,
                "fixed_M_mask_divisors": 1,
                "primitive_unordered_ratio_pairs_le_100": 3043,
                "nonconstant_gcds": 0,
                "direct_fixed_M_ordered_pairs_le_24": 358,
                "direct_fixed_M_nontrivial_divisibility_hits": 0,
                "same_Q_ordered_pairs_le_200": 24463,
                "same_Q_mask_hits": [[1, 1]],
                "original_problem_proved": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
