from fractions import Fraction

from verify_resonant_ansatz_no_go import (
    ansatz_no_go_ledger,
    best_integer_side_length,
    densest_dyadic_divisor_bin,
    primorial_multistar_certificate,
)


def test_dyadic_bin_has_the_pigeonhole_divisor_count():
    result = densest_dyadic_divisor_bin(30030)
    assert result["tau"] == 64
    assert result["count"] == 8
    assert result["count"] >= result["pigeonhole_lower_bound"]
    assert all(
        result["lower_endpoint"] <= divisor < result["upper_endpoint"]
        for divisor in result["selected"]
    )


def test_rank_three_divisor_multistar_has_constant_overlap_per_divisor():
    for prime_count in range(3, 9):
        result = primorial_multistar_certificate(prime_count)
        assert result["tau"] == result["squarefree_tau"]
        assert result["n"] <= result["linear_size_bound"]
        assert (
            result["certified_average_degree"]
            >= result["uniform_average_lower_bound"]
        )
        assert result["certified_H"] > result["n"] ** 2
        assert all(
            witness["product"] == result["number"]
            for witness in result["witnesses"]
        )


def test_variable_side_length_cannot_beat_logarithmic_growth():
    result = best_integer_side_length(100)
    assert result["side_length"] == 4
    assert result["choices"][4] > result["choices"][2]
    assert result["choices"][4] > result["choices"][10]


def test_no_go_ledger_keeps_a_strict_power_gap():
    ledger = ansatz_no_go_ledger()
    assert ledger["target_average_exponent"] == Fraction(2, 5)
    assert ledger["ansatz_power_exponent"] == 0
    assert ledger["target_over_ansatz"] == "n^(2/5-o(1))"
