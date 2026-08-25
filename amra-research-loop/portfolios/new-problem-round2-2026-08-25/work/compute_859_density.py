#!/usr/bin/env python3
"""Exact finite diagnostics for Erdos problem 859.

For each t, compute every lcm of a set of distinct positive integers summing
to t.  Minimal elements for divisibility generate A_t as a union of sets of
multiples.  The union density is then evaluated by collapsed, exact
inclusion-exclusion.  No finite output is promoted to an asymptotic claim.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from fractions import Fraction
from pathlib import Path


def minimal_divisibility_generators(values: set[int]) -> list[int]:
    kept: list[int] = []
    for value in sorted(values):
        if not any(value % divisor == 0 for divisor in kept):
            kept.append(value)
    return kept


def exact_union_density(generators: list[int], closure_cap: int) -> tuple[Fraction, int]:
    # Indicator of the current union as sum_m coefficient[m] * 1_{m | n}.
    coefficients: dict[int, int] = {}
    for generator in generators:
        old = tuple(coefficients.items())
        coefficients[generator] = coefficients.get(generator, 0) + 1
        for modulus, coefficient in old:
            joint = math.lcm(modulus, generator)
            coefficients[joint] = coefficients.get(joint, 0) - coefficient
            if coefficients[joint] == 0:
                del coefficients[joint]
        if len(coefficients) > closure_cap:
            raise RuntimeError(
                f"collapsed inclusion-exclusion exceeded closure cap {closure_cap}"
            )
    density = sum((Fraction(c, m) for m, c in coefficients.items()), Fraction())
    return density, len(coefficients)


def brute_period_density(t: int, generators: list[int]) -> tuple[Fraction, int]:
    period = math.lcm(*range(1, t + 1))
    hits = sum(any(n % generator == 0 for generator in generators) for n in range(1, period + 1))
    return Fraction(hits, period), period


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-t", type=int, default=45)
    parser.add_argument("--state-cap", type=int, default=2_000_000)
    parser.add_argument("--closure-cap", type=int, default=2_000_000)
    parser.add_argument("--brute-through", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    started = time.monotonic()
    dp: list[set[int]] = [set() for _ in range(args.max_t + 1)]
    dp[0].add(1)
    stopped_at: int | None = None
    stop_reason: str | None = None
    for part in range(1, args.max_t + 1):
        for total in range(args.max_t - part, -1, -1):
            if not dp[total]:
                continue
            destination = dp[total + part]
            for old_lcm in dp[total]:
                destination.add(math.lcm(old_lcm, part))
            if len(destination) > args.state_cap:
                stopped_at = part
                stop_reason = (
                    f"subset-sum lcm state cap {args.state_cap} exceeded "
                    f"at part={part}, sum={total + part}"
                )
                break
        if stop_reason:
            break

    exact_through = args.max_t if stopped_at is None else stopped_at - 1
    rows: list[dict[str, object]] = []
    for t in range(1, exact_through + 1):
        generators = minimal_divisibility_generators(dp[t])
        try:
            density, closure_terms = exact_union_density(generators, args.closure_cap)
        except RuntimeError as exc:
            stop_reason = str(exc)
            exact_through = t - 1
            break
        brute: dict[str, object] | None = None
        if t <= args.brute_through:
            brute_density, period = brute_period_density(t, generators)
            if brute_density != density:
                raise AssertionError(
                    f"period replay disagrees at t={t}: {brute_density} != {density}"
                )
            brute = {
                "period": period,
                "density_numerator": brute_density.numerator,
                "density_denominator": brute_density.denominator,
            }
        effective_exponent = None
        if t >= 3 and density > 0:
            effective_exponent = -math.log(float(density)) / math.log(math.log(t))
        rows.append(
            {
                "t": t,
                "lcm_state_count": len(dp[t]),
                "minimal_generator_count": len(generators),
                "minimal_generators": generators,
                "collapsed_closure_terms": closure_terms,
                "density_numerator": density.numerator,
                "density_denominator": density.denominator,
                "density_decimal": float(density),
                "effective_exponent_diagnostic": effective_exponent,
                "brute_period_replay": brute,
            }
        )

    payload = {
        "schema_version": "amra.erdos859-density-evidence.v1",
        "claim_scope": "exact finite values only; no asymptotic inference",
        "parameters": {
            "requested_max_t": args.max_t,
            "state_cap": args.state_cap,
            "closure_cap": args.closure_cap,
            "brute_through": args.brute_through,
        },
        "resource_guard": {
            "required_slice": "openmath.slice",
            "observed_cgroup": Path("/proc/self/cgroup").read_text().strip(),
            "inside_openmath_slice": "openmath.slice" in Path("/proc/self/cgroup").read_text(),
        },
        "exact_through": exact_through,
        "stop_reason": stop_reason,
        "elapsed_seconds": time.monotonic() - started,
        "pid": os.getpid(),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: payload[k] for k in ("exact_through", "stop_reason", "elapsed_seconds")}))


if __name__ == "__main__":
    main()
