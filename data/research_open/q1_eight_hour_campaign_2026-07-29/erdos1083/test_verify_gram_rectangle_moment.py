from fractions import Fraction

import verify_gram_rectangle_moment as verifier


def test_exact_rectangle_exponent_ledger() -> None:
    ledger = verifier.exponent_ledger(1, 30)
    assert ledger["service_exponent"] == Fraction(33, 10)
    assert ledger["union_exponent"] == Fraction(27, 10)
    assert ledger["cell_moment_exponent"] == Fraction(39, 10)
    assert (
        ledger["target_point_moment_exponent"]
        == Fraction(37, 10)
    )
    assert ledger["cell_surplus_exponent"] == Fraction(1, 5)
    assert (
        ledger["cell_average_gain_exponent"] == Fraction(3, 5)
    )
    assert (
        ledger["required_average_gain_exponent"]
        == Fraction(2, 5)
    )
    assert (
        ledger["maximum_point_representation_exponent"]
        == Fraction(1, 5)
    )


def test_translation_fan_has_quadratic_cell_but_linear_point_energy() -> None:
    certificate = verifier.translation_fan(17)
    assert certificate["diagonal_product_sums_match"]
    assert certificate["all_diagonal_distances_match"]
    assert certificate["all_first_cross_values_match"]
    assert certificate["all_second_cross_values_match"]
    assert certificate["all_gram_identities"]
    assert certificate["cross_cell_count"] == 2
    assert certificate["cross_occurrence_count"] == 34
    assert (
        certificate["cell_moment"]
        == certificate["expected_cell_moment"]
    )
    assert (
        certificate["point_moment"]
        == certificate["expected_point_moment"]
    )
    assert certificate["cell_moment"] == 17 * certificate["point_moment"]


def test_finite_cauchy_and_point_refinement_bounds() -> None:
    certificate = verifier.cauchy_moment(
        (7, 5, 4),
        ((3, 2, 2), (2, 2, 1), (1, 1, 1, 1)),
    )
    assert certificate["occurrence_count"] == 16
    assert certificate["cell_count"] == 3
    assert certificate["maximum_point_pairs_per_cell"] == 4
    assert certificate["cell_cauchy_holds"]
    assert certificate["point_refinement_holds"]


def test_rational_hyperbola_parameters_match_radial_offsets() -> None:
    certificate = verifier.translation_fan(3)
    first = certificate["first_vertical_difference"]
    second = certificate["second_vertical_difference"]
    delta = (
        verifier.radial_offset(1, 5)
        - verifier.radial_offset(0, 6)
    )
    assert first**2 - second**2 == delta


def test_gram_identity_on_independent_rational_points() -> None:
    assert verifier.gram_identity(
        (Fraction(1), Fraction(3)),
        (Fraction(5), Fraction(8)),
        (Fraction(7), Fraction(-2)),
        (Fraction(11), Fraction(4)),
    )
