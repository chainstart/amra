#!/usr/bin/env python3
"""Exact phase and cyclic-gap audit for several narrow-prime absorbers."""

from __future__ import annotations

import argparse
import json
import math
from functools import reduce
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


def absorber_values(k: int, width: int) -> dict[str, int]:
    near_primes = [p for p in primes_below(k + width + 1) if k < p <= k + width]
    rising = math.prod(range(k + 1, k + width + 1))
    return {
        "prime_product": math.prod(near_primes),
        "canonical_binomial": math.comb(k + width, width),
        "full_rising_factorial": rising,
        "interval_lcm": reduce(math.lcm, range(k + 1, k + width + 1), 1),
    }


def centered(residue: int, modulus: int) -> int:
    return residue if residue <= modulus // 2 else residue - modulus


def largest_cyclic_gap(period: int, representatives: list[int]) -> int:
    representatives.sort()
    if len(representatives) == 1:
        return period
    return max(
        [
            representatives[index + 1] - representatives[index]
            for index in range(len(representatives) - 1)
        ]
        + [period + representatives[0] - representatives[-1]]
    )


def local_ap_gap(p: int, k: int, absorber: int) -> int:
    width = p - k
    step = pow(absorber, -1, p)
    residues = sorted({(-offset * step) % p for offset in range(width)})
    return largest_cyclic_gap(p, residues)


def quantiles(values: list[float]) -> dict[str, float]:
    return {
        "minimum": min(values),
        "median": median(values),
        "mean": fmean(values),
        "maximum": max(values),
    }


def phase_summary(k: int, width: int) -> dict[str, object]:
    interval_primes = [p for p in primes_below(2 * k) if k < p < 2 * k]
    absorbed = [p for p in interval_primes if p <= k + width]
    remaining = [p for p in interval_primes if p > k + width]
    absorbers = absorber_values(k, width)
    prime_offsets = [p - k for p in absorbed]
    rising_over_lcm = absorbers["full_rising_factorial"] // absorbers["interval_lcm"]
    for p in remaining:
        b = p - k
        binomial_residue = ((-1) ** width * math.comb(b - 1, width)) % p
        assert absorbers["canonical_binomial"] % p == binomial_residue
        assert absorbers["full_rising_factorial"] % p == (
            math.factorial(width) * binomial_residue
        ) % p
        assert absorbers["prime_product"] % p == math.prod(
            (offset - b) % p for offset in prime_offsets
        ) % p
        assert absorbers["interval_lcm"] % p == (
            absorbers["full_rising_factorial"] * pow(rising_over_lcm, -1, p)
        ) % p

    variants: dict[str, object] = {}
    for name, absorber in absorbers.items():
        phase_rows = []
        for p in remaining:
            q_residue = absorber % p
            inverse = pow(absorber, -1, p)
            local_gap = local_ap_gap(p, k, absorber)
            phase_rows.append(
                {
                    "p": p,
                    "b": p - k,
                    "Q_mod_p": q_residue,
                    "centered_Q_mod_p": centered(q_residue, p),
                    "inverse_step": inverse,
                    "centered_inverse": centered(inverse, p),
                    "local_AP_gap": local_gap,
                    "local_AP_gap_over_density_scale": local_gap / (p / (p - k)),
                }
            )
        q_phase = [abs(row["centered_Q_mod_p"]) / row["p"] for row in phase_rows]
        inverse_phase = [abs(row["centered_inverse"]) / row["p"] for row in phase_rows]
        gap_ratios = [row["local_AP_gap_over_density_scale"] for row in phase_rows]
        minimum_q_phase_row = min(
            phase_rows, key=lambda row: abs(row["centered_Q_mod_p"]) / row["p"]
        )
        minimum_inverse_phase_row = min(
            phase_rows, key=lambda row: abs(row["centered_inverse"]) / row["p"]
        )
        maximum_gap_row = max(
            phase_rows, key=lambda row: row["local_AP_gap_over_density_scale"]
        )
        variants[name] = {
            "decimal_digits": len(str(absorber)),
            "natural_log": math.log(absorber),
            "absorbs_every_near_prime": all(absorber % p == 0 for p in absorbed),
            "centered_Q_mod_p_over_p": quantiles(q_phase),
            "centered_inverse_over_p": quantiles(inverse_phase),
            "local_AP_gap_over_density_scale": quantiles(gap_ratios),
            "extreme_witnesses": {
                "minimum_Q_phase": minimum_q_phase_row,
                "minimum_inverse_phase": minimum_inverse_phase_row,
                "maximum_local_AP_gap_ratio": maximum_gap_row,
            },
            "Q_phase_below_threshold_counts": {
                "0.01": sum(value < 0.01 for value in q_phase),
                "0.05": sum(value < 0.05 for value in q_phase),
                "0.10": sum(value < 0.10 for value in q_phase),
            },
        }
    return {
        "k": k,
        "A": width,
        "absorbed_primes": absorbed,
        "remaining_prime_count": len(remaining),
        "variants": variants,
    }


def exact_global_gap(k: int, width: int) -> dict[str, object]:
    interval_primes = [p for p in primes_below(2 * k) if k < p < 2 * k]
    remaining = [p for p in interval_primes if p > k + width]
    period = math.prod(remaining)
    allowed_count = math.prod(p - k for p in remaining)
    variants: dict[str, object] = {}
    for name, absorber in absorber_values(k, width).items():
        local_sets = [
            {(-offset * pow(absorber, -1, p)) % p for offset in range(p - k)}
            for p in remaining
        ]
        representatives = [
            n
            for n in range(period)
            if all(n % p in allowed for p, allowed in zip(remaining, local_sets, strict=True))
        ]
        assert len(representatives) == allowed_count
        gap = largest_cyclic_gap(period, representatives)
        variants[name] = {
            "largest_cyclic_gap": gap,
            "gap_over_density_scale": gap / (period / allowed_count),
            "Q_mod_remaining_primes": {str(p): absorber % p for p in remaining},
            "inverse_steps": {str(p): pow(absorber, -1, p) for p in remaining},
        }
    return {
        "k": k,
        "A": width,
        "remaining_primes": remaining,
        "period": period,
        "allowed_count": allowed_count,
        "variants": variants,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print(
        json.dumps(
            {
                "schema_version": "erdos451.absorption_dilate_audit.v1",
                "exact_global_gap_cases": [
                    exact_global_gap(18, 5),
                    exact_global_gap(20, 5),
                    exact_global_gap(24, 7),
                ],
                "asymptotic_scale_phase_cases": [
                    phase_summary(1000, max(1, int(1000 / math.log(1000) ** 2))),
                    phase_summary(10000, max(1, int(10000 / math.log(10000) ** 2))),
                ],
                "interpretation": (
                    "Exact finite arithmetic only. Cyclic gaps test the t-coordinate after n=Q*t; "
                    "phase summaries neither prove nor disprove a uniform correlated-dilate lemma."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
