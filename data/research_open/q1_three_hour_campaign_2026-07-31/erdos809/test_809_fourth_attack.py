#!/usr/bin/env python3
"""Regression tests for the fourth 2026-07-31 Erdős #809 attack."""

from __future__ import annotations

import unittest

import verify_809_fourth_attack as verifier


class FourthAttackGuards(unittest.TestCase):
    def test_sharp_one_congestion(self) -> None:
        result = verifier.sharp_one_congestion_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(result["congestion"], 1)

    def test_two_role_collision(self) -> None:
        result = verifier.two_role_collision_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(result["cycle_length"], 7)
        self.assertEqual(result["gamma_edges_on_cycle"], 2)
        self.assertFalse(result["rainbow"])

    def test_empty_shore_unbounded(self) -> None:
        result = verifier.empty_shore_unbounded_guard(congestion=50)
        self.assertTrue(result["passed"])
        self.assertEqual(result["congestion"], 50)

    def test_aggregate_double_count(self) -> None:
        result = verifier.aggregate_double_count_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(
            result["pair_incidence_sum"],
            10,
        )

    def test_zero_shore_energy(self) -> None:
        result = verifier.zero_shore_energy_guard()
        self.assertTrue(result["passed"])
        self.assertGreaterEqual(
            result["forced_missing_pairs"],
            result["claimed_lower_bound"],
        )


if __name__ == "__main__":
    unittest.main()
