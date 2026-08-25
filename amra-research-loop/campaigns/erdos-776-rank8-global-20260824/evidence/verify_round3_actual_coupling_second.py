#!/usr/bin/env python3
"""Exact guards for the second round-3 actual-coupling mechanism."""

from __future__ import annotations

import importlib.util
import json
from hashlib import sha256
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "verify_rank8_obstructions.py"
SPEC = importlib.util.spec_from_file_location("rank8_engine", ENGINE_PATH)
assert SPEC is not None and SPEC.loader is not None
ENGINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ENGINE)


def secondary_orbit(v: int, target: int = 4) -> dict[int, int]:
    rank = v - 26
    runs = []
    values = {rank: 0}
    while rank > target:
        runs = ENGINE.defect_step(runs, rank, v)
        rank -= 1
        values[rank] = ENGINE.runs_value(runs)
    return values


def actual_row(v: int) -> dict[str, object]:
    values = secondary_orbit(v)
    n = v - 25
    baselines = {
        4: comb(n - 1, 4) + comb(n - 2, 3),
        5: comb(n - 1, 5) + comb(n - 2, 4),
        6: comb(n - 1, 6) + comb(n - 2, 5),
    }
    tails = {
        2: values[4] - baselines[4],
        3: values[5] - baselines[5],
        4: values[6] - baselines[6],
    }
    assert tails[2] == v + ENGINE.kk(tails[3], 3)
    return {
        "V": v,
        "E4": values[4],
        "E5": values[5],
        "E6": values[6],
        "baseline4": baselines[4],
        "baseline5": baselines[5],
        "baseline6": baselines[6],
        "B2": tails[2],
        "Z3": tails[3],
        "Z4": tails[4],
        "B2_word": ENGINE.canonical(tails[2], 2),
        "Z3_word": ENGINE.canonical(tails[3], 3),
        "KK2_B2": ENGINE.kk(tails[2], 2),
        "KK3_Z3": ENGINE.kk(tails[3], 3),
    }


def leading_top_lemma_guards() -> dict[str, int]:
    cases = 0
    for a in range(2, 80):
        for b in range(a):
            x = comb(a, 2) + b
            for jump in range(a + 1):
                y = x + jump
                assert ENGINE.kk(y, 2) - ENGINE.kk(x, 2) <= 1
                cases += 1
    return {"checked_cases": cases}


def main() -> None:
    before = actual_row(1471)
    after = actual_row(1472)
    assert after["B2"] - before["B2"] == 6
    assert before["B2_word"] == [(64, 2), (16, 1)]
    assert after["B2_word"] == [(64, 2), (22, 1)]
    assert before["KK2_B2"] == after["KK2_B2"] == 65
    assert after["Z3"] - before["Z3"] == 14
    assert after["Z4"] - before["Z4"] == 28
    payload = {
        "status": "PASS",
        "actual_counterexample": {"before": before, "after": after},
        "leading_top_lemma": leading_top_lemma_guards(),
        "classification": (
            "Exact actual V=1471 counterexample kills Delta B2<=3; "
            "the all-parameter leading-top lemma is symbolic and LTJ remains open"
        ),
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
