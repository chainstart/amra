#!/usr/bin/env python3
"""Regression tests for signed-residual factorial energy."""

import unittest

from verify_signed_residual_factorial_energy import run_all


class SignedResidualFactorialEnergyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = run_all()

    def test_prime_nonvanishing(self) -> None:
        self.assertTrue(self.result["prime_nonvanishing"]["pass"])

    def test_reciprocal_frame(self) -> None:
        self.assertTrue(self.result["common_x_reciprocal_frame"]["pass"])

    def test_two_multiplier_debt(self) -> None:
        self.assertTrue(self.result["two_multiplier_debt"]["pass"])

    def test_aperiodic_escape_debt(self) -> None:
        self.assertTrue(self.result["aperiodic_escape_debt"]["pass"])
        popular = self.result["aperiodic_escape_debt"]["popular_difference_certificate"]
        self.assertEqual(popular["mu"], 1)
        self.assertEqual(popular["lower_cost"], 1)

    def test_full_transverse_minimum_debt(self) -> None:
        self.assertTrue(self.result["full_transverse_minimum_debt"]["pass"])

    def test_stable_collision_ledger(self) -> None:
        ledger = self.result["stable_collision_ledger"]
        self.assertTrue(ledger["pass"])
        self.assertFalse(ledger["outer_geometric_extraction_proved"])

    def test_scope_firewall(self) -> None:
        self.assertFalse(self.result["original_problem_proved"])
        frame = self.result["common_x_reciprocal_frame"]
        self.assertTrue(frame["transversality_fails"])
        self.assertFalse(frame["power_large_family"])
        self.assertFalse(self.result["full_transverse_minimum_debt"]["power_large_family"])


if __name__ == "__main__":
    unittest.main()
