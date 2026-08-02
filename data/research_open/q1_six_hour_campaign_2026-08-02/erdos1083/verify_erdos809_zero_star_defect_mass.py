#!/usr/bin/env python3
"""Finite guard for the exact zero-star colour-mass ledger."""

from __future__ import annotations

import itertools
import json


def ledger(
    leaf_count: int,
    supports: tuple[int, ...],
    extra_outer: tuple[int, ...],
) -> dict[str, int | bool]:
    if len(supports) != len(extra_outer):
        raise ValueError("one extra-outer count is required per colour")
    if any(extra < 0 for extra in extra_outer):
        raise ValueError("extra endpoint counts must be nonnegative")

    full_mask = (1 << leaf_count) - 1
    support_sizes = [(mask & full_mask).bit_count() for mask in supports]
    star_mass = sum(support_sizes)
    defect = 0
    predicted_slack = 0
    for size, extra in zip(support_sizes, extra_outer):
        # A colour with star support contains the centre plus all supported
        # leaves. A colour with empty support need not contain the centre.
        endpoint_count = (size + 1 + extra) if size else extra
        defect += max(0, endpoint_count - 1)
        predicted_slack += extra if size else max(0, extra - 1)
    return {
        "leaf_count": leaf_count,
        "colour_count": len(supports),
        "star_mass": star_mass,
        "defect": defect,
        "slack": defect - star_mass,
        "predicted_slack": predicted_slack,
        "pass": star_mass <= defect and defect - star_mass == predicted_slack,
    }


def exhaustive_certificate(max_leaves: int = 4, max_colours: int = 3) -> dict[str, int | bool]:
    systems = 0
    equality_systems = 0
    for leaf_count in range(1, max_leaves + 1):
        masks = tuple(range(1 << leaf_count))
        for colour_count in range(1, max_colours + 1):
            for supports in itertools.product(masks, repeat=colour_count):
                for extra_outer in itertools.product(range(3), repeat=colour_count):
                    result = ledger(leaf_count, supports, extra_outer)
                    assert result["pass"]
                    if result["star_mass"] == result["defect"]:
                        equality_systems += 1
                    systems += 1
    return {
        "max_leaves": max_leaves,
        "max_colours": max_colours,
        "systems": systems,
        "equality_systems": equality_systems,
        "pass": True,
    }


def main() -> int:
    result = exhaustive_certificate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
