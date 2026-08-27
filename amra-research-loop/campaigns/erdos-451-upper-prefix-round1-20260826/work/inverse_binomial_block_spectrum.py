#!/usr/bin/env python3
"""Finite spectral audit for dyadic inverse-binomial prime-offset blocks."""

from __future__ import annotations

import argparse
import json
import math
from statistics import fmean, median


def primes_below(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * limit
    if limit:
        sieve[0] = 0
    if limit > 1:
        sieve[1] = 0
    for n in range(2, math.isqrt(limit - 1) + 1):
        if sieve[n]:
            sieve[n * n : limit : n] = b"\x00" * (((limit - 1 - n * n) // n) + 1)
    return [n for n in range(2, limit) if sieve[n]]


def centered(residue: int, modulus: int) -> int:
    return residue if residue <= modulus // 2 else residue - modulus


def normalized_kernel(width: int, frequency: int, modulus: int) -> float:
    frequency = centered(frequency % modulus, modulus)
    if frequency == 0:
        return 1.0
    numerator = abs(math.sin(math.pi * width * frequency / modulus))
    denominator = width * abs(math.sin(math.pi * frequency / modulus))
    return numerator / denominator


def block_rows(k: int) -> list[tuple[int, list[int]]]:
    width = max(1, int(k / math.log(k) ** 2))
    interval_primes = [p for p in primes_below(2 * k) if k + width < p < 2 * k]
    rows = []
    lower = width
    while lower < k:
        upper = min(2 * lower, k)
        block = [p for p in interval_primes if lower < p - k <= upper]
        if block:
            rows.append((lower, block))
        lower = upper
    return rows


def audit_block(k: int, A: int, lower: int, block: list[int], frequency_limit: int) -> dict[str, object]:
    absorber = math.comb(k + A, A)
    period = math.prod(block)
    offsets = [p - k for p in block]
    rank = len(block)

    local_data = []
    for p, b in zip(block, offsets, strict=True):
        cofactor = (period // p) % p
        derivative = math.prod((b - other) % p for other in offsets if other != b) % p
        assert cofactor == ((-1) ** (rank - 1) * derivative) % p
        binomial_phase = ((-1) ** A * math.comb(b - 1, A)) % p
        assert absorber % p == binomial_phase
        combined = absorber * cofactor % p
        expected_combined = ((-1) ** (A + rank - 1) * math.comb(b - 1, A) * derivative) % p
        assert combined == expected_combined
        local_data.append((p, b, combined))

    tested_limit = min(frequency_limit, min(block) - 1)
    best = None
    log_weights = []
    for global_frequency in range(1, tested_limit + 1):
        local_frequencies = [
            centered((global_frequency * pow(combined, -1, p)) % p, p)
            for p, _, combined in local_data
        ]
        kernel_values = [
            normalized_kernel(b, h, p)
            for (p, b, _), h in zip(local_data, local_frequencies, strict=True)
        ]
        log_weight = sum(math.log(max(value, 1e-300)) for value in kernel_values)
        log_weights.append(log_weight)
        record = {
            "global_frequency": global_frequency,
            "log_abs_normalized_Fourier_coefficient": log_weight,
            "geometric_mean_local_kernel": math.exp(log_weight / rank),
            "maximum_abs_local_frequency_over_p": max(
                abs(h) / p for h, (p, _, _) in zip(local_frequencies, local_data, strict=True)
            ),
            "small_kernel_frequency_count": sum(
                abs(h) <= p / b
                for h, (p, b, _) in zip(local_frequencies, local_data, strict=True)
            ),
        }
        if best is None or log_weight > best["log_abs_normalized_Fourier_coefficient"]:
            best = record
    assert best is not None

    dual_cutoff = max(1, k // max(offsets))
    phase_radius = dual_cutoff
    bad_pairs = [
        (p, h)
        for p in block
        for h in range(1, dual_cutoff + 1)
        if abs(centered(h * (absorber % p), p)) <= phase_radius
    ]
    divisor_upper_bound = (
        2
        * dual_cutoff
        * phase_radius
        * math.log(dual_cutoff * absorber + phase_radius)
        / math.log(k)
    )

    reciprocal_density_log = sum(math.log(p / (p - k)) for p in block)
    return {
        "b_range": [lower, min(2 * lower, k)],
        "rank": rank,
        "reciprocal_density_log": reciprocal_density_log,
        "dense_seed_relative_density_threshold_proxy": k * math.log(k) / lower**2,
        "global_frequency_scan": {
            "tested_limit": tested_limit,
            "best": best,
            "median_log_abs_coefficient": median(log_weights),
            "mean_log_abs_coefficient": fmean(log_weights),
        },
        "low_dual_phase_scan": {
            "h_cutoff": dual_cutoff,
            "centered_residue_radius": phase_radius,
            "bad_pair_count": len(bad_pairs),
            "bad_prime_count": len({p for p, _ in bad_pairs}),
            "divisor_union_upper_bound": divisor_upper_bound,
        },
    }


def audit_k(k: int, frequency_limit: int) -> dict[str, object]:
    A = max(1, int(k / math.log(k) ** 2))
    return {
        "k": k,
        "A": A,
        "blocks": [
            audit_block(k, A, lower, block, frequency_limit)
            for lower, block in block_rows(k)
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frequency-limit", type=int, default=512)
    args = parser.parse_args()
    print(
        json.dumps(
            {
                "schema_version": "erdos451.inverse_binomial_block_spectrum.v1",
                "cases": [audit_k(1000, args.frequency_limit), audit_k(10000, args.frequency_limit)],
                "boundary": (
                    "Finite exact modular identities plus floating-point Fourier magnitudes. "
                    "The scan is a falsification diagnostic, not an asymptotic theorem."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
