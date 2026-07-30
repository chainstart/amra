"""Tests for the fully independent dense ruled-column audit."""

from independent_verify_dense_ruled_columns import (
    audit,
    brute_two_square_count,
    common_denominator_scaling_audit,
    critical_exponent_audit,
    independent_dense_certificate,
    independent_divisor_count,
)


def test_full_independent_audit():
    result = audit(exhaustive=True)
    assert result["verdict"] == "PASS_WITH_SHARPENING"
    assert result["exhaustive_occupancy_patterns"] == 64
    assert result["critical_exponents"]["distance_exponent"] == "4"
    primary = result["primary"]
    assert primary["star_sum"] == primary["psi"]
    assert (
        primary["left_star"] + primary["right_star"]
        == primary["base_star"]
    )
    assert (
        2 * primary["retained_side"] >= primary["base_star"]
    )
    assert primary["signed_products"] >= primary["positive_products"]


def test_independent_number_theory_primitives():
    assert [independent_divisor_count(value) for value in range(1, 11)] == [
        1, 2, 2, 3, 2, 4, 2, 4, 3, 4
    ]
    assert brute_two_square_count(1) == 4
    assert brute_two_square_count(5) == 8
    assert brute_two_square_count(25) == 12
    for value in range(1, 100):
        assert (
            brute_two_square_count(value)
            <= 4 * independent_divisor_count(value)
        )


def test_both_sides_and_gapped_height_fibres():
    slopes = (-5, -2, 1, 4, 9)
    radials = (1, 2, 3, 5, 8)
    occupied = (
        {(1, radial) for radial in radials}
        | {(-5, 1), (-2, 2), (4, 5), (9, 8)}
    )
    heights = {
        column: tuple(
            7 * index * index + 3 * column[0] - column[1]
            for index in range(5)
        )
        for column in occupied
    }
    result = independent_dense_certificate(
        slopes, radials, occupied, heights, 5
    )
    assert result["left_star"] > 0
    assert result["right_star"] > 0
    assert result["signed_products"] >= result["positive_products"]
    assert result["actual_distance_labels"] > 0


def test_empty_and_zero_second_moment_cases_are_harmless():
    slopes = (0, 2, 7)
    radials = (1, 3, 8)
    for occupied in (
        set(),
        {(0, 1), (2, 3), (7, 8)},
    ):
        heights = {
            column: (-10 + column[0], 1, 20 + column[1])
            for column in occupied
        }
        result = independent_dense_certificate(
            slopes, radials, occupied, heights, 3
        )
        assert result["psi"] == 0
        assert result["original_bound"] == "0"
        assert result["sharpened_bound"] == "0"


def test_common_denominator_scope_and_exponent_ledger():
    result = common_denominator_scaling_audit(
        12,
        (-7, 1, 8),
        (1, 5),
        (-11, 4, 9),
    )
    assert result["coordinate_scale"] == 144
    assert result["squared_distance_scale"] == 20736
    assert result["scaled_points"] == 18
    exponents = critical_exponent_audit()
    assert exponents["radial_second_moment_exponent"] == "3"
    assert exponents["distance_exponent"] == "4"
