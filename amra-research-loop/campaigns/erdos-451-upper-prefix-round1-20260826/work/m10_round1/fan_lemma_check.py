#!/usr/bin/env python3
"""Finite off-by-one checks for the proved M10 coherent-fan lemmas.

The checks are diagnostics only.  The evidence note contains the proofs.
"""

from itertools import combinations
import json
import math


def allowed(s, k, moduli):
    return all(0 <= s % q < q - k for q in moduli)


fan_systems = 0
common_quotient_rows = 0
one_merge_rows = 0
multi_merge_rows = 0

for k in range(4, 23):
    ambient = list(range(k + 1, 2 * k))
    for size in (2, 3):
        for system in combinations(ambient, size):
            L, P = min(system), max(system)
            D, B = P - L, L - k
            if D == 0:
                continue
            T = (B - 1) // D
            fan_systems += 1

            for t in range(1, T + 1):
                fan = range(t * P, t * P + B - t * D)
                assert all(allowed(s, k, system) for s in fan)

            # The fan interval is exactly the allowed set with a common
            # quotient t across the block.
            for t in range(0, T + 3):
                lo = t * P
                hi = (t + 1) * L - k - 1
                expected = set(range(lo, hi + 1)) if lo <= hi else set()
                search_hi = max(lo, (t + 1) * L)
                actual = {
                    s
                    for s in range(max(0, lo - 2), search_hi + 2)
                    if all(s // q == t for q in system)
                    and allowed(s, k, system)
                }
                assert actual == expected
                common_quotient_rows += 1

            for r in ambient:
                if r in system or r >= P:
                    continue
                c = r - k
                for N in range(1, T + 1):
                    w = B - N * D
                    if min(c, w) * (N + 1) <= r:
                        continue
                    assert any(
                        allowed(s, k, system + (r,))
                        for s in range(k, N * P + B + 1)
                    )
                    one_merge_rows += 1

            extras = [r for r in ambient if r not in system and r < P]
            for new in combinations(extras, 2):
                c = min(r - k for r in new)
                R = max(new)
                for N in range(1, T + 1):
                    w = B - N * D
                    for M in range(2, 6):
                        if M**2 > N or 2 * R >= M * min(c, w):
                            continue
                        assert any(
                            allowed(s, k, system + new)
                            for s in range(k, N * P + B + 1)
                        )
                        multi_merge_rows += 1


def is_prime(n):
    if n < 2:
        return False
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            return False
    return True


# The all-small exhaustive range has too little fan length for the
# two-coordinate hypothesis M^2 <= N.  Exercise that branch on actual prime
# systems at moderate k.
for k in range(60, 401, 10):
    primes = [p for p in range(k + 1, 2 * k) if is_prime(p)]
    if len(primes) < 4:
        continue
    system = tuple(primes[-2:])
    new = tuple(primes[-4:-2])
    L, P = min(system), max(system)
    D, B = P - L, L - k
    if D == 0:
        continue
    T = (B - 1) // D
    c = min(r - k for r in new)
    R = max(new)
    for N in range(1, T + 1):
        w = B - N * D
        for M in range(2, math.isqrt(N) + 1):
            if 2 * R >= M * min(c, w):
                continue
            assert any(
                allowed(s, k, system + new)
                for s in range(k, N * P + B + 1)
            )
            multi_merge_rows += 1

print(
    json.dumps(
        {
            "classification": "finite_diagnostic_only",
            "fan_systems": fan_systems,
            "common_quotient_rows": common_quotient_rows,
            "one_coordinate_merge_rows": one_merge_rows,
            "two_coordinate_merge_rows": multi_merge_rows,
        },
        sort_keys=True,
    )
)
