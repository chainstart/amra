#!/usr/bin/env python3
"""Regression tests for the independent k=5 audit and k=6 extension."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from independent_verify_multiedge_and_k6 import build_audits


DIRECTORY = Path(__file__).resolve().parent


@pytest.fixture(scope="module")
def rebuilt() -> tuple[dict[str, object], dict[str, object]]:
    return build_audits()


def test_independent_k5_certificate(
    rebuilt: tuple[dict[str, object], dict[str, object]],
) -> None:
    independent, _ = rebuilt
    saved = json.loads(
        (DIRECTORY / "independent_multiedge_audit_certificate.json")
        .read_text(encoding="utf-8")
    )
    assert independent == saved
    assert independent["forest_count"] == 2932
    audit = independent["audit"]
    summary = audit["independent_layer_summary"]
    assert (
        summary["negative_count"],
        summary["positive_count"],
        summary["direct_or_single_edge_count"],
        summary["direct_or_single_matching_size"],
        summary["direct_or_single_deficiency"],
        summary["expanded_edge_count"],
        summary["expanded_matching_size"],
        summary["expanded_deficiency"],
    ) == (43648, 45620, 112556, 43642, 6, 1987196, 43648, 0)
    assert audit["saved_payload_sha256"] == (
        "648d0237235a5e40ebf85a9251172feed"
        "5ae232f7b003396266c173abd1c56a6"
    )
    assert audit["collision_component_sizes"] == [[2, 1]] * 6
    assert audit["same_union_source_target_deficiency_rows"] == [
        [8, 4, 4],
        [4, 6, 0],
    ]


def test_complete_q2_k6_matching(
    rebuilt: tuple[dict[str, object], dict[str, object]],
) -> None:
    _, k6 = rebuilt
    saved = json.loads(
        (DIRECTORY / "q2_k6_extension_certificate.json")
        .read_text(encoding="utf-8")
    )
    assert k6 == saved
    layer = k6["layer"]
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
        112200,
        117384,
        257996,
        111344,
        856,
        5470120,
        112200,
        0,
    )
    completion = layer["base_to_expanded_completion"]
    assert completion["augmenting_path_count"] == 856
    assert completion["augmenting_path_length_histogram"] == {
        "1": 169,
        "2": 687,
    }
    assert completion["new_edges_per_path_histogram"] == {
        "1": 184,
        "2": 672,
    }
