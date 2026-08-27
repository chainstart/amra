#!/usr/bin/env python3
"""Replay and compare the non-affine annular near-extremizer search."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import collections
from pathlib import Path


def load_search(path: Path):
    spec = importlib.util.spec_from_file_location("annular_search", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load search module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def constant_offset_fraction(n: int, start: int, gap: int, offset: int = 1) -> float:
    union = {
        quotient * modulus - offset
        for modulus in range(start, start + gap * n, gap)
        for quotient in range(1, n + 1)
    }
    return len(union) / (n * n)


def constant_offset_gcd_weight(n: int, start: int, gap: int) -> float:
    moduli = list(range(start, start + gap * n, gap))
    return sum(
        math.gcd(moduli[left], moduli[right]) / moduli[right]
        for right in range(1, n) for left in range(right)
    )


def greedy_affine_chart_coverages(row: dict, max_slope: int = 16) -> dict[str, float]:
    """Measure how much of a batch a small greedily chosen chart family covers."""
    charts: dict[tuple[int, int], set[int]] = collections.defaultdict(set)
    for index, offset in enumerate(row["offsets"]):
        modulus = row["modulus_start"] + row["modulus_gap"] * index
        target = modulus - offset
        for slope in range(1, max_slope + 1):
            charts[(slope, modulus - slope * target)].add(index)
    covered: set[int] = set()
    remaining = list(charts.values())
    result = {}
    for count in range(1, 9):
        best = max(remaining, key=lambda members: len(members - covered))
        covered.update(best)
        remaining.remove(best)
        if count in {1, 2, 4, 8}:
            result[str(count)] = len(covered) / row["N"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--simulator", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(args.input.read_text())
    if source.get("status") != "completed":
        raise ValueError("search source is not complete")
    champion = source["best_genuinely_nonaffine_batch"]
    if champion is None:
        raise ValueError("search source has no champion")
    module = load_search(args.simulator)
    replay = module.simulate(
        champion["N"], champion["modulus_start"], champion["modulus_gap"],
        champion["policy"], champion["schedule_seed"]
    )
    if replay is None:
        raise AssertionError("champion did not replay")
    for key in (
        "distinct_union_points", "distinct_offsets", "largest_affine_offset_chart",
        "largest_integer_affine_chart",
        "crt_compatible_pairs", "union_commutative_hash64",
    ):
        if replay[key] != champion[key]:
            raise AssertionError((key, replay[key], champion[key]))
    for key in (
        "distinct_union_fraction", "crt_compatible_pair_fraction",
        "largest_affine_offset_chart_fraction", "largest_integer_affine_chart_fraction",
    ):
        if not math.isclose(replay[key], champion[key], rel_tol=1e-14, abs_tol=1e-15):
            raise AssertionError(key)

    comparator = constant_offset_fraction(
        champion["N"], champion["modulus_start"], champion["modulus_gap"]
    )
    comparator_weight = constant_offset_gcd_weight(
        champion["N"], champion["modulus_start"], champion["modulus_gap"]
    )
    largest_scale_rows = []
    grouped: dict[str, list[dict]] = {}
    for key, row in source["best_by_policy_and_scale"].items():
        grouped.setdefault(row["policy"], []).append(row)
    for policy, rows in sorted(grouped.items()):
        row = max(rows, key=lambda item: item["N"])
        row_constant_comparator = constant_offset_fraction(
            row["N"], row["modulus_start"], row["modulus_gap"]
        )
        largest_scale_rows.append({
            "policy": policy,
            "N": row["N"],
            "modulus_gap": row["modulus_gap"],
            "distinct_union_fraction": row["distinct_union_fraction"],
            "distinct_offsets": row["distinct_offsets"],
            "largest_affine_offset_chart_fraction": row["largest_affine_offset_chart_fraction"],
            "largest_integer_affine_chart_fraction": row["largest_integer_affine_chart_fraction"],
            "crt_compatible_pair_fraction": row["crt_compatible_pair_fraction"],
            "greedy_integer_affine_chart_coverages": greedy_affine_chart_coverages(row),
            "same_moduli_constant_offset_union_fraction": row_constant_comparator,
            "nonaffine_to_constant_union_fraction_ratio": (
                row["distinct_union_fraction"] / row_constant_comparator
            ),
        })
    payload = {
        "schema_version": "erdos-25.nonaffine-annular-packing-analysis.v1",
        "status": "passed",
        "source_elapsed_seconds": source["elapsed_seconds"],
        "source_trials": source["trials"],
        "source_simulated_batches": source["simulated_target_irredundant_batches"],
        "source_exact_progression_incidences": source["exact_progression_incidences"],
        "champion": champion,
        "champion_replay": {
            "status": "passed",
            "union_commutative_hash64": replay["union_commutative_hash64"],
        },
        "champion_greedy_integer_affine_chart_coverages": greedy_affine_chart_coverages(champion),
        "same_moduli_constant_offset_union_fraction": comparator,
        "nonaffine_to_constant_union_fraction_ratio": champion["distinct_union_fraction"] / comparator,
        "same_moduli_constant_offset_gcd_weight": comparator_weight,
        "nonaffine_to_constant_gcd_weight_ratio": champion["crt_compatible_gcd_weight"] / comparator_weight,
        "largest_sampled_scale_by_policy": largest_scale_rows,
        "interpretation_limit": "A positive finite separation from the constant-offset comparator supports but does not prove affine near-extremizer rigidity.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "passed",
        "champion_N": champion["N"],
        "nonaffine_union_fraction": champion["distinct_union_fraction"],
        "constant_offset_union_fraction": comparator,
        "ratio": payload["nonaffine_to_constant_union_fraction_ratio"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
