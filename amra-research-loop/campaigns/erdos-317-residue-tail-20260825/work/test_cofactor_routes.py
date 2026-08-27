#!/usr/bin/env python3
"""Exact adversarial tests for top-prime cofactor mechanisms in #317."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
from pathlib import Path


def sieve(limit: int) -> list[int]:
    flag = bytearray(b"\x01") * (limit + 1)
    flag[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if flag[p]:
            flag[p * p : limit + 1 : p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [n for n in range(2, limit + 1) if flag[n]]


def crt(residues: list[tuple[int, int]]) -> tuple[int, int]:
    modulus = math.prod(p for p, _ in residues)
    value = 0
    for p, residue in residues:
        partial = modulus // p
        value += residue * partial * pow(partial, -1, p)
    return value % modulus, modulus


def signed_cofactor_crt(primes: tuple[int, ...], signs: tuple[int, ...]) -> dict[str, object]:
    product = math.prod(primes)
    prescriptions = []
    for p, sign in zip(primes, signs):
        cofactor = product // p
        prescriptions.append((p, sign * pow(cofactor, -1, p) % p))
    multiplier, modulus = crt(prescriptions)
    replay = {
        str(p): (multiplier * (product // p)) % p
        for p in primes
    }
    expected = {str(p): sign % p for p, sign in zip(primes, signs)}
    if replay != expected or math.gcd(multiplier, product) != 1:
        raise AssertionError("CRT cofactor replay failed")
    return {
        "primes": primes,
        "signs": signs,
        "multiplier_mod_product": multiplier,
        "product": modulus,
        "replay": replay,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    primes = sieve(args.limit)
    lcm_value = 1
    prime_index = 0
    active_primes: list[int] = []
    largest_prime_allowed: list[dict[str, int]] = []
    prime_endpoint_allowed: list[dict[str, int]] = []
    for n in range(2, args.limit + 1):
        lcm_value = math.lcm(lcm_value, n)
        if prime_index < len(primes) and primes[prime_index] == n:
            active_primes.append(n)
            prime_index += 1
        p = active_primes[-1]
        required = pow((lcm_value // p) % p, -1, p)
        if n >= 5 and required in (1, p - 1):
            largest_prime_allowed.append({"n": n, "prime": p, "required": required})
        if n == p and required in (1, p - 1):
            prime_endpoint_allowed.append({"prime": p, "required": required})

    crt_cases = []
    for prime_set in ((5, 7), (5, 7, 11), (11, 13, 17, 19)):
        for signs in itertools.product((-1, 1), repeat=len(prime_set)):
            crt_cases.append(signed_cofactor_crt(prime_set, signs))

    cgroup = Path("/proc/self/cgroup").read_text().strip()
    payload = {
        "schema_version": "amra.erdos317-cofactor-route-test.v1",
        "claim_scope": "finite counterinstances plus a general CRT identity proved in the accompanying note",
        "limit": args.limit,
        "largest_prime_allowed_count": len(largest_prime_allowed),
        "largest_prime_allowed_first": largest_prime_allowed[:40],
        "prime_endpoint_allowed": prime_endpoint_allowed,
        "all_sign_patterns_replayed": len(crt_cases),
        "crt_cases": crt_cases,
        "resource_guard": {
            "observed_cgroup": cgroup,
            "inside_openmath_slice": "openmath.slice" in cgroup,
        },
        "pid": os.getpid(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "largest_prime_allowed_count": payload["largest_prime_allowed_count"],
        "prime_endpoint_allowed_count": len(prime_endpoint_allowed),
        "crt_patterns": len(crt_cases),
    }))


if __name__ == "__main__":
    main()
