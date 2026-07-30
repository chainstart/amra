from fractions import Fraction

import verify_labelled_c4_algebra as verifier


def test_signed_root_completion_has_at_most_four_values() -> None:
    values = verifier.possible_fourth_values(1, 4, 9)
    assert values == (0, 4, 16, 36)
    assert len(values) <= 4
    assert all(
        verifier.elimination_polynomial(1, 4, 9, fourth) == 0
        for fourth in values
    )


def test_actual_rectangle_closes_and_kills_polynomial() -> None:
    certificate = verifier.rectangle_certificate(0, 5, 2, 9)
    assert certificate["signed_differences"] == (-2, 3, -4, -9)
    assert certificate["adjusted_values"] == (4, 9, 16, 81)
    assert certificate["cocycle_closes"]
    assert certificate["polynomial_vanishes"]
    assert certificate["fourth_is_in_signed_root_list"]
    assert verifier.elimination_polynomial(1, 2, 3, 4) == 64


def test_adjacent_equal_label_midpoint_degeneracy() -> None:
    degeneracy = verifier.degeneracy_certificate(0, 4, 2, 7)
    assert degeneracy["adjacent_first_pair_equal"]
    assert degeneracy["first_partner_is_vertical_midpoint"]
    assert not degeneracy["vertical_parallelogram"]


def test_opposite_equal_label_vertical_parallelogram() -> None:
    degeneracy = verifier.degeneracy_certificate(1, 4, 2, 5)
    assert degeneracy["opposite_pair_ac_equal"]
    assert degeneracy["vertical_parallelogram"]


def test_arithmetic_progression_barrier_preserves_multiplicity() -> None:
    length = 7
    certificate = verifier.arithmetic_progression_barrier(length)
    assert certificate["edge_label_count"] == length
    assert certificate["point_rectangle_count"] == length**4
    assert (
        certificate["distinct_label_quadruple_count"]
        <= certificate["label_quadruple_upper_bound"]
    )
    assert certificate["maximum_fourth_choices"] <= 4
    assert certificate["polynomial_failure_count"] == 0
    assert certificate["additive_energy_formula_holds"]
    assert (
        certificate["vertical_parallelogram_count"]
        == (2 * length**3 + length) // 3
    )


def test_eta_one_thirtieth_exact_capacity_ledger() -> None:
    ledger = verifier.exponent_ledger(1, 30)
    assert ledger["cell_universe_exponent"] == Fraction(27, 10)
    assert ledger["maximum_hub_exponent"] == Fraction(9, 10)
    assert ledger["hub_coordinate_vertex_exponent"] == Fraction(19, 10)
    assert ledger["failed_moment_edge_exponent"] == Fraction(29, 10)
    assert ledger["kst_edge_threshold_exponent"] == Fraction(29, 10)
    assert ledger["edge_surplus_over_kst_exponent"] == 0
    assert (
        ledger["algebraic_label_quadruple_exponent"]
        == Fraction(81, 10)
    )
    assert (
        ledger["point_rectangle_capacity_exponent"]
        == Fraction(78, 10)
    )
    assert (
        ledger["algebraic_excess_over_point_capacity_exponent"]
        == Fraction(3, 10)
    )
    assert ledger["fourth_label_degree_bound"] == 4
