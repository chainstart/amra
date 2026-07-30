from fractions import Fraction

import verify_hub_concentration_dichotomy as verifier


def test_finite_low_link_edges_are_hub_covered() -> None:
    certificate = verifier.finite_cover_certificate(20)
    assert certificate["declared_hubs"] == certificate["detected_hubs"]
    assert certificate["low_edge_count"] > 0
    assert certificate["all_low_edges_covered"]
    assert (
        certificate["maximum_hub_pair_weight"]
        < certificate["minimum_outside_pair_weight"]
    )


def test_link_and_hub_exponent_identities() -> None:
    eta = Fraction(1, 30)
    ledger = verifier.exponent_ledger(1, 30)
    assert (
        ledger["link_from_two_small_blocks"]
        == ledger["target_link"]
    )
    assert ledger["low_overlap_capacity"] == ledger["overlap_mass"]
    assert ledger["line_alternative"] == (
        Fraction(5, 2) - 3 * eta / 2
    )


def test_residual_gap_is_exact() -> None:
    eta = Fraction(1, 30)
    ledger = verifier.exponent_ledger(1, 30)
    assert ledger["residual_gap"] == (
        Fraction(1, 6) + 5 * eta / 2
    )
    assert ledger["required_hub_for_target"] == (
        Fraction(5, 6) + 2 * eta
    )
    assert ledger["required_hub_for_target"] == ledger["hub_upper"]


def test_zero_eta_partial_line_bound_is_five_halves() -> None:
    ledger = verifier.exponent_ledger(0, 1)
    assert ledger["line_alternative"] == Fraction(5, 2)
    assert ledger["line_target"] == Fraction(8, 3)
    assert ledger["residual_gap"] == Fraction(1, 6)
