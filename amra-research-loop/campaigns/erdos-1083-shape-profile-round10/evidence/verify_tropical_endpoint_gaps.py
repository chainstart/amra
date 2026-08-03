#!/usr/bin/env python3
"""Bounded guards for the tropical endpoint-gap shape theorem."""

from fractions import Fraction
from itertools import combinations


def minkowski(a, b):
    return {x + y for x in a for y in b}


def stats(a):
    ordered = sorted(a)
    assert len(ordered) >= 2
    return (
        ordered[-1] - ordered[0],
        ordered[1] - ordered[0],
        ordered[-1] - ordered[-2],
    )


def scaled(lam, a):
    return {lam * x for x in a}


def main():
    checks = 0
    universe = tuple(Fraction(n) for n in range(-3, 6))
    supports = [set(c) for size in (2, 3, 4)
                for c in combinations(universe, size)]

    # Exhaustive positive-support sum/min/min law on 246^2 pairs.
    for a in supports:
        wa, la, ra = stats(a)
        for b in supports:
            wb, lb, rb = stats(b)
            w, left, right = stats(minkowski(a, b))
            assert (w, left, right) == (wa + wb, min(la, lb), min(ra, rb))
            checks += 1

    # Both signs and zero/nonzero endpoint anchors.
    cases = [
        {Fraction(0), Fraction(2), Fraction(5), Fraction(9)},
        {Fraction(2), Fraction(4), Fraction(7), Fraction(11)},
        {Fraction(-9), Fraction(-5), Fraction(-2), Fraction(0)},
        {Fraction(-11), Fraction(-7), Fraction(-4), Fraction(-2)},
    ]
    magnitudes = [Fraction(n) for n in (1, 3, 7, 11)]
    for x in cases:
        D, ell, rr = stats(x)
        for sign in (1, -1):
            normalized = set()
            raw_left = []
            raw_right = []
            for mag in magnitudes:
                w, left, right = stats(scaled(sign * mag, x))
                normalized.add((left / w, right / w))
                raw_left.append(left)
                raw_right.append(right)
                expected = (ell / D, rr / D) if sign > 0 else (rr / D, ell / D)
                assert (left / w, right / w) == expected
                checks += 1
            assert len(normalized) == 1
            assert len(set(raw_left)) == len(magnitudes)
            assert len(set(raw_right)) == len(magnitudes)

    # Abstract exact censor: simultaneous feasibility leaves at most one
    # equality-wall row across both endpoints.
    lambdas = [Fraction(n) for n in (5, 8, 13, 21, 34)]
    c_left, c_right = Fraction(2), Fraction(3)
    # Formal thresholds are 3 and 5.  Actual rows have lambda>=5, so the
    # smaller left equality is infeasible and only right equality remains.
    L, R = c_left * Fraction(3), c_right * Fraction(5)
    eq_left = {j for j, lam in enumerate(lambdas) if c_left * lam == L}
    eq_right = {j for j, lam in enumerate(lambdas) if c_right * lam == R}
    assert len(eq_left) == 0 and len(eq_right) == 1
    core = set(range(len(lambdas))) - eq_left - eq_right
    assert len(core) == len(lambdas) - 1
    for j in core:
        f_left, f_right = c_left * lambdas[j], c_right * lambdas[j]
        assert f_left > L and f_right > R
        a_left, a_right = L, R
        assert min(a_left, f_left) == L
        assert min(a_right, f_right) == R
        checks += 1

    # Equal thresholds select the same unique scalar row at both endpoints.
    L2, R2 = c_left * Fraction(8), c_right * Fraction(8)
    both = {j for j, lam in enumerate(lambdas)
            if c_left * lam == L2 or c_right * lam == R2}
    assert len(both) == 1

    # Higher-layer coordinatewise-min failure.
    a, b = {Fraction(0), Fraction(2), Fraction(100)}, {Fraction(0), Fraction(3), Fraction(100)}
    assert sorted(minkowski(a, b))[:4] == [0, 2, 3, 5]
    checks += 1

    print("PASS tropical-endpoint-gap-shape")
    print(f"checks={checks} support_pairs={len(supports) ** 2} branches={len(cases) * 2}")


if __name__ == "__main__":
    main()
