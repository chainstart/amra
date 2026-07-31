#!/usr/bin/env python3
"""Regression tests for the fifth 2026-07-31 Erdős #809 attack."""

from __future__ import annotations

import unittest

import verify_809_fifth_attack as verifier


class FifthAttackGuards(unittest.TestCase):
    def test_zero_shore_rectangle(self) -> None:
        result = verifier.zero_shore_rectangle_guard(h=15)
        self.assertTrue(result["passed"])
        self.assertEqual(result["missing_rectangle"], 225)

    def test_branch_one_bound(self) -> None:
        result = verifier.branch_one_bound_guard()
        self.assertTrue(result["passed"])
        self.assertLessEqual(
            result["coordinate_vertices"],
            result["W_upper_bound"],
        )

    def test_connector_transversal(self) -> None:
        result = verifier.connector_transversal_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(result["transversal_number"], 3)


if __name__ == "__main__":
    unittest.main()
