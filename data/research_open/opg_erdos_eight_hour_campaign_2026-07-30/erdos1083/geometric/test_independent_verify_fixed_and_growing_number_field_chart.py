"""Tests for the independent fixed/growing number-field audit."""

from independent_verify_fixed_and_growing_number_field_chart import audit


def test_independent_fixed_and_growing_number_field_chart():
    result = audit()
    assert result["verdict"] == "PASS"
    assert result["imports_author_verifier"] is False
    assert result["rational_two_square_checks"] == 400
    assert result["ideal_envelope_checks"] == 25
    assert result["quadratic_conjugate_checks"] == 288
    assert result["zero_label_pairs"] == 81
    assert result["uniform_degree_condition"] == (
        "D=o(sqrt(log log t))"
    )
