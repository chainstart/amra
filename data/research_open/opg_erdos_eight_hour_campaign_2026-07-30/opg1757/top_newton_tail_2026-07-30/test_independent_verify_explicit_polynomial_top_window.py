#!/usr/bin/env python3
"""Tests for the independent explicit polynomial-window audit."""

from independent_verify_explicit_polynomial_top_window import audit


def test_independent_explicit_polynomial_window():
    result = audit(maximum_loss=9, maximum_depth=5)
    assert result["status"] == "PASS"
    assert result["imports_existing_opg_verifier"] is False
    assert result["faulhaber_checks"] == 8
    assert result["newton_partition_checks"] == 30
    assert result["moment_conversion_checks"] == 30
    assert result["exceptional_norm_checks"] == 8
    assert result["fixed_offset_absorption_checks"] == 256
    assert result["effective_threshold"] == "2^2584"
    assert result["threshold_theta"] == "1/4"
    assert result["proved_eta"] == "1/8"
