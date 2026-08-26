#!/usr/bin/env python3
"""Deterministic independent replay of the campaign's machine-checkable claims."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


def primes_upto(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def carry_free(n: int, p: int) -> bool:
    half = (p - 1) // 2
    while n:
        if n % p > half:
            return False
        n //= p
    return True


def valuation_zero(n: int, p: int) -> bool:
    power = p
    valuation = 0
    while power <= 2 * n:
        valuation += (2 * n) // power - 2 * (n // power)
        power *= p
    return valuation == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = args.campaign / "evidence"
    scan = json.loads((evidence / "exact_carry_scan_2b.json").read_text())
    direct = json.loads((evidence / "record_1293081501_independent_replay.json").read_text())
    crt = json.loads((evidence / "crt_adversary_search.json").read_text())

    assert scan["max_n_scanned"] == 2_000_000_000
    assert scan["maximum"]["n"] == direct["n"]
    assert scan["accepted_prime_count_at_maximum"] == direct["accepted_prime_count"]
    assert abs(scan["maximum"]["value"] - direct["reciprocal_sum_kahan"]) < 1e-10
    assert scan["maximum"]["value"] > 1.1792429057944818
    witness = scan["single_top_power_test"]
    assert 2 * (witness["n"] % witness["top_power"]) < witness["top_power"]
    assert 2 * (witness["n"] % witness["bad_lower_power"]) >= witness["bad_lower_power"]

    rng = random.Random(37720260826)
    ps = primes_upto(10000)
    replayed = 0
    for _ in range(50000):
        n = rng.randint(1, 2_000_000_000)
        p = ps[rng.randrange(len(ps))]
        assert carry_free(n, p) == valuation_zero(n, p), (n, p)
        replayed += 1

    checked_trials = 0
    for trial in crt.get("trials", []):
        if "n" not in trial:
            continue
        n = int(trial["n"])
        verified = [p for p in primes_upto(trial["prime_limit"]) if p >= 3 and carry_free(n, p)]
        assert verified == trial["verified_accepted_primes"]
        assert trial["model_matches_verifier"]
        checked_trials += 1

    result = {
        "schema_version": "amra.erdos377.blind-replay.v1",
        "status": "passed",
        "random_seed": 37720260826,
        "random_kummer_legendre_pairs": replayed,
        "crt_trials_replayed": checked_trials,
        "finite_record_replayed": direct["n"],
        "statement_scope": "finite and reduction claims only",
        "not_certified": [
            "boundedness for every n",
            "maximality beyond 2000000000",
            "the unaudited 2010 three-prime preprint",
            "novelty or publication priority of the finite record",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
