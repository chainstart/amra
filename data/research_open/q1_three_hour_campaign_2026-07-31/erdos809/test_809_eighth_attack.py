#!/usr/bin/env python3
"""Regression tests for the eighth 2026-07-31 Erdős #809 attack."""

from __future__ import annotations

import unittest

import verify_809_eighth_attack as verifier


class EighthAttackGuards(unittest.TestCase):
    def test_full_contract_countermodel(self) -> None:
        result = verifier.full_contract_countermodel_guard()
        self.assertTrue(result["passed"])
        self.assertTrue(result["specific_absorption_fails"])
        self.assertTrue(result["actual_budget_closes"])
        self.assertGreater(result["Ropp_over_nE0opp"], 0.4)

    def test_L4_two(self) -> None:
        result = verifier.l4_two_guard(
            verifier.build_linear_residual_graph()
        )
        self.assertTrue(result["passed"])
        self.assertEqual(result["vertex_pairs"], 780)

    def test_asymptotic_formula(self) -> None:
        result = verifier.asymptotic_formula_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(result["limiting_residual_ratio"], 0.4)

    def test_degree_support(self) -> None:
        result = verifier.degree_support_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(
            result["residual_moment"],
            result["degree_deficit_form"],
        )
        self.assertLessEqual(
            result["residual_moment"],
            result["degree_support_bound"],
        )


if __name__ == "__main__":
    unittest.main()
