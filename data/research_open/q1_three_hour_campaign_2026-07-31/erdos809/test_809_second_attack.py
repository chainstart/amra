#!/usr/bin/env python3
"""Regression tests for the second 2026-07-31 Erdős #809 attack."""

from __future__ import annotations

import unittest

import verify_809_second_attack as verifier


class SecondAttackGuards(unittest.TestCase):
    def test_arbitrary_witness_budget_no_go(self) -> None:
        result = verifier.arbitrary_witness_budget_guard()
        self.assertTrue(result["passed"])
        self.assertTrue(result["defect_exceeds_surplus"])
        self.assertLess(
            result["good_colours"], result["BCM_finite_target"]
        )

    def test_canonical_BCM_witness(self) -> None:
        result = verifier.canonical_witness_guard()
        self.assertTrue(result["passed"])
        self.assertTrue(result["maximum_degree_branch_applies"])
        self.assertEqual(result["good_edge_defect"], 0)

    def test_dense_core_compatibility(self) -> None:
        result = verifier.dense_core_compatibility_guard()
        self.assertTrue(result["passed"])
        self.assertGreater(result["edge_pairs_checked"], 0)


if __name__ == "__main__":
    unittest.main()
