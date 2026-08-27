#!/usr/bin/env python3
"""Exact counterexample search for three short-window block-merge candidates.

This is deliberately a falsification script, not evidence for a universal
statement.  All intervals are half-open as integer windows and cyclic in the
corresponding residue group.  The structured search uses one old modulus q,
the allowed interval [0,d), and

    J = [0, (t-1)q+d),

so that X=B cap J consists of exactly t complete blocks of d consecutive
integers.  This already suffices to test the proposed universal bounds.  A
separate small exhaustive search checks every window modulo pq for b=1.
"""

from __future__ import annotations

import argparse
import json
from math import gcd
from typing import Iterable


def primes_through(n: int) -> list[int]:
    sieve = [True] * (n + 1)
    if n >= 0:
        sieve[0] = False
    if n >= 1:
        sieve[1] = False
    for a in range(2, int(n**0.5) + 1):
        if sieve[a]:
            sieve[a * a : n + 1 : a] = [False] * (((n - a * a) // a) + 1)
    return [a for a, ok in enumerate(sieve) if ok]


def max_abs_cyclic_interval_sum(values: list[int]) -> tuple[int, int, int, int]:
    """Return |sum|, start, width, signed sum for a nonempty cyclic interval.

    The input has sum zero in our application.  A wrapping interval is the
    negative of its nonwrapping complement, so scanning all ordinary
    intervals also gets the cyclic optimum (the full interval contributes 0).
    Ties are broken by (start,width,signed_sum).
    """

    best: tuple[int, int, int, int] | None = None
    prefix = 0
    min_prefix = 0
    min_index = 0
    max_prefix = 0
    max_index = 0
    for end, value in enumerate(values, start=1):
        prefix += value
        candidates = (
            (abs(prefix - min_prefix), min_index, end - min_index, prefix - min_prefix),
            (abs(prefix - max_prefix), max_index, end - max_index, prefix - max_prefix),
        )
        for candidate in candidates:
            if best is None or candidate[0] > best[0] or (
                candidate[0] == best[0] and candidate[1:] < best[1:]
            ):
                best = candidate
        if prefix < min_prefix:
            min_prefix = prefix
            min_index = end
        if prefix > max_prefix:
            max_prefix = prefix
            max_index = end
    assert best is not None
    return best


def evaluate_counts(
    *, q: int, p: int, d: int, t: int, counts: list[int], family: str
) -> dict[str, dict[str, object]]:
    b = 1
    two_to_b = 2
    n_points = d * t
    window_length = (t - 1) * q + d
    projection = [a for a, count in enumerate(counts) if count]
    energy = sum(count * count for count in counts)

    centered_integer = [p * count - n_points for count in counts]
    discrepancy_num, interval_start, interval_width, signed_num = (
        max_abs_cyclic_interval_sum(centered_integer)
    )
    if signed_num < 0:
        # Complementing gives the positive discrepancy with the same absolute
        # value and makes the reported survivor count easier to inspect.
        interval_start = (interval_start + interval_width) % p
        interval_width = p - interval_width
        signed_num = -signed_num
    external_interval = [
        (interval_start + offset) % p for offset in range(interval_width)
    ]
    external_count = sum(counts[a] for a in external_interval)
    assert signed_num == p * external_count - interval_width * n_points

    common = {
        "family": family,
        "b": b,
        "old_moduli": [q],
        "old_cyclic_intervals": [{"start": 0, "width": d}],
        "external_modulus_p": p,
        "gcd_q_p": gcd(q, p),
        "window_J_half_open": [0, window_length],
        "block_count_t": t,
        "X_size_N": n_points,
        "projection_residues": projection,
        "residue_multiplicities": counts,
    }
    return {
        "P1": {
            **common,
            "integer_test": {
                "lhs_2_to_b_times_projection_size": two_to_b * len(projection),
                "rhs_min_p_N": min(p, n_points),
                "violates": two_to_b * len(projection) < min(p, n_points),
            },
        },
        "P2": {
            **common,
            "external_cyclic_interval": {
                "start": interval_start,
                "width_d": interval_width,
                "X_intersection_size": external_count,
            },
            "integer_test": {
                "lhs_abs_p_times_count_minus_dN": discrepancy_num,
                "rhs_p_squared_times_2_to_b": p * p * two_to_b,
                "violates": discrepancy_num > p * p * two_to_b,
            },
        },
        "P3": {
            **common,
            "collision_energy_E": energy,
            "integer_test": {
                "lhs_pE": p * energy,
                "rhs_N_squared_plus_p_times_2_to_b_times_N": (
                    n_points * n_points + p * two_to_b * n_points
                ),
                "violates": (
                    p * energy
                    > n_points * n_points + p * two_to_b * n_points
                ),
            },
        },
    }


def structured_counts(q: int, p: int, d: int, t: int) -> list[int]:
    counts = [0] * p
    for block in range(t):
        base = block * q
        for offset in range(d):
            counts[(base + offset) % p] += 1
    return counts


def first_structured_counterexamples(
    pairs: Iterable[tuple[int, int]], family: str
) -> dict[str, dict[str, object] | None]:
    """Least examples in the explicit pair order, then d, then t."""

    answer: dict[str, dict[str, object] | None] = {
        "P1": None,
        "P2": None,
        "P3": None,
    }
    for p, q in pairs:
        assert gcd(p, q) == 1
        for d in range(1, q + 1):
            for t in range(1, p + 1):
                records = evaluate_counts(
                    q=q,
                    p=p,
                    d=d,
                    t=t,
                    counts=structured_counts(q, p, d, t),
                    family=family,
                )
                for name in answer:
                    if answer[name] is None and records[name]["integer_test"]["violates"]:
                        answer[name] = records[name]
        if all(record is not None for record in answer.values()):
            break
    return answer


def counts_for_window(q: int, p: int, d: int, start: int, length: int) -> list[int]:
    counts = [0] * p
    for n in range(start, start + length):
        if n % q < d:
            counts[n % p] += 1
    return counts


def evaluate_arbitrary_window(
    *, q: int, p: int, d: int, start: int, length: int, counts: list[int]
) -> dict[str, dict[str, object]]:
    n_points = sum(counts)
    projection = [a for a, count in enumerate(counts) if count]
    energy = sum(count * count for count in counts)
    centered_integer = [p * count - n_points for count in counts]
    discrepancy_num, interval_start, interval_width, signed_num = (
        max_abs_cyclic_interval_sum(centered_integer)
    )
    if signed_num < 0:
        interval_start = (interval_start + interval_width) % p
        interval_width = p - interval_width
        signed_num = -signed_num
    external_residues = [
        (interval_start + offset) % p for offset in range(interval_width)
    ]
    external_count = sum(counts[a] for a in external_residues)
    assert signed_num == p * external_count - interval_width * n_points
    common = {
        "family": "all b=1 windows in the stated finite range",
        "b": 1,
        "old_moduli": [q],
        "old_cyclic_intervals": [{"start": 0, "width": d}],
        "external_modulus_p": p,
        "window_J_half_open": [start, start + length],
        "X_size_N": n_points,
        "projection_residues": projection,
        "residue_multiplicities": counts,
    }
    return {
        "P1": {
            **common,
            "integer_test": {
                "lhs_2_to_b_times_projection_size": 2 * len(projection),
                "rhs_min_p_N": min(p, n_points),
                "violates": 2 * len(projection) < min(p, n_points),
            },
        },
        "P2": {
            **common,
            "external_cyclic_interval": {
                "start": interval_start,
                "width_d": interval_width,
                "X_intersection_size": external_count,
            },
            "integer_test": {
                "lhs_abs_p_times_count_minus_dN": discrepancy_num,
                "rhs_p_squared_times_2_to_b": 2 * p * p,
                "violates": discrepancy_num > 2 * p * p,
            },
        },
        "P3": {
            **common,
            "collision_energy_E": energy,
            "integer_test": {
                "lhs_pE": p * energy,
                "rhs_N_squared_plus_p_times_2_to_b_times_N": (
                    n_points * n_points + 2 * p * n_points
                ),
                "violates": p * energy > n_points * n_points + 2 * p * n_points,
            },
        },
    }


def exhaustive_small_b1(max_q: int, max_p: int) -> dict[str, object]:
    """Check all nonempty windows of length <pq in a small exact range.

    Fixing the old interval start at zero loses no cases: a global integer
    translation moves its start to zero and merely translates J and the
    arbitrary external cyclic interval.
    """

    first: dict[str, dict[str, object] | None] = {
        "P1": None,
        "P2": None,
        "P3": None,
    }
    tested_windows = 0
    tested_boxes = 0
    primes = primes_through(max_p)
    for p in primes:
        for q in range(2, max_q + 1):
            if gcd(q, p) != 1:
                continue
            period = p * q
            for d in range(1, q + 1):
                tested_boxes += 1
                for start in range(period):
                    counts = [0] * p
                    for length in range(1, period):
                        n = start + length - 1
                        if n % q < d:
                            counts[n % p] += 1
                        tested_windows += 1
                        if not any(counts):
                            continue
                        records = evaluate_arbitrary_window(
                            q=q,
                            p=p,
                            d=d,
                            start=start,
                            length=length,
                            counts=counts.copy(),
                        )
                        for name in first:
                            if (
                                first[name] is None
                                and records[name]["integer_test"]["violates"]
                            ):
                                first[name] = records[name]
    return {
        "scope": {
            "b": 1,
            "old_modulus_q": [2, max_q],
            "external_p": f"every prime <= {max_p} coprime to q",
            "old_width": "every 1<=d<=q; old start fixed to 0 by translation",
            "window_start": "every residue modulo pq",
            "window_length": "every 1<=L<pq",
            "external_interval_for_P2": "every cyclic interval (optimized exactly)",
            "tested_boxes": tested_boxes,
            "tested_windows": tested_windows,
        },
        "first_counterexamples_in_loop_order": first,
    }


def aligned_451_structured(max_k: int) -> dict[str, object]:
    """Search the b=1 family with the exact 451 interval widths and starts.

    Translating n by -(k+1) simultaneously changes both actual allowed arcs
    {k+1,...,q-1,0} and {k+1,...,p-1,0} to arcs starting at zero.  We search
    J'=[0,(t-1)q+(q-k)) in this normalized coordinate and report J in the
    original coordinate as well.
    """

    primes = primes_through(2 * max_k)
    first: dict[str, dict[str, object] | None] = {
        "P1": None,
        "P2": None,
        "P3": None,
    }
    tested = 0
    for k in range(2, max_k + 1):
        interval_primes = [q for q in primes if k < q < 2 * k]
        for p in interval_primes:
            for q in [r for r in interval_primes if r < p]:
                old_width = q - k
                external_width = p - k
                for t in range(1, p + 1):
                    tested += 1
                    counts = structured_counts(q, p, old_width, t)
                    n_points = old_width * t
                    projection = [a for a, count in enumerate(counts) if count]
                    energy = sum(count * count for count in counts)
                    normalized_length = (t - 1) * q + old_width
                    common = {
                        "family": "exact 451-aligned one-old-prime block family",
                        "k": k,
                        "b": 1,
                        "old_prime_q": q,
                        "external_prime_p": p,
                        "original_old_allowed_cyclic_interval": {
                            "start": k + 1,
                            "width": old_width,
                        },
                        "original_external_allowed_cyclic_interval": {
                            "start": k + 1,
                            "width": external_width,
                        },
                        "normalizing_translation": "n' = n-(k+1)",
                        "normalized_window_J_half_open": [0, normalized_length],
                        "original_window_J_half_open": [
                            k + 1,
                            k + 1 + normalized_length,
                        ],
                        "block_count_t": t,
                        "X_size_N": n_points,
                        "projection_residues_in_normalized_coordinate": projection,
                        "residue_multiplicities_in_normalized_coordinate": counts,
                    }
                    if first["P1"] is None and 2 * len(projection) < min(p, n_points):
                        first["P1"] = {
                            **common,
                            "integer_test": {
                                "lhs_2_to_b_times_projection_size": 2 * len(projection),
                                "rhs_min_p_N": min(p, n_points),
                                "violates": True,
                            },
                        }
                    external_count = sum(counts[:external_width])
                    discrepancy_num = abs(
                        p * external_count - external_width * n_points
                    )
                    if first["P2"] is None and discrepancy_num > 2 * p * p:
                        first["P2"] = {
                            **common,
                            "X_intersection_external_allowed_size": external_count,
                            "integer_test": {
                                "lhs_abs_p_times_count_minus_dN": discrepancy_num,
                                "rhs_p_squared_times_2_to_b": 2 * p * p,
                                "violates": True,
                            },
                        }
                    if (
                        first["P3"] is None
                        and p * energy > n_points * n_points + 2 * p * n_points
                    ):
                        first["P3"] = {
                            **common,
                            "collision_energy_E": energy,
                            "integer_test": {
                                "lhs_pE": p * energy,
                                "rhs_N_squared_plus_p_times_2_to_b_times_N": (
                                    n_points * n_points + 2 * p * n_points
                                ),
                                "violates": True,
                            },
                        }
        if all(record is not None for record in first.values()):
            return {
                "scope": f"increasing k<= {max_k}; every q<p in (k,2k); every 1<=t<=p",
                "ordering": "k, then p, then q, then t, all increasing",
                "tested_parameter_tuples_until_all_found": tested,
                "first_counterexamples_in_that_order": first,
            }
    return {
        "scope": f"every k<= {max_k}; every q<p in (k,2k); every 1<=t<=p",
        "ordering": "k, then p, then q, then t, all increasing",
        "tested_parameter_tuples": tested,
        "first_counterexamples_in_that_order": first,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-q-exhaustive", type=int, default=10)
    parser.add_argument("--max-p-exhaustive", type=int, default=11)
    parser.add_argument("--max-p-structured", type=int, default=101)
    parser.add_argument("--max-k-451-aligned", type=int, default=100)
    args = parser.parse_args()

    primes = primes_through(args.max_p_structured)
    q_equals_p_plus_one = [(p, p + 1) for p in primes]
    increasing_prime_pairs = [
        (p, q)
        for p in primes
        for q in reversed([r for r in primes if r < p][-4:])
    ]

    report = {
        "schema_version": "erdos451.generic_block_merge_search.v1",
        "candidate_integer_forms": {
            "P1": "2^b |proj_p X| >= min(p,N)",
            "P2": "|p |X cap I|-dN| <= p^2 2^b for every cyclic I of width d",
            "P3": "p E_p(X) <= N^2+p 2^b N",
        },
        "structured_q_equals_p_plus_one": {
            "ordering": "increasing external prime p, then d, then t",
            "scope": f"every prime p<={args.max_p_structured}, q=p+1, 1<=d<=q, 1<=t<=p",
            "first_counterexamples": first_structured_counterexamples(
                q_equals_p_plus_one, "q=p+1 block-convolution family"
            ),
        },
        "structured_increasing_prime_pairs": {
            "ordering": "increasing external prime p; previous primes q in decreasing order; then d,t",
            "scope": (
                f"every prime p<={args.max_p_structured}, the four largest primes q<p, "
                "1<=d<=q, 1<=t<=p"
            ),
            "first_counterexamples": first_structured_counterexamples(
                increasing_prime_pairs,
                "old prime q < external prime p block-convolution family",
            ),
        },
        "structured_exact_451_aligned": aligned_451_structured(
            args.max_k_451_aligned
        ),
        "exhaustive_small_b1": exhaustive_small_b1(
            args.max_q_exhaustive, args.max_p_exhaustive
        ),
        "interpretation": (
            "A counterexample is exact and refutes the corresponding universal constant-2 "
            "candidate. Absence in a reported finite scope is finite evidence only."
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
