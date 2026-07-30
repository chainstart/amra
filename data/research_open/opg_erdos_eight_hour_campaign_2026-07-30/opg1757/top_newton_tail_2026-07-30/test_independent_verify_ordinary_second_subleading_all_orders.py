#!/usr/bin/env python3
"""Tests for the independent ordinary second-subleading red-team audit."""

from independent_verify_ordinary_second_subleading_all_orders import audit


def test_independent_second_subleading_audit():
    result = audit(maximum_loss=14, maximum_depth=8)
    assert result["status"] == "PASS"
    assert result["imports_existing_opg_verifier"] is False
    assert result["rank_four_exact_profile_checks"] == 33
    assert result["exceptional_rank_four_nonzero"] is True
    assert result["g4_built_by_generic_convolution"] is True
    assert result["g1_exactly_antisymmetric"] is True
    assert result["sixth_moment_first_total_order"] == 5
    assert result["boundary_cancellations"] == ["d=0", "d=1"]
    assert result["maximum_exact_ordinary_depth"] == 8
