"""Tests for the independent weighted layer-cake red-team audit."""

from independent_verify_weighted_ruled_layer_cake import (
    audit,
    brute_r2,
    exhaustive_height_size_audit,
    independent_weighted_certificate,
    trial_divisor_count,
)


def test_ordered_omega_and_empty_fibres():
    slopes = (0, 1, 2)
    radii = (1, 2)
    heights = {
        (0, 1): (0, 3, 8),
        (1, 1): (5, 9),
        (2, 1): (),
        (0, 2): (-7,),
        (1, 2): (4, 12, 19, 30),
    }
    result = independent_weighted_certificate(slopes, radii, heights)
    assert result["Omega"] == 6
    assert result["ordered_overlap_tokens"] == 6
    assert result["star_sum"] == 6


def test_signed_products_retain_both_sides_without_two():
    slopes = (-5, -1, 2, 6, 10)
    radii = (1, 2, 3, 5, 7)
    # Make slope 2 the unique heaviest star while its neighbours occupy
    # both signs.  Fibre sizes are deliberately nonuniform.
    heights = {
        (2, radius): tuple(range(-radius, 8 + radius))
        for radius in radii
    }
    heights.update({
        (-5, 1): (-20, -3, 11),
        (-1, 2): (-8, 4, 17, 31),
        (6, 3): (-13, 2, 9, 26, 44),
        (10, 5): (-21, 0, 23),
    })
    result = independent_weighted_certificate(slopes, radii, heights)
    assert result["base"] == 2
    assert result["signed_negative_pairs"] > 0
    assert result["signed_positive_pairs"] > 0
    assert result["constant_two_removed"]
    assert result["anchored_inputs"] == (
        result["selected_H"] * result["signed_products"]
    )


def test_arbitrary_gapped_height_anchor_and_two_square_fibres():
    slopes = (-3, 0, 4)
    radii = (1, 3, 5)
    heights = {
        (slope, radius): tuple(
            11 * index * index
            - 7 * index
            + 5 * slope
            - 2 * radius
            for index in range((slope + radius) % 5 + 1)
        )
        for slope in slopes
        for radius in radii
    }
    result = independent_weighted_certificate(slopes, radii, heights)
    assert result["status"] == "nonvacuous_checks_passed"
    assert result["selected_distance_labels"] <= (
        result["actual_distance_labels"]
    )
    for value in range(1, 100):
        assert brute_r2(value) <= 4 * trial_divisor_count(value)


def test_exhaustive_small_height_profiles():
    result = exhaustive_height_size_audit()
    assert result["profiles"] == 729
    assert 0 < result["nonvacuous_profiles"] < 729


def test_full_independent_audit():
    result = audit(exhaustive=True)
    assert result["verdict"] == "PASS"
    assert result["exhaustive"]["profiles"] == 729
    assert result["primary"]["constant_two_removed"]
