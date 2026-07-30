#!/usr/bin/env python3
"""Regression tests for the marginal-only synchronization audit."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from verify_sync_extraction_drc import (
    build_audit,
    drc_common_mass_bound,
    split_extremizer,
)


CERTIFICATE = Path(__file__).with_name(
    "sync_extraction_drc_certificate.json"
)


def test_split_extremizer_exact_counts() -> None:
    row = split_extremizer(10)
    assert row["points"] == 10**5
    assert row["source_incidence_sum"] == 10**4
    assert row["source_count_per_angle"] == 10**3
    assert row["maximum_source_fibre_angle_degree"] == 1
    assert row["maximum_two_angle_source_codegree"] == 0
    assert row["minimum_rotation_success_over_n"] == Fraction(72, 100)
    assert row["common_rotation_reservoir_mass"] == 9 * 10**4


def test_weighted_drc_and_saved_certificate() -> None:
    bound = drc_common_mass_bound(
        angle_count=20,
        density=Fraction(9, 10),
        threshold=Fraction(1, 2),
        chosen_angles=3,
    )
    assert bound > Fraction(1, 4)
    saved = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    rebuilt = build_audit()
    assert rebuilt == saved
    ledger = rebuilt["exponent_ledger"]
    assert ledger["global_source_incidence_mass"] == "N^(4/5)"
    assert ledger["unconditional_same_radius_sparse_certificate"] == "O(1)"
    assert (
        ledger["resulting_unconditional_distance_exponent"]
        == "does_not_exceed_3/5"
    )
