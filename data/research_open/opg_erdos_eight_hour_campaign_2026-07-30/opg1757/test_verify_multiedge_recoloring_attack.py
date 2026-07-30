#!/usr/bin/env python3
"""Regression tests for the q=2,k=5 multiedge recolouring attack."""

from __future__ import annotations

import json
from pathlib import Path

from verify_global_cycle_opening import E, F, is_forest
from verify_multiedge_recoloring_attack import (
    VERTEX_COUNT,
    active_vertices,
    apply_protected_basis_exchange,
    build_audit,
    inverse_protected_basis_exchange,
    inverse_tagged_two_stage_move,
    tagged_two_stage_move,
)


CERTIFICATE = Path(__file__).with_name(
    "multiedge_recoloring_attack_certificate.json"
)


def test_protected_basis_exchange_and_tagged_chain_inverse() -> None:
    source = (
        frozenset({(0, 2), (0, 3), (1, 2)}),
        frozenset({E, (1, 3), F, (4, 5)}),
    )
    reserve = (0, (1, 2), (0, 2))
    target, tag = tagged_two_stage_move(
        VERTEX_COUNT, source, reserve
    )
    assert all(is_forest(VERTEX_COUNT, forest) for forest in target)
    assert E in target[0] and E not in target[1] and F in target[1]
    assert active_vertices(target) == active_vertices(source)
    assert inverse_tagged_two_stage_move(
        VERTEX_COUNT, target, tag
    ) == source

    base = inverse_protected_basis_exchange(
        VERTEX_COUNT, target, *reserve
    )
    assert (
        apply_protected_basis_exchange(
            VERTEX_COUNT, base, *reserve
        )
        == target
    )


def test_saved_certificate_is_exactly_reproducible() -> None:
    saved = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    rebuilt = build_audit()
    assert rebuilt == saved
    layer = rebuilt["layer"]
    assert (
        layer["negative_count"],
        layer["positive_count"],
        layer["direct_or_single_matching_size"],
        layer["direct_or_single_deficiency"],
        layer["expanded_matching_size"],
        layer["expanded_deficiency"],
    ) == (43648, 45620, 43642, 6, 43648, 0)
    assert layer["augmenting_path_count"] == 6
    assert layer["augmenting_path_lengths"] == [2] * 6

    kernel = rebuilt["hall_kernel"]
    assert (
        kernel["source_count"],
        kernel["target_count"],
        kernel["deficiency"],
        kernel["reserve_graph_matching_size"],
    ) == (12, 6, 6, 12)
    assert [
        (
            block["source_count"],
            block["all_same_union_target_count"],
            block["hall_deficiency_with_arbitrary_recoloring"],
        )
        for block in kernel["same_union_blocks"]
    ] == [(8, 4, 4), (4, 6, 0)]
    assert all(
        len(bucket["source_indices"]) == 2
        for bucket in kernel["collision_buckets"]
    )
