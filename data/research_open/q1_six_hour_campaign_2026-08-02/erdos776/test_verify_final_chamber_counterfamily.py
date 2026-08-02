#!/usr/bin/env python3
"""Focused tests for the final-chamber counterfamily."""

from verify_final_chamber_counterfamily import (
    check_complete_dyadic_base,
    check_dyadic_legality,
    check_stable_rank_six,
    check_surplus_identities,
    check_two_canonical_levels,
)


def test_dyadic_legality() -> None:
    check_dyadic_legality()


def test_two_canonical_levels() -> None:
    check_two_canonical_levels()


def test_surplus_identities() -> None:
    check_surplus_identities()


def test_stable_rank_six() -> None:
    check_stable_rank_six()


def test_complete_dyadic_base() -> None:
    check_complete_dyadic_base()
