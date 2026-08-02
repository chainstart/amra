"""Regression wrapper for the author-independent signed-switch audit."""

from verify_signed_switch_blind_audit_ii import (
    check_binary_box_endpoint,
    check_cyclotomic_algebra,
    check_finite_quotient_and_escape,
    check_phi6_automaton_and_fibres,
)


def test_blind_cyclotomic_and_finite_shadow_guards():
    cyclotomic = check_cyclotomic_algebra()
    finite = check_finite_quotient_and_escape()
    assert cyclotomic["sharp_identities"] == 48
    assert cyclotomic["rectangle_states"] == 39308
    assert finite["quotient_tiles"] == 15
    assert finite["torsion_orders_checked"] == 511


def test_blind_phi6_and_binary_box_guards():
    phi6 = check_phi6_automaton_and_fibres()
    binary = check_binary_box_endpoint()
    assert phi6["binary_words"] == 8190
    assert phi6["valid_rank_two_fibres"] > 0
    assert binary["separating_quotient_tiles"] == 12
    assert binary["endpoint_exponent"] < 5 / 9
    assert binary["gap"] > 0
