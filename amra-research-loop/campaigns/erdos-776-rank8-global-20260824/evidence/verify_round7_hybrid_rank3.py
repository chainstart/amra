#!/usr/bin/env python3
"""Guard the Round 7 hybrid rank-three certificate.

The universal implication is proved in ROUND7_HYBRID_RANK3_CERTIFICATE.md.
The actual-orbit scan is a bounded kill test for the new disjunctive premise;
it cannot prove that the premise holds for all parameters.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


R6 = load_module("round6_hybrid_engine", HERE / "probe_round6_rank34_suffix_budget.py")
R5 = R6.R5


def classify(item: dict[str, Any]) -> dict[str, Any]:
    a = int(item["a"])
    delta3 = int(item["deltas"]["3"])
    delta4 = int(item["deltas"]["4"])
    amplitude_cap = R5.R4.upper(a - 1, 3)
    prefix_branch = int(item["prefix"]["Z4"]) >= 2
    amplitude_branch = max(0, delta4) <= amplitude_cap
    covered = prefix_branch or amplitude_branch

    if covered:
        # Both branches imply delta_3 <= a by the symbolic lemma.  Retain an
        # exact actual-row assertion to catch a recurrence or indexing error.
        assert delta3 <= a
        assert delta3 <= int(item["budgets"]["3"])

    return {
        "V": int(item["V"]),
        "a": a,
        "delta_3": delta3,
        "delta_4": delta4,
        "rank_3_budget": int(item["budgets"]["3"]),
        "Z4_common_prefix": int(item["prefix"]["Z4"]),
        "amplitude_cap": amplitude_cap,
        "prefix_branch": prefix_branch,
        "amplitude_branch": amplitude_branch,
        "covered": covered,
    }


def scan_chunk(bounds: tuple[int, int]) -> dict[str, Any]:
    start, end = bounds
    before = R6.residual_row(start)
    counts = {
        "prefix_branch": 0,
        "amplitude_branch": 0,
        "both_branches": 0,
        "prefix_exception": 0,
        "uncovered": 0,
    }
    prefix_exceptions: list[dict[str, Any]] = []
    first_uncovered: dict[str, Any] | None = None

    for parameter in range(start, end + 1):
        after = R6.residual_row(parameter + 1)
        item = R6.comparison(before, after)
        row = classify(item)
        if row["prefix_branch"]:
            counts["prefix_branch"] += 1
        else:
            counts["prefix_exception"] += 1
            prefix_exceptions.append(row)
        if row["amplitude_branch"]:
            counts["amplitude_branch"] += 1
        if row["prefix_branch"] and row["amplitude_branch"]:
            counts["both_branches"] += 1
        if not row["covered"]:
            counts["uncovered"] += 1
            if first_uncovered is None:
                first_uncovered = row | {
                    "before_Z4_word": item["before_words"]["Z4"],
                    "after_Z4_word": item["after_words"]["Z4"],
                }
        before = after

    return {
        "range": [start, end],
        "counts": counts,
        "prefix_exceptions": prefix_exceptions,
        "first_uncovered": first_uncovered,
    }


def symbolic_guards() -> dict[str, int]:
    cases = 0
    for a in range(15, 201):
        # The proof note handles a>=15; B2>=V>=125 makes the actual top a>=16.
        assert R5.R4.kk(a, 3) <= a - 1
        amplitude_cap = R5.R4.upper(a - 1, 3)
        assert R5.R4.kk(amplitude_cap, 4) <= a - 1
        for leading_z4_top in range(5, a + 1):
            for second_prefix_top in range(3, leading_z4_top):
                assert 1 + second_prefix_top <= a
                cases += 1
    return {
        "leading_tops_checked": 186,
        "prefix_index_cases": cases,
    }


def local_information_no_go() -> dict[str, Any]:
    """Refute deriving the rank-3 target from the known low-rank data alone."""
    parameter = 125
    before_z4 = 27404
    after_z4 = 27616
    before_z3 = parameter + R5.R4.kk(before_z4, 4)
    after_z3 = parameter + 1 + R5.R4.kk(after_z4, 4)
    before_b2 = parameter + R5.R4.kk(before_z3, 3)
    after_b2 = parameter + 1 + R5.R4.kk(after_z3, 3)
    a = R5.R4.canonical(before_b2, 2)[0][0]
    rank3_budget = R5.R4.upper(a - 1, 2)
    amplitude_cap = R5.R4.upper(a - 1, 3)
    before_word = R5.R4.canonical(before_z4, 4)
    after_word = R5.R4.canonical(after_z4, 4)
    prefix = R6.common_prefix_length(before_word, after_word)

    assert before_word == [(29, 4), (28, 3), (27, 2), (26, 1)]
    assert after_word == [(30, 4), (11, 3), (10, 2), (1, 1)]
    assert before_z3 == 4185 and after_z3 == 4252
    assert before_b2 == 577 and after_b2 == 582
    assert a == 34 and rank3_budget == 66 and amplitude_cap == 28
    assert prefix == 0
    assert after_z4 - before_z4 == 212 > amplitude_cap
    assert after_z3 - before_z3 == 67 > rank3_budget
    assert after_z4 <= R5.R4.suspension(before_z3, 3)
    assert after_z3 <= R5.R4.suspension(before_b2, 2)
    assert after_b2 - before_b2 == 5 <= a

    return {
        "classification": "synthetic_local_counterexample",
        "V": parameter,
        "Z4_words": {"before": before_word, "after": after_word},
        "Z4_jump": after_z4 - before_z4,
        "Z4_common_prefix": prefix,
        "amplitude_cap": amplitude_cap,
        "Z3_jump": after_z3 - before_z3,
        "rank_3_budget": rank3_budget,
        "B2_jump": after_b2 - before_b2,
        "LTJ_allowance": a,
        "diagonal_caps": {
            "Z4_next_at_most": R5.R4.suspension(before_z3, 3),
            "Z3_next_at_most": R5.R4.suspension(before_b2, 2),
        },
        "scope": (
            "Refutes deriving the hybrid premise or rank-3 budget from the "
            "low-rank recurrences plus known diagonal domination alone. It is "
            "not an actual-orbit row and it does not refute LTJ."
        ),
    }


def merge(results: list[dict[str, Any]], start: int, end: int, workers: int) -> dict[str, Any]:
    count_keys = results[0]["counts"]
    counts = {
        key: sum(int(result["counts"][key]) for result in results)
        for key in count_keys
    }
    exceptions = sorted(
        [row for result in results for row in result["prefix_exceptions"]],
        key=lambda row: row["V"],
    )
    uncovered = [
        result["first_uncovered"]
        for result in results
        if result["first_uncovered"] is not None
    ]
    first_uncovered = min(uncovered, key=lambda row: row["V"]) if uncovered else None
    return {
        "status": "FAIL" if first_uncovered is not None else "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "parameter_range": [start, end],
        "workers": workers,
        "symbolic_convention_guards": symbolic_guards(),
        "local_information_no_go": local_information_no_go(),
        "branch_counts": counts,
        "prefix_exceptions": exceptions,
        "first_uncovered": first_uncovered,
        "scope": (
            "The hybrid implication is symbolic. PASS means only that the new "
            "disjunctive actual-orbit premise survived this bounded kill test; "
            "it is not an all-parameter proof of that premise or of LTJ."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=125)
    parser.add_argument("--end", type=int, default=2000)
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()
    if args.start < 125 or args.end < args.start or args.workers < 1:
        raise SystemExit("invalid scan parameters")

    size = (args.end - args.start + 1 + args.workers - 1) // args.workers
    chunks = [
        (chunk_start, min(args.end, chunk_start + size - 1))
        for chunk_start in range(args.start, args.end + 1, size)
    ]
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(scan_chunk, chunks))
    print(json.dumps(merge(results, args.start, args.end, args.workers), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
