#!/usr/bin/env python3
"""Exact guards for SECOND_SCALAR_FINAL_SCRATCH.md (not an unbounded proof)."""

from math import gcd
import json

import sympy as sp
from sympy.polys.numberfields import galois_group


x, y = sp.symbols("x y")
P = 1 + x + x**3 + x**5 + x**6
f = y**3 + y**2 - 3 * y - 1


def main() -> None:
    assert sp.expand(x**3 * f.subs(y, x + x**-1)) == P
    assert sp.Poly(f, y, domain=sp.QQ).is_irreducible
    assert sp.discriminant(f, y) == 148
    assert f.subs(y, -3) < 0 < f.subs(y, -2)
    assert f.subs(y, sp.Rational(-1, 2)) > 0 > f.subs(y, 0)
    assert f.subs(y, 1) < 0 < f.subs(y, 2)
    assert sp.expand((-f.subs(y, 2)) * (-f.subs(y, -2))) == 5
    assert sp.expand(x**6 * P.subs(x, x**-1)) == P
    group, _ = galois_group(P, x)
    assert group.order() == 48

    checked = 0
    for r in range(1, 61):
        for s in range(r + 1, 61):
            if gcd(r, s) != 1:
                continue
            checked += 1
            left = sp.Poly(P.subs(x, x**r), x, domain=sp.QQ)
            right = sp.Poly(P.subs(x, x**s), x, domain=sp.QQ)
            assert sp.gcd(left, right).degree() == 0

    print(
        json.dumps(
            {
                "schema": "amra.erdos1083.second-scalar-global-structure.v1",
                "pass": True,
                "galois_group_order": 48,
                "primitive_unordered_gcd_guards_le_60": checked,
                "unbounded_claim_computational_only": False,
                "original_problem_proved": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
