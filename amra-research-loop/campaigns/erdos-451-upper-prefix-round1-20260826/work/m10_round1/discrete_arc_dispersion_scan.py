#!/usr/bin/env python3
"""Finite scan of the decisive discrete arc-dispersion ratio.

All CRT periods, target lengths, and arc endpoints use Python integers.
Dirichlet-kernel weights and the final mass use double precision.  This is
diagnostic evidence only, not an asymptotic bound.
"""

from __future__ import annotations

import argparse
import json
import math


def primes_below(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * limit
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit - 1) + 1):
        if sieve[p]:
            sieve[p * p : limit : p] = b"\x00" * (
                (limit - 1 - p * p) // p + 1
            )
    return [p for p in range(2, limit) if sieve[p]]


def dirichlet_average_abs(length: int, a: int, prime: int) -> float:
    a %= prime
    if a == 0 or length == 1:
        return 1.0
    return abs(math.sin(math.pi * length * a / prime)) / (
        length * abs(math.sin(math.pi * a / prime))
    )


def local_weight(prime: int, width: int, frequency: int) -> float:
    left = (width + 1) // 2
    right = width + 1 - left
    return dirichlet_average_abs(left, frequency, prime) * dirichlet_average_abs(
        right, frequency, prime
    )


def scan_system(
    moduli: list[int],
    widths: list[int],
    c_num: int,
    c_den: int,
    dilation: int,
    max_arc: int,
    scales: int,
) -> dict[str, object]:
    rank = len(moduli)
    period = math.prod(moduli)
    density_denominator = math.prod(widths)
    h_num = pow(c_num, rank) * period
    h_den = pow(c_den, rank) * density_denominator
    h = (h_num + h_den - 1) // h_den
    arc = (period + h - 1) // h
    thresholds = []
    for scale in range(scales):
        threshold = min(period // 2, arc * (1 << scale))
        if threshold > max_arc:
            break
        if not thresholds or threshold != thresholds[-1]:
            thresholds.append(threshold)
    if not thresholds:
        return {
            "status": "skipped_arc_too_large",
            "rank": rank,
            "P": str(period),
            "D_integer": str(density_denominator),
            "h": h,
            "X": arc,
            "max_arc": max_arc,
            "dilation": dilation,
        }

    local_l1 = []
    inverses = []
    inverse_dilation = pow(dilation, -1, period)
    for prime, width in zip(moduli, widths):
        local_l1.append(sum(local_weight(prime, width, a) for a in range(prime)))
        cofactor = period // prime
        inverses.append(pow(cofactor, -1, prime))
    total_l1 = math.prod(local_l1)

    positive_mass = 0.0
    profile = []
    threshold_index = 0
    for dilated_frequency in range(1, thresholds[-1] + 1):
        weight = 1.0
        global_frequency = inverse_dilation * dilated_frequency
        for prime, width, inverse in zip(moduli, widths, inverses):
            local_frequency = (inverse * global_frequency) % prime
            weight *= local_weight(prime, width, local_frequency)
        positive_mass += weight
        if dilated_frequency == thresholds[threshold_index]:
            centered_mass = 2.0 * positive_mass
            baseline = dilated_frequency * total_l1 / period
            ratio = centered_mass / baseline
            profile.append(
                {
                    "X": dilated_frequency,
                    "centered_arc_mass": centered_mass,
                    "uniform_baseline_X_over_P_times_L": baseline,
                    "ratio_to_stated_one_sided_baseline": ratio,
                    "effective_K": ratio ** (1.0 / rank),
                }
            )
            threshold_index += 1
            if threshold_index == len(thresholds):
                break
    return {
        "status": "finite_diagnostic_only",
        "rank": rank,
        "P": str(period),
        "D_integer": str(density_denominator),
        "h": h,
        "X_min": arc,
        "dilation": dilation,
        "local_l1": local_l1,
        "L": total_l1,
        "dyadic_arc_profile": profile,
        "max_effective_K": max(row["effective_K"] for row in profile),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("k", type=int)
    parser.add_argument("c_num", type=int)
    parser.add_argument("c_den", type=int, nargs="?", default=1)
    parser.add_argument("--max-arc", type=int, default=10_000_000)
    parser.add_argument("--scales", type=int, default=1)
    args = parser.parse_args()
    all_primes = [p for p in primes_below(2 * args.k) if p > args.k]
    widths = [p - args.k for p in all_primes]
    full = scan_system(
        all_primes, widths, args.c_num, args.c_den, 1, args.max_arc, args.scales
    )

    exceptional = None
    if widths and widths[0] == 1:
        exceptional_prime = all_primes[0]
        exceptional = scan_system(
            all_primes[1:],
            widths[1:],
            args.c_num,
            args.c_den,
            exceptional_prime,
            args.max_arc,
            args.scales,
        )
        exceptional["removed_width_one_prime"] = exceptional_prime

    print(
        json.dumps(
            {
                "classification": "finite_discrete_arc_dispersion_diagnostic_only",
                "k": args.k,
                "C": f"{args.c_num}/{args.c_den}",
                "full_system": full,
                "width_one_eliminated_system": exceptional,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
