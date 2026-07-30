#!/usr/bin/env python3
"""Exact checks for the geometric-radius high-energy branch."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction

from verify_affine_copy_barrier import parameter_line_count


@dataclass(frozen=True)
class SearchResult:
    radius_count: int
    height_count: int
    height_universe_size: int
    configurations_checked: int
    minimum_line_count: int
    point_count: int
    minimum_over_f_three_halves: float
    minimizer: tuple[tuple[int, ...], ...]


def geometric_circles(
    height_sets: tuple[tuple[int, ...], ...],
    *,
    ratio: int = 2,
    radial_scale: int = 1,
) -> list[tuple[int, int]]:
    if ratio < 2 or radial_scale < 1:
        raise ValueError("need integer ratio >= 2 and positive scale")
    return [
        (radial_scale * ratio**index, height)
        for index, heights in enumerate(height_sets)
        for height in heights
    ]


def theorem_lower_bound(height_sets: tuple[tuple[int, ...], ...]) -> int:
    radius_count = len(height_sets)
    point_count = sum(len(heights) for heights in height_sets)
    return math.ceil((radius_count + 1) * point_count / 4)


def offsets_by_product(radius_count: int, ratio: int = 2) -> dict[int, set[int]]:
    result: dict[int, set[int]] = {}
    for left in range(radius_count):
        for right in range(left, radius_count):
            result.setdefault(left + right, set()).add(
                (ratio**left - ratio**right) ** 2
            )
    return result


def has_sidon_differences(values: set[int]) -> bool:
    ordered = sorted(values)
    differences = [
        ordered[right] - ordered[left]
        for left in range(len(ordered))
        for right in range(left + 1, len(ordered))
    ]
    return len(differences) == len(set(differences))


def identical_height_energy_lower_bound(
    radius_count: int,
    height_set: tuple[int, ...],
) -> int:
    squared_differences = {
        (left - right) ** 2
        for left in height_set
        for right in height_set
    }
    y_size = len(squared_differences)
    total = Fraction(0, 1)
    for offsets in offsets_by_product(radius_count).values():
        t_size = len(offsets)
        total += Fraction(t_size * t_size * y_size, t_size + y_size)
    return math.floor(total)


def verify_thin_slab_instance(
    height_sets: tuple[tuple[int, ...], ...],
    *,
    ratio: int = 2,
    radial_scale: int,
) -> tuple[int, int]:
    all_heights = [height for heights in height_sets for height in heights]
    if not all_heights:
        raise ValueError("need at least one circle")
    span = max(all_heights) - min(all_heights)
    if span >= radial_scale:
        raise ValueError("thin-slab hypothesis requires span < radial_scale")
    line_count = parameter_line_count(
        geometric_circles(
            height_sets,
            ratio=ratio,
            radial_scale=radial_scale,
        )
    )
    lower_bound = theorem_lower_bound(height_sets)
    if line_count < lower_bound:
        raise AssertionError((line_count, lower_bound, height_sets))
    return line_count, lower_bound


def exhaustive_search(
    radius_count: int,
    height_count: int,
    height_universe_size: int,
) -> SearchResult:
    candidates = tuple(
        itertools.combinations(range(height_universe_size), height_count)
    )
    if not candidates:
        raise ValueError("height universe is too small")

    best_count: int | None = None
    best_sets: tuple[tuple[int, ...], ...] | None = None
    checked = 0
    for height_sets in itertools.product(candidates, repeat=radius_count):
        checked += 1
        line_count = parameter_line_count(geometric_circles(height_sets))
        if best_count is None or line_count < best_count:
            best_count = line_count
            best_sets = height_sets

    assert best_count is not None and best_sets is not None
    point_count = radius_count * height_count
    return SearchResult(
        radius_count=radius_count,
        height_count=height_count,
        height_universe_size=height_universe_size,
        configurations_checked=checked,
        minimum_line_count=best_count,
        point_count=point_count,
        minimum_over_f_three_halves=best_count / point_count**1.5,
        minimizer=best_sets,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-large-search", action="store_true")
    args = parser.parse_args()

    searches = [
        exhaustive_search(3, 3, 6),
        exhaustive_search(4, 3, 5),
        exhaustive_search(3, 4, 6),
    ]
    if args.include_large_search:
        searches.append(exhaustive_search(3, 3, 7))

    thin_slab_sets = (
        (0, 1, 4, 7),
        (0, 2, 5),
        (1, 3, 6, 8, 9),
        (0, 9),
    )
    line_count, lower_bound = verify_thin_slab_instance(
        thin_slab_sets,
        radial_scale=11,
    )
    identical_height_set = (0, 2, 9, 20, 21)
    identical_sets = (identical_height_set,) * 5
    identical_line_count = parameter_line_count(
        geometric_circles(identical_sets)
    )
    identical_lower_bound = identical_height_energy_lower_bound(
        5,
        identical_height_set,
    )
    payload = {
        "thin_slab_check": {
            "line_count": line_count,
            "theorem_lower_bound": lower_bound,
            "height_sets": thin_slab_sets,
        },
        "identical_height_check": {
            "line_count": identical_line_count,
            "energy_lower_bound": identical_lower_bound,
            "all_offset_sets_sidon": all(
                has_sidon_differences(values)
                for values in offsets_by_product(5).values()
            ),
            "height_set": identical_height_set,
        },
        "exhaustive_searches": [asdict(result) for result in searches],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
