from fractions import Fraction

import verify_strong_pair_bsg_audit as verifier


def test_hyperbola_factorization_and_shift() -> None:
    for delta in (1, 17, 16065):
        for parameter in range(2, 20):
            x_value, y_value = verifier.hyperbola_pair(parameter, delta)
            assert x_value * x_value - y_value * y_value == delta


def test_rational_example_has_exact_multiplicity_one() -> None:
    certificate = verifier.rational_multiplicity_one_example(15, 6, 16065)
    assert certificate["shifted_values_match"]
    assert certificate["actual_shifted_blocks_match"]
    assert (
        certificate["larger_radial_offset"]
        - certificate["smaller_radial_offset"]
        == certificate["offset_difference"]
    )
    assert set(certificate["first_selected_counts"]) == {1}
    assert set(certificate["second_selected_counts"]) == {1}


def test_zero_shift_interval_saturates_rm_squared_order() -> None:
    for height_count in (50, 100):
        overlap_size = 10
        energy = verifier.zero_shift_interval_energy(
            height_count, overlap_size
        )
        assert energy <= 4 * overlap_size * height_count**2
        assert energy >= overlap_size * height_count**2


def test_exponent_ledger() -> None:
    ledger = verifier.exponent_ledger(1, 30)
    eta = Fraction(1, 30)
    assert ledger["overlap_exponent"] == Fraction(5, 6) - eta
    assert ledger["minimum_bsg_parameter_exponent"] == (
        Fraction(1, 6) + eta
    )
    assert ledger["automatic_bsg_parameter_exponent"] == (
        Fraction(13, 6) + eta
    )
    assert ledger["global_propagation_gap_exponent"] == (
        Fraction(2, 3) + eta
    )
