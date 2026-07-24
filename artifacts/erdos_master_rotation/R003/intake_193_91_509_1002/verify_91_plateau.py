#!/usr/bin/env python3
"""Finite and symbolic checks supporting the plateau audit for #91."""

from math import comb


# OEIS A186704, n=1,...,13.  This is used only as a small-data sanity check,
# never as evidence for an asymptotic assertion.
f = [None, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6]
plateaux = {}
for n in range(1, 14):
    plateaux.setdefault(f[n], []).append(n)
assert plateaux == {
    0: [1],
    1: [2, 3],
    2: [4, 5],
    3: [6, 7],
    4: [8, 9],
    5: [10, 11, 12],
    6: [13],
}


# The counting lemma in the public May 2026 comment uses
# C(N,3)>2N(N-1), which is equivalent to N>14.
for n_points in range(15, 501):
    assert comb(n_points, 3) > 2 * n_points * (n_points - 1)
assert comb(14, 3) == 2 * 14 * 13


# A monotone integer o(n) sequence can nevertheless have arbitrarily long
# runs of strict increases.  Thus sublinearity alone cannot give bounded-gap
# plateaux.  Mark increments in [2^(2k), 2^(2k)+k-1].
limit = 2**24


def countermodel(n: int) -> int:
    return sum(
        max(0, min(k, n - 2 ** (2 * k) + 1))
        for k in range(1, 13)
    )


for k in range(1, 13):
    start = 2 ** (2 * k)
    assert all(
        countermodel(n + 1) == countermodel(n) + 1
        for n in range(start - 1, start + k - 1)
    )
assert countermodel(limit) <= 12 * 13 // 2
assert countermodel(limit) / limit < 5e-6

print("PASS #91: plateau counting threshold and sublinear countermodel")
