#!/usr/bin/env python3
"""Finite exact guard for the proposed Erdős #776 rank-18 barrier.

This script is falsifier/regression evidence only.  No finite parameter scan
proves the all-V inequality D_18 <= B_18.
"""

from __future__ import annotations

import json
from math import comb


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    """Ordinary greedy Macaulay expansion, with no project-engine import."""
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    result: list[tuple[int, int]] = []
    remaining = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if remaining == 0:
            break
        low = lower - 1
        high = cap if cap is not None else max(lower + 1, 2 * lower)
        if cap is None:
            while comb(high, lower) <= remaining:
                high *= 2
        while low + 1 < high:
            middle = (low + high) // 2
            if comb(middle, lower) <= remaining:
                low = middle
            else:
                high = middle
        upper = low if cap is None else min(low, cap - 1)
        while upper >= lower and comb(upper, lower) > remaining:
            upper -= 1
        if upper >= lower:
            result.append((upper, lower))
            remaining -= comb(upper, lower)
            cap = upper
    if remaining:
        raise AssertionError((number, rank, result, remaining))
    return result


Run = tuple[int, int, int]


def canonical_runs(number: int, rank: int) -> list[Run]:
    """Independent run-compressed greedy expansion.

    A run (high, low, offset) represents
    sum_{i=low}^high C(i+offset, i).
    """
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
            upper_offset = 1
            while comb(lower + upper_offset, upper_offset) <= remaining:
                upper_offset *= 2
        else:
            upper_offset = offset_cap + 1
        low_offset, high_offset = -1, upper_offset
        while low_offset + 1 < high_offset:
            middle = (low_offset + high_offset) // 2
            if comb(lower + middle, middle) <= remaining:
                low_offset = middle
            else:
                high_offset = middle
        offset = low_offset
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


def kk(number: int, rank: int) -> int:
    return sum(
        comb(upper, lower - 1)
        for upper, lower in canonical(number, rank)
    )


def upper_raise(number: int, rank: int) -> int:
    return sum(
        comb(upper, lower + 1)
        for upper, lower in canonical(number, rank)
    )


def upper_raise_compressed(number: int, rank: int) -> int:
    # Raising C(i+offset,i) gives C(i+offset,i+1).  Hockey-stick
    # summation over one run gives the displayed difference.
    return sum(
        comb(high + offset + 1, offset)
        - comb(low + offset, offset)
        for high, low, offset in canonical_runs(number, rank)
        if offset >= 1
    )


def p18(parameter: int) -> int:
    return comb(parameter - 12, 18) + comb(parameter - 13, 17)


def b18(parameter: int) -> int:
    return (
        comb(parameter - 12, 18)
        + sum(
            comb(parameter - 31 + lower, lower)
            for lower in range(4, 18)
        )
        + comb(parameter - 30, 3)
        - 1
    )


def b18_expanded(parameter: int) -> int:
    return (
        comb(parameter - 12, 18)
        + sum(
            comb(parameter - 31 + lower, lower)
            for lower in range(4, 18)
        )
        + comb(parameter - 31, 3)
        + comb(parameter - 32, 2)
        + comb(parameter - 33, 1)
    )


def delta_quadratic(parameter: int) -> int:
    return (
        parameter
        - 28
        + 2 * comb(parameter - 29, 2)
        + comb(parameter - 30, 2)
    )


def delta_cubic(parameter: int) -> int:
    return comb(parameter - 27, 3) - comb(parameter - 30, 3) + 1


def reverse_orbit(
    parameter: int,
    *,
    compressed: bool,
) -> dict[str, object]:
    raise_fn = upper_raise_compressed if compressed else upper_raise
    top_rank = parameter - 12
    value = b18(parameter)
    states = {18: value}
    failure: dict[str, int] | None = None
    for rank in range(18, top_rank):
        if value < parameter:
            failure = {"rank": rank, "value": value}
            break
        value = raise_fn(value - parameter, rank)
        states[rank + 1] = value
    return {
        "failure": failure,
        "terminal": states.get(top_rank),
        "penultimate": states.get(top_rank - 1),
        "states": states,
    }


def endpoint_orbits(parameter: int) -> tuple[dict[int, int], dict[int, int]]:
    top_rank = parameter - 12
    lower = {top_rank: 0}
    upper = {top_rank: 1}
    for rank in range(top_rank - 1, 17, -1):
        lower[rank] = parameter + kk(lower[rank + 1], rank + 1)
        upper[rank] = parameter + kk(upper[rank + 1], rank + 1)
    return lower, upper


