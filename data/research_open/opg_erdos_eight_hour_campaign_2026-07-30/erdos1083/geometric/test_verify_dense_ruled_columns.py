"""Regression tests for dense ruled-column stability."""

from verify_dense_ruled_columns import (
    audit,
    dense_lattice_column_certificate,
    dense_ruled_column_certificate,
)


def test_saved_sparse_pattern_passes_both_bounds():
    result = audit()
    assert result["verdict"] == "PASS"
    certificate = result["certificate"]
    assert certificate["distinct_distance_labels"] >= (
        certificate["exact_theorem_bound"]
    )
    assert certificate["distinct_distance_labels"] >= (
        certificate["moment_theorem_bound"]
    )


def test_radial_second_moment_and_star_identity():
    slopes = (-3, -1, 0, 2, 5)
    radial_parameters = (1, 2, 3, 4, 5, 6)
    occupied = {
        (slope, radial)
        for slope in slopes
        for radial in radial_parameters
        if (slope - radial) % 4 != 0
    }
    shifts = {
        column: 2 * column[0] - column[1]
        for column in occupied
    }
    result = dense_ruled_column_certificate(
        slopes,
        radial_parameters,
        occupied,
        9,
        shifts,
    )
    assert result["psi"] > 0
    assert result["base_star"] * len(slopes) >= result["psi"]
    assert result["retained_signed_star"] == result["base_star"]


def test_complete_grid_is_included_as_special_case():
    slopes = (0, 1, 3, 4)
    radial_parameters = (1, 2, 4, 5)
    occupied = {
        (slope, radial)
        for slope in slopes
        for radial in radial_parameters
    }
    shifts = {column: 0 for column in occupied}
    result = dense_ruled_column_certificate(
        slopes,
        radial_parameters,
        occupied,
        7,
        shifts,
    )
    expected_psi = (
        len(radial_parameters)
        * len(slopes)
        * (len(slopes) - 1)
    )
    assert result["psi"] == expected_psi


def test_arbitrary_gapped_integer_height_fibres():
    slopes = (-2, 0, 1, 4)
    radial_parameters = (1, 2, 3, 5, 7)
    occupied = {
        (slope, radial)
        for slope in slopes
        for radial in radial_parameters
        if (slope + radial) % 5 != 0
    }
    height_sets = {
        (slope, radial): tuple(
            sorted(
                {
                    3 * index * index
                    + slope * radial
                    - 2 * index
                    for index in range(8)
                }
            )
        )
        for slope, radial in occupied
    }
    result = dense_lattice_column_certificate(
        slopes,
        radial_parameters,
        occupied,
        8,
        height_sets,
    )
    assert result["distinct_distance_labels"] >= (
        result["exact_theorem_bound"]
    )
