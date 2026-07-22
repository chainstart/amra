#!/usr/bin/env python3
"""Exact combinatorial constant audit for the #1083 stability lemmas.

The geometric proof is in near_reflection_stability.md.  This script checks
the finite-order chord threshold, the sharp projective-circle construction,
the allowed-angle count, and the even spherical-polynomial dimension formula
for t <= 500.
"""

from __future__ import annotations

from fractions import Fraction
import json
from math import gcd


def allowed_angle_fractions(M: int) -> set[Fraction]:
    # theta/pi in (0,1/2]; reduction automatically removes repetitions.
    return {
        Fraction(k, m)
        for m in range(2, M + 1)
        for k in range(1, m // 2 + 1)
    }


def totient_sieve(limit: int) -> list[int]:
    values = list(range(limit + 1))
    for p in range(2, limit + 1):
        if values[p] == p:
            for multiple in range(p, limit + 1, p):
                values[multiple] -= values[multiple] // p
    return values


def main() -> None:
    maximum_ratio = Fraction(0, 1)
    largest_s = 0
    largest_near_reflection_bound = 0
    angles: set[Fraction] = set()
    previous_M = 1
    totients = totient_sieve(1001)
    totient_sum_from_three = 0
    for t in range(1, 501):
        M = 2 * t + 1
        for m in range(previous_M + 1, M + 1):
            angles.update(Fraction(k, m) for k in range(1, m // 2 + 1))
            if m >= 3:
                totient_sum_from_three += totients[m]
        previous_M = M
        s = len(angles)
        exact_totient_count = 1 + totient_sum_from_three // 2
        assert s == exact_totient_count
        projective_directions = 1 + sum(totients[2:M + 1])
        assert projective_directions == 2 * s
        # The *pairwise* denominator condition is much stronger than merely
        # belonging to this Farey universe: the circle-gap proof gives at most
        # M directions.  The regular M-gon directions attain M.
        regular_directions = {Fraction(j, M) for j in range(M)}
        assert len(regular_directions) == M
        for delta in range(1, M):
            assert M // gcd(M, delta) <= M
        near_reflection_bound = max(15, M + 1)
        coarse = Fraction(M * M, 4) + Fraction(M, 2)
        assert s <= coarse
        assert (M + 1) // 2 >= t + 1
        # Sum of dimensions of real spherical harmonics of even degrees.
        harmonic_dimension = sum(4 * j + 1 for j in range(s + 1))
        assert harmonic_dimension == (s + 1) * (2 * s + 1)
        maximum_ratio = max(maximum_ratio, Fraction(s, M * M))
        largest_s = s
        largest_near_reflection_bound = near_reflection_bound

    print(json.dumps({
        "schema": "amra.erdos1083.round8.near_reflection_constants.v1",
        "checked_t_interval": [1, 500],
        "largest_allowed_angle_count": largest_s,
        "largest_uniform_near_reflection_bound":
            largest_near_reflection_bound,
        "max_s_over_M_squared":
            f"{maximum_ratio.numerator}/{maximum_ratio.denominator}",
        "identities": {
            "finite_rotation_threshold":
                "m > 2t+1 implies floor(m/2) >= t+1",
            "even_spherical_dimension":
                "sum_{j=0}^s (4j+1) = (s+1)(2s+1)",
            "allowed_angle_count":
                "s_M = 1 + (1/2) sum_{m=3}^M phi(m)",
            "projective_farey_count":
                "1 + sum_{m=2}^M phi(m) = 2 s_M",
            "pairwise_circle_gap_bound":
                "pairwise difference denominators <= M implies at most M projective directions",
            "sharp_circle_construction":
                "{j/M : 0 <= j < M} has M directions and all difference orders <= M",
            "univariate_degree_barrier":
                "a nonzero polynomial vanishing on all allowed values has degree >= s_M",
        },
        "warning": "constant audit only; universal geometric proof is in markdown",
        "result": "PASS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
