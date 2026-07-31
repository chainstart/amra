#!/usr/bin/env python3
"""Regression tests for the first 2026-07-31 Erdős #809 attack."""

from __future__ import annotations

import unittest

import verify_809_first_attack as verifier


class FirstAttackGuards(unittest.TestCase):
    def test_four_bridge_L4(self) -> None:
        result = verifier.l4_guard()
        self.assertTrue(result["passed"])
        self.assertGreater(result["endpoint_pairs_checked"], 0)

    def test_four_bridge_rainbow_colouring(self) -> None:
        result = verifier.colouring_guard()
        self.assertTrue(result["passed"])
        self.assertGreater(result["cycles_checked"], 0)
        self.assertGreater(result["defect"], 0)

    def test_A_orientation_sharpness(self) -> None:
        result = verifier.orientation_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(result["A_endpoint_distance"], 3)
        self.assertEqual(result["outer_endpoint_distance"], 2)
        self.assertEqual(result["outer_codegree"], 2)

    def test_contaminated_A_geodesic(self) -> None:
        result = verifier.contaminated_geodesic_guard(common_neighbors=9)
        self.assertTrue(result["passed"])
        self.assertEqual(result["A_endpoint_distance"], 3)
        self.assertEqual(result["outer_codegree"], 9)
        self.assertFalse(result["specified_edge_in_C7"])


if __name__ == "__main__":
    unittest.main()
