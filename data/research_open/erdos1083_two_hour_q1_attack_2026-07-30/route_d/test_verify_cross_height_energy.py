from fractions import Fraction

from verify_cross_height_energy import (
    cancellation_model,
    endpoint_certificate,
    minimal_row_pair_bound,
    two_ninths_endpoint_certificate,
)


def test_endpoint_certificate() -> None:
    cert = endpoint_certificate()
    assert cert["same_height_gap"].numerator == 26
    assert cert["same_height_gap"].denominator == 41
    assert cert["minimal_row_height_gap"].numerator == 6


def test_euclidean_cancellation_model() -> None:
    cert = cancellation_model(5, 7, 11)
    assert cert["target_count"] == 77
    assert cert["target_plane_count"] == 77
    assert cert["distance_count"] <= 2 * cert["target_count"]
    assert cert["reverse_circle_count"] == 11
    assert cert["source_points_per_reverse_circle"] == 5
    assert cert["producers_per_reverse_circle"] == 7


def test_model_grid() -> None:
    for source_count in range(2, 7):
        for row_size in range(source_count, 8):
            for height_count in range(2, 9):
                cert = cancellation_model(source_count, row_size, height_count)
                assert cert["distance_count"] <= cert["distance_upper"]
                assert cert["target_plane_count"] == cert["target_count"]


def test_minimal_row_pair_bound() -> None:
    assert minimal_row_pair_bound(1) == 0
    assert minimal_row_pair_bound(2) == 2
    assert minimal_row_pair_bound(8) == 56


def test_two_ninths_cross_height_gaps() -> None:
    cert = two_ninths_endpoint_certificate()
    assert cert["same_height_gap"] == Fraction(5, 9)
    assert cert["minimal_row_height_gap"] == Fraction(1, 9)
