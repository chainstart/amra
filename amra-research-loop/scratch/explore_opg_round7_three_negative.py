#!/usr/bin/env python3
"""Discovery-only exact scans for the eight three-negative route chambers."""

from __future__ import annotations

from pathlib import Path
import sys


SCRATCH = Path(__file__).parent
EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path[:0] = [str(SCRATCH), str(EVIDENCE)]

from explore_opg_round7_plr_quartic import (  # noqa: E402
    bernstein_entries,
    common_monomial,
    divide_monomial,
    divide_one_minus_variable,
)
from verify_c_zero_fibre import (  # noqa: E402
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_nonnegative_route_chambers import (  # noqa: E402
    B_EDGE,
    add,
    coefficient,
    multiply,
    state_polynomial,
)


T_SLOTS = (2, 4, 6)
DIVISIBLE_T_SLOTS = (4, 6)


def build_delta():
    deletion, connectivity, _, _ = reconstruct_original()
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    return add_original(
        multiply_original(a_slope, e_zero),
        multiply_original(d_slope, c_zero),
        -1,
    )


def determinant(entries):
    return add(multiply(entries[0], entries[2]), multiply(entries[1], entries[1]), -1)


def signs(poly):
    return len(poly), sum(value < 0 for value in poly.values())


def scan_quadratic_discriminants(poly):
    rows = []
    for slot, name in ((0, "c"), (1, "q0"), (3, "q3"), (5, "q4")):
        degree = max(monomial[slot] for monomial in poly)
        if degree != 2:
            continue
        entries = tuple(coefficient(poly, slot, index) for index in range(3))
        discriminant = add(
            multiply(entries[1], entries[1]),
            multiply(entries[0], entries[2]),
            -4,
        )
        rows.append({
            "variable": name,
            "entry_signs": [signs(entry) for entry in entries],
            "discriminant": signs(discriminant),
            "discriminant_common": common_monomial(discriminant),
        })
    return rows


def scan_state(delta, state):
    cleared = state_polynomial(delta, tuple(state))
    quotient = cleared
    for slot in DIVISIBLE_T_SLOTS:
        quotient = divide_one_minus_variable(quotient, slot)
    row = {
        "state": state,
        "cleared": len(cleared),
        "quotient": signs(quotient),
        "degrees": [max(monomial[slot] for monomial in quotient) for slot in range(7)],
        "directions": [],
    }
    for slot, name in ((4, "t3"), (6, "t4")):
        entries = bernstein_entries(quotient, slot, 2)
        det = determinant(entries)
        common = common_monomial(det)
        residual = divide_monomial(det, common)
        row["directions"].append({
            "first": name,
            "entries": [signs(entry) for entry in entries],
            "determinant": signs(det),
            "common": common,
            "residual": signs(residual),
            "quadratic_discriminants": scan_quadratic_discriminants(residual),
        })
    return row


def main():
    delta = build_delta()
    for state in ("LLL", "LLR", "LRR"):
        print(scan_state(delta, state))


if __name__ == "__main__":
    main()
