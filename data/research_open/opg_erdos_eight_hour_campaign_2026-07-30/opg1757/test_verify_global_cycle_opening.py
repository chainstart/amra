#!/usr/bin/env python3
"""Tests for the deterministic global cycle-opening exchange."""

from __future__ import annotations

import json
from pathlib import Path

from verify_global_cycle_opening import (
    E,
    build_audit,
    cycle_opening_map,
    inverse_from_tag,
    is_forest,
)


CERTIFICATE = Path(__file__).with_name(
    "global_cycle_opening_certificate.json"
)


def test_explicit_outside_path_obstruction_is_opened() -> None:
    # Red star 0-r-1 together with local edge 45 realizes the partition
    # obstruction from PROOF_ATTACK.md.  Vertices r,b are 6,7.
    red = frozenset(
        {(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (4, 5)}
    )
    blue = frozenset(
        {(0, 1), (0, 4), (1, 5), (2, 3), (0, 7), (2, 7)}
    )
    assert is_forest(8, red)
    assert is_forest(8, blue)
    target, tag = cycle_opening_map(8, (red, blue))
    assert tag == (0, 6)
    assert E in target[0] and E not in target[1]
    assert is_forest(8, target[0])
    assert is_forest(8, target[1])
    assert inverse_from_tag(target, tag) == (red, blue)


def test_saved_finite_audit_is_reproducible() -> None:
    saved = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    rebuilt = build_audit()
    assert rebuilt == saved
    small = rebuilt["small_complete_graph_rows"]
    assert [row["forest_count"] for row in small] == [2, 7, 38, 291]
    assert all(
        row["tagged_image_count"] == row["source_pair_count"]
        for row in small
    )
    rows = rebuilt["q2_finite_audit"]["layer_rows"]
    assert [row["k"] for row in rows] == list(range(1, 8))
    assert all(
        row["tagged_image_count"] == row["negative_count"]
        for row in rows
    )
    assert rebuilt["q2_finite_audit"]["first_untagged_collision"] is not None
    union_deficiencies = [
        row["direct_or_single_exchange_matching_deficiency"]
        for row in rows
    ]
    assert union_deficiencies == [0, 0, 0, 0, 6, 856, 5312]
    union_witness = rebuilt["q2_finite_audit"][
        "first_direct_or_single_exchange_hall_witness"
    ]
    assert (
        union_witness["k"],
        union_witness["source_count"],
        union_witness["target_count"],
    ) == (5, 12, 6)
