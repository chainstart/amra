#!/usr/bin/env python3
"""Bounded guards for the interval shape-to-distance interface no-go."""

from fractions import Fraction
from math import factorial, log


def gaps(values):
    x = sorted(values)
    return x[1] - x[0], x[-1] - x[-2], x[-1] - x[0]


def parameters(L):
    M = 2 * factorial(L) ** 2
    S = M + 1
    U = S * M
    return M, S, U


def complement(S, U, d):
    return {r + d * S * k for r in range(d) for k in range(U // d)}


def main():
    checks = 0

    # All-L arithmetic identities and scale firewall.
    for L in range(1, 13):
        M, S, U = parameters(L)
        assert U < S * S
        for e in range(1, L + 1):
            d = S * e
            assert U % d == 0
            assert e * e < M
            assert e < U // d
            assert d * d == d * S * e
            checks += 1
        if L >= 3:
            assert log(U) > L

    # Exhaust one nontrivial exact instance without materializing U*S pairs:
    # unique quotient/remainder decoding checks every n in V.
    L = 3
    M, S, U = parameters(L)
    X = set(range(S))
    profile = None
    scalars = []
    for e in range(1, L + 1):
        d = S * e
        A = complement(S, U, d)
        assert len(A) == U
        assert d * d in A
        for n in range(S * U):
            r = n % d
            h = (n - r) // d
            x = h % S
            k = h // S
            assert 0 <= r < d and 0 <= x < S and 0 <= k < U // d
            assert n == (r + d * S * k) + d * x
        left, right, width = gaps(A)
        source = {d * x for x in X}
        sl, sr, sw = gaps(source)
        theta = (Fraction(sl, sw), Fraction(sr, sw), left, right)
        assert theta == (Fraction(1, S - 1), Fraction(1, S - 1), 1, 1)
        profile = theta if profile is None else profile
        assert theta == profile
        scalars.append(d)
        checks += S * U + 1

    # Common positive tangent and exact label set.
    rho2 = Fraction(1, 4)
    R0 = max(d * d for d in scalars) + 1
    tau0 = R0 - rho2
    assert tau0 > 0
    for d in scalars:
        A = complement(S, U, d)
        T = {Fraction(R0 + a) - rho2 - d * d for a in A}
        assert min(T) > 0 and tau0 in T
        checks += 2
    distances = {(d - e) ** 2 for i, d in enumerate(scalars) for e in scalars[i + 1:]}
    assert distances == {S * S * h * h for h in range(1, L)}
    assert len(distances) == L - 1 and len({profile}) == 1

    print("PASS shape-distance-interface-no-go")
    print(f"checks={checks} exhaustive_L=3 rows={L} labels={len(distances)} profile_range=1")


if __name__ == "__main__":
    main()
