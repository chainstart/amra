"""Independent tests for the all-rank saddle pole argument."""

import sympy as sp

from independent_verify_all_rank_saddle_pole_valuation import (
    W,
    antisymmetric_convolution_audit,
    audit,
    coefficient_extraction_audit,
    derivative_pole_propagation_audit,
    enumerate_defect_configurations,
    gamma_one_critical_value,
    independent_main_integral_jets,
    low_rank_second_differences,
    main_and_exceptional_cancellation,
    r,
)


def test_exact_eleven_defect_configurations_and_small_rank_boundary():
    configs = enumerate_defect_configurations()
    assert len(configs) == 11
    assert all(config[3] == 0 for config in configs)
    records, _ = independent_main_integral_jets()
    infeasible_r2 = [
        record
        for record in records
        if sp.sympify(record["n1"]).subs(r, 2) < 0
    ]
    assert len(infeasible_r2) == 1
    assert infeasible_r2[0]["amplitude_order"] == 2
    assert infeasible_r2[0]["n3"] == 1
    assert infeasible_r2[0]["specialization_r2_zero_if_infeasible"]


def test_only_gamma_one_and_critical_value():
    symbol_a = sp.Symbol("a")
    assert sp.simplify(
        gamma_one_critical_value()
        - (
            sp.Rational(1, 12)
            + symbol_a / 2
            - symbol_a**2 / 2
        )
    ) == 0
    # Gamma index j loses 3j pole orders. Top defect <=3 permits j<=1.
    assert [index for index in range(6) if 3 * index <= 3] == [0, 1]


def test_main_and_exceptional_layers_cancel():
    _, second, exceptional, total = main_and_exceptional_cancellation()
    assert second[:2] == [0, 0]
    assert sp.cancel(second[2] + exceptional[2]) == 0
    assert sp.cancel(second[3] + exceptional[3]) == 0
    assert total == [0, 0, 0, 0]


def test_low_rank_epsilon_boundary():
    assert low_rank_second_differences() == (0, 0)


def test_full_convolution_antisymmetry_and_even_derivatives():
    assert antisymmetric_convolution_audit() == list(range(6))


def test_derivative_pole_and_final_coefficient_propagation():
    assert len(derivative_pole_propagation_audit()) == 25
    assert coefficient_extraction_audit() == list(range(6))


def test_full_independent_audit_records_localization_obligation():
    result = audit()
    assert result["verdict"] == "PASS_WITH_LOCALIZATION_PROOF_OBLIGATION"
    assert result["total_top_layers"] == ["0", "0", "0", "0"]
    assert result["low_rank_second_differences"] == ["0", "0"]
    assert not result["author_verifier_imported"]
