#!/usr/bin/env python3
"""Bounded exact guards for the gauge-invariant width profile theorem."""

from fractions import Fraction
from itertools import product


def endpoints(values):
    return min(values), max(values)


def width(values):
    lo, hi = endpoints(values)
    return hi - lo


def minkowski(a, b):
    return {x + y for x in a for y in b}


def scaled(lam, x):
    return {lam * value for value in x}


def profile(lam, x, lam0, total_width):
    d = width(scaled(lam, x))
    d0 = width(scaled(lam0, x))
    return d, d0, total_width - d, total_width - d0


def main():
    checks = 0
    masks = [
        {Fraction(0), Fraction(2)},
        {Fraction(-3), Fraction(1), Fraction(4)},
        {Fraction(1, 2), Fraction(7, 2)},
    ]

    # Width classifies endpoint pairs modulo diagonal translation.
    pairs = [(Fraction(-2), Fraction(5)), (Fraction(3), Fraction(10))]
    assert pairs[0][1] - pairs[0][0] == pairs[1][1] - pairs[1][0]
    c = pairs[1][0] - pairs[0][0]
    assert (pairs[0][0] + c, pairs[0][1] + c) == pairs[1]
    checks += 2

    # Both endpoints, hence widths, add under positive Minkowski product.
    for a, b in product(masks, repeat=2):
        lo, hi = endpoints(minkowski(a, b))
        alo, ahi = endpoints(a)
        blo, bhi = endpoints(b)
        assert (lo, hi) == (alo + blo, ahi + bhi)
        assert width(minkowski(a, b)) == width(a) + width(b)
        checks += 2

    positive = [Fraction(n) for n in (1, 3, 7, 11, 19)]
    negative = [-x for x in positive]
    lam0 = Fraction(13)
    total_width = Fraction(100)

    cases = [
        ({Fraction(0), Fraction(2), Fraction(5)}, positive, "positive-zero"),
        ({Fraction(2), Fraction(5), Fraction(9)}, positive, "positive-nonzero"),
        ({Fraction(-5), Fraction(-2), Fraction(0)}, negative, "negative-zero"),
        ({Fraction(-9), Fraction(-5), Fraction(-2)}, negative, "negative-nonzero"),
    ]

    for x, lambdas, label in cases:
        d = width(x)
        profiles = [profile(lam, x, lam0, total_width) for lam in lambdas]
        phis = [min(scaled(lam, x)) for lam in lambdas]
        widths = [width(scaled(lam, x)) for lam in lambdas]
        assert all(w == abs(lam) * d for lam, w in zip(lambdas, widths))
        assert len(set(profiles)) == len(lambdas)
        assert len(set(widths)) == len(lambdas)
        if label in {"positive-zero", "negative-zero"}:
            assert len(set(phis)) == 1
        else:
            assert len(set(phis)) == len(lambdas)
        for lam, p in zip(lambdas, profiles):
            dj = abs(lam) * d
            d0 = abs(lam0) * d
            assert p == (dj, d0, total_width - dj, total_width - d0)
            assert (p[0] - dj, p[2] + dj - total_width,
                    p[1] - d0, p[3] + d0 - total_width) == (0, 0, 0, 0)
            checks += 4

    print("PASS gauge-invariant-width-profile")
    print(f"exact_checks={checks} branches={len(cases)}")


if __name__ == "__main__":
    main()
