#!/usr/bin/env python3
"""Regression test for the compact final q=2 layer k=8."""

from __future__ import annotations

import json
from pathlib import Path

from verify_q2_k8_reserve import build_audit


CERTIFICATE = Path(__file__).with_name(
    "q2_k8_extension_certificate.json"
)


def test_saved_q2_k8_certificate_is_reproducible() -> None:
    saved = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    rebuilt = build_audit()
    assert rebuilt == saved
    assert rebuilt["model_range"] == {
        "maximum_forest_size_on_six_vertices": 5,
        "total_colored_copies": 10,
        "maximum_possible_k": 8,
    }
    assert [
        (
            row["k"],
            row["negative_count"],
            row["matching_size"],
            row["deficiency"],
        )
        for row in rebuilt["prior_certified_layers"]
    ] == [
        (1, 2, 2, 0),
        (2, 115, 115, 0),
        (3, 1585, 1585, 0),
        (4, 10730, 10730, 0),
        (5, 43648, 43648, 0),
        (6, 112200, 112200, 0),
        (7, 172800, 172800, 0),
    ]
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
        124416,
        124416,
        138816,
        115324,
        9092,
        5114592,
        124416,
        0,
    )
    assert (
        layer["direct_or_single_hall_source_count"],
        layer["direct_or_single_hall_target_count"],
    ) == (18216, 9124)
    completion = layer["base_to_expanded_completion"]
    assert completion["augmenting_path_count"] == 9092
    assert completion["augmenting_path_length_histogram"] == {
        "1": 19,
        "2": 6545,
        "3": 2272,
        "4": 225,
        "5": 30,
        "6": 1,
    }
    assert completion["new_edges_per_path_histogram"] == {
        "1": 23,
        "2": 6653,
        "3": 2179,
        "4": 209,
        "5": 27,
        "6": 1,
    }
    assert rebuilt["resource_accounting"] == {
        "preconstruction_maximum_candidate_degree_bound": 126,
        "preconstruction_expanded_csr_upper_bound_bytes": 63701000,
        "representation": "uint64 row offsets plus uint32 target indices",
        "base_csr_bytes": 1550600,
        "expanded_csr_bytes": 21453704,
        "combined_csr_bytes": 23004304,
        "python_list_adjacency_not_materialized": True,
    }
