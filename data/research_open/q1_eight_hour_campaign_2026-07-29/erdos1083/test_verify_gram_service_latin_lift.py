from fractions import Fraction

import verify_gram_service_latin_lift as verifier


def test_same_product_radial_gap_factorization() -> None:
    gap = verifier.same_product_radial_gap(2, 9, 3, 7)
    assert gap["factorization_holds"]
    assert gap["direct_gap"] == gap["factored_gap"]
    assert gap["direct_gap"] > 0


def test_service_pair_formula_recovers_required_partner_shift() -> None:
    fan = verifier.paired_service_fan(7)
    assert fan["service_count"] == 7
    assert fan["all_services_valid"]
    assert fan["distinct_cross_cells"] == 2
    assert fan["cross_cell_multiplicities"] == (7, 7)
    assert fan["height_capacity_per_class"] == 7
    assert fan["paired_type_multiplicity_bound_is_sharp"]


def test_opposite_cross_shifts_are_degenerate() -> None:
    assert (
        verifier.required_partner_shift(
            Fraction(3),
            Fraction(-3),
            10,
            12,
        )
        is None
    )


def test_unshifted_latin_graph_has_no_nontrivial_service_lift() -> None:
    audit = verifier.latin_service_lift_audit(7, 4)
    assert audit["edge_count"] == 4 * 7**2
    assert audit["distinct_nontrivial_block_pairs"] > 0
    assert audit["candidate_edge_pairs"] > 0
    assert audit["compatible_nontrivial_services"] == 0
    assert audit["unshifted_latin_cannot_lift"]
    assert audit["minimum_gap_exceeds_height_square_range"]


def test_eta_one_thirtieth_service_pair_ledger() -> None:
    ledger = verifier.exponent_ledger(1, 30)
    assert ledger["hub_class_exponent"] == Fraction(9, 10)
    assert ledger["service_mass_exponent"] == Fraction(33, 10)
    assert (
        ledger["distinct_cross_edge_exponent"]
        == Fraction(29, 10)
    )
    assert (
        ledger["average_service_occurrences_per_cross_edge_exponent"]
        == Fraction(2, 5)
    )
    assert (
        ledger["point_moment_from_exact_edge_saturation_exponent"]
        == Fraction(37, 10)
    )
    assert ledger["target_point_moment_exponent"] == Fraction(37, 10)
    assert (
        ledger["minimum_paired_signed_type_exponent"]
        == Fraction(23, 10)
    )
    assert (
        ledger["available_same_diagonal_block_pair_exponent"]
        == Fraction(14, 5)
    )
    assert (
        ledger["block_pair_capacity_slack_exponent"]
        == Fraction(1, 2)
    )
    assert (
        ledger["partner_projection_average_degree_exponent"]
        == Fraction(13, 10)
    )
    assert (
        ledger["hub_projection_average_degree_exponent"]
        == Fraction(7, 5)
    )
