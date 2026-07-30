#!/usr/bin/env python3
"""Tests for the weighted-chart extraction interface."""

from __future__ import annotations

import random
from fractions import Fraction

from verify_cross_plane_weighted_chart_interface import (
    audit,
    chord_length,
    pentagonal_prism_ledger,
    radial_statistics,
    rational_chord_certificate,
    rational_unit_point,
)


def test_radial_energy_to_overlap_inequality():
    generator = random.Random(1083)
    for _ in range(200):
        data = {
            radius: [
                generator.randint(0, 30)
                for _ in range(generator.randint(2, 8))
            ]
            for radius in range(generator.randint(1, 10))
        }
        result = radial_statistics(data)
        if result["U"] == 0:
            assert result["cross_energy"] == 0
        else:
            assert (
                result["weighted_overlap"]*result["U"]
                >= result["cross_energy"]
            )


def test_rational_unit_circle_chords():
    parameters = (
        Fraction(0),
        Fraction(3, 4),
        Fraction(5, 12),
    )
    points = [rational_unit_point(value) for value in parameters]
    chords = {
        chord_length(points[left], points[right])
        for left in range(3)
        for right in range(left)
    }
    assert chords == {
        Fraction(6, 5),
        Fraction(10, 13),
        Fraction(32, 65),
    }


def test_rational_chord_layer_cake_with_empty_and_gapped_fibres():
    parameters = (
        Fraction(0),
        Fraction(3, 4),
        Fraction(5, 12),
    )
    radii = (1, 2, 3, 4, 5)
    height_sets = {}
    for ray in range(3):
        for radius in radii:
            size = (5*ray+3*radius) % 11
            if (ray+radius) % 5 == 0:
                size = 0
            height_sets[(ray, radius)] = {
                7*index+2*ray-radius
                for index in range(size)
            }
    result = rational_chord_certificate(
        parameters, radii, height_sets
    )
    assert result["scale_q"] == 65
    assert result["distance_labels"] >= (
        result["theorem_lower_bound"]
    )
    assert result["distance_inputs"] > 0


def test_pentagonal_prism_exact_no_go():
    for height in range(1, 30):
        result = pentagonal_prism_ledger(height)
        assert result["points"] == 5*height
        assert result["Omega_cyl"] == 20*height
        assert result["distance_labels"] == 3*height
        assert not result["ratio_is_rational"]
        assert result["cross_plane_codegree"] > 0


def test_full_extraction_interface_audit():
    result = audit()
    assert (
        result["verdict"]
        == "PARTIAL_THEOREMS_PASS_FULL_EXTRACTION_OPEN"
    )
    assert len(result["missing_branches"]) == 2
    assert (
        result["critical_success_condition"]
        == "chi+kappa<1 at gamma=7,u=2"
    )
