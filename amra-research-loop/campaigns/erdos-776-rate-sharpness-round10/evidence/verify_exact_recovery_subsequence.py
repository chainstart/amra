#!/usr/bin/env python3
"""Exact arithmetic guards for rho(j_R)=R+1."""

import json
from math import comb


def q_of(j):
    return (224 * (1 << (j - 1)) + 4) // 3


def main():
    A, B = 25, 58
    aa, bb = {4: A}, {4: B}
    for n in range(4, 21):
        A = comb(A, 2) - (20 * n - 49)
        B = comb(B, 2) - (20 * n - 52)
        aa[n + 1], bb[n + 1] = A, B

    rows = []
    for R in range(5, 18):
        E = 11 * 2 ** (R - 4)
        j = E - 5
        q = q_of(j)
        assert j % 2 == 1
        assert q > 2**E
        assert bb[R] < 2 ** (11 * 2 ** (R - 5))
        assert q > bb[R] ** 2 > bb[R] + 5 * R
        for n in range(4, R + 1):
            D = comb(bb[n], 2) - comb(aa[n] + 1, 2) + 2
            assert D < bb[n] ** 2 < q
        lower_next = 2 ** (2 + 2**R)
        assert bb[R + 2] >= lower_next
        assert q < 2 ** (E + 1)
        assert bb[R + 2] > 2048 * q
        Dnext = bb[R + 2] - aa[R + 2] - aa[R + 1] - 1
        assert Dnext > 4 * q
        assert 2 ** (R - 1) < E - 1 < 2**R
        p = 2 + (j + 3).bit_length()
        assert p == R + 2
        rows.append({"R": R, "j_bits": j.bit_length(), "j": j if j < 10**7 else None, "p": p})
    print(json.dumps({
        "schema":"amra.erdos776.round10.exact-rate-subsequence.v1",
        "verdict":"PASS",
        "subsequence":"j_R=11*2^(R-4)-5",
        "exact_first_recovery":"rho(j_R)=R+1",
        "round9_bound":"p(j_R)=R+2",
        "rows":rows,
        "scope_warning":"fixed K4,r9 sharp-rate subsequence only; no public promotion"
    },indent=2))


if __name__ == '__main__': main()
