"""Tests for the independent critical square-root window audit."""

from fractions import Fraction

from independent_verify_critical_sqrt_bottom_window import (
    WINDOW_THRESHOLD,
    actual_newton_scope,
    audit,
    certified_depth,
    dominated_convergence_audit,
    endpoint_parameters,
    equation_35_bound,
    exact_main_ratio,
    small_n_scope_counterexample,
    window_boundary_audit,
)


def test_not_a_literal_corollary_four_substitution():
    boundary = window_boundary_audit(WINDOW_THRESHOLD)
    assert boundary["depth"] == 6
    assert boundary["equation_39_condition_2^52"]
    assert not boundary["corollary_4_condition_2^54"]
    assert boundary["positive"]


def test_all_earlier_terms_stay_in_heat_range():
    for multiplier in (1, 4, 25, 100):
        k = multiplier * WINDOW_THRESHOLD + (multiplier % 2)
        boundary = window_boundary_audit(k)
        assert boundary["earlier_terms_checked"] == certified_depth(k) + 1
        assert boundary["positive"]


def test_equation_35_actual_support_and_small_n_scope():
    for k in range(2, 50):
        for depth in range(7):
            _, vertex_count, excess = endpoint_parameters(k, depth)
            for ell in range(depth + 1):
                earlier_n, earlier_r, exponent = actual_newton_scope(
                    k, depth, ell
                )
                assert earlier_n >= 4
                assert earlier_r >= 1
                assert exponent >= 0
                assert (
                    exact_main_ratio(vertex_count, excess, ell)
                    <= equation_35_bound(vertex_count, excess, ell)
                )
    counterexample = small_n_scope_counterexample()
    assert counterexample["earlier_power_exponent"] < 0
    assert counterexample["inequality_fails_outside_scope"]


def test_main_model_has_a_valid_factorial_envelope():
    samples = dominated_convergence_audit()
    assert [entry["target_lambda"] for entry in samples] == [
        "0", "1/4", "1", "4"
    ]
    for entry in samples:
        sequence = entry["sequence"]
        assert sequence[-1]["absolute_error"] < sequence[0]["absolute_error"]
        assert sequence[-1]["absolute_error"] < 0.003


def test_full_independent_audit():
    result = audit()
    assert result["verdict"] == "PASS_WITH_SCOPE_CLARIFICATION"
    assert result["status"] == "all_independent_checks_passed"
    assert (
        result["exact_equation_35_checks_on_actual_support"]
        == 3555
    )
    assert "not a literal consequence" in (
        result["classification"]["fixed_window"]
    )
