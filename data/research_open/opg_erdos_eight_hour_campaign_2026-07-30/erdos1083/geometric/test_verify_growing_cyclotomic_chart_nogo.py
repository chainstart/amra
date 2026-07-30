"""Tests for the growing cyclotomic chart extraction no-go."""

from verify_growing_cyclotomic_chart_nogo import (
    audit,
    chord_squared_minimal_degree,
    circular_unit_log_determinant,
    enumerate_prism_distances,
    low_rank_capture_bound,
    palette_exponent_ledger,
    prism_ledger,
)


def test_exact_critical_local_ledger():
    result = prism_ledger(11, 121)
    assert result["points"] == 11**3
    assert result["Omega"] == 11**3 * 10
    assert result["chord_types"] == 5
    assert result["separated_cross_labels"] == 5 * 119
    assert result["distance_upper"] == 5 * 121 + 120
    assert result["chord_squared_field_degree"] == 5


def test_distance_layers_are_separated_from_vertical_two_onward():
    for prime in (5, 7, 11, 13):
        result = enumerate_prism_distances(prime, 9)
        expected = ((prime - 1) // 2) * 7
        assert result["separated_labels"] == expected


def test_every_chord_squared_generates_the_real_cyclotomic_field():
    for prime in (5, 7, 11):
        for distance in range(1, (prime - 1) // 2 + 1):
            result = chord_squared_minimal_degree(prime, distance)
            assert result["degree"] == (prime - 1) // 2


def test_circular_unit_rank_and_low_rank_capture():
    for prime in (5, 7, 11, 13):
        result = circular_unit_log_determinant(prime)
        assert result["rank"] == (prime - 3) // 2
    capture = low_rank_capture_bound(101, 3)
    assert capture["captured_chord_types"] == 4
    assert capture["captured_overlap_fraction"] == "2/25"


def test_full_cyclotomic_nogo_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert result["minimal_polynomial_checks"] == 10
    assert len(result["critical_local_ledgers"]) == 4


def test_conditional_field_palette_exponent():
    result = palette_exponent_ledger(5, 1, 0.3, 0.2)
    assert abs(float(result["distance_exponent"]) - 3.5) < 1e-12
