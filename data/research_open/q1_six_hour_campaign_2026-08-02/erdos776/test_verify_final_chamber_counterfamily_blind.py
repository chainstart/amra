"""Focused regressions for the independent final-chamber blind audit."""

from verify_final_chamber_counterfamily_blind import (
    check_deficit_and_tail_arithmetic,
    check_family,
    check_small_double_negative_base,
)


def test_blind_family_reconstruction() -> None:
    check_family()


def test_blind_deficit_and_tail_arithmetic() -> None:
    check_deficit_and_tail_arithmetic()


def test_blind_small_double_negative_base() -> None:
    check_small_double_negative_base()
