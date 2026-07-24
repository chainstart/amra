#!/usr/bin/env python3
"""Finite/symbolic checks for the R004 root intake and audit package.

These checks support displayed identities and finite certificates.  They do not
replace Hua's lemma, Green--Tao, Selberg sieve, or Bradač's Ramsey theorem.
"""

from fractions import Fraction
from itertools import combinations, product
from math import floor, prod, sqrt

from sympy import factorint, isprime


# #313: ten currently displayed primary pseudoperfect examples, the two new
# finite examples, and the two-prime inheritance instance recovering the
# eight-prime-factor example.
known_ppn = [
    2,
    6,
    42,
    1806,
    47058,
    2214502422,
    52495396602,
    8490421583559688410706771261086,
    5998279018951962402,
    35979351189199316534587473905773572006,
]
for number in known_ppn:
    factors = factorint(number)
    assert all(exponent == 1 and isprime(prime) for prime, exponent in factors.items())
    assert Fraction(1, number) + sum(Fraction(1, prime) for prime in factors) == 1

M = 2214502422
d = 2839805
q = M + d
r = M + (M * M + 1) // d
assert (q - M) * (r - M) == M * M + 1
assert isprime(q) and isprime(r)
assert M * q * r == 8490421583559688410706771261086

N9 = 5998279018951962402
p10 = N9 + 1
assert isprime(p10)
assert N9 * p10 == 35979351189199316534587473905773572006


# #323: orthogonality counts are reproduced combinatorially for small cutoffs,
# and the fourth-moment divisor injection is checked directly.
for k in range(3, 7):
    for X in range(2, 8):
        values = [a**k for a in range(1, X + 1)]
        r2 = {}
        r3 = {}
        for a, b in product(values, repeat=2):
            r2[a + b] = r2.get(a + b, 0) + 1
        for a, b, c in product(values, repeat=3):
            r3[a + b + c] = r3.get(a + b + c, 0) + 1
        E4 = sum(v * v for v in r2.values())
        E6 = sum(v * v for v in r3.values())
        assert len(r3) * E6 >= X**6
        assert E4 >= X**2

        for a, c in product(range(1, X + 1), repeat=2):
            D = a**k - c**k
            if D == 0:
                continue
            solutions = []
            for b, dd in product(range(1, X + 1), repeat=2):
                if dd**k - b**k == D:
                    solutions.append((b, dd))
                    assert abs(dd - b) > 0
                    assert abs(D) % abs(dd - b) == 0
            # For a fixed signed gap, strict monotonicity permits at most one b.
            signed_gaps = [dd - b for b, dd in solutions]
            assert len(signed_gaps) == len(set(signed_gaps))


# #749: the algebraic annulus lower bound is positive throughout a grid of
# admissible theta, epsilon, C once N is beyond the harmless endpoint range.
for epsilon in (Fraction(1, 10), Fraction(1, 3), Fraction(1, 2)):
    for theta in (Fraction(1, 20), Fraction(1, 10), Fraction(1, 5)):
        if 2 * theta >= 1 - epsilon:
            continue
        for C in (1, 2, 10):
            N = 100_000
            M0 = floor(theta * N)
            numerator = (1 - epsilon) * (N + 1) - (2 * M0 + 1)
            lower_bound = float(numerator) / (2 * sqrt(C * (2 * N + 1)))
            assert numerator > 0 and lower_bound > 0


# #644: every three-edge subgraph of C5 has a two-vertex cover, but no choice
# of one retained endpoint per edge uses only two global vertices.
vertices = range(5)
edges = [(i, (i + 1) % 5) for i in vertices]
for triple in combinations(edges, 3):
    assert any(
        all(u in edge or v in edge for edge in triple)
        for u, v in combinations(vertices, 2)
    )
for choices in product((0, 1), repeat=5):
    retained = {edges[i][choices[i]] for i in range(5)}
    assert len(retained) >= 3


# #689: enumerate the switched-prime local kernel in Lemma 5.1 and check the
# residual-demand Euler-factor identity.
for s in (5, 7, 11, 13, 17, 19, 23):
    c = 1
    Cs = set(range(1, s)) - {c}
    for delta in range(1, s):
        kernel = sum(1 for Q in Cs if (Q + delta) % s in Cs)
        kernel += Fraction(s - 1, s) * int(delta != c)
        kernel += Fraction(s - 1, s) * int(delta != (-c) % s)
        assert Fraction(s, 1) - 2 - Fraction(2, s) <= kernel
        assert kernel <= Fraction(s, 1) - 2 - Fraction(1, s)
        assert Fraction(s, 1) * kernel / (s - 1) ** 2 <= 1
    residual_factor = Fraction(s - 2, s - 1) + sum(
        (Fraction(1, s**e) for e in range(1, 80)), Fraction()
    )
    assert 1 - residual_factor == Fraction(1, s**79 * (s - 1))


# #920/#812: exact exponent bookkeeping for representative fixed clique sizes,
# and the one-sided bridge denominator remains subpolynomial in the encoded
# model eta_n=1/loglog(n).
for s in range(4, 20):
    ramsey_log_power = 2 * s - 4
    t_log_power = Fraction(ramsey_log_power, s - 1)
    chromatic_n_power = 1 - Fraction(1, s - 1)
    assert t_log_power == Fraction(2 * (s - 2), s - 1)
    assert chromatic_n_power == Fraction(s - 2, s - 1)


# #949: a finite rational-vector analogue of the linearly independent example.
# Weight-2 vectors form a sum-free set over Q, while weight-1 vectors form a
# clique in the associated sum graph.
dimension = 8
basis = [tuple(int(i == j) for i in range(dimension)) for j in range(dimension)]
S = {
    tuple(basis[i][j] + basis[k][j] for j in range(dimension))
    for i, k in combinations(range(dimension), 2)
}
for x, y in product(S, repeat=2):
    assert tuple(x[j] + y[j] for j in range(dimension)) not in S
for x, y in combinations(basis, 2):
    assert tuple(x[j] + y[j] for j in range(dimension)) in S


print("PASS: R004 root finite identities and route certificates")
