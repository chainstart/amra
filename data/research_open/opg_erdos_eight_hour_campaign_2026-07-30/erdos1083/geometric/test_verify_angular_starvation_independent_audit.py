#!/usr/bin/env python3
"""Tests for the independent angular-starvation audit."""

from __future__ import annotations

from fractions import Fraction

import sympy as sp

from verify_angular_starvation_independent_audit import (
    audit,
    exponent_ledger,
    ruled_product_and_distance_fibres,
    resultant_degree_for_two_targets,
    target_circle_coefficients,
    two_target_difference_coefficients,
    weak_lambda_quantifier_counterexample,
)


def test_circle_repetition_classification():
    assert (
        target_circle_coefficients(0, 7, 2, 80)
        == target_circle_coefficients(0, -7, 2, 80)
    )
    assert (
        target_circle_coefficients(1, 7, 2, 80)
        != target_circle_coefficients(1, -7, 2, 80)
    )
    assert (
        target_circle_coefficients(sp.Rational(3, 5), 7, 2, 80)
        != target_circle_coefficients(sp.Rational(3, 5), -7, 2, 80)
    )


def test_two_target_positive_dimensional_classification():
    assert two_target_difference_coefficients(
        0, (7, 2), (-7, 2)
    ) == (0, 0, 0)
    assert two_target_difference_coefficients(
        1, (7, 2), (-7, 2)
    ) != (0, 0, 0)
    assert two_target_difference_coefficients(
        0, (7, 2), (-7, 3)
    ) != (0, 0, 0)


def test_nondegenerate_two_target_system_is_at_most_quadratic():
    cases = [
        (sp.Rational(3, 5), (1, 2), (4, -1), 25),
        (1, (1, 2), (4, -1), 25),
        (0, (1, 2), (4, -1), 25),
    ]
    for cosine, first, second, distance in cases:
        degree = resultant_degree_for_two_targets(
            cosine, first, second, distance
        )
        assert degree is not None
        assert degree <= 2


def test_theorem_three_exponents():
    ledger = exponent_ledger()
    assert ledger["aggregate_energy"] == Fraction(13, 5)
    assert ledger["diagonal_energy"] == Fraction(12, 5)
    assert ledger["aggregate_minus_diagonal_gap"] == Fraction(1, 5)
    assert ledger["radius_energy_to_mass"] == Fraction(3, 5)


def test_lambda_radius_quantifier_must_be_bound():
    example = weak_lambda_quantifier_counterexample(100)
    assert example["energy"] == 10001
    assert example["averaging_floor"] > 1
    assert not example["good_radius_is_energy_witness"]


def test_ruled_product_and_sum_of_two_squares_fibres():
    for t in range(3, 12):
        result = ruled_product_and_distance_fibres(
            t, range(1, t)
        )
        assert result["maximum_product_fibre"] <= (
            result["product_divisor_bound"]
        )
        assert result["maximum_distance_fibre"] <= (
            result["r2_divisor_bound"]
        )
        assert result["maximum_label"] <= 2*t**4
        assert result["distinct_products"] >= (
            result["input_products"]
            / result["product_divisor_bound"]
        )
        assert result["distinct_distance_labels"] >= (
            result["sum_of_two_squares_inputs"]
            / result["r2_divisor_bound"]
        )


def test_full_independent_audit_verdict():
    result = audit()
    assert result["verdict_as_written"] == "PASS"
    assert result["theorem_3_mass_and_exponents"] == "PASS"
    assert (
        result["proposition_4"]
        == "PASS_WITNESS_RADIUS_AND_ANCHOR_BOUND"
    )
    assert result["cross_plane_transfer_32a_32c"] == "PASS"
