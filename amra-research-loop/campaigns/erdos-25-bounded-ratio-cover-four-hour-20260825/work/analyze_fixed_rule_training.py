#!/usr/bin/env python3
"""Apply strict signed-cycle gates and replay fixed-rule champions."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path


def load_simulator(path: Path):
    spec = importlib.util.spec_from_file_location("confined_echo_search", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load simulator from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def metrics_from_endpoints(endpoints: list[dict]) -> dict:
    values = [row["normalised_deleted_mass"] for row in endpoints]
    differences = [right - left for left, right in zip(values, values[1:])][-14:]
    rises = [value for value in differences if value > 0]
    drops = [-value for value in differences if value < 0]
    passed = len(differences) >= 10 and len(rises) >= 2 and len(drops) >= 2
    second_rise = sorted(rises, reverse=True)[1] if passed else 0.0
    second_drop = sorted(drops, reverse=True)[1] if passed else 0.0
    return {
        "difference_count": len(differences),
        "rise_count": len(rises),
        "drop_count": len(drops),
        "strict_cycle_gate_passed": passed,
        "second_largest_recent_rise": second_rise,
        "second_largest_recent_drop": second_drop,
        "strict_recent_two_cycle_floor": min(second_rise, second_drop),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--simulator", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replays", type=int, default=3)
    parser.add_argument("--rank-mode", choices=("raw", "cell_relative"), default="raw")
    args = parser.parse_args()
    source = json.loads(args.input.read_text())
    if source.get("status") != "completed":
        raise ValueError("training source is not complete")
    rows = []
    for champion in source["champions"]:
        strict = metrics_from_endpoints(champion["last_sixteen_endpoints"])
        item = {key: champion[key] for key in (
            "Q", "N", "base", "growth", "attack_phase", "policy", "theta",
            "schedule_seed", "cell_modulus", "cell_residue", "selected_classes",
            "certified_rare_index_survivor_density_lower_bound",
            "certified_original_survivor_density_lower_bound", "deleted_bitmap_sha256",
        )}
        item["training_metrics_recorded"] = champion["signed_metrics"]
        item["strict_metrics"] = strict
        item["cell_relative_strict_floor"] = (
            champion["Q"] * champion["cell_modulus"] * strict["strict_recent_two_cycle_floor"]
        )
        rows.append(item)
    rows.sort(
        key=lambda row: (
            row["strict_metrics"]["strict_recent_two_cycle_floor"]
            if args.rank_mode == "raw" else row["cell_relative_strict_floor"],
            row["cell_relative_strict_floor"],
            row["strict_metrics"]["strict_recent_two_cycle_floor"],
            row["training_metrics_recorded"].get("recent_two_cycle_floor", 0.0),
            row["N"],
        ),
        reverse=True,
    )
    module = load_simulator(args.simulator)
    replay_rows = []
    for champion in rows[: args.replays]:
        result = module.simulate(
            champion["Q"], champion["N"], champion["base"], champion["growth"],
            champion["attack_phase"], champion["policy"], champion["theta"],
            champion["schedule_seed"], champion["cell_modulus"], champion["cell_residue"],
        )
        if result is None or result["deleted_bitmap_sha256"] != champion["deleted_bitmap_sha256"]:
            raise AssertionError("fixed rule did not replay byte-for-byte")
        replay_metrics = metrics_from_endpoints(result["endpoint_rows"][-16:])
        if not math.isclose(
            replay_metrics["strict_recent_two_cycle_floor"],
            champion["strict_metrics"]["strict_recent_two_cycle_floor"],
            rel_tol=1e-13,
            abs_tol=1e-15,
        ):
            raise AssertionError("strict signed metric changed on replay")
        replay_rows.append({
            "N": champion["N"],
            "Q": champion["Q"],
            "g": champion["cell_modulus"],
            "deleted_bitmap_sha256": champion["deleted_bitmap_sha256"],
            "status": "passed",
        })
    payload = {
        "schema_version": "erdos-25.fixed-rule-training-analysis.v1",
        "status": "passed",
        "source_elapsed_seconds": source["elapsed_seconds"],
        "source_trials": source["trials"],
        "source_exact_rare_indices_simulated": source["exact_rare_indices_simulated"],
        "strict_gate": "at least ten recent differences, including at least two rises and two drops",
        "rank_mode": args.rank_mode,
        "strict_champions": rows,
        "mechanical_replays": replay_rows,
        "interpretation_limit": "Strict finite training cycles are hypotheses only; blind fixed-rule extension remains mandatory.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "passed",
        "champions": len(rows),
        "strict_gate_passers": sum(row["strict_metrics"]["strict_cycle_gate_passed"] for row in rows),
        "replays": len(replay_rows),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
