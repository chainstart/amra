import sympy as sp

import verify_translated_latin_service_complex as verifier


def test_four_and_six_cycle_equal_shift_radial_identity() -> None:
    four_cycle = verifier.equal_shift_cycle_radial_identity(
        (sp.Integer(3), 5, 8, 6),
        sp.Integer(2),
        sp.Integer(3),
    )
    six_cycle = verifier.equal_shift_cycle_radial_identity(
        (sp.Integer(3), 5, 8, 6, 4, 4),
        sp.Integer(2),
        sp.Integer(3),
    )
    assert four_cycle["scaled_identity_holds"]
    assert six_cycle["scaled_identity_holds"]
    assert four_cycle["partner_cycle_sum"] == 0
    assert four_cycle["radial_cycle_sum"] == 0
    assert six_cycle["partner_cycle_sum"] == 0
    assert six_cycle["radial_cycle_sum"] == 0


def test_q3_u2_translated_latin_core_is_exactly_satisfiable() -> None:
    certificate = verifier.translated_latin_sat_core()
    assert certificate["permutation_pair_search_space"] == 36
    assert certificate["hub_translation_polynomial_holds"]
    assert certificate["translation_gap_polynomial_holds"]
    assert certificate["service_count"] == 6
    assert certificate["all_original_gram_equalities_hold"]
    assert certificate["all_local_four_cycle_sums_zero"]
    assert certificate["used_cross_edge_count"] == 12
    assert certificate["pairable_core_cross_edge_count"] == 12
    assert certificate["all_pairable_core_edges_used_once"]
    assert certificate["unpairable_boundary_block_count"] == 2
    assert (
        certificate["distinct_cross_cell_count"]
        <= certificate["cross_cell_block_bound"]
    )


def test_sat_core_closes_the_first_dual_cochain_cycles() -> None:
    certificate = verifier.translated_latin_sat_core()
    assert certificate["partner_projection_cycle_rank"] == 0
    assert certificate["hub_projection_cycle_rank"] == 3
    assert certificate["parallel_hub_two_cycle_count"] == 3
    assert certificate["all_parallel_hub_two_cycles_close"]


def test_round25_ledger_has_no_asymptotic_surplus() -> None:
    ledger = verifier.exponent_ledger()
    assert ledger["service_mass_exponent"] == sp.Rational(33, 10)
    assert ledger["cross_edge_exponent"] == sp.Rational(29, 10)
    assert (
        ledger["required_compatibility_degree_exponent"]
        == sp.Rational(2, 5)
    )
    assert ledger["finite_sat_core_power_surplus"] == 0