def audit_zero_basin_step(parameter: int) -> int:
    lower, upper = endpoint_orbits(parameter)
    top_rank = parameter - 12
    checked = 0
    for rank in range(18, top_rank):
        next_rank = rank + 1
        assert lower[rank] - parameter == kk(
            lower[next_rank], next_rank
        )
        assert upper[rank] - parameter == kk(
            upper[next_rank], next_rank
        )

        lower_image = upper_raise(lower[rank] - parameter, rank)
        upper_image = upper_raise(upper[rank] - 1 - parameter, rank)
        assert lower[next_rank] <= lower_image < upper[next_rank]
        assert lower[next_rank] <= upper_image < upper[next_rank]

        if lower[rank] > parameter:
            below_image = upper_raise(
                lower[rank] - 1 - parameter, rank
            )
            assert below_image < lower[next_rank]
        above_image = upper_raise(upper[rank] - parameter, rank)
        assert above_image >= upper[next_rank]

        # The two independent U implementations must agree at all four
        # boundary arguments used above.
        arguments = [
            lower[rank] - parameter,
            upper[rank] - 1 - parameter,
            upper[rank] - parameter,
        ]
        if lower[rank] > parameter:
            arguments.append(lower[rank] - 1 - parameter)
        for argument in arguments:
            assert upper_raise(argument, rank) == upper_raise_compressed(
                argument, rank
            )
        checked += 1
    return checked


def main() -> None:
    formula_range = range(40, 1_001)
    for parameter in formula_range:
        candidate = b18(parameter)
        assert candidate == b18_expanded(parameter)
        assert p18(parameter) - candidate == delta_quadratic(parameter)
        assert p18(parameter) - candidate == delta_cubic(parameter)
        expected_canonical = (
            [(parameter - 12, 18)]
            + [
                (parameter - 31 + lower, lower)
                for lower in range(17, 3, -1)
            ]
            + [
                (parameter - 31, 3),
                (parameter - 32, 2),
                (parameter - 33, 1),
            ]
        )
        assert canonical(candidate, 18) == expected_canonical

    failed_rows: list[dict[str, int]] = []
    for parameter in range(40, 69):
        result = reverse_orbit(parameter, compressed=True)
        failure = result["failure"]
        assert isinstance(failure, dict)
        assert failure["rank"] == parameter - 13
        assert failure["value"] < parameter
        failed_rows.append(
            {
                "V": parameter,
                "failure_rank": failure["rank"],
                "failure_value": failure["value"],
            }
        )

    contiguous_success_end = 500
    for parameter in range(69, contiguous_success_end + 1):
        result = reverse_orbit(parameter, compressed=True)
        assert result["failure"] is None
        assert result["penultimate"] == parameter
        assert result["terminal"] == 0

    strategic_parameters = [632, 750, 1_000]
    strategic_rows: list[dict[str, int]] = []
    for parameter in strategic_parameters:
        result = reverse_orbit(parameter, compressed=True)
        assert result["failure"] is None
        assert result["penultimate"] == parameter
        assert result["terminal"] == 0
        strategic_rows.append(
            {
                "V": parameter,
                "penultimate": int(result["penultimate"]),
                "terminal": int(result["terminal"]),
            }
        )

    # Full-state comparison between ordinary and compressed U is deliberately
    # kept small; the larger checks above use only the exact compressed form.
    ordinary_agreement_end = 100
    ordinary_steps = 0
    for parameter in range(40, ordinary_agreement_end + 1):
        ordinary = reverse_orbit(parameter, compressed=False)
        compressed = reverse_orbit(parameter, compressed=True)
        assert ordinary == compressed
        ordinary_steps += len(ordinary["states"]) - 1

    basin_parameters = [40, 50, 69, 70, 100]
    basin_steps = {
        parameter: audit_zero_basin_step(parameter)
        for parameter in basin_parameters
    }

    result = {
        "status": "PASS",
        "scope": "FINITE FALSIFIER/REGRESSION EVIDENCE ONLY",
        "not_proved": (
            "No finite scan proves D18<=B18 for every V>=70."
        ),
        "formula_and_canonical_range": [40, 1_000],
        "expected_failure_range": [40, 68],
        "first_and_last_failure": [failed_rows[0], failed_rows[-1]],
        "contiguous_success_range": [69, contiguous_success_end],
        "strategic_success_parameters": strategic_rows,
        "ordinary_vs_compressed_range": [40, ordinary_agreement_end],
        "ordinary_vs_compressed_steps": ordinary_steps,
        "zero_basin_endpoint_parameters": basin_parameters,
        "zero_basin_endpoint_steps": basin_steps,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
