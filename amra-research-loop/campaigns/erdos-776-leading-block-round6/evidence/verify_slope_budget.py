#!/usr/bin/env python3
"""Exact arithmetic guards for the affine slope-budget lemma."""
from fractions import Fraction


def upper(alpha, delta, beta, v, c, q):
    return (alpha + delta - 3) * q + beta + v + 2 - c


def actual_qs(q0=300, count=8):
    out = []
    q = q0
    for _ in range(count):
        out.append(q)
        q = 4 * q - 4
    return out


def main():
    # Subcritical rational budgets become strictly decreasing on actual q.
    cases = [
        (Fraction(0), Fraction(0), 20, 0, 9),
        (Fraction(2), Fraction(0), 1000, -7, 11),
        (Fraction(1, 2), Fraction(9, 4), 50, 3, 4),
    ]
    qs = actual_qs(count=12)
    for alpha, delta, beta, v, c in cases:
        assert alpha + delta < 3
        vals = [upper(alpha, delta, beta, v, c, q) for q in qs]
        assert all(y < x for x, y in zip(vals, vals[1:]))
        assert vals[-1] < 0

    # Equality has zero q-slope and its sign is not determined.
    assert upper(Fraction(1), Fraction(2), 10, 0, 1, qs[0]) == 11
    assert upper(Fraction(3), Fraction(0), -20, 0, 1, qs[0]) == -19

    # Original interface has alpha=delta=0 and coefficient -3 after
    # combining canonical continuation with the -4q surplus term.
    assert upper(Fraction(0), Fraction(0), 20, 0, 9, 301) == -890
    print("affine leading/bottom slope budget: PASS")


if __name__ == "__main__":
    main()
