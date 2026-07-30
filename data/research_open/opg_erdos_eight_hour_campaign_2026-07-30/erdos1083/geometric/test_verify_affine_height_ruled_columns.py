#!/usr/bin/env python3
"""Tests for affine-height ruled-column expansion."""

from __future__ import annotations

from verify_affine_height_ruled_columns import (
    affine_shift_table,
    audit,
    divisor_count,
    ruled_column_certificate,
    squared_distance,
)


def brute_divisor_count(value):
    return sum(value % divisor == 0 for divisor in range(1, value+1))


def test_divisor_count():
    for value in range(1, 500):
        assert divisor_count(value) == brute_divisor_count(value)


def test_encoded_distance_is_cartesian_distance():
    for slope in range(-3, 4):
        for other_slope in range(-3, 4):
            left = (slope, 4, 7)
            right = (other_slope, 2, -5)
            cartesian_left = (4, 4*slope, 7)
            cartesian_right = (2, 2*other_slope, -5)
            expected = sum(
                (a-b)**2
                for a, b in zip(cartesian_left, cartesian_right)
            )
            assert squared_distance(left, right) == expected


def test_common_height_columns():
    for t in range(3, 9):
        slopes = tuple(range(1, t+1))
        radial = tuple(range(1, t+1))
        shifts = {
            (slope, value): 0
            for slope in slopes
            for value in radial
        }
        result = ruled_column_certificate(
            slopes, radial, t*t, shifts
        )
        assert result["raw_inputs"] == t*(t-1)*t*t
        assert result["distinct_distance_labels"] >= (
            result["theorem_lower_bound"]
        )
        assert result["maximum_squared_distance"] < 2*t**4


def test_affine_height_columns():
    for t in range(3, 9):
        slopes = tuple(range(1, t+1))
        radial = tuple(range(1, t+1))
        coefficients = {
            slope: slope % 3-1 for slope in slopes
        }
        intercepts = {
            slope: 2*slope-t for slope in slopes
        }
        shifts = affine_shift_table(
            slopes, radial, coefficients, intercepts
        )
        result = ruled_column_certificate(
            slopes, radial, t*t, shifts
        )
        assert result["distinct_products"] >= (
            t*(t-1)/result["product_divisor_bound"]
        )
        assert result["distinct_distance_labels"] >= (
            result["post_product_inputs"]
            / result["r2_divisor_bound"]
        )


def test_arbitrary_bounded_integer_column_translates():
    for t in range(3, 8):
        slopes = tuple(range(-t//2, t//2+1))
        radial = tuple(range(1, t+1))
        shifts = {
            (slope, value): (
                (slope*slope+3*value+2*slope*value) % (t*t)
            )-t*t//2
            for slope in slopes
            for value in radial
        }
        result = ruled_column_certificate(
            slopes, radial, t*t, shifts
        )
        assert result["distinct_distance_labels"] >= (
            result["theorem_lower_bound"]
        )


def test_full_affine_height_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert result["covers_common_height"]
    assert result["covers_affine_height_shifts"]
