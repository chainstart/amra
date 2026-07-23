#!/usr/bin/env python3
"""Exact R002 checks for the current Erdős #776 Macaulay endpoint.

The finite evaluations in this file are falsifier/regression evidence only.
The all-parameter equivalences and the two failed proof routes are written
out in REPORT.md.

The new part of the evaluator is a run-compressed exact implementation of

    E_V = V - 3,
    E_{q-1} = V + KK_q(E_q).

A run (high, low, offset) represents all canonical terms

    C(i + offset, i),  high >= i >= low.

When taking a lower shadow, the offset rises by one.  When adding V, the
usual suffix-carry test is constant throughout one run, by the hockey-stick
identity.  Thus no floating point arithmetic or parameter cutoff is hidden
in the compression.
"""

from __future__ import annotations

import json
from math import comb


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    """Ordinary greedy canonical expansion, used as an independent oracle."""
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    out: list[tuple[int, int]] = []
    remaining = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if remaining == 0:
            break
        lo = lower - 1
        hi = cap if cap is not None else max(lower + 1, 2 * lower)
        if cap is None:
            while comb(hi, lower) <= remaining:
                hi *= 2
        while lo + 1 < hi:
            middle = (lo + hi) // 2
            if comb(middle, lower) <= remaining:
                lo = middle
            else:
                hi = middle
        upper = lo
        if cap is not None:
            upper = min(upper, cap - 1)
            while upper >= lower and comb(upper, lower) > remaining:
                upper -= 1
        if upper >= lower:
            out.append((upper, lower))
            remaining -= comb(upper, lower)
            cap = upper
    if remaining:
        raise AssertionError((number, rank, out, remaining))
    return out


def lower_shadow(number: int, rank: int) -> int:
    return sum(comb(upper, lower - 1) for upper, lower in canonical(number, rank))


def upper_raise(number: int, rank: int) -> int:
    return sum(comb(upper, lower + 1) for upper, lower in canonical(number, rank))


Run = tuple[int, int, int]


def canonical_runs(number: int, rank: int) -> list[Run]:
    """Run-length compressed greedy canonical expansion."""
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    remaining = number
    lower = rank
    offset_cap: int | None = None
    runs: list[Run] = []
    while remaining:
        if lower < 1:
            raise AssertionError((number, rank, remaining, runs))
        if offset_cap is None:
            high_offset = 1
            while comb(lower + high_offset, high_offset) <= remaining:
                high_offset *= 2
        else:
            high_offset = offset_cap + 1
        lo, hi = -1, high_offset
        while lo + 1 < hi:
            middle = (lo + hi) // 2
            if comb(lower + middle, middle) <= remaining:
                lo = middle
            else:
                hi = middle
        offset = lo
        if offset < 0:
            raise AssertionError((number, rank, remaining, lower, offset_cap))

        left, right = 1, lower
        while left < right:
            length = (left + right + 1) // 2
            low_rank = lower - length + 1
            value = (
                comb(lower + offset + 1, offset + 1)
                - comb(low_rank + offset, offset + 1)
            )
            if value <= remaining:
                left = length
            else:
                right = length - 1
        length = left
        low_rank = lower - length + 1
        value = (
            comb(lower + offset + 1, offset + 1)
            - comb(low_rank + offset, offset + 1)
        )
        runs.append((lower, low_rank, offset))
        remaining -= value
        lower -= length
        offset_cap = offset
    return runs


def runs_value(runs: list[Run]) -> int:
    return sum(
        comb(high + offset + 1, offset + 1)
        - comb(low + offset, offset + 1)
        for high, low, offset in runs
    )


def add_to_runs(runs: list[Run], rank: int, increment: int) -> list[Run]:
    """Add to a canonical expansion by exact compressed suffix carry."""
    tail = 0
    for index in range(len(runs) - 1, -1, -1):
        high, low, offset = runs[index]
        # At the lowest term of this run, the unfilled capacity immediately
        # below it is C(low+offset, offset+1).  Hockey-stick cancellation
        # makes the same carry decision valid throughout the whole run.
        if (
            low > 1
            and tail + increment < comb(low + offset, offset + 1)
        ):
            return (
                runs[: index + 1]
                + canonical_runs(tail + increment, low - 1)
            )
        tail += (
            comb(high + offset + 1, offset + 1)
            - comb(low + offset, offset + 1)
        )
    return canonical_runs(tail + increment, rank)


def defect_step(runs: list[Run], rank: int, parameter: int) -> list[Run]:
    """Apply E_(q-1) = V + KK_q(E_q), with q=rank."""
    shadow_runs: list[Run] = []
    rank_zero_terms = 0
    for high, low, offset in runs:
        if high >= 2:
            shadow_runs.append(
                (high - 1, max(low, 2) - 1, offset + 1)
            )
        if low == 1:
            rank_zero_terms += 1
    return add_to_runs(
        shadow_runs,
        rank - 1,
        parameter + rank_zero_terms,
    )


