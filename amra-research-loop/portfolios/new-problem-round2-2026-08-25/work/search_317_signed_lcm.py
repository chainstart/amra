#!/usr/bin/env python3
"""Exact finite search for signed LCM-spacing witnesses in Erdos #317."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import time
from pathlib import Path

import z3


def primes_through(n: int) -> list[int]:
    primes: list[int] = []
    for candidate in range(2, n + 1):
        if all(candidate % p for p in primes if p * p <= candidate):
            primes.append(candidate)
    return primes


def valuation(n: int, p: int) -> int:
    answer = 0
    while n % p == 0:
        answer += 1
        n //= p
    return answer


def exact_mitm(weights: list[int], target: int = 1) -> tuple[bool, list[int] | None]:
    split = len(weights) // 2
    left_weights = weights[:split]
    right_weights = weights[split:]
    left: dict[int, tuple[int, ...]] = {}
    for coeffs in itertools.product((-1, 0, 1), repeat=len(left_weights)):
        value = sum(c * w for c, w in zip(coeffs, left_weights))
        left.setdefault(value, coeffs)
    for right_coeffs in itertools.product((-1, 0, 1), repeat=len(right_weights)):
        right_value = sum(c * w for c, w in zip(right_coeffs, right_weights))
        wanted = target - right_value
        if wanted in left:
            return True, list(left[wanted] + right_coeffs)
    return False, None


def highest_power_residues(n: int, lcm_value: int, coeffs: list[int]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for p in primes_through(n):
        exponent = valuation(lcm_value, p)
        active = [k for k in range(1, n + 1) if valuation(k, p) == exponent]
        terms = [
            {
                "k": k,
                "delta": coeffs[k - 1],
                "weight_mod_p": (lcm_value // k) % p,
            }
            for k in active
            if coeffs[k - 1]
        ]
        residue = sum(item["delta"] * item["weight_mod_p"] for item in terms) % p
        rows.append(
            {
                "prime": p,
                "max_exponent": exponent,
                "active_indices": active,
                "nonzero_witness_terms": terms,
                "residue": residue,
                "expected_residue": 1 % p,
            }
        )
    return rows


def solve_z3(n: int, timeout_ms: int) -> tuple[str, list[int] | None, float]:
    lcm_value = math.lcm(*range(1, n + 1))
    weights = [lcm_value // k for k in range(1, n + 1)]
    variables = [z3.Int(f"d_{n}_{k}") for k in range(1, n + 1)]
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    solver.add(*(z3.Or(d == -1, d == 0, d == 1) for d in variables))
    solver.add(z3.Sum(*(d * w for d, w in zip(variables, weights))) == 1)
    started = time.monotonic()
    result = solver.check()
    elapsed = time.monotonic() - started
    if result == z3.sat:
        model = solver.model()
        coeffs = [model.eval(d).as_long() for d in variables]
        return "sat", coeffs, elapsed
    if result == z3.unsat:
        return "unsat", None, elapsed
    return "unknown", None, elapsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-n", type=int, default=2)
    parser.add_argument("--max-n", type=int, default=80)
    parser.add_argument("--timeout-ms", type=int, default=20_000)
    parser.add_argument("--mitm-through", type=int, default=18)
    parser.add_argument("--z3-through", type=int, default=14)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    started = time.monotonic()
    rows: list[dict[str, object]] = []
    for n in range(args.min_n, args.max_n + 1):
        lcm_value = math.lcm(*range(1, n + 1))
        weights = [lcm_value // k for k in range(1, n + 1)]
        if n <= args.z3_through:
            status, coeffs, elapsed = solve_z3(n, args.timeout_ms)
        else:
            status, coeffs, elapsed = "skipped_after_kill_gate", None, 0.0
        row: dict[str, object] = {
            "n": n,
            "lcm": lcm_value,
            "lcm_decimal_digits": len(str(lcm_value)),
            "solver_status": status,
            "solver_elapsed_seconds": elapsed,
        }
        if n <= args.mitm_through:
            mitm_sat, mitm_coeffs = exact_mitm(weights)
            row["exact_mitm_status"] = "sat" if mitm_sat else "unsat"
            if status in ("sat", "unsat") and ((status == "sat") != mitm_sat):
                raise AssertionError(
                    f"z3/MITM disagreement at n={n}: z3={status}, mitm={mitm_sat}"
                )
            if mitm_coeffs is not None:
                mitm_residual = sum(c * w for c, w in zip(mitm_coeffs, weights))
                if mitm_residual != 1:
                    raise AssertionError(f"invalid MITM witness at n={n}")
                row["mitm_direct_replay_residual"] = mitm_residual
                if coeffs is None:
                    coeffs = mitm_coeffs
        if coeffs is not None:
            residual = sum(c * w for c, w in zip(coeffs, weights))
            if residual != 1:
                raise AssertionError(f"invalid witness at n={n}: residual={residual}")
            row["witness"] = {str(k): c for k, c in enumerate(coeffs, 1) if c}
            row["support_size"] = sum(c != 0 for c in coeffs)
            row["direct_replay_residual"] = residual
            row["highest_prime_power_residues"] = highest_power_residues(n, lcm_value, coeffs)
        rows.append(row)
        print(f"n={n} status={status} elapsed={elapsed:.3f}s", flush=True)

    payload = {
        "schema_version": "amra.erdos317-signed-lcm-evidence.v1",
        "claim_scope": "exact finite solver evidence; no eventual-n inference",
        "parameters": vars(args) | {"output": str(args.output)},
        "resource_guard": {
            "required_slice": "openmath.slice",
            "observed_cgroup": Path("/proc/self/cgroup").read_text().strip(),
            "inside_openmath_slice": "openmath.slice" in Path("/proc/self/cgroup").read_text(),
        },
        "elapsed_seconds": time.monotonic() - started,
        "pid": os.getpid(),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"elapsed_seconds": payload["elapsed_seconds"], "rows": len(rows)}))


if __name__ == "__main__":
    main()
