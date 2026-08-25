#!/usr/bin/env python3
"""Measure existential residue-core margins across sparse carry depths."""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import time
from pathlib import Path

from search_residue_cores import MODULI, evaluate


DEPTHS = tuple(range(10, 23))


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def sparse_coins(rng: random.Random, depth: int) -> tuple[list[int], dict]:
    x0 = rng.randint(1, 24)
    y0 = rng.randint(1, 24)
    while math.gcd(x0, y0) != 1:
        y0 = rng.randint(1, 24)
    bits_x = [0] * depth
    bits_y = [0] * depth
    for word in (bits_x, bits_y):
        for position in rng.sample(range(depth), rng.randint(1, min(4, depth))):
            word[position] = 1
    x, y = x0, y0
    coins: list[int] = []
    for level in range(depth + 1):
        coins.extend((x, y))
        if level < depth:
            x = 2 * x + bits_x[level]
            y = 2 * y + bits_y[level]
    return coins, {"x0": x0, "y0": y0, "bits_x": bits_x, "bits_y": bits_y, "mode": "one_to_four_sparse_carries"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=2700)
    parser.add_argument("--seed", type=int, default=3540829)
    parser.add_argument("--checkpoint-seconds", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    started_wall = time.time()
    started = time.monotonic()
    deadline = started + args.seconds
    next_checkpoint = started + min(args.checkpoint_seconds, args.seconds)
    next_report = started + 60
    trials = 0
    buckets = {
        str(depth): {
            "trials": 0,
            "paths_with_covering_split": 0,
            "paths_with_certified_split": 0,
            "smallest_best_margin": None,
            "hardest": None,
        }
        for depth in DEPTHS
    }

    def snapshot(status: str) -> dict:
        elapsed = time.monotonic() - started
        return {
            "schema_version": "erdos-354.sparse-depth-scaling.v1",
            "status": status,
            "guard_required": True,
            "seed": args.seed,
            "requested_seconds": args.seconds,
            "started_unix": started_wall,
            "elapsed_seconds": elapsed,
            "trials": trials,
            "trials_per_second": trials / elapsed,
            "by_depth": buckets,
            "interpretation_limit": "Finite-depth scaling can kill uniform bounds but cannot decide eventual good-split existence."
        }

    while time.monotonic() < deadline:
        trials += 1
        depth = DEPTHS[(trials - 1) % len(DEPTHS)]
        modulus = MODULI[(trials // len(DEPTHS)) % len(MODULI)]
        coins, metadata = sparse_coins(rng, depth)
        bucket = buckets[str(depth)]
        bucket["trials"] += 1
        candidates = [
            evaluate(coins, metadata, split, modulus)
            for split in range(4, 2 * depth + 1, 2)
        ]
        covered = [candidate for candidate in candidates if candidate["prefix_covers"]]
        if covered:
            bucket["paths_with_covering_split"] += 1
            best = max(covered, key=lambda candidate: candidate["core_power_run"] - candidate["height_spread"])
            margin = best["core_power_run"] - best["height_spread"]
            if bucket["smallest_best_margin"] is None or margin < bucket["smallest_best_margin"]:
                bucket["smallest_best_margin"] = margin
                bucket["hardest"] = {"modulus": modulus, "metadata": metadata, "best_split": best, "best_margin": margin}
            if best["certified_interval_lower_bound"] > 0:
                bucket["paths_with_certified_split"] += 1

        now = time.monotonic()
        if now >= next_checkpoint:
            atomic_json(args.output, snapshot("running"))
            next_checkpoint = now + args.checkpoint_seconds
        if now >= next_report:
            print(json.dumps({"elapsed_seconds": round(now-started, 1), "trials": trials, "smallest_best_margin_by_depth": {key: value["smallest_best_margin"] for key, value in buckets.items()}}, sort_keys=True), flush=True)
            next_report = now + 60

    payload = snapshot("completed") | {"completed_unix": time.time()}
    atomic_json(args.output, payload)
    print(json.dumps({"status": "completed", "elapsed_seconds": payload["elapsed_seconds"], "trials": trials}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
