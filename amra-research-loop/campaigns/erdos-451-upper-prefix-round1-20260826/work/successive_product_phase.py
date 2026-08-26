#!/usr/bin/env python3
"""Exact phase-coherence diagnostics for successive Erdős-451 CRT merges.

This is a falsification/diagnostic program.  It compares deterministic merge
orders and two oracle-greedy orders.  It does not infer an asymptotic theorem
from a finite scan.
"""

from __future__ import annotations

import argparse
import json
from math import ceil, isqrt, log, log1p


def primes_through(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * (n + 1)
    if n >= 0:
        sieve[0] = 0
    if n >= 1:
        sieve[1] = 0
    for a in range(2, isqrt(n) + 1):
        if sieve[a]:
            sieve[a * a : n + 1 : a] = b"\x00" * (((n - a * a) // a) + 1)
    return [a for a in range(2, n + 1) if sieve[a]]


def euclidean_quotients(step: int, p: int) -> list[int]:
    """Partial quotients of p/step, sufficient as a rational-rotation proxy."""

    a, b = p, step
    answer: list[int] = []
    while b:
        answer.append(a // b)
        a, b = b, a % b
    return answer


def scaled_orbit_word(p: int, allowed_width: int, step: int) -> list[int]:
    """p times the centered indicator of [0,allowed_width) along the orbit."""

    return [
        p * int((t * step) % p < allowed_width) - allowed_width
        for t in range(p)
    ]


def full_cyclic_discrepancy_integer(values: list[int]) -> int:
    """Maximum absolute cyclic interval sum for a zero-sum word."""

    assert sum(values) == 0
    prefix = 0
    low = 0
    high = 0
    for value in values:
        prefix += value
        low = min(low, prefix)
        high = max(high, prefix)
    return high - low


def short_cyclic_discrepancy_integer(values: list[int], max_length: int) -> int:
    """Exact maximum over cyclic intervals with 1<=length<=max_length."""

    p = len(values)
    max_length = min(max_length, p)
    best = 0
    doubled = values + values[: max_length - 1]
    for start in range(p):
        total = 0
        for length in range(1, max_length + 1):
            total += doubled[start + length - 1]
            best = max(best, abs(total))
    return best


def largest_orbit_gap(p: int, step: int, count: int) -> int:
    points = sorted({(t * step) % p for t in range(count)})
    assert len(points) == count
    return max(
        points[index + 1] - points[index]
        for index in range(len(points) - 1)
    ) if len(points) > 1 else p


def close_cyclic_gap(p: int, step: int, count: int) -> int:
    points = sorted({(t * step) % p for t in range(count)})
    if len(points) == 1:
        return p
    return max(
        [
            points[index + 1] - points[index]
            for index in range(len(points) - 1)
        ]
        + [p + points[0] - points[-1]]
    )


def cheap_phase_metrics(k: int, p: int, old_product: int) -> dict[str, object]:
    step = old_product % p
    assert step
    width = p - k
    word = scaled_orbit_word(p, width, step)
    full_integer = full_cyclic_discrepancy_integer(word)
    centered = min(step, p - step)
    quotients = euclidean_quotients(step, p)
    return {
        "p": p,
        "allowed_width": width,
        "step_Q_mod_p": step,
        "centered_step": centered,
        "centered_step_ratio": centered / p,
        "full_discrepancy_integer": full_integer,
        "full_discrepancy": full_integer / p,
        "full_discrepancy_over_p": full_integer / (p * p),
        "continued_fraction_quotients": quotients,
        "max_partial_quotient": max(quotients),
        "sum_partial_quotients": sum(quotients),
    }


def add_expensive_metrics(record: dict[str, object]) -> None:
    p = int(record["p"])
    width = int(record["allowed_width"])
    step = int(record["step_Q_mod_p"])
    short_length = ceil(p**0.5)
    word = scaled_orbit_word(p, width, step)
    short_integer = short_cyclic_discrepancy_integer(word, short_length)
    record["short_orbit_length"] = short_length
    record["short_discrepancy_integer"] = short_integer
    record["short_discrepancy"] = short_integer / p
    record["sqrt_orbit_largest_cyclic_gap"] = close_cyclic_gap(
        p, step, short_length
    )


def alternating_order(ps: list[int]) -> list[int]:
    answer: list[int] = []
    low = 0
    high = len(ps) - 1
    while low <= high:
        answer.append(ps[low])
        low += 1
        if low <= high:
            answer.append(ps[high])
            high -= 1
    return answer


def greedy_order(k: int, ps: list[int], criterion: str) -> list[int]:
    remaining = set(ps)
    # Fix the first coordinate at the smallest prime.  Phase diagnostics begin
    # with the second coordinate; optimizing the empty old product is vacuous.
    order = [min(remaining)]
    remaining.remove(order[0])
    old_product = order[0]
    while remaining:
        scored: list[tuple[tuple[float, ...], int]] = []
        for p in sorted(remaining):
            record = cheap_phase_metrics(k, p, old_product)
            if criterion == "discrepancy":
                key = (
                    float(record["full_discrepancy"]),
                    -float(record["centered_step_ratio"]),
                    float(p),
                )
            elif criterion == "centered_step":
                key = (
                    -float(record["centered_step_ratio"]),
                    float(record["full_discrepancy"]),
                    float(p),
                )
            else:
                raise ValueError(criterion)
            scored.append((key, p))
        selected = min(scored)[1]
        order.append(selected)
        remaining.remove(selected)
        old_product *= selected
    return order


def diagnose_order(k: int, order: list[int]) -> dict[str, object]:
    old_product = order[0]
    rows: list[dict[str, object]] = []
    for index, p in enumerate(order[1:], start=1):
        record = cheap_phase_metrics(k, p, old_product)
        add_expensive_metrics(record)
        record["merge_index_zero_based"] = index
        rows.append(record)
        old_product *= p

    sum_log_discrepancy = sum(log1p(float(row["full_discrepancy"])) for row in rows)
    sum_log_cf = sum(log1p(int(row["max_partial_quotient"])) for row in rows)
    sum_log_inverse_centered = sum(
        log(int(row["p"]) / int(row["centered_step"])) for row in rows
    )
    worst = max(rows, key=lambda row: float(row["full_discrepancy_over_p"]))
    return {
        "prime_count": len(order),
        "order": order,
        "cumulative_proxies": {
            "sum_log_1_plus_full_discrepancy": sum_log_discrepancy,
            "sum_log_1_plus_max_partial_quotient": sum_log_cf,
            "sum_log_p_over_centered_step": sum_log_inverse_centered,
            "sum_log_1_plus_full_discrepancy_over_k": sum_log_discrepancy / k,
            "near_unit_phase_count_centered_step_at_most_2": sum(
                int(int(row["centered_step"]) <= 2) for row in rows
            ),
            "macroscopic_discrepancy_count_at_least_p_over_5": sum(
                int(float(row["full_discrepancy_over_p"]) >= 0.2)
                for row in rows
            ),
        },
        "worst_full_discrepancy_row": worst,
        "rows": rows,
    }


def parse_k_values(text: str) -> list[int]:
    return sorted({int(piece) for piece in text.split(",") if piece.strip()})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--k-values",
        default="10,20,50,83,100,200,271,400,650,760,1000,1480",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="omit complete order and per-merge rows from the JSON report",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="with --summary-only, retain only selected cumulative and worst-row fields",
    )
    args = parser.parse_args()
    k_values = parse_k_values(args.k_values)
    all_primes = primes_through(2 * max(k_values))
    cases: list[dict[str, object]] = []
    for k in k_values:
        ps = [p for p in all_primes if k < p < 2 * k]
        if len(ps) < 2:
            continue
        orders = {
            "increasing": ps,
            "decreasing": list(reversed(ps)),
            "alternating_low_high": alternating_order(ps),
            "greedy_min_full_discrepancy": greedy_order(k, ps, "discrepancy"),
            "greedy_max_centered_step": greedy_order(k, ps, "centered_step"),
        }
        diagnoses = {
            name: diagnose_order(k, order) for name, order in orders.items()
        }
        if args.summary_only:
            for diagnosis in diagnoses.values():
                diagnosis.pop("order")
                diagnosis.pop("rows")
                if args.compact:
                    cumulative = diagnosis["cumulative_proxies"]
                    diagnosis["cumulative_proxies"] = {
                        key: cumulative[key]
                        for key in (
                            "sum_log_1_plus_full_discrepancy",
                            "sum_log_1_plus_full_discrepancy_over_k",
                            "sum_log_1_plus_max_partial_quotient",
                            "sum_log_p_over_centered_step",
                            "near_unit_phase_count_centered_step_at_most_2",
                            "macroscopic_discrepancy_count_at_least_p_over_5",
                        )
                    }
                    worst = diagnosis["worst_full_discrepancy_row"]
                    diagnosis["worst_full_discrepancy_row"] = {
                        key: worst[key]
                        for key in (
                            "merge_index_zero_based",
                            "p",
                            "allowed_width",
                            "step_Q_mod_p",
                            "centered_step",
                            "full_discrepancy",
                            "full_discrepancy_over_p",
                            "short_orbit_length",
                            "short_discrepancy",
                            "max_partial_quotient",
                            "sqrt_orbit_largest_cyclic_gap",
                        )
                    }
        cases.append(
            {
                "k": k,
                "interval_prime_count": len(ps),
                **({} if args.summary_only else {"interval_primes": ps}),
                "orders": diagnoses,
            }
        )
    print(
        json.dumps(
            {
                "schema_version": "erdos451.successive_product_phase.v1",
                "definitions": {
                    "phase_step": "Q_old mod p_new",
                    "centered_step": "min(step,p-step)",
                    "full_discrepancy": "max over all orbit starts and lengths of |#hits-T(p-k)/p| for the fixed aligned interval [0,p-k)",
                    "short_discrepancy": "the same maximum with length at most ceil(sqrt(p))",
                    "sqrt_orbit_largest_cyclic_gap": "largest cyclic gap among the first ceil(sqrt(p)) multiples of the phase step",
                    "cumulative_proxies": "diagnostics only; no proved block recursion currently multiplies these quantities",
                },
                "cases": cases,
                "interpretation": "Every row is exact finite arithmetic. Greedy orders are oracle diagnostics, not a constructive asymptotic theorem. Passing behavior is not proof.",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
