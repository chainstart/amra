#!/usr/bin/env python3
"""Exact finite verification for the coupled conductor-heat and triangular identities.

This script verifies identities only.  Its finite output is not evidence for
an asymptotic estimate.
"""

from fractions import Fraction
from math import comb, gcd, log
import json


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return n == d
        d += 1 if d == 2 else 2
    return True


def one_case(k: int, limit: int) -> dict:
    A = int(k / (log(k) ** 2))
    Q0 = comb(k + A, A)
    primes = [p for p in range(k + A + 1, 2 * k) if is_prime(p)]
    P = 1
    for p in primes:
        P *= p

    allowed_sets = {}
    for p in primes:
        d = p - k - 1
        qinv = pow(Q0, -1, p)
        allowed_sets[p] = {(-qinv * j) % p for j in range(1, d + 1)}

    tested_pairs = 0
    distinct_products = set()
    triangular_matches = True
    centered_matches = True
    heat_matches = True
    maximum_allowed = 0
    minimum_violations = len(primes)

    kappa = Fraction(1, 1)
    for p in primes:
        kappa *= Fraction(k, p - 1)

    for u in range(1, limit + 1):
        for t in range(1, limit + 1):
            x = u * t
            if gcd(x, P) != 1:
                continue
            tested_pairs += 1
            distinct_products.add(x)
            y = Q0 * x

            allowed = {p for p in primes if x % p in allowed_sets[p]}
            forbidden = set(primes) - allowed
            maximum_allowed = max(maximum_allowed, len(allowed))
            minimum_violations = min(minimum_violations, len(forbidden))

            triangular = 1
            seen = set()
            for j in range(1, k):
                for p in primes:
                    if p > k + j and (y + j) % p == 0:
                        if p in seen:
                            triangular_matches = False
                        seen.add(p)
                        triangular *= p
            expected = 1
            for p in allowed:
                expected *= p
            triangular_matches &= triangular == expected

            direct_centered = Fraction(1, 1)
            weighted_missing = Fraction(1, 1)
            for p in primes:
                delta = Fraction(p - k - 1, p - 1)
                if p in allowed:
                    direct_centered *= 1 - delta
                else:
                    direct_centered *= -delta
                    weighted_missing *= -Fraction(p - k - 1, k)
            centered_matches &= direct_centered == kappa * weighted_missing

            # sigma=1, so p^{-sigma}=1/p and every quantity is rational.
            direct_heat = Fraction(1, 1)
            heat_base = Fraction(1, 1)
            heat_violation = Fraction(1, 1)
            for p in primes:
                delta = Fraction(p - k - 1, p - 1)
                q = Fraction(1, p)
                z = (1 - delta) if p in allowed else -delta
                direct_heat *= delta + q * z
                a = delta + q * (1 - delta)
                heat_base *= a
                if p in forbidden:
                    heat_violation *= delta * (1 - q) / a
            heat_matches &= direct_heat == heat_base * heat_violation

    return {
        "k": k,
        "A": A,
        "Q0": Q0,
        "remaining_primes": primes,
        "tested_unit_pairs": tested_pairs,
        "distinct_products": len(distinct_products),
        "maximum_allowed_coordinates": maximum_allowed,
        "minimum_violations": minimum_violations,
        "triangular_identity_exact": triangular_matches,
        "full_centered_weight_identity_exact": centered_matches,
        "conductor_heat_violation_identity_exact_at_sigma_1": heat_matches,
    }


def main() -> None:
    cases = [one_case(k, 32) for k in (20, 30, 45, 60)]
    payload = {
        "schema_version": "erdos451.coupled_heat_triangular_audit.v1",
        "scope": {
            "k_values": [20, 30, 45, 60],
            "rectangle_side": 32,
            "arithmetic": "exact Fraction arithmetic",
            "boundary": "Finite verification of algebraic identities only; no asymptotic estimate is inferred.",
        },
        "cases": cases,
        "all_identities_exact": all(
            case[flag]
            for case in cases
            for flag in (
                "triangular_identity_exact",
                "full_centered_weight_identity_exact",
                "conductor_heat_violation_identity_exact_at_sigma_1",
            )
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
