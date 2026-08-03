#!/usr/bin/env python3
"""Blind direct-orbit and arithmetic audit of all-j first-wall recovery.

This checker is standard-library-only and imports no round-8 author code.
The accompanying note supplies the universal monotonicity and induction
arguments; bounded raw replays are guards, not finite extrapolation.
"""

from math import comb


def C(a, k):
    return comb(a, k) if a >= k >= 0 else 0


def canonical(value, rank):
    assert value >= 0 and rank >= 1
    rem = value
    ceiling = None
    out = []
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
    assert all(out[i][0] > out[i + 1][0] for i in range(len(out) - 1))
    return tuple(out)


def upper(word):
    return sum(C(a, k + 1) for a, k in word)


def q_of(j):
    assert j >= 1 and j % 2 == 1
    h = 112 * 2 ** (j - 1)
    assert (2 * h + 4) % 3 == 0
    return (2 * h + 4) // 3


def constants(last):
    A, B = {4: 25}, {4: 58}
    for n in range(4, last):
        A[n + 1] = C(A[n], 2) - (20 * n - 49)
        B[n + 1] = C(B[n], 2) - (20 * n - 52)
    return A, B


def raw_first_recovery(j, max_rank=40):
    q = q_of(j)
    h = 112 * 2 ** (j - 1)
    b = q + 4
    tau = 4 * q - 2
    x = C(h + b - 2, 3) + C(b - 1, 2) + 2 - 2 * h
    y = C(h + b - 1, 3) + C(b, 2) + 2 - 2 * h
    for rank in range(3, max_rank + 1):
        wx, wy = canonical(x, rank), canonical(y, rank)
        ux, uy = upper(wx), upper(wy)
        gamma = uy - ux - x - tau
        if gamma >= 0:
            return rank, gamma
        x, y = ux - tau + 1, uy - tau
        assert x >= 0 and y >= 0
    raise AssertionError("recovery guard too short")


def main():
    # Exact small actual bases excluded from the stable m>=6 argument.
    bases = {j: raw_first_recovery(j) for j in (1, 3, 5)}

    A, B = constants(16)
    assert A[6] == 35995 and B[6] == 1319452
    assert B[6] >= 30 * A[6]
    for n in range(6, 15):
        assert B[n] >= 30 * A[n]
        assert A[n] > A[n - 1]
        # Exact induction margin after replacing B_n by 30 A_n.
        margin = (
            C(30 * A[n], 2) - (20 * n - 52)
            - 30 * (C(A[n], 2) - (20 * n - 49))
        )
        assert margin == 435 * A[n] ** 2 + 580 * n - 1418 > 0

    # Independently verify monotonicity of the fixed-rank Macaulay raise on
    # a dense finite guard.  The note proves it universally by greedy carry.
    for rank in range(2, 9):
        previous = -1
        for value in range(3000):
            raised = upper(canonical(value, rank))
            assert raised >= previous
            previous = raised

    # Raw finite guard across several scalar regimes.  For j>=7 compare the
    # first recovery with the first predicted B wall; recovery is at or before
    # that wall, exactly as the universal proof states.
    A_long, B_long = constants(16)
    records = []
    for j in range(7, 108, 2):
        q = q_of(j)
        wall = next(m for m in range(6, 16)
                    if B_long[m] >= q - (5 * m - 16))
        recovery, gamma = raw_first_recovery(j)
        assert recovery <= wall
        records.append((j, recovery, wall, gamma > 0))

    # Both strict estimates used by the minimum-wall proof are numerically
    # guarded at every negative-predecessor wall in the sample.
    for j, recovery, wall, _ in records:
        q = q_of(j)
        if recovery == wall and wall >= 6:
            t = q - (5 * wall - 16)
            assert t > q // 2
            assert A_long[wall] + 1 < FractionLike(q, 6)
            lower = C(t, 2) - C(A_long[wall] + 1, 2) + 2 - 4 * q
            assert lower > 0

    print("PASS independent all-j first-wall recovery guards")
    print(f"bases={bases}")
    print(f"raw_members={len(records)} first={records[:5]} last={records[-3:]}")
    print("ratio_induction=B>=30A; strict_bounds=A+1<q/6,t>q/2")


class FractionLike:
    """Tiny exact comparison helper for integer < numerator/denominator."""

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __gt__(self, integer):
        return self.numerator > integer * self.denominator


if __name__ == "__main__":
    main()
