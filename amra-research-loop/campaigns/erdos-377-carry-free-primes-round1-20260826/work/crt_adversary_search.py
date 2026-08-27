#!/usr/bin/env python3
"""Bounded Max-SMT search for integers carry-free in many small prime bases."""

from __future__ import annotations

import argparse
import json
import math
import time
from fractions import Fraction
from pathlib import Path

import z3


def primes_upto(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [p for p in range(3, limit + 1) if sieve[p]]


def carry_free(n: int, p: int) -> bool:
    half = (p - 1) // 2
    while n:
        if n % p > half:
            return False
        n //= p
    return True


def solve_trial(bound: int, prime_limit: int, timeout_ms: int) -> dict:
    primes = primes_upto(prime_limit)
    solver = z3.Solver()
    n = z3.Int("n")
    solver.add(n >= prime_limit, n <= bound)
    accepted: dict[int, z3.BoolRef] = {}
    scale = 1_000_000
    # Rounded reciprocal weights keep the pseudo-Boolean objective in a small
    # range, allowing certified binary search.  Every returned candidate is
    # ranked and reported again with its exact rational reciprocal mass.
    objective_terms = []
    digit_variable_count = 0
    for p in primes:
        flag = z3.Bool(f"accept_{p}")
        accepted[p] = flag
        quotient = n
        power = 1
        digit_index = 0
        accepted_digits = []
        while power <= bound:
            next_quotient = z3.Int(f"q_{p}_{digit_index + 1}")
            digit = z3.Int(f"d_{p}_{digit_index}")
            solver.add(quotient == p * next_quotient + digit)
            solver.add(digit >= 0, digit < p, next_quotient >= 0)
            accepted_digits.append(digit <= (p - 1) // 2)
            quotient = next_quotient
            power *= p
            digit_index += 1
            digit_variable_count += 1
        solver.add(quotient == 0)
        solver.add(flag == z3.And(accepted_digits))
        objective_terms.append(z3.If(flag, round(scale / p), 0))
    objective = z3.Sum(objective_terms)
    started = time.monotonic()
    deadline = started + timeout_ms / 1000
    lower = 0
    upper = sum(round(scale / p) for p in primes)
    best_model = None
    checks = 0
    status = z3.unknown
    if 3250 <= bound:
        solver.push()
        solver.add(n == 3250)
        solver.set(timeout=max(1, min(5000, timeout_ms // 10)))
        seed_status = solver.check()
        checks += 1
        if seed_status == z3.sat:
            best_model = solver.model()
            lower = best_model.eval(objective, model_completion=True).as_long() + 1
        solver.pop()
    while lower <= upper and time.monotonic() < deadline - 0.05:
        midpoint = (lower + upper) // 2
        solver.push()
        solver.add(objective >= midpoint)
        remaining_ms = max(1, int((deadline - time.monotonic()) * 1000))
        solver.set(timeout=remaining_ms)
        status = solver.check()
        checks += 1
        if status == z3.sat:
            best_model = solver.model()
            achieved = best_model.eval(objective, model_completion=True).as_long()
            lower = max(midpoint, achieved) + 1
        elif status == z3.unsat:
            upper = midpoint - 1
        else:
            solver.pop()
            break
        solver.pop()
    elapsed = time.monotonic() - started
    record = {
        "bound": str(bound),
        "prime_limit": prime_limit,
        "prime_count": len(primes),
        "digit_variable_count": digit_variable_count,
        "timeout_ms": timeout_ms,
        "status": str(status),
        "solver_checks": checks,
        "rounded_objective_upper_after_search": upper,
        "elapsed_seconds": round(elapsed, 4),
    }
    if best_model is not None:
        candidate_n = best_model.eval(n, model_completion=True).as_long()
        model_primes = [p for p in primes if z3.is_true(best_model.eval(accepted[p], model_completion=True))]
        verified_primes = [p for p in primes if carry_free(candidate_n, p)]
        mass = sum((Fraction(1, p) for p in verified_primes), Fraction())
        effective_modulus_product = 1
        for p in verified_primes:
            power = p
            while power <= bound:
                power *= p
            effective_modulus_product *= power
        record.update(
            {
                "n": str(candidate_n),
                "model_accepted_primes": model_primes,
                "verified_accepted_primes": verified_primes,
                "verified_mass": float(mass),
                "verified_mass_exact": f"{mass.numerator}/{mass.denominator}",
                "model_matches_verifier": model_primes == verified_primes,
                "effective_modulus_product_over_bound_log10": (
                    math.log10(effective_modulus_product) - math.log10(bound)
                    if verified_primes
                    else None
                ),
                "rounded_objective": best_model.eval(objective, model_completion=True).as_long(),
                "rounded_optimality_proved": lower == upper + 1 and status != z3.unknown,
            }
        )
    return record


def checkpoint(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=2700)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    deadline = started + args.seconds
    payload = {
        "schema_version": "amra.erdos377.crt-adversary.v1",
        "epistemic_status": "bounded Max-SMT falsification; not an all-n proof",
        "budget_seconds": args.seconds,
        "trials": [],
    }
    schedules = [
        (10**6, 47),
        (10**9, 71),
        (10**12, 97),
        (10**18, 127),
        (10**24, 151),
        (10**30, 181),
        (10**40, 211),
        (10**60, 251),
    ]
    schedule_index = 0
    while time.monotonic() < deadline - 10:
        if schedule_index < len(schedules):
            bound, prime_limit = schedules[schedule_index]
        else:
            # Revisit the hardest scale with a progressively wider prime set;
            # each run has a fresh exact model and a bounded timeout.
            extra = schedule_index - len(schedules)
            prime_limit = min(397, 269 + 16 * extra)
            bound = 10 ** min(100, 50 + 5 * extra)
        schedule_index += 1
        remaining_ms = int((deadline - time.monotonic() - 5) * 1000)
        timeout_ms = max(1000, min(300000, remaining_ms))
        record = solve_trial(bound, prime_limit, timeout_ms)
        payload["trials"].append(record)
        payload["elapsed_seconds"] = round(time.monotonic() - started, 3)
        checkpoint(args.output, payload)
        print(json.dumps(record, sort_keys=True), flush=True)
    payload["completed"] = True
    payload["elapsed_seconds"] = round(time.monotonic() - started, 3)
    checkpoint(args.output, payload)
    print(json.dumps({"completed": True, "elapsed_seconds": payload["elapsed_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
