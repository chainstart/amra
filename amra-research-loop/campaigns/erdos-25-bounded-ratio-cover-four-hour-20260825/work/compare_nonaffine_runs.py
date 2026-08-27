#!/usr/bin/env python3
"""Compare two independently seeded finite non-affine annular searches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def summarise(source: dict) -> dict:
    rows = source["largest_sampled_scale_by_policy"]
    least_large = min(rows, key=lambda row: row["distinct_union_fraction"])
    return {
        "source_elapsed_seconds": source["source_elapsed_seconds"],
        "source_trials": source["source_trials"],
        "source_simulated_batches": source["source_simulated_batches"],
        "champion_N": source["champion"]["N"],
        "champion_nonaffine_union_fraction": source["champion"]["distinct_union_fraction"],
        "champion_constant_offset_union_fraction": source["same_moduli_constant_offset_union_fraction"],
        "champion_nonaffine_to_constant_ratio": source["nonaffine_to_constant_union_fraction_ratio"],
        "champion_greedy_integer_affine_chart_coverages": source["champion_greedy_integer_affine_chart_coverages"],
        "least_union_fraction_among_largest_policy_scales": least_large,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--confirmation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    primary = json.loads(args.primary.read_text())
    confirmation = json.loads(args.confirmation.read_text())
    if primary.get("status") != "passed" or confirmation.get("status") != "passed":
        raise ValueError("both analyses must have passed their exact champion replays")
    runs = [summarise(primary), summarise(confirmation)]
    payload = {
        "schema_version": "erdos-25.nonaffine-annular-packing-comparison.v1",
        "status": "passed",
        "runs": runs,
        "both_champions_larger_than_same_moduli_constant_offset": all(
            run["champion_nonaffine_to_constant_ratio"] > 1 for run in runs
        ),
        "interpretation_limit": "Agreement between two finite random seeds is a robustness check, not an independent mathematical audit or an inverse theorem.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "passed",
        "ratios": [run["champion_nonaffine_to_constant_ratio"] for run in runs],
        "champion_N": [run["champion_N"] for run in runs],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
