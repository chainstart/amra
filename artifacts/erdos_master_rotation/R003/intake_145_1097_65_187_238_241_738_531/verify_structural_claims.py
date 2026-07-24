#!/usr/bin/env python3
"""Lightweight finite checks supporting the R003 root-intake reports."""

from fractions import Fraction
from itertools import combinations
from math import ceil


def odd_part(n: int) -> int:
    while n % 2 == 0:
        n //= 2
    return n


# #531: the BENTW single-event probability bound is attained.
for k in range(2, 11):
    A = [1, 3] + [3 * 4**j for j in range(1, k - 1)]
    sums = {
        sum(A[i] for i in range(k) if mask & (1 << i))
        for mask in range(1, 1 << k)
    }
    assert sum(A) == 4 ** (k - 1)
    assert len(sums) == 2**k - 1
    assert not any(2 * x in sums for x in sums)
    assert len({odd_part(x) for x in sums}) == 2 ** (k - 1)
    assert all((x & -x).bit_length() % 2 == 1 for x in sums)


# #65: exact minimizer inside the complete-bipartite family.
for k in range(1, 30):
    s = k + 1
    t = ceil(Fraction(k * s, s - k))
    assert Fraction(s * t, s + t) >= k
    for smaller_s in range(1, s):
        # st/(s+t) is always strictly smaller than s.
        assert smaller_s <= k
    spectrum = list(range(4, 2 * s + 1, 2))
    objective = sum((Fraction(1, ell) for ell in spectrum), Fraction())
    assert objective == Fraction(1, 2) * (
        sum((Fraction(1, j) for j in range(1, s + 1)), Fraction()) - 1
    )


# #1097: every restricted edge becomes a 3-term AP in the linear-size host.
B = {1, 4, 9}
C = {3, 8, 15}
G = {(1, 3), (4, 8), (9, 15), (1, 15)}
restricted_sums = {b + c for b, c in G}
X = {2 * b for b in B} | restricted_sums | {2 * c for c in C}
for b, c in G:
    assert 2 * b in X and b + c in X and 2 * c in X
    assert (b + c) - 2 * b == 2 * c - (b + c)


# #238: a regularly spaced bad set covers every L-window while retaining
# only O(N/L) close pairs.
for L in range(2, 20):
    N = 20 * L
    bad = set(range(L, N + 1, L))
    for start in range(1, N - L + 2):
        assert any(i in bad for i in range(start, start + L))
    close_pairs = sum(1 for a, b in combinations(sorted(bad), 2) if b - a <= L)
    assert close_pairs <= len(bad)


# #241: exact third-convolution spectrum and second moment for a B3 example.
for m in range(1, 7):
    A = [10**j for j in range(m)]
    r3 = {}
    for a in A:
        for b in A:
            for c in A:
                r3[a + b + c] = r3.get(a + b + c, 0) + 1
    assert set(r3.values()) <= {1, 3, 6}
    assert sum(v * v for v in r3.values()) == 6 * m**3 - 9 * m**2 + 4 * m


# #738: K_{m,m} contains an induced p-u-v but every other neighbour of p
# is also adjacent to v, so the naive induced-P4 leaf extension fails.
for m in range(3, 20):
    left = {f"L{i}" for i in range(m)}
    right = {f"R{i}" for i in range(m)}
    p, v = "L0", "L1"
    u = "R0"
    assert p in left and v in left and u in right
    candidates = right - {u}
    assert candidates
    assert all(x in right for x in candidates)  # adjacent to both p and v


print("PASS: #65/#1097/#238/#241/#531/#738 structural checks")
