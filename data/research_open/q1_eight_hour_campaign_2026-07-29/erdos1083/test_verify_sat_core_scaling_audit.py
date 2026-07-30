from fractions import Fraction

import verify_sat_core_scaling_audit as verifier


def test_same_skeleton_replication_keeps_degree_one() -> None:
    certificate = verifier.same_skeleton_translation_replication(11)
    assert certificate["height_capacity"] == 33
    assert certificate["service_count"] == 66
    assert certificate["cross_edge_count"] == 132
    assert certificate["average_cross_edge_service_occurrence"] == 1
    assert certificate["distinct_visited_cross_cells"] == 6
    assert certificate["maximum_visited_cell_representation"] == 11
    assert not certificate["compatibility_degree_grows"]
    assert certificate["full_cell_upper_bound_on_fixed_skeleton"] > 0


def test_full_cross_copy_replication_is_quadratic_but_degree_one() -> None:
    certificate = verifier.full_cross_copy_translation_replication(11)
    assert certificate["height_capacity"] == 33
    assert certificate["service_count"] == 6 * 11**2
    assert certificate["cross_edge_count"] == 12 * 11**2
    assert certificate["average_cross_edge_service_occurrence"] == 1
    assert certificate["visited_cross_cell_upper_bound"] == 12 * 21
    assert certificate["maximum_visited_cell_representation"] == 11
    assert certificate["generic_translation_has_no_extra_compatibilities"]


def test_transcendental_step_forces_the_swapped_translation_pair() -> None:
    assert verifier.transcendental_translation_differences(20, 2, 3) == (
        (0, 0),
    )


def test_separated_full_cross_layering_has_cubic_services_and_cells() -> None:
    certificate = verifier.separated_layering(7, 11)
    assert certificate["radius_class_count"] == 35
    assert certificate["height_capacity"] == 33
    assert certificate["service_count"] == 6 * 7 * 11**2
    assert certificate["cross_edge_count"] == 12 * 7 * 11**2
    assert certificate["average_cross_edge_service_occurrence"] == 1
    assert certificate["separated_full_cell_lower_bound"] > 0


def test_eta_one_thirtieth_synchronized_cycle_thresholds() -> None:
    ledger = verifier.synchronized_cycle_capacity_ledger()
    assert ledger["target_compatibility_degree_exponent"] == Fraction(2, 5)
    assert (
        ledger["partner_palette_threshold_for_any_cycle"]
        == Fraction(13, 10)
    )
    assert (
        ledger["partner_palette_threshold_for_c4"]
        == Fraction(3, 10)
    )
    assert (
        ledger["partner_palette_threshold_for_c4_or_c6"]
        == Fraction(19, 30)
    )
    assert (
        ledger["hub_palette_threshold_for_any_cycle"]
        == Fraction(7, 5)
    )
    assert (
        ledger["hub_palette_threshold_for_c4"]
        == Fraction(9, 20)
    )
    assert (
        ledger["hub_palette_threshold_for_c4_or_c6"]
        == Fraction(23, 30)
    )
    assert ledger["full_cross_copy_service_exponent"] == 2
    assert ledger["layered_balanced_service_exponent"] == 3
    assert ledger["required_service_exponent"] == Fraction(33, 10)
    assert ledger["layered_separated_cell_exponent"] == 3
    assert ledger["allowed_cell_exponent"] == Fraction(27, 10)
    assert ledger["layered_cell_excess_exponent"] == Fraction(3, 10)
    assert ledger["layered_service_deficit_exponent"] == Fraction(3, 10)


def test_finite_coloured_c4_capacity_scales_by_palette() -> None:
    capacity = verifier.monochromatic_c4_capacity(49, 3)
    assert capacity["per_colour_c4_free_capacity"] == 49 * 7 + 49
    assert (
        capacity["total_c4_free_coloured_capacity"]
        == 3 * capacity["per_colour_c4_free_capacity"]
    )
