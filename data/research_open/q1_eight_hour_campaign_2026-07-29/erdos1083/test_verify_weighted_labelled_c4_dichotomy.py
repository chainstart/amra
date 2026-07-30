from fractions import Fraction

import verify_weighted_labelled_c4_dichotomy as verifier


def test_complete_ap_saturates_common_difference_energy() -> None:
    length = 7
    statistics = verifier.complete_ap_model(length)
    assert statistics["cycle_count"] == length**4
    assert statistics["fibre_collision_injection_holds"]
    assert statistics["additive_energy_bound_holds"]
    assert (
        statistics["excess_fibre_moment"]
        == statistics["common_nonzero_difference_energy"]
    )
    assert (
        statistics["maximum_additive_energy"]
        == (2 * length**3 + length) // 3
    )


def test_translation_fan_refutes_additive_energy_from_one_fibre() -> None:
    length = 7
    statistics = verifier.translation_fan_model(length)
    assert statistics["cycle_count"] == length
    assert statistics["occupied_signed_fibres"] == 1
    assert statistics["maximum_signed_fibre"] == length
    assert statistics["fibre_second_moment"] == length**2
    assert (
        statistics["base_additive_energy"]
        == statistics["minimum_energy_formula"]
        == 2 * length**2 - length
    )
    assert statistics["marginal_cocycle_energy"] == length**4
    assert (
        statistics["marginal_cocycle_energy"]
        > statistics["cycle_count"]
    )


def test_weighted_inequality_survives_irregular_sparse_edges() -> None:
    sets = (
        (0, 1, 3, 7),
        (-2, 0, 4, 7),
        (1, 2, 6, 9),
        (-3, 2, 5, 8),
    )
    complete_blocks = tuple(
        {
            (first, second)
            for first in sets[first_index]
            for second in sets[second_index]
            if (3 * first + 5 * second) % 4 != 1
        }
        for first_index, second_index in (
            (0, 1),
            (2, 1),
            (2, 3),
            (0, 3),
        )
    )
    statistics = verifier.weighted_cycle_statistics(
        sets,
        complete_blocks,
    )
    assert statistics["cycle_count"] > 0
    assert statistics["fibre_collision_injection_holds"]
    assert statistics["additive_energy_bound_holds"]
    assert (
        statistics["fibre_second_moment"]
        >= statistics["cauchy_fibre_lower_bound"]
    )


def test_latin_transversal_graph_exactly_saturates_kst_scale() -> None:
    field_order = 7
    hub_groups = 4
    model = verifier.latin_transversal_model(
        field_order,
        hub_groups,
    )
    assert model["is_c4_free"]
    assert model["c4_count"] == 0
    assert model["edge_count"] == model["kst_scale"]
    assert model["partner_degree"] == hub_groups
    assert model["degree_variance"] == 0
    assert (
        model["uncovered_hub_pairs"]
        == model["expected_uncovered_within_groups"]
    )
    assert (
        model["stability_identity_lhs"]
        == model["stability_identity_rhs"]
    )
    assert (
        model["distinct_real_cells"]
        <= model["real_cell_upper_bound"]
    )
    assert model["maximum_cell_representation"] <= field_order


def test_eta_one_thirtieth_weighted_ledger() -> None:
    ledger = verifier.exponent_ledger(1, 30)
    assert ledger["hub_group_exponent"] == Fraction(9, 10)
    assert ledger["hub_vertex_exponent"] == Fraction(19, 10)
    assert ledger["partner_vertex_exponent"] == 2
    assert ledger["forced_edge_exponent"] == Fraction(29, 10)
    assert ledger["kst_edge_threshold_exponent"] == Fraction(29, 10)
    assert ledger["edge_surplus_exponent"] == 0
    assert (
        ledger["hypothetical_constant_surplus_c4_exponent"]
        == Fraction(19, 5)
    )
    assert (
        ledger["endpoint_reuse_target_exponent"]
        == Fraction(1, 5)
    )
    assert (
        ledger["palette_needed_for_endpoint_reuse_exponent"]
        == Fraction(18, 5)
    )
    assert (
        ledger["palette_needed_for_maximal_additive_energy_exponent"]
        == Fraction(13, 5)
    )
    assert (
        ledger["signed_triple_palette_bound_from_M"]
        == Fraction(81, 10)
    )
    assert ledger["radius_quartet_count_exponent"] == Fraction(19, 5)
    assert (
        ledger["global_palette_gap_for_endpoint_reuse_exponent"]
        == Fraction(9, 2)
    )
    assert (
        ledger["block_palette_gap_for_endpoint_reuse_exponent"]
        == Fraction(12, 5)
    )
