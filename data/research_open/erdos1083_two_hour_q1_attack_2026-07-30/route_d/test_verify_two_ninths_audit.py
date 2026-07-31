from fractions import Fraction

from verify_two_ninths_audit import (
    cross_energy_certificate,
    endpoint_certificate,
    exponent_certificate,
    independent_geometry_check,
    threshold_from_fixed_a_saving,
    threshold_from_ledger_saving,
)


def test_independent_geometry() -> None:
    cert = independent_geometry_check()
    assert cert["maximum_fibre"] <= 2
    assert cert["circles"] == cert["lines"]
    assert cert["incidences"] > 0


def test_q_branch_is_strongly_excluded() -> None:
    cert = exponent_certificate(Fraction(2, 9))
    assert cert["q_branch_gap"] == Fraction(13, 16)


def test_main_branch_crossing() -> None:
    before = exponent_certificate(Fraction(2, 9) - Fraction(1, 1000))
    endpoint = exponent_certificate(Fraction(2, 9))
    after = exponent_certificate(Fraction(2, 9) + Fraction(1, 1000))
    assert before["main_branch_gap"] > 0
    assert endpoint["main_branch_gap"] == 0
    assert after["main_branch_gap"] < 0


def test_endpoint_ledger() -> None:
    cert = endpoint_certificate()
    assert cert["kappa"] == Fraction(2, 9)
    assert cert["rich_line_term_gap_at_m_one"] == Fraction(5, 9)


def test_saving_to_threshold_conversion() -> None:
    delta = Fraction(1, 100)
    assert threshold_from_fixed_a_saving(delta) == Fraction(2, 9) + delta / 6
    assert threshold_from_ledger_saving(delta) == Fraction(2, 9) + delta / 18


def test_cross_energy_saving_floor() -> None:
    cert = cross_energy_certificate()
    assert cert["one_fibre_saving_needed"] == Fraction(1, 18)
    assert cert["all_a_saving_needed"] == Fraction(1, 18)
