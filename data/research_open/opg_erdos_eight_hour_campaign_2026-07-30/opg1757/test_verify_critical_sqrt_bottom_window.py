#!/usr/bin/env python3
"""Tests for the critical square-root bottom Newton certificate."""

from __future__ import annotations

import math
from fractions import Fraction

from verify_critical_sqrt_bottom_window import (
    WINDOW_DENOMINATOR,
    WINDOW_K0,
    audit,
    determinant_relative_remainder_bound,
    main_term_ratio_exact,
    main_term_ratio_float,
    maximum_certified_depth,
    parameters,
    predicted_main_scaling,
    scaling_samples,
    window_certificate,
)


def test_parameter_parities():
    for k in range(10, 50):
        for depth in range(6):
            q0, n, excess = parameters(k, depth)
            assert q0 == (k-2)//2
            assert n == q0+4+depth
            assert excess == (1 if k % 2 else 2)+2*depth


def test_explicit_window_boundary_exactly_implies_heat_condition():
    for multiplier in (1, 2, 4, 10, 100, 1000):
        for parity in (0, 1):
            k = multiplier*WINDOW_K0+parity
            depth = maximum_certified_depth(k)
            result = window_certificate(k, depth)
            assert result["heat_condition"]
            assert result["positive"]
            assert depth == math.isqrt(k)//WINDOW_DENOMINATOR


def test_every_smaller_depth_is_certified():
    k = 100*WINDOW_K0
    maximum = maximum_certified_depth(k)
    for depth in range(maximum+1):
        assert window_certificate(k, depth)["positive"]


def test_exact_and_log_main_newton_sums_agree():
    for n in (20, 40, 80, 120):
        for excess in (1, 2, 3, 5, 8, 11):
            exact = main_term_ratio_exact(n, excess)
            floating = main_term_ratio_float(n, excess)
            assert abs(float(exact)-floating) < 1e-9


def test_main_term_scaling_samples_approach_prediction():
    grouped = {}
    for sample in scaling_samples():
        grouped.setdefault(sample["target_lambda"], []).append(sample)
    for samples in grouped.values():
        errors = [sample["absolute_error"] for sample in samples]
        assert errors[-1] < errors[0]
        assert errors[-1] < 0.003
        final = samples[-1]
        assert 0 < final["main_term_ratio"] < 1
        assert abs(
            final["predicted"]
            -predicted_main_scaling(final["N"], final["R"])
        ) < 1e-15


def test_existing_determinant_remainder_does_not_close_scaling():
    for lam in (Fraction(1, 4), Fraction(1), Fraction(4)):
        values = []
        for n in (10**4, 10**6, 10**8):
            excess = max(1, math.isqrt(lam.numerator*n//lam.denominator))
            values.append(float(
                determinant_relative_remainder_bound(n, excess)
            ))
        expected = float(2**48*lam)
        assert abs(values[-1]-expected)/expected < 0.001
        assert values[-1] > 1


def test_full_critical_window_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert result["explicit_c"] == "2^-28"
    assert result["explicit_k0"] == 9*2**58
    assert result["exact_main_sum_checks"] == 9
