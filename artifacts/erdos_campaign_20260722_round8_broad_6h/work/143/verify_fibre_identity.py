#!/usr/bin/env python3
"""Finite falsifier for the rational-fibre identities in the round-8 note."""

from fractions import Fraction
from math import gcd, lcm


def main() -> None:
    checked = 0
    gamma = Fraction(3, 2)
    for a in range(1, 31):
        for q in range(1, 31):
            if gcd(a, q) != 1:
                continue
            for b in range(1, 31):
                for r in range(1, 31):
                    if gcd(b, r) != 1:
                        continue
                    g_left = gcd(a * r, b * q)
                    g_right = gcd(a, b) * gcd(q, r)
                    assert g_left == g_right

                    alpha = gamma * Fraction(a, q)
                    beta = gamma * Fraction(b, r)
                    if alpha == beta:
                        continue
                    aa, qq, bb, rr = a, q, b, r
                    if alpha < beta:
                        alpha, beta = beta, alpha
                        aa, qq, bb, rr = b, r, a, q
                    ratio = Fraction(aa * rr, bb * qq)
                    bracket_height = Fraction(ratio.denominator, 1) / beta
                    bracket_gcd = Fraction(lcm(qq, rr), 1) / (
                        gamma * gcd(aa, bb)
                    )
                    assert bracket_height == bracket_gcd
                    checked += 1

    print(f"status=PASS checked_oriented_pairs={checked}")


if __name__ == "__main__":
    main()
