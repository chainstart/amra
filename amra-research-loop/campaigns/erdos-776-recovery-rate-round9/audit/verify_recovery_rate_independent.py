#!/usr/bin/env python3
"""Blind arithmetic audit of the explicit K4,r9 recovery-rank bound."""

from math import comb


def C(a, k):
    return comb(a, k) if a >= k >= 0 else 0


def constants(last):
    A, B = {4: 25}, {4: 58}
    for n in range(4, last):
        A[n + 1] = C(A[n], 2) - (20 * n - 49)
        B[n + 1] = C(B[n], 2) - (20 * n - 52)
    return A, B


def q_of(j):
    assert j >= 1 and j % 2 == 1
    numerator = 224 * (1 << (j - 1)) + 4
    assert numerator % 3 == 0
    return numerator // 3


def ceil_log2(n):
    assert n >= 1
    return (n - 1).bit_length()


def p_of(j):
    return 2 + ceil_log2(j + 4)


def canonical(value, rank):
    rem, ceiling, out = value, None, []
    for k in range(rank, 0, -1):
        if rem == 0:
            break
        lo = k - 1
        if ceiling is None:
            hi = k + 1
            while C(hi, k) <= rem:
                hi *= 2
        else:
            hi = ceiling
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if C(mid, k) <= rem:
                lo = mid
            else:
                hi = mid
        if lo >= k:
            out.append((lo, k))
            rem -= C(lo, k)
            ceiling = lo
    assert rem == 0
    return tuple(out)


def upper(word):
    return sum(C(a, k + 1) for a, k in word)


def first_recovery(j, max_rank=20):
    q = q_of(j)
    h, b, tax = 112 * 2 ** (j - 1), q + 4, 4 * q - 2
    x = C(h + b - 2, 3) + C(b - 1, 2) + 2 - 2 * h
    y = C(h + b - 1, 3) + C(b, 2) + 2 - 2 * h
    for rank in range(3, max_rank + 1):
        ux, uy = upper(canonical(x, rank)), upper(canonical(y, rank))
        gamma = uy - ux - x - tax
        if gamma >= 0:
            return rank
        x, y = ux - tax + 1, uy - tax
    raise AssertionError("finite raw guard too short")


def main():
    A, B = constants(19)
    assert B[5] == 1625 > 2 ** 10

    for n in range(5, 18):
        assert B[n] >= 20 * n
        # Exact taxed recurrence and monotonic quadratic lower bound.
        assert B[n + 1] == B[n] * B[n] // 2 - B[n] // 2 - (20 * n - 52)
        assert B[n + 1] >= B[n] * B[n] // 4
        exponent = 2 + 2 ** (n - 2)
        assert B[n] >= 2 ** exponent

    # Integer-only ceiling and exponent comparisons.  Do not materialize a
    # 100,000-bit q_j in every row: the exact q_j inequality is audited below
    # on a dense bounded prefix and sparse large witnesses.
    for j in range(1, 100002, 2):
        p = p_of(j)
        assert p >= 5
        assert (1 << (p - 2)) >= j + 4
        assert (1 << (p - 3)) < j + 4
        exponent_at_p = 2 + (1 << (p - 2))
        assert exponent_at_p >= j + 6

    # Exact arithmetic witnesses for q_j < 2^(j+6).  The general inequality
    # is the separately checked algebra 112*2^j+4 < 192*2^j.
    for j in list(range(1, 2002, 2)) + [10001, 100001, 1000001]:
        q = q_of(j)
        assert q < (1 << (j + 6))
        assert 112 * (1 << j) + 4 < 192 * (1 << j)

    # Independent raw orbit guard includes all three exact small bases.
    records = []
    for j in range(1, 202, 2):
        recovery = first_recovery(j)
        assert recovery <= p_of(j)
        records.append((j, recovery, p_of(j)))
    assert records[:3] == [(1, 4, 5), (3, 4, 5), (5, 5, 6)]

    # p(j) itself is unbounded; it is a memberwise upper bound, never a
    # uniform recovery rank.  Round four separately proves actual unboundedness.
    assert p_of((1 << 41) + 1) > 42

    print("PASS independent explicit recovery-rate audit")
    print(f"B5={B[5]} ceiling_rows=50001 raw_members={len(records)}")
    print(f"bases={records[:3]} last={records[-1]}")


if __name__ == "__main__":
    main()
