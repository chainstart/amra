#!/usr/bin/env python3
"""Tests for weighted ruled-column layer cake."""

from __future__ import annotations

import random

from verify_weighted_ruled_layer_cake import (
    audit,
    layer_cake_certificate,
    normalized_height_sets,
    squared_distance,
    weighted_overlap,
)


def test_weighted_overlap_counts_ordered_pairs_and_empty_fibres():
    slopes = (0, 1, 2)
    radii = (1, 2)
    raw = {
        (0, 1): {0, 1, 2},
        (1, 1): {4, 5},
        (2, 1): set(),
        (0, 2): {7},
        (1, 2): {8, 9, 10, 11},
    }
    heights = normalized_height_sets(slopes, radii, raw)
    # radius 1: min(3,2) in both orientations; radius 2:
    # min(1,4) in both orientations.  All other terms meet an empty set.
    assert weighted_overlap(slopes, radii, heights) == 6


def test_encoded_distance_is_genuine_cartesian_distance():
    left = (-3, 5, 17)
    right = (2, 5, -11)
    encoded = squared_distance(left, right)
    p = (5, -15, 17)
    q = (5, 10, -11)
    cartesian = sum((a-b)**2 for a, b in zip(p, q))
    assert encoded == cartesian


def test_highly_nonuniform_gapped_height_sets():
    slopes = tuple(range(-3, 4))
    radii = tuple(range(1, 8))
    height_sets = {}
    sizes = (0, 1, 2, 3, 7, 16, 31)
    for slope in slopes:
        for radius in radii:
            size = sizes[(slope+2*radius) % len(sizes)]
            height_sets[(slope, radius)] = {
                13*index+5*slope-2*radius
                for index in range(size)
            }
    result = layer_cake_certificate(
        slopes, radii, height_sets
    )
    assert result["Omega"] > 0
    assert result["selected_H"] in (1, 2, 4, 8, 16)
    assert result["layer_product"]*result["dyadic_levels"] >= (
        result["selected_star_weight"]
    )
    assert result["distinct_distance_labels"] >= (
        result["theorem_lower_bound"]
    )


def test_random_finite_layer_cake_certificates():
    generator = random.Random(1083)
    for trial in range(20):
        slopes = tuple(range(-2, 3))
        radii = tuple(range(1, 6))
        height_sets = {}
        for slope in slopes:
            for radius in radii:
                size = generator.randint(0, 20)
                height_sets[(slope, radius)] = {
                    generator.randint(-100, 100)
                    for _ in range(size)
                }
        heights = normalized_height_sets(
            slopes, radii, height_sets
        )
        if weighted_overlap(slopes, radii, heights) == 0:
            continue
        result = layer_cake_certificate(
            slopes, radii, height_sets
        )
        assert result["maximum_product_fibre"] <= (
            result["product_divisor_bound"]
        )
        assert result["maximum_distance_fibre"] <= (
            result["r2_divisor_bound"]
        )
        assert result["distinct_distance_labels"] >= (
            result["theorem_lower_bound"]
        )


def test_duplicate_input_heights_are_deduplicated():
    slopes = (0, 1)
    radii = (1,)
    raw = {
        (0, 1): [0, 0, 1, 1, 2],
        (1, 1): [5, 5, 6, 7, 8],
    }
    heights = normalized_height_sets(slopes, radii, raw)
    assert heights[(0, 1)] == (0, 1, 2)
    assert heights[(1, 1)] == (5, 6, 7, 8)
    assert weighted_overlap(slopes, radii, heights) == 6
    result = layer_cake_certificate(slopes, radii, raw)
    assert result["U"] == 4


def test_full_weighted_layer_cake_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert result["finite_ledger"]["Omega"] > 0
    assert "t^(4+eta-o(1))" in result["critical_interface"]
