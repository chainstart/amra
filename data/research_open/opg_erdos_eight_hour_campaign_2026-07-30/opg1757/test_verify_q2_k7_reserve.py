#!/usr/bin/env python3
"""Regression tests for the compact q=2,k=7 reserve audit."""

from __future__ import annotations

import json
from pathlib import Path

from verify_q2_k7_reserve import build_audit


CERTIFICATE = Path(__file__).with_name(
    "q2_k7_extension_certificate.json"
)


def test_saved_q2_k7_certificate_is_reproducible() -> None:
    saved = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    rebuilt = build_audit()
    assert rebuilt == saved
    layer = rebuilt["layer"]
    assert (
        layer["negative_count"],
        layer["positive_count"],
        layer["direct_or_single_edge_count"],
        layer["direct_or_single_matching_size"],
        layer["direct_or_single_deficiency"],
        layer["expanded_edge_count"],
        layer["expanded_matching_size"],
        layer["expanded_deficiency"],
    ) == (
        172800,
        177984,
        306408,
        167488,
        5312,
        8160144,
        172800,
        0,
    )
    assert (
        layer["direct_or_single_hall_source_count"],
        layer["direct_or_single_hall_target_count"],
    ) == (17656, 12344)
    completion = layer["base_to_expanded_completion"]
    assert completion["augmenting_path_count"] == 5312
    assert completion["augmenting_path_length_histogram"] == {
        "1": 667,
        "2": 4557,
        "3": 88,
    }
    assert completion["new_edges_per_path_histogram"] == {
        "1": 715,
        "2": 4510,
        "3": 87,
    }
    assert rebuilt["resource_accounting"] == {
        "representation": "uint64 row offsets plus uint32 target indices",
        "base_csr_bytes": 2608040,
        "expanded_csr_bytes": 34022984,
        "combined_csr_bytes": 36631024,
        "python_list_adjacency_not_materialized": True,
    }
