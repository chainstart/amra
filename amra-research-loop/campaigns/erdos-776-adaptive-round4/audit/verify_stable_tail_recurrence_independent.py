#!/usr/bin/env python3
"""Independent finite-prefix check of the K4,r9 stable-tail recurrence.

The raw orbit is reconstructed from the original h,b,n,H,x,y formulas.  The
stable words and A/B recurrences below are then checked against greedy
Macaulay expansion; they are not imported from the author checker.
"""

from math import comb


def C(n, k):
    return comb(n, k) if n >= k >= 0 else 0


def canonical(value, rank):
    rem, ceiling, out = value, None, []
    for lower in range(rank, 0, -1):
        if rem == 0:
            break
        lo = lower - 1
        hi = ceiling if ceiling is not None else max(2, lower + 1)
        if ceiling is None:
            while C(hi, lower) <= rem:
                hi *= 2
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if C(mid, lower) <= rem:
                lo = mid
            else:
                hi = mid
        if lo >= lower:
            out.append((lo, lower))
            rem -= C(lo, lower)
            ceiling = lo
    assert rem == 0
    return tuple(out)


def upper_word(word):
    return sum(C(top, lower + 1) for top, lower in word)


def q_of(j):
    assert j >= 3 and j % 2 == 1
    h = 112 * 2 ** (j - 1)
    assert (2 * h + 4) % 3 == 0
    return (2 * h + 4) // 3


def constants(last):
    A = {4: 25}
    B = {4: 58}
    for n in range(4, last):
        A[n + 1] = C(A[n], 2) - (20 * n - 49)
        B[n + 1] = C(B[n], 2) - (20 * n - 52)
    return A, B


def expected_words(n, q, h, A, B):
    b = q + 4
    x = [(h + b - 2, n), (q - 1, n - 1)]
    y = [(h + b - 1, n), (q, n - 1)]
    x.extend((q - (5 * i + 1), n - 1 - i) for i in range(1, n - 3))
    y.extend((q - 5 * i, n - 1 - i) for i in range(1, n - 3))
    x.extend(((q - 5 * (n - 3), 2), (A[n], 1)))
    y.extend(((q - (5 * (n - 3) - 1), 2), (B[n], 1)))
    return tuple(x), tuple(y)


def first_odd_j_above(bound):
    j = max(3, bound.bit_length())
    if j % 2 == 0:
        j += 1
    while q_of(j) <= bound:
        j += 2
    return j


def main():
    # Large enough to exercise several squaring steps while remaining a cheap
    # independent raw-orbit test under the campaign memory cap.
    R = 12
    A, B = constants(R + 1)
    bounds = []
    for n in range(4, R + 2):
        bounds.extend((A[n] + 5 * (n - 3), B[n] + 5 * (n - 3) - 1))
    for n in range(4, R + 1):
        constant = B[n + 1] - A[n + 1] - A[n] - 1
        bounds.append(max(0, constant // 4 + 1))
    j = first_odd_j_above(max(bounds))
    q = q_of(j)
    h = 112 * 2 ** (j - 1)
    b = q + 4
    N = C(q, 2) + 9
    H = C(b, 2) + 1
    tau = H - N
    assert tau == 4 * q - 2
    x = C(h + b - 2, 3) + C(b - 1, 2) + 2 - 2 * h
    y = C(h + b - 1, 3) + C(b, 2) + 2 - 2 * h

    checked = []
    early_gammas = {}
    for rank in range(3, R + 2):
        xword, yword = canonical(x, rank), canonical(y, rank)
        ux, uy = upper_word(xword), upper_word(yword)
        gamma = uy - ux - x - tau
        if rank < 4:
            early_gammas[rank] = gamma
        else:
            expected_x, expected_y = expected_words(rank, q, h, A, B)
            assert xword == expected_x
            assert yword == expected_y
            if rank <= R:
                predicted = B[rank + 1] - A[rank + 1] - A[rank] - 1 - 4 * q
                assert gamma == predicted < 0
                checked.append(rank)
        x, y = ux - tau + 1, uy - tau
        assert x >= 0 and y >= 0

    # The original low ranks are also negative for this actual member.
    assert all(value < 0 for value in early_gammas.values())
    print("PASS: raw stable-tail recurrence finite-prefix audit")
    print(f"checked actual odd j={j}, ranks 3..{R}")
    print(f"stable words/recurrences checked at ranks {checked[0]}..{checked[-1] + 1}")
    print("all tested surpluses through R are negative; all next states are nonnegative")
    print(f"q bit length={q.bit_length()}, A_(R+1) bit length={A[R+1].bit_length()}")


if __name__ == "__main__":
    main()
