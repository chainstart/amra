from fractions import Fraction

import verify_real_multi_hub_reuse as verifier


def test_one_real_coordinate_serves_all_hub_pairs() -> None:
    certificate = verifier.multi_hub_star(8, 12, 30)
    assert certificate["service_count"] == 28
    assert (
        certificate["service_count"]
        == certificate["expected_service_count"]
    )
    assert certificate["receiving_radius_count"] == 7
    assert certificate["maximum_receiving_height_count"] <= 8
    assert certificate["total_partner_height_count"] == 28
    assert certificate["all_product_sums_match"]
    assert certificate["all_shifted_values_match"]


def test_star_scales_quadratically_in_hub_count() -> None:
    for hub_count in (3, 5, 9):
        certificate = verifier.multi_hub_star(
            hub_count, hub_count + 2, 3 * hub_count + 2
        )
        assert certificate["service_count"] == (
            hub_count * (hub_count - 1) // 2
        )
        assert (
            certificate["maximum_receiving_height_count"] <= hub_count
        )


def test_subtraction_identity_for_two_services() -> None:
    shared = Fraction(11)
    first = (Fraction(0), Fraction(0), Fraction(7))
    second = (Fraction(3), Fraction(2), Fraction(5))
    first_delta = (first[0] - shared) ** 2 - (
        first[1] - first[2]
    ) ** 2
    second_delta = (second[0] - shared) ** 2 - (
        second[1] - second[2]
    ) ** 2
    assert verifier.subtraction_identity(
        first, second, shared, first_delta, second_delta
    )


def test_required_pointwise_bound_is_refuted() -> None:
    ledger = verifier.exponent_ledger(1, 30)
    assert ledger["required_c"] > 0
    assert (
        ledger["pointwise_service_exponent_in_u"]
        > ledger["required_pointwise_exponent"]
    )
    assert ledger["best_unconditional_c"] == 0
