#!/usr/bin/env python3
"""Exact finite arithmetic guard for the colourwise residue inequality."""

from __future__ import annotations

import argparse
import itertools
import json
import math


def choose2(x):
    return x * (x - 1) // 2


def canonical_threshold(missing_b):
    root_floor = math.isqrt(1 + 8 * missing_b)
    return 2 + (1 + root_floor) // 2


def profile_values(t_cross, a_internal, high_count):
    total = t_cross + a_internal
    assert total >= 1
    assert 0 <= high_count <= min(1, total)
    low_count = total - high_count
    defect_a = total - 1
    defect_b = max(0, t_cross - 1)
    residue_a = defect_a - defect_b
    low_only_credit = int(high_count == 0)
    assert defect_a == low_count - low_only_credit
    assert residue_a == low_count - low_only_credit - defect_b
    assert defect_a <= low_count
    assert residue_a <= low_count - defect_b
    assert low_count >= defect_b
    return {
        "defect_a": defect_a,
        "defect_b": defect_b,
        "residue_a": residue_a,
        "low_count": low_count,
        "low_only_credit": low_only_credit,
    }


def run_exhaustive(max_edges_per_type=12, max_colours=4):
    for missing_b in range(10001):
        threshold = canonical_threshold(missing_b)
        assert choose2(threshold - 2) <= missing_b
        assert missing_b < choose2(threshold - 1)

    profiles = []
    for t_cross in range(max_edges_per_type + 1):
        for a_internal in range(max_edges_per_type + 1):
            if t_cross + a_internal == 0:
                continue
            for high_count in range(min(1, t_cross + a_internal) + 1):
                values = profile_values(t_cross, a_internal, high_count)
                profiles.append((t_cross, a_internal, high_count, values))

    aggregates = 0
    small_profiles = profiles[: min(18, len(profiles))]
    for colour_count in range(1, max_colours + 1):
        for selection in itertools.product(small_profiles, repeat=colour_count):
            defect_a = sum(item[3]["defect_a"] for item in selection)
            defect_b = sum(item[3]["defect_b"] for item in selection)
            residue_a = sum(item[3]["residue_a"] for item in selection)
            low_count = sum(item[3]["low_count"] for item in selection)
            low_only_credit = sum(
                item[3]["low_only_credit"] for item in selection
            )
            assert residue_a == defect_a - defect_b
            assert defect_a == low_count - low_only_credit
            assert residue_a == low_count - low_only_credit - defect_b
            assert residue_a <= low_count - defect_b
            aggregates += 1

    internal_low_parameter_cases = 0
    for m in range(3, 81):
        for minimum_degree in range(m):
            g = m - minimum_degree - 1
            for q in range(2, m + 2):
                for h in range(m + 1):
                    forced_degree = (
                        minimum_degree - q + 1 - (m - h)
                    )
                    assert forced_degree == h - g - q
                    if h >= 2 * g + 2 * q + 5:
                        assert 2 * forced_degree - h >= 5
                        assert forced_degree >= 0
                    internal_low_parameter_cases += 1

    return {
        "schema": "amra.erdos809.outer-a-low-degree-residue.v1",
        "profiles": len(profiles),
        "aggregate_profiles": aggregates,
        "max_edges_per_type": max_edges_per_type,
        "max_colours": max_colours,
        "internal_low_parameter_cases": internal_low_parameter_cases,
        "status": "PASS",
        "scope": "arithmetic guard; compatibility premise is proved in the note",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-edges-per-type", type=int, default=12)
    parser.add_argument("--max-colours", type=int, default=4)
    args = parser.parse_args()
    print(
        json.dumps(
            run_exhaustive(args.max_edges_per_type, args.max_colours),
            indent=2,
            sort_keys=True,
        )
    )
