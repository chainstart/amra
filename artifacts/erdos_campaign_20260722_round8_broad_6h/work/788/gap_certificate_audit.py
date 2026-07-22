#!/usr/bin/env python3
"""Exact audit of common restricted-sum certificates in small lattice boxes."""

from __future__ import annotations

import itertools
import json
import math


def box(lengths):
    return list(itertools.product(*(range(length) for length in lengths)))


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def restricted_sumset(points):
    return {add(x, y) for i, x in enumerate(points) for y in points[i + 1 :]}


def representation_matching_sizes(points):
    counts = {}
    for i, x in enumerate(points):
        for y in points[i + 1 :]:
            value = add(x, y)
            counts[value] = counts.get(value, 0) + 1
    return counts


def exact_common_formula(points, subset_size):
    holes = len(points) - subset_size
    counts = representation_matching_sizes(points)
    return {value for value, count in counts.items() if count > holes}


def brute_common_intersection(points, subset_size):
    common = None
    for chosen in itertools.combinations(points, subset_size):
        sums = restricted_sumset(chosen)
        common = sums if common is None else common & sums
    return common or set()


def tent_count(length, coordinate_sum):
    return length - abs(coordinate_sum - (length - 1))


def central_core(lengths, subset_size):
    volume = math.prod(lengths)
    holes = volume - subset_size
    if 2 * holes + 2 > volume:
        return set(), None
    theta = ((2 * holes + 2) / volume) ** (1 / len(lengths))
    thresholds = [math.ceil(theta * length) for length in lengths]
    core = {
        value
        for value in itertools.product(*(range(2 * length - 1) for length in lengths))
        if all(
            tent_count(length, coordinate_sum) >= threshold
            for length, coordinate_sum, threshold in zip(lengths, value, thresholds)
        )
    }
    return core, {"theta": theta, "thresholds": thresholds}


def main() -> None:
    rows = []
    cases = [
        ((4,), 3),
        ((5,), 3),
        ((6,), 4),
        ((2, 3), 4),
        ((2, 4), 5),
        ((3, 3), 5),
        ((3, 4), 7),
        ((2, 2, 2), 5),
        ((2, 2, 3), 7),
    ]
    for lengths, subset_size in cases:
        points = box(lengths)
        exact = exact_common_formula(points, subset_size)
        brute = brute_common_intersection(points, subset_size)
        core, core_data = central_core(lengths, subset_size)
        assert exact == brute
        assert core <= exact
        rows.append(
            {
                "lengths": lengths,
                "volume": len(points),
                "subset_size": subset_size,
                "holes": len(points) - subset_size,
                "common_size": len(exact),
                "central_core_size": len(core),
                "central_core_data": core_data,
                "exact_equals_bruteforce": exact == brute,
                "central_core_is_certificate": core <= exact,
            }
        )
    systematic_boxes = sorted({
        lengths
        for rank in range(1, 4)
        for lengths in itertools.product(range(2, 15), repeat=rank)
        if math.prod(lengths) <= 14
    })
    systematic_instances = 0
    half_density_nonempty_failures = 0
    for lengths in systematic_boxes:
        points = box(lengths)
        volume = len(points)
        for subset_size in range(1, volume + 1):
            exact = exact_common_formula(points, subset_size)
            brute = brute_common_intersection(points, subset_size)
            core, _ = central_core(lengths, subset_size)
            assert exact == brute
            assert core <= exact
            if subset_size <= math.ceil(volume / 2) and exact:
                half_density_nonempty_failures += 1
            systematic_instances += 1
    assert half_density_nonempty_failures == 0
    print(
        json.dumps(
            {
                "status": "PASS",
                "scope": "finite boxes only; the general matching proof is in attempt.md",
                "systematic_scan": {
                    "ranks": [1, 3],
                    "maximum_volume": 14,
                    "boxes": len(systematic_boxes),
                    "box_subset_size_instances": systematic_instances,
                    "half_density_nonempty_failures": half_density_nonempty_failures,
                },
                "rows": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
