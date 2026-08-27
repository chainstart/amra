#!/usr/bin/env python3
"""Time-resident exact search for delayed subset-sum intervals in Erdős #354.

A finite 0/1 carry word defines a genuine binary parameter cylinder.  Every
reported subset-sum bit is exact: Python integers are used as bitsets and coin
insertion is ``S <- S union (S+c)``.  Finite avoidance never claims an infinite
counterexample; it only rejects proposed uniform finite-depth lemmas.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import time
from pathlib import Path


TARGETS = (2, 4, 8, 16, 32, 64, 128, 256)
MODES = ("random", "correlated", "sparse", "dense", "blocks", "alternating")


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def longest_power_run(bits: int, cap: int = 256) -> int:
    run_starts = bits
    length = 1
    while length < cap:
        run_starts &= run_starts >> length
        if not run_starts:
            break
        length *= 2
    return length


def digit_pair(rng: random.Random, mode: str, position: int) -> tuple[int, int]:
    if mode == "random":
        return rng.randrange(2), rng.randrange(2)
    if mode == "correlated":
        first = rng.randrange(2)
        return first, first if rng.random() < 0.92 else 1 - first
    if mode == "sparse":
        return int(rng.random() < 0.08), int(rng.random() < 0.08)
    if mode == "dense":
        return int(rng.random() >= 0.08), int(rng.random() >= 0.08)
    if mode == "blocks":
        block = (position // rng.choice((2, 3, 4, 5))) & 1
        return block, block if rng.random() < 0.85 else 1 - block
    return position & 1, (position + (1 if rng.random() < 0.25 else 0)) & 1


def mutate_word(rng: random.Random, source: dict, depth: int) -> tuple[int, int, list[int], list[int], str]:
    bx = list(source["bits_x"])
    by = list(source["bits_y"])
    for _ in range(rng.randint(1, 5)):
        word = bx if rng.randrange(2) == 0 else by
        index = rng.randrange(depth)
        word[index] ^= 1
    return source["x0"], source["y0"], bx, by, "mutation"


def fresh_word(rng: random.Random, depth: int, trial: int) -> tuple[int, int, list[int], list[int], str]:
    mode = MODES[trial % len(MODES)]
    x0 = rng.randint(1, 24)
    y0 = rng.randint(1, 24)
    while math.gcd(x0, y0) != 1:
        y0 = rng.randint(1, 24)
    pairs = [digit_pair(rng, mode, i) for i in range(depth)]
    return x0, y0, [pair[0] for pair in pairs], [pair[1] for pair in pairs], mode


def evaluate(x0: int, y0: int, bits_x: list[int], bits_y: list[int], mode: str) -> dict:
    reach = 1
    total = 0
    x = x0
    y = y0
    coins: list[int] = []
    first_depth: dict[str, int | None] = {str(target): None for target in TARGETS}
    for level in range(len(bits_x) + 1):
        for coin in (x, y):
            coins.append(coin)
            reach |= reach << coin
            total += coin
        power = longest_power_run(reach)
        for target in TARGETS:
            if first_depth[str(target)] is None and power >= target:
                first_depth[str(target)] = level
        if level < len(bits_x):
            x = 2 * x + bits_x[level]
            y = 2 * y + bits_y[level]
    encoded = reach.to_bytes((reach.bit_length() + 7) // 8, "little")
    return {
        "x0": x0,
        "y0": y0,
        "bits_x": bits_x,
        "bits_y": bits_y,
        "mode": mode,
        "coins": coins,
        "first_depth": first_depth,
        "final_power_run": longest_power_run(reach),
        "total_sum": total,
        "reachable_count": reach.bit_count(),
        "reachable_sha256": hashlib.sha256(encoded).hexdigest(),
    }


def delay(candidate: dict, target: int, depth: int) -> int:
    value = candidate["first_depth"][str(target)]
    return depth + 1 if value is None else value


def score(candidate: dict, depth: int) -> tuple[int, ...]:
    return tuple(delay(candidate, target, depth) for target in reversed(TARGETS))


def residue_height_profile(candidate: dict) -> dict[str, dict]:
    profile: dict[str, dict] = {}
    for modulus in (3, 5, 7, 8, 11, 13, 16, 23, 31, 32, 47, 61, 64, 97, 127):
        infinity = candidate["total_sum"] + 1
        least = [infinity] * modulus
        least[0] = 0
        for coin in candidate["coins"]:
            previous = least
            least = previous.copy()
            residue = coin % modulus
            for old_residue, old_height in enumerate(previous):
                if old_height == infinity:
                    continue
                new_residue = (old_residue + residue) % modulus
                new_height = old_height + coin
                if new_height < least[new_residue]:
                    least[new_residue] = new_height
        covered = all(value != infinity for value in least)
        profile[str(modulus)] = {
            "covered": covered,
            "maximum_least_representative": max(least) if covered else None,
            "height_over_modulus": max(least) / modulus if covered else None,
        }
    return profile


def serialise_candidate(candidate: dict) -> dict:
    return {key: value for key, value in candidate.items() if key != "coins"} | {
        "coins": candidate["coins"]
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=4500)
    parser.add_argument("--depth", type=int, default=20)
    parser.add_argument("--seed", type=int, default=3540825)
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
    best: dict[str, dict] = {}
    champion: dict | None = None
    last_payload: dict = {}

    while time.monotonic() < deadline:
        trials += 1
        if champion is not None and trials % 3 == 0:
            parameters = mutate_word(rng, champion, args.depth)
        else:
            parameters = fresh_word(rng, args.depth, trials)
        candidate = evaluate(*parameters)
        if champion is None or score(candidate, args.depth) > score(champion, args.depth):
            champion = candidate
        for target in TARGETS:
            key = str(target)
            current = best.get(key)
            if current is None or delay(candidate, target, args.depth) > delay(current, target, args.depth):
                best[key] = candidate

        now = time.monotonic()
        if now >= next_checkpoint or now >= deadline:
            assert champion is not None
            elapsed = now - started
            last_payload = {
                "schema_version": "erdos-354.interval-delay-search.v1",
                "status": "running" if now < deadline else "completed",
                "guard_required": True,
                "seed": args.seed,
                "depth": args.depth,
                "requested_seconds": args.seconds,
                "started_unix": started_wall,
                "elapsed_seconds": elapsed,
                "trials": trials,
                "trials_per_second": trials / elapsed,
                "interpretation_limit": "Finite cylinders can reject uniform prefix-depth claims but cannot prove an infinite counterexample.",
                "champion": serialise_candidate(champion),
                "best_delay_by_target": {key: serialise_candidate(value) for key, value in best.items()},
                "champion_residue_height_profile": residue_height_profile(champion),
            }
            atomic_json(args.output, last_payload)
            next_checkpoint = now + args.checkpoint_seconds
        if now >= next_report:
            assert champion is not None
            elapsed = now - started
            print(
                json.dumps(
                    {
                        "elapsed_seconds": round(elapsed, 1),
                        "trials": trials,
                        "champion_delays": {
                            str(target): delay(champion, target, args.depth) for target in TARGETS
                        },
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            next_report = now + 60

    # The loop may have crossed the deadline immediately after its last periodic
    # write; always persist an explicitly completed record.
    assert champion is not None
    elapsed = time.monotonic() - started
    last_payload.update(
        {
            "status": "completed",
            "elapsed_seconds": elapsed,
            "trials": trials,
            "trials_per_second": trials / elapsed,
            "completed_unix": time.time(),
            "champion": serialise_candidate(champion),
            "best_delay_by_target": {key: serialise_candidate(value) for key, value in best.items()},
            "champion_residue_height_profile": residue_height_profile(champion),
        }
    )
    atomic_json(args.output, last_payload)
    print(json.dumps({"status": "completed", "elapsed_seconds": elapsed, "trials": trials}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
