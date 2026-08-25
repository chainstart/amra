#!/usr/bin/env python3
"""Exact time-resident search after the mod-5 delay family is disrupted."""

from __future__ import annotations

import argparse
import json
import os
import random
import time
from pathlib import Path

from search_interval_delays import TARGETS, evaluate


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def first_or_censored(candidate: dict, target: int, depth: int) -> int:
    value = candidate["first_depth"][str(target)]
    return depth + 1 if value is None else value


def recovery_score(candidate: dict, break_at: int, depth: int) -> tuple[int, ...]:
    return tuple(
        first_or_censored(candidate, target, depth) - break_at
        for target in reversed(TARGETS)
    )


def make_candidate(rng: random.Random, depth: int, trial: int, source: dict | None) -> tuple:
    break_at = 1 + trial % min(10, depth - 3)
    bits_x = [0] * depth
    bits_y = [0] * depth
    bits_y[0] = 1
    bits_y[break_at] = 1

    if source is not None and trial % 3 == 0:
        break_at = source["break_at"]
        bits_x = list(source["bits_x"])
        bits_y = list(source["bits_y"])
        for _ in range(rng.randint(1, 4)):
            position = rng.randrange(break_at + 1, depth)
            if rng.randrange(2):
                bits_x[position] ^= 1
            else:
                bits_y[position] ^= 1
    else:
        mode = trial % 5
        for position in range(break_at + 1, depth):
            if mode == 0:  # sparse, but with certified later disturbances
                bits_x[position] = int(rng.random() < 0.08)
                bits_y[position] = int(rng.random() < 0.08)
            elif mode == 1:  # highly correlated
                bit = rng.randrange(2)
                bits_x[position] = bit
                bits_y[position] = bit if rng.random() < 0.9 else 1 - bit
            elif mode == 2:  # alternating
                bits_x[position] = position & 1
                bits_y[position] = (position + 1) & 1
            elif mode == 3:  # dense
                bits_x[position] = int(rng.random() > 0.08)
                bits_y[position] = int(rng.random() > 0.08)
            else:
                bits_x[position] = rng.randrange(2)
                bits_y[position] = rng.randrange(2)
        # Exclude the completely dyadic-looking continuation inside the tested
        # word; an irrational extension remains available after every word.
        bits_x[-1] = 1
        bits_y[-2] = 1
    return 20, 7, bits_x, bits_y, "post_break", break_at


def compact(candidate: dict) -> dict:
    return {key: value for key, value in candidate.items() if key != "coins"} | {
        "coins": candidate["coins"]
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=4200)
    parser.add_argument("--depth", type=int, default=22)
    parser.add_argument("--seed", type=int, default=3540826)
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
    champion: dict | None = None
    champions_by_break: dict[str, dict] = {}

    while time.monotonic() < deadline:
        trials += 1
        parameters = make_candidate(rng, args.depth, trials, champion)
        *evaluation_parameters, break_at = parameters
        candidate = evaluate(*evaluation_parameters)
        candidate["break_at"] = break_at
        old = champions_by_break.get(str(break_at))
        if old is None or recovery_score(candidate, break_at, args.depth) > recovery_score(old, break_at, args.depth):
            champions_by_break[str(break_at)] = candidate
        if champion is None or recovery_score(candidate, break_at, args.depth) > recovery_score(
            champion, champion["break_at"], args.depth
        ):
            champion = candidate

        now = time.monotonic()
        if now >= next_checkpoint:
            assert champion is not None
            elapsed = now - started
            atomic_json(
                args.output,
                {
                    "schema_version": "erdos-354.post-break-recovery.v1",
                    "status": "running",
                    "guard_required": True,
                    "seed": args.seed,
                    "depth": args.depth,
                    "requested_seconds": args.seconds,
                    "started_unix": started_wall,
                    "elapsed_seconds": elapsed,
                    "trials": trials,
                    "trials_per_second": trials / elapsed,
                    "interpretation_limit": "Finite recovery delays do not prove or refute eventual precompleteness.",
                    "champion": compact(champion),
                    "champions_by_break": {key: compact(value) for key, value in champions_by_break.items()},
                },
            )
            next_checkpoint = now + args.checkpoint_seconds
        if now >= next_report:
            assert champion is not None
            print(
                json.dumps(
                    {
                        "elapsed_seconds": round(now - started, 1),
                        "trials": trials,
                        "break_at": champion["break_at"],
                        "first_depth": champion["first_depth"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            next_report = now + 60

    assert champion is not None
    elapsed = time.monotonic() - started
    payload = {
        "schema_version": "erdos-354.post-break-recovery.v1",
        "status": "completed",
        "guard_required": True,
        "seed": args.seed,
        "depth": args.depth,
        "requested_seconds": args.seconds,
        "started_unix": started_wall,
        "completed_unix": time.time(),
        "elapsed_seconds": elapsed,
        "trials": trials,
        "trials_per_second": trials / elapsed,
        "interpretation_limit": "Finite recovery delays do not prove or refute eventual precompleteness.",
        "champion": compact(champion),
        "champions_by_break": {key: compact(value) for key, value in champions_by_break.items()},
    }
    atomic_json(args.output, payload)
    print(json.dumps({"status": "completed", "elapsed_seconds": elapsed, "trials": trials}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
