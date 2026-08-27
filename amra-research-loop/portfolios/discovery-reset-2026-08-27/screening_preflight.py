#!/usr/bin/env python3
"""Reproduce the bounded preflight checks used in the 2026-08-27 screening.

The checks are admission evidence only.  A bounded failure is never reported as
a resolution of either open problem.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from typing import Any

from sympy import primerange
from z3 import Int, Or, Solver, sat


def erdos_273_preflight(prime_cap: int) -> dict[str, Any]:
    reciprocal_sum = 0.0
    selected_primes: list[int] = []
    for prime in primerange(5, prime_cap + 1):
        selected_primes.append(int(prime))
        reciprocal_sum += 1.0 / (int(prime) - 1)
        if reciprocal_sum >= 1.0:
            break
    if reciprocal_sum < 1.0:
        raise RuntimeError(f"reciprocal sum stayed below one through {prime_cap}")

    moduli = [prime - 1 for prime in selected_primes]
    period = math.lcm(*moduli)
    return {
        "first_prime_bound": selected_primes[-1],
        "primes": selected_primes,
        "moduli": moduli,
        "moduli_count": len(moduli),
        "reciprocal_sum": reciprocal_sum,
        "lcm": period,
        "lcm_bits": period.bit_length(),
        "single_period_bitset_mib": period / 8 / 1024 / 1024,
    }


def factor_exponents(
    value: int, primes: list[int], prime_index: dict[int, int]
) -> list[tuple[int, int]]:
    remainder = value
    factors: list[tuple[int, int]] = []
    for index, prime in enumerate(primes):
        if prime * prime > remainder:
            break
        if remainder % prime:
            continue
        exponent = 0
        while remainder % prime == 0:
            remainder //= prime
            exponent += 1
        factors.append((index, exponent))
        if remainder == 1:
            break
    if remainder > 1:
        factors.append((prime_index[remainder], 1))
    return factors


def erdos_436_preflight(
    r_values: list[int], solver_timeout_ms: int
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for bound in r_values:
        primes = [int(prime) for prime in primerange(2, bound + 3)]
        prime_index = {prime: index for index, prime in enumerate(primes)}
        variables = [Int(f"character_{bound}_{prime}") for prime in primes]
        solver = Solver()
        solver.set(timeout=solver_timeout_ms)
        for variable in variables:
            solver.add(variable >= 0, variable < 5)

        labels = []
        for value in range(1, bound + 3):
            terms = [
                exponent * variables[index]
                for index, exponent in factor_exponents(value, primes, prime_index)
            ]
            labels.append((sum(terms) if terms else 0) % 5)
        for index in range(bound):
            solver.add(
                Or(
                    labels[index] != 0,
                    labels[index + 1] != 0,
                    labels[index + 2] != 0,
                )
            )

        started = time.monotonic()
        status = solver.check()
        elapsed = time.monotonic() - started
        results.append(
            {
                "R": bound,
                "status": str(status),
                "seconds": elapsed,
                "prime_variables": len(primes),
            }
        )
        if status != sat:
            break
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime-cap", type=int, default=1_000_000)
    parser.add_argument(
        "--r-values", type=int, nargs="+", default=[30, 60, 120, 240, 480]
    )
    parser.add_argument("--solver-timeout-ms", type=int, default=20_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = {
        "schema_version": "amra.discovery-screening-preflight.v1",
        "scope": "bounded admission checks; no open-problem resolution claim",
        "erdos_273": erdos_273_preflight(args.prime_cap),
        "erdos_436": erdos_436_preflight(args.r_values, args.solver_timeout_ms),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
