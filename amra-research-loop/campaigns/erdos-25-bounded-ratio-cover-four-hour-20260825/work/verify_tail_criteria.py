#!/usr/bin/env python3
"""Finite exact checks for the CRT and prime-saturation examples."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


def primes_through(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime-limit", type=int, default=10_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    finite_primes = [2, 3, 5, 7, 11]
    period = math.prod(finite_primes)
    covered = bytearray(period)
    for prime in finite_primes:
        residue = prime - 1
        covered[residue:period:prime] = b"\x01" * (((period - 1 - residue) // prime) + 1)
    uncovered = covered.count(0)
    expected_complement = math.prod(prime - 1 for prime in finite_primes)
    if uncovered != expected_complement:
        raise AssertionError((uncovered, expected_complement))
    exact_union_density = Fraction(period - uncovered, period)
    crt_union_density = 1 - math.prod(Fraction(prime - 1, prime) for prime in finite_primes)
    if exact_union_density != crt_union_density:
        raise AssertionError((exact_union_density, crt_union_density))

    primes = primes_through(args.prime_limit)
    target_uncovered_checks = 0
    for index, prime in enumerate(primes):
        target = prime - 1
        if any(target % earlier == earlier - 1 for earlier in primes[:index]):
            raise AssertionError((prime, target))
        target_uncovered_checks += 1
    for n in range(1, args.prime_limit):
        if not any((n + 1) % prime == 0 for prime in primes):
            raise AssertionError(n)

    collision_height = 80
    common = math.lcm(*range(1, 2 * collision_height + 1)) - 1
    collision_pairs = []
    for k in range(2 * collision_height, collision_height, -1):
        step = (common + 1) // k
        target = step - 1
        if not target < step <= 2 * target:
            raise AssertionError((k, target, step))
        if collision_pairs and not (
            collision_pairs[-1][1] < target and collision_pairs[-1][2] < step
        ):
            raise AssertionError("targets and steps must increase")
        if any(target % earlier_step == earlier_target for _, earlier_target, earlier_step in collision_pairs):
            raise AssertionError("a target was covered by an earlier progression")
        if (common - target) % step:
            raise AssertionError("common collision point missing")
        collision_pairs.append((k, target, step))

    base_pairs = [(2, 3), (5, 7), (11, 15), (19, 24)]
    lift_g, lift_a, lift_limit = 7, 3, 200_000
    lifted_pairs = [(lift_a + lift_g * r, lift_g * d) for r, d in base_pairs]
    for n in range(1, lift_limit + 1):
        base_member = any(n >= r and (n - r) % d == 0 for r, d in base_pairs)
        lifted_n = lift_a + lift_g * n
        lifted_member = any(
            lifted_n >= target and (lifted_n - target) % step == 0
            for target, step in lifted_pairs
        )
        if base_member != lifted_member:
            raise AssertionError((n, lifted_n))

    payload = {
        "schema_version": "erdos-25.tail-criteria-replay.v1",
        "status": "passed",
        "finite_crt_primes": finite_primes,
        "finite_crt_period": period,
        "finite_crt_exact_union_density": [exact_union_density.numerator, exact_union_density.denominator],
        "finite_crt_complement_count": uncovered,
        "prime_limit": args.prime_limit,
        "prime_targets_checked_uncovered": target_uncovered_checks,
        "positive_integers_checked_covered": args.prime_limit - 1,
        "irredundant_collision_family_size": collision_height,
        "irredundant_collision_common_point_decimal_digits": len(str(common)),
        "affine_lift_g": lift_g,
        "affine_lift_a": lift_a,
        "affine_lift_membership_checks": lift_limit,
        "coverage_identity": "For the infinite prime family d=p, r=p-1, n is covered exactly because n+1 has a prime divisor.",
        "bitmap_sha256": hashlib.sha256(covered).hexdigest(),
        "interpretation_limit": "The finite replay checks the algebra and CRT counts; divergence of the reciprocal-prime sum is a classical theorem used in the natural proof.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "passed",
        "prime_targets_checked_uncovered": target_uncovered_checks,
        "positive_integers_checked_covered": args.prime_limit - 1,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
