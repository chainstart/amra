#!/usr/bin/env python3
"""Efficient finite falsifier for the Round 6 rank-3/rank-4 targets.

Each parameter orbit is reconstructed once per worker chunk and reused for
both adjacent comparisons.  The scan can kill a universal target but cannot
prove one.  All-parameter claims require a separate symbolic wall theorem.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from concurrent.futures import ProcessPoolExecutor
from math import comb
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


R5 = load_module("round5_rank34_engine", HERE / "verify_round5_adjoint_suffix_budget.py")


def residual_row(parameter: int) -> dict[str, Any]:
    values = R5.R3.secondary_orbit(parameter, target=4)
    n = parameter - 25
    residuals = {
        rank: values[rank + 2] - comb(n - 1, rank + 2) - comb(n - 2, rank + 1)
        for rank in range(2, 5)
    }
    word2 = R5.R3.ENGINE.canonical(residuals[2], 2)
    return {
        "V": parameter,
        "residuals": residuals,
        "a": word2[0][0],
        "B2_word": word2,
        "Z3_word": R5.R3.ENGINE.canonical(residuals[3], 3),
        "Z4_word": R5.R3.ENGINE.canonical(residuals[4], 4),
    }


def common_prefix_length(left: list[list[int]] | list[tuple[int, int]], right: list[list[int]] | list[tuple[int, int]]) -> int:
    length = 0
    for first, second in zip(left, right):
        if tuple(first) != tuple(second):
            break
        length += 1
    return length


def comparison(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    a = int(before["a"])
    ladder = R5.budgets(a, maximum_rank=4)
    delta2 = int(after["residuals"][2]) - int(before["residuals"][2])
    delta3 = int(after["residuals"][3]) - int(before["residuals"][3])
    delta4 = int(after["residuals"][4]) - int(before["residuals"][4])
    return {
        "V": int(before["V"]),
        "a": a,
        "deltas": {"2": delta2, "3": delta3, "4": delta4},
        "budgets": {"3": ladder[3], "4": ladder[4]},
        "margins": {
            "LTJ": a - delta2,
            "rank_3": ladder[3] - max(0, delta3),
            "rank_4": ladder[4] - max(0, delta4),
        },
        "prefix": {
            "Z3": common_prefix_length(before["Z3_word"], after["Z3_word"]),
            "Z4": common_prefix_length(before["Z4_word"], after["Z4_word"]),
        },
        "before_words": {"B2": before["B2_word"], "Z3": before["Z3_word"], "Z4": before["Z4_word"]},
        "after_words": {"B2": after["B2_word"], "Z3": after["Z3_word"], "Z4": after["Z4_word"]},
    }


def scan_chunk(bounds: tuple[int, int]) -> dict[str, Any]:
    start, end = bounds
    before = residual_row(start)
    first_failures: dict[str, dict[str, Any] | None] = {"rank_3": None, "rank_4": None, "LTJ": None}
    tightest: dict[str, list[dict[str, Any]]] = {"rank_3": [], "rank_4": [], "LTJ": []}
    positive_walls = 0
    prefix_histogram: dict[str, int] = {}

    for parameter in range(start, end + 1):
        after = residual_row(parameter + 1)
        item = comparison(before, after)
        if item["deltas"]["3"] > 0 or item["deltas"]["4"] > 0:
            positive_walls += 1
        key = f"Z3:{item['prefix']['Z3']}/Z4:{item['prefix']['Z4']}"
        prefix_histogram[key] = prefix_histogram.get(key, 0) + 1
        for target in ("rank_3", "rank_4", "LTJ"):
            margin = int(item["margins"][target])
            if margin < 0 and first_failures[target] is None:
                first_failures[target] = item
            tightest[target].append(item)
            tightest[target].sort(key=lambda row: (row["margins"][target], row["V"]))
            del tightest[target][8:]
        before = after

    return {
        "range": [start, end],
        "first_failures": first_failures,
        "tightest": tightest,
        "positive_walls": positive_walls,
        "prefix_histogram": prefix_histogram,
    }


def merge(results: list[dict[str, Any]], start: int, end: int, workers: int) -> dict[str, Any]:
    failures: dict[str, dict[str, Any] | None] = {}
    tightest: dict[str, list[dict[str, Any]]] = {}
    for target in ("rank_3", "rank_4", "LTJ"):
        candidates = [result["first_failures"][target] for result in results if result["first_failures"][target] is not None]
        failures[target] = min(candidates, key=lambda row: row["V"]) if candidates else None
        rows = [row for result in results for row in result["tightest"][target]]
        tightest[target] = sorted(rows, key=lambda row: (row["margins"][target], row["V"]))[:12]

    histogram: dict[str, int] = {}
    for result in results:
        for key, count in result["prefix_histogram"].items():
            histogram[key] = histogram.get(key, 0) + count
    return {
        "status": "FAIL" if any(row is not None for row in failures.values()) else "PASS",
        "parameter_range": [start, end],
        "workers": workers,
        "first_failures": failures,
        "tightest": tightest,
        "positive_walls": sum(result["positive_walls"] for result in results),
        "prefix_histogram": dict(sorted(histogram.items())),
        "scope": "Finite falsifier and wall classifier only. Absence of a counterexample is not an all-parameter proof.",
    }


def compact_row(row: dict[str, Any]) -> dict[str, Any]:
    """Keep the exact numerical certificate while dropping long binomial words."""
    return {
        key: row[key]
        for key in ("V", "a", "deltas", "budgets", "margins", "prefix")
    }


def compact_report(report: dict[str, Any]) -> dict[str, Any]:
    report = dict(report)
    report["first_failures"] = {
        target: compact_row(row) if row is not None else None
        for target, row in report["first_failures"].items()
    }
    report["tightest"] = {
        target: [compact_row(row) for row in rows]
        for target, rows in report["tightest"].items()
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=125)
    parser.add_argument("--end", type=int, default=2000)
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    if args.start < 40 or args.end < args.start or args.workers < 1:
        raise SystemExit("invalid scan parameters")
    size = (args.end - args.start + 1 + args.workers - 1) // args.workers
    chunks = [
        (chunk_start, min(args.end, chunk_start + size - 1))
        for chunk_start in range(args.start, args.end + 1, size)
    ]
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(scan_chunk, chunks))
    report = merge(results, args.start, args.end, args.workers)
    if args.compact:
        report = compact_report(report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
