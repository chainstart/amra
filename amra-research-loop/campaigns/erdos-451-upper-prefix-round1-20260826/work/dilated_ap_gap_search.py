#!/usr/bin/env python3
"""Exact small-system falsification tests for anchored dilated AP CRT boxes."""

from __future__ import annotations

import argparse
import json
from itertools import product
from math import prod


def allowed_set(q: int, width: int, step: int) -> set[int]:
    return {(-step * offset) % q for offset in range(width)}


def cyclic_gap(q_period: int, representatives: list[int]) -> int:
    representatives.sort()
    return max(
        representatives[index + 1] - representatives[index]
        for index in range(len(representatives) - 1)
    ) if len(representatives) > 1 else q_period


def largest_gap(q_period: int, representatives: list[int]) -> int:
    representatives.sort()
    if len(representatives) == 1:
        return q_period
    return max(
        [
            representatives[index + 1] - representatives[index]
            for index in range(len(representatives) - 1)
        ]
        + [q_period + representatives[0] - representatives[-1]]
    )


def evaluate(moduli: tuple[int, ...], widths: tuple[int, ...], steps: tuple[int, ...]) -> dict[str, object]:
    period = prod(moduli)
    local = [
        allowed_set(q, width, step)
        for q, width, step in zip(moduli, widths, steps, strict=True)
    ]
    representatives = [
        n
        for n in range(period)
        if all(n % q in a for q, a in zip(moduli, local, strict=True))
    ]
    assert len(representatives) == prod(widths)
    gap = largest_gap(period, representatives)
    density_scale = period / len(representatives)
    return {
        "moduli": list(moduli),
        "widths": list(widths),
        "steps": list(steps),
        "period": period,
        "allowed_count": len(representatives),
        "largest_cyclic_gap": gap,
        "density_scale_Q_over_size": density_scale,
        "gap_over_density_scale": gap / density_scale,
        "representatives": representatives,
    }


def exhaustive_three_moduli() -> dict[str, object]:
    moduli = (5, 7, 11)
    best: dict[str, object] | None = None
    rows = 0
    for widths in product(*(range(2, q) for q in moduli)):
        for steps in product(*(range(1, q) for q in moduli)):
            rows += 1
            record = evaluate(moduli, widths, steps)
            if best is None or record["gap_over_density_scale"] > best["gap_over_density_scale"]:
                best = record
    assert best is not None
    return {
        "scope": "moduli (5,7,11), every width 2<=d<q, every nonzero step; anchored AP contains 0",
        "tested_systems": rows,
        "maximum": best,
    }


def fixed_balanced_four_moduli() -> dict[str, object]:
    moduli = (5, 7, 11, 13)
    widths = (3, 4, 6, 7)
    best: dict[str, object] | None = None
    rows = 0
    for steps in product(*(range(1, q) for q in moduli)):
        rows += 1
        record = evaluate(moduli, widths, steps)
        if best is None or record["gap_over_density_scale"] > best["gap_over_density_scale"]:
            best = record
    assert best is not None
    interval_record = evaluate(moduli, widths, (1, 1, 1, 1))
    return {
        "scope": "moduli (5,7,11,13), fixed widths (3,4,6,7), every nonzero step; anchored AP contains 0",
        "tested_systems": rows,
        "unit_step_interval_baseline": interval_record,
        "maximum": best,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print(
        json.dumps(
            {
                "schema_version": "erdos451.dilated_ap_gap_search.v1",
                "exhaustive_three_moduli": exhaustive_three_moduli(),
                "fixed_balanced_four_moduli": fixed_balanced_four_moduli(),
                "interpretation": "Exact finite falsification only. A maximum is not evidence for a uniform theorem.",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
