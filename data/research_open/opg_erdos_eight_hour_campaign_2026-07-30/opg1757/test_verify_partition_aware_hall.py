#!/usr/bin/env python3
"""Regression tests for the partition-aware OPG-1757 proof attack."""

from __future__ import annotations

import json
from pathlib import Path

from verify_partition_aware_hall import (
    build_audit,
    incidence_forest,
    refines,
    safe_by_split_then_merge,
    safe_coarsening_by_quotient,
)


CERTIFICATE = Path(__file__).with_name(
    "partition_aware_hall_certificate.json"
)


def test_partition_direction_and_context_aware_merge() -> None:
    discrete = (0, 1, 2, 3)
    merge_01 = (0, 0, 1, 2)
    external_discrete = (0, 1, 2, 3)
    external_01 = (0, 0, 1, 2)

    assert refines(discrete, merge_01)
    assert not refines(merge_01, discrete)
    assert incidence_forest(discrete, external_discrete)
    assert safe_coarsening_by_quotient(
        discrete, merge_01, external_discrete
    )
    assert incidence_forest(merge_01, external_discrete)

    assert incidence_forest(discrete, external_01)
    assert not incidence_forest(merge_01, external_01)
    assert not safe_coarsening_by_quotient(
        discrete, merge_01, external_01
    )
    assert safe_by_split_then_merge(
        merge_01, discrete, external_discrete
    )


def test_saved_certificate_is_exactly_reproducible() -> None:
    saved = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    rebuilt = build_audit()
    assert rebuilt == saved
    assert [row["partition_count"] for row in rebuilt["partition_state_rows"]] == [
        1,
        2,
        5,
        15,
        52,
        203,
    ]
    hall = rebuilt["q2_k3_hall_partition_audit"]
    assert (
        hall["hall_source_count"],
        hall["hall_target_count"],
        hall["hall_deficiency"],
        hall["active_active_escape_count"],
    ) == (8, 6, 2, 8)
    assert all(
        row["colored_joint_safe_context_count"] > 0
        for row in hall["escape_rows"]
    )
    assert all(
        row["red_universal_merge_witness"] is not None
        or row["blue_universal_merge_witness"] is not None
        for row in hall["escape_rows"]
    )
    context_kernel = hall["partition_restricted_hall_kernel"]
    assert context_kernel["four_rule_deficient_context_count"] == 1710
    witness = context_kernel["first_four_rule_context_hall_witness"]
    assert witness["source_indices"] == [1538, 1546]
    assert witness["all_compatible_positive_count"] == 0
    assert witness["all_compatible_negative_count"] > 0
