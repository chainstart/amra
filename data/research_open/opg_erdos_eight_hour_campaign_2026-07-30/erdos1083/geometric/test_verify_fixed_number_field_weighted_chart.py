"""Tests for the fixed-number-field terminal certificate."""

import pytest

from verify_fixed_number_field_weighted_chart import (
    audit,
    divisor_count,
    ideal_divisor_local_envelope,
    integer_two_square_count,
    salem_single_embedding_obstruction,
    unit_log_box_lattice_count,
)


def test_rational_special_case_and_nonzero_boundary():
    assert integer_two_square_count(1) == 4
    assert integer_two_square_count(5) == 8
    assert integer_two_square_count(25) == 12
    for value in range(1, 200):
        assert integer_two_square_count(value) <= 4 * divisor_count(value)
    with pytest.raises(ValueError):
        integer_two_square_count(0)


def test_ideal_divisor_tau_power_envelope():
    result = ideal_divisor_local_envelope(4, 3)
    assert result["patterns_checked"] == 125
    assert result["maximum"] == 125
    assert result["tau_power_envelope"] == 125


def test_fixed_rank_unit_boxes_are_polylogarithmic():
    assert unit_log_box_lattice_count(0, 100) == 1
    assert unit_log_box_lattice_count(1, 10) == 21
    assert unit_log_box_lattice_count(3, 10) == 21**3


def test_single_embedding_height_is_insufficient():
    result = salem_single_embedding_obstruction(24)
    assert result["bounded_distinguished_coordinates"]
    assert result["unbounded_other_conjugate"]
    assert result["last_sample"]["other_conjugate_x_abs"] > 1000


def test_full_number_field_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert result["rational_two_square_checks"] == 500
    assert result["ideal_local_envelopes"] == 20
