#!/usr/bin/env python3
"""Blind direct-orbit audit of the actual K4,r9 budget-three switch.

Standard-library only.  This file does not import either round-7 author
verifier.  It reconstructs the original integer orbit and greedy Macaulay
words from their definitions.
"""

from math import comb


def C(a, k):
    return comb(a, k) if a >= k >= 0 else 0


def canonical(value, rank):
    assert value >= 0 and rank >= 1
    remainder = value
    ceiling = None
    out = []
    for k in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = k - 1
        if ceiling is None:
            hi = k + 1
            while C(hi, k) <= remainder:
                hi *= 2
        else:
            hi = ceiling
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if C(mid, k) <= remainder:
                lo = mid
            else:
                hi = mid
        if lo >= k:
            out.append((lo, k))
            remainder -= C(lo, k)
            ceiling = lo
    assert remainder == 0
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


def stable_word(q, rank, bottom, side):
    H = 5 * q // 2
    if side == "x":
        word = [(H, rank), (q - 1, rank - 1)]
        word.extend((q - (1 + 5 * i), rank - 1 - i)
                    for i in range(1, rank - 3))
        word.extend(((q - (5 * rank - 15), 2), (bottom, 1)))
    else:
        word = [(H + 1, rank), (q, rank - 1)]
        word.extend((q - 5 * i, rank - 1 - i)
                    for i in range(1, rank - 3))
        word.extend(((q - (5 * rank - 16), 2), (bottom, 1)))
    return tuple(word)


def main():
    j = 1231
    q = q_of(j)
    h = 112 * 2 ** (j - 1)
    b = q + 4
    H = 5 * q // 2
    tau = 4 * q - 2
    A, B = constants(13)

    assert 2 * h == 3 * q - 4
    x = C(h + b - 2, 3) + C(b - 1, 2) + 2 - 2 * h
    y = C(h + b - 1, 3) + C(b, 2) + 2 - 2 * h
    assert canonical(x, 3) == ((H, 3), (q, 2), (9, 1))
    assert canonical(y, 3) == ((H + 1, 3), (q + 1, 2), (12, 1))

    gammas = {}
    words = {}
    for rank in range(3, 13):
        xword = canonical(x, rank)
        yword = canonical(y, rank)
        words[rank] = (xword, yword)
        if 4 <= rank <= 11:
            assert xword == stable_word(q, rank, A[rank], "x")
            assert yword == stable_word(q, rank, B[rank], "y")
        ux, uy = upper(xword), upper(yword)
        gammas[rank] = uy - ux - x - tau
        next_x, next_y = ux - tau + 1, uy - tau
        assert next_x >= 0 and next_y >= 0
        x, y = next_x, next_y

    # Rank 12: x remains in the inherited stable cell; y crosses exactly one
    # rank-two wall by three units while every higher digit stays unchanged.
    assert words[12][0] == stable_word(q, 12, A[12], "x")
    stable_y12 = stable_word(q, 12, B[12], "y")
    actual_y12 = words[12][1]
    t = q - (5 * 12 - 16)  # q-44
    assert stable_y12[-2:] == ((t, 2), (B[12], 1))
    assert 3 * t + 3 <= B[12] < 4 * t + 6
    residual = B[12] - 3 * t - 3
    expected_switched = stable_y12[:-2] + ((t + 3, 2), (residual, 1))
    assert actual_y12 == expected_switched
    assert 0 <= residual < t + 3
    assert actual_y12[-3][0] == t + 4 > actual_y12[-2][0] == t + 3

    # Exact Pascal transfer and round-six sign convention.
    residual_formula = C(B[11], 2) - 3 * q - (5 * 12 - 21)
    assert residual == residual_formula
    alpha, delta = 3, 0
    assert alpha + delta == 3

    # Actual surplus crosses zero on the identical orbit member.
    assert gammas[11] < 0 < gammas[12]

    # Complete one-wall classification.  Delta_s is the cost of moving the
    # rank-two top from t to t+s.  s=3 is exactly the stated half-open wall;
    # s=4 collides with the fixed preceding top t+4.
    def wall(s):
        return C(t + s, 2) - C(t, 2)

    assert wall(3) == 3 * t + 3
    assert wall(4) == 4 * t + 6
    assert wall(3) <= B[12] < wall(4)
    assert (t + 4) == actual_y12[-3][0]
    assert not (actual_y12[-3][0] > t + 4)  # s=4 violates strict order

    print("PASS independent actual budget-three switch")
    print(f"j={j} q_bits={q.bit_length()} residual_bits={residual.bit_length()}")
    print(f"gamma11_sign={gammas[11] < 0} gamma12_sign={gammas[12] > 0}")
    print("shift=3 alpha=3 delta=0; s=3 iff [3t+3,4t+6); s=4 collision")


if __name__ == "__main__":
    main()
