"""Tests for the all-depth initial ordinary Newton chain."""

from independent_verify_ordinary_initial_newton_chain import audit


def test_initial_ordinary_newton_chain():
    result = audit()
    assert result["status"] == "PROVED"
    assert result["finite_root_evidence_used"] is False
    assert result["unconditional_weighted_C3_ranks"] == [0, 1, 2, 3]
    assert result["finite_redundancy_depths"] == 998
    assert result["minimal_remaining_target"] == (
        "normalized signed symbol log-concavity for every rank"
    )
