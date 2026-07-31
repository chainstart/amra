from fractions import Fraction

from verify_spectral_block_breakthrough import (
    affine_quadratic_three_row_model,
    build_exact_block_model,
    direct_tiling_rank_certificate,
    endpoint_certificate,
    hypercube_identical_spectrum_model,
    parabolic_resolution_endpoint_certificate,
    parabolic_lift_certificate,
)


def test_endpoint_identities() -> None:
    result = endpoint_certificate()
    assert result["pass"]
    assert result["block_size"] == "13/18"
    assert result["number_blocks"] == "25/18"
    assert result["pair_count"] == "17/6"
    assert result["intersection_mass"] == "40/9"


def test_exact_block_has_at_most_two_transverse_dilation_spaces() -> None:
    result = direct_tiling_rank_certificate()
    assert result["pass"]
    assert result["log_S_SU_exponent_limit"] == "29/14"
    assert result["independent_dilation_space_bound"] == 2


def test_parabolic_resolution_endpoint_ledger() -> None:
    result = parabolic_resolution_endpoint_certificate()
    assert result["pass"]
    assert result["fixed_difference_energy"] == "19/18"
    assert result["rich_tangent_row_degree"] == "5/9"
    assert result["tangent_pair_mass"] == "19/9"
    assert result["one_fibre_value_capacity"] == "4/3"
    assert result["one_fibre_cannot_fill_spectrum"]


def test_exact_block_design_saturates_cauchy_schwarz() -> None:
    result = build_exact_block_model(4, 3, 6)
    assert result["rows"] == 12
    assert result["union_size"] == 24
    assert result["label_degree"] == 3
    assert result["cs_equality"]
    assert result["zero_or_full_intersections"]
    assert result["label_variance"] == "0"
    assert result["fractional_defect"] == 0


def test_block_model_rejects_invalid_parameters() -> None:
    try:
        build_exact_block_model(0, 3, 6)
    except ValueError as error:
        assert "positive" in str(error)
    else:
        raise AssertionError("zero group count should be rejected")


def test_three_distinct_heights_have_one_identical_spectrum() -> None:
    result = affine_quadratic_three_row_model()
    assert result["spectra_equal"]
    assert result["each_row_injective"]
    assert result["row_count"] == 3
    assert result["common_spectrum"] == [
        Fraction(45, 4),
        Fraction(49, 4),
        Fraction(57, 4),
        Fraction(61, 4),
    ]
    interface = result["euclidean_interface"]
    assert interface["all_tangent_squares_positive"]
    assert interface["positive_radius_one"]
    assert interface["all_target_planes_nonperpendicular"]
    assert interface["all_targets_off_axis"]
    assert interface["distinct_height_rows"]
    assert interface["nonaligned_parallel_axes"]
    assert interface["producer_distances_exact"]
    assert interface["anchor_distances_exact"]
    assert interface["all_translated_sources_distinct"]
    assert interface["all_targets_distinct"]
    assert interface["selected_labels_match_tangent_count"]
    assert interface["anchor_circle_distinct_from_rows"]


def test_pair_overlap_can_use_one_source_value_per_row() -> None:
    result = affine_quadratic_three_row_model()
    assert result["fixed_source_overlap_size"] == 2
    assert result["target_row_size"] == 2


def test_hypercube_gives_arbitrarily_many_identical_rows() -> None:
    result = hypercube_identical_spectrum_model(6)
    assert result["row_count"] == 6
    assert result["target_row_size"] == 32
    assert result["spectrum_size"] == 64
    assert result["spectra_equal"]
    assert result["each_row_injective"]
    assert result["all_tangent_squares_positive"]
    assert result["tangent_universe_size"] <= result["tangent_universe_upper_bound"]
    interface = result["euclidean_interface"]
    assert interface["positive_radius_one"]
    assert interface["all_target_planes_nonperpendicular"]
    assert interface["nonaligned_parallel_axes"]
    assert interface["producer_distances_exact"]
    assert interface["anchor_distances_exact"]
    assert interface["all_translated_sources_distinct"]
    assert interface["all_targets_distinct"]
    assert interface["target_point_count"] == 6 * 32
    assert interface["target_plane_count"] == result["tangent_universe_size"]


def test_parabolic_lift_is_exact() -> None:
    result = parabolic_lift_certificate()
    assert result["pass"]
    assert result["parameter_points"] == 6
    assert result["complete_incidences"] == 12
    assert result["distance_values"] == 4
