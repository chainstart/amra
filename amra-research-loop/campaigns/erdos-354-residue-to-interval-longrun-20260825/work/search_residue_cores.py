#!/usr/bin/env python3
"""Guarded adversarial search around the disjoint residue-core bridge."""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import time
from pathlib import Path

from search_interval_delays import MODES, digit_pair, longest_power_run


MODULI = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def make_coins(rng: random.Random, depth: int, trial: int) -> tuple[list[int], dict]:
    mode = MODES[trial % len(MODES)]
    x0 = rng.randint(1, 20)
    y0 = rng.randint(1, 20)
    while math.gcd(x0, y0) != 1:
        y0 = rng.randint(1, 20)
    x, y = x0, y0
    bits_x: list[int] = []
    bits_y: list[int] = []
    coins: list[int] = []
    for level in range(depth + 1):
        coins.extend((x, y))
        if level < depth:
            bx, by = digit_pair(rng, mode, level)
            bits_x.append(bx)
            bits_y.append(by)
            x = 2 * x + bx
            y = 2 * y + by
    return coins, {"x0": x0, "y0": y0, "bits_x": bits_x, "bits_y": bits_y, "mode": mode}


def least_prefix_representatives(coins: list[int], modulus: int) -> list[int] | None:
    infinity = sum(coins) + 1
    least = [infinity] * modulus
    least[0] = 0
    for coin in coins:
        previous = least
        least = previous.copy()
        residue = coin % modulus
        for old_residue, old_value in enumerate(previous):
            if old_value == infinity:
                continue
            new_residue = (old_residue + residue) % modulus
            new_value = old_value + coin
            if new_value < least[new_residue]:
                least[new_residue] = new_value
    return None if infinity in least else least


def tail_quotient_zero_bits(coins: list[int], modulus: int) -> int:
    reachable = [0] * modulus
    reachable[0] = 1
    for coin in coins:
        quotient, residue = divmod(coin, modulus)
        previous = reachable
        reachable = previous.copy()
        for old_residue, quotient_bits in enumerate(previous):
            if not quotient_bits:
                continue
            total_residue = old_residue + residue
            carry, new_residue = divmod(total_residue, modulus)
            reachable[new_residue] |= quotient_bits << (quotient + carry)
    return reachable[0]


def evaluate(coins: list[int], metadata: dict, split: int, modulus: int) -> dict:
    prefix = coins[:split]
    tail = coins[split:]
    least = least_prefix_representatives(prefix, modulus)
    result = metadata | {"modulus": modulus, "split": split, "coins": coins}
    if least is None:
        return result | {"prefix_covers": False, "height_spread": None, "core_power_run": 1, "certified_interval_lower_bound": 0}
    heights = [(value - residue) // modulus for residue, value in enumerate(least)]
    spread = max(heights) - min(heights)
    core_run = longest_power_run(tail_quotient_zero_bits(tail, modulus), cap=1024)
    interval = modulus * max(0, core_run - spread)
    return result | {
        "prefix_covers": True,
        "least_representatives": least,
        "height_spread": spread,
        "core_power_run": core_run,
        "certified_interval_lower_bound": interval,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=3600)
    parser.add_argument("--depth", type=int, default=19)
    parser.add_argument("--seed", type=int, default=3540827)
    parser.add_argument("--checkpoint-seconds", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    started_wall = time.time()
    started = time.monotonic()
    deadline = started + args.seconds
    next_checkpoint = started + min(args.checkpoint_seconds, args.seconds)
    next_report = started + 60
    trials = covered = bridged = 0
    worst: dict | None = None
    best: dict | None = None
    buckets = {str(q): {"trials": 0, "covered": 0, "bridged": 0, "largest_interval": 0} for q in MODULI}

    def snapshot(status: str) -> dict:
        elapsed = time.monotonic() - started
        return {
            "schema_version": "erdos-354.residue-core-search.v1",
            "status": status,
            "guard_required": True,
            "seed": args.seed,
            "depth": args.depth,
            "requested_seconds": args.seconds,
            "started_unix": started_wall,
            "elapsed_seconds": elapsed,
            "trials": trials,
            "trials_per_second": trials / elapsed,
            "prefix_covered_trials": covered,
            "bridge_certified_trials": bridged,
            "by_modulus": buckets,
            "worst_covered_candidate": worst,
            "best_certified_candidate": best,
            "interpretation_limit": "Finite search tests the sufficient bridge and cannot establish universal tail-core growth."
        }

    while time.monotonic() < deadline:
        trials += 1
        coins, metadata = make_coins(rng, args.depth, trials)
        modulus = MODULI[trial_index := (trials % len(MODULI))]
        # Prefix length is a number of coins, with both dilation sequences mixed.
        split = 4 + 2 * rng.randrange(2, max(3, args.depth // 2))
        candidate = evaluate(coins, metadata, split, modulus)
        bucket = buckets[str(modulus)]
        bucket["trials"] += 1
        if candidate["prefix_covers"]:
            covered += 1
            bucket["covered"] += 1
            deficit = candidate["height_spread"] + 1 - candidate["core_power_run"]
            old_deficit = -1 if worst is None else worst["height_spread"] + 1 - worst["core_power_run"]
            if worst is None or deficit > old_deficit:
                worst = candidate
            if candidate["certified_interval_lower_bound"] > 0:
                bridged += 1
                bucket["bridged"] += 1
                bucket["largest_interval"] = max(bucket["largest_interval"], candidate["certified_interval_lower_bound"])
                if best is None or candidate["certified_interval_lower_bound"] > best["certified_interval_lower_bound"]:
                    best = candidate

        now = time.monotonic()
        if now >= next_checkpoint:
            atomic_json(args.output, snapshot("running"))
            next_checkpoint = now + args.checkpoint_seconds
        if now >= next_report:
            print(json.dumps({"elapsed_seconds": round(now-started, 1), "trials": trials, "covered": covered, "bridged": bridged, "best_interval": 0 if best is None else best["certified_interval_lower_bound"]}, sort_keys=True), flush=True)
            next_report = now + 60

    payload = snapshot("completed") | {"completed_unix": time.time()}
    atomic_json(args.output, payload)
    print(json.dumps({"status": "completed", "elapsed_seconds": payload["elapsed_seconds"], "trials": trials}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
