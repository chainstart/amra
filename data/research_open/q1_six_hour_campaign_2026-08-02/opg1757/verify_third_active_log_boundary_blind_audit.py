#!/usr/bin/env python3
"""Independent scalar guards for the OPG third-active blind audit.

This file deliberately imports none of the author workbench modules.  It
checks the quantitative domination, retained-shift legality, bulk/top
splice, and fixed-depth obstruction algebra used in the manuscripts.
"""

from __future__ import annotations

import json
import math


OBJECTS = (
    # name, L offset, k offset, low shift, high shift, bulk loss
    ("odd_sufficient", 15, 8, 0, 19, 12),
    ("even_sufficient", 17, 10, 0, 23, 14),
    ("odd_page", 14, 8, 2, 18, 12),
    ("even_page", 16, 10, 2, 22, 14),
)


def retained_shift_guard(max_s: int = 4000) -> dict[str, int | bool]:
    rows = 0
    high_rows = 0
    for name, length_offset, index_offset, low, high, bulk_loss in OBJECTS:
        start = 8 if name.startswith("odd") else 9
        for s in range(start, max_s + 1):
            first = math.ceil(241 * math.log(s))
            last = 2 * s - bulk_loss
            for d in range(first, last + 1):
                length = 2 * s - length_offset
                k = d + index_offset
                low_index = k - low
                if 0 <= low_index <= length:
                    retained = low_index
                else:
                    retained = k - high
                    high_rows += 1
                assert 0 <= retained <= length, (name, s, d, retained, length)
                if name.startswith("odd") and retained == k - high:
                    assert retained <= length - 8
                if name.startswith("even") and retained == k - high:
                    assert retained <= length - 10
                rows += 1
    return {"shift_rows": rows, "high_endpoint_rows": high_rows, "pass": True}


def logarithmic_budget_guard() -> dict[str, float | int | bool]:
    # log(1+x)>x-x^2/2 for x>0.
    lower_65 = 9 / 50
    lower_76 = 11 / 72
    assert 241 * 9 > 30 * 50
    assert 241 * 11 > 36 * 72
    assert 241 * math.log(6 / 5) > 30
    assert 241 * math.log(7 / 6) > 36
    # The four exact q+M budgets quoted in the source tables.
    assert (19 + 11, 18 + 8, 23 + 13, 22 + 10) == (30, 26, 36, 32)
    return {
        "p6_rational_slope": 241 * lower_65,
        "p7_rational_slope": 241 * lower_76,
        "p6_budget": 30,
        "p7_budget": 36,
        "pass": True,
    }


def splice_guard(max_s: int = 4000) -> dict[str, int | bool]:
    rows = 0
    for parity in ("odd", "even"):
        start = 8 if parity == "odd" else 9
        bulk_loss = 12 if parity == "odd" else 14
        top_width = 8 if parity == "odd" else 10
        for s in range(start, max_s + 1):
            bulk_last = 2 * s - bulk_loss
            top_first = 2 * s - 4 - (top_width - 1)
            assert top_first == bulk_last + 1
            assert (2 * s - 4) - top_first + 1 == top_width
            rows += 1
    return {"splice_rows": rows, "pass": True}


def fixed_layer_guard(max_r: int = 100) -> dict[str, int | bool]:
    for r in range(3, max_r + 1):
        slope_kernel = 3**r - 3 * 2**r + 3
        assert slope_kernel > 0
        if r < max_r:
            following = 3 ** (r + 1) - 3 * 2 ** (r + 1) + 3
            assert following - 2 * slope_kernel == 3**r - 3

    def coefficient(s: int, r: int) -> int:
        return (
            408 * 4**r
            - 16 * (2 * s + 87) * 3**r
            + 96 * (s + 18) * 2**r
            - 48 * (2 * s + 19)
        )

    for s in range(8, 200):
        assert coefficient(s, 3) == -96 * (2 * s - 15)
        assert coefficient(s, 4) == -1152 * (s - 16)
    assert coefficient(17, 4) == -1152
    return {"layer_rows": max_r - 2, "first_witness": -1152, "pass": True}


def run_all() -> dict[str, object]:
    result = {
        "retained_shifts": retained_shift_guard(),
        "logarithmic_budget": logarithmic_budget_guard(),
        "splices": splice_guard(),
        "fixed_layer": fixed_layer_guard(),
    }
    result["pass"] = all(bool(row["pass"]) for row in result.values())
    return result


if __name__ == "__main__":
    print(json.dumps(run_all(), sort_keys=True))
