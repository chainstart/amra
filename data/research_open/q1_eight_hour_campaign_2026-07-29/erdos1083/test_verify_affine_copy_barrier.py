from fractions import Fraction
from math import comb

from verify_affine_copy_barrier import (
    all_pairs_st_exponent,
    balanced_energy_line_exponent,
    construct,
    critical_exponent,
    geometric_grid_line_count,
    sidon_grid_line_count,
)


def test_exact_two_slice_barrier() -> None:
    for q in range(2, 25):
        result = construct(q)
        assert result.affine_copy_count == comb(q, 2)
        assert result.endpoint_union_size == q
        assert result.distinct_parameter_count == comb(q, 2)
        assert result.all_slopes_positive
        assert result.all_height_squares_nonnegative


def test_sidon_balanced_grid_line_count() -> None:
    for radius_count in range(1, 6):
        for height_count in range(1, 7):
            assert sidon_grid_line_count(radius_count, height_count) == (
                height_count * comb(radius_count + 1, 2)
            )
            assert geometric_grid_line_count(radius_count, height_count) == (
                height_count * comb(radius_count + 1, 2)
            )


def test_critical_exponent_thresholds() -> None:
    assert critical_exponent(Fraction(1, 4)) == Fraction(11, 20)
    assert critical_exponent(Fraction(1, 3)) == Fraction(3, 5)
    assert critical_exponent(Fraction(1, 2)) == Fraction(7, 10)
    assert all_pairs_st_exponent(Fraction(4, 3)) == Fraction(3, 5)
    assert all_pairs_st_exponent(Fraction(3, 2)) == Fraction(13, 20)
    assert balanced_energy_line_exponent(Fraction(7, 3)) == Fraction(4, 3)
    assert balanced_energy_line_exponent(Fraction(2, 1)) == Fraction(3, 2)
