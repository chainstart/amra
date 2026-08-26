#!/usr/bin/env python3
"""Locate the largest weighted-prefix contributions in small failed rows."""

from __future__ import annotations

import argparse
import heapq
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


def local_phi(residue: int, width: int) -> float:
    r = (width + 1) // 2
    s = width + 1 - r
    absolute = abs(residue)
    numerator = 0.0
    if absolute < r:
        numerator += s * (r - absolute) / r
    if absolute < s:
        numerator += r * (s - absolute) / s
    return numerator / (r + s)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("k", type=int)
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()
    moduli = [p for p in primes_below(2 * args.k) if p > args.k]
    widths = [p - args.k for p in moduli]
    period = math.prod(moduli)
    density_denominator = math.prod(widths)
    rank = len(moduli)
    h = (pow(2, rank) * period + density_denominator - 1) // density_denominator

    heap: list[tuple[float, int, float, list[int]]] = []
    admitted = 0
    positive_mass = 0.0
    for ell in range(1, h):
        product = 1.0
        residues = []
        for prime, width in zip(moduli, widths):
            residue = ell % prime
            if 2 * residue > prime:
                residue -= prime
            residues.append(residue)
            product *= local_phi(residue, width)
            if product == 0.0:
                break
        if product == 0.0:
            continue
        admitted += 1
        contribution = 2.0 * (1.0 - ell / h) * product
        positive_mass += contribution
        row = (contribution, ell, product, residues)
        if len(heap) < args.top:
            heapq.heappush(heap, row)
        elif contribution > heap[0][0]:
            heapq.heapreplace(heap, row)

    rows = [
        {
            "ell": ell,
            "centered_residues": residues,
            "local_product": product,
            "triangular_pair_contribution": contribution,
        }
        for contribution, ell, product, residues in sorted(heap, reverse=True)
    ]
    print(
        json.dumps(
            {
                "classification": "finite_positive_prefix_witness_only",
                "k": args.k,
                "C": "2/1",
                "m": rank,
                "primes": moduli,
                "widths": widths,
                "h": h,
                "admitted_positive_ell": admitted,
                "Q_h": 1.0 + positive_mass,
                "top_contributions": rows,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
