#!/usr/bin/env python3
"""Regression tests for the seventh 2026-07-31 Erdos #809 attack."""

from __future__ import annotations

import unittest

import verify_809_seventh_attack as verifier


class SeventhAttackGuards(unittest.TestCase):
    def test_opposite_core(self) -> None:
        result = verifier.opposite_core_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(
            result["missing_P"] + result["missing_C"],
            result["psi"] + result["cut_edges"],
        )

    def test_opposite_star(self) -> None:
        result = verifier.opposite_star_guard()
        self.assertTrue(result["passed"])
        self.assertLessEqual(
            result["maximum_complement_error"],
            result["kappa"],
        )

    def test_absorption_certificate(self) -> None:
        result = verifier.absorption_certificate_guard()
        self.assertTrue(result["passed"])
        self.assertTrue(result["absorbed"])


if __name__ == "__main__":
    unittest.main()
