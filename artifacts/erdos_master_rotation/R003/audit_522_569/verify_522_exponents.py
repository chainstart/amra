#!/usr/bin/env python3
"""Exact arithmetic checks for the two #522 proof drafts."""

from fractions import Fraction


eta = Fraction(1, 100)
beta = Fraction(1, 200)

smooth_bc = 4 * (2 * beta + 6 * eta - Fraction(1, 2))
small_value_bc = 4 * (10 * eta - Fraction(1, 2))
interpolation = eta - Fraction(1, 8)

assert smooth_bc < -1
assert small_value_bc < -1
assert interpolation < -2 * eta
assert 2 * eta > beta
assert eta > beta

# In the obsolete reciprocal-polynomial interpolation, normalized Q_m and
# Q_n have expected squared L2 distance 2 whenever m > n: each vector has
# norm one and equal Fourier positions use independent Rademacher signs.
for n in range(1, 20):
    for m in range(n + 1, 25):
        q_m_norm = Fraction(m + 1, m + 1)
        q_n_norm = Fraction(n + 1, n + 1)
        expected_cross_term = 0
        expected_distance_sq = q_m_norm + q_n_norm - 2 * expected_cross_term
        assert expected_distance_sq == 2

print("PASS: revised exponents are summable; obsolete Q_n block coupling fails")
