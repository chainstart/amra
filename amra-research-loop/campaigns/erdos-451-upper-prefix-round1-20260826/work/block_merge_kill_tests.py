#!/usr/bin/env python3
"""Exact adversarial tests for short-window block-merge inequalities."""

from __future__ import annotations

import json
from math import prod


def primes_below(n: int) -> list[int]:
    sieve = [True] * n
    if n:
        sieve[0] = False
    if n > 1:
        sieve[1] = False
    for q in range(2, int(n**0.5) + 1):
        if sieve[q]:
            sieve[q * q : n : q] = [False] * (((n - 1) - q * q) // q + 1)
    return [q for q, ok in enumerate(sieve) if ok]


def scan_case(k: int, old_count: int) -> dict[str, object]:
    ps = [p for p in primes_below(2 * k) if k < p < 2 * k]
    old = ps[:old_count]
    p = ps[old_count]
    q_period = prod(old)
    period = q_period * p
    b = len(old)
    old_ok = [all(n % q == 0 or n % q > k for q in old) for n in range(period)]
    new_ok = [n % p == 0 or n % p > k for n in range(period)]

    # Prefix arrays for old count, new survivors, and each external residue.
    old_prefix = [0]
    new_prefix = [0]
    residue_prefix = [[0] for _ in range(p)]
    for n in range(2 * period):
        idx = n % period
        is_old = old_ok[idx]
        old_prefix.append(old_prefix[-1] + int(is_old))
        new_prefix.append(new_prefix[-1] + int(is_old and new_ok[idx]))
        for a in range(p):
            residue_prefix[a].append(residue_prefix[a][-1] + int(is_old and idx % p == a))

    def count(prefix: list[int], start: int, length: int) -> int:
        return prefix[start + length] - prefix[start]

    lengths = sorted(
        {
            p,
            2 * p,
            q_period,
            min(period, 2 * q_period),
            min(period, 4 * q_period),
            period,
        }
    )
    worst_projection = {"ratio": 1.0}
    worst_discrepancy = {"normalized": 0.0}
    worst_energy = {"normalized_excess": 0.0}
    for length in lengths:
        for start in range(period):
            n_old = count(old_prefix, start, length)
            if not n_old:
                continue
            counts = [count(prefix, start, length) for prefix in residue_prefix]
            projection = sum(c > 0 for c in counts)
            ratio = projection / min(p, n_old)
            if ratio < worst_projection["ratio"]:
                worst_projection = {
                    "ratio": ratio,
                    "start": start,
                    "length": length,
                    "old_count": n_old,
                    "projection_size": projection,
                    "residue_counts": counts,
                }

            survivors = count(new_prefix, start, length)
            alpha_num = p - k
            discrepancy_num = abs(p * survivors - alpha_num * n_old)
            normalized = discrepancy_num / (p * p * (2**b))
            if normalized > worst_discrepancy["normalized"]:
                worst_discrepancy = {
                    "normalized": normalized,
                    "start": start,
                    "length": length,
                    "old_count": n_old,
                    "new_survivors": survivors,
                    "p_times_absolute_conditional_discrepancy": discrepancy_num,
                    "candidate_bound_p_squared_2_to_b": p * p * (2**b),
                }

            energy = sum(c * c for c in counts)
            # p*E-N^2 <= p*2^b*N is the integer form of
            # E <= N^2/p + 2^b N.
            excess_num = max(0, p * energy - n_old * n_old)
            normalized_excess = excess_num / (p * (2**b) * n_old)
            if normalized_excess > worst_energy["normalized_excess"]:
                worst_energy = {
                    "normalized_excess": normalized_excess,
                    "start": start,
                    "length": length,
                    "old_count": n_old,
                    "collision_energy": energy,
                    "pE_minus_N2": excess_num,
                    "candidate_allowance": p * (2**b) * n_old,
                }

    return {
        "k": k,
        "old_primes": old,
        "external_prime": p,
        "old_period_Q": q_period,
        "joint_period_Qp": period,
        "window_lengths": lengths,
        "worst_projection": worst_projection,
        "worst_conditional_discrepancy_C_equals_2": worst_discrepancy,
        "worst_collision_energy_C_equals_2": worst_energy,
    }


def main() -> None:
    cases = [scan_case(10, 2), scan_case(15, 2), scan_case(20, 2)]
    print(
        json.dumps(
            {
                "schema_version": "erdos451.block_merge_kill_tests.v1",
                "candidates": {
                    "projection": "|proj_p(B cap J)| >= 2^{-b} min(p, |B cap J|)",
                    "conditional_discrepancy": "|#(B cap J cap I_p)-(d/p)#(B cap J)| <= p*2^b",
                    "collision_energy": "sum_a multiplicity(a)^2 <= N^2/p+2^b*N"
                },
                "cases": cases,
                "interpretation": "Exact finite falsification only; a passing row is not a theorem.",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