def compressed_defects_at_5_and_6(parameter: int) -> dict[str, object]:
    """Return exact E_5,E_6 and their compressed canonical expansions."""
    if parameter < 7:
        raise ValueError(parameter)
    rank = parameter
    runs = canonical_runs(parameter - 3, rank)
    e6: int | None = None
    runs6: list[Run] | None = None
    while rank > 5:
        if rank == 6:
            e6 = runs_value(runs)
            runs6 = list(runs)
        runs = defect_step(runs, rank, parameter)
        rank -= 1
    if e6 is None or runs6 is None:
        raise AssertionError(parameter)
    return {
        "E5": runs_value(runs),
        "E6": e6,
        "runs5": runs,
        "runs6": runs6,
    }


def ordinary_defects(parameter: int) -> dict[int, int]:
    defects = {parameter: parameter - 3}
    for rank in range(parameter, 5, -1):
        defects[rank - 1] = (
            parameter + lower_shadow(defects[rank], rank)
        )
    return defects


def f5(parameter: int) -> int:
    return (
        comb(parameter + 1, 5)
        + comb(parameter - 1, 4)
        + comb(parameter - 2, 3)
    )


def f6(parameter: int) -> int:
    return (
        comb(parameter + 1, 6)
        + comb(parameter - 1, 5)
        + comb(parameter - 2, 4)
    )


def endpoint_excess_from_h(h_value: int) -> tuple[int, int]:
    d_value = 2 + lower_shadow(h_value, 2)
    return d_value, lower_shadow(d_value, 2)


def evaluate(parameter: int) -> dict[str, object]:
    state = compressed_defects_at_5_and_6(parameter)
    h_value = int(state["E5"]) - f5(parameter)
    g_value = f6(parameter) - int(state["E6"])
    d_value, endpoint_excess = endpoint_excess_from_h(h_value)
    threshold = None
    threshold_margin = None
    if parameter >= 70_501:
        threshold = (
            comb(parameter - 4, 2) - comb(70_496, 2)
        )
        threshold_margin = g_value - threshold
    return {
        "V": parameter,
        "h_E5_minus_F5": h_value,
        "g_F6_minus_E6": g_value,
        "g_minus_binom_Vminus4_2": (
            g_value - comb(parameter - 4, 2)
        ),
        "d_2_plus_KK2_h": d_value,
        "rank3_endpoint_excess": endpoint_excess,
        "rank6_required_threshold": threshold,
        "rank6_threshold_margin": threshold_margin,
        "E5_canonical_runs": state["runs5"],
    }


def main() -> None:
    crosschecks = 0
    for parameter in range(7, 181):
        compressed = compressed_defects_at_5_and_6(parameter)
        ordinary = ordinary_defects(parameter)
        assert compressed["E5"] == ordinary[5]
        assert compressed["E6"] == ordinary[6]
        assert runs_value(compressed["runs5"]) == compressed["E5"]
        assert runs_value(compressed["runs6"]) == compressed["E6"]
        crosschecks += 1

    strategic_parameters = [
        379,
        5_668,
        5_669,
        5_670,
        5_671,
        5_701,
        5_702,
        6_328,
        6_329,
        66_843,
        66_844,
        70_500,
        70_501,
        74_997,
        150_000,
        200_000,
    ]
    evaluations = [evaluate(value) for value in strategic_parameters]

    # Strict synthetic boundary audit inherited from the all-V rank-5
    # reduction.  These two adjacent integers are the actual discontinuity.
    d_safe, excess_safe = endpoint_excess_from_h(70_500)
    d_fail, excess_fail = endpoint_excess_from_h(70_501)
    assert (d_safe, excess_safe) == (378, 28)
    assert (d_fail, excess_fail) == (379, 29)

    # On the observed h=8 plateau, P=U_4(E_4)-E_5 equals
    # C(V-2,2)-4.  The coarse diagonal estimate G>=P-1 reaches the
    # required G>=C(V-1,2)-66846 exactly at V=66843 and misses at 66844.
    h_plateau = 8
    d_plateau = 2 + lower_shadow(h_plateau, 2)
    p_offset = upper_raise(d_plateau, 2) - h_plateau
    assert (d_plateau, p_offset) == (7, -4)
    coarse_margins = {
        str(value): (
            comb(value - 2, 2)
            + p_offset
            - 1
            - (comb(value - 1, 2) - 66_846)
        )
        for value in (66_843, 66_844)
    }
    assert coarse_margins == {"66843": 0, "66844": -1}

    result = {
        "schema": "amra.erdos776.r002-rank5-rotation.v1",
        "status": "PASS",
        "ordinary_vs_run_compressed_crosschecks": crosschecks,
        "crosschecked_V_range": [7, 180],
        "strategic_exact_evaluations": evaluations,
        "synthetic_rank5_boundary": {
            "h_safe": 70_500,
            "d_safe": d_safe,
            "endpoint_excess_safe": excess_safe,
            "h_next": 70_501,
            "d_next": d_fail,
            "endpoint_excess_next": excess_fail,
        },
        "diagonal_route_first_coarse_failure_on_h8_plateau": {
            "identity": (
                "P=U4(E4)-E5=binom(V-2,2)-4; "
                "using only G>=P-1"
            ),
            "required": "G>=binom(V-1,2)-66846",
            "margins": coarse_margins,
        },
        "scope": (
            "Exact finite evaluations and implementation equivalence only. "
            "They do not prove h(V)<=70500 for all V."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
