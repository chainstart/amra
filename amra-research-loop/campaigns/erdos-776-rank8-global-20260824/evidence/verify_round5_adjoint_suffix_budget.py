#!/usr/bin/env python3
"""Exact guards for the Round 5 adjoint suffix-budget ladder.

Finite actual rows are falsifiers and identity guards only.  The universal
budget implication is proved symbolically in ROUND5_ADJOINT_SUFFIX_BUDGET.md.
"""

from __future__ import annotations

import importlib.util
import json
from hashlib import sha256
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


R4 = load_module("round4_budget_engine", HERE / "verify_round4_ltj_diagonal_loss.py")
R3 = load_module("round3_actual_engine", HERE / "verify_round3_actual_coupling_second.py")


def budgets(leading_top: int, maximum_rank: int = 7) -> dict[int, int]:
    if leading_top < 2:
        raise ValueError(leading_top)
    result = {3: R4.upper(leading_top - 1, 2)}
    for rank in range(4, maximum_rank + 1):
        previous = result[rank - 1]
        result[rank] = R4.upper(previous - 1, rank - 1) if previous else 0
    return result


def residuals(parameter: int, maximum_rank: int = 7) -> dict[int, int]:
    values = R3.secondary_orbit(parameter, target=4)
    n = parameter - 25
    return {
        rank: values[rank + 2] - comb(n - 1, rank + 2) - comb(n - 2, rank + 1)
        for rank in range(2, maximum_rank + 1)
    }


def actual_case(parameter: int) -> dict[str, object]:
    before = residuals(parameter)
    after = residuals(parameter + 1)
    row = R3.actual_row(parameter)
    leading_top = int(row["B2_word"][0][0])
    ladder = budgets(leading_top)
    deltas = {rank: after[rank] - before[rank] for rank in before}

    assert deltas[2] == R3.actual_row(parameter + 1)["B2"] - row["B2"]
    for rank in range(3, 8):
        exact_next = 1 + R3.ENGINE.kk(after[rank], rank) - R3.ENGINE.kk(before[rank], rank)
        assert deltas[rank - 1] == exact_next
        assert exact_next <= 1 + R3.ENGINE.kk(max(0, deltas[rank]), rank)

    sufficient_at = []
    for rank in range(3, 8):
        if max(0, deltas[rank]) <= ladder[rank]:
            bound = max(0, deltas[rank])
            for lower_step in range(rank, 3, -1):
                bound = 1 + R3.ENGINE.kk(bound, lower_step)
                assert bound <= ladder[lower_step - 1]
            ltj_bound = 1 + R3.ENGINE.kk(bound, 3)
            assert ltj_bound <= leading_top
            assert deltas[2] <= leading_top
            sufficient_at.append(rank)

    return {
        "V_to_Vplus1": [parameter, parameter + 1],
        "leading_top_a": leading_top,
        "deltas": {str(rank): deltas[rank] for rank in sorted(deltas)},
        "budgets": {str(rank): ladder[rank] for rank in sorted(ladder)},
        "sufficient_ranks": sufficient_at,
        "actual_LTJ_margin": leading_top - deltas[2],
    }


def symbolic_guards() -> dict[str, int]:
    subadditivity_cases = 0
    for rank in range(3, 8):
        for base in range(101):
            for increment in range(51):
                assert R4.kk(base + increment, rank) - R4.kk(base, rank) <= R4.kk(increment, rank)
                subadditivity_cases += 1

    budget_cases = 0
    for leading_top in range(2, 121):
        ladder = budgets(leading_top)
        assert 1 + R4.kk(ladder[3], 3) <= leading_top
        budget_cases += 1
        for rank in range(4, 8):
            if ladder[rank - 1] == 0:
                assert ladder[rank] == 0
                continue
            assert 1 + R4.kk(ladder[rank], rank) <= ladder[rank - 1]
            budget_cases += 1
    return {
        "shadow_subadditivity_cases": subadditivity_cases,
        "adjoint_budget_cases": budget_cases,
    }


def main() -> None:
    parameters = (125, 154, 186, 468, 600, 845, 1435, 1471)
    cases = [actual_case(parameter) for parameter in parameters]
    by_parameter = {case["V_to_Vplus1"][0]: case for case in cases}

    rank7_failure = by_parameter[186]
    assert rank7_failure["leading_top_a"] == 36
    assert rank7_failure["deltas"]["7"] == 14
    assert rank7_failure["budgets"]["7"] == 9
    assert 7 not in rank7_failure["sufficient_ranks"]

    rank6_failure = by_parameter[845]
    assert rank6_failure["leading_top_a"] == 52
    assert rank6_failure["deltas"]["6"] == 250
    assert rank6_failure["budgets"]["6"] == 211
    assert 6 not in rank6_failure["sufficient_ranks"]

    rank5_failure = by_parameter[1435]
    assert rank5_failure["leading_top_a"] == 63
    assert rank5_failure["deltas"]["5"] == 622
    assert rank5_failure["budgets"]["5"] == 484
    assert rank5_failure["actual_LTJ_margin"] == 61
    assert 4 in rank5_failure["sufficient_ranks"]
    assert 5 not in rank5_failure["sufficient_ranks"]

    wall = by_parameter[1471]
    assert wall["leading_top_a"] == 64
    assert wall["deltas"] == {
        "2": 6,
        "3": 14,
        "4": 28,
        "5": 63,
        "6": 199,
        "7": 664,
    }
    assert wall["budgets"] == {
        "3": 193,
        "4": 380,
        "5": 513,
        "6": 490,
        "7": 338,
    }
    assert 5 in wall["sufficient_ranks"] and 6 in wall["sufficient_ranks"]
    assert 7 not in wall["sufficient_ranks"]

    payload = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "symbolic_guards": symbolic_guards(),
        "selected_actual_rows": cases,
        "actual_fixed_rank_counterexamples": {
            "rank_5": {
                "V_to_Vplus1": [1435, 1436],
                "delta_5": 622,
                "A_5": 484,
            },
            "rank_6": {
                "V_to_Vplus1": [845, 846],
                "delta_6": 250,
                "A_6": 211,
            },
            "rank_7": {
                "V_to_Vplus1": [186, 187],
                "delta_7": 14,
                "A_7": 9,
            },
            "scope": "kills fixed-rank five, six, and seven adjoint-budget proposals; rank-three, rank-four, and joint multirank targets remain open",
        },
        "scope": (
            "Finite rows guard exact identities and seek counterexamples only. "
            "The all-parameter conditional budget implication is symbolic; "
            "no all-V actual suffix bound or LTJ theorem is inferred."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
