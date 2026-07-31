from fractions import Fraction

from verify_four_plane_matching_barrier import (
    adjacent_coefficient,
    cell_weight,
    diagonalization_identity,
    horizontal_labels,
    verify_coefficient_diverse_case,
    verify_case,
)


def test_exact_euclidean_matching_barrier_small_cases() -> None:
    for k, q in ((1, 3), (2, 4), (3, 5), (4, 6)):
        result = verify_case(k, q)
        assert result["point_count"] == 2 * k * q
        assert result["squared_distances_including_zero"] == 2 * k * q
        assert result["nonzero_squared_distances"] == 2 * k * q - 1
        assert result["exact_arithmetic"] is True


def test_all_adjacent_matching_coefficients_are_identical() -> None:
    for k in range(1, 8):
        coefficients = {adjacent_coefficient(k, edge) for edge in range(k)}
        assert len(coefficients) == 1


def test_horizontal_fractional_layers_are_strict_and_below_one() -> None:
    for k in range(1, 8):
        labels = horizontal_labels(k)
        assert labels[0] == 0
        assert labels == sorted(set(labels))
        assert labels[-1] < 1


def test_rich_cell_threshold() -> None:
    for q in range(2, 20):
        for height_difference in range(q // 2 + 1):
            assert cell_weight(q, height_difference) >= q


def test_split_normal_form_identity_exactly() -> None:
    rationals = (
        Fraction(-5, 7),
        Fraction(-1, 3),
        Fraction(0),
        Fraction(2, 9),
        Fraction(8, 9),
    )
    for c in rationals:
        assert -1 < c < 1
        assert diagonalization_identity(
            c, Fraction(2, 3), Fraction(-7, 5), Fraction(11, 13)
        )


def test_coefficient_diverse_ruled_barrier() -> None:
    for k, q in ((1, 4), (2, 5), (3, 6), (4, 7)):
        result = verify_coefficient_diverse_case(k, q)
        assert result["point_count"] == 2 * k * q
        assert result["distinct_squared_coefficients"] == k
        assert (
            result["squared_distances_including_zero"]
            <= result["upper_bound_3KQ"]
        )
        assert result["exact_arithmetic"] is True
