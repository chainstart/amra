#!/usr/bin/env python3
"""Tests for the all-orders second subleading certificate."""

from __future__ import annotations

import sympy as sp

from verify_ordinary_second_subleading_all_orders import (
    audit,
    second_subleading_polynomial,
)


def test_all_orders_second_subleading_certificate():
    result = audit()
    assert result["status"] == (
        "all_orders_symbolic_certificate_passed"
    )
    assert result["finite_loss_interpolation"] is False
    assert result["maximum_inverse_s_rank"] == 4
    assert result["fourth_profile_symbol_identities"] == 3
    assert result["central_binomial_h4_identity"] is True
    assert result["all_depth_generating_function_identity"] is True


def test_second_subleading_polynomial_known_values():
    expected = {
        2: 42,
        3: sp.Rational(557, 2),
        4: sp.Rational(2527, 2),
        8: sp.Rational(3253987, 72),
        12: sp.Rational(4571549, 12),
        22: sp.Rational(247951763, 24),
    }
    for depth, value in expected.items():
        assert second_subleading_polynomial(depth) == value
