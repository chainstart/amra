#!/usr/bin/env python3
"""Exact counterexample to universal scalar-copy coprimality."""

import json
import sympy as sp


def main() -> None:
    x = sp.symbols("x")
    aperiodic = 1 + x + x**3 + x**5 + x**6
    # M=20 makes the two summand supports disjoint, so source is a 0/1 mask.
    source = sp.expand(aperiodic * (1 + x**20))
    coefficients = sp.Poly(source, x).all_coeffs()
    gcd = sp.monic(sp.gcd(source, source.subs(x, x**3)))
    assert all(coefficient in (0, 1) for coefficient in coefficients)
    assert sp.rem(source, aperiodic, domain=sp.ZZ) == 0
    assert gcd != 1
    assert sp.rem(gcd, 1 + x**20, domain=sp.ZZ) == 0
    print(json.dumps({
        "schema": "amra.erdos1083.scalar-copy-gcd-counterexample.v1",
        "evidence_level": 3,
        "source_mask": str(source),
        "source_support_size": int(sum(coefficients)),
        "contains_aperiodic_factor": str(aperiodic),
        "scales": [1, 3],
        "gcd": str(gcd),
        "shared_factor": "x**20 + 1",
        "refutes": "universal pairwise coprimality for non-cyclotomic 0/1 sources",
        "leaves_open": "irreducible sources and source-specific Galois criteria",
        "public_exponent_changed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
