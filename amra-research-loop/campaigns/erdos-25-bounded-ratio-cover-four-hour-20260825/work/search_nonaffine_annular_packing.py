#!/usr/bin/env python3
"""Search target-irredundant non-affine perturbations of multiplication batches."""

from __future__ import annotations

import argparse
import collections
import json
import math
import os
import random
import time
from pathlib import Path


MASK64 = (1 << 64) - 1
MAX_AFFINE_SLOPE = 16


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def splitmix64(value: int) -> int:
    value = (value + 0x9E3779B97F4A7C15) & MASK64
    value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
    value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & MASK64
    return value ^ (value >> 31)


def offsets_for(policy: str, n: int, start: int, gap: int, rng: random.Random) -> list[int]:
    maximum = max(1, start // 2)
    initial = rng.randint(max(2, int(math.sqrt(n))), maximum)
    if policy == "linear":
        final = rng.randint(1, max(1, initial // 3))
        return [initial - ((initial - final) * index // max(1, n - 1)) for index in range(n)]
    if policy == "power":
        exponent = rng.uniform(0.35, 3.5)
        final = rng.randint(1, max(1, initial // 4))
        return [
            final + int((initial - final) * (1.0 - index / max(1, n - 1)) ** exponent)
            for index in range(n)
        ]
    if policy == "blocks":
        block_count = rng.randint(max(2, int(math.sqrt(n) / 2)), max(3, int(2 * math.sqrt(n))))
        levels = sorted({rng.randint(1, initial) for _ in range(3 * block_count)}, reverse=True)
        levels = levels[:block_count]
        while len(levels) < block_count:
            levels.append(1)
        levels.sort(reverse=True)
        return [levels[min(block_count - 1, index * block_count // n)] for index in range(n)]
    if policy == "random_staircase":
        total_drop = rng.randint(max(1, initial // 3), initial - 1)
        cuts = sorted(rng.randrange(n) for _ in range(total_drop))
        counts = collections.Counter(cuts)
        current = initial
        result = []
        for index in range(n):
            current = max(1, current - counts[index])
            result.append(current)
        return result
    if policy == "sawtooth":
        period = rng.randint(max(3, int(math.sqrt(n) / 2)), max(4, int(2 * math.sqrt(n))))
        current = rng.randint(max(2, int(math.sqrt(n))), maximum)
        result = []
        for index in range(n):
            result.append(current)
            if (index + 1) % period == 0:
                current = max(1, current - rng.randint(1, max(1, period * gap)))
            else:
                current = min((start + gap * (index + 1)) // 2, current + rng.randrange(gap))
        return result
    if policy == "bounded_walk":
        current = rng.randint(max(2, int(math.sqrt(n))), maximum)
        result = []
        for index in range(n):
            result.append(current)
            change = rng.randint(-2 * gap, gap - 1)
            current = min(
                (start + gap * (index + 1)) // 2,
                max(1, current + change),
            )
        return result
    raise ValueError(policy)


def simulate(n: int, start: int, gap: int, policy: str, seed: int) -> dict | None:
    rng = random.Random(seed)
    offsets = offsets_for(policy, n, start, gap, rng)
    if any(right - left >= gap for left, right in zip(offsets, offsets[1:])):
        raise AssertionError("offset increase would violate target monotonicity")
    moduli = [start + gap * index for index in range(n)]
    targets = [modulus - offset for modulus, offset in zip(moduli, offsets)]
    if any(not (0 < target < modulus <= 2 * target) for target, modulus in zip(targets, moduli)):
        return None
    if any(left >= right for left, right in zip(targets, targets[1:])):
        raise AssertionError("targets must strictly increase")
    # The annular choice start > gap*n and offset <= start/2 makes the full
    # target span smaller than twice the least modulus.  Consequently an
    # earlier progression can cover a later target only at its first echo.
    # Keep this geometric premise executable rather than silently relying on
    # it in the cheaper irredundancy check below.
    if targets[-1] - targets[0] >= 2 * moduli[0]:
        raise AssertionError("target span permits an unchecked higher echo")
    earlier_echoes: set[int] = set()
    for target, modulus in zip(targets, moduli):
        if target in earlier_echoes:
            return None
        earlier_echoes.add(target + modulus)

    union: set[int] = set()
    for target, modulus in zip(targets, moduli):
        union.update(range(target, target + n * modulus, modulus))
    counts = collections.Counter(offsets)
    distinct_offsets = len(counts)
    largest_offset_chart = max(counts.values())
    affine_counts = collections.Counter(
        (slope, modulus - slope * target)
        for target, modulus in zip(targets, moduli)
        for slope in range(1, MAX_AFFINE_SLOPE + 1)
    )
    largest_affine_parameters, largest_affine_chart = max(
        affine_counts.items(), key=lambda item: item[1]
    )
    compatible_pairs = 0
    compatible_gcd_weight = 0.0
    for right in range(1, n):
        for left in range(right):
            gcd = math.gcd(moduli[left], moduli[right])
            if (offsets[left] - offsets[right]) % gcd == 0:
                compatible_pairs += 1
                compatible_gcd_weight += gcd / moduli[right]
    pair_count = n * (n - 1) // 2
    union_hash = 0
    for value in union:
        union_hash ^= splitmix64(value)
    return {
        "N": n,
        "modulus_start": start,
        "modulus_gap": gap,
        "modulus_end": start + gap * (n - 1),
        "policy": policy,
        "schedule_seed": seed,
        "target_minimum": targets[0],
        "target_maximum": targets[-1],
        "maximum_step_to_target_ratio": max(d / r for r, d in zip(targets, moduli)),
        "target_irredundant": True,
        "incidences": n * n,
        "distinct_union_points": len(union),
        "distinct_union_fraction": len(union) / (n * n),
        "collision_fraction": 1.0 - len(union) / (n * n),
        "distinct_offsets": distinct_offsets,
        "distinct_offset_fraction": distinct_offsets / n,
        "largest_affine_offset_chart": largest_offset_chart,
        "largest_affine_offset_chart_fraction": largest_offset_chart / n,
        "largest_integer_affine_chart": largest_affine_chart,
        "largest_integer_affine_chart_fraction": largest_affine_chart / n,
        "largest_integer_affine_chart_parameters": {
            "c": largest_affine_parameters[0],
            "b": largest_affine_parameters[1],
        },
        "crt_compatible_pairs": compatible_pairs,
        "crt_compatible_pair_fraction": compatible_pairs / max(1, pair_count),
        "crt_compatible_gcd_weight": compatible_gcd_weight,
        "crt_compatible_gcd_weight_per_class": compatible_gcd_weight / n,
        "offset_minimum": min(offsets),
        "offset_maximum": max(offsets),
        "offsets": offsets,
        "union_commutative_hash64": f"{union_hash:016x}",
        "finite_scope": "First N terms of N exact progressions; no infinite density conclusion.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=2700)
    parser.add_argument("--seed", type=int, default=25082517)
    parser.add_argument("--max-n", type=int, default=1800)
    parser.add_argument("--checkpoint-seconds", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    started_wall = time.time()
    started = time.monotonic()
    deadline = started + args.seconds
    next_checkpoint = started + min(args.checkpoint_seconds, args.seconds)
    next_report = started + 60
    trials = simulated = incidences = 0
    best = None
    strata: dict[str, dict] = {}
    policies = ["linear", "power", "blocks", "random_staircase", "sawtooth", "bounded_walk"]

    def score(row: dict) -> tuple:
        qualifies = (
            row["distinct_offsets"] >= math.sqrt(row["N"])
            and row["largest_integer_affine_chart_fraction"] <= 0.5
        )
        return (
            0 if qualifies else 1,
            row["distinct_union_fraction"],
            row["largest_integer_affine_chart_fraction"],
            -row["distinct_offset_fraction"],
        )

    def snapshot(status: str) -> dict:
        return {
            "schema_version": "erdos-25.nonaffine-annular-packing-search.v1",
            "status": status,
            "guard_required": True,
            "seed": args.seed,
            "requested_seconds": args.seconds,
            "max_n": args.max_n,
            "started_unix": started_wall,
            "elapsed_seconds": time.monotonic() - started,
            "trials": trials,
            "simulated_target_irredundant_batches": simulated,
            "exact_progression_incidences": incidences,
            "best_genuinely_nonaffine_batch": best,
            "best_by_policy_and_scale": strata,
            "score_gate": "at least sqrt(N) distinct offsets and no integer affine chart d=cr+b (1<=c<=16, enough to capture any majority chart in the sampled gap range) containing more than half the batch",
            "interpretation_limit": "Finite near-extremizer search only; a small union is not an infinite counterexample and a large union is not a rigidity theorem.",
        }

    while time.monotonic() < deadline:
        n = max(48, min(args.max_n, int(10 ** rng.uniform(math.log10(48), math.log10(args.max_n)))))
        gap = rng.choice([1, 2, 3, 4, 6, 8])
        start = rng.randint(gap * n + 1, 3 * gap * n)
        policy = rng.choice(policies)
        schedule_seed = rng.randrange(2**63)
        row = simulate(n, start, gap, policy, schedule_seed)
        trials += 1
        if row is not None:
            simulated += 1
            incidences += n * n
            if best is None or score(row) < score(best):
                best = row
            key = f"policy={policy};gap={gap};floor_log2_N={n.bit_length()-1}"
            old = strata.get(key)
            if old is None or score(row) < score(old):
                strata[key] = row
        now = time.monotonic()
        if now >= next_checkpoint:
            atomic_json(args.output, snapshot("running"))
            next_checkpoint = now + args.checkpoint_seconds
        if now >= next_report:
            print(json.dumps({
                "elapsed_seconds": round(now - started, 1),
                "trials": trials,
                "simulated": simulated,
                "exact_progression_incidences": incidences,
                "best_distinct_union_fraction": None if best is None else best["distinct_union_fraction"],
                "best_distinct_offsets": None if best is None else best["distinct_offsets"],
            }, sort_keys=True), flush=True)
            next_report = now + 60
    payload = snapshot("completed")
    payload["completed_unix"] = time.time()
    atomic_json(args.output, payload)
    print(json.dumps({
        "status": "completed",
        "elapsed_seconds": payload["elapsed_seconds"],
        "trials": trials,
        "simulated": simulated,
        "exact_progression_incidences": incidences,
    }, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
