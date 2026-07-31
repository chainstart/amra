#!/usr/bin/env python3
"""Regression tests for the sixth 2026-07-31 Erdos #809 attack."""

from __future__ import annotations

import unittest

import verify_809_sixth_attack as verifier


class SixthAttackGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = verifier.build_three_hub_graph()

    def test_overlap_high_low(self) -> None:
        result = verifier.overlap_high_low_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(
            result["rectangle_area_sum"],
            result["weight_square_sum"],
        )

    def test_full_contract_obstruction(self) -> None:
        result = verifier.contract_obstruction_guard()
        self.assertTrue(result["passed"])
        self.assertGreater(result["zero_shore_excess_E0"], 0)
        self.assertGreater(result["fixed_missing_A_pair_overlap"], 1)
        self.assertGreaterEqual(result["aligned_clique_core"], 18)

    def test_L4_two(self) -> None:
        result = verifier.l4_two_guard(self.graph)
        self.assertTrue(result["passed"])
        self.assertGreater(result["deletion_checks"], 100_000)


if __name__ == "__main__":
    unittest.main()
