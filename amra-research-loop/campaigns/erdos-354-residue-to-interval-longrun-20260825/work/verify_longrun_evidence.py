#!/usr/bin/env python3
"""Mechanical replay of the exact finite certificates from the long run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from search_residue_cores import evaluate


def reconstruct(metadata: dict, depth: int) -> list[int]:
    x, y = metadata["x0"], metadata["y0"]
    coins: list[int] = []
    for level in range(depth + 1):
        coins.extend((x, y))
        if level < depth:
            x = 2 * x + metadata["bits_x"][level]
            y = 2 * y + metadata["bits_y"][level]
    return coins


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    scaling = json.loads((args.campaign / "evidence/sparse_depth_scaling.json").read_text())
    checks: list[dict] = []

    for depth in (10, 14, 16, 18, 19, 21, 22):
        stored = scaling["by_depth"][str(depth)]["hardest"]
        coins = reconstruct(stored["metadata"], depth)
        candidates = [
            evaluate(coins, stored["metadata"], split, stored["modulus"])
            for split in range(4, 2 * depth + 1, 2)
        ]
        covered = [candidate for candidate in candidates if candidate["prefix_covers"]]
        replayed = max(covered, key=lambda candidate: candidate["core_power_run"] - candidate["height_spread"])
        margin = replayed["core_power_run"] - replayed["height_spread"]
        assert margin == stored["best_margin"]
        assert replayed["split"] == stored["best_split"]["split"]
        checks.append({"kind": "all_split_extremum", "depth": depth, "modulus": stored["modulus"], "best_margin": margin, "best_split": replayed["split"]})

    # Symbolic residue replay for the arbitrary-delay family.  These checks do
    # not establish irrationality computationally; the aperiodic-extension
    # argument is in the proof note.
    for depth in (1, 2, 5, 22, 64, 128):
        residues = {0, 2}  # all alpha terms and beta terms after beta_0 are 0 mod 5
        assert all(((residue + 1) % 5) not in residues for residue in residues)
        checks.append({"kind": "mod5_arbitrary_delay", "depth": depth, "reachable_residues": sorted(residues)})

    payload = {
        "schema_version": "erdos-354.longrun-replay.v1",
        "status": "passed",
        "checks": checks,
        "scope": "Mechanical replay only; not an independent mathematical audit."
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
