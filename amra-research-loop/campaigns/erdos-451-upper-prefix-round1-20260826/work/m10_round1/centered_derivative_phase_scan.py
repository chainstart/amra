#!/usr/bin/env python3
"""Finite diagnostics for centered F'(d_i) phases on actual 451 blocks.

The output is descriptive only.  It tests whether the local derivative and
inverse-derivative residues show obvious smallness, adjacent-offset
coherence, or low-frequency bias.  It does not promote a distribution law.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
import statistics


def prime_sieve(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (
                (limit - p * p) // p + 1
            )
    return [n for n in range(2, limit + 1) if sieve[n]]


def centered(residue: int, modulus: int) -> int:
    residue %= modulus
    return residue if 2 * residue <= modulus else residue - modulus


def pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(vx * vy)


def discrepancy(unit_values: list[float]) -> float:
    values = sorted(unit_values)
    q = len(values)
    return max(
        max((index + 1) / q - value, value - index / q)
        for index, value in enumerate(values)
    )


def block_row(k: int, scale: int, primes: list[int], frequencies: int) -> dict[str, object]:
    offsets = [p - k for p in primes]
    q = len(primes)
    derivative_centers = []
    derivative_residues = []
    inverse_residues = []
    raw_inverse_units = []
    for index, (p, d) in enumerate(zip(primes, offsets)):
        derivative = 1
        for other_index, other_d in enumerate(offsets):
            if other_index != index:
                derivative = derivative * (d - other_d) % p
        assert derivative
        inverse = pow(derivative, -1, p)
        derivative_center = centered(derivative, p)
        inverse_center = centered(inverse, p)
        derivative_centers.append(derivative_center)
        derivative_residues.append(derivative_center / p)
        inverse_residues.append(inverse_center / p)
        raw_inverse_units.append(inverse / p)

    # Exact local identity F'(d_i)=(-1)^(q-1)P/p_i (mod p_i).
    period = math.prod(primes)
    cofactor_sum = sum(period // p for p in primes)
    sign = -1 if (q - 1) % 2 else 1
    for p, derivative_integer in zip(primes, derivative_centers):
        assert (derivative_integer - sign * (period // p)) % p == 0
        assert (sign * cofactor_sum - derivative_integer) % p == 0

    adjacent_derivative = pearson(derivative_residues[:-1], derivative_residues[1:])
    adjacent_inverse = pearson(inverse_residues[:-1], inverse_residues[1:])
    spectral = []
    for frequency in range(1, frequencies + 1):
        value = abs(
            sum(cmath.exp(2j * math.pi * frequency * x) for x in raw_inverse_units)
        ) / q
        spectral.append(value)
    small_thresholds = (0.01, 0.05, 0.10)
    return {
        "k": k,
        "scale": scale,
        "rank": q,
        "offset_min": min(offsets),
        "offset_max": max(offsets),
        "derivative_mean_abs": statistics.fmean(abs(x) for x in derivative_residues),
        "derivative_mean_square": statistics.fmean(x * x for x in derivative_residues),
        "inverse_mean_abs": statistics.fmean(abs(x) for x in inverse_residues),
        "inverse_mean_square": statistics.fmean(x * x for x in inverse_residues),
        "derivative_adjacent_correlation": adjacent_derivative,
        "inverse_adjacent_correlation": adjacent_inverse,
        "derivative_same_sign_adjacent_fraction": sum(
            x * y > 0 for x, y in zip(derivative_residues[:-1], derivative_residues[1:])
        )
        / (q - 1),
        "inverse_same_sign_adjacent_fraction": sum(
            x * y > 0 for x, y in zip(inverse_residues[:-1], inverse_residues[1:])
        )
        / (q - 1),
        "inverse_star_discrepancy": discrepancy(raw_inverse_units),
        "inverse_max_low_frequency_coefficient": max(spectral),
        "inverse_max_low_frequency_scaled_sqrt_rank": max(spectral) * math.sqrt(q),
        "derivative_small_fractions": {
            str(threshold): sum(abs(x) <= threshold for x in derivative_residues) / q
            for threshold in small_thresholds
        },
        "inverse_small_fractions": {
            str(threshold): sum(abs(x) <= threshold for x in inverse_residues) / q
            for threshold in small_thresholds
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-k", type=int, default=200)
    parser.add_argument("--max-k", type=int, default=5000)
    parser.add_argument("--step", type=int, default=29)
    parser.add_argument("--min-rank", type=int, default=12)
    parser.add_argument("--frequencies", type=int, default=16)
    args = parser.parse_args()
    primes = prime_sieve(2 * args.max_k)
    rows = []
    for k in range(args.min_k, args.max_k + 1, args.step):
        blocks: dict[int, list[int]] = {}
        for p in primes:
            if p <= k:
                continue
            if p >= 2 * k:
                break
            offset = p - k
            scale = 1 << (offset.bit_length() - 1)
            blocks.setdefault(scale, []).append(p)
        for scale, block in blocks.items():
            if len(block) >= args.min_rank:
                rows.append(block_row(k, scale, block, args.frequencies))

    aggregate_fields = (
        "derivative_mean_abs",
        "derivative_mean_square",
        "inverse_mean_abs",
        "inverse_mean_square",
        "derivative_adjacent_correlation",
        "inverse_adjacent_correlation",
        "inverse_star_discrepancy",
        "inverse_max_low_frequency_scaled_sqrt_rank",
    )

    def aggregate(selected: list[dict[str, object]], field: str) -> dict[str, float]:
        values = [float(row[field]) for row in selected]
        return {
            "mean": statistics.fmean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
        }

    def stratum(selected: list[dict[str, object]]) -> dict[str, object]:
        return {
            "systems": len(selected),
            "rank_range": [
                min(row["rank"] for row in selected),
                max(row["rank"] for row in selected),
            ],
            "aggregates": {
                field: aggregate(selected, field) for field in aggregate_fields
            },
            "mean_small_fractions": {
                family: {
                    threshold: statistics.fmean(
                        float(row[family][threshold]) for row in selected
                    )
                    for threshold in ("0.01", "0.05", "0.1")
                }
                for family in (
                    "derivative_small_fractions",
                    "inverse_small_fractions",
                )
            },
        }

    payload = {
        "classification": "finite_actual_block_phase_diagnostic_only",
        "parameters": vars(args),
        "systems": len(rows),
        "rank_range": [min(row["rank"] for row in rows), max(row["rank"] for row in rows)],
        "uniform_centered_benchmarks": {
            "mean_abs": 0.25,
            "mean_square": 1 / 12,
            "small_fraction_at_tau": "2*tau",
            "adjacent_correlation": 0.0,
        },
        "rank_strata": {
            "all": stratum(rows),
            "rank_at_least_50": stratum(
                [row for row in rows if int(row["rank"]) >= 50]
            ),
            "rank_at_least_100": stratum(
                [row for row in rows if int(row["rank"]) >= 100]
            ),
        },
        "smallest_derivative_mean_abs": sorted(
            rows, key=lambda row: row["derivative_mean_abs"]
        )[:8],
        "smallest_inverse_mean_abs": sorted(
            rows, key=lambda row: row["inverse_mean_abs"]
        )[:8],
        "largest_inverse_discrepancy": sorted(
            rows, key=lambda row: row["inverse_star_discrepancy"], reverse=True
        )[:8],
        "largest_inverse_low_frequency": sorted(
            rows,
            key=lambda row: row["inverse_max_low_frequency_scaled_sqrt_rank"],
            reverse=True,
        )[:8],
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
