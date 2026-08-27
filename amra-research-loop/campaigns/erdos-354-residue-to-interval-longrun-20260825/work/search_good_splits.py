#!/usr/bin/env python3
"""Test the existential (rather than arbitrary) residue-core split."""

from __future__ import annotations

import argparse
import json
import os
import random
import time
from pathlib import Path

from search_residue_cores import MODULI, evaluate, make_coins


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def compact(candidate: dict) -> dict:
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=3000)
    parser.add_argument("--depth", type=int, default=19)
    parser.add_argument("--seed", type=int, default=3540828)
    parser.add_argument("--checkpoint-seconds", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    started_wall = time.time()
    started = time.monotonic()
    deadline = started + args.seconds
    next_checkpoint = started + min(args.checkpoint_seconds, args.seconds)
    next_report = started + 60
    trials = any_covered = any_bridged = 0
    hardest: dict | None = None
    largest: dict | None = None
    buckets = {str(q): {"trials": 0, "any_covered": 0, "any_bridged": 0, "smallest_best_margin": None} for q in MODULI}

    def snapshot(status: str) -> dict:
        elapsed = time.monotonic() - started
        return {
            "schema_version": "erdos-354.existential-split-search.v1",
            "status": status,
            "guard_required": True,
            "seed": args.seed,
            "depth": args.depth,
            "requested_seconds": args.seconds,
            "started_unix": started_wall,
            "elapsed_seconds": elapsed,
            "trials": trials,
            "trials_per_second": trials / elapsed,
            "paths_with_a_covering_split": any_covered,
            "paths_with_a_certified_split": any_bridged,
            "by_modulus": buckets,
            "hardest_path": hardest,
            "largest_certificate": largest,
            "interpretation_limit": "Existence in finite words is evidence only; it gives no uniform infinite-path theorem."
        }

    while time.monotonic() < deadline:
        trials += 1
        coins, metadata = make_coins(rng, args.depth, trials)
        modulus = MODULI[trials % len(MODULI)]
        bucket = buckets[str(modulus)]
        bucket["trials"] += 1
        candidates = [
            evaluate(coins, metadata, split, modulus)
            for split in range(4, 2 * args.depth + 1, 2)
        ]
        covered = [candidate for candidate in candidates if candidate["prefix_covers"]]
        if not covered:
            continue
        any_covered += 1
        bucket["any_covered"] += 1
        best = max(covered, key=lambda candidate: candidate["core_power_run"] - candidate["height_spread"])
        best_margin = best["core_power_run"] - best["height_spread"]
        previous_margin = bucket["smallest_best_margin"]
        bucket["smallest_best_margin"] = best_margin if previous_margin is None else min(previous_margin, best_margin)
        record = {
            "modulus": modulus,
            "metadata": metadata,
            "best_split": best,
            "best_margin": best_margin,
            "covered_splits": len(covered),
        }
        if hardest is None or best_margin < hardest["best_margin"]:
            hardest = record
        certified = [candidate for candidate in covered if candidate["certified_interval_lower_bound"] > 0]
        if certified:
            any_bridged += 1
            bucket["any_bridged"] += 1
            local_largest = max(certified, key=lambda candidate: candidate["certified_interval_lower_bound"])
            if largest is None or local_largest["certified_interval_lower_bound"] > largest["best_split"]["certified_interval_lower_bound"]:
                largest = {
                    "modulus": modulus,
                    "metadata": metadata,
                    "best_split": local_largest,
                    "best_margin": local_largest["core_power_run"] - local_largest["height_spread"],
                    "covered_splits": len(covered),
                }

        now = time.monotonic()
        if now >= next_checkpoint:
            atomic_json(args.output, snapshot("running"))
            next_checkpoint = now + args.checkpoint_seconds
        if now >= next_report:
            print(json.dumps({"elapsed_seconds": round(now-started, 1), "trials": trials, "any_covered": any_covered, "any_bridged": any_bridged, "hardest_best_margin": None if hardest is None else hardest["best_margin"]}, sort_keys=True), flush=True)
            next_report = now + 60

    payload = snapshot("completed") | {"completed_unix": time.time()}
    atomic_json(args.output, payload)
    print(json.dumps({"status": "completed", "elapsed_seconds": payload["elapsed_seconds"], "trials": trials}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
