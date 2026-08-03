#!/usr/bin/env python3
"""Bounded guards for the exact positive-product profile interface."""

from fractions import Fraction
from itertools import product


def minkowski(a, b):
    return {x + y for x in a for y in b}


def four_profile(lam, X, phi0, alpha0, v):
    phi = min(lam * x for x in X)
    alpha = v - phi
    return (phi, phi0, alpha, alpha0)


def main():
    finite_checks = 0

    # Positive-mask least support is additive under Minkowski product.
    sets = [
        {Fraction(0), Fraction(2)},
        {Fraction(-3), Fraction(1), Fraction(4)},
        {Fraction(1, 2), Fraction(7, 2)},
    ]
    for A, B in product(sets, repeat=2):
        assert min(minkowski(A, B)) == min(A) + min(B)
        finite_checks += 1

    phi0, alpha0, v = Fraction(5), Fraction(9), Fraction(37)

    # Positive-sign zero anchor: literal profile range one.
    X_zero = {Fraction(0), Fraction(2), Fraction(5)}
    positive = [Fraction(n) for n in (1, 3, 7, 11, 19)]
    profiles_zero = [four_profile(lam, X_zero, phi0, alpha0, v) for lam in positive]
    assert len(set(profiles_zero)) == 1
    finite_checks += len(positive)

    # Positive-sign nonzero anchor: literal profile injective.
    X_nonzero = {Fraction(2), Fraction(5), Fraction(9)}
    profiles_pos = [four_profile(lam, X_nonzero, phi0, alpha0, v) for lam in positive]
    assert len(set(profiles_pos)) == len(positive)
    finite_checks += len(positive)

    # Negative-sign natural-order formula uses max X and is injective here.
    negative = [-lam for lam in positive]
    profiles_neg = [four_profile(lam, X_zero, phi0, alpha0, v) for lam in negative]
    assert len(set(profiles_neg)) == len(negative)
    for lam, p in zip(negative, profiles_neg):
        assert p[0] == lam * max(X_zero)
        finite_checks += 1

    # Exact graph/fibre and residual identities, including repeated scalars.
    lambdas = [Fraction(2), Fraction(2), Fraction(3), Fraction(8)]
    ps = [four_profile(lam, X_nonzero, phi0, alpha0, v) for lam in lambdas]
    phis = [p[0] for p in ps]
    assert len(set(ps)) == len(set(phis))
    for p in ps:
        phi, _, alpha, _ = p
        assert alpha + phi == v
        assert alpha + phi - v == 0
        finite_checks += 1
    for phi in set(phis):
        assert sum(p[0] == phi for p in ps) == sum(p == (phi, phi0, v - phi, alpha0) for p in ps)
        finite_checks += 1

    print("PASS exact-positive-product-profile")
    print(f"finite_checks={finite_checks} zero_range=1 nonzero_range={len(set(profiles_pos))}")


if __name__ == "__main__":
    main()
