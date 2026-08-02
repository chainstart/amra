"""Regression tests for the full-Euclidean interval multirow no-go."""

from verify_full_euclidean_interval_multirow_nogo import (
    coordinate_partition_certificate,
    divisors_below_sqrt,
    euclidean_certificate,
    mixed_radix_certificate,
    squarefree_count_certificate,
)


def test_mixed_radix_interval_tilings_are_direct():
    assert mixed_radix_certificate(11, 6, 1) == 66
    assert mixed_radix_certificate(11, 6, 2) == 66


def test_all_rows_have_the_same_complete_spectrum():
    result = coordinate_partition_certificate(31, 30)
    assert result["leaf_rows"] == 4
    assert result["common_labels"] == 31 * 31 * 30
    assert result["pass"]


def test_common_tangent_and_actual_distance_identity():
    result = euclidean_certificate(31, 30)
    assert result["rows"] == 5
    assert result["common_tangent_positive"]
    assert result["centre_scalar_irrational"]
    assert result["symbolic_distance_cells"] > 0
    assert result["pass"]


def test_squarefree_family_is_unbounded_but_below_sqrt_c():
    assert divisors_below_sqrt(2310) == [
        m for m in range(1, 49) if 2310 % m == 0
    ]
    result = squarefree_count_certificate()
    assert result["squarefree_rows"] == 4
    assert result["pass"]
